from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import Book


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["title", "author", "pages", "description", "status"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("book-list")

    def form_valid(self, form):
        messages.success(self.request, "Book updated!")
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("book-list")

    def form_valid(self, form):
        messages.success(self.request, f"'{self.object.title}' deleted.")
        return super().form_valid(form)