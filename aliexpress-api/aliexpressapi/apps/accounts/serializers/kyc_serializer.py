from rest_framework import serializers
from apps.accounts.models.kyc import KYCApplication, KYCDocument


class KYCDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCDocument
        fields = ["id", "document_type", "file", "uploaded_at"]


class KYCApplicationSerializer(serializers.ModelSerializer):
    documents = KYCDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = KYCApplication
        fields = ["id", "status", "submitted_at", "reviewed_at", "notes", "documents"]
