from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "site_name",
        "site_title",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "site_name",
        "site_title",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        """Only allow one active SiteSettings instance."""
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)