from django.conf import settings

from finances.models import FinanceViewPermission


def global_urls(request):
    """Expose globally configured URLs in templates."""
    return {
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
        'DISCORD_URL': getattr(settings, 'DISCORD_URL', ''),
        'INSTAGRAM_URL': getattr(settings, 'INSTAGRAM_URL', ''),
        'FACEBOOK_URL': getattr(settings, 'FACEBOOK_URL', ''),
        'can_view_finances': _can_view_finances(request.user),
    }


def _can_view_finances(user):
    """Return True if the user can view the finances section."""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return FinanceViewPermission.objects.filter(user=user).exists()
