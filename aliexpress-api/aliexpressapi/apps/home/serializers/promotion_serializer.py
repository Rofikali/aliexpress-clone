# apps/home/serializers/promotion_serializer.py
from rest_framework import serializers
from apps.home.models.promotion import HomepagePromotion


class HomepagePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepagePromotion
        fields = ["id", "title", "description", "image", "link_url", "sort_order"]
