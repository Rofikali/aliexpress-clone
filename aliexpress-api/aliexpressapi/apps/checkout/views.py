from django.shortcuts import render

# Create your views here.
# apps/checkout/views.py
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from pydantic import ValidationError

from apps.checkout.contracts import CheckoutCommand
from apps.checkout.errors import CheckoutError
from apps.checkout.services.checkout_service import CheckoutService
from apps.checkout.repositories.checkout_repository import CheckoutRepository
from apps.outbox.repositories import OutboxRepository
from apps.outbox.services import OutboxService
from components.responses.response_factory import ResponseFactory
from components.validation.pydantic import format_pydantic_errors


class CheckoutViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CheckoutService(
            CheckoutRepository(),
            OutboxService(OutboxRepository()),
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "Idempotency-Key",
                OpenApiTypes.UUID,
                location=OpenApiParameter.HEADER,
                required=True,
            )
        ],
        tags=["Checkout"],
        summary="Checkout cart",
    )
    def create(self, request):
        try:
            command = CheckoutCommand.model_validate(
                {"idempotency_key": request.headers.get("Idempotency-Key")}
            )
        except ValidationError as error:
            return ResponseFactory.error(
                message="Request validation failed",
                errors=format_pydantic_errors(error),
                status=status.HTTP_400_BAD_REQUEST,
                request=request,
            )

        try:
            order, created = self.service.checkout(
                user=request.user,
                idempotency_key=command.idempotency_key,
            )
        except CheckoutError as error:
            return ResponseFactory.error(
                message=str(error),
                errors=[{"code": error.code, "message": str(error)}],
                status=error.status_code,
                request=request,
            )

        return ResponseFactory.success_resource(
            item={"order_id": str(order.id)},
            message="Checkout completed" if created else "Checkout already completed",
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            request=request,
        )
