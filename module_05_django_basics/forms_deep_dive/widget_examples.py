"""Django Form Widget Customization Examples."""

from django import forms


class SurveyForm(forms.Form):
    """Demonstrates various Django form widgets."""

    # Text widgets
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"})
    )

    # Choice widgets
    RATING_CHOICES = [(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    CATEGORY_CHOICES = [
        ("tech", "Technology"),
        ("science", "Science"),
        ("art", "Art"),
        ("sports", "Sports"),
    ]
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    # Date/time widgets
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    # Hidden widget
    referrer = forms.CharField(widget=forms.HiddenInput, required=False)