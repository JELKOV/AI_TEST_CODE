from enum import StrEnum
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, model_validator


PRESENTATION_PATH = Path(__file__).with_name("presentation.html")


class ContractPaymentTiming(StrEnum):
    CONTRACT_SIGNED = "CONTRACT_SIGNED"
    PLAN_CONFIRMED = "PLAN_CONFIRMED"
    SHOOTING_COMPLETED = "SHOOTING_COMPLETED"
    FINAL_DELIVERY = "FINAL_DELIVERY"


class ContractPaymentTerms(BaseModel):
    advance_payment_percentage: int
    interim_payment_percentage: int
    final_payment_percentage: int
    advance_timing: ContractPaymentTiming
    interim_timing: ContractPaymentTiming
    final_timing: ContractPaymentTiming

    @model_validator(mode="after")
    def validate_payment_terms(self) -> "ContractPaymentTerms":
        total = (
            self.advance_payment_percentage
            + self.interim_payment_percentage
            + self.final_payment_percentage
        )
        if total != 100:
            raise ValueError("payment percentages must sum to 100")

        timings = [self.advance_timing, self.interim_timing, self.final_timing]
        if len(set(timings)) != len(timings):
            raise ValueError("payment timing values must be unique")

        timing_order = {
            ContractPaymentTiming.CONTRACT_SIGNED: 0,
            ContractPaymentTiming.PLAN_CONFIRMED: 1,
            ContractPaymentTiming.SHOOTING_COMPLETED: 2,
            ContractPaymentTiming.FINAL_DELIVERY: 3,
        }
        timings = [self.advance_timing, self.interim_timing, self.final_timing]
        positions = [timing_order[timing] for timing in timings]
        if positions != sorted(positions):
            raise ValueError(
                "advance payment timing must not be later than interim or final"
            )
        return self


def create_app() -> FastAPI:
    application = FastAPI(title="AI-TDD AdMarket Contract API")

    @application.get("/", include_in_schema=False)
    def presentation() -> FileResponse:
        return FileResponse(PRESENTATION_PATH)

    @application.post(
        "/contracts/payment-terms/validate",
        response_model=ContractPaymentTerms,
    )
    def validate_contract_payment_terms(payload: ContractPaymentTerms) -> ContractPaymentTerms:
        return payload

    return application


app = create_app()
