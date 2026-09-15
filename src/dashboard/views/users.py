from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from dashboard.forms import DashboardUserCreateForm, DashboardUserEditForm
from dashboard.views.auth import StaffRequiredMixin


class UserListView(StaffRequiredMixin, View):
    """List users with search, role filters, and pagination."""
    template_name = 'dashboard/users/list.html'

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')

        # Filter query
        q = request.GET.get('q', '').strip()
        if q:
            users = users.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )

        # Role filter
        role = request.GET.get('role', '')
        if role == 'superuser':
            users = users.filter(is_superuser=True)
        elif role == 'staff':
            users = users.filter(is_staff=True, is_superuser=False)
        elif role == 'active':
            users = users.filter(is_active=True)
        elif role == 'inactive':
            users = users.filter(is_active=False)

        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'users': page_obj,
            'page_obj': page_obj,
            'total_count': users.count(),
            'search_query': q,
            'current_role': role,
            'active_nav': 'users',
        }
        return render(request, self.template_name, context)


class UserCreateView(StaffRequiredMixin, CreateView):
    """Add a new user."""
    model = User
    form_class = DashboardUserCreateForm
    template_name = 'dashboard/users/form.html'
    success_url = reverse_lazy('dashboard:user_list')

    def form_valid(self, form):
        messages.success(self.request, f"User '{form.cleaned_data['username']}' created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = 'Add New User'
        ctx['active_nav'] = 'users'
        return ctx


class UserUpdateView(StaffRequiredMixin, UpdateView):
    """Edit an existing user."""
    model = User
    form_class = DashboardUserEditForm
    template_name = 'dashboard/users/form.html'
    success_url = reverse_lazy('dashboard:user_list')

    def form_valid(self, form):
        messages.success(self.request, f"User '{self.object.username}' updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = f"Edit User: {self.object.username}"
        ctx['is_edit'] = True
        ctx['target_user'] = self.object
        ctx['active_nav'] = 'users'
        return ctx


class UserDeleteView(StaffRequiredMixin, View):
    """Delete a user with safety checks."""
    template_name = 'dashboard/users/confirm_delete.html'

    def get(self, request, pk):
        user_to_delete = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {
            'target_user': user_to_delete,
            'active_nav': 'users',
        })

    def post(self, request, pk):
        user_to_delete = get_object_or_404(User, pk=pk)

        # Safety Guard 1: Cannot delete oneself
        if user_to_delete.id == request.user.id:
            messages.error(request, "Security violation: You cannot delete your own active administrator account.")
            return redirect('dashboard:user_list')

        # Safety Guard 2: Cannot delete sole superuser
        if user_to_delete.is_superuser:
            superuser_count = User.objects.filter(is_superuser=True).count()
            if superuser_count <= 1:
                messages.error(request, "Action prevented: Cannot delete the only remaining superuser.")
                return redirect('dashboard:user_list')

        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"User '{username}' was permanently removed.")
        return redirect('dashboard:user_list')
