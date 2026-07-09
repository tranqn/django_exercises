"""Bulk operations and query performance.

Docs: https://docs.djangoproject.com/en/stable/ref/models/querysets/
"""


def fast_inserts():
    from myapp.models import Tag
    # One round-trip instead of N:
    Tag.objects.bulk_create(
        [Tag(name=f"tag{i}") for i in range(1000)], batch_size=500
    )


def fast_updates():
    from myapp.models import Product
    products = list(Product.objects.all())
    for p in products:
        p.price *= 1.1
    Product.objects.bulk_update(products, ["price"], batch_size=500)


# Avoid the N+1 problem:
#   Book.objects.select_related("author")        # forward FK -> JOIN
#   Author.objects.prefetch_related("book_set")  # reverse FK -> 2 queries
#
# Read-only speedups:
#   .values() / .values_list()   # dicts/tuples, skip model instances
#   .iterator()                  # stream large result sets with low memory
#   .only(...) / .defer(...)     # load a subset of columns
#   .exists() / .count()         # cheaper than len(list(qs))