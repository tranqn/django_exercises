from rest_framework import serializers
from .models import Market, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "name", "email", "city"]


class MarketDetailSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(), source="seller", write_only=True
    )

    class Meta:
        model = Market
        fields = ["id", "name", "location", "description", "seller", "seller_id", "created_at"]


class MarketWithStatsSerializer(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()
    name_upper = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = ["id", "name", "name_upper", "location", "seller_name"]

    def get_seller_name(self, obj):
        return obj.seller.name if obj.seller else None

    def get_name_upper(self, obj):
        return obj.name.upper()