from django.contrib import admin
from apps.accounts.models.user import User
from apps.accounts.models.device import UserDevice as device
from apps.accounts.models.password_reset import PasswordResetToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "role",
        "kyc_status",
        "is_staff",
        "is_active",
        "last_login",
        "created_at",
    )
    list_filter = ("role", "kyc_status", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username", "phone_number")}),
        ("Role & KYC", {"fields": ("role", "kyc_status")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        # remove created_at and updated_at from editable fieldsets
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "kyc_status",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)

    # 👇 this is the correct way to display non-editable fields
    readonly_fields = ("created_at", "updated_at", "last_login")


@admin.register(device)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "device_type",
        "device_token",
        "ip_address",
        "last_active",
        "created_at",
    )
    list_filter = ("device_type", "created_at", "last_active")
    search_fields = ("user__email", "device_token", "ip_address")
    ordering = ("-last_active",)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "token",
        "created_at",
        "expires_at",
        "used",
    )
    list_filter = ("used", "expires_at")
    search_fields = ("user__email", "token")
    ordering = ("-created_at",)
