# from django.contrib import admin

# # Register your models here.
# from .models import Products, ProductImages


# @admin.register(Products)
# class ProductsAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "price", "image", "created_at", "updated_at")
#     search_fields = ("title", "description")
#     list_filter = ("created_at",)
#     ordering = ("-created_at",)
#     readonly_fields = ("created_at", "updated_at")

#     def has_add_permission(self, request):
#         # return False
#         return True

#     def has_change_permission(self, request, obj=None):
#         return True

#     def has_delete_permission(self, request, obj=None):
#         return True

#     def has_view_permission(self, request, obj=None):
#         return True

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.select_related()

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#         obj.updated_by = request.user
#         super().save_model(request, obj, form, change)

#     def delete_model(self, request, obj):
#         obj.delete()

#     # def get_readonly_fields(self, request, obj=None):
#     #     if obj:
#     #         return self.readonly_fields + ("created_by", "updated_by")
#     #     return self.readonly_fields

#     # def get_fields(self, request, obj=None):
#     #     fields = super().get_fields(request, obj)
#     #     if obj:
#     #         return fields + ("created_by", "updated_by")
#     #     return fields


# @admin.register(ProductImages)
# class ProductImagesAdmin(admin.ModelAdmin):
#     list_display = ("id", "img_name")


from django.contrib import admin
from apps.products.models.product_model import Product
from apps.products.models.category_model import Category
from apps.products.models.product_images_model import ProductImages
from apps.products.models.brand_model import Brand
from apps.products.models.product_variant_model import ProductVariant
from apps.products.models.product_attribute_model import ProductAttribute
from apps.products.models.inventory_model import Inventory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent")
    search_fields = ("name",)
    list_filter = ("parent",)
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "brand",
        "category",
        # 'seller',
        "price",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "description")
    list_filter = ("brand", "category", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProductImages)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image")
    search_fields = ("product__title",)


# @admin.register(ProductVariant)
# class ProductVariantAdmin(admin.ModelAdmin):
#     # list_display = ("id", "product", "name", "price")
#     list_display = ("id", "product", "price")
#     search_fields = ("product__title", "name")


# @admin.register(ProductAttribute)
# class ProductAttributeAdmin(admin.ModelAdmin):
#     list_display = ("id", "variant", "attribute_name", "attribute_value")
#     search_fields = ("attribute_name", "attribute_value")


class ProductAttributeInline(admin.TabularInline):
    """
    Inline attributes inside ProductVariant.
    Uses a tabular layout for compact editing.
    """

    model = ProductAttribute
    extra = 1  # Show 1 empty row by default
    fields = ("attribute_name", "attribute_value")
    show_change_link = True


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    Admin for Product Variants with inline attributes.
    """

    list_display = (
        "id",
        "product",
        "sku",
        # "name",
        "price",
        "stock",
        # "is_active",
        "created_at",
    )
    list_display_links = ("id", "sku")
    list_filter = ("product__brand", "product__category")
    search_fields = ("product__title", "sku")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("product", "sku", "price", "stock"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [ProductAttributeInline]  # 🚀 Inline attributes here


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """
    Still keep standalone admin for Product Attributes (optional).
    """

    list_display = ("id", "variant", "attribute_name", "attribute_value")
    list_display_links = ("id", "attribute_name")
    list_filter = (
        "attribute_name",
        "variant__product__brand",
        "variant__product__category",
    )
    search_fields = (
        "attribute_name",
        "attribute_value",
        "variant__sku",
        "variant__product__title",
    )
    ordering = ("attribute_name",)
    list_per_page = 50


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "stock", "sku")
    search_fields = ("product__title", "sku")
    list_filter = ("product",)
