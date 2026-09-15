from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from dashboard.forms import DashboardLoginForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Verify that the current user is authenticated and is staff."""
    login_url = reverse_lazy('dashboard:login')

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Access restricted. Staff or Administrator privileges required.")
            return redirect('dashboard:login')
        return super().handle_no_permission()


class DashboardLoginView(View):
    """Custom admin login view with dark glassmorphism styling."""
    template_name = 'dashboard/login.html'

    def get(self, request):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return redirect('dashboard:overview')
        form = DashboardLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DashboardLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                    next_url = request.GET.get('next') or request.POST.get('next')
                    return redirect(next_url or 'dashboard:overview')
                else:
                    messages.error(request, "Access denied. Only staff and administrators can access this portal.")
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        return render(request, self.template_name, {'form': form})


class DashboardLogoutView(View):
    """Custom logout view."""
    def get(self, request):
        return self.post(request)

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('dashboard:login')
