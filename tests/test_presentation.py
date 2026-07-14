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
