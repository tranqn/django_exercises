from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Market, Seller
from .serializers import MarketModelSerializer, SellerSerializer
from .pagination import StandardPagination


class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.select_related("seller").all()
    serializer_class = MarketModelSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "location", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["-created_at"]

    @action(detail=True, methods=["get"])
    def seller_info(self, request, pk=None):
        market = self.get_object()
        serializer = SellerSerializer(market.seller)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        recent = Market.objects.order_by("-created_at")[:5]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "city"]