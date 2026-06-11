"""
View-level caching and ORM optimization patterns.
"""

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Article


@method_decorator(cache_page(60 * 5), name="dispatch")
class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"

    def get_queryset(self):
        # select_related: FK joins in one query (avoids N+1).
        # prefetch_related: separate query for M2M/reverse FK.
        return (
            Article.objects
            .select_related("author")
            .prefetch_related("tags")
            .only("title", "summary", "author__username")
        )