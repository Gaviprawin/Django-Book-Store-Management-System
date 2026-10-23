from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "book",
        "book_title",
        "unit_price",
        "quantity",
        "subtotal",
    )
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "total_amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "user__username", "user__email")
    readonly_fields = (
        "order_number",
        "user",
        "total_amount",
        "shipping_address",
        "phone",
        "created_at",
        "updated_at",
    )
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "book_title",
        "unit_price",
        "quantity",
        "subtotal",
    )
    readonly_fields = (
        "order",
        "book",
        "book_title",
        "unit_price",
        "quantity",
        "subtotal",
    )
