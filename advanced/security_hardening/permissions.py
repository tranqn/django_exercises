"""Reusable DRF permission classes."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level: only the owner may modify; others read-only."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "owner_id", None) == request.user.id


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff