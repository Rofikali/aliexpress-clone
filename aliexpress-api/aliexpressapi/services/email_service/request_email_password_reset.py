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
