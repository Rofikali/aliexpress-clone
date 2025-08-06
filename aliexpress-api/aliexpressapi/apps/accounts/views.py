from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from apps.postsapi.serializers import PostSerializer
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.postsapi.models import Post
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema
from apps.core.services import ImageFileService
from .serializers import UpdateUserImageSerializer, UserSerializer
from .serializers import (
    LoginSerializer,
    # AllPostsSerializer,
    UserRegistrationSerializer,
    UsersCollectionSerializer,
)
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import logout
# import response

User = get_user_model()
# from .models import Post, User, Comment, Like, Post

# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# drf spectacular schema
from rest_framework.views import APIView

from rest_framework.decorators import action

from drf_spectacular.utils import OpenApiParameter

# from common.paginations.custompagination import CustomCursorPagination
from common.pagination.views import (
    CustomCursorPagination,
)  # Adjust the import path as necessary

# rewrite this code to use the CSRF token in the header using viewsets


class CSRFTokenViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = [AllowAny]  # Disable permissions for this route

    """
    Provides a CSRF token to the client as a cookie.
    """

    @extend_schema(
        tags=["accounts"],
    )
    def list(self, request, *args, **kwargs):
        csrf_token = get_token(request)  # Generate or retrieve CSRF token
        response = JsonResponse({"detail": "CSRF cookie set"})
        # Optional: Include token in response header
        response["X-CSRFToken"] = csrf_token
        # return response
        return Response(
            {"detail": "CSRF cookie set", "csrfToken": csrf_token},
            status=status.HTTP_200_OK,
        )


class RegisterUserViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = [AllowAny]  # Disable permissions for this route

    @extend_schema(
        # This links the serializer for the request body
        request=UserRegistrationSerializer,
        responses={
            201: UserRegistrationSerializer
        },  # Expected response will be the created category
        tags=["accounts"],
    )
    def create(self, request):
        """
        Registering a user

        """
        serializer = UserRegistrationSerializer(data=request.data)
        # print("serializer ---->", serializer)
        # print("request.data ---->", request.data)

        if serializer.is_valid():
            try:
                # Create the user
                user = serializer.save()
                # print("user ---->", user)

                # Optionally create a token
                token = Token.objects.create(user=user)

                response = Response(
                    {
                        "token": token.key,
                        "success": f"You {request.user.username} or successfully registered !!",
                        "status": status.HTTP_201_CREATED,
                    }
                )
                return response
            except InterruptedError:
                return Response(
                    {"error": "A user with this email or username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = [AllowAny]  # Disable permissions for this route

    @extend_schema(
        # This links the serializer for the request body
        request=LoginSerializer,
        responses={
            201: LoginSerializer
        },  # Expected response will be the created category
        tags=["accounts"],
    )
    def create(self, request):
        if self.is_rate_limited(request):
            raise ValidationError("Too many login attempts. Try again later.")

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # ✅ Set sessionid cookie

                return Response(
                    {"detail": "Login successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_rate_limited(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        user_email = request.data.get("email")

        cache_key = f"login_attempt_{user_email}_{ip_address}"
        attempts = cache.get(cache_key, 0)

        if attempts >= 100:  # Limit to 10 attempts
            return True

        cache.set(cache_key, attempts + 1, timeout=60)  # 60 seconds timeout
        return False


class LoggedInUserViewSet(ViewSet):
    """
    API to get details of the logged-in user.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer},
        tags=["accounts"],
    )
    def list(self, request):
        # print("🔍 [DEBUG] Incoming request to LoggedInUserViewSet.retrieve")

        # Authentication Info
        # print(f"🔐 [DEBUG] Authenticated user: {request.user}")
        # print(f"🔐 [DEBUG] Is user authenticated? {request.user.is_authenticated}")

        # # Headers
        # print("📦 [DEBUG] Request Headers:")
        for key, value in request.headers.items():
            print(f"   {key}: {value}")

        # Cookies
        # print("🍪 [DEBUG] Request Cookies:")
        for key, value in request.COOKIES.items():
            print(f"   {key}: {value}")

        # Session
        print("📘 [DEBUG] Session Keys:")
        for key in request.session.keys():
            print(f"   {key}: {request.session.get(key)}")

        # Serialize and prepare response
        serializer = UserSerializer(request.user, context={"request": request})
        csrf_token = get_token(request)
        session_id = request.COOKIES.get("sessionid", None)

        # print("✅ [DEBUG] Serialized user data:", serializer.data)

        response = Response(
            {
                "debug": "No errors, user fetched",
                "user_data": serializer.data,
                "csrf_token": csrf_token,
                "sessionid": session_id,
            },
            status=status.HTTP_200_OK,
        )

        # Optionally also return CSRF token in headers (for frontend convenience)
        response.headers["X-CSRFToken"] = csrf_token

        return response


# add pagination logic here
class ProfileViewSet(ViewSet):
    authentication_classes = [
        SessionAuthentication
    ]  # Disable authentication for this route

    permission_classes = [IsAuthenticated]  # Disable permissions for this route
    """
    API to display the user's posts and profile information.
    """

    @extend_schema(
        responses={200: UserSerializer},
        tags=["accounts"],
        description="Retrieve a user's profile and their posts.",
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve a user's profile and their posts.
        """
        try:
            user = get_object_or_404(User, pk=pk)
            # posts = Post.objects.filter(user=user).order_by("-created_at")

            # Serialize the data
            # post_serializer = PostSerializer(posts, many=True, context={"request": request})
            user_serializer = UserSerializer(user, context={"request": request})

            return Response(
                {
                    # "posts": post_serializer.data,
                    "user": user_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfilePostViewSet(ViewSet):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["accounts"],
        parameters=[
            OpenApiParameter(
                name="cursor",
                required=False,
                location=OpenApiParameter.QUERY,
                description="Cursor for pagination",
            ),
        ],
        responses={200: PostSerializer(many=True)},
        description="Paginated posts of a user using cursor pagination.",
    )
    def list(self, request, user_id=None):
        try:
            user = get_object_or_404(User, pk=user_id)
            queryset = Post.objects.filter(user=user).order_by("-created_at")
            paginator = CustomCursorPagination()
            paginated_qs = paginator.paginate_queryset(queryset, request)

            serializer = PostSerializer(
                paginated_qs, many=True, context={"request": request}
            )
            # print("🔍 [DEBUG] Paginated posts data:", serializer.data)

            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={204: None},
        tags=["accounts"],
    )
    def create(self, request):
        # print("🔍 [DEBUG] Incoming request to LogoutViewSet.create")
        # print(f"🔐 [DEBUG] Authenticated user: {request.user}")
        # print(f"🔐 [DEBUG] Is user authenticated? {request.user.is_authenticated}")

        # Log out the user by flushing the session
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class Update(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UpdateUserImageSerializer},
        tags=["accounts"],
        description="Update user profile image with cropping data.",
    )
    @action(detail=False, methods=["post"])
    def user_image(self, request):
        print("Content-Type:", request.content_type)
        print("Received data:", request.data)
        print("Files:", request.FILES)

        # ✅ Let DRF handle merging
        serializer = UpdateUserImageSerializer(data=request.data)

        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            ImageFileService.update_image(request.user, serializer.validated_data)
            return Response(
                {
                    "success": "OK",
                    "image": request.build_absolute_uri(request.user.image.url),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateViewSet(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=["accounts"],
        description="Update user's profile name and bio.",
    )
    @action(detail=False, methods=["patch"])
    def profile(self, request):
        """
        Patch the authenticated user's name and bio.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "OK"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRandomUsersViewSet(ViewSet):
    @extend_schema(
        request=UserSerializer,  # This links the serializer for the request body
        responses={
            201: UserSerializer
        },  # Expected response will be the created category
        tags=["accounts"],
    )
    def list(self, request):
        try:
            # Fetch random users for suggestions (limit to 5)
            suggested_users = User.objects.order_by("?")[:5]
            # Fetch random users for following (limit to 10)
            following_users = User.objects.order_by("?")[:10]

            # Serialize the data
            suggested_serializer = UserSerializer(
                suggested_users, many=True, context={"request": request}
            )
            following_serializer = UserSerializer(
                following_users, many=True, context={"request": request}
            )

            return Response(
                {
                    "suggested": suggested_serializer.data,
                    "following": following_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_verified:
            return Response(
                {"status": "email-already-verified"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Generate email verification token
        uid = urlsafe_base64_encode(user.pk.encode("utf-8"))
        token = default_token_generator.make_token(user)

        # Generate verification link
        verification_link = f"http://{get_current_site(request).domain}{
            reverse('email_verification', kwargs={'uidb64': uid, 'token': token})
        }"

        # Send verification email
        send_mail(
            "Email Verification",
            f"Please verify your email using this link: {verification_link}",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )

        return Response({"status": "verification-link-sent"}, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode("utf-8")
            user = User.objects.get(pk=uid)

            # Check if the token is valid
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({"status": "email-verified"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"status": "invalid-token"}, status=status.HTTP_400_BAD_REQUEST
                )

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"status": "invalid-link"}, status=status.HTTP_400_BAD_REQUEST
            )


class RequestPasswordReset(APIView):
    """
    API to send a password reset email.
    """

    def post(self, request):
        email = request.data.get("email")

        # Check if email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate the password reset token
        uid = urlsafe_base64_encode(str(user.pk).encode("utf-8"))
        token = default_token_generator.make_token(user)

        # Generate the reset password link
        reset_password_link = f"http://{get_current_site(request).domain}{
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        }"

        # Send the reset email
        send_mail(
            "Password Reset Request",
            f"You can reset your password using the following link: {
                reset_password_link
            }",
            "from@example.com",
            [email],
            fail_silently=False,
        )

        return Response({"status": "reset-link-sent"}, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self, request, uidb64, token):
        # Validate the request data
        password = request.data.get("password")
        password_confirmation = request.data.get("password_confirmation")

        if password != password_confirmation:
            raise ValidationError({"password": "Passwords do not match"})

        try:
            # Decode the UID
            uid = urlsafe_base64_decode(uidb64).decode("utf-8")
            user = User.objects.get(pk=uid)

            # Check if the token is valid
            if not default_token_generator.check_token(user, token):
                return Response(
                    {"error": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the password
            user.set_password(password)
            user.save()

            return Response(
                {"status": "password reset successful"}, status=status.HTTP_200_OK
            )

        except (User.DoesNotExist, ValueError, OverflowError):
            return Response(
                {"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetLinkController(APIView):
    def post(self, request):
        email = request.data.get("email")

        # Validate email
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "No user found with this email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate the password reset token
        uid = urlsafe_base64_encode(user.pk.encode("utf-8"))
        token = default_token_generator.make_token(user)

        # Generate the password reset URL
        reset_url = f"http://{get_current_site(request).domain}{
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        }"

        # Send email with the password reset link
        send_mail(
            "Password Reset Request",
            f"Use the following link to reset your password: {reset_url}",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )

        return Response(
            {"status": "password reset link sent"}, status=status.HTTP_200_OK
        )


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            # Decode the user ID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(id=uid)

            # Check the token
            if default_token_generator.check_token(user, token):
                if not user.email_verified:
                    user.email_verified = True
                    user.save()

                    # Optionally, you can log the user in after email verification
                    login(request, user)

                    # Return a success response
                    return Response(
                        {"message": "Email successfully verified."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Email already verified."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"message": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )


def send_verification_email(user):
    uid = urlsafe_base64_encode(str(user.id).encode())
    token = default_token_generator.make_token(user)
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

    email_subject = "Verify your email address"
    email_message = render_to_string(
        "email/verify_email.html",
        {
            "user": user,
            "verification_url": verification_url,
        },
    )
    send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email])


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    # You can use UsersCollectionSerializer for list representation
    def get_serializer_class(self):
        if self.action == "list":
            return UsersCollectionSerializer
        return UserSerializer
