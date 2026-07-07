"""Database functions — push computation into SQL.

Docs: https://docs.djangoproject.com/en/stable/ref/models/database-functions/
"""
from django.db.models import Value
from django.db.models.functions import (
    Coalesce, Concat, Lower, Length, TruncMonth,
)


def examples():
    from myapp.models import Customer, Order

    # Concat + Lower: build a normalized full name in the DB.
    Customer.objects.annotate(
        full_name=Lower(Concat("first_name", Value(" "), "last_name")),
    )

    # Coalesce: first non-null value (handy for defaults).
    Order.objects.annotate(amount=Coalesce("discount_total", "total"))

    # Length: filter by a computed string length.
    Customer.objects.annotate(n=Length("username")).filter(n__gt=20)

    # TruncMonth: bucket time-series rows by month.
    Order.objects.annotate(month=TruncMonth("created")).values("month")