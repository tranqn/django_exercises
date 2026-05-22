from rest_framework import viewsets
from .models import Market
from .serializers import MarketModelSerializer
from .nested_serializer import MarketDetailSerializer


class MarketMultiSerializerViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.select_related("seller").all()

    def get_serializer_class(self):
        if self.action == "list":
            return MarketModelSerializer
        if self.action == "retrieve":
            return MarketDetailSerializer
        return MarketModelSerializer