from rest_framework import serializers
from .models import Market


class MarketBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name"]


class MarketListSerializer(MarketBaseSerializer):
    class Meta(MarketBaseSerializer.Meta):
        fields = MarketBaseSerializer.Meta.fields + ["location", "seller"]


class MarketFullSerializer(MarketBaseSerializer):
    class Meta(MarketBaseSerializer.Meta):
        fields = MarketBaseSerializer.Meta.fields + ["location", "description", "seller", "created_at"]