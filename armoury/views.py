from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EquipmentForm
from .models import Equipment

User = get_user_model()


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
        messages.success(request, f'Du har lånt "{item.name}".')

    return redirect('armoury:equipment_detail', pk=pk)


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
