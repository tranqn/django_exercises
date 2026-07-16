"""Dashboard view with per-status task counts."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.views.generic import TemplateView

from .models import Task


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(owner=self.request.user)
        ctx["stats"] = tasks.aggregate(
            total=Count("id"),
            todo=Count("id", filter=Q(status="todo")),
            doing=Count("id", filter=Q(status="doing")),
            done=Count("id", filter=Q(status="done")),
        )
        ctx["recent"] = tasks[:5]
        return ctx