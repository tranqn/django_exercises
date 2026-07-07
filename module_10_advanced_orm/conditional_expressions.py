"""Conditional expressions — Case / When / Value.

Docs: https://docs.djangoproject.com/en/stable/ref/models/conditional-expressions/
"""
from django.db.models import Case, When, Value, CharField, BooleanField, Q


def label_orders():
    from myapp.models import Order

    return Order.objects.annotate(
        tier=Case(
            When(total__gte=1000, then=Value("gold")),
            When(total__gte=100, then=Value("silver")),
            default=Value("bronze"),
            output_field=CharField(),
        ),
        is_priority=Case(
            When(Q(express=True) | Q(total__gte=500), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    )


# Conditional aggregation — count subsets in a single query:
#   from django.db.models import Count
#   Order.objects.aggregate(
#       paid=Count("id", filter=Q(status="paid")),
#       refunded=Count("id", filter=Q(status="refunded")),
#   )