"""Formsets and model formsets (django.forms.formset_factory).

Docs: https://docs.djangoproject.com/en/stable/topics/forms/formsets/
Formsets manage multiple copies of the same form on a single page.
"""
from django import forms
from django.forms import formset_factory, modelformset_factory


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=100)
    pub_date = forms.DateField()


# A formset of 3 empty ArticleForms
ArticleFormSet = formset_factory(ArticleForm, extra=3, can_delete=True)


def manage_articles(request):
    from django.shortcuts import render
    if request.method == "POST":
        formset = ArticleFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                # cleaned_data is {} for the empty "extra" forms
                if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                    print(form.cleaned_data["title"])
    else:
        formset = ArticleFormSet()
    return render(request, "articles.html", {"formset": formset})


# Model formset — edit several existing rows at once:
# AuthorFormSet = modelformset_factory(Author, fields=["name", "email"], extra=1)
# formset = AuthorFormSet(queryset=Author.objects.all())