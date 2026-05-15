from rest_framework import serializers


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    seller = serializers.IntegerField()

    def create(self, validated_data):
        from .models import Market
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.location = validated_data.get("location", instance.location)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance