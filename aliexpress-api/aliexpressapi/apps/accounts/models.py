# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import BaseUserManager
import uuid
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.validators import RegexValidator


# ---------------------------
# Custom User Manager
# ---------------------------
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(
            email=email, username=username, created_at=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


# ---------------------------
# User model
# ---------------------------
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("buyer", "Buyer"),
        ("seller", "Seller"),
        ("admin", "Admin"),
    )

    KYC_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[
            RegexValidator(r"^\+?[0-9\- ]{7,13}$", "Enter a valid phone number.")
        ],
        db_index=True,
    )

    # password is handled by AbstractBaseUser (password hash)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="buyer", db_index=True
    )
    kyc_status = models.CharField(
        max_length=20, choices=KYC_STATUS_CHOICES, default="pending", db_index=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # admin UI access
    last_login = models.DateTimeField(blank=True, null=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
            models.Index(fields=["role"]),
            models.Index(fields=["kyc_status"]),
        ]

    def __str__(self):
        return f"{self.username} <{self.email}>"

    def promote_to_seller(self):
        self.role = "seller"
        self.save(update_fields=["role", "updated_at"])

    def set_kyc_status(self, status: str):
        if status not in dict(self.KYC_STATUS_CHOICES):
            raise ValueError("Invalid KYC status")
        self.kyc_status = status
        self.save(update_fields=["kyc_status", "updated_at"])


# ---------------------------
# UserDevice model
# ---------------------------
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
        # optionally enforce uniqueness per user/device token if desired:
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


# ---------------------------
# Password Reset Token model
# ---------------------------
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


# ---------------------------
# Utility helper for creating tokens
# ---------------------------
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


import uuid
from django.db import models
from django.conf import settings


class RefreshToken(models.Model):
    """
    Persistent refresh token record to support rotation and blacklist.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="refresh_tokens",
    )
    jti = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(
        null=True, blank=True
    )  # optional: device fingerprinting
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "jti"]),
            models.Index(fields=["revoked_at"]),
        ]

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None and (
            self.expires_at is None or self.expires_at > timezone.now()
        )

    def revoke(self):
        from django.utils.timezone import now

        if self.revoked_at is None:
            self.revoked_at = now()
            self.save(update_fields=["revoked_at"])
