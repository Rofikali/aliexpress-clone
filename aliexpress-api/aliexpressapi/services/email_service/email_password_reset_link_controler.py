from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response
# import response

User = get_user_model()
# from .models import Post, User, Comment, Like, Post

# from django.contrib.auth.models import User

# drf spectacular schema
from rest_framework.views import APIView


# from common.paginations.custompagination import CustomCursorPagination


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
