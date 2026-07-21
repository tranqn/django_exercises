# Shop — Architecture & Order Flow

## Components
| Concern | Module |
|---|---|
| Catalog | models.py (Product, Category) |
| Cart | cart.py (session-backed) |
| Orders | order_models.py (Order, OrderItem) |
| Checkout | checkout.py (atomic, locks stock) |
| Async email | tasks.py (Celery) |
| Payments | webhooks.py |
| Discounts | discounts.py (Coupon) |
| API | api.py (DRF) |

## Order lifecycle
    pending --(payment webhook)--> paid --(fulfilment)--> shipped
        \--(timeout / failure)--> cancelled

## Why these choices
- The cart lives in the session so anonymous users can shop.
- create_order() runs in a transaction and uses select_for_update() so two
  buyers cannot oversell the last unit.
- The confirmation email is sent via transaction.on_commit() so it never
  fires for an order that gets rolled back.

## Exercises
1. Add a stock-reservation timeout that cancels unpaid orders after 30 min.
2. Merge a guest cart into the user's cart on login.
3. Verify the webhook signature before trusting the payload.
4. Add an idempotency key so a retried webhook can't double-process an order.