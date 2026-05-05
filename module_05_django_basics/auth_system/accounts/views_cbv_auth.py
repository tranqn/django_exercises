from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy


class DashboardView(LoginRequiredMixin, ListView):
    """Only authenticated users can see the dashboard."""
    template_name = "accounts/dashboard.html"
    login_url = "/accounts/login/"

    def get_queryset(self):
        return []


class AdminOnlyView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Only staff users can access this view."""
    template_name = "accounts/admin_panel.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return []