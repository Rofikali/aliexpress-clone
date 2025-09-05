from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
from django.core.validators import RegexValidator
from django.conf import settings
import uuid


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

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="buyer", db_index=True
    )
    kyc_status = models.CharField(
        max_length=20, choices=KYC_STATUS_CHOICES, default="pending", db_index=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True, db_index=True)
    is_email_verified = models.BooleanField(default=False, db_index=True)  # ✅ new

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
            models.Index(fields=["is_email_verified"]),  # ✅ new index
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
