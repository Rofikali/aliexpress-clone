# # from django.contrib import admin
# # from apps.products.models.product_model import Product
# # from apps.products.models.category_model import Category
# # from apps.products.models.product_images_model import ProductImages
# # from apps.products.models.brand_model import Brand
# # from apps.products.models.product_variant_model import ProductVariant
# # from apps.products.models.product_attribute_model import ProductAttribute
# # from apps.products.models.inventory_model import Inventory
# # import nested_admin


# # @admin.register(Category)
# # class CategoryAdmin(admin.ModelAdmin):
# #     list_display = ("id", "name", "parent")
# #     search_fields = ("name",)
# #     list_filter = ("parent",)
# #     ordering = ("name",)


# # @admin.register(Brand)
# # class BrandAdmin(admin.ModelAdmin):
# #     list_display = ("id", "name")
# #     search_fields = ("name",)
# #     ordering = ("name",)


# # @admin.register(ProductImages)
# # class ProductImageAdmin(admin.ModelAdmin):
# #     list_display = ("id", "product", "image")
# #     search_fields = ("product__title",)


# # @admin.register(Inventory)
# # class InventoryAdmin(admin.ModelAdmin):
# #     list_display = ("id", "product", "stock", "sku")
# #     search_fields = ("product__title", "sku")
# #     list_filter = ("product",)


# # class ProductAttributeInline(nested_admin.NestedTabularInline):
# #     """
# #     Attributes nested inside Variants.
# #     """

# #     model = ProductAttribute
# #     extra = 1
# #     fields = ("attribute_name", "attribute_value")
# #     show_change_link = True


# # class ProductVariantInline(nested_admin.NestedTabularInline):
# #     """
# #     Variants nested inside Product.
# #     """

# #     model = ProductVariant
# #     extra = 1
# #     fields = ("sku", "price", "stock")
# #     readonly_fields = ("created_at", "updated_at")
# #     show_change_link = True
# #     inlines = [ProductAttributeInline]  # 🔥 Nest attributes under variants


# # @admin.register(Product)
# # class ProductAdmin(nested_admin.NestedModelAdmin):
# #     """
# #     Products with nested Variants and Attributes.
# #     """

# #     list_display = (
# #         "id",
# #         "title",
# #         "brand",
# #         "category",
# #         "price",
# #         "created_at",
# #         "updated_at",
# #     )
# #     search_fields = ("title", "description")
# #     list_filter = ("brand", "category", "created_at")
# #     ordering = ("-created_at",)
# #     readonly_fields = ("created_at", "updated_at")
# #     inlines = [ProductVariantInline]  # 🔥 Variants inline with nested attributes


# # uncomment below codebase
# from django.contrib import admin
# import nested_admin

# from apps.products.models.product_model import Product
# from apps.products.models.category_model import Category
# from apps.products.models.product_images_model import ProductImages
# from apps.products.models.brand_model import Brand

# # from apps.products.models.product_variant_model import ProductVariant
# from apps.products.models.inventory_model import Inventory
# # from apps.products.models.product_variant_model import ProductVariantAttribute


# from apps.products.models.product_attribute_model import (
#     ProductAttribute,
#     ProductAttributeValue,
# )
# from apps.products.models.product_variant_model import (
#     ProductVariant,
#     ProductVariantAttribute,
# )


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "parent")
#     search_fields = ("name",)
#     list_filter = ("parent",)
#     ordering = ("name",)


# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#     search_fields = ("name",)
#     ordering = ("name",)


# @admin.register(ProductImages)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ("id", "product", "image")
#     search_fields = ("product__title",)


# @admin.register(Inventory)
# class InventoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "product", "stock", "sku")
#     search_fields = ("product__title", "sku")
#     list_filter = ("product",)


# # -------------------------
# # ATTRIBUTE + VALUES ADMIN
# # -------------------------


# @admin.register(ProductAttribute)
# class ProductAttributeAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "sort_order", "created_at", "updated_at")
#     search_fields = ("name",)
#     ordering = ("sort_order", "name")


# @admin.register(ProductAttributeValue)
# class ProductAttributeValueAdmin(admin.ModelAdmin):
#     list_display = ("id", "attribute", "value", "created_at", "updated_at")
#     search_fields = ("value", "attribute__name")
#     list_filter = ("attribute",)
#     ordering = ("attribute__sort_order", "value")


# # -------------------------
# # INLINE NESTING
# # -------------------------


# class ProductVariantAttributeInline(nested_admin.NestedTabularInline):
#     """Assign attribute values to a variant."""

#     model = ProductVariantAttribute
#     extra = 1
#     autocomplete_fields = ("value",)
#     show_change_link = True


# class ProductVariantInline(nested_admin.NestedTabularInline):
#     """Variants nested inside Product."""

#     model = ProductVariant
#     extra = 1
#     fields = ("sku", "price", "stock", "image")
#     readonly_fields = ("created_at", "updated_at")
#     show_change_link = True
#     inlines = [ProductVariantAttributeInline]


# # -------------------------
# # PRODUCT ADMIN
# # -------------------------


# @admin.register(Product)
# class ProductAdmin(nested_admin.NestedModelAdmin):
#     """Products with nested Variants and Attributes."""

#     list_display = (
#         "id",
#         "title",
#         "brand",
#         "slug",
#         "created_at",
#         "updated_at",
#     )
#     search_fields = ("title", "description", "slug")
#     list_filter = ("brand", "created_at")
#     ordering = ("-created_at",)
#     readonly_fields = ("created_at", "updated_at")

#     # ⚡ Production-grade polish
#     prepopulated_fields = {"slug": ("title",)}
#     autocomplete_fields = ("brand",'category')  # extend later with category/seller

#     inlines = [ProductVariantInline]


# # class ProductVariantAttributeInline(nested_admin.NestedTabularInline):
# #     """
# #     Assign attribute values to a variant.
# #     Enforces using predefined ProductAttributeValue (dropdown).
# #     """

# #     model = ProductVariantAttribute
# #     extra = 1
# #     autocomplete_fields = ("attribute_value",)
# #     show_change_link = True


# # class ProductVariantInline(nested_admin.NestedTabularInline):
# #     """
# #     Variants nested inside Product.
# #     """

# #     model = ProductVariant
# #     extra = 1
# #     fields = ("sku", "price", "stock", "image")
# #     readonly_fields = ("created_at", "updated_at")
# #     show_change_link = True
# #     inlines = [ProductVariantAttributeInline]


# # @admin.register(Product)
# # class ProductAdmin(nested_admin.NestedModelAdmin):
# #     """
# #     Products with nested Variants and Attributes.
# #     """

# #     list_display = (
# #         "id",
# #         "title",
# #         "brand",
# #         "category",
# #         "price",
# #         "created_at",
# #         "updated_at",
# #     )
# #     search_fields = ("title", "description", "sku")
# #     list_filter = ("brand", "category", "created_at")
# #     ordering = ("-created_at",)
# #     readonly_fields = ("created_at", "updated_at")

# #     # ⚡ Production-grade improvements
# #     autocomplete_fields = ("category", "brand", "seller")
# #     prepopulated_fields = {"slug": ("title",)}

# #     inlines = [ProductVariantInline]


# apps/products/admin.py
from django.contrib import admin
import nested_admin

from apps.products.models.product import Product
from apps.products.models.category import Category
from apps.products.models.product_images import ProductImages
from apps.products.models.brand import Brand
from apps.products.models.inventory import Inventory
from apps.products.models.product_attribute import (
    ProductAttribute,
    ProductAttributeValue,
)
from apps.products.models.product_variant import (
    ProductVariant,
    ProductVariantValue,
)


# -------------------------
# CATEGORY + BRAND ADMIN
# -------------------------


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


# -------------------------
# IMAGES + INVENTORY ADMIN
# -------------------------


@admin.register(ProductImages)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image")
    search_fields = ("product__title",)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "stock", "sku")
    search_fields = ("product__title", "sku")
    list_filter = ("product",)


# -------------------------
# ATTRIBUTE + VALUES ADMIN
# -------------------------


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sort_order")
    search_fields = ("name",)
    ordering = ("sort_order", "name")


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ("id", "attribute", "value")
    search_fields = ("value", "attribute__name")
    list_filter = ("attribute",)
    ordering = ("attribute__sort_order", "value")


# -------------------------
# INLINE NESTING
# -------------------------


class ProductVariantValueInline(nested_admin.NestedTabularInline):
    """Assign attribute values (Color=Red, Size=L) to a variant."""

    model = ProductVariantValue
    extra = 1
    autocomplete_fields = ("attribute", "value")
    show_change_link = True


class ProductVariantInline(nested_admin.NestedTabularInline):
    """Variants nested inside Product."""

    model = ProductVariant
    extra = 1
    fields = (
        "sku",
        "price",
        "discount_price",
        "stock",
        "currency",
        "image",
        "is_active",
    )
    readonly_fields = ("created_at", "updated_at")
    show_change_link = True
    inlines = [ProductVariantValueInline]


# -------------------------
# PRODUCT ADMIN
# -------------------------


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    """Products with nested Variants and Attributes."""

    list_display = (
        "id",
        "title",
        "brand",
        "category",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "description", "slug", "sku")
    list_filter = ("brand", "category", "is_active", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("brand", "category", "seller")

    inlines = [ProductVariantInline]


# # -------------------------
# # BASIC REGISTRATIONS
# # -------------------------
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "parent")
#     search_fields = ("name",)
#     list_filter = ("parent",)
#     ordering = ("name",)
#     raw_id_fields = ("parent",)  # avoid huge nested selects


# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#     search_fields = ("name",)
#     ordering = ("name",)


# @admin.register(ProductImages)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ("id", "product", "image")
#     search_fields = ("product__title",)
#     raw_id_fields = ("product",)


# @admin.register(Inventory)
# class InventoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "product", "sku", "stock")
#     search_fields = ("product__title", "sku")
#     list_filter = ("product",)
#     raw_id_fields = ("product",)


# # -------------------------
# # ATTRIBUTE + VALUES ADMIN
# # -------------------------
# @admin.register(ProductAttribute)
# class ProductAttributeAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "sort_order")
#     search_fields = ("name",)
#     ordering = ("sort_order", "name")


# @admin.register(ProductAttributeValue)
# class ProductAttributeValueAdmin(admin.ModelAdmin):
#     list_display = ("id", "attribute", "value")
#     search_fields = ("value", "attribute__name")
#     list_filter = ("attribute",)
#     ordering = ("attribute__sort_order", "value")
#     raw_id_fields = ("attribute",)


# # -------------------------
# # INLINE NESTING
# # -------------------------
# class ProductVariantAttributeInline(nested_admin.NestedTabularInline):
#     """Assign attribute values to a variant."""

#     model = ProductVariantAttribute
#     extra = 0
#     autocomplete_fields = ("attribute", "value")
#     show_change_link = True
#     # Avoid loading too many inline rows at once
#     max_num = 50


# class ProductVariantInline(nested_admin.NestedTabularInline):
#     """Variants nested inside Product."""

#     model = ProductVariant
#     extra = 0
#     fields = (
#         "sku",
#         "price",
#         "discount_price",
#         "stock",
#         "currency",
#         "image",
#         "is_active",
#     )
#     readonly_fields = ("created_at", "updated_at")
#     show_change_link = True
#     inlines = [ProductVariantAttributeInline]
#     raw_id_fields = ("image",)
#     max_num = 200  # guardrail; admin UI will enforce this limit


# # -------------------------
# # PRODUCT ADMIN
# # -------------------------
# @admin.register(Product)
# class ProductAdmin(nested_admin.NestedModelAdmin):
#     """Products with nested Variants and Attributes."""

#     list_display = (
#         "id",
#         "title",
#         "seller",
#         "brand",
#         "category",
#         "is_active",
#         "created_at",
#     )
#     search_fields = ("title", "description", "slug", "sku")
#     list_filter = ("brand", "category", "is_active", "created_at")
#     ordering = ("-created_at",)
#     readonly_fields = ("created_at", "updated_at")
#     prepopulated_fields = {"slug": ("title",)}
#     autocomplete_fields = ("brand", "category")
#     raw_id_fields = ("seller",)  # sellers list can be huge — use raw id
#     inlines = [ProductVariantInline]

#     def get_queryset(self, request):
#         # use select_related to avoid N+1 fetching of FK fields in list view
#         qs = super().get_queryset(request)
#         return qs.select_related("brand", "category", "seller")


# # -------------------------
# # VARIANT ADMIN (separate fast-access admin)
# # -------------------------
# @admin.register(ProductVariant)
# class ProductVariantAdmin(admin.ModelAdmin):
#     """Quick access to variants without rendering via nested inlines — good for scaling."""

#     list_display = (
#         "id",
#         "product",
#         "sku",
#         "price",
#         "discount_price",
#         "stock",
#         "is_active",
#     )
#     search_fields = ("sku", "product__title")
#     list_filter = ("is_active", "product")
#     raw_id_fields = ("product", "image")
#     autocomplete_fields = ("product",)
#     ordering = ("-created_at",)

#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related("product", "image")
