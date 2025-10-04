from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status

from apps.home.models.section_category import HomepageCategory
from apps.home.serializers.section_category_serializer import HomepageCategorySerializer
from components.responses.response_factory import ResponseFactory
from drf_spectacular.utils import extend_schema, OpenApiResponse


# -----------------------------
# Category endpoints
# -----------------------------
class HomepageCategoryViewSet(viewsets.ViewSet):
    @extend_schema(
        responses={200: HomepageCategorySerializer(many=True)},
        tags=["Homepage"],
        summary="List top homepage categories",
    )
    def list(self, request):
        categories = HomepageCategory.objects.select_related("category").order_by(
            "sort_order"
        )
        serializer = HomepageCategorySerializer(
            categories, many=True, context={"request": request}
        )
        return ResponseFactory.success_collection(
            items=serializer.data,
            message="Categories list",
            request=request,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={200: HomepageCategorySerializer},
        tags=["Homepage"],
        summary="Retrieve single category details",
    )
    def retrieve(self, request, pk=None):
        category = get_object_or_404(
            HomepageCategory.objects.select_related("category"), pk=pk
        )
        serializer = HomepageCategorySerializer(category, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data, message="Category detail", request=request
        )
