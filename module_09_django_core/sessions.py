"""The sessions framework (django.contrib.sessions).

Docs: https://docs.djangoproject.com/en/stable/topics/http/sessions/
"""


def set_cart(request):
    # Sessions behave like a dict hanging off the request.
    request.session["cart"] = {"item_42": 2}
    request.session["last_seen"] = "2026-06-30"
    request.session.set_expiry(0)  # expire when the browser closes


def read_cart(request):
    cart = request.session.get("cart", {})
    # Mutating a nested object in place requires marking the session dirty:
    cart["item_7"] = 1
    request.session.modified = True
    return cart


def clear_cart(request):
    request.session.pop("cart", None)


# settings.py:
#   SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
#   SESSION_COOKIE_AGE = 1209600   # 2 weeks, in seconds
#   SESSION_COOKIE_SECURE = True   # send only over HTTPS
# Purge expired rows periodically: manage.py clearsessions