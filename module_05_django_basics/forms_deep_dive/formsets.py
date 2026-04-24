from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import Book


class SimpleBookForm(forms.Form):
    title = forms.CharField(max_length=200)
    pages = forms.IntegerField(min_value=1)


# Create a formset with 3 extra blank forms
BookFormSet = formset_factory(SimpleBookForm, extra=3)

# ModelFormSet — directly linked to the Book model
BookModelFormSet = modelformset_factory(
    Book,
    fields=["title", "pages", "published"],
    extra=2,
    can_delete=True,
)