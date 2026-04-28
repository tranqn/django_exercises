from django.shortcuts import render, redirect
from django.contrib import messages
from .upload_forms import ImageUploadForm


def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES["image"])
            messages.success(request, "Image uploaded!")
            return redirect("upload")
    else:
        form = ImageUploadForm()
    return render(request, "forms_demo/upload.html", {"form": form})