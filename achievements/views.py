from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render

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
