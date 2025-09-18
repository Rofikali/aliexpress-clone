import uuid
from django.db import models
from django.conf import settings


class KYCApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="kyc"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_kyc",
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"KYCApplication({self.user.username}, {self.status})"


class KYCDocument(models.Model):
    DOC_TYPES = [
        ("id_card", "ID Card"),
        ("passport", "Passport"),
        ("license", "Driving License"),
        ("address_proof", "Proof of Address"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        KYCApplication, on_delete=models.CASCADE, related_name="documents"
    )
    document_type = models.CharField(max_length=50, choices=DOC_TYPES)
    file = models.FileField(upload_to="kyc_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for {self.application.user.username}"
