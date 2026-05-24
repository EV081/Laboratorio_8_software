from fastapi.testclient import TestClient

from restaurant_service.application.register_dinner import RegisterDinnerUseCase
from restaurant_service.domain.model.dinner import Dinner
from restaurant_service.domain.ports.dinner_publisher import DinnerPublisher
from restaurant_service.infrastructure.rest.api import create_app


class _FakePublisher(DinnerPublisher):
    def __init__(self) -> None:
        self.published: list[Dinner] = []

    def publish(self, dinner: Dinner) -> None:
        self.published.append(dinner)


def _client() -> tuple[TestClient, _FakePublisher]:
    publisher = _FakePublisher()
    use_case = RegisterDinnerUseCase(publisher)
    app = create_app(use_case)
    return TestClient(app), publisher


def test_post_dinners_returns_202_and_publishes():
    client, publisher = _client()
    response = client.post(
        "/dinners",
        json={
            "amount": "120.50",
            "card_number": "4111111111111111",
            "restaurant_code": "REST-001",
            "occurred_at": "2026-05-24T19:30:00",
        },
    )
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert len(publisher.published) == 1
    assert publisher.published[0].restaurant_code == "REST-001"


def test_post_dinners_rejects_negative_amount():
    client, _ = _client()
    response = client.post(
        "/dinners",
        json={
            "amount": "-5",
            "card_number": "C1",
            "restaurant_code": "R1",
            "occurred_at": "2026-05-24T19:30:00",
        },
    )
    assert response.status_code == 422


def test_post_dinners_rejects_missing_fields():
    client, _ = _client()
    response = client.post("/dinners", json={"amount": "10"})
    assert response.status_code == 422


def test_health_endpoint():
    client, _ = _client()
    assert client.get("/health").json() == {"status": "ok"}


def test_post_dinners_returns_400_when_domain_rejects_whitespace_card():
    client, _ = _client()
    response = client.post(
        "/dinners",
        json={
            "amount": "10",
            "card_number": "   ",
            "restaurant_code": "R1",
            "occurred_at": "2026-05-24T19:30:00",
        },
    )
    assert response.status_code == 400
    assert "card_number" in response.json()["detail"]
