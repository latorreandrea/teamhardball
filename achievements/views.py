from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from .models import AchievementDefinition, UserAchievement
from .forms import AchievementDefinitionForm, UserAchievementCreateForm, AchievementMembershipForm


@staff_member_required
def admin_dashboard(request):
    definition_count = AchievementDefinition.objects.count()
    active_definition_count = AchievementDefinition.objects.filter(is_active=True).count()
    award_count = UserAchievement.objects.count()
    manual_award_count = award_count

    return render(request, 'achievements/admin/dashboard.html', {
        'definition_count': definition_count,
        'active_definition_count': active_definition_count,
        'award_count': award_count,
        'manual_award_count': manual_award_count,
    })


@staff_member_required
def achievement_definition_list(request):
    definitions = AchievementDefinition.objects.order_by('title')
    return render(request, 'achievements/admin/achievement_definition_list.html', {
        'definitions': definitions,
    })


@staff_member_required
def achievement_definition_create(request):
    if request.method == 'POST':
        form = AchievementDefinitionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achievement definition oprettet.')
            return redirect('achievements:definition_list')
    else:
        form = AchievementDefinitionForm()

    return render(request, 'achievements/admin/achievement_definition_form.html', {
        'form': form,
        'title': 'Opret nyt achievement',
    })


@staff_member_required
def achievement_definition_edit(request, pk):
    definition = get_object_or_404(AchievementDefinition, pk=pk)
    if request.method == 'POST':
        form = AchievementDefinitionForm(request.POST, request.FILES, instance=definition)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achievement definition opdateret.')
            return redirect('achievements:definition_list')
    else:
        form = AchievementDefinitionForm(instance=definition)

    return render(request, 'achievements/admin/achievement_definition_form.html', {
        'form': form,
        'title': f'Rediger achievement: {definition.title}',
    })


@staff_member_required
def achievement_definition_detail(request, pk):
    definition = get_object_or_404(AchievementDefinition, pk=pk)
    assignees = (
        UserAchievement.objects
        .filter(achievement=definition)
        .select_related('user')
        .order_by('user__last_name')
    )

    if request.method == 'POST':
        form = AchievementMembershipForm(request.POST, achievement=definition)
        if form.is_valid():
            achievement = definition
            add_users = form.cleaned_data['add_users']
            remove_users = form.cleaned_data['remove_users']
            created_count = 0
            removed_count = 0

            for user in add_users:
                obj, created = UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement,
                    defaults={
                        'awarded_by': request.user,
                        'reason': '',
                    },
                )
                if created:
                    created_count += 1

            if remove_users:
                removed_count, _ = UserAchievement.objects.filter(
                    achievement=achievement,
                    user__in=remove_users,
                ).delete()

            if created_count:
                messages.success(request, f'{created_count} bruger(e) tilføjet til achievement.')
            if removed_count:
                messages.success(request, f'{removed_count} tilknytninger fjernet.')
            return redirect('achievements:definition_detail', pk=definition.pk)
    else:
        form = AchievementMembershipForm(achievement=definition)

    return render(request, 'achievements/admin/achievement_definition_detail.html', {
        'definition': definition,
        'assignees': assignees,
        'form': form,
    })


@staff_member_required
def achievement_definition_delete(request, pk):
    definition = get_object_or_404(AchievementDefinition, pk=pk)
    if request.method == 'POST':
        definition.delete()
        messages.success(request, 'Achievement definition slettet.')
        return redirect('achievements:definition_list')

    return render(request, 'achievements/admin/achievement_definition_confirm_delete.html', {
        'definition': definition,
    })


@staff_member_required
def user_achievement_list(request):
    awards = (
        UserAchievement.objects
        .select_related('user', 'achievement', 'awarded_by')
        .order_by('-awarded_at')
    )
    return render(request, 'achievements/admin/user_achievement_list.html', {
        'awards': awards,
    })


@staff_member_required
def user_achievement_create(request):
    if request.method == 'POST':
        form = UserAchievementCreateForm(request.POST)
        if form.is_valid():
            achievement = form.cleaned_data['achievement']
            users = form.cleaned_data['users']
            reason = form.cleaned_data['reason']
            created_count = 0
            duplicate_count = 0

            for user in users:
                _, created = UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement,
                    defaults={
                        'awarded_by': request.user,
                        'reason': reason,
                    },
                )
                if created:
                    created_count += 1
                else:
                    duplicate_count += 1

            if created_count:
                messages.success(request, f'{created_count} achievement(s) tildelt.')
            if duplicate_count:
                messages.warning(request, f'{duplicate_count} bruger(e) havde allerede denne achievement.')
            return redirect('achievements:award_list')
    else:
        form = UserAchievementCreateForm()

    return render(request, 'achievements/admin/user_achievement_form.html', {
        'form': form,
        'title': 'Tildel achievement manuelt',
    })


@login_required
def achievement_catalogue(request):
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

    return render(request, 'achievements/user/achievement_list.html', {
        'definitions': definitions,
        'owned_ids': set(owned_ids),
    })


@login_required
def achievement_public_detail(request, pk):
    definition = get_object_or_404(AchievementDefinition, pk=pk, is_active=True)
    owned = UserAchievement.objects.filter(user=request.user, achievement=definition).exists()
    assignee_qs = (
        UserAchievement.objects
        .filter(achievement=definition)
        .select_related('user')
        .order_by('user__last_name', 'user__first_name')
    )
    total_assignees = assignee_qs.count()
    assignees = assignee_qs[:6]
    extra_count = total_assignees - len(assignees)

    return render(request, 'achievements/user/achievement_detail.html', {
        'definition': definition,
        'owned': owned,
        'assignees': assignees,
        'total_assignees': total_assignees,
        'extra_count': extra_count,
    })
