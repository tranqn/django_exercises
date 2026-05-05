"""
Management command or script to set up default groups and permissions.
Run in Django shell or as a management command.

python manage.py shell < accounts/setup_groups.py
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create groups
editors, _ = Group.objects.get_or_create(name="Editors")
moderators, _ = Group.objects.get_or_create(name="Moderators")
viewers, _ = Group.objects.get_or_create(name="Viewers")

# Assign permissions to groups
# Editors can add and change questions
add_q = Permission.objects.get(codename="add_question")
change_q = Permission.objects.get(codename="change_question")
editors.permissions.add(add_q, change_q)

# Moderators can do everything editors can + delete
delete_q = Permission.objects.get(codename="delete_question")
moderators.permissions.add(add_q, change_q, delete_q)

# Add user to group
# user.groups.add(editors)
# user.has_perm('polls.add_question')  # True

print("Groups created: Editors, Moderators, Viewers")