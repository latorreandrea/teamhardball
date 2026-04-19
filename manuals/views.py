from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .forms import ChapterFormSet, ManualForm
from .models import Manual


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC VIEWS (login required)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def manual_list(request):
    """Show all manuals the current user is authorised to read."""
    all_manuals = Manual.objects.prefetch_related('chapters')
    accessible  = [m for m in all_manuals if m.is_accessible_by(request.user)]
    return render(request, 'manuals/manual_list.html', {'manuals': accessible})


@login_required
def manual_detail(request, pk):
    """Show all chapters of a manual, ordered, for authorised users."""
    manual = get_object_or_404(Manual, pk=pk)
    if not manual.is_accessible_by(request.user):
        return HttpResponseForbidden(
            'Dit nuværende rang giver ikke adgang til denne manual.'
        )
    chapters = manual.chapters.order_by('order', 'pk')
    return render(request, 'manuals/manual_detail.html', {
        'manual': manual,
        'chapters': chapters,
    })


# ─────────────────────────────────────────────────────────────────────────────
# STAFF-ONLY ADMIN VIEWS
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required
def admin_manual_list(request):
    """List all manuals for staff."""
    manuals = Manual.objects.prefetch_related('chapters').order_by('-created_at')
    return render(request, 'manuals/admin/manual_list.html', {'manuals': manuals})


@staff_member_required
def admin_manual_create(request):
    """Create a new manual with an inline chapter formset."""
    if request.method == 'POST':
        form    = ManualForm(request.POST, request.FILES)
        formset = ChapterFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            manual          = form.save()
            formset.instance = manual
            formset.save()
            messages.success(request, f'Manualen "{manual.title}" er oprettet.')
            return redirect('manuals:admin_manual_list')
    else:
        form    = ManualForm()
        formset = ChapterFormSet()
    return render(request, 'manuals/admin/manual_form.html', {
        'form':    form,
        'formset': formset,
        'action':  'Opret',
    })


@staff_member_required
def admin_manual_edit(request, pk):
    """Edit an existing manual and its chapters."""
    manual = get_object_or_404(Manual, pk=pk)
    if request.method == 'POST':
        form    = ManualForm(request.POST, request.FILES, instance=manual)
        formset = ChapterFormSet(request.POST, request.FILES, instance=manual)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'Manualen "{manual.title}" er opdateret.')
            return redirect('manuals:admin_manual_edit', pk=manual.pk)
    else:
        form    = ManualForm(instance=manual)
        formset = ChapterFormSet(instance=manual)
    return render(request, 'manuals/admin/manual_form.html', {
        'form':    form,
        'formset': formset,
        'action':  'Rediger',
        'manual':  manual,
    })


@staff_member_required
def admin_manual_delete(request, pk):
    """Delete a manual (confirmation page)."""
    manual = get_object_or_404(Manual, pk=pk)
    if request.method == 'POST':
        title = manual.title
        # Delete associated images from storage
        for chapter in manual.chapters.all():
            if chapter.image:
                chapter.image.delete(save=False)
        if manual.cover_image:
            manual.cover_image.delete(save=False)
        manual.delete()
        messages.success(request, f'Manualen "{title}" er slettet.')
        return redirect('manuals:admin_manual_list')
    return render(request, 'manuals/admin/confirm_delete.html', {'manual': manual})
