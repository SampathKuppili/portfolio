from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(
        max_length=150
    )

    site_title = models.CharField(
        max_length=200
    )

    meta_description = models.TextField(
        blank=True
    )

    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
        ordering = ["-updated_at"]