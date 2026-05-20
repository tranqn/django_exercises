from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Market, Seller
from .serializers import MarketModelSerializer, SellerSerializer


class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.select_related("seller").all()
    serializer_class = MarketModelSerializer

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