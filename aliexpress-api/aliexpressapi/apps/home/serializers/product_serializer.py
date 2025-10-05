# apps/home/serializers/section_product_serializer.py
from rest_framework import serializers
from apps.home.models.product import HomepageProduct
from apps.products.serializers.product import ProductSerializer


class HomepageProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    image = serializers.ImageField(source='product.image')
    description = serializers.CharField(source='product.description')

    class Meta:
        model = HomepageProduct
        fields = ["id", "sort_order", "product", "featured_rank",'image','description']
        # fields = ["id", "sort_order",'section','featured_rank']

    def get_product(self, obj):
        return obj.product.title if obj.product else None


class HomepageProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, context={"request": None})

    class Meta:
        model = HomepageProduct
        fields = ["id", "sort_order", "featured_rank", "product"]
        # fields = ["id", "sort_order",'section','featured_rank']
