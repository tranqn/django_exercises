from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "pages", "published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Book title"}),
            "pages": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }
        labels = {
            "title": "Book Title",
            "published": "Is Published?",
        }
        help_texts = {
            "pages": "Enter the number of pages.",
        }

    def clean_pages(self):
        pages = self.cleaned_data["pages"]
        if pages > 10000:
            raise forms.ValidationError("A book can't have more than 10,000 pages.")
        return pages