import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """Validate allowed file extensions."""
    allowed = [".pdf", ".doc", ".docx", ".jpg", ".png", ".gif"]
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed:
        raise ValidationError(f"File type '{ext}' is not allowed. Allowed: {', '.join(allowed)}")


def validate_file_size(value, max_mb=10):
    """Validate maximum file size."""
    max_bytes = max_mb * 1024 * 1024
    if value.size > max_bytes:
        raise ValidationError(f"File too large. Max size: {max_mb}MB.")


def upload_to_path(instance, filename):
    """Generate dynamic upload path: uploads/<model>/<year>/<month>/<filename>"""
    from django.utils import timezone
    now = timezone.now()
    model_name = instance.__class__.__name__.lower()
    return f"uploads/{model_name}/{now.year}/{now.month:02d}/{filename}"


# Model usage:
# class Document(models.Model):
#     file = models.FileField(
#         upload_to=upload_to_path,
#         validators=[validate_file_extension, validate_file_size],
#     )