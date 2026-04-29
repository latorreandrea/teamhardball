from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, get_object_or_404

from .models import AchievementDefinition, UserAchievement


def achievement_catalogue(request):
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
    })


def achievement_public_detail(request, pk):
    definition = get_object_or_404(AchievementDefinition, pk=pk, is_active=True)
    owned = False
    if request.user.is_authenticated:
        owned = UserAchievement.objects.filter(user=request.user, achievement=definition).exists()

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
        'assignees': assignees,
        'total_assignees': total_assignees,
        'extra_count': extra_count,
    })
