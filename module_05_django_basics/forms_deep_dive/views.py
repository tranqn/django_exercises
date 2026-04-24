from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactForm
from .model_forms import BookForm
from .models import Book


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            messages.success(request, f"Thanks {name}, message sent!")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "forms_demo/contact.html", {"form": form})


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"Book '{book.title}' created!")
            return redirect("book-list")
    else:
        form = BookForm()
    return render(request, "forms_demo/book_form.html", {"form": form, "action": "Create"})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{book.title}' updated!")
            return redirect("book-list")
    else:
        form = BookForm(instance=book)
    return render(request, "forms_demo/book_form.html", {"form": form, "action": "Update"})