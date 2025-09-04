from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import uuid


class PasswordResetToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_resets",
    )
    token = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)
    used = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = "password reset token"
        verbose_name_plural = "password reset tokens"
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["used"]),
        ]

    def __str__(self):
        return f"PasswordResetToken(user={self.user_id}, used={self.used})"

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def mark_used(self):
        self.used = True
        self.save(update_fields=["used"])


def create_password_reset_token(user, ttl_seconds: int = 60 * 60):
    """
    Convenience function to create a one-time password reset token
    TTL default = 1 hour.
    Returns (token_str, instance)
    """
    import secrets

    token_str = secrets.token_urlsafe(48)
    expires = timezone.now() + timedelta(seconds=ttl_seconds)
    instance = PasswordResetToken.objects.create(
        user=user, token=token_str, expires_at=expires
    )
    return token_str, instance
