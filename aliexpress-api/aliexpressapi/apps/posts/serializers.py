from apps.comments.serializers import CommentSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.like.serializers import LikeSerializer
from rest_framework import serializers

from .models import Post


user = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    # likes = LikeSerializer(many=True)
    likes = LikeSerializer(many=True, read_only=True, source="liked_post")
    video = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "text", "video", "created_at", "comments", "likes", "user"]
        depth = 2
        # fields = ["id", "text", "video", "created_at","likes", "user"]

    def get_user(self, obj):
        request = self.context.get("request")
        user = obj.user

        # print(f"[DEBUG] Entered get_user for user ID: {getattr(user, 'id', 'Unknown')}")
        # print(
        #     f"[DEBUG] Has image attribute? {'Yes' if hasattr(user, 'image') else 'No'}"
        # )

        image_url = None
        if hasattr(user, "image") and user.image and hasattr(user.image, "url"):
            print(f"[DEBUG] Image field exists and is set: {user.image}")
            try:
                raw_url = user.image.url
                # print(f"[DEBUG] Raw image URL: {raw_url}")
                image_url = (
                    request.build_absolute_uri(raw_url)
                    if request
                    else f"{settings.MEDIA_URL}{raw_url}"
                )
                # print(f"[DEBUG] Final image URL: {image_url}")
            except ValueError as e:
                print(f"[ERROR] No image file associated with user {user.id}: {e}")
            except Exception as e:
                print(
                    f"[ERROR] Unexpected error while resolving image URL for user {user.id}: {e}"
                )
        else:
            print(f"[WARNING] User {user.id} has no image or it's empty.")

        return {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "image": image_url,
        }

    def get_video(self, obj):
        request = self.context.get("request")

        video_url = None
        if hasattr(obj, "video") and obj.video:  # Safely check the video exists
            try:
                # print("Video field exists:", obj.video)
                if request:
                    video_url = request.build_absolute_uri(obj.video.url)
                    # print("Full video URL with request:", video_url)
                else:
                    video_url = f"{settings.MEDIA_URL}{obj.video.url}"
                    # print("Fallback video URL without request:", video_url)
            except ValueError as e:
                # Handles "The 'video' attribute has no file associated with it."
                # print("Caught ValueError when accessing video URL:", str(e))
                video_url = None
        else:
            print("No video file associated or video field is missing.")

        return video_url

    def get_created_at(self, obj):
        return obj.created_at.strftime("%b %d %Y")
