"""Database transactions — atomicity and row locking.

Docs: https://docs.djangoproject.com/en/stable/topics/db/transactions/
"""
from django.db import transaction


@transaction.atomic
def transfer(from_acct, to_acct, amount):
    """All-or-nothing: any exception rolls the whole block back."""
    from_acct.balance -= amount
    from_acct.save()
    to_acct.balance += amount
    to_acct.save()


def process(order_id):
    with transaction.atomic():  # nested atomic() uses savepoints
        from myapp.models import Order
        # select_for_update locks the rows until the transaction ends.
        order = Order.objects.select_for_update().get(pk=order_id)
        order.status = "processing"
        order.save()
        # Run side effects only after a successful commit:
        transaction.on_commit(lambda: print(f"order {order_id} committed"))


# Pitfall: ATOMIC_REQUESTS=True wraps every request in a transaction.