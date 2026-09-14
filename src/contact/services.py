"""Contact service functions."""

import logging

from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger('contact')


def save_contact_message(form):
    """Save a contact message and optionally send an email notification."""
    message = form.save()
    logger.info("New contact message from %s <%s>: %s", message.name, message.email, message.subject)

    # Send email notification (uses console backend in development)
    try:
        send_mail(
            subject=f"[Portfolio] New message: {message.subject}",
            message=(
                f"From: {message.name} <{message.email}>\n\n"
                f"{message.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
    except Exception as e:
        logger.error("Failed to send contact notification email: %s", e)

    return message
