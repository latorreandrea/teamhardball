from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EquipmentForm
from .models import Equipment

User = get_user_model()

# ---------------------------------------------------------------------------
# Rank-aware Full Metal Jacket-style email openers
# ---------------------------------------------------------------------------
import random

_FMJ_TEMPLATES_DA = [
    "Hør her, {rank}! Nogen har sat øjnene på dit udstyr.",
    "Rør dig ikke, {rank}! Dit udstyr er under angreb.",
    "Hvad sker der, {rank}? Dine ejendele tiltrækker opmærksomhed som en rekrut på første dag.",
    "Advarsel, {rank}! En operatør har identificeret dit udstyr som et muligt mål.",
    "Hold fast i hatten, {rank} — en af dine egne har kastet blikket på dit kit.",
]

_FMJ_TEMPLATES_EN = [
    "Listen up, {rank}! Someone has set their sights on your gear.",
    "Don't move, {rank}! Your equipment is under siege.",
    "What's going on, {rank}? Your property is drawing attention like a fresh recruit on day one.",
    "Warning, {rank}! An operator has flagged your equipment as a potential acquisition.",
    "Hold on to your helmet, {rank} — one of your own has eyes on your kit.",
]


def _fmj_openers(owner):
    """Return a tuple (danish_opener, english_opener) using the owner's rank."""
    rank = owner.get_rank_display()
    da   = random.choice(_FMJ_TEMPLATES_DA).format(rank=rank)
    en   = random.choice(_FMJ_TEMPLATES_EN).format(rank=rank)
    return da, en


def _send_borrow_notification(request, item, borrower):
    """Send an email to the equipment owner notifying them of a borrow request."""
    owner = item.owner

    opener_da, opener_en = _fmj_openers(owner)

    # Build absolute URL to borrower's operator detail page.
    borrower_url = request.build_absolute_uri(
        f'/users/{borrower.pk}/operator/'
    )
    discord_url  = getattr(settings, 'DISCORD_URL', '')

    subject = f'[N.S.O.G.] Låneforespørgsel på "{item.name}" / Borrow request for "{item.name}"'

    body = f"""\
{opener_da}

Operatør {borrower.get_rank_display()} {borrower.first_name} {borrower.last_name} har anmodet om at låne dit udstyr: {item.name}.

Kontakt vedkommende:
  Telefon : {borrower.phone if borrower.phone else '—'}
  E-mail  : {borrower.email}
  Profil  : {borrower_url}

I kan også finde hinanden på Discord: {discord_url}

— N.S.O.G. Automated Systems · Crudeles in Proelio

---

{opener_en}

Operator {borrower.get_rank_display()} {borrower.first_name} {borrower.last_name} has requested to borrow your equipment: {item.name}.

Contact them at:
  Phone  : {borrower.phone if borrower.phone else '—'}
  E-mail : {borrower.email}
  Profile: {borrower_url}

You can also reach each other on Discord: {discord_url}

— N.S.O.G. Automated Systems · Crudeles in Proelio
"""
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [owner.email],
            fail_silently=True,
        )
    except Exception:
        pass


@login_required
def equipment_list(request):
    """Show all registered equipment with optional search and category filter."""
    qs = Equipment.objects.select_related('owner', 'borrowed_by')

    query    = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        qs = qs.filter(
            Q(name__icontains=query) |
            Q(owner__first_name__icontains=query) |
            Q(owner__last_name__icontains=query)
        )

    if category:
        qs = qs.filter(category=category)

    return render(request, 'armoury/equipment_list.html', {
        'equipment_list': qs,
        'categories':     Equipment.CATEGORY_CHOICES,
        'query':          query,
        'active_category': category,
    })


@login_required
def equipment_detail(request, pk):
    """Show the detail page for a single piece of equipment."""
    item = get_object_or_404(
        Equipment.objects.select_related('owner', 'borrowed_by'),
        pk=pk,
    )
    return render(request, 'armoury/equipment_detail.html', {'item': item})


@login_required
def equipment_create(request):
    """Register a new piece of equipment. Owner is set to the logged-in user."""
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment       = form.save(commit=False)
            equipment.owner = request.user
            equipment.save()
            messages.success(request, f'"{equipment.name}" er nu registreret i våbenkammeret.')
            return redirect('armoury:equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()

    return render(request, 'armoury/equipment_form.html', {
        'form':   form,
        'action': 'Registrer',
    })


@login_required
def equipment_edit(request, pk):
    """Edit an existing piece of equipment. Only the owner may edit."""
    item = get_object_or_404(Equipment, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.name}" er opdateret.')
            return redirect('armoury:equipment_detail', pk=item.pk)
    else:
        form = EquipmentForm(instance=item)

    return render(request, 'armoury/equipment_form.html', {
        'form':   form,
        'item':   item,
        'action': 'Rediger',
    })


@login_required
def equipment_borrow(request, pk):
    """Mark equipment as borrowed by the current user."""
    if request.method != 'POST':
        return redirect('armoury:equipment_detail', pk=pk)

    item = get_object_or_404(Equipment, pk=pk)

    if item.owner == request.user:
        messages.warning(request, 'Du kan ikke låne dit eget udstyr.')
    elif not item.is_available:
        messages.warning(request, 'Dette udstyr er allerede udlånt.')
    else:
        item.borrowed_by = request.user
        item.save(update_fields=['borrowed_by'])
        _send_borrow_notification(request, item, request.user)
        messages.success(request, f'Du har lånt "{item.name}". Ejeren er blevet underrettet.')

    return redirect('armoury:equipment_detail', pk=pk)


@login_required
def equipment_delete(request, pk):
    """Delete a piece of equipment. Only the owner may delete it."""
    item = get_object_or_404(Equipment, pk=pk, owner=request.user)

    if request.method == 'POST':
        name = item.name
        item.delete()
        messages.success(request, f'"{name}" er slettet fra våbenkammeret.')
        return redirect('armoury:equipment_list')

    # GET: show confirmation page
    return render(request, 'armoury/equipment_confirm_delete.html', {'item': item})


@login_required
def equipment_return(request, pk):
    """Mark borrowed equipment as returned."""
    if request.method != 'POST':
        return redirect('armoury:equipment_detail', pk=pk)

    item = get_object_or_404(Equipment, pk=pk)

    if item.borrowed_by != request.user:
        messages.warning(request, 'Du har ikke dette udstyr til låns.')
    else:
        item.borrowed_by = None
        item.save(update_fields=['borrowed_by'])
        messages.success(request, f'"{item.name}" er returneret.')

    return redirect('armoury:equipment_detail', pk=pk)
