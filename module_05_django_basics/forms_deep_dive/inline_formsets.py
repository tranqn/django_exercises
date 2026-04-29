from django.forms import inlineformset_factory
from .models import Book, Review

# Inline formset: manage Reviews within a Book form
ReviewFormSet = inlineformset_factory(
    Book,
    Review,
    fields=["reviewer_name", "rating", "comment"],
    extra=2,
    can_delete=True,
    min_num=0,
    validate_min=True,
)