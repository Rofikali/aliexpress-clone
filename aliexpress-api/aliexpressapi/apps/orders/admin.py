from django.contrib import admin

from .models import Order, OrderItem, Shipment, Return


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "created_at"]
    search_fields = ["user__username", "status"]
    list_filter = ["status", "created_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "price"]
    search_fields = ["order__id", "product__name"]


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "tracking_number", "status", "shipped_at",'estimated_delivery']
    search_fields = ["tracking_number", "order__id"]
    list_filter = ["status", "shipped_at"]


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ["id", "order_item", "reason", "status", "created_at"]
    search_fields = ["order_item__id", "reason"]
    list_filter = ["status", "created_at"]
