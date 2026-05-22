from rest_framework import viewsets
from .models import Market
from .serializers import MarketModelSerializer


class PublicMarketViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only endpoint — no auth required."""
    queryset = Market.objects.filter(seller__isnull=False)
    serializer_class = MarketModelSerializer
    search_fields = ["name", "location"]