# # apps/accounts/views/password_views.py
# from rest_framework import viewsets
# from apps.accounts.serializers.password_serializer import PasswordResetConfirmSerializer, PasswordResetRequestSerializer
# from drf_spectacular.utils import (
#     extend_schema,
#     OpenApiResponse,
# )
# from rest_framework import permissions
# from components.responses.response_factory import ResponseFactory
# from rest_framework import status


# # ------------------------------
# # Password Reset
# # ------------------------------
# class PasswordResetRequestViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @extend_schema(
#         request=PasswordResetRequestSerializer,
#         responses={200: OpenApiResponse(description="Reset email sent")},
#     )
#     def create(self, request):
#         """Request a password reset link"""
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # TODO: send email logic
#         return ResponseFactory.success.send(
#             body={},
#             message="Password reset link sent",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# # ------------------------------
# # Password Reset Confirm
# # ------------------------------
# class PasswordResetConfirmViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @extend_schema(
#         request=PasswordResetConfirmSerializer,
#         responses={200: OpenApiResponse(description="Password has been reset")},
#     )
#     def create(self, request):
#         """Confirm password reset"""
#         serializer = PasswordResetConfirmSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # TODO: reset logic
#         return ResponseFactory.success.send(
#             body={},
#             message="Password has been reset",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


from rest_framework import viewsets, status, permissions
from apps.accounts.serializers.password_serializer import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
# from apps.accounts.models import create_password_reset_token
from apps.accounts.models.password_reset import create_password_reset_token
from django.conf import settings
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema, OpenApiResponse
from components.responses.response_factory import ResponseFactory


# ------------------------------
# Password Reset Request
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
        user = serializer.context["user"]

        # create token
        token, _ = create_password_reset_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        # send email
        send_mail(
            "Password Reset Request",
            f"Hello {user.username},\n\nClick the link to reset your password:\n{reset_link}\n\nIf you didn’t request this, ignore this email.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return ResponseFactory.success.send(
            body={"reset_link": reset_link if settings.DEBUG else ""},
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
        serializer.save()

        return ResponseFactory.success.send(
            body={},
            message="Password has been reset",
            request=request,
            status=status.HTTP_200_OK,
        )
