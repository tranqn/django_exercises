"""
Seed deterministic demo data for local development and CI fixtures:

    python manage.py seed_demo_data --users 10
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo users for local development."

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=5)

    def handle(self, *args, **options):
        created = 0
        for i in range(options["users"]):
            _, was_created = User.objects.get_or_create(
                username=f"demo_user_{i}",
                defaults={"email": f"demo_user_{i}@example.com"},
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new users"))