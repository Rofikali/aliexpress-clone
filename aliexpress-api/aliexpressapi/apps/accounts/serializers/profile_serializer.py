# apps/accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


from apps.accounts.models.user import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "role",
            "kyc_status",
            "is_active",
            "is_email_verified",  # ✅ new
            "last_login",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "is_email_verified",
            "last_login",
            "created_at",
            "updated_at",
        ]


class KYCSubmitSerializer(serializers.Serializer):
    # for simplicity, assume client uploads URLs or uses multipart elsewhere
    documents = serializers.ListField(child=serializers.URLField(), allow_empty=False)
    extra = serializers.JSONField(required=False)
