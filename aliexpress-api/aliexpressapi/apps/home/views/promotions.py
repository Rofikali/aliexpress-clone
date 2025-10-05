from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from apps.home.models.promotion import HomepagePromotion
from apps.home.serializers.promotion_serializer import HomepagePromotionSerializer
from components.responses.response_factory import ResponseFactory
from drf_spectacular.utils import extend_schema, OpenApiResponse


# -----------------------------
# Promotions endpoints
# -----------------------------
class HomepagePromotionViewSet(viewsets.ViewSet):
    @extend_schema(
        responses={200: HomepagePromotionSerializer(many=True)},
        tags=["Homepage"],
        summary="List active promotions",
    )
    def list(self, request):
        promotions = HomepagePromotion.objects.filter(is_active=True).order_by(
            "sort_order"
        )
        serializer = HomepagePromotionSerializer(
            promotions, many=True, context={"request": request}
        )
        return ResponseFactory.success_collection(
            items=serializer.data, message="Promotions list", request=request
        )

    @extend_schema(
        responses={200: HomepagePromotionSerializer},
        tags=["Homepage"],
        summary="Retrieve single promotion details",
    )
    def retrieve(self, request, pk=None):
        promotion = get_object_or_404(HomepagePromotion, pk=pk, is_active=True)
        serializer = HomepagePromotionSerializer(
            promotion, context={"request": request}
        )
        return ResponseFactory.success_resource(
            item=serializer.data, message="Promotion detail", request=request
        )
