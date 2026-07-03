"""Internationalization and localization (i18n / l10n).

Docs: https://docs.djangoproject.com/en/stable/topics/i18n/
Workflow: mark strings -> makemessages -> translate .po -> compilemessages
"""
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy, ngettext


def greeting(count):
    title = _("Welcome to our site")  # translated at call time
    msg = ngettext(
        "You have %(count)d message",
        "You have %(count)d messages",
        count,
    ) % {"count": count}
    return title, msg


# Lazy translation for module-level strings (models, form labels):
#   class Meta:
#       verbose_name = gettext_lazy("article")

# settings.py:
#   USE_I18N = True
#   LANGUAGE_CODE = "en-us"
#   LANGUAGES = [("en", "English"), ("de", "German"), ("vi", "Vietnamese")]
#   MIDDLEWARE += ["django.middleware.locale.LocaleMiddleware"]
#   LOCALE_PATHS = [BASE_DIR / "locale"]

# Templates:
#   {% load i18n %}
#   {% translate "Hello" %}
#   {% blocktranslate %}Hi {{ name }}{% endblocktranslate %}

# Commands:
#   django-admin makemessages -l de
#   django-admin compilemessages