from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from dashboard.views.auth import StaffRequiredMixin
from contact.models import ContactMessage


class ContactListView(StaffRequiredMixin, View):
    """Inbox for contact form submissions."""
    template_name = 'dashboard/contacts/list.html'

    def get(self, request):
        messages_qs = ContactMessage.objects.all().order_by('-created_at')
        unread_count = ContactMessage.objects.filter(is_read=False).count()

        q = request.GET.get('q', '').strip()
        status = request.GET.get('status', '')

        if q:
            messages_qs = messages_qs.filter(
                Q(name__icontains=q) |
                Q(email__icontains=q) |
                Q(subject__icontains=q) |
                Q(message__icontains=q)
            )

        if status == 'unread':
            messages_qs = messages_qs.filter(is_read=False)
        elif status == 'read':
            messages_qs = messages_qs.filter(is_read=True)

        paginator = Paginator(messages_qs, 15)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            'contact_messages': page_obj,
            'page_obj': page_obj,
            'unread_count': unread_count,
            'search_query': q,
            'current_status': status,
            'active_nav': 'contacts',
        })


class ContactDetailView(StaffRequiredMixin, View):
    """View details of a single contact message."""
    template_name = 'dashboard/contacts/detail.html'

    def get(self, request, pk):
        message_obj = get_object_or_404(ContactMessage, pk=pk)
        # Auto-mark as read when opened
        if not message_obj.is_read:
            message_obj.is_read = True
            message_obj.save(update_fields=['is_read'])

        return render(request, self.template_name, {
            'message_obj': message_obj,
            'active_nav': 'contacts',
        })


class ContactToggleReadView(StaffRequiredMixin, View):
    """Toggle read/unread status."""
    def post(self, request, pk):
        message_obj = get_object_or_404(ContactMessage, pk=pk)
        message_obj.is_read = not message_obj.is_read
        message_obj.save(update_fields=['is_read'])
        status_text = "marked as read" if message_obj.is_read else "marked as unread"
        messages.info(request, f"Message from {message_obj.name} was {status_text}.")
        return redirect('dashboard:contact_list')


class ContactDeleteView(StaffRequiredMixin, View):
    """Permanently delete a contact message."""
    def post(self, request, pk):
        message_obj = get_object_or_404(ContactMessage, pk=pk)
        sender = message_obj.name
        message_obj.delete()
        messages.success(request, f"Message from {sender} was permanently deleted.")
        return redirect('dashboard:contact_list')
