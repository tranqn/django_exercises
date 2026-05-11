from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone


class Command(BaseCommand):
    help = "Clear all expired sessions from the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Show count without deleting",
        )

    def handle(self, *args, **options):
        expired = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired.count()

        if options["dry_run"]:
            self.stdout.write(f"Found {count} expired sessions (dry run).")
        else:
            expired.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {count} expired sessions."))