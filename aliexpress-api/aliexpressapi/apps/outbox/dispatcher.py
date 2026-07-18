from dataclasses import dataclass
from datetime import timedelta
from typing import Protocol

from django.utils import timezone

from apps.outbox.models import OutboxEvent
from apps.outbox.repositories import OutboxRepository


class OutboxPublisher(Protocol):
    def publish(self, *, event: OutboxEvent) -> None: ...


@dataclass(frozen=True)
class DispatchResult:
    claimed: int = 0
    published: int = 0
    retried: int = 0
    failed: int = 0
    reclaimed: int = 0


class OutboxDispatcher:
    def __init__(
        self,
        repository: OutboxRepository,
        *,
        max_attempts: int = 5,
        retry_base_seconds: int = 30,
        lease_seconds: int = 300,
        clock=timezone.now,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if retry_base_seconds < 1:
            raise ValueError("retry_base_seconds must be at least 1")
        if lease_seconds < 1:
            raise ValueError("lease_seconds must be at least 1")

        self.repository = repository
        self.max_attempts = max_attempts
        self.retry_base_seconds = retry_base_seconds
        self.lease_seconds = lease_seconds
        self.clock = clock

    def dispatch_available(self, *, publisher: OutboxPublisher, limit: int = 100):
        if limit < 1:
            raise ValueError("limit must be at least 1")

        now = self.clock()
        reclaimed = self.repository.reclaim_expired_claims(
            before=now - timedelta(seconds=self.lease_seconds),
            available_at=now,
        )
        events = self.repository.claim_available(limit=limit, now=now)
        result = DispatchResult(claimed=len(events), reclaimed=reclaimed)

        for event in events:
            try:
                publisher.publish(event=event)
            except Exception as error:
                status = self.repository.record_failure(
                    event_id=event.id,
                    error=str(error),
                    retry_at=now + timedelta(seconds=self._retry_delay(event.attempts)),
                    max_attempts=self.max_attempts,
                )
                if status == OutboxEvent.Status.FAILED:
                    result = DispatchResult(
                        claimed=result.claimed,
                        published=result.published,
                        retried=result.retried,
                        failed=result.failed + 1,
                        reclaimed=result.reclaimed,
                    )
                else:
                    result = DispatchResult(
                        claimed=result.claimed,
                        published=result.published,
                        retried=result.retried + 1,
                        failed=result.failed,
                        reclaimed=result.reclaimed,
                    )
            else:
                self.repository.mark_published(event_id=event.id, published_at=self.clock())
                result = DispatchResult(
                    claimed=result.claimed,
                    published=result.published + 1,
                    retried=result.retried,
                    failed=result.failed,
                    reclaimed=result.reclaimed,
                )

        return result

    def _retry_delay(self, attempts: int) -> int:
        return self.retry_base_seconds * (2 ** (attempts - 1))
