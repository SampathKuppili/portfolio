from .models import SiteSettings


def site_context(request):
    """Provide site settings and common data to all templates."""
    from portfolio.services import get_active_profile

    try:
        settings = SiteSettings.objects.filter(is_active=True).first()
    except Exception:
        settings = None

    try:
        profile = get_active_profile()
    except Exception:
        profile = None

    return {
        'site_settings': settings,
        'profile': profile,
    }
