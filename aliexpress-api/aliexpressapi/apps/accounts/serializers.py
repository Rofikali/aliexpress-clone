from django.conf import settings

# from django.contrib.auth import get_user_model
# from .models import Post

# from .models import Post, Comment, Like
# from .models import Post, Comment, Like, User
from rest_framework import serializers

# from django.contrib.auth import get_user_model

# User = get_user_model()
from .models import User


"""
{
    "name": "mike",
    "email": "mike@example.com",
    "password": "geekyshows",
    "password_confirmation": "geekyshows",
    "first_name":"mike",
    "last_name":"vi"
}
"""


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "email",
            "password",
            "password_confirmation",
        ]  # Include required fields
        extra_kwargs = {
            "password": {"write_only": True},  # Ensure password is write-only
        }

    def validate(self, data):
        """
        Ensure passwords match.
        """
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def validate_email(self, value):
        """
        Ensure email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """
        Create a new user after removing password_confirmation.
        """
        # Remove password_confirmation from validated_data
        validated_data.pop("password_confirmation", None)
        # Use create_user to ensure password is hashed
        user = User.objects.create_user(
            email=validated_data["email"],
            name=validated_data.get("name", ""),
            username=validated_data.get("username"),
            password=validated_data["password"],
        )
        return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'name',
#                   'bio', 'image']  # Include only safe fields
# gpt code


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "bio", "image"]

        # def get_image(self, obj):
        #     print('inside obj in userSerialzer ', obj)
        #     print('obj image ', obj.image)
        #     print('obj image url ', obj.image.url )
        #     if obj.image:
        #         request = self.context.get("request")
        #         return (
        #             request.build_absolute_uri(obj.image.url)
        #             if request
        #             else f"{settings.MEDIA_URL}{obj.image.url}"
        #         )
        #     return None

        # context={"request": request}

        # def get_image(self, obj):
        # request = self.context.get("request")

        # print(f"[DEBUG] Entered get_image for user: {getattr(obj, 'id', 'Unknown')}")
        # print(
        #     f"[DEBUG] Has image attribute? {'Yes' if hasattr(obj, 'image') else 'No'}"
        # )

        # if hasattr(obj, "image") and obj.image:
        #     print(f"[DEBUG] Image field is present: {obj.image}")
        #     try:
        #         image_url = obj.image.url
        #         print(f"[DEBUG] Image URL resolved: {image_url}")
        #         full_url = (
        #             request.build_absolute_uri(image_url)
        #             if request
        #             else f"{settings.MEDIA_URL}{image_url}"
        #         )
        #         print(f"[DEBUG] Final image URL: {full_url}")
        #         return full_url
        #     except ValueError as e:
        #         print(f"[ERROR] No image file for user {obj.id}: {e}")
        #     except Exception as e:
        #         print(f"[ERROR] Unexpected error for user {obj.id}: {e}")
        # else:
        #     print(f"[WARNING] User {obj.id} has no image or image is empty.")

        # return None

    def get_image(self, obj):
        request = self.context.get("request")

        # print(f"[DEBUG] Entered get_image for user: {getattr(obj, 'id', 'Unknown')}")
        # print(
        #     f"[DEBUG] Has image attribute? {'Yes' if hasattr(obj, 'image') else 'No'}"
        # )

        if hasattr(obj, "image") and obj.image and hasattr(obj.image, "url"):
            # print(f"[DEBUG] Image field is present and has URL: {obj.image}")
            try:
                image_url = obj.image.url
                # print(f"[DEBUG] Image URL resolved: {image_url}")
                full_url = (
                    request.build_absolute_uri(image_url)
                    if request
                    else f"{settings.MEDIA_URL}{image_url}"
                )
                # print(f"[DEBUG] Final image URL: {full_url}")
                return full_url
            except ValueError as e:
                print(f"[ERROR] No image file for user {obj.id}: {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected error for user {obj.id}: {e}")
        else:
            print(
                f"[WARNING] User {obj.id} has no image or image has no associated file (empty or missing)."
            )

        return None


# class UpdateUserImageSerializer(serializers.Serializer):
#     height = serializers.FloatField()
#     width = serializers.FloatField()
#     top = serializers.FloatField()
#     left = serializers.FloatField()
#     image = serializers.ImageField()


class UpdateUserImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    height = serializers.FloatField(required=True)
    width = serializers.FloatField(required=True)
    top = serializers.FloatField(required=True)
    left = serializers.FloatField(required=True)

    def validate(self, data):
        if data["height"] <= 0 or data["width"] <= 0:
            raise serializers.ValidationError("Height and width must be positive.")
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UsersCollectionSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        # This method is used to represent the collection of users
        return [UserSerializer(user).data for user in data]
