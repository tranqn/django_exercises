"""Cart and discount tests."""
import pytest
from decimal import Decimal
from .models import Product, Category

pytestmark = pytest.mark.django_db


@pytest.fixture
def product(db):
    cat = Category.objects.create(name="Books")
    return Product.objects.create(category=cat, name="Django Book",
                                  price=Decimal("39.00"), stock=5)


def test_cart_totals(rf, product):
    from django.contrib.sessions.middleware import SessionMiddleware
    from .cart import Cart
    request = rf.get("/")
    SessionMiddleware(lambda r: None).process_request(request)
    request.session.save()
    cart = Cart(request)
    cart.add(product, qty=2)
    assert cart.total == Decimal("78.00")
    assert len(list(cart)) == 1


def test_coupon_discount():
    from .discounts import Coupon
    c = Coupon(code="SAVE10", percent_off=10, active=True)
    assert c.discount_for(Decimal("78.00")) == Decimal("7.80")