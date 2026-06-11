"""
Custom management command:

    python manage.py prune_expired_sessions --dry-run

Place under <app>/management/commands/prune_expired_sessions.py.
"""

from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone


class Command(BaseCommand):
    help = "Delete expired sessions from the database session store."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be deleted without deleting.",
        )

    def handle(self, *args, **options):
        expired = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired.count()

        if options["dry_run"]:
            self.stdout.write(f"[dry-run] {count} expired sessions would be removed")
            return

        expired.delete()
        self.stdout.write(self.style.SUCCESS(f"Removed {count} expired sessions"))