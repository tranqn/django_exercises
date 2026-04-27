"""
Custom context processors — make variables available in ALL templates.

Add to settings.py TEMPLATES OPTIONS context_processors:
    'forms_demo.context_processors.site_settings',
"""


def site_settings(request):
    return {
        "SITE_NAME": "Django Exercise",
        "SITE_VERSION": "1.0",
        "CURRENT_YEAR": 2026,
    }