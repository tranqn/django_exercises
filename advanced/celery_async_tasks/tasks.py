import time
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_email, username):
    """Send welcome email asynchronously."""
    # send_mail(subject="Welcome!", message=f"Hello {username}!", ...)
    logger.info(f"Welcome email sent to {user_email}")
    return {"status": "sent", "email": user_email}


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_data_export(self, export_id):
    """Long-running export with retry logic."""
    try:
        logger.info(f"Processing export {export_id}...")
        time.sleep(5)  # Simulate heavy work
        return {"status": "completed", "export_id": export_id}
    except Exception as exc:
        logger.error(f"Export {export_id} failed: {exc}")
        raise self.retry(exc=exc)


@shared_task
def generate_report(report_type, date_range):
    """Generate a report in the background."""
    logger.info(f"Generating {report_type} report for {date_range}")
    # Heavy computation here...
    return {"report_type": report_type, "status": "generated"}