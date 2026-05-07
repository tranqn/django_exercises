from django.views.generic import DetailView
from .models import Book


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_books"] = Book.objects.filter(
            author=self.object.author
        ).exclude(pk=self.object.pk)[:5]
        return context