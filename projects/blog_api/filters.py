"""Filtering, search and ordering for posts."""
import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name="tags__name", lookup_expr="iexact")
    category = django_filters.CharFilter(field_name="category__slug")
    created_after = django_filters.DateFilter(field_name="created", lookup_expr="gte")

    class Meta:
        model = Post
        fields = ["status", "category", "tag", "created_after"]


# In the viewset:
#   filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#   filterset_class = PostFilter
#   search_fields = ["title", "body"]
#   ordering_fields = ["created", "updated"]