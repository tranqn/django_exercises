from rest_framework import serializers
from .models import Market, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "name", "email", "city", "created_at"]
        read_only_fields = ["created_at"]


class MarketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name", "location", "description", "seller", "created_at"]
        read_only_fields = ["created_at"]