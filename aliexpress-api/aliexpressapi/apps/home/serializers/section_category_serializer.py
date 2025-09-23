# apps/home/serializers/section_category_serializer.py
from rest_framework import serializers
from apps.home.models.section_category import HomepageCategory
from apps.products.serializers.category import CategorySerializer


class HomepageCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = HomepageCategory
        fields = ["id", "category", "sort_order"]
