# new here
# apps.products/viewsets.py
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from apps.products.models.brand import (
    Brand,
)
from apps.products.serializers.brand import BrandSerializer

from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import (
    # cache_factory,
    get_cache,
)  # ✅ generic cache factory
from components.paginations.base_pagination import BaseCursorPagination


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
        # cursor = "all"  # not paginated
        # cache_data = self.cache.get_results(cursor)

        # if cache_data:
        #     return ResponseFactory.success_collection(
        #         items=cache_data.get("items", []),
        #         pagination=cache_data.get("pagination", {}),
        #         message="Products fetched successfully (cache)",
        #         status=status.HTTP_200_OK,
        #         request=request,
        #         cache="HIT",
        #     )

        queryset = Brand.objects.all().order_by("-created_at")
        paginator = BaseCursorPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = BrandSerializer(page, many=True, context={"request": request})

        response_data = paginator.get_paginated_response_data(serializer.data)
        # self.cache.cache_results(cursor, response_data)

        return ResponseFactory.success_collection(
            items=response_data["items"],
            pagination=response_data["pagination"],
            message="Brands fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
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
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Single Brand fetched successfully",
            request=request,
            status=status.HTTP_200_OK,
        )
