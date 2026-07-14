from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from apps.payments.services.payment_service import PaymentService
from apps.payments.repositories.payment_repository import PaymentRepository
from apps.orders.services.order_service import OrderService
from apps.orders.repositories.order_repository import OrderRepository
from components.responses.response_factory import ResponseFactory


class PaymentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = PaymentService(PaymentRepository())
        self.order_service = OrderService(OrderRepository())

    @extend_schema(
        parameters=[
            OpenApiParameter("provider", OpenApiTypes.STR),
            OpenApiParameter(
                "Idempotency-Key",
                OpenApiTypes.UUID,
                location=OpenApiParameter.HEADER,
                required=False,
            ),
        ],
        tags=["Payments"],
        summary="Initiate payment",
    )
    def create(self, request):
        order = self.order_service.get_order(
            order_id=request.data["order_id"],
            user=request.user,
        )

        response = self.payment_service.initiate_payment(
            order=order,
            provider=request.data["provider"],
            idempotency_key=request.headers.get("Idempotency-Key"),
        )

        return ResponseFactory.success_resource(
            item=response,
            message="Payment initiated",
            status=status.HTTP_200_OK,
            request=request,
        )
