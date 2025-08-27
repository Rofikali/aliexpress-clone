from rest_framework.viewsets import ViewSet
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import Order, OrderItem, Shipment, Return
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    ShipmentSerializer,
    ReturnSerializer,
)

# from components.responses.success import SuccessResponse
# from components.responses.error import ErrorRespo
from components.responses.response_factory import ResponseFactory
from components.caching.cache_factory import get_cache
from components.paginations.base_pagination import BaseCursorPagination


# -------------------- ORDERS --------------------
class OrderViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    cache = get_cache("orders")

    @extend_schema(
        responses={200: OrderSerializer(many=True)},
        tags=["Orders"],
        summary="List all user orders",
    )
    def list(self, request):
        try:
            cache_key = f"orders:user:{request.user.id}:list"
            cached = self.cache.get(cache_key)
            if cached:
                return ResponseFactory.success(
                    body=cached,
                    message="Orders fetched from cache",
                    request=request,
                    status_code=status.HTTP_200_OK,
                )

            qs = Order.objects.filter(user=request.user).order_by("-created_at")
            serializer = OrderSerializer(qs, many=True, context={"request": request})

            self.cache.set(cache_key, serializer.data, timeout=600)
            return ResponseFactory.success(
                body=serializer.data,
                message="Orders fetched successfully",
                request=request,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return ResponseFactory.error(
                "Failed to fetch orders", {"detail": str(e)}, request, status_code=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        responses={200: OrderSerializer},
        tags=["Orders"],
        summary="Retrieve single order",
    )
    def retrieve(self, request, pk=None):
        try:
            cache_key = f"orders:{pk}:user:{request.user.id}"
            cached = self.cache.get(cache_key)
            if cached:
                return ResponseFactory.success(
                    body=cached, message="Fetched from cache", request=request, status_code=status.HTTP_200_OK
                )

            order = get_object_or_404(Order, id=pk, user=request.user)
            serializer = OrderSerializer(order, context={"request": request})

            self.cache.set(cache_key, serializer.data, timeout=600)
            return ResponseFactory.success(
                serializer.data, "Order fetched successfully", request=request, status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return ErrorResponse.send("Order not found", {"detail": str(e)}, request)


# -------------------- ORDER ITEMS --------------------
class OrderItemViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "cursor",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="Pagination cursor",
            ),
        ],
        responses={200: OrderItemSerializer(many=True)},
        tags=["Order Items"],
        summary="List items in an order",
    )
    def list(self, request, order_id=None):
        try:
            order = get_object_or_404(Order, id=order_id, user=request.user)
            qs = OrderItem.objects.filter(order=order).order_by("-created_at")

            paginator = BaseCursorPagination()
            page = paginator.paginate_queryset(qs, request)
            serializer = OrderItemSerializer(
                page, many=True, context={"request": request}
            )

            return SuccessResponse.send(
                paginator.get_paginated_response(serializer.data).data,
                "Order items fetched successfully",
                request,
            )
        except Exception as e:
            return ErrorResponse.send(
                "Failed to fetch order items", {"detail": str(e)}, request
            )


# -------------------- SHIPMENTS --------------------
class ShipmentViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: ShipmentSerializer(many=True)},
        tags=["Shipments"],
        summary="List user shipments",
    )
    def list(self, request):
        try:
            qs = Shipment.objects.filter(order__user=request.user).order_by(
                "-created_at"
            )
            serializer = ShipmentSerializer(qs, many=True, context={"request": request})
            return SuccessResponse.send(
                serializer.data, "Shipments fetched successfully", request
            )
        except Exception as e:
            return ErrorResponse.send(
                "Failed to fetch shipments", {"detail": str(e)}, request
            )


# -------------------- RETURNS --------------------
class ReturnViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: ReturnSerializer(many=True)},
        tags=["Returns"],
        summary="List user returns",
    )
    def list(self, request):
        try:
            qs = Return.objects.filter(order_item__order__user=request.user).order_by(
                "-created_at"
            )
            serializer = ReturnSerializer(qs, many=True, context={"request": request})
            return SuccessResponse.send(
                serializer.data, "Returns fetched successfully", request
            )
        except Exception as e:
            return ErrorResponse.send(
                "Failed to fetch returns", {"detail": str(e)}, request
            )
