import random
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed database with sample books"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10, help="Number of books")
        parser.add_argument("--clear", action="store_true", help="Clear existing data first")

    def handle(self, *args, **options):
        count = options["count"]

        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing books..."))
            # Book.objects.all().delete()

        titles = [
            "Django for Beginners", "Python Crash Course", "Clean Code",
            "Design Patterns", "The Pragmatic Programmer", "Refactoring",
            "Test-Driven Development", "REST API Design", "Microservices",
            "System Design Interview",
        ]

        for i in range(count):
            title = f"{random.choice(titles)} Vol. {i+1}"
            pages = random.randint(100, 800)
            self.stdout.write(f"  Creating: {title} ({pages} pages)")
            # Book.objects.create(title=title, pages=pages)

        self.stdout.write(self.style.SUCCESS(f"Created {count} books!"))