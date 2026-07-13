from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SendVerificationEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_verified:
            return Response(
                {"status": "email-already-verified"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Generate email verification token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verification_link = request.build_absolute_uri(
            reverse("email_verification", kwargs={"uidb64": uid, "token": token})
        )

        # Send verification email
        send_mail(
            "Email Verification",
            f"Please verify your email using this link: {verification_link}",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )

        return Response({"status": "verification-link-sent"}, status=status.HTTP_200_OK)
