# apps.products.serializers.category_serializers.py
from rest_framework import serializers
from apps.products.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]
