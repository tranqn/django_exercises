from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .inline_formsets import ReviewFormSet


def book_with_reviews(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        formset = ReviewFormSet(request.POST, instance=book)
        if formset.is_valid():
            formset.save()
            return redirect("book-detail", pk=book.pk)
    else:
        formset = ReviewFormSet(instance=book)
    return render(request, "forms_demo/book_reviews.html", {
        "book": book,
        "formset": formset,
    })