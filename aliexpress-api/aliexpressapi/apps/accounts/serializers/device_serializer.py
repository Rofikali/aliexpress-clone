# apps/accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class DeviceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    device_type = serializers.ChoiceField(choices=["mobile", "desktop", "tablet"])
    device_token = serializers.CharField(allow_null=True, required=False)
    last_active = serializers.DateTimeField(read_only=True)
