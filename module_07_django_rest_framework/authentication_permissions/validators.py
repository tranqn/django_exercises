import re
from rest_framework import serializers


def validate_no_html(value):
    """Reject input containing HTML tags."""
    if re.search(r"<[^>]+>", value):
        raise serializers.ValidationError("HTML tags are not allowed.")
    return value


def validate_no_script(value):
    """Reject input containing script tags (XSS prevention)."""
    if re.search(r"<script", value, re.IGNORECASE):
        raise serializers.ValidationError("Script content is not allowed.")
    return value


def validate_safe_filename(value):
    """Ensure filename doesn't contain path traversal."""
    if ".." in value or "/" in value or "\\" in value:
        raise serializers.ValidationError("Invalid filename.")
    return value


# Usage in serializer:
# name = serializers.CharField(validators=[validate_no_html])