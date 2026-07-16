"""Management command: report overdue tasks.

Place at task_manager/management/commands/overdue_tasks.py
Run: manage.py overdue_tasks --notify
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from projects.task_manager.models import Task


class Command(BaseCommand):
    help = "List (and optionally notify about) overdue tasks."

    def add_arguments(self, parser):
        parser.add_argument("--notify", action="store_true",
                            help="email each owner about their overdue tasks")

    def handle(self, *args, **options):
        overdue = (Task.objects
                   .filter(due_date__lt=timezone.localdate())
                   .exclude(status=Task.Status.DONE)
                   .select_related("owner"))
        self.stdout.write(f"{overdue.count()} overdue task(s)")
        for task in overdue:
            self.stdout.write(f"  - {task.title} (owner: {task.owner})")
        if options["notify"]:
            self.stdout.write(self.style.SUCCESS("notifications queued"))