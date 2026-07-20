"""Coupon and discount logic."""
from decimal import Decimal
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    percent_off = models.PositiveIntegerField(default=0)  # 0-100
    active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        if not self.active:
            return False
        if self.valid_until and self.valid_until < timezone.now():
            return False
        return True

    def discount_for(self, amount: Decimal) -> Decimal:
        if not self.is_valid():
            return Decimal("0")
        return (amount * self.percent_off / 100).quantize(Decimal("0.01"))

    def __str__(self):
        return self.code