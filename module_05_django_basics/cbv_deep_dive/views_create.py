from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Book


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["title", "author", "pages", "description", "status"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("book-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Book created successfully!")
        return super().form_valid(form)