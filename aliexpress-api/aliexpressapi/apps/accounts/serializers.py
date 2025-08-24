# from django.conf import settings
# from rest_framework import serializers

# # from django.contrib.auth import get_user_model

# # User = get_user_model()
# from .models import User


# """
# {
#     "name": "mike",
#     "email": "mike@example.com",
#     "password": "geekyshows",
#     "password_confirmation": "geekyshows",
#     "first_name":"mike",
#     "last_name":"vi"
# }
# """


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password_confirmation = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "name",
#             "username",
#             "email",
#             "password",
#             "password_confirmation",
#         ]  # Include required fields
#         extra_kwargs = {
#             "password": {"write_only": True},  # Ensure password is write-only
#         }

#     def validate(self, data):
#         """
#         Ensure passwords match.
#         """
#         if data["password"] != data["password_confirmation"]:
#             raise serializers.ValidationError("Passwords must match.")
#         return data

#     def validate_email(self, value):
#         """
#         Ensure email is unique.
#         """
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("A user with this email already exists.")
#         return value

#     def create(self, validated_data):
#         """
#         Create a new user after removing password_confirmation.
#         """
#         # Remove password_confirmation from validated_data
#         validated_data.pop("password_confirmation", None)
#         # Use create_user to ensure password is hashed
#         user = User.objects.create_user(
#             email=validated_data["email"],
#             name=validated_data.get("name", ""),
#             username=validated_data.get("username"),
#             password=validated_data["password"],
#         )
#         return user


# class UserSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "name", "bio", "image"]


#     def get_image(self, obj):
#         request = self.context.get("request")

#         if hasattr(obj, "image") and obj.image and hasattr(obj.image, "url"):
#             # print(f"[DEBUG] Image field is present and has URL: {obj.image}")
#             try:
#                 image_url = obj.image.url
#                 # print(f"[DEBUG] Image URL resolved: {image_url}")
#                 full_url = (
#                     request.build_absolute_uri(image_url)
#                     if request
#                     else f"{settings.MEDIA_URL}{image_url}"
#                 )
#                 # print(f"[DEBUG] Final image URL: {full_url}")
#                 return full_url
#             except ValueError as e:
#                 print(f"[ERROR] No image file for user {obj.id}: {e}")
#             except Exception as e:
#                 print(f"[ERROR] Unexpected error for user {obj.id}: {e}")
#         else:
#             print(
#                 f"[WARNING] User {obj.id} has no image or image has no associated file (empty or missing)."
#             )

#         return None

# class UpdateUserImageSerializer(serializers.Serializer):
#     image = serializers.ImageField(required=True)
#     height = serializers.FloatField(required=True)
#     width = serializers.FloatField(required=True)
#     top = serializers.FloatField(required=True)
#     left = serializers.FloatField(required=True)

#     def validate(self, data):
#         if data["height"] <= 0 or data["width"] <= 0:
#             raise serializers.ValidationError("Height and width must be positive.")
#         return data


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()


# class UsersCollectionSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         # This method is used to represent the collection of users
#         return [UserSerializer(user).data for user in data]


# apps/accounts/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "password", "role"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
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


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class DeviceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    device_type = serializers.ChoiceField(choices=["mobile", "desktop", "tablet"])
    device_token = serializers.CharField(allow_null=True, required=False)
    last_active = serializers.DateTimeField(read_only=True)


class KYCSubmitSerializer(serializers.Serializer):
    # for simplicity, assume client uploads URLs or uses multipart elsewhere
    documents = serializers.ListField(child=serializers.URLField(), allow_empty=False)
    extra = serializers.JSONField(required=False)
