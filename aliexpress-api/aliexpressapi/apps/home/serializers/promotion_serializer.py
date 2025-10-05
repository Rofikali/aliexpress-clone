# apps/home/serializers/promotion_serializer.py
from rest_framework import serializers
from apps.home.models.promotion import HomepagePromotion


class HomepagePromotionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomepagePromotion
        fields = ["id", "title",  "image", "link_url", "sort_order"]
        # fields = ["id", "title", "description", "image", "link_url", "sort_order"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None
