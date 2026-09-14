"""Tests for contact form and views."""

from django.test import TestCase, Client
from django.urls import reverse

from .forms import ContactForm
from .models import ContactMessage


class ContactModelTest(TestCase):
    def test_create_message(self):
        msg = ContactMessage.objects.create(
            name='Test User', email='test@example.com',
            subject='Hello', message='This is a test message.',
        )
        self.assertEqual(str(msg), 'Test User — Hello')
        self.assertFalse(msg.is_read)

    def test_message_ordering(self):
        msg1 = ContactMessage.objects.create(
            name='First', email='a@b.com', subject='Sub1', message='Msg 1',
        )
        msg2 = ContactMessage.objects.create(
            name='Second', email='a@b.com', subject='Sub2', message='Msg 2',
        )
        messages = ContactMessage.objects.all()
        self.assertEqual(messages[0], msg2)  # newest first


class ContactFormTest(TestCase):
    def test_valid_form(self):
        form = ContactForm(data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a long enough test message.',
            'honeypot': '',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = ContactForm(data={
            'name': 'Test',
            'email': 'not-an-email',
            'subject': 'Test',
            'message': 'A test message content.',
            'honeypot': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_required_fields(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)

    def test_message_too_short(self):
        form = ContactForm(data={
            'name': 'Test',
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'Short',
            'honeypot': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_honeypot_rejection(self):
        form = ContactForm(data={
            'name': 'Bot',
            'email': 'bot@spam.com',
            'subject': 'Spam',
            'message': 'Buy cheap stuff now!!!',
            'honeypot': 'I am a bot',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('honeypot', form.errors)


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_page_get(self):
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Send a Message')

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact:contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Hello',
            'message': 'This is a test message content.',
            'honeypot': '',
        })
        self.assertEqual(response.status_code, 302)  # redirect on success
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_form_invalid(self):
        response = self.client.post(reverse('contact:contact'), {
            'name': '',
            'email': 'bad',
            'subject': '',
            'message': '',
            'honeypot': '',
        })
        self.assertEqual(response.status_code, 200)  # stays on page
        self.assertEqual(ContactMessage.objects.count(), 0)
