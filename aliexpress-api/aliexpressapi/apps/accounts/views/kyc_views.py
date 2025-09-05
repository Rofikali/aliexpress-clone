from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils import timezone

from apps.accounts.models.kyc import KYCApplication, KYCDocument
from apps.accounts.serializers.kyc_serializer import (
    KYCApplicationSerializer,
    KYCDocumentSerializer,
)


class KYCApplicationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: KYCApplicationSerializer},
        tags=["KYC"],
        summary="Get my KYC application",
    )
    def list(self, request):
        try:
            application = KYCApplication.objects.get(user=request.user)
        except KYCApplication.DoesNotExist:
            return Response(
                {"detail": "No KYC found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = KYCApplicationSerializer(application)
        return Response(serializer.data)

    @extend_schema(
        request=None,
        responses={201: KYCApplicationSerializer},
        tags=["KYC"],
        summary="Submit new KYC application",
    )
    def create(self, request):
        application, created = KYCApplication.objects.get_or_create(user=request.user)
        if not created:
            return Response(
                {"message": "KYC already submitted"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = KYCApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class KYCDocumentUploadViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=KYCDocumentSerializer,
        responses={201: KYCDocumentSerializer},
        tags=["KYC"],
        summary="Upload a KYC document",
    )
    def create(self, request):
        try:
            application, _ = KYCApplication.objects.get_or_create(user=request.user)
            serializer = KYCDocumentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(application=application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: KYCDocumentSerializer(many=True)},
        tags=["KYC"],
        summary="List my uploaded documents",
    )
    def list(self, request):
        docs = KYCDocument.objects.filter(application__user=request.user)
        serializer = KYCDocumentSerializer(docs, many=True)
        return Response(serializer.data)
