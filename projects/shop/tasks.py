"""Celery tasks for the shop."""
from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_order_confirmation(self, order_id):
    from django.core.mail import send_mail
    from .order_models import Order
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return None
    try:
        send_mail(
            subject=f"Order #{order.pk} confirmed",
            message=f"Thanks! Your total is {order.total}.",
            from_email=None,
            recipient_list=[order.email],
        )
    except Exception as exc:
        raise self.retry(exc=exc)
    return {"order": order_id, "status": "emailed"}