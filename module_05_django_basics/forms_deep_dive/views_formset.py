from django.shortcuts import render, redirect
from django.contrib import messages
from .formsets import BookFormSet, BookModelFormSet
from .models import Book


def bulk_book_create(request):
    if request.method == "POST":
        formset = BookFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    title = form.cleaned_data["title"]
                    pages = form.cleaned_data["pages"]
                    Book.objects.create(title=title, pages=pages)
            messages.success(request, "Books created!")
            return redirect("book-list")
    else:
        formset = BookFormSet()
    return render(request, "forms_demo/formset.html", {"formset": formset})


def manage_books(request):
    if request.method == "POST":
        formset = BookModelFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Books updated!")
            return redirect("book-list")
    else:
        formset = BookModelFormSet(queryset=Book.objects.all())
    return render(request, "forms_demo/formset.html", {"formset": formset})