# apps/home/serializers/section_product_serializer.py
from rest_framework import serializers
from apps.home.models.section_product import HomepageProduct
from apps.products.serializers.product import ProductSerializer


class HomepageProductSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True, context={"request": None})

    class Meta:
        model = HomepageProduct 
        fields = ["id", "sort_order",'featured_rank']
        # fields = ["id", "sort_order",'section','featured_rank']



class HomepageProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, context={"request": None})

    class Meta:
        model = HomepageProduct 
        fields = ["id", "sort_order",'featured_rank','product']
        # fields = ["id", "sort_order",'section','featured_rank']
