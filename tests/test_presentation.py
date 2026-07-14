from fastapi.testclient import TestClient

from app.main import create_app


def test_serves_presentation_lab() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "AI가 구현 속도를 높이고" in response.text


def test_presentation_links_to_primary_sources() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "https://newsletter.kentbeck.com/p/canon-tdd" in response.text
    assert "https://fastapi.tiangolo.com/tutorial/testing/" in response.text
    assert 'href="/docs"' in response.text


def test_presentation_connects_video_to_ai_tdd_workflow() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "AAd8taPTyTM" in response.text
    assert "t=137s" in response.text
    assert "계획 → RED → GREEN → REFACTOR → 검증" in response.text


def test_presentation_runs_admarket_contract_payment_scenarios() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "AdMarket Contract Payment Terms" in response.text
    assert "POST /contracts/payment-terms/validate" in response.text
    assert "Valid Terms (정상 지급조건)" in response.text
    assert "Invalid Total (합계 오류)" in response.text
    assert "Invalid Order (순서 오류)" in response.text
