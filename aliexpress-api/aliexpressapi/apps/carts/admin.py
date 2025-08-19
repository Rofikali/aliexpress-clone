# from django.contrib import admin

# # Register your models here.
# from .models import Cart, CartItem, Wishlist, WishlistItem


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ("user", "created_at", "updated_at")
#     search_fields = ("user__username",)
#     list_filter = ("created_at", "updated_at")


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ("cart", "product", "quantity", "added_at")
#     search_fields = ("cart__user__username", "product__name")
#     list_filter = ("added_at",)


# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ("user", "created_at")
#     search_fields = ("user__username",)
#     list_filter = ("created_at",)


# @admin.register(WishlistItem)
# class WishlistItemAdmin(admin.ModelAdmin):
#     list_display = ("wishlist", "product", "added_at")
#     search_fields = ("wishlist__user__username", "product__name")
#     list_filter = ("added_at",)
