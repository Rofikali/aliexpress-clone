from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from apps.home.models.section_product import HomepageProduct
from apps.home.serializers.section_product_serializer import HomepageProductSerializer, HomepageProductDetailSerializer
from components.responses.response_factory import ResponseFactory
from drf_spectacular.utils import extend_schema, OpenApiResponse


# -----------------------------
# Featured Products endpoints
# -----------------------------
class HomepageFeaturedProductViewSet(viewsets.ViewSet):
    @extend_schema(
        responses={200: HomepageProductSerializer(many=True)},
        tags=["Homepage"],
        summary="List top featured products",
    )
    def list(self, request):
        products = HomepageProduct.objects.select_related("product").order_by(
            "featured_rank"
        )
        serializer = HomepageProductSerializer(
            products, many=True, context={"request": request}
        )
        return ResponseFactory.success_collection(
            items=serializer.data, message="Featured products list", request=request
        )

    @extend_schema(
        responses={200: HomepageProductSerializer},
        tags=["Homepage"],
        summary="Retrieve single featured product details",
    )
    def retrieve(self, request, pk=None):
        product = get_object_or_404(
            HomepageProduct.objects.select_related("product"), pk=pk
        )
        serializer = HomepageProductDetailSerializer(product, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data, message="Featured product detail", request=request
        )
