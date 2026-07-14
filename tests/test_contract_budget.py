from fastapi.testclient import TestClient

from app.main import create_app


def test_accepts_confirmed_budget_with_production_and_total_amounts() -> None:
    payload = {
        "budget_type": "CONFIRMED_AMOUNT",
        "production_cost": 80_000_000,
        "total_budget": 250_000_000,
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/budget/validate", json=payload)

    assert response.status_code == 200
    assert response.json() == payload


def test_rejects_confirmed_amount_mixed_with_budget_ranges() -> None:
    payload = {
        "budget_type": "CONFIRMED_AMOUNT",
        "production_cost": 80_000_000,
        "total_budget": 250_000_000,
        "production_budget_range": "RANGE_50M_150M_KRW",
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/budget/validate", json=payload)

    assert response.status_code == 422
    assert "confirmed amount cannot include budget ranges" in response.text
