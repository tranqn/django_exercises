from django.views.generic import TemplateView, RedirectView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Welcome to Django Exercise"
        return context


class OldPageRedirect(RedirectView):
    pattern_name = "home"
    permanent = True


class ExternalRedirect(RedirectView):
    url = "https://docs.djangoproject.com/"