
# # apps/accounts/views/email_verification_views.py

# from rest_framework import viewsets, permissions, status
# from rest_framework.response import Response
# from drf_spectacular.utils import extend_schema, OpenApiResponse

# from django.conf import settings
# from django.utils import timezone

# from apps.accounts.serializers.email_verification_serializer import (
#     EmailVerificationSerializer,
#     EmailVerificationConfirmSerializer,
# )

# # from apps.accounts.models import EmailVerification
# from apps.accounts.models.email_verification import EmailVerification
# from components.responses.response_factory import ResponseFactory

# from django.core.mail import send_mail
# import random
# import string
# import datetime


# def generate_otp(length=6):
#     """Generate numeric OTP"""
#     return "".join(random.choices(string.digits, k=length))


# # ------------------------------
# # ------------------------------
# # Request OTP
# # ------------------------------
# class EmailVerificationRequestViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         request=EmailVerificationSerializer,
#         responses={200: OpenApiResponse(description="Verification OTP sent")},
#         tags=["Accounts Email Verification"],
#         summary="Request Email Verification OTP",
#         description="Send an OTP to the user’s email for verification.",
#     )
#     def create(self, request):
#         print("📩 [EmailVerificationRequest] Incoming OTP request...")

#         serializer = EmailVerificationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print("✅ Serializer validated:", serializer.validated_data)

#         user = request.user
#         print(f"👤 Current user: {user.email} (ID={user.id})")

#         otp = generate_otp()
#         expires_at = timezone.now() + datetime.timedelta(minutes=10)
#         print(f"🔑 Generated OTP: {otp}, expires at {expires_at}")

#         # Store OTP
#         record = EmailVerification.objects.create(
#             user=user, otp=otp, expires_at=expires_at, is_used=False
#         )
#         print(f"🗂️ OTP record saved in DB (ID={record.id})")

#         try:
#             send_mail(
#                 subject="Verify your email",
#                 message=f"Your OTP is: {otp}",
#                 from_email="no-reply@example.com",
#                 recipient_list=[user.email],
#                 fail_silently=False,
#             )
#             sent = True
#             print("📨 Email sent successfully!")
#         except Exception as e:
#             print("❌ Email sending failed:", str(e))
#             sent = False

#         response_body = {
#             "sent": sent,
#             "expires_at": expires_at,
#         }

#         # 👇 For console backend, expose OTP for easier testing
#         if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
#             response_body["debug_otp"] = otp
#             print(f"🐛 Debug OTP (console backend): {otp}")

#         print("✅ OTP response ready to send back to client.")
#         return ResponseFactory.success.send(
#             body=response_body,
#             message="Verification OTP sent to email",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# # ------------------------------
# # Confirm OTP
# # ------------------------------
# class EmailVerificationConfirmViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         request=EmailVerificationConfirmSerializer,
#         responses={200: OpenApiResponse(description="Email verified successfully")},
#         tags=["Accounts Email Verification"],
#         summary="Confirm Email Verification OTP",
#         description="Verify the user’s email by submitting the OTP.",
#     )
#     def create(self, request):
#         print("📩 [EmailVerificationConfirm] Incoming OTP confirmation request...")

#         serializer = EmailVerificationConfirmSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print("✅ Serializer validated:", serializer.validated_data)

#         otp = serializer.validated_data["otp"]
#         user = request.user
#         print(f"👤 User trying to verify: {user.email} (ID={user.id}) with OTP: {otp}")

#         try:
#             record = EmailVerification.objects.filter(
#                 user=user, otp=otp, is_used=False, expires_at__gte=timezone.now()
#             ).latest("created_at")
#             print(f"🔍 OTP record found in DB (ID={record.id}), created_at={record.created_at}")
#         except EmailVerification.DoesNotExist:
#             print("❌ No matching OTP found (invalid or expired).")
#             return ResponseFactory.error(
#                 message="Invalid or expired OTP",
#                 errors={"otp": "Invalid or expired OTP"},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Mark OTP as used
#         record.is_used = True
#         record.save()
#         print(f"✅ OTP {otp} marked as used in DB (record ID={record.id})")

#         # Verify user email
#         user.is_email_verified = True
#         user.save(update_fields=["is_email_verified"])
#         print(f"🎉 User {user.email} successfully verified (is_email_verified=True)")

#         print("✅ Response ready to send: Email verified successfully.")
#         return ResponseFactory.success.send(
#             body={"verified": True},
#             message="Email verified successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )

# apps/accounts/views/email_verification_views.py
from rest_framework import viewsets, permissions, status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.conf import settings
from django.utils import timezone
from components.responses.response_factory import ResponseFactory
from apps.accounts.serializers.email_verification_serializer import (
    EmailVerificationSerializer,
    EmailVerificationConfirmSerializer,
)
from apps.accounts.models.email_verification import EmailVerification
from django.core.mail import send_mail


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

        # create_pending invalidates old unused codes
        verification = EmailVerification.objects.create_pending(user)

        try:
            send_mail(
                subject="Verify your email",
                message=f"Your verification code is: {verification.code}",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
                recipient_list=[user.email],
                fail_silently=False,
            )
            sent = True
        except Exception as e:
            print("❌ Email sending failed:", str(e))
            sent = False

        response_body = {"sent": sent, "expires_at": verification.expires_at}

        if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
            response_body["debug_code"] = verification.code

        return ResponseFactory.success_collection(
            items=response_body,
            message="Verification OTP sent to email",
            request=request,
            status=status.HTTP_200_OK,
        )


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

        code = serializer.validated_data["code"]
        user = request.user

        try:
            record = EmailVerification.objects.filter(
                user=user, code=code, is_used=False, expires_at__gte=timezone.now()
            ).latest("created_at")
        except EmailVerification.DoesNotExist:
            return ResponseFactory.error(
                message="Invalid or expired code",
                errors={"code": "Invalid or expired code"},
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark used and verify user
        record.is_used = True
        record.used_at = timezone.now()
        record.save(update_fields=["is_used", "used_at"])

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return ResponseFactory.success_collection(
            items={"verified": True},
            message="Email verified successfully",
            request=request,
            status=status.HTTP_200_OK,
        )
