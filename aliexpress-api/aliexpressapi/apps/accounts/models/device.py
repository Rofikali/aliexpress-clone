from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


class UserDevice(models.Model):
    DEVICE_TYPE_CHOICES = (
        ("mobile", "Mobile"),
        ("desktop", "Desktop"),
        ("tablet", "Tablet"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="devices"
    )
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    device_token = models.CharField(
        max_length=255, blank=True, null=True, help_text="Push/Platform token"
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    last_active = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "user device"
        verbose_name_plural = "user devices"
        indexes = [
            models.Index(fields=["user", "device_type"]),
            models.Index(fields=["device_token"]),
            models.Index(fields=["last_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "device_token"], name="uq_user_device_token"
            )
        ]

    def __str__(self):
        return f"Device {self.id} for {self.user}"

    def touch(self):
        self.last_active = timezone.now()
        self.save(update_fields=["last_active"])
