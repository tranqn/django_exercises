from rest_framework import serializers
from .models import Market


class MarketListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        markets = [Market(**item) for item in validated_data]
        return Market.objects.bulk_create(markets)


class MarketBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name", "location", "description", "seller"]
        list_serializer_class = MarketListSerializer


# Usage in view:
# @api_view(["POST"])
# def bulk_create_markets(request):
#     serializer = MarketBulkSerializer(data=request.data, many=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)