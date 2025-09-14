# new here
# apps.products/viewsets.py
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from apps.products.models import (
    Brand,
)
from apps.products.serializers.brand_serializer import BrandSerializer  

from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import (
    # cache_factory,
    get_cache,
)  # ✅ generic cache factory


# apps.products/viewsets.py

# apps.products/viewsets.py


# -------------------- BRAND --------------------
class BrandViewSet(ViewSet):
    cache = get_cache("brands")

    @extend_schema(
        responses={200: BrandSerializer(many=True)},
        tags=["Brands"],
        summary="All Brands retrieve",
        description="Retrieve all brands with caching.",
    )
    def list(self, request):
        cursor = "all"  # not paginated
        cache_data = self.cache.get_results(cursor)
        if cache_data:
            return ResponseFactory.success(
                data=cache_data,
                message="Brands fetched successfully",
                request=request,
                extra={"from_cache": True},
                status=status.HTTP_200_OK,
            )

        queryset = Brand.objects.all().order_by("-created_at")
        serializer = BrandSerializer(queryset, many=True)
        response_data = serializer.data

        self.cache.cache_results(cursor, response_data)

        return ResponseFactory.success(
            data=response_data,
            message="Brands fetched successfully",
            request=request,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={200: BrandSerializer},
        tags=["Brands"],
        summary="Single Brand retrieve",
        description="Retrieve a single brand by ID.",
    )
    def retrieve(self, request, pk=None):
        brand = get_object_or_404(Brand, id=pk)
        serializer = BrandSerializer(brand)
        return ResponseFactory.success(data=serializer.data, request=request)
