import uuid

from django.db import models
from django.utils import timezone


class OutboxEvent(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING"
        PROCESSING = "PROCESSING"
        PUBLISHED = "PUBLISHED"
        FAILED = "FAILED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aggregate_type = models.CharField(max_length=64)
    aggregate_id = models.UUIDField()
    event_type = models.CharField(max_length=128)
    payload = models.JSONField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    attempts = models.PositiveIntegerField(default=0)
    available_at = models.DateTimeField(default=timezone.now, db_index=True)
    processing_started_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    manual_replay_count = models.PositiveIntegerField(default=0)
    last_replayed_at = models.DateTimeField(null=True, blank=True)
    last_replay_reason = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["aggregate_type", "aggregate_id", "event_type"],
                name="outbox_unique_aggregate_event",
            )
        ]
        indexes = [
            models.Index(fields=["status", "available_at"]),
        ]
