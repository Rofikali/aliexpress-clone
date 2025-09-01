# from django.contrib.auth import get_user_model
# from django.core.cache import cache
# from rest_framework import status
# from drf_spectacular.utils import extend_schema
# from .serializers import (
#     LoginSerializer,
# )

# User = get_user_model()


# # apps/accounts/views.py
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from rest_framework import permissions
# from rest_framework_simplejwt.tokens import RefreshToken

# from .serializers import (
#     RegisterSerializer,
#     TokenPairSerializer,
#     RefreshSerializer,
#     ProfileSerializer,
#     PasswordResetRequestSerializer,
#     PasswordResetConfirmSerializer,
#     DeviceSerializer,
# )
# from components.responses.response_factory import ResponseFactory
# from components.caching.cache_factory import get_cache

# User = get_user_model()
# cache = get_cache("accounts")


# from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

# from django.contrib.auth import get_user_model
# from rest_framework import viewsets
# from drf_spectacular.utils import (
#     OpenApiResponse,
# )

# from .serializers import (
#     KYCSubmitSerializer,
# )
# from components.caching.cache_factory import get_cache

# User = get_user_model()
# cache = get_cache("accounts")


# # @extend_schema(
# #         parameters=[
# #             OpenApiParameter(
# #                 name="cursor",
# #                 type=OpenApiTypes.STR,
# #                 location=OpenApiParameter.QUERY,
# #                 description="Cursor for pagination (optional). Leave empty or 'first' to fetch first page.",
# #                 required=False,
# #             ),
# #         ],
# #         request=ProductSerializer,
# #         responses={200: ProductSerializer(many=True)},
# #         tags=["Products"],
# #         summary="All Products retrieve",
# #         description="Retrieve all products with cursor pagination and caching.",
# #     )
# # ------------------------------
# # Register
# # ------------------------------
# class RegisterViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]
#     # {
#     #     "username": "string",
#     #     "email": "user@example.com",
#     #     "phone_number": "81-64049-1",
#     #     "password": "stringst",
#     #     "role": "buyer",
#     # },

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="email",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Cursor for pagination (optional). Leave empty or 'first' to fetch first page.",
#                 required=True,
#             ),
#         ],
#         request=RegisterSerializer,
#         responses={200: ProfileSerializer},
#         tags=["Accounts Auth"],
#         summary="User Registration",
#         description="Register a new user and return their profile information.",
#     )
#     def create(self, request):
#         """Register a new user"""
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         data = ProfileSerializer(user, context={"request": request}).data
#         return ResponseFactory.success.send(
#             body=data,
#             message="User registered",
#             request=request,
#             status=status.HTTP_201_CREATED,
#         )


# # ------------------------------
# # Login
# # ------------------------------
# class LoginViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @extend_schema(
#         request=LoginSerializer,
#         responses={
#             200: TokenPairSerializer,
#             401: OpenApiResponse(description="Invalid credentials"),
#         },
#     )
#     def create(self, request):
#         """Authenticate and return JWT tokens"""
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]

#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         user.last_login = timezone.now()
#         user.save(update_fields=["last_login"])

#         return ResponseFactory.success.send(
#             body={
#                 "access": access_token,
#                 "refresh": refresh_token,
#                 "access_expires_at": (
#                     timezone.now() + refresh.access_token.lifetime
#                 ).isoformat(),
#             },
#             message="Logged in",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# # ------------------------------
# # Refresh Token
# # ------------------------------
# class RefreshViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @extend_schema(
#         request=RefreshSerializer,
#         responses={200: OpenApiResponse(description="New access token")},
#     )
#     def create(self, request):
#         """Refresh JWT access token"""
#         serializer = RefreshSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         refresh = serializer.validated_data["refresh_obj"]
#         new_access = str(refresh.access_token)
#         return ResponseFactory.success.send(
#             body={"access": new_access},
#             message="Token refreshed",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


# # ------------------------------
# # Logout
# # ------------------------------
# class LogoutViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         request={"type": "object", "properties": {"refresh": {"type": "string"}}},
#         responses={200: OpenApiResponse(description="Successfully logged out")},
#     )
#     def create(self, request):
#         """Blacklist refresh token & logout"""
#         refresh_token = request.data.get("refresh")
#         if not refresh_token:
#             return ResponseFactory.error.send(
#                 message="No refresh token provided",
#                 errors={},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#         except Exception as e:
#             return ResponseFactory.error.send(
#                 message="Invalid token",
#                 errors={"detail": str(e)},
#                 request=request,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         return ResponseFactory.success.send(
#             body={}, message="Logged out", request=request, status=status.HTTP_200_OK
#         )


# # ------------------------------
# # Profile
# # ------------------------------
# class ProfileViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         responses={200: ProfileSerializer},
#     )
#     def list(self, request):
#         """Get current user profile"""
#         data = ProfileSerializer(request.user, context={"request": request}).data
#         return ResponseFactory.success.send(
#             body=data,
#             message="Profile retrieved",
#             request=request,
#             status=status.HTTP_200_OK,
#         )


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


# # ------------------------------
# # Devices
# # ------------------------------
# class DeviceViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         responses={200: DeviceSerializer(many=True)},
#         parameters=[OpenApiParameter("active_only", bool, required=False)],
#     )
#     def list(self, request):
#         """List devices used by this user"""
#         active_only = request.query_params.get("active_only")
#         devices = []  # TODO: query user devices
#         return ResponseFactory.success.send(
#             body=devices,
#             message="Devices retrieved",
#             request=request,
#             status=status.HTTP_200_OK,
#         )

#     @extend_schema(request=DeviceSerializer, responses={201: DeviceSerializer})
#     def create(self, request):
#         """Register a new device"""
#         serializer = DeviceSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # TODO: save device
#         return ResponseFactory.success.send(
#             body=serializer.data,
#             message="Device registered",
#             request=request,
#             status=status.HTTP_201_CREATED,
#         )


# # ------------------------------
# # KYC
# # ------------------------------
# class KYCViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(request=KYCSubmitSerializer, responses={201: KYCSubmitSerializer})
#     def create(self, request):
#         """Submit KYC details"""
#         serializer = KYCSubmitSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # TODO: save KYC
#         return ResponseFactory.success.send(
#             body=serializer.data,
#             message="KYC submitted",
#             request=request,
#             status=status.HTTP_201_CREATED,
#         )

#     @extend_schema(responses={200: KYCSubmitSerializer})
#     def list(self, request):
#         """Get user’s KYC details"""
#         # TODO: fetch user KYC
#         return ResponseFactory.success.send(
#             body={}, message="KYC details", request=request, status=status.HTTP_200_OK
#         )
