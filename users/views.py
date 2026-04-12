from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .forms import JoinRequestForm
from .models import JoinRequest, User


def join_request(request):
    """
    View for non-registered users to submit a membership request.
    Displays a form to collect name, surname, email, and phone number.
    """
    if request.method == 'POST':
        form = JoinRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                'Din anmodning er blevet modtaget! Vi vil kontakte dig hurtigst muligt. / '
                'Your request has been received! We will contact you as soon as possible.'
            )
            return redirect('home:index')
    else:
        form = JoinRequestForm()
    
    return render(request, 'users/join_request.html', {'form': form})


@login_required
def profile_area(request):
    """
    Display the user's private area with profile information and navigation options.
    This view is primarily used for mobile/tablet devices to provide a dedicated page
    instead of a dropdown menu.
    """
    return render(request, 'users/profile_area.html', {
        'user': request.user
    })


@staff_member_required
def admin_dashboard(request):
    """
    Custom admin dashboard with all site management functionalities.
    Displays pending join requests count and provides access to various admin sections.
    """
    pending_requests_count = JoinRequest.objects.filter(status='pending').count()
    
    context = {
        'pending_requests_count': pending_requests_count,
    }
    
    return render(request, 'users/admin_dashboard.html', context)


@staff_member_required
def new_recruits(request):
    """
    View for admins to manage membership join requests.
    Shows all pending, approved, and rejected requests with filtering options.
    """
    status_filter = request.GET.get('status', 'pending')
    
    if status_filter == 'all':
        join_requests = JoinRequest.objects.all()
    else:
        join_requests = JoinRequest.objects.filter(status=status_filter)
    
    pending_count = JoinRequest.objects.filter(status='pending').count()
    
    context = {
        'requests': join_requests,  # Changed key to match template variable
        'status_filter': status_filter,
        'pending_count': pending_count,
    }
    
    return render(request, 'users/new_recruits.html', context)


@staff_member_required
def approve_request(request, request_id):
    """
    Approve a join request and create a new user account.
    Generates a temporary password and sends welcome email.
    """
    join_req = get_object_or_404(JoinRequest, id=request_id)
    
    if join_req.status != 'pending':
        messages.warning(request, 'Denne anmodning er allerede behandlet.')
        return redirect('users:new_recruits')
    
    # Generate password
    password = join_req.generate_password()
    
    # Create new user
    user = User.objects.create_user(
        email=join_req.email,
        password=password,
        nome=join_req.nome,
        cognome=join_req.cognome,
        rango='recruit'
    )
    
    # Update join request status
    join_req.status = 'approved'
    join_req.processed_at = timezone.now()
    join_req.processed_by = request.user
    join_req.save()
    
    # Send approval email
    send_approval_email(join_req, password)
    
    messages.success(
        request,
        f'Anmodning godkendt! {join_req.nome} {join_req.cognome} er nu medlem.'
    )
    
    return redirect('users:new_recruits')


@staff_member_required
def reject_request(request, request_id):
    """
    Reject a join request with a reason.
    Sends rejection email to the applicant.
    """
    join_req = get_object_or_404(JoinRequest, id=request_id)
    
    if join_req.status != 'pending':
        messages.warning(request, 'Denne anmodning er allerede behandlet.')
        return redirect('users:new_recruits')
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('reason', '')
        
        if not rejection_reason:
            messages.error(request, 'Du skal angive en årsag til afvisning.')
            return redirect('users:new_recruits')
        
        # Update join request status
        join_req.status = 'rejected'
        join_req.rejection_reason = rejection_reason
        join_req.processed_at = timezone.now()
        join_req.processed_by = request.user
        join_req.save()
        
        # Send rejection email
        send_rejection_email(join_req)
        
        messages.info(
            request,
            f'Anmodning afvist. {join_req.nome} {join_req.cognome} er blevet informeret.'
        )
        
        return redirect('users:new_recruits')
    
    return redirect('users:new_recruits')


def send_approval_email(join_request, password):
    """Send approval email to new member"""
    subject = 'Velkommen til N.S.O.G.! / Welcome to N.S.O.G.!'
    
    message = f"""
Kære {join_request.nome},

Din anmodning om medlemskab er blevet godkendt!

Log ind på dit private område: {settings.SITE_URL}/accounts/login/

Dine login-oplysninger:
Email: {join_request.email}
Password: {password}

VIGTIGT: Efter dit første login skal du ændre din adgangskode.

Velkommen ombord!
Her er vores Discord-kanal: {settings.DISCORD_LINK if hasattr(settings, 'DISCORD_LINK') else '[Discord link]'}

---

Dear {join_request.nome},

Your membership request has been approved!

Access your private area: {settings.SITE_URL}/accounts/login/

Your login credentials:
Email: {join_request.email}
Password: {password}

IMPORTANT: After your first login, you must change your password.

Welcome aboard!
Here is our Discord channel: {settings.DISCORD_LINK if hasattr(settings, 'DISCORD_LINK') else '[Discord link]'}

---
N.S.O.G. - Crudeles in Proelio
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [join_request.email],
        fail_silently=False,
    )


def send_rejection_email(join_request):
    """Send rejection email to applicant"""
    subject = 'Din anmodning til N.S.O.G. / Your N.S.O.G. application'
    
    message = f"""
Kære {join_request.nome},

Desværre kan vi ikke godkende din anmodning om medlemskab på nuværende tidspunkt.

Årsag: {join_request.rejection_reason}

Du er velkommen til at ansøge igen i fremtiden.

---

Dear {join_request.nome},

Unfortunately, we cannot approve your membership request at this time.

Reason: {join_request.rejection_reason}

You are welcome to apply again in the future.

---
N.S.O.G. - Crudeles in Proelio
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [join_request.email],
        fail_silently=False,
    )
