from rest_framework import viewsets
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)
from apps.accounts.serializers.device_serializer import DeviceSerializer
from rest_framework import permissions
from components.responses.response_factory import ResponseFactory
from rest_framework import status


# ------------------------------
# Devices
# ------------------------------
class DeviceViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: DeviceSerializer(many=True)},
        parameters=[OpenApiParameter("active_only", bool, required=False)],
    )
    def list(self, request):
        """List devices used by this user"""
        active_only = request.query_params.get("active_only")
        devices = []  # TODO: query user devices
        return ResponseFactory.success.send(
            body=devices,
            message="Devices retrieved",
            request=request,
            status=status.HTTP_200_OK,
        )

    @extend_schema(request=DeviceSerializer, responses={201: DeviceSerializer})
    def create(self, request):
        """Register a new device"""
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: save device
        return ResponseFactory.success.send(
            body=serializer.data,
            message="Device registered",
            request=request,
            status=status.HTTP_201_CREATED,
        )
