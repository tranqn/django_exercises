from django.contrib import admin
from django.utils.html import format_html


# Inline for reviews inside book admin
class ReviewInline(admin.TabularInline):
    model = None  # Review model
    extra = 1
    readonly_fields = ["created_at"]


@admin.action(description="Mark selected as published")
def make_published(modeladmin, request, queryset):
    count = queryset.update(status="published")
    modeladmin.message_user(request, f"{count} book(s) marked as published.")


class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status", "pages", "price", "colored_status"]
    list_filter = ["status", "categories", "publication_date"]
    search_fields = ["title", "author__first_name", "author__last_name", "isbn"]
    list_editable = ["status"]
    list_per_page = 25
    date_hierarchy = "publication_date"
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["categories"]
    actions = [make_published]

    fieldsets = [
        ("Basic Info", {"fields": ["title", "slug", "isbn", "description"]}),
        ("Details", {"fields": ["author", "publisher", "categories", "pages", "price"]}),
        ("Publication", {"fields": ["status", "publication_date"], "classes": ["collapse"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Status", ordering="status")
    def colored_status(self, obj):
        colors = {"draft": "#ffa500", "published": "#28a745", "archived": "#6c757d"}
        color = colors.get(obj.status, "#000")
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>', color, obj.get_status_display())


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "book_count"]
    search_fields = ["first_name", "last_name", "email"]

    @admin.display(description="Name")
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description="Books")
    def book_count(self, obj):
        return obj.books.count()


admin.site.site_header = "Django Bookstore Admin"
admin.site.site_title = "Bookstore"
admin.site.index_title = "Welcome to Bookstore Admin"