# apps/home/views/home_viewset.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from apps.home.models.section import HomepageSection
from apps.home.serializers.section_serializer import HomepageSectionSerializer
from components.caching.cache_factory import get_cache
from components.responses.response_factory import ResponseFactory

CACHE = get_cache("homepage")  # use your existing cache factory


class HomepageViewSet(viewsets.ViewSet):
    """
    Return a list of active homepage sections (cached).
    """

    @extend_schema(
        responses={200: HomepageSectionSerializer(many=True)},
        tags=["Homepage"],
        summary="Get homepage sections",
    )
    def list(self, request):
        # cache_key = "homepage:sections"
        # cached = CACHE.get_results(cache_key)
        # if cached:
        #     return ResponseFactory.success_collection(
        #         items=cached.get("items", []),
        #         pagination=cached.get("pagination", {}),
        #         message="Homepage sections (cache)",
        #         status=status.HTTP_200_OK,
        #         request=request,
        #         cache="HIT",
        #     )

        # qs = HomepageSection.objects.filter(is_active=True).prefetch_related(
        #     "banners", "products__product"
        # )

        qs = HomepageSection.objects.filter(is_active=True).prefetch_related(
            "banners",
            "products__product",
            "categories__category",  # ✅ new
        )

        serializer = HomepageSectionSerializer(
            qs, many=True, context={"request": request}
        )
        data = serializer.data
        # CACHE.cache_results(cache_key, {"items": data, "pagination": {}})
        return ResponseFactory.success_collection(
            items=data,
            pagination={},
            message="Homepage sections",
            status=status.HTTP_200_OK,
            request=request,
        )

    @extend_schema(
        responses={200: HomepageSectionSerializer},
        tags=["Homepage"],
        summary="Retrieve single homepage section",
    )
    def retrieve(self, request, pk=None):
        section = get_object_or_404(HomepageSection, pk=pk, is_active=True)
        serializer = HomepageSectionSerializer(section, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Homepage section retrieved",
            status=status.HTTP_200_OK,
            request=request,
        )

    @extend_schema(
        responses={200: HomepageSectionSerializer},
        tags=["Homepage"],
        summary="Retrieve homepage Banner and Porducts section",
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="featured",
    )
    def featured(self, request):
        # cache_key = "homepage:featured"
        # cached = CACHE.get_results(cache_key)
        # if cached:
        #     return ResponseFactory.success_collection(
        #         items=cached.get("items", []),
        #         pagination=cached.get("pagination", {}),
        #         message="Featured (cache)",
        #         status=status.HTTP_200_OK,
        #         request=request,
        #         cache="HIT",
        #     )

        sections = HomepageSection.objects.filter(
            is_active=True, type__in=["banner", "product_carousel"]
        ).prefetch_related("banners", "products__product")
        serializer = HomepageSectionSerializer(
            sections, many=True, context={"request": request}
        )
        data = serializer.data
        # CACHE.cache_results(cache_key, {"items": data, "pagination": {}})
        return ResponseFactory.success_collection(
            items=data,
            pagination={},
            message="Featured homepage content",
            status=status.HTTP_200_OK,
            request=request,
        )
