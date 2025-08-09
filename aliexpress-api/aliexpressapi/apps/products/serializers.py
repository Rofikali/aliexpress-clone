from rest_framework.serializers import ModelSerializer
from .models import Products


# class ProductSerializer(ModelSerializer):
#     Model = Products
#     fields = ["title", "description"]



class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = ["title", "description", "price", "image", "created_at", "updated_at"]



