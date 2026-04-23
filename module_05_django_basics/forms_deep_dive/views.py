from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data["name"]
            messages.success(request, f"Thanks {name}, message sent!")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "forms_demo/contact.html", {"form": form})