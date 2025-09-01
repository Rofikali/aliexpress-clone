from rest_framework import viewsets
from apps.accounts.serializers.password_serializer import PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from rest_framework import permissions
from components.responses.response_factory import ResponseFactory
from rest_framework import status


# ------------------------------
# Password Reset
# ------------------------------
class PasswordResetRequestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: OpenApiResponse(description="Reset email sent")},
    )
    def create(self, request):
        """Request a password reset link"""
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: send email logic
        return ResponseFactory.success.send(
            body={},
            message="Password reset link sent",
            request=request,
            status=status.HTTP_200_OK,
        )


# ------------------------------
# Password Reset Confirm
# ------------------------------
class PasswordResetConfirmViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: OpenApiResponse(description="Password has been reset")},
    )
    def create(self, request):
        """Confirm password reset"""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: reset logic
        return ResponseFactory.success.send(
            body={},
            message="Password has been reset",
            request=request,
            status=status.HTTP_200_OK,
        )
