# apps/accounts/views/auth_views.py
from rest_framework import viewsets, permissions, status
from datetime import timezone as dt_timezone
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.conf import settings

# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError

from apps.accounts.serializers.profile_serializer import ProfileSerializer
from apps.accounts.serializers.auth_serializer import (
    RegisterSerializer,
    LoginSerializer,
    TokenPairSerializer,
)
from apps.accounts.models.email_verification import EmailVerification

from drf_spectacular.utils import extend_schema, OpenApiResponse

from components.responses.response_factory import ResponseFactory
from components.authentication.jwt_utils import create_token_pair_for_user

from django.core.mail import send_mail

User = get_user_model()


# ------------------------------
# Register
# ------------------------------
class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: ProfileSerializer},
        tags=["Accounts Auth"],
        summary="User Registration",
        description="Register a new user, return profile & tokens, and send email verification OTP.",
    )
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save(is_active=True, is_email_verified=False)
        except IntegrityError:
            return ResponseFactory.error(
                message="A user with these credentials already exists.",
                status=status.HTTP_400_BAD_REQUEST,
                request=request,
            )

        # Generate tokens via SimpleJWT
        tokens = create_token_pair_for_user(user)

        # Create OTP entry using manager (invalidates previous pending ones)
        verification = EmailVerification.objects.create_pending(user)

        # Send OTP (sync; consider async in prod)
        try:
            send_mail(
                subject="Verify your email",
                message=f"Your verification code is: {verification.code}",
                from_email=getattr(
                    settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"
                ),
                recipient_list=[user.email],
                fail_silently=False,
            )
            sent = True
        except Exception as e:
            # Don't block registration; log and return false sent flag
            print(f"❌ Email sending failed: {e}")
            sent = False

        data = {
            "profile": ProfileSerializer(user, context={"request": request}).data,
            "tokens": tokens,
            "email_verification": {"sent": sent, "expires_at": verification.expires_at},
        }
        # return ResponseFactory.success(
        #     data=data,
        #     message="User registered successfully. Verification OTP sent to email.",
        #     status=status.HTTP_201_CREATED,
        #     request=request,
        # )
        return ResponseFactory.success_collection(
            items=data,
            message="User registered successfully. Verification OTP sent to email.",
            status=status.HTTP_201_CREATED,
            request=request,
        )


# ------------------------------
# Login
# (Optional: you can instead use the SimpleJWT TokenObtainPair endpoint)
# ------------------------------
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: TokenPairSerializer,
            401: OpenApiResponse(description="Invalid credentials or unverified email"),
        },
        tags=["Accounts Auth"],
        summary="Login User",
        description="Authenticate and return JWT tokens. Requires verified email.",
    )
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if not user.is_email_verified:
            return ResponseFactory.error(
                message="Please verify your email before logging in.",
                errors={"email": ["Email not verified"]},
                request=request,
                status=status.HTTP_403_FORBIDDEN,
            )

        tokens = create_token_pair_for_user(user)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return ResponseFactory.success(
            data=tokens,
            message="Logged in successfully",
            request=request,
            status=status.HTTP_200_OK,
        )


# ------------------------------
# Logout (blacklist refresh)
# ------------------------------
class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request={"type": "object", "properties": {"refresh": {"type": "string"}}},
        responses={200: OpenApiResponse(description="Successfully logged out")},
        tags=["Accounts Auth"],
        summary="Logout User",
        description="Blacklist refresh token & logout.",
    )
    def create(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return ResponseFactory.error(
                message="No refresh token provided",
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            # mark token blacklisted (requires token_blacklist app)
            token.blacklist()
        except TokenError:
            return ResponseFactory.error(
                message="Invalid or expired refresh token",
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return ResponseFactory.success(
            data={},
            message="Logged out successfully",
            request=request,
            status=status.HTTP_200_OK,
        )


# ------------------------------
# Refresh
# ------------------------------
class RefreshViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request={"type": "object", "properties": {"refresh": {"type": "string"}}},
        responses={200: OpenApiResponse(description="New access token issued")},
        tags=["Accounts Auth"],
        summary="Refresh Token",
        description="Use refresh token to get new access token.",
    )
    def create(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return ResponseFactory.error(
                message="No refresh token provided",
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh_obj = RefreshToken(refresh_token)
        except TokenError:
            return ResponseFactory.error(
                message="Invalid or expired refresh token",
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Optionally rotate refresh tokens here; by default, SimpleJWT ROTATE_REFRESH_TOKENS config handles rotation for views
        access = refresh_obj.access_token

        access_expires_at = timezone.datetime.fromtimestamp(
            int(access["exp"]), tz=dt_timezone.utc
        ).isoformat()

        tokens = {
            "access": str(access),
            "access_expires_at": access_expires_at,
        }

        return ResponseFactory.success(
            data=tokens,
            message="Token refreshed successfully",
            request=request,
            status=status.HTTP_200_OK,
        )
