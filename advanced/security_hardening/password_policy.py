"""
AUTH_PASSWORD_VALIDATORS for settings.py plus a custom validator
that rejects passwords containing the username.
"""

from django.core.exceptions import ValidationError

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


class NoUsernameInPasswordValidator:
    def validate(self, password, user=None):
        if user and user.get_username().lower() in password.lower():
            raise ValidationError("Password must not contain your username.")

    def get_help_text(self):
        return "Your password can't contain your username."