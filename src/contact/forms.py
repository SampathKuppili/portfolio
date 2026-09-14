from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Public contact form with honeypot spam protection."""

    # Honeypot field — should remain empty; bots tend to fill it
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
        label='',
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name',
                'id': 'contact-name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
                'id': 'contact-email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject',
                'id': 'contact-subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Your message...',
                'rows': 5,
                'id': 'contact-message',
            }),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get('honeypot', '')
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message) < 10:
            raise forms.ValidationError("Please write at least 10 characters.")
        return message
