# Shop — E-commerce Order Service

A checkout pipeline: catalog, a session cart, orders, async confirmation
email, payment webhooks, coupons, and a small product API.

## Flow
    browse -> add to session cart -> checkout -> Order created
          -> payment webhook marks Order paid
          -> Celery task emails the confirmation

## Layout
    models.py        Product, Category
    cart.py          session-based Cart
    order_models.py  Order, OrderItem
    checkout.py      order creation from the cart
    tasks.py         Celery confirmation email
    webhooks.py      payment provider webhook
    discounts.py     coupon logic
    api.py           DRF product endpoints