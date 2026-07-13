"""Custom permissions for the blog API."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Read for anyone; write only for the object's author (or staff)."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff