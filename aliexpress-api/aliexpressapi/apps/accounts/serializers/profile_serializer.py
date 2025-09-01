# apps/accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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
            "last_login",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "role",
            "kyc_status",
            "is_active",
            "last_login",
            "created_at",
            "updated_at",
        ]


class KYCSubmitSerializer(serializers.Serializer):
    # for simplicity, assume client uploads URLs or uses multipart elsewhere
    documents = serializers.ListField(child=serializers.URLField(), allow_empty=False)
    extra = serializers.JSONField(required=False)
