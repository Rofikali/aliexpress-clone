from rest_framework import serializers
from .models import Order, OrderItem, Shipment, Return
from apps.products.serializers.product import ProductSerializer  # ✅ if exists


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "seller",
            "quantity",
            "price",
            "SKU",
            "created_at",
            "updated_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "total_amount",
            "status",
            "items",
            "created_at",
            "updated_at",
        ]


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            "id",
            "order",
            "warehouse",
            "carrier",
            "tracking_number",
            "status",
            "shipped_at",
            "estimated_delivery",
            "created_at",
            "updated_at",
        ]


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = [
            "id",
            "order_item",
            "reason",
            "status",
            "processed_at",
            "created_at",
            "updated_at",
        ]
