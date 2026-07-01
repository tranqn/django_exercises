"""Structured JSON logging for production.

Add LOGGING (below) to settings.py. In production, ship stdout to your
aggregator (Loki, CloudWatch, ELK). JSON lines make fields queryable.
"""
import logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"level": "WARNING", "propagate": True},
        "django.db.backends": {"level": "WARNING", "propagate": False},
    },
}


class RequestIDFilter(logging.Filter):
    """Attach a per-request correlation id to every log record."""

    def filter(self, record):
        from .request_context import get_request_id
        record.request_id = get_request_id()
        return True