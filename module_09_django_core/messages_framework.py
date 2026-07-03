"""The messages framework — one-time flash notifications.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/messages/
"""
from django.contrib import messages
from django.shortcuts import redirect


def update_profile(request):
    # ... save the profile ...
    messages.success(request, "Your profile was updated.")
    messages.warning(request, "Remember to verify your email.")
    messages.error(request, "Avatar upload failed.")
    return redirect("profile")


# Template (messages are consumed the first time they are iterated):
#   {% if messages %}
#   <ul class="messages">
#     {% for message in messages %}
#       <li class="{{ message.tags }}">{{ message }}</li>
#     {% endfor %}
#   </ul>
#   {% endif %}

# settings.py:
#   MIDDLEWARE includes 'django.contrib.messages.middleware.MessageMiddleware'
#   from django.contrib.messages import constants
#   MESSAGE_TAGS = {constants.ERROR: "danger"}  # map levels to CSS classes