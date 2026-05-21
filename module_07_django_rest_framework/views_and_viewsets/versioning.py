"""
DRF API Versioning

settings.py:
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}

urls.py:
    path('api/<str:version>/', include(router.urls)),
"""

from rest_framework import serializers, viewsets
from .models import Market


class MarketSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name", "location"]


class MarketSerializerV2(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = ["id", "name", "location", "description", "seller_name", "created_at"]

    def get_seller_name(self, obj):
        return obj.seller.name


class MarketVersionedViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()

    def get_serializer_class(self):
        if self.request.version == "v2":
            return MarketSerializerV2
        return MarketSerializerV1