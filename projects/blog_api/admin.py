"""Admin registration for blog models."""
from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status", "category", "created"]
    list_filter = ["status", "category", "created"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["author"]
    date_hierarchy = "created"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Tag)
admin.site.register(Comment)