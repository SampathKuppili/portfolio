"""Tests for the common app."""

from django.test import TestCase

from .models import SiteSettings


class SiteSettingsTest(TestCase):
    def test_create_settings(self):
        settings = SiteSettings.objects.create(
            site_name='Test Site', site_title='Test Title',
        )
        self.assertEqual(str(settings), 'Test Site')
        self.assertTrue(settings.is_active)

    def test_context_processor(self):
        SiteSettings.objects.create(
            site_name='Test', site_title='Title', is_active=True,
        )
        response = self.client.get('/')
        self.assertIn('site_settings', response.context)
