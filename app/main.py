from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


PRESENTATION_PATH = Path(__file__).with_name("presentation.html")


class ReservationCreate(BaseModel):
    room_id: str = Field(min_length=1)
    customer_name: str
    starts_at: datetime
    ends_at: datetime


class Reservation(ReservationCreate):
    id: int


def create_app() -> FastAPI:
    application = FastAPI(title="AI-TDD Reservation API")
    reservations: list[Reservation] = []

    @application.get("/", include_in_schema=False)
    def presentation() -> FileResponse:
        return FileResponse(PRESENTATION_PATH)

    @application.post(
        "/reservations",
        response_model=Reservation,
        status_code=status.HTTP_201_CREATED,
    )
    def create_reservation(payload: ReservationCreate) -> Reservation:
        if payload.ends_at <= payload.starts_at:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="end_must_be_after_start",
            )
        reservation = Reservation(id=len(reservations) + 1, **payload.model_dump())
        has_conflict = any(
            current.room_id == reservation.room_id
            and reservation.starts_at < current.ends_at
            and current.starts_at < reservation.ends_at
            for current in reservations
        )
        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="reservation_conflict",
            )
        reservations.append(reservation)
        return reservation

    @application.get("/reservations", response_model=list[Reservation])
    def list_reservations() -> list[Reservation]:
        return reservations

    return application


app = create_app()
