"""Payment provider webhook (Stripe-style)."""
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .order_models import Order


@csrf_exempt
@require_POST
def payment_webhook(request):
    # In production: verify the signature header before trusting the payload.
    try:
        event = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("invalid payload")

    if event.get("type") == "payment_intent.succeeded":
        order_id = event["data"]["object"]["metadata"].get("order_id")
        Order.objects.filter(pk=order_id, status=Order.Status.PENDING).update(
            status=Order.Status.PAID
        )
    return HttpResponse(status=200)