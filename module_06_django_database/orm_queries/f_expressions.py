"""
F Expressions — Reference model fields in queries and updates.

from django.db.models import F
"""

# Compare two fields: books where pages > price * 10
# Book.objects.filter(pages__gt=F("price") * 10)

# Increment without race condition
# Book.objects.filter(pk=1).update(pages=F("pages") + 10)

# Bulk update: increase all prices by 10%
# Book.objects.update(price=F("price") * 1.10)

# String concatenation with F + Concat
# from django.db.models.functions import Concat
# from django.db.models import Value
# Author.objects.annotate(
#     full_name=Concat(F("first_name"), Value(" "), F("last_name"))
# )

# Compare dates
# from datetime import timedelta
# Book.objects.filter(updated_at__gt=F("created_at") + timedelta(days=7))