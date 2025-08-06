from django.contrib import admin
from .models import User
from apps.like.models import Like
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin for handling the extended User model.
    """

    # Fields to display in the list view
    list_display = (
        "id",
        "email",
        "name",
        "username",
        "bio",
        "image",
        "is_staff",
        "is_active"
    )
    list_filter = ("is_staff", "is_active")

    # Fields to edit in the admin panel
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",'username', "bio", "image")}),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Fields required when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "name", "bio", "image"),
            },
        ),
    )

    # User identification fields
    search_fields = ("email", "name")
    ordering = ("email",)

