# apps/cart_wishlist/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem, Wishlist, WishlistItem
from apps.products.serializers.product import ProductSerializer


# -------------------- CART ITEM --------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "added_at"]


# -------------------- CART --------------------
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]


# -------------------- WISHLIST ITEM --------------------
class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ["id", "product", "added_at"]


# -------------------- WISHLIST --------------------
class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "items", "created_at"]
        read_only_fields = ["user", "created_at"]
