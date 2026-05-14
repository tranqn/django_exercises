"""
Custom data migration — seed initial categories.
Created with: python manage.py makemigrations --empty bookstore -n seed_categories
"""

from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model("bookstore", "Category")
    categories = [
        ("Fiction", "fiction"),
        ("Non-Fiction", "non-fiction"),
        ("Science", "science"),
        ("Technology", "technology"),
        ("History", "history"),
        ("Biography", "biography"),
        ("Self-Help", "self-help"),
        ("Programming", "programming"),
    ]
    for name, slug in categories:
        Category.objects.get_or_create(name=name, slug=slug)


def remove_categories(apps, schema_editor):
    Category = apps.get_model("bookstore", "Category")
    slugs = ["fiction", "non-fiction", "science", "technology", "history", "biography", "self-help", "programming"]
    Category.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("bookstore", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]