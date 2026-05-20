import django_filters
from .models import Market


class MarketFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(lookup_expr="icontains")
    seller_city = django_filters.CharFilter(field_name="seller__city", lookup_expr="icontains")
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Market
        fields = ["name", "location", "seller"]