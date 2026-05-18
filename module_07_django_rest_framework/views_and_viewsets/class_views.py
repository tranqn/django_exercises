from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Market
from .serializers import MarketModelSerializer


class MarketList(APIView):
    def get(self, request):
        markets = Market.objects.all()
        serializer = MarketModelSerializer(markets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MarketModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarketDetail(APIView):
    def get_object(self, pk):
        try:
            return Market.objects.get(pk=pk)
        except Market.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        market = self.get_object(pk)
        serializer = MarketModelSerializer(market)
        return Response(serializer.data)

    def put(self, request, pk):
        market = self.get_object(pk)
        serializer = MarketModelSerializer(market, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        market = self.get_object(pk)
        market.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)