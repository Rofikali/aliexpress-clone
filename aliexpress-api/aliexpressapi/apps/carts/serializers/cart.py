# apps/cart/serializers.py
from rest_framework import serializers
from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem
# from apps.products.serializers import ProductVariantSerializer  # assuming you have one
from apps.products.serializers.product_variants import ProductVariantSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    product_variant_id = serializers.UUIDField(write_only=True)

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_variant",
            "product_variant_id",
            "quantity",
            "price",
            "discount_price",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.subtotal


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = ["id", "is_active", "items", "total_items", "total_price"]
