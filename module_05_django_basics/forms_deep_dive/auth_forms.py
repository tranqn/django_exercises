from django import forms
from django.contrib.auth.password_validation import validate_password


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_new_password(self):
        password = self.cleaned_data["new_password"]
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        new_pw = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")
        if new_pw and confirm and new_pw != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data