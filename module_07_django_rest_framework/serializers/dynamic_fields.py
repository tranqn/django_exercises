from rest_framework import serializers


class DynamicFieldsMixin:
    """Allow the client to specify which fields to return."""

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            for field_name in set(self.fields) - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


# Usage:
# class MarketSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
#     class Meta:
#         model = Market
#         fields = "__all__"
#
# In views:
# serializer = MarketSerializer(markets, many=True, fields=["id", "name"])