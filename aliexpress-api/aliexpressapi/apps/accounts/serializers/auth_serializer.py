# # apps/accounts/serializers.py
# from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers

# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8)

#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "phone_number", "password", "role"]

#     def validate_password(self, value):
#         validate_password(value)
#         return value

#     def create(self, validated_data):
#         password = validated_data.pop("password")
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         email = attrs.get("email")
#         password = attrs.get("password")
#         try:
#             user = User.objects.get(email__iexact=email)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("Invalid credentials")
#         if not user.check_password(password):
#             raise serializers.ValidationError("Invalid credentials")
#         if not user.is_active:
#             raise serializers.ValidationError("User is deactivated")
#         attrs["user"] = user
#         return attrs


# class TokenPairSerializer(serializers.Serializer):
#     access = serializers.CharField(read_only=True)
#     refresh = serializers.CharField(read_only=True)
#     access_expires_at = serializers.DateTimeField(read_only=True)


# class RefreshSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     def validate(self, attrs):
#         token = attrs.get("refresh")
#         try:
#             refresh = RefreshToken(token)
#         except Exception:
#             raise serializers.ValidationError("Invalid refresh token")
#         attrs["refresh_obj"] = refresh
#         return attrs


from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework import serializers
import re

from rest_framework_simplejwt.tokens import RefreshToken  # used in RefreshSerializer

User = get_user_model()


def _validate_phone(value: str) -> str:
    """
    Lightweight phone validation (E.164-ish without +).
    Replace with django-phonenumber-field if you want full support.
    """
    # allow digits, 7-15 length (typical E.164 range)
    if not re.fullmatch(r"\d{7,15}", value or ""):
        raise serializers.ValidationError(
            "Enter a valid phone number (digits only, 7-15)."
        )
    return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "password", "role"]

    def validate_email(self, value):
        # normalize + ensure unique at serializer level for nicer 400s
        value = (value or "").strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        value = (value or "").strip()
        if value and User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate_phone_number(self, value):
        if value in (None, ""):
            return value
        return _validate_phone(value)

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        # Capture DB integrity errors into serializer errors (clean 400)
        try:
            user.save()
        except IntegrityError:
            raise serializers.ValidationError(
                "A user with these credentials already exists."
            )
        return user


class LoginSerializer(serializers.Serializer):
    # Decide on primary identifier. Keeping email here to match your flow.
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = (attrs.get("email") or "").strip().lower()
        password = attrs.get("password") or ""

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is deactivated")

        attrs["user"] = user
        return attrs


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    access_expires_at = serializers.DateTimeField(read_only=True)


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("refresh")
        try:
            refresh = RefreshToken(token)
        except Exception:
            raise serializers.ValidationError("Invalid refresh token")
        attrs["refresh_obj"] = refresh
        return attrs
