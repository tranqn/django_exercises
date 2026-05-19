from rest_framework import generics
from .models import Market, Seller
from .serializers import MarketModelSerializer, SellerSerializer


class MarketListCreate(generics.ListCreateAPIView):
    queryset = Market.objects.select_related("seller").all()
    serializer_class = MarketModelSerializer


class MarketRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketModelSerializer


class SellerListCreate(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer