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

    unread_contacts_count = 0
    if request.path.startswith('/dashboard/') and getattr(request, 'user', None) and request.user.is_authenticated and request.user.is_staff:
        try:
            from contact.models import ContactMessage
            unread_contacts_count = ContactMessage.objects.filter(is_read=False).count()
        except Exception:
            pass

    return {
        'site_settings': settings,
        'profile': profile,
        'unread_contacts_count': unread_contacts_count,
    }
