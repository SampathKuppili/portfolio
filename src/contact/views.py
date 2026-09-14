"""Contact view — form display and submission."""

from django.contrib import messages
from django.views.generic import FormView

from .forms import ContactForm
from .services import save_contact_message


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        save_contact_message(form)
        messages.success(self.request, "Thank you! Your message has been sent successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
