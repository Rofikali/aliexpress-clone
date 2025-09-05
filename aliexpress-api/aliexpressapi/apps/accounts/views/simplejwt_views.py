# apps/accounts/views/simplejwt_views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.accounts.serializers.auth_serializer import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Use the custom serializer that can enforce is_email_verified or other business rules.
    """
    serializer_class = CustomTokenObtainPairSerializer
