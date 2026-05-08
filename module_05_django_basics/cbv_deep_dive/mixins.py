from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin(LoginRequiredMixin):
    """Only allow the owner of an object to access the view."""
    owner_field = "created_by"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if getattr(obj, self.owner_field) != self.request.user:
            raise PermissionDenied("You don't have permission to access this.")
        return obj


class StaffRequiredMixin(LoginRequiredMixin):
    """Only allow staff members."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Staff access required.")
        return super().dispatch(request, *args, **kwargs)


class TitleMixin:
    """Add a title to context data."""
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context