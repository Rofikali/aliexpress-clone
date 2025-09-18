
# # apps/accounts/serializers.py
# from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
# from rest_framework_simplejwt.tokens import RefreshToken

# User = get_user_model()


# # class RegisterSerializer(serializers.ModelSerializer):
# #     password = serializers.CharField(write_only=True, min_length=8)

# #     class Meta:
# #         model = User
# #         fields = ["id", "username", "email", "phone_number", "password", "role"]

# #     def validate_password(self, value):
# #         validate_password(value)
# #         return value

# #     def create(self, validated_data):
# #         password = validated_data.pop("password")
# #         user = User(**validated_data)
# #         user.set_password(password)
# #         user.save()
# #         return user


# # class LoginSerializer(serializers.Serializer):
# #     email = serializers.EmailField()
# #     password = serializers.CharField(write_only=True)

# #     def validate(self, attrs):
# #         email = attrs.get("email")
# #         password = attrs.get("password")
# #         try:
# #             user = User.objects.get(email__iexact=email)
# #         except User.DoesNotExist:
# #             raise serializers.ValidationError("Invalid credentials")
# #         if not user.check_password(password):
# #             raise serializers.ValidationError("Invalid credentials")
# #         if not user.is_active:
# #             raise serializers.ValidationError("User is deactivated")
# #         attrs["user"] = user
# #         return attrs


# # class TokenPairSerializer(serializers.Serializer):
# #     access = serializers.CharField(read_only=True)
# #     refresh = serializers.CharField(read_only=True)
# #     access_expires_at = serializers.DateTimeField(read_only=True)


# # class RefreshSerializer(serializers.Serializer):
# #     refresh = serializers.CharField()

# #     def validate(self, attrs):
# #         token = attrs.get("refresh")
# #         try:
# #             refresh = RefreshToken(token)
# #         except Exception:
# #             raise serializers.ValidationError("Invalid refresh token")
# #         attrs["refresh_obj"] = refresh
# #         return attrs


# # class ProfileSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = [
# #             "id",
# #             "username",
# #             "email",
# #             "phone_number",
# #             "role",
# #             "kyc_status",
# #             "is_active",
# #             "last_login",
# #             "created_at",
# #             "updated_at",
# #         ]
# #         read_only_fields = [
# #             "id",
# #             "role",
# #             "kyc_status",
# #             "is_active",
# #             "last_login",
# #             "created_at",
# #             "updated_at",
# #         ]


# # class PasswordResetRequestSerializer(serializers.Serializer):
# #     email = serializers.EmailField()


# # class PasswordResetConfirmSerializer(serializers.Serializer):
# #     token = serializers.CharField()
# #     new_password = serializers.CharField(min_length=8)

# #     def validate_new_password(self, value):
# #         validate_password(value)
# #         return value


# # class DeviceSerializer(serializers.Serializer):
# #     id = serializers.IntegerField(read_only=True)
# #     device_type = serializers.ChoiceField(choices=["mobile", "desktop", "tablet"])
# #     device_token = serializers.CharField(allow_null=True, required=False)
# #     last_active = serializers.DateTimeField(read_only=True)


# # class KYCSubmitSerializer(serializers.Serializer):
# #     # for simplicity, assume client uploads URLs or uses multipart elsewhere
# #     documents = serializers.ListField(child=serializers.URLField(), allow_empty=False)
# #     extra = serializers.JSONField(required=False)
