from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

# from core.models import AutoUpdate
from apps.core.models import (
    AutoUpdate,
)  # Adjust the import based on your project structure


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, AutoUpdate):
    """
    Custom User model extending AbstractUser.
    """

    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="user_images/", blank=True, null=True)
    email = models.EmailField(unique=True)  # Email as the unique identifier
    username = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True,
        help_text="This Field is not Required",
    )  # Make username optional
    name = models.CharField(max_length=255, help_text="this field is required")

    # Custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Use email as the primary identifier
    REQUIRED_FIELDS = ["username"]  # Required fields when creating a superuser

    def __str__(self):
        return self.email
