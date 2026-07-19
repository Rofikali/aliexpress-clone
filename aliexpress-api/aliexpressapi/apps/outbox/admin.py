from django.contrib import admin

from apps.outbox.models import OutboxEvent


@admin.register(OutboxEvent)
class OutboxEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event_type",
        "aggregate_type",
        "status",
        "attempts",
        "manual_replay_count",
        "available_at",
        "created_at",
    )
    list_filter = ("status", "event_type", "aggregate_type")
    search_fields = ("id", "aggregate_id", "event_type")
    readonly_fields = (
        "id",
        "aggregate_type",
        "aggregate_id",
        "event_type",
        "payload",
        "status",
        "attempts",
        "available_at",
        "processing_started_at",
        "published_at",
        "last_error",
        "manual_replay_count",
        "last_replayed_at",
        "last_replay_reason",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
