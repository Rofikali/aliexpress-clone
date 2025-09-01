from rest_framework import viewsets
# from apps.accounts.serializers import (
#     ProfileSerializer,
#     KYCSubmitSerializer,
# )

from apps.accounts.serializers.profile_serializer import ProfileSerializer, KYCSubmitSerializer

from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import permissions
from components.responses.response_factory import ResponseFactory
from rest_framework import status


# ------------------------------
# Profile
# ------------------------------
class ProfileViewSet(viewsets.ViewSet):
    route_name = "profile auth"   # ✅ Override → /auth/ instead of /logins/
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: ProfileSerializer},
    )
    def list(self, request):
        """Get current user profile"""
        data = ProfileSerializer(request.user, context={"request": request}).data
        return ResponseFactory.success.send(
            body=data,
            message="Profile retrieved",
            request=request,
            status=status.HTTP_200_OK,
        )


# ------------------------------
# KYC
# ------------------------------
class KYCViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=KYCSubmitSerializer, responses={201: KYCSubmitSerializer})
    def create(self, request):
        """Submit KYC details"""
        serializer = KYCSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: save KYC
        return ResponseFactory.success.send(
            body=serializer.data,
            message="KYC submitted",
            request=request,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(responses={200: KYCSubmitSerializer})
    def list(self, request):
        """Get user’s KYC details"""
        # TODO: fetch user KYC
        return ResponseFactory.success.send(
            body={}, message="KYC details", request=request, status=status.HTTP_200_OK
        )
