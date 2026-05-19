from rest_framework import serializers
from .models import Market, Seller


class MarketWithStringRelation(serializers.ModelSerializer):
    """Shows seller's __str__() instead of ID."""
    seller = serializers.StringRelatedField()

    class Meta:
        model = Market
        fields = ["id", "name", "location", "seller"]


class MarketWithHyperlink(serializers.HyperlinkedModelSerializer):
    """Shows seller as a URL link."""
    class Meta:
        model = Market
        fields = ["url", "name", "location", "seller"]


class SellerWithMarkets(serializers.ModelSerializer):
    """Seller with nested list of markets."""
    markets = serializers.StringRelatedField(many=True, read_only=True)
    market_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ["id", "name", "email", "city", "markets", "market_count"]

    def get_market_count(self, obj):
        return obj.markets.count()