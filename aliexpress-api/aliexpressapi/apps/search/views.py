from apps.accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from common.pagination.views import (
    CustomCursorPagination,
)  # Adjust the import path as necessary
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

User = get_user_model()


from django.contrib.auth import get_user_model

User = get_user_model()


class UserSearchViewSet(ViewSet):
    """
    A viewset for searching users, supporting cursor-based pagination.
    """

    @extend_schema(
        responses={200: UserSerializer},
        tags=["Search"],
        description="Search for users by username or name (supports cursor pagination).",
    )
    def list(self, request):
        try:
            query = request.GET.get("q", "").strip().lower()
            if not query:
                return Response(
                    {"detail": "No record found."},
                    status=status.HTTP_200_OK,
                )

            # Build queryset
            queryset = User.objects.filter(
                Q(username__icontains=query) | Q(name__icontains=query)
            ).order_by("-created_at")

            # Try cache
            cache_key = f"user_search:{query}:{request.GET.get('cursor', '')}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)

            # Paginate
            paginator = CustomCursorPagination()
            paginated_qs = paginator.paginate_queryset(queryset, request)

            serializer = UserSerializer(
                paginated_qs, many=True, context={"request": request}
            )

            response = paginator.get_paginated_response(serializer.data)

            # Cache for 15 minutes
            cache.set(cache_key, response.data, timeout=60 * 15)

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
