from uuid import uuid4

import pytest
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from apps.outbox.models import OutboxEvent
from apps.outbox.rabbitmq import RabbitMQPublisher


class FakeChannel:
    def __init__(self):
        self.exchange_arguments = None
        self.publish_arguments = None
        self.confirmed = False

    def exchange_declare(self, **kwargs):
        self.exchange_arguments = kwargs

    def confirm_delivery(self):
        self.confirmed = True

    def basic_publish(self, **kwargs):
        self.publish_arguments = kwargs
        return True


class FakeConnection:
    def __init__(self, channel):
        self.channel_instance = channel
        self.closed = False

    def channel(self):
        return self.channel_instance

    def close(self):
        self.closed = True


class FakePika:
    @staticmethod
    def URLParameters(value):
        return value

    @staticmethod
    def BasicProperties(**kwargs):
        return kwargs


@pytest.mark.django_db
def test_rabbitmq_publisher_emits_durable_confirmed_event_message():
    event = OutboxEvent.objects.create(
        aggregate_type="order",
        aggregate_id=uuid4(),
        event_type="order.created",
        payload={"order_id": str(uuid4())},
        available_at=timezone.now(),
    )
    channel = FakeChannel()
    connection = FakeConnection(channel)
    publisher = RabbitMQPublisher(
        url="amqp://example",
        exchange="marketplace.events",
        connection_factory=lambda parameters: connection,
        pika_module=FakePika,
    )

    publisher.publish(event=event)

    assert connection.closed
    assert channel.confirmed
    assert channel.exchange_arguments == {
        "exchange": "marketplace.events",
        "exchange_type": "topic",
        "durable": True,
    }
    assert channel.publish_arguments["routing_key"] == "order.created"
    assert channel.publish_arguments["mandatory"]
    assert channel.publish_arguments["properties"]["delivery_mode"] == 2
    assert channel.publish_arguments["properties"]["message_id"] == str(event.id)


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_request_id_is_echoed_and_metrics_are_exposed_in_development(client):
    request_id = uuid4()

    response = client.get(reverse("healthz"), HTTP_X_REQUEST_ID=str(request_id))
    metrics_response = client.get(reverse("metrics"))

    assert response.status_code == 200
    assert response["X-Request-ID"] == str(request_id)
    assert metrics_response.status_code == 200
    assert b"http_requests_total" in metrics_response.content


@pytest.mark.django_db
@override_settings(DEBUG=False, METRICS_BEARER_TOKEN="metrics-token")
def test_metrics_requires_a_bearer_token_outside_development(client):
    denied_response = client.get(reverse("metrics"))
    granted_response = client.get(
        reverse("metrics"),
        HTTP_AUTHORIZATION="Bearer metrics-token",
    )

    assert denied_response.status_code == 404
    assert granted_response.status_code == 200
