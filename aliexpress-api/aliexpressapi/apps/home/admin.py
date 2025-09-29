# from django.contrib import admin
# from apps.home.models.banner import HomepageBanner
# from apps.home.models.section import HomepageSection
# from apps.home.models.section_product import HomepageProduct
# from apps.home.models.section_category import HomepageCategory


# @admin.register(HomepageSection)
# class HomepageSectionAdmin(admin.ModelAdmin):
#     list_display = ("title", "type", "is_active")
#     list_filter = ("is_active", "type")
#     search_fields = ("title",)
#     # ordering = ("sort_order",)


# @admin.register(HomepageBanner)
# class HomepageBannerAdmin(admin.ModelAdmin):
#     list_display = ("title", "section", "link_url", "created_at")
#     search_fields = ("title",)
#     list_filter = ("section",)


# @admin.register(HomepageProduct)
# class HomepageProductAdmin(admin.ModelAdmin):
#     list_display = ("product", "section")
#     list_display = ("product", "section", "featured_rank")
#     list_filter = ("section",)
#     search_fields = ("product__name",)
#     ordering = ("featured_rank",)


# @admin.register(HomepageCategory)
# class HomepageCategoryAdmin(admin.ModelAdmin):
#     list_display = ("section", "category", "sort_order")
#     list_filter = ("section",)
#     search_fields = ("category__name",)
#     ordering = ("sort_order",)


from django.contrib import admin
from apps.home.models.banner import HomepageBanner
from apps.home.models.section import HomepageSection
from apps.home.models.section_product import HomepageProduct
from apps.home.models.section_category import HomepageCategory
from apps.home.models.promotion import HomepagePromotion  # ✅ new


@admin.register(HomepageSection)
class HomepageSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "is_active")
    list_filter = ("is_active", "type")
    search_fields = ("title",)
    # ordering = ("sort_order",)


@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "link_url", "created_at")
    search_fields = ("title",)
    list_filter = ("section",)


@admin.register(HomepageProduct)
class HomepageProductAdmin(admin.ModelAdmin):
    list_display = ("product", "section", "featured_rank")
    list_filter = ("section",)
    search_fields = ("product__name",)
    ordering = ("featured_rank",)


@admin.register(HomepageCategory)
class HomepageCategoryAdmin(admin.ModelAdmin):
    list_display = ("section", "category", "sort_order")
    list_filter = ("section",)
    search_fields = ("category__name",)
    ordering = ("sort_order",)


@admin.register(HomepagePromotion)  # ✅ new
class HomepagePromotionAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "link_url", "is_active", "sort_order")
    list_filter = ("section", "is_active")
    search_fields = ("title",)
    ordering = ("sort_order",)
