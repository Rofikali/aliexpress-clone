# new here
# apps.products/viewsets.py
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from apps.products.models.category_model import (
    Category,
)
from apps.products.serializers.category_serializer import (
    CategorySerializer
)

from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import (
    # cache_factory,
    get_cache,
)  # ✅ generic cache factory





# -------------------- CATEGORY --------------------
class CategoryViewSet(ViewSet):
    cache = get_cache("categories")

    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"],
        summary="All Categories retrieve",
        description="Retrieve all product categories with caching.",
    )
    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"],
        summary="All Categories retrieve",
        description="Retrieve all product categories with caching.",
    )
    def list(self, request):
        cursor = "all"  # not paginated, static key
        cache_data = self.cache.get_results(cursor)
        if cache_data:
            return ResponseFactory.success(
                data=cache_data,
                message="Categories fetched successfully",
                request=request,
                extra={"from_cache": True},
                status=status.HTTP_200_OK,
            )

        queryset = Category.objects.all().order_by("-created_at")
        serializer = CategorySerializer(queryset, many=True)
        response_data = serializer.data

        self.cache.cache_results(cursor, response_data)

        return ResponseFactory.success(
            data=response_data,
            message="Categories fetched successfully",
            request=request,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={200: CategorySerializer},
        tags=["Categories"],
        summary="Single Category retrieve",
        description="Retrieve a single category by ID.",
    )
    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category)
        return ResponseFactory.success(data=serializer.data, request=request)
