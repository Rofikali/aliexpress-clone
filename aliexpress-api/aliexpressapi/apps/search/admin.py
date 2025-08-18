# from django.contrib import admin


# from .models import SearchIndex, RecommendationRule, RecommendationLog


# @admin.register(SearchIndex)
# class SearchIndexAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "category",
#         "brand",
#         "price",
#         "stock",
#         "created_at",
#         "updated_at",
#     )
#     search_fields = ("title", "description")
#     list_filter = ("category", "brand")


# @admin.register(RecommendationRule)
# class RecommendationRuleAdmin(admin.ModelAdmin):
#     list_display = ("rule_type", "created_at", "updated_at")
#     search_fields = ("rule_type",)
#     list_filter = ("rule_type",)


# @admin.register(RecommendationLog)
# class RecommendationLogAdmin(admin.ModelAdmin):
#     list_display = ("user", "product", "recommended_product", "rule", "timestamp")
#     search_fields = ("user__username", "product__title", "recommended_product__title")
#     list_filter = ("rule", "timestamp")
