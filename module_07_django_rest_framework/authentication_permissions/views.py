from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}!"})


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def public_view(request):
    return Response({"message": "This is public!"})


@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def admin_only_view(request):
    return Response({"message": "Admin access granted."})