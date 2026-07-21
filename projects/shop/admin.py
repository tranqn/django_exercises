"""Shop admin with order inlines."""
from django.contrib import admin
from .models import Product, Category
from .order_models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "price", "qty"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "status", "total", "created"]
    list_filter = ["status", "created"]
    inlines = [OrderItemInline]
    date_hierarchy = "created"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "available"]
    list_editable = ["price", "stock", "available"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Category)