from django.contrib import admin

# Register your models here.
from .models import Products, ProductImages


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "image", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        # return False
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.delete()

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields + ("created_by", "updated_by")
    #     return self.readonly_fields

    # def get_fields(self, request, obj=None):
    #     fields = super().get_fields(request, obj)
    #     if obj:
    #         return fields + ("created_by", "updated_by")
    #     return fields


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "img_name")
