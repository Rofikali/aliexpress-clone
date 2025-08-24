from django.contrib import admin
from .models import User, UserDevice, PasswordResetToken

# from django.contrib import admin
# from .models import User
# # from apps.like.models import Like
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     """
#     Custom User admin for handling the extended User model.
#     """

#     # Fields to display in the list view
#     list_display = (
#         "id",
#         "email",
#         "name",
#         "username",
#         "bio",
#         "image",
#         "is_staff",
#         "is_active"
#     )
#     list_filter = ("is_staff", "is_active")

#     # Fields to edit in the admin panel
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (_("Personal Info"), {"fields": ("name",'username', "bio", "image")}),
#         (
#             _("Permissions"),
#             {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )

#     # Fields required when creating a new user
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2", "name", "bio", "image"),
#             },
#         ),
#     )

#     # User identification fields
#     search_fields = ("email", "name")
#     ordering = ("email",)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "email",
#         "username",
#         "role",
#         "kyc_status",
#         "is_staff",
#         "is_active",
#         "last_login",
#         "created_at",
#     )
#     list_filter = ("role", "kyc_status", "is_staff", "is_active")
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Personal Info", {"fields": ("username", "phone_number")}),
#         ("Role & KYC", {"fields": ("role", "kyc_status")}),
#         ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
#         ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("email", "username", "password1", "password2", "role", "kyc_status"),
#         }),
#     )
#     search_fields = ("email", "username")
#     ordering = ("email",)

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
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        # remove created_at and updated_at from editable fieldsets
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "role", "kyc_status"),
        }),
    )
    search_fields = ("email", "username")
    ordering = ("email",)

    # 👇 this is the correct way to display non-editable fields
    readonly_fields = ("created_at", "updated_at", "last_login")


@admin.register(UserDevice)
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