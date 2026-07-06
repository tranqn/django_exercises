"""Validators — reusable field validation.

Docs: https://docs.djangoproject.com/en/stable/ref/validators/
"""
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator,
)
from django.utils.translation import gettext_lazy as _


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _("%(value)s is not an even number"),
            params={"value": value},
        )


# Class-based validator: configurable and serializable into migrations.
slug_validator = RegexValidator(
    regex=r"^[a-z0-9-]+$",
    message="Only lowercase letters, numbers and hyphens are allowed.",
)


# Model usage:
#   class Event(models.Model):
#       seats = models.IntegerField(
#           validators=[MinValueValidator(1), MaxValueValidator(500)]
#       )
#       slug = models.CharField(max_length=50, validators=[slug_validator])
#       attendees = models.IntegerField(validators=[validate_even])
#
# Validators run on form.is_valid() and Model.full_clean(), not bare .save().