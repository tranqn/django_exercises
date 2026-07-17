"""Session-based shopping cart."""
from decimal import Decimal
from .models import Product

CART_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_KEY, {})

    def add(self, product, qty=1, override=False):
        pid = str(product.id)
        item = self.cart.setdefault(pid, {"qty": 0, "price": str(product.price)})
        item["qty"] = qty if override else item["qty"] + qty
        self.save()

    def remove(self, product):
        self.cart.pop(str(product.id), None)
        self.save()

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        for product in products:
            item = self.cart[str(product.id)]
            yield {
                "product": product,
                "qty": item["qty"],
                "price": Decimal(item["price"]),
                "total": Decimal(item["price"]) * item["qty"],
            }

    @property
    def total(self):
        return sum(Decimal(i["price"]) * i["qty"] for i in self.cart.values())

    def clear(self):
        self.session.pop(CART_SESSION_KEY, None)
        self.session.modified = True