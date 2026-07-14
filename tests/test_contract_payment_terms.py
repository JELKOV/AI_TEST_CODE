from fastapi.testclient import TestClient

from app.main import create_app


def test_accepts_valid_contract_payment_terms() -> None:
    payload = {
        "advance_payment_percentage": 30,
        "interim_payment_percentage": 30,
        "final_payment_percentage": 40,
        "advance_timing": "CONTRACT_SIGNED",
        "interim_timing": "PLAN_CONFIRMED",
        "final_timing": "FINAL_DELIVERY",
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/payment-terms/validate", json=payload)

    assert response.status_code == 200
    assert response.json() == payload


def test_rejects_payment_percentage_sum_not_100() -> None:
    payload = {
        "advance_payment_percentage": 20,
        "interim_payment_percentage": 30,
        "final_payment_percentage": 40,
        "advance_timing": "CONTRACT_SIGNED",
        "interim_timing": "PLAN_CONFIRMED",
        "final_timing": "FINAL_DELIVERY",
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/payment-terms/validate", json=payload)

    assert response.status_code == 422
    assert "payment percentages must sum to 100" in response.text


def test_rejects_negative_payment_percentage_even_when_sum_is_100() -> None:
    payload = {
        "advance_payment_percentage": -10,
        "interim_payment_percentage": 50,
        "final_payment_percentage": 60,
        "advance_timing": "CONTRACT_SIGNED",
        "interim_timing": "PLAN_CONFIRMED",
        "final_timing": "FINAL_DELIVERY",
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/payment-terms/validate", json=payload)

    assert response.status_code == 422
    assert "greater than or equal to 0" in response.text


def test_rejects_duplicate_payment_timings() -> None:
    payload = {
        "advance_payment_percentage": 30,
        "interim_payment_percentage": 30,
        "final_payment_percentage": 40,
        "advance_timing": "CONTRACT_SIGNED",
        "interim_timing": "CONTRACT_SIGNED",
        "final_timing": "FINAL_DELIVERY",
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/payment-terms/validate", json=payload)

    assert response.status_code == 422
    assert "payment timing values must be unique" in response.text


def test_rejects_reversed_payment_timing_order() -> None:
    payload = {
        "advance_payment_percentage": 30,
        "interim_payment_percentage": 30,
        "final_payment_percentage": 40,
        "advance_timing": "PLAN_CONFIRMED",
        "interim_timing": "CONTRACT_SIGNED",
        "final_timing": "FINAL_DELIVERY",
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/payment-terms/validate", json=payload)

    assert response.status_code == 422
    assert "advance payment timing must not be later than interim or final" in response.text


def test_openapi_exposes_three_contract_rule_demo_routes() -> None:
    with TestClient(create_app()) as client:
        schema = client.get("/openapi.json").json()

    assert set(schema["paths"]) == {
        "/contracts/payment-terms/validate",
        "/contracts/budget/validate",
        "/contracts/submission-material/validate",
    }
    assert "/reservations" not in schema["paths"]
    assert schema["info"]["title"] == "AI-TDD AdMarket Contract API"
