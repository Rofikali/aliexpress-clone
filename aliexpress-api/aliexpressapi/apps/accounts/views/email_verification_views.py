# # apps/accounts/views/email_verification_views.py
# from rest_framework import viewsets, permissions, status
# from apps.accounts.models.email_verification import EmailVerification
# from apps.accounts.serializers.email_verification_serializer import (
#     EmailVerificationSerializer,
#     EmailVerificationConfirmSerializer,
# )
# from components.responses.response_factory import ResponseFactory
# from django.utils import timezone


# class EmailVerificationRequestViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request):
#         """Request a new OTP"""
#         verification = EmailVerification.objects.create_pending(request.user)
#         # (send email same as in RegisterViewSet)
#         return ResponseFactory.success(
#             body={"expires_at": verification.expires_at},
#             message="Verification code sent to email.",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# class EmailVerificationConfirmViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     def create(self, request):
#         """Confirm OTP"""
#         serializer = EmailVerificationConfirmSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"]
#         code = serializer.validated_data["code"]

#         try:
#             verification = EmailVerification.objects.filter(
#                 user__email=email, code=code, is_used=False
#             ).latest("created_at")
#         except EmailVerification.DoesNotExist:
#             return ResponseFactory.error(
#                 message="Invalid or expired code.",
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if verification.is_expired():
#             return ResponseFactory.error(
#                 message="Code has expired.",
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # ✅ Mark verified
#         verification.is_used = True
#         verification.used_at = timezone.now()
#         verification.save(update_fields=["is_used", "used_at"])

#         # user = verification.user
#         # user.is_active = True  # or set `is_email_verified = True` if you add field
#         # user.save(update_fields=["is_active"])
#         user = verification.user
#         user.is_email_verified = True  # ✅ instead of toggling is_active
#         user.save(update_fields=["is_email_verified"])

#         return ResponseFactory.success(
#             body={},
#             message="Email verified successfully.",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# apps/accounts/views/email_verification_views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from django.conf import settings
from django.utils import timezone

from apps.accounts.serializers.email_verification_serializer import (
    EmailVerificationSerializer,
    EmailVerificationConfirmSerializer,
)
# from apps.accounts.models import EmailVerification
from apps.accounts.models.email_verification import EmailVerification
from components.responses.response_factory import ResponseFactory

from django.core.mail import send_mail
import random
import string
import datetime


def generate_otp(length=6):
    """Generate numeric OTP"""
    return "".join(random.choices(string.digits, k=length))


# ------------------------------
# Request OTP
# ------------------------------
class EmailVerificationRequestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=EmailVerificationSerializer,
        responses={200: OpenApiResponse(description="Verification OTP sent")},
        tags=["Accounts Email Verification"],
        summary="Request Email Verification OTP",
        description="Send an OTP to the user’s email for verification.",
    )
    def create(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        otp = generate_otp()
        expires_at = timezone.now() + datetime.timedelta(minutes=10)

        # Store OTP
        EmailVerification.objects.create(
            user=user, otp=otp, expires_at=expires_at, is_used=False
        )

        try:
            send_mail(
                subject="Verify your email",
                message=f"Your OTP is: {otp}",
                from_email="no-reply@example.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
            sent = True
        except Exception as e:
            print("❌ Email sending failed:", str(e))
            sent = False

        response_body = {
            "sent": sent,
            "expires_at": expires_at,
        }

        # 👇 For console backend, expose OTP for easier testing
        if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
            response_body["debug_otp"] = otp

        return ResponseFactory.success.send(
            body=response_body,
            message="Verification OTP sent to email",
            request=request,
            status=status.HTTP_200_OK,
        )


# ------------------------------
# Confirm OTP
# ------------------------------
class EmailVerificationConfirmViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=EmailVerificationConfirmSerializer,
        responses={200: OpenApiResponse(description="Email verified successfully")},
        tags=["Accounts Email Verification"],
        summary="Confirm Email Verification OTP",
        description="Verify the user’s email by submitting the OTP.",
    )
    def create(self, request):
        serializer = EmailVerificationConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data["otp"]
        user = request.user

        try:
            record = EmailVerification.objects.filter(
                user=user, otp=otp, is_used=False, expires_at__gte=timezone.now()
            ).latest("created_at")
        except EmailVerification.DoesNotExist:
            return ResponseFactory.error(
                message="Invalid or expired OTP",
                errors={"otp": "Invalid or expired OTP"},
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark OTP as used and verify email
        record.is_used = True
        record.save()
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return ResponseFactory.success.send(
            body={"verified": True},
            message="Email verified successfully",
            request=request,
            status=status.HTTP_200_OK,
        )
