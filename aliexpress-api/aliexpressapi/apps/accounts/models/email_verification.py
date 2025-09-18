# apps/accounts/models/email_verification.py
import uuid
import random
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings


class EmailVerificationManager(models.Manager):
    def create_pending(self, user):
        """Create or replace a pending verification for the user"""
        # Invalidate old codes
        self.filter(user=user, is_used=False).update(
            is_used=True, used_at=timezone.now()
        )

        code = str(random.randint(100000, 999999))  # 6-digit OTP
        verification = self.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=10),  # valid for 10 min
        )
        return verification


class EmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verifications",
    )
    code = models.CharField(max_length=6)  # OTP
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    objects = EmailVerificationManager()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"EmailVerification(user={self.user.email}, code={self.code}, used={self.is_used})"
