# from rest_framework import serializers
# from apps.products.models.product_attribute_model import (
#     ProductAttribute,
# )


# class ProductAttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttribute
#         fields = [
#             "id",
#             "name",
#         ]

from rest_framework import serializers
from apps.products.models.product_attribute_model import (
    ProductAttribute,
    ProductAttributeValue,
)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    values = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = '__all__'
