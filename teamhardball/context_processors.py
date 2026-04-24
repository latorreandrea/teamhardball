from django.conf import settings


def global_urls(request):
    """Expose globally configured URLs in templates."""
    return {
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
        'DISCORD_URL': getattr(settings, 'DISCORD_URL', ''),
    }
