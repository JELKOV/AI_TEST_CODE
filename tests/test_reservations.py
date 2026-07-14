from fastapi.testclient import TestClient

from app.main import create_app


def test_create_reservation() -> None:
    with TestClient(create_app()) as client:
        response = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "안제호",
                "starts_at": "2026-07-15T10:00:00+09:00",
                "ends_at": "2026-07-15T11:00:00+09:00",
            },
        )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "room_id": "room-a",
        "customer_name": "안제호",
        "starts_at": "2026-07-15T10:00:00+09:00",
        "ends_at": "2026-07-15T11:00:00+09:00",
    }


def test_rejects_end_time_not_after_start_time() -> None:
    with TestClient(create_app()) as client:
        response = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "안제호",
                "starts_at": "2026-07-15T10:00:00+09:00",
                "ends_at": "2026-07-15T10:00:00+09:00",
            },
        )

    assert response.status_code == 422
    assert response.json() == {"detail": "end_must_be_after_start"}


def test_rejects_overlapping_reservation_for_same_room() -> None:
    with TestClient(create_app()) as client:
        first = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "첫 번째 고객",
                "starts_at": "2026-07-15T10:00:00+09:00",
                "ends_at": "2026-07-15T11:00:00+09:00",
            },
        )
        overlapping = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "두 번째 고객",
                "starts_at": "2026-07-15T10:30:00+09:00",
                "ends_at": "2026-07-15T11:30:00+09:00",
            },
        )

    assert first.status_code == 201
    assert overlapping.status_code == 409
    assert overlapping.json() == {"detail": "reservation_conflict"}


def test_rejects_empty_room_id() -> None:
    with TestClient(create_app()) as client:
        response = client.post(
            "/reservations",
            json={
                "room_id": "",
                "customer_name": "안제호",
                "starts_at": "2026-07-15T10:00:00+09:00",
                "ends_at": "2026-07-15T11:00:00+09:00",
            },
        )

    assert response.status_code == 422


def test_lists_created_reservations() -> None:
    with TestClient(create_app()) as client:
        created = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "안제호",
                "starts_at": "2026-07-15T10:00:00+09:00",
                "ends_at": "2026-07-15T11:00:00+09:00",
            },
        )
        response = client.get("/reservations")

    assert created.status_code == 201
    assert response.status_code == 200
    assert response.json() == [created.json()]


def test_allows_adjacent_reservation_for_same_room() -> None:
    with TestClient(create_app()) as client:
        first = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "첫 번째 고객",
                "starts_at": "2026-07-15T10:00:00+09:00",
                "ends_at": "2026-07-15T11:00:00+09:00",
            },
        )
        adjacent = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "두 번째 고객",
                "starts_at": "2026-07-15T11:00:00+09:00",
                "ends_at": "2026-07-15T12:00:00+09:00",
            },
        )

    assert first.status_code == 201
    assert adjacent.status_code == 201


def test_allows_overlapping_time_for_different_room() -> None:
    with TestClient(create_app()) as client:
        first = client.post(
            "/reservations",
            json={
                "room_id": "room-a",
                "customer_name": "첫 번째 고객",
                "starts_at": "2026-07-15T10:00:00+09:00",
                "ends_at": "2026-07-15T11:00:00+09:00",
            },
        )
        another_room = client.post(
            "/reservations",
            json={
                "room_id": "room-b",
                "customer_name": "두 번째 고객",
                "starts_at": "2026-07-15T10:30:00+09:00",
                "ends_at": "2026-07-15T11:30:00+09:00",
            },
        )

    assert first.status_code == 201
    assert another_room.status_code == 201
