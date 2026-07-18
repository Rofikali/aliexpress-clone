import hmac

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from apps.outbox.models import OutboxEvent
from components.observability.metrics import OUTBOX_EVENTS


@require_GET
def metrics(request):
    if not settings.DEBUG:
        token = settings.METRICS_BEARER_TOKEN
        authorization = request.headers.get("Authorization", "")
        if not token or not hmac.compare_digest(authorization, f"Bearer {token}"):
            return HttpResponseNotFound()

    for status in OutboxEvent.Status.values:
        OUTBOX_EVENTS.labels(status=status).set(0)

    event_counts = OutboxEvent.objects.values("status").annotate(count=Count("id"))
    for event_count in event_counts:
        OUTBOX_EVENTS.labels(status=event_count["status"]).set(event_count["count"])

    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
