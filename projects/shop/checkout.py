"""Create an Order from the session cart inside a transaction."""
from django.db import transaction
from .cart import Cart
from .order_models import Order, OrderItem
from .models import Product
from .tasks import send_order_confirmation


@transaction.atomic
def create_order(request, email):
    cart = Cart(request)
    if not cart.cart:
        raise ValueError("Cart is empty")

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=email,
    )
    for item in cart:
        # Lock the row and re-check stock before committing.
        locked = Product.objects.select_for_update().get(pk=item["product"].pk)
        if locked.stock < item["qty"]:
            raise ValueError(f"Not enough stock for {locked.name}")
        locked.stock -= item["qty"]
        locked.save(update_fields=["stock"])
        OrderItem.objects.create(order=order, product=locked,
                                 price=item["price"], qty=item["qty"])

    cart.clear()
    # Email only after the transaction actually commits.
    transaction.on_commit(lambda: send_order_confirmation.delay(order.id))
    return order