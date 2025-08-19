# from django.contrib import admin

# # Register your models here.
# from .models import Order, OrderItem, Shipment, Return


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "total_amount", "status", "created_at", "updated_at")
#     list_filter = ("status", "created_at", "updated_at")
#     search_fields = ("user__username", "status")


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "order",
#         "product",
#         "seller",
#         "quantity",
#         "price",
#         "SKU",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("order__status", "created_at", "updated_at")
#     search_fields = ("order__id", "product__name", "seller__username", "SKU")


# @admin.register(Shipment)
# class ShipmentAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "order",
#         "warehouse",
#         "carrier",
#         "tracking_number",
#         "status",
#         "estimated_delivery",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("status", "created_at", "updated_at")
#     search_fields = ("order__id", "warehouse__name", "carrier", "tracking_number")


# @admin.register(Return)
# class ReturnAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "order_item",
#         "reason",
#         "status",
#         "processed_at",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("status", "created_at", "updated_at")
#     search_fields = ("order_item__id", "reason", "status")
