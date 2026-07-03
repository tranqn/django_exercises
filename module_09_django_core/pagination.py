"""Pagination with django.core.paginator.Paginator.

Docs: https://docs.djangoproject.com/en/stable/topics/pagination/
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def article_list(request):
    from myapp.models import Article
    object_list = Article.objects.order_by("-pub_date")
    paginator = Paginator(object_list, 10)  # 10 items per page

    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "article_list.html", {"page_obj": page_obj})


# Template usage:
#   {% for article in page_obj %} ... {% endfor %}
#   Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
#   {% if page_obj.has_next %}
#     <a href="?page={{ page_obj.next_page_number }}">Next</a>
#   {% endif %}

# Class-based shortcut: ListView paginates with `paginate_by = 10`.