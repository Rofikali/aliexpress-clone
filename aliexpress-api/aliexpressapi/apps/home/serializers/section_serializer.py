# # apps/home/serializers/section_serializer.py
# from rest_framework import serializers
# from apps.home.models.section import HomepageSection
# from apps.home.serializers.banner_serializer import HomepageBannerSerializer
# from apps.home.serializers.section_product_serializer import HomepageProductSerializer


# class HomepageSectionSerializer(serializers.ModelSerializer):
#     banners = HomepageBannerSerializer(many=True, read_only=True)
#     products = HomepageProductSerializer(many=True, read_only=True)

#     class Meta:
#         model = HomepageSection
#         fields = [
#             "id",
#             "title",
#             "slug",
#             "type",
#             "position",
#             "is_active",
#             "metadata",
#             "banners",
#             "products",
#         ]


# apps/home/serializers/section_serializer.py
from rest_framework import serializers
from apps.home.models.section import HomepageSection
from apps.home.serializers.banner_serializer import HomepageBannerSerializer
from apps.home.serializers.section_product_serializer import HomepageProductSerializer
from apps.home.serializers.section_category_serializer import HomepageCategorySerializer
from apps.home.serializers.promotion_serializer import HomepagePromotionSerializer


# i just commented this nothing else
class HomepageSectionSerializer(serializers.ModelSerializer):
    banners = HomepageBannerSerializer(many=True, read_only=True)
    products = HomepageProductSerializer(many=True, read_only=True)
    categories = HomepageCategorySerializer(many=True, read_only=True)  # ✅ new
    promotions = HomepagePromotionSerializer(many=True, read_only=True)  # ✅ new

    class Meta:
        model = HomepageSection
        fields = [
            "id",
            "title",
            "slug",
            "type",
            "position",
            "is_active",
            # "metadata",
            "banners",
            "products",
            "categories",  # ✅ new
            "promotions",  # ✅ added
        ]


# class HomepageSectionDetailSerializer(serializers.ModelSerializer):
#     banners = HomepageBannerSerializer(many=True, read_only=True)
#     products = HomepageProductSerializer(many=True, read_only=True)
#     categories = HomepageCategorySerializer(many=True, read_only=True)  # ✅ new
#     promotions = HomepagePromotionSerializer(many=True, read_only=True)  # ✅ new

#     class Meta:
#         model = HomepageSection
#         fields = [
#             "id",
#             "title",
#             "slug",
#             "type",
#             "position",
#             "is_active",
#             "metadata",
#             "banners",
#             "products",
#             "categories",  # ✅ new
#             "promotions",  # ✅ added
#         ]
