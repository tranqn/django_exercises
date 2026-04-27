"""Example views using Django messages framework."""

from django.shortcuts import redirect
from django.contrib import messages


def example_messages(request):
    """Demonstrate different message levels."""
    messages.debug(request, "Debug message — only shown in dev.")
    messages.info(request, "This is an informational message.")
    messages.success(request, "Operation completed successfully!")
    messages.warning(request, "Warning: this action cannot be undone.")
    messages.error(request, "Error: something went wrong.")
    return redirect("index")