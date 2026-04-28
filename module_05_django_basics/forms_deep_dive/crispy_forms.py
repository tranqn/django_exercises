from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML


class CrispyContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Your Information",
                Row(
                    Column("first_name", css_class="col-md-6"),
                    Column("last_name", css_class="col-md-6"),
                ),
                Row(
                    Column("email", css_class="col-md-6"),
                    Column("phone", css_class="col-md-6"),
                ),
            ),
            Fieldset(
                "Your Message",
                "subject",
                "message",
            ),
            HTML("<hr>"),
            Submit("submit", "Send Message", css_class="btn-primary"),
        )