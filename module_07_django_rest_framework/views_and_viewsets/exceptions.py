from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses.

    settings.py:
    REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'myapp.exceptions.custom_exception_handler',
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "error": True,
            "status_code": response.status_code,
            "message": str(exc),
            "details": response.data,
        }
        response.data = custom_data

    return response