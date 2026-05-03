from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AchievementDefinitionForm
from .models import AchievementDefinition, UserAchievement


def achievement_catalogue(request):
    # --- Admin: handle new-achievement form submission ---
    create_form = None
    if request.user.is_staff:
        if request.method == 'POST':
            create_form = AchievementDefinitionForm(request.POST, request.FILES)
            if create_form.is_valid():
                create_form.save()
                messages.success(request, 'Badge oprettet.')
                return redirect('achievements:achievement_catalogue')
            # Form invalid — fall through so the modal re-opens with errors
        else:
            create_form = AchievementDefinitionForm()

    owned_ids = []
    if request.user.is_authenticated:
        owned_ids = list(
            UserAchievement.objects
            .filter(user=request.user)
            .values_list('achievement_id', flat=True)
        )

    definitions = AchievementDefinition.objects.filter(is_active=True).annotate(
        owned=Case(
            When(id__in=owned_ids, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-owned', 'title')

    return render(request, 'achievements/achievement_list.html', {
        'definitions': definitions,
        'create_form': create_form,
    })


def achievement_public_detail(request, pk):
    # Staff can view and edit inactive badges; regular users only see active ones
    if request.user.is_staff:
        definition = get_object_or_404(AchievementDefinition, pk=pk)
    else:
        definition = get_object_or_404(AchievementDefinition, pk=pk, is_active=True)

    owned = False
    if request.user.is_authenticated:
        owned = UserAchievement.objects.filter(user=request.user, achievement=definition).exists()

    # --- Admin: handle edit form submission ---
    edit_form = None
    if request.user.is_staff:
        if request.method == 'POST':
            edit_form = AchievementDefinitionForm(request.POST, request.FILES, instance=definition)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, f'Badge "{definition.title}" er opdateret.')
                return redirect('achievements:achievement_detail', pk=definition.pk)
            # Form invalid — fall through so the modal re-opens with errors
        else:
            edit_form = AchievementDefinitionForm(instance=definition)

    assignees = (
        UserAchievement.objects
        .filter(achievement=definition)
        .select_related('user')
        .order_by('user__last_name', 'user__first_name')
    )[:12]
    total_assignees = UserAchievement.objects.filter(achievement=definition).count()
    extra_count = max(total_assignees - len(assignees), 0)

    return render(request, 'achievements/achievement_detail.html', {
        'definition': definition,
        'owned': owned,
        'edit_form': edit_form,
        'assignees': assignees,
        'total_assignees': total_assignees,
        'extra_count': extra_count,
    })


@staff_member_required
def achievement_delete(request, pk):
    definition = get_object_or_404(AchievementDefinition, pk=pk)
    if request.method == 'POST':
        title = definition.title
        # Cascade to UserAchievement is handled by on_delete=CASCADE on the FK
        definition.delete()
        messages.success(request, f'Badge "{title}" og alle tilknyttede tildelinger er slettet.')
        return redirect('achievements:achievement_catalogue')
    # Non-POST access falls back to the detail page
    return redirect('achievements:achievement_detail', pk=pk)
