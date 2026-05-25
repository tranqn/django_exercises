from rest_framework import viewsets, permissions
from .permissions import IsAdminOrReadOnly


class MarketPermissionViewSet(viewsets.ModelViewSet):
    """Different permissions per action."""

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]