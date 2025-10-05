from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from apps.home.models.banner import HomepageBanner
from apps.home.serializers.banner_serializer import HomepageBannerSerializer
from components.responses.response_factory import ResponseFactory
from drf_spectacular.utils import extend_schema, OpenApiResponse


# -----------------------------
# Banner endpoints
# -----------------------------
class HomepageBannerViewSet(viewsets.ViewSet):
    @extend_schema(
        responses={200: HomepageBannerSerializer(many=True)},
        tags=["Homepage"],
        summary="List all active banners",
    )
    def list(self, request):
        banners = HomepageBanner.objects.filter(is_active=True).order_by("sort_order")
        serializer = HomepageBannerSerializer(
            banners, many=True, context={"request": request}
        )
        return ResponseFactory.success_collection(
            items=serializer.data, message="Banners list", request=request
        )

    @extend_schema(
        responses={200: HomepageBannerSerializer},
        tags=["Homepage"],
        summary="Retrieve single banner details",
    )
    def retrieve(self, request, pk=None):
        banner = get_object_or_404(HomepageBanner, pk=pk, is_active=True)
        serializer = HomepageBannerSerializer(banner, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data, message="Banner detail", request=request
        )
