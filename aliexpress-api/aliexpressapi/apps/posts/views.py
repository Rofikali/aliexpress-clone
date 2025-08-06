from common.pagination.views import (
    CustomCursorPagination,
)  # Adjust the import path as necessary
from apps.core.services import FileService  # if you have this service
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Post
from .serializers import PostSerializer


class HomeViewSet(ViewSet):
    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer},
        tags=["Posts"],
        summary="List all posts with pagination",
        description="This endpoint returns paginated posts.",
    )
    def list(self, request):
        try:
            queryset = Post.objects.all().order_by("-created_at")  # or 'id'
            paginator = CustomCursorPagination()
            paginated_qs = paginator.paginate_queryset(queryset, request)
            serializer = PostSerializer(
                paginated_qs, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostDetailViewSets(ViewSet):
    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer},
        tags=["Posts"],
        summary="Single post retrieve",
        description="This endpoint allows you to retrieve a single post.",
    )
    def retrieve(self, request, pk=None):
        try:
            post = get_object_or_404(Post, id=pk)

            # related_posts = Post.objects.filter(user=post.user).values()
            related_posts_ids = Post.objects.filter(user=post.user).values_list(
                "id", flat=True
            )

            post_serializer = PostSerializer(
                [post], many=True, context={"request": request}
            )

            return Response(
                {"post": post_serializer.data, "ids": list(related_posts_ids)},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostCreateViewSet(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    """
    ViewSet to handle post creation with a video.
    """

    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer},
        tags=["Posts"],
        summary="create post",
        description="This endpoint allows you to create a new post.",
    )

    # @action(detail=False, methods=['post'])
    def create(self, request):
        data = request.data
        video = request.FILES.get("video")

        if not video or not video.name.endswith(".mp4"):
            print("video is not there ", video)
            return Response(
                {"error": "The video field is required and must be a valid MP4 file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "text" not in data:
            print("Text is not there ", data)
            return Response(
                {"error": "The text field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post(user=request.user, text=data["text"])
            print("post is text and user there ", post)
            post = FileService.add_video(post, video)
            print("post fileser.add video ", video)
            post.save()

            return Response({"success": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteViewSet(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer},
        tags=["Posts"],
        summary="create post",
        description="This endpoint allows you to create a new post.",
    )
    def destroy(self, request, pk=None):
        user = request.user
        try:
            post = get_object_or_404(Post, id=pk, user=user)
            post.delete()
            return Response(
                {"success": "Post deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
