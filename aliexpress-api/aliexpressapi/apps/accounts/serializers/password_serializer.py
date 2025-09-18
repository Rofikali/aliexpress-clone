# # apps/accounts/serializers.py
# from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers

# User = get_user_model()


# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()


# class PasswordResetConfirmSerializer(serializers.Serializer):
#     token = serializers.CharField()
#     new_password = serializers.CharField(min_length=8)

#     def validate_new_password(self, value):
#         validate_password(value)
#         return value

from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accounts.models.password_reset import PasswordResetToken

User = get_user_model()


# -----------------------
# Request Reset Serializer
# -----------------------
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user with this email address.")
        self.context["user"] = user
        return value


# -----------------------
# Confirm Reset Serializer
# -----------------------
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            reset_token = PasswordResetToken.objects.get(token=data["token"])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid token."})

        if reset_token.used:
            raise serializers.ValidationError({"token": "Token already used."})
        if reset_token.is_expired:
            raise serializers.ValidationError({"token": "Token expired."})

        data["reset_token"] = reset_token
        return data

    def save(self, **kwargs):
        reset_token = self.validated_data["reset_token"]
        user = reset_token.user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        reset_token.mark_used()
        return user
