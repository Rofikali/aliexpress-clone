from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "notification_type", "user", "created_at", "read_at")
    list_filter = ("notification_type", "read_at")
    search_fields = ("id", "event_id", "user__email")
    readonly_fields = ("id", "event_id", "user", "notification_type", "payload", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
