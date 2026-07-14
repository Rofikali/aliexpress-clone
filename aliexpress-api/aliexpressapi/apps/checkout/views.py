from django.shortcuts import render

# Create your views here.
# apps/checkout/views.py
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from apps.checkout.services.checkout_service import CheckoutService
from apps.checkout.repositories.checkout_repository import CheckoutRepository
from apps.carts.views import CartViewSet
from components.responses.response_factory import ResponseFactory


class CheckoutViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CheckoutService(CheckoutRepository())

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "Idempotency-Key",
                OpenApiTypes.UUID,
                location=OpenApiParameter.HEADER,
                required=False,
            )
        ],
        tags=["Checkout"],
        summary="Checkout cart",
    )
    def create(self, request):
        cart = CartViewSet().get_cart(request)
        key = request.headers.get("Idempotency-Key")

        order = self.service.checkout(
            cart=cart,
            user=request.user,
            idempotency_key=key,
        )

        return ResponseFactory.success_resource(
            item={"order_id": str(order.id)},
            message="Checkout completed",
            status=status.HTTP_201_CREATED,
            request=request,
        )
