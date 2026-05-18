from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Market
from .serializers import MarketModelSerializer


@api_view(["GET", "POST"])
def market_list(request):
    if request.method == "GET":
        markets = Market.objects.all()
        serializer = MarketModelSerializer(markets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = MarketModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def market_detail(request, pk):
    try:
        market = Market.objects.get(pk=pk)
    except Market.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MarketModelSerializer(market)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = MarketModelSerializer(market, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        market.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)