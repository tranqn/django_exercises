from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_simple_email(to_email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
    )


def send_html_email(to_email, subject, template_name, context):
    """Send HTML email with plain text fallback."""
    html_content = render_to_string(template_name, context)
    text_content = f"Please view this email in an HTML-capable email client."

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


# Usage with Celery:
# @shared_task
# def send_order_confirmation(order_id, user_email):
#     send_html_email(
#         to_email=user_email,
#         subject="Order Confirmed!",
#         template_name="emails/order_confirmation.html",
#         context={"order_id": order_id},
#     )