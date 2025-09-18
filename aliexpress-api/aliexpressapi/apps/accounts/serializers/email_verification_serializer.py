# apps/accounts/serializers/email_verification_serializer.py
from rest_framework import serializers


class EmailVerificationSerializer(serializers.Serializer):
    """Request OTP"""

    email = serializers.EmailField(required=False)

    def validate_email(self, value):
        # Optional: ensure email belongs to logged-in user if provided
        return value


class EmailVerificationConfirmSerializer(serializers.Serializer):
    """Confirm OTP"""

    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Invalid verification code format.")
        return value
