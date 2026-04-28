from django import forms


class FileUploadForm(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()


class ImageUploadForm(forms.Form):
    title = forms.CharField(max_length=200)
    image = forms.ImageField(
        help_text="Max 5MB. Accepted formats: JPG, PNG, GIF."
    )

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image file too large (max 5MB).")
        return image