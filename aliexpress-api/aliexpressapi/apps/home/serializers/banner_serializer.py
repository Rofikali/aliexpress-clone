# apps/home/serializers/banner_serializer.py
from rest_framework import serializers
from apps.home.models.banner import HomepageBanner


class HomepageBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomepageBanner
        fields = [
            "id",
            "title",
            "image",
            # "link_url",
            "alt_text",
            "sort_order",
            "is_active",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None
