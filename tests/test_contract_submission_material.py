from fastapi.testclient import TestClient

from app.main import create_app


def test_rejects_attached_material_without_file_id() -> None:
    payload = {
        "material_type": "NDA",
        "format_type": "ATTACHED_FORMAT",
    }

    with TestClient(create_app()) as client:
        response = client.post("/contracts/submission-material/validate", json=payload)

    assert response.status_code == 422
    assert "file_id required for attached format" in response.text
