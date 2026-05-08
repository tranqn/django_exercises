from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    rating = forms.ChoiceField(choices=[(i, f"{i} Stars") for i in range(1, 6)])
    feedback = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}))


class FeedbackView(FormView):
    template_name = "feedback.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Process the form data
        name = form.cleaned_data["name"]
        messages.success(self.request, f"Thank you {name} for your feedback!")
        return super().form_valid(form)