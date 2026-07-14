from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_openapi_schema_is_available(client):
    response = client.get(reverse("schema"))

    assert response.status_code == 200
    assert "openapi" in response.content.decode()


@pytest.mark.django_db
def test_health_endpoints_are_available(client):
    assert client.get(reverse("healthz")).json() == {"status": "ok"}
    assert client.get(reverse("readyz")).json() == {"status": "ok"}
