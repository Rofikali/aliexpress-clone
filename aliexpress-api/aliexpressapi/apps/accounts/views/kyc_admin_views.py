from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils import timezone

from apps.accounts.models.kyc import KYCApplication
from apps.accounts.serializers.kyc_serializer import KYCApplicationSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class KYCReviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={200: KYCApplicationSerializer(many=True)},
        tags=["KYC Review"],
        summary="List all KYC applications (Admin only)",
    )
    def list(self, request):
        qs = KYCApplication.objects.all()
        serializer = KYCApplicationSerializer(qs, many=True)
        return Response(serializer.data)

    @extend_schema(
        request={
            "type": "object",
            "properties": {"status": {"type": "string"}, "notes": {"type": "string"}},
        },
        responses={200: KYCApplicationSerializer},
        tags=["KYC Review"],
        summary="Approve/Reject a KYC application (Admin only)",
    )
    def update(self, request, pk=None):
        try:
            application = KYCApplication.objects.get(pk=pk)
        except KYCApplication.DoesNotExist:
            return Response(
                {"error": "KYC not found"}, status=status.HTTP_404_NOT_FOUND
            )

        status_choice = request.data.get("status")
        notes = request.data.get("notes", "")

        if status_choice not in dict(KYCApplication.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )

        application.status = status_choice
        application.notes = notes
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()

        serializer = KYCApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)
