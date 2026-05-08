from django.urls import path
from .views_basic import HomeView
from .views_list import BookListView
from .views_detail import BookDetailView
from .views_create import BookCreateView
from .views_update_delete import BookUpdateView, BookDeleteView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
]