from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# import response

User = get_user_model()

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
