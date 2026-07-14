import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AdminExpenseRequestForm,
    ClarificationResponseForm,
    ExpenseRequestForm,
    TransactionForm,
)
from .models import ExpenseRequest, FinanceViewPermission, Transaction

User = get_user_model()
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Permission helpers
# ---------------------------------------------------------------------------

def can_view_finances(user):
    """Return True if the user is staff OR has been granted finance view permission."""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return FinanceViewPermission.objects.filter(user=user).exists()


def finance_access_required(view_func):
    """Decorator: require staff OR finance view permission."""
    decorated = user_passes_test(
        can_view_finances,
        login_url='/',
        redirect_field_name=None,
    )
    return decorated(view_func)


# ---------------------------------------------------------------------------
# Admin / staff views — transactions
# ---------------------------------------------------------------------------

@finance_access_required
def transaction_list(request):
    """Show all transactions with running balance, search, type filter, and
    column sorting (sort=created_at|entry_type|amount|description, order=asc|desc).
    """
    qs = Transaction.objects.select_related(
        'recorded_by', 'incurred_by', 'expense_request',
    )

    # Filters
    entry_type = request.GET.get('type', '').strip()
    query = request.GET.get('q', '').strip()

    if entry_type in ('income', 'expense'):
        qs = qs.filter(entry_type=entry_type)

    if query:
        qs = qs.filter(
            Q(description__icontains=query) |
            Q(incurred_by__first_name__icontains=query) |
            Q(incurred_by__last_name__icontains=query) |
            Q(note__icontains=query)
        )

    # Sorting
    sort_by = request.GET.get('sort', '').strip()
    order = request.GET.get('order', 'asc').strip()
    ALLOWED_SORTS = {'created_at', 'entry_type', 'amount', 'description'}
    if sort_by in ALLOWED_SORTS:
        direction = '-' if order == 'desc' else ''
        qs = qs.order_by(f'{direction}{sort_by}')
    else:
        # Default: newest first
        qs = qs.order_by('-created_at')

    # Balance (calculated on the *filtered* set, not the full DB)
    totals = qs.aggregate(
        total_income=Sum('amount', filter=Q(entry_type=Transaction.ENTRY_INCOME)),
        total_expense=Sum('amount', filter=Q(entry_type=Transaction.ENTRY_EXPENSE)),
    )
    income = totals['total_income'] or 0
    expense = totals['total_expense'] or 0
    balance = income - expense

    return render(request, 'finances/admin/transaction_list.html', {
        'transactions': qs,
        'total_income': income,
        'total_expense': expense,
        'balance': balance,
        'active_type': entry_type,
        'query': query,
        'sort_by': sort_by,
        'order': order,
    })


@user_passes_test(lambda u: u.is_staff)
def transaction_create(request):
    """Create a new income or expense transaction."""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.recorded_by = request.user
            transaction.save()
            messages.success(
                request,
                f'Transaktion "{transaction.description}" er registreret.',
            )
            return redirect('finances:transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'finances/admin/transaction_form.html', {
        'form': form,
        'action': 'Registrer',
    })


# ---------------------------------------------------------------------------
# Admin / staff views — expense requests
# ---------------------------------------------------------------------------

@user_passes_test(lambda u: u.is_staff)
def admin_request_list(request):
    """List expense requests with status filter for admin processing."""
    status_filter = request.GET.get('status', 'pending')

    if status_filter == 'all':
        requests_qs = ExpenseRequest.objects.select_related('user', 'processed_by').all()
    else:
        requests_qs = ExpenseRequest.objects.filter(
            status=status_filter,
        ).select_related('user', 'processed_by')

    pending_count = ExpenseRequest.objects.filter(
        status=ExpenseRequest.STATUS_PENDING,
    ).count()

    return render(request, 'finances/admin/request_list.html', {
        'requests': requests_qs,
        'status_filter': status_filter,
        'pending_count': pending_count,
    })


@user_passes_test(lambda u: u.is_staff)
def admin_request_action(request, pk):
    """Approve, reject, or request clarification for an expense request."""
    expense_req = get_object_or_404(
        ExpenseRequest.objects.select_related('user'),
        pk=pk,
    )

    if expense_req.status not in (ExpenseRequest.STATUS_PENDING, ExpenseRequest.STATUS_CLARIFICATION):
        messages.warning(request, 'Denne anmodning er allerede behandlet.')
        return redirect('finances:admin_request_list')

    if request.method == 'POST':
        form = AdminExpenseRequestForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            message = form.cleaned_data['message']

            expense_req.processed_at = timezone.now()
            expense_req.processed_by = request.user

            if action == 'approve':
                expense_req.status = ExpenseRequest.STATUS_APPROVED
                expense_req.admin_message = message
                expense_req.save()
                messages.success(
                    request,
                    f'Anmodning fra {expense_req.user.get_full_name()} er godkendt.',
                )
            elif action == 'reject':
                expense_req.status = ExpenseRequest.STATUS_REJECTED
                expense_req.admin_message = message
                expense_req.save()
                _send_request_rejection_email(request, expense_req)
                messages.info(
                    request,
                    f'Anmodning fra {expense_req.user.get_full_name()} er afvist.',
                )
            elif action == 'clarify':
                expense_req.status = ExpenseRequest.STATUS_CLARIFICATION
                expense_req.admin_message = message
                expense_req.save()
                _send_clarification_email(request, expense_req)
                messages.info(
                    request,
                    f'Afklaring anmodet fra {expense_req.user.get_full_name()}.',
                )

            return redirect('finances:admin_request_list')
    else:
        form = AdminExpenseRequestForm()

    return render(request, 'finances/admin/request_action.html', {
        'form': form,
        'expense_request': expense_req,
    })


# ---------------------------------------------------------------------------
# Admin / staff views — permissions
# ---------------------------------------------------------------------------

@user_passes_test(lambda u: u.is_staff)
def permission_list(request):
    """List users with finance view permission, and allow granting/revoking."""
    permissions = FinanceViewPermission.objects.select_related('user', 'granted_by').all()
    permitted_ids = set(permissions.values_list('user_id', flat=True))

    # Users that can be granted permission (active, not staff, not already permitted)
    available_users = User.objects.filter(
        is_active=True, is_staff=False,
    ).exclude(id__in=permitted_ids).order_by('last_name', 'first_name')

    return render(request, 'finances/admin/permission_list.html', {
        'permissions': permissions,
        'available_users': available_users,
    })


@user_passes_test(lambda u: u.is_staff)
def permission_grant(request):
    """Grant finance view permission to a user (POST only)."""
    if request.method != 'POST':
        return redirect('finances:permission_list')

    user_id = request.POST.get('user_id')
    if not user_id:
        messages.error(request, 'Vælg en bruger.')
        return redirect('finances:permission_list')

    user = get_object_or_404(User, id=user_id, is_active=True)

    if FinanceViewPermission.objects.filter(user=user).exists():
        messages.warning(request, f'{user.get_full_name()} har allerede adgang.')
    else:
        FinanceViewPermission.objects.create(user=user, granted_by=request.user)
        messages.success(
            request,
            f'{user.get_full_name()} har nu adgang til økonomien.',
        )

    return redirect('finances:permission_list')


@user_passes_test(lambda u: u.is_staff)
def permission_revoke(request, pk):
    """Revoke finance view permission (POST only)."""
    if request.method != 'POST':
        return redirect('finances:permission_list')

    perm = get_object_or_404(FinanceViewPermission, pk=pk)
    name = perm.user.get_full_name()
    perm.delete()
    messages.info(request, f'{name}s adgang til økonomien er blevet tilbagekaldt.')

    return redirect('finances:permission_list')


# ---------------------------------------------------------------------------
# Member views — expense requests
# ---------------------------------------------------------------------------

@login_required
def expense_request_create(request):
    """Allow logged-in members to submit a new spending request."""
    if request.method == 'POST':
        form = ExpenseRequestForm(request.POST)
        if form.is_valid():
            expense_req = form.save(commit=False)
            expense_req.user = request.user
            expense_req.save()
            messages.success(
                request,
                'Din udgiftsanmodning er indsendt og afventer godkendelse. '
                'Du får besked, når den er behandlet. / '
                'Your expense request has been submitted and is pending approval. '
                'You will be notified when it has been processed.',
            )
            return redirect('finances:my_requests')
    else:
        form = ExpenseRequestForm()

    return render(request, 'finances/expense_request_form.html', {
        'form': form,
    })


@login_required
def my_requests(request):
    """Show the logged-in user's own expense requests."""
    requests_qs = ExpenseRequest.objects.filter(
        user=request.user,
    ).order_by('-created_at')

    return render(request, 'finances/my_requests.html', {
        'requests': requests_qs,
    })


@login_required
def request_clarify(request, pk):
    """Allow a member to respond to an admin's clarification request."""
    expense_req = get_object_or_404(
        ExpenseRequest,
        pk=pk,
        user=request.user,
        status=ExpenseRequest.STATUS_CLARIFICATION,
    )

    if request.method == 'POST':
        form = ClarificationResponseForm(request.POST, instance=expense_req)
        if form.is_valid():
            # Save the response and reset status to pending for admin review
            expense_req = form.save(commit=False)
            expense_req.status = ExpenseRequest.STATUS_PENDING
            expense_req.save()
            messages.success(
                request,
                'Dit svar er sendt. Din anmodning er nu til gennemgang igen. / '
                'Your response has been sent. Your request is now under review again.',
            )
            return redirect('finances:my_requests')
    else:
        form = ClarificationResponseForm(instance=expense_req)

    return render(request, 'finances/request_clarify.html', {
        'form': form,
        'expense_request': expense_req,
    })


# ---------------------------------------------------------------------------
# Email helpers (bilingual DA/EN)
# ---------------------------------------------------------------------------

def _send_clarification_email(request, expense_req):
    """Send bilingual email asking the member for more details."""
    subject = (
        f'[N.S.O.G.] Afklaring på din udgiftsanmodning / '
        f'Clarification on your expense request'
    )
    clarify_url = request.build_absolute_uri(
        f'/oekonomi/request/{expense_req.pk}/clarify/'
    )

    body = f"""\
Kære {expense_req.user.first_name},

Administratoren har brug for flere oplysninger om din udgiftsanmodning:

  Beløb      : {expense_req.amount} kr.
  Beskrivelse: {expense_req.description}

Besked fra admin:
{expense_req.admin_message}

Du kan svare på denne anmodning her:
{clarify_url}

— N.S.O.G. Automated Systems · Crudeles in Proelio

---

Dear {expense_req.user.first_name},

The administrator needs more information regarding your expense request:

  Amount     : {expense_req.amount} kr.
  Description: {expense_req.description}

Message from the admin:
{expense_req.admin_message}

You can respond to this request here:
{clarify_url}

— N.S.O.G. Automated Systems · Crudeles in Proelio
"""
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [expense_req.user.email],
            fail_silently=True,
        )
    except Exception:
        pass


def _send_request_rejection_email(request, expense_req):
    """Send bilingual email notifying the member that their request was rejected."""
    subject = (
        f'[N.S.O.G.] Din udgiftsanmodning er blevet afvist / '
        f'Your expense request has been rejected'
    )

    body = f"""\
Kære {expense_req.user.first_name},

Din udgiftsanmodning på {expense_req.amount} kr. er blevet afvist.

Beskrivelse: {expense_req.description}

{f'Begrundelse: {expense_req.admin_message}' if expense_req.admin_message else ''}

Du kan indsende en ny anmodning, hvis du har brug for hjælp.
Kontakt en administrator, hvis du har spørgsmål.

— N.S.O.G. Automated Systems · Crudeles in Proelio

---

Dear {expense_req.user.first_name},

Your expense request for {expense_req.amount} kr. has been rejected.

Description: {expense_req.description}

{f'Reason: {expense_req.admin_message}' if expense_req.admin_message else ''}

You may submit a new request if you need help.
Contact an administrator if you have any questions.

— N.S.O.G. Automated Systems · Crudeles in Proelio
"""
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [expense_req.user.email],
            fail_silently=True,
        )
    except Exception:
        pass