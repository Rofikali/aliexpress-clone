# # apps/accounts/views/auth_views.py

# from rest_framework import viewsets, permissions, status

# from apps.accounts.serializers.profile_serializer import ProfileSerializer
# from apps.accounts.serializers.auth_serializer import (
#     RegisterSerializer,
#     LoginSerializer,
#     TokenPairSerializer,
# )

# from drf_spectacular.utils import (
#     extend_schema,
#     OpenApiResponse,
#     OpenApiExample,
# )
# from django.utils import timezone

# from components.responses.response_factory import ResponseFactory
# from components.authentication.jwt_utils import (
#     create_token_pair_for_user,
#     decode_access,
#     blacklist_refresh_token,
# )
# from django.contrib.auth import get_user_model


# User = get_user_model()


# from django.db import IntegrityError


# class RegisterViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @extend_schema(
#         request=RegisterSerializer,
#         responses={201: ProfileSerializer},
#         tags=["Accounts Auth"],
#         summary="User Registration",
#         description="Register a new user and return their profile information with JWT tokens.",
#         examples=[
#             OpenApiExample(
#                 "Registration Request Example",
#                 value={
#                     "username": "user1",
#                     "email": "user1@example.com",
#                     "phone_number": "971283761",
#                     "password": "geekyshows",
#                     "role": "buyer",
#                 },
#                 request_only=True,
#             ),
#             OpenApiExample(
#                 "Registration Response Example",
#                 value={
#                     "status": "success",
#                     "success": True,
#                     "code": 201,
#                     "message": "User registered successfully",
#                     "request": {
#                         "id": "uuid",
#                         "timestamp": "2025-08-31T04:28:08.724Z",
#                         "latency_ms": 32.5,
#                         "region": "Nepal-01",
#                         "cache": "MISS",
#                     },
#                     "errors": None,
#                     "data": {
#                         "profile": {
#                             "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                             "username": "user1",
#                             "email": "user1@example.com",
#                             "phone_number": "971283761",
#                             "role": "buyer",
#                             "kyc_status": "pending",
#                             "is_active": True,
#                             "last_login": "2025-08-31T04:28:08.724Z",
#                             "created_at": "2025-08-31T04:28:08.724Z",
#                             "updated_at": "2025-08-31T04:28:08.724Z",
#                         },
#                         "tokens": {
#                             "access": "jwt-access-token",
#                             "refresh": "jwt-refresh-token",
#                             "access_expires_at": "2025-08-31T07:28:08.724Z",
#                         },
#                     },
#                 },
#                 response_only=True,
#             ),
#         ],
#     )
#     def create(self, request):
#         print("➡️ [RegisterViewSet.create] Incoming data:", request.data)

#         serializer = RegisterSerializer(data=request.data)
#         print("➡️ [RegisterViewSet.create] Serializer initialized")

#         serializer.is_valid(raise_exception=True)
#         print(
#             "✅ [RegisterViewSet.create] Serializer validated:",
#             serializer.validated_data,
#         )

#         try:
#             user = serializer.save()
#             print("✅ [RegisterViewSet.create] User saved:", user)
#         except IntegrityError as e:
#             print("❌ [RegisterViewSet.create] IntegrityError:", str(e))
#             return ResponseFactory.error(
#                 message="A user with these credentials already exists.",
#                 status=status.HTTP_400_BAD_REQUEST,
#                 request=request,
#             )
#         except Exception as e:
#             print("❌ [RegisterViewSet.create] Unexpected save error:", str(e))
#             raise  # re-raise so you still see the stack trace in logs

#         try:
#             tokens = create_token_pair_for_user(user)
#             print("✅ [RegisterViewSet.create] Tokens generated:", tokens)
#         except Exception as e:
#             print("❌ [RegisterViewSet.create] Token generation failed:", str(e))
#             raise

#         data = {
#             "profile": ProfileSerializer(user, context={"request": request}).data,
#             "tokens": tokens,
#         }
#         print("➡️ [RegisterViewSet.create] Final response data:", data)

#         try:
#             response = ResponseFactory.success(
#                 data=data,
#                 message="User registered successfully",
#                 status=status.HTTP_201_CREATED,
#                 request=request,
#             )
#             print(
#                 "✅ [RegisterViewSet.create] ResponseFactory.success built successfully"
#             )
#             return response
#         except Exception as e:
#             print("❌ [RegisterViewSet.create] ResponseFactory failed:", str(e))
#             raise


# apps/accounts/views/auth_views.py

from rest_framework import viewsets, permissions, status
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.accounts.serializers.profile_serializer import ProfileSerializer
from apps.accounts.serializers.auth_serializer import (
    RegisterSerializer,
    LoginSerializer,
    TokenPairSerializer,
)
from apps.accounts.models.email_verification import EmailVerification

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)

from components.responses.response_factory import ResponseFactory
from components.authentication.jwt_utils import (
    create_token_pair_for_user,
    decode_access,
    blacklist_refresh_token,
)
# from components.tasks.email import send_verification_email  # <-- async task

User = get_user_model()


# ------------------------------
# Register
# ------------------------------
# apps/accounts/views/auth_views.py (RegisterViewSet updated)
from apps.accounts.models.email_verification import EmailVerification
from django.core.mail import send_mail
from django.conf import settings


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
            # user = serializer.save()
            user = serializer.save(is_active=True, is_email_verified=False)
            print("✅ [RegisterViewSet.create] User saved:", user)
        except IntegrityError:
            return ResponseFactory.error(
                message="A user with these credentials already exists.",
                status=status.HTTP_400_BAD_REQUEST,
                request=request,
            )

        # ✅ Step 1: Generate tokens
        tokens = create_token_pair_for_user(user)

        # ✅ Step 2: Create OTP entry
        verification = EmailVerification.objects.create_pending(user)

        # ✅ Step 3: Send OTP via email (sync, no Celery)
        try:
            send_mail(
                subject="Verify your email",
                message=f"Your verification code is: {verification.code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Don’t block registration, but log/send response
            print(f"❌ Email sending failed: {e}")

        # ✅ Step 4: Build response
        data = {
            "profile": ProfileSerializer(user, context={"request": request}).data,
            "tokens": tokens,
            "email_verification": {
                "sent": True,
                "expires_at": verification.expires_at,
            },
        }
        return ResponseFactory.success(
            data=data,
            message="User registered successfully. Verification OTP sent to email.",
            status=status.HTTP_201_CREATED,
            request=request,
        )


# ------------------------------
# Login
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

        # Enforce email verification before login
        # if not user.is_email_verified:
        #     return ResponseFactory.error(
        #         message="Email not verified. Please check your inbox.",
        #         request=request,
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )

        if not user.is_email_verified:  # ✅ strict block
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
            body=tokens,
            message="Logged in successfully",
            request=request,
            status=status.HTTP_200_OK,
        )


# ------------------------------
# Logout
# ------------------------------
class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request={"type": "object", "properties": {"refresh": {"type": "string"}}},
        responses={200: OpenApiResponse(description="Successfully logged out")},
        tags=["Accounts Auth"],
        summary="Logout User",
        description="Invalidate refresh token & logout.",
    )
    def create(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return ResponseFactory.error(
                message="No refresh token provided",
                errors={},
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        success = blacklist_refresh_token(refresh_token)
        if not success:
            return ResponseFactory.error(
                message="Invalid or expired refresh token",
                errors={},
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return ResponseFactory.success(
            body={},
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
                errors={},
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        decoded = decode_access(refresh_token, verify=True)
        if not decoded:
            return ResponseFactory.error(
                message="Invalid or expired refresh token",
                errors={},
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=decoded["user_id"])
        except User.DoesNotExist:
            return ResponseFactory.error(
                message="User not found",
                errors={},
                request=request,
                status=status.HTTP_404_NOT_FOUND,
            )

        tokens = create_token_pair_for_user(user)
        return ResponseFactory.success(
            body=tokens,
            message="Token refreshed successfully",
            request=request,
            status=status.HTTP_200_OK,
        )


# # # ------------------------------
# # # Login
# # # ------------------------------
# class LoginViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @extend_schema(
#         request=LoginSerializer,
#         responses={
#             200: TokenPairSerializer,
#             401: OpenApiResponse(description="Invalid credentials"),
#         },
#         tags=["Accounts Auth"],
#         summary="Login User",
#         description="Authenticate with username/email and return JWT tokens.",
#     )
#     def create(self, request):
#         """Authenticate and return JWT tokens"""
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]

#         # Generate tokens using our utils
#         tokens = create_token_pair_for_user(user)

#         # Update last login
#         user.last_login = timezone.now()
#         user.save(update_fields=["last_login"])

#         return ResponseFactory.success(
#             body=tokens,
#             message="Logged in successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# # # ------------------------------
# # # Logout
# # # ------------------------------
# class LogoutViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         request={"type": "object", "properties": {"refresh": {"type": "string"}}},
#         responses={200: OpenApiResponse(description="Successfully logged out")},
#         tags=["Accounts Auth"],
#         summary="Logout User",
#         description="Invalidate the refresh token (blacklist) and logout the user.",
#     )
#     def create(self, request):
#         """Blacklist refresh token & logout"""
#         refresh_token = request.data.get("refresh")

#         if not refresh_token:
#             return ResponseFactory.error(
#                 message="No refresh token provided",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         success = blacklist_refresh_token(refresh_token)
#         if not success:
#             return ResponseFactory.error(
#                 message="Invalid or expired refresh token",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return ResponseFactory.success(
#             body={},
#             message="Logged out successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# # # ------------------------------
# # # Refresh
# # # ------------------------------
# class RefreshViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @extend_schema(
#         request={"type": "object", "properties": {"refresh": {"type": "string"}}},
#         responses={200: OpenApiResponse(description="New access token issued")},
#         tags=["Accounts Auth"],
#         summary="Refresh Token",
#         description="Use a valid refresh token to get a new access token.",
#     )
#     def create(self, request):
#         """Exchange refresh token for new access token"""
#         refresh_token = request.data.get("refresh")
#         if not refresh_token:
#             return ResponseFactory.error(
#                 message="No refresh token provided",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         decoded = decode_access(refresh_token, verify=True)
#         if not decoded:
#             return ResponseFactory.error(
#                 message="Invalid or expired refresh token",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             user = User.objects.get(id=decoded["user_id"])
#         except User.DoesNotExist:
#             return ResponseFactory.error(
#                 message="User not found",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         tokens = create_token_pair_for_user(user)
#         return ResponseFactory.success(
#             body=tokens,
#             message="Token refreshed successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# accounts/views/auth.py


# class RegisterViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     def create(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         # Optional: defer tokens until verification completed
#         tokens = create_token_pair_for_user(user)
#         user.last_login = timezone.now()
#         user.save(update_fields=["last_login"])

#         resp = ResponseFactory.success(
#             data={
#                 "profile": ProfileSerializer(user, context={"request": request}).data,
#                 "tokens": tokens,
#             },
#             message="User registered successfully",
#             request=request,
#             status=status.HTTP_201_CREATED,
#         )

#         # If using cookie refresh, set cookie here
#         if settings.JWT_REFRESH_COOKIE:
#             resp.set_cookie(
#                 settings.JWT_REFRESH_COOKIE,
#                 tokens["refresh"],
#                 max_age=15 * 24 * 3600,  # align with REFRESH_TOKEN_LIFETIME
#                 httponly=True,
#                 secure=settings.JWT_COOKIE_SECURE,
#                 samesite=settings.JWT_COOKIE_SAMESITE,
#             )
#         return resp


# class LoginViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     def create(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]

#         tokens = create_token_pair_for_user(user)
#         user.last_login = timezone.now()
#         user.save(update_fields=["last_login"])

#         resp = ResponseFactory.success(
#             data=tokens,
#             message="Logged in successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )
#         if settings.JWT_REFRESH_COOKIE:
#             resp.set_cookie(
#                 settings.JWT_REFRESH_COOKIE,
#                 tokens["refresh"],
#                 max_age=15 * 24 * 3600,
#                 httponly=True,
#                 secure=settings.JWT_COOKIE_SECURE,
#                 samesite=settings.JWT_COOKIE_SAMESITE,
#             )
#         return resp


# class RefreshViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     def create(self, request):
#         # Prefer cookie; fallback to body for non-browser clients
#         refresh = request.COOKIES.get(settings.JWT_REFRESH_COOKIE) or request.data.get(
#             "refresh"
#         )
#         if not refresh:
#             return ResponseFactory.error(
#                 message="No refresh token provided",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             tokens = refresh_access_token(refresh)  # rotates by your settings
#         except Exception:
#             return ResponseFactory.error(
#                 message="Invalid or expired refresh token",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         resp = ResponseFactory.success(
#             data={
#                 "access": tokens["access"],
#                 "access_expires_at": tokens["access_expires_at"].isoformat(),
#                 "refresh": tokens["refresh"],
#             },
#             message="Token refreshed successfully",
#             request=request,
#             status=status.HTTP_200_OK,
#         )
#         if settings.JWT_REFRESH_COOKIE and tokens.get("refresh"):
#             resp.set_cookie(
#                 settings.JWT_REFRESH_COOKIE,
#                 tokens["refresh"],
#                 max_age=15 * 24 * 3600,
#                 httponly=True,
#                 secure=settings.JWT_COOKIE_SECURE,
#                 samesite=settings.JWT_COOKIE_SAMESITE,
#             )
#         return resp


# class LogoutViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request):
#         refresh = request.COOKIES.get(settings.JWT_REFRESH_COOKIE) or request.data.get(
#             "refresh"
#         )
#         if not refresh:
#             return ResponseFactory.error(
#                 message="No refresh token provided",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         ok = blacklist_refresh_token(refresh)
#         resp = ResponseFactory.success(
#             data={},
#             message="Logged out successfully"
#             if ok
#             else "Already invalid or could not blacklist",
#             request=request,
#             status=status.HTTP_200_OK,
#         )
#         if settings.JWT_REFRESH_COOKIE:
#             resp.delete_cookie(settings.JWT_REFRESH_COOKIE)
#         return resp
