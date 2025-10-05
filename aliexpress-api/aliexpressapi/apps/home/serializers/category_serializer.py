# apps/home/serializers/section_category_serializer.py
from rest_framework import serializers
from apps.home.models.category import HomepageCategory
from apps.products.serializers.category import CategorySerializer


class HomepageCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    # description = serializers.CharField(source="category.description", read_only=True)

    class Meta:
        model = HomepageCategory
        fields = ["id", "category", "sort_order"]

    def get_category(self, obj):
        # print("obj category name ", obj.category.name)
        # return obj.category.name if obj.category else None

        if obj.category:
            return {
                'id': obj.category.id,
                "name": obj.category.name,
                "description": obj.category.description,
            }


# for details
# class HomepageCategoryDetailSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)

#     class Meta:
#         model = HomepageCategory
#         fields = ["id", "category", "sort_order"]
