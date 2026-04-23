from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject", "")
        message = cleaned_data.get("message", "")
        if subject and message and subject.lower() in message.lower():
            raise forms.ValidationError(
                "Message should not just repeat the subject."
            )
        return cleaned_data