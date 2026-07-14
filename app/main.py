from enum import StrEnum
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, model_validator

PRESENTATION_PATH = Path(__file__).with_name("presentation.html")
TVCF_LOGO_PATH = Path(__file__).with_name("tvcfLogo.png")


class ContractPaymentTiming(StrEnum):
    CONTRACT_SIGNED = "CONTRACT_SIGNED"
    PLAN_CONFIRMED = "PLAN_CONFIRMED"
    SHOOTING_COMPLETED = "SHOOTING_COMPLETED"
    FINAL_DELIVERY = "FINAL_DELIVERY"


class ContractBudgetType(StrEnum):
    CONFIRMED_AMOUNT = "CONFIRMED_AMOUNT"


class ContractMaterialType(StrEnum):
    NDA = "NDA"
    OTHER_MATERIAL = "OTHER_MATERIAL"


class ContractMaterialFormat(StrEnum):
    FREE_FORMAT = "FREE_FORMAT"
    ATTACHED_FORMAT = "ATTACHED_FORMAT"


class ContractSubmissionMaterial(BaseModel):
    material_type: ContractMaterialType
    format_type: ContractMaterialFormat
    file_id: str | None = None

    @model_validator(mode="after")
    def validate_attached_file(self) -> "ContractSubmissionMaterial":
        if self.format_type == ContractMaterialFormat.ATTACHED_FORMAT and not self.file_id:
            raise ValueError("file_id required for attached format")
        return self


class ContractBudget(BaseModel):
    budget_type: ContractBudgetType
    production_cost: int = Field(..., ge=0)
    total_budget: int = Field(..., ge=0)
    production_budget_range: str | None = None
    total_budget_range: str | None = None
    campaign_scale: str | None = None

    @model_validator(mode="after")
    def validate_budget_shape(self) -> "ContractBudget":
        proposal_fields = (
            self.production_budget_range,
            self.total_budget_range,
            self.campaign_scale,
        )
        if any(value is not None for value in proposal_fields):
            raise ValueError("confirmed amount cannot include budget ranges or campaign scale")
        return self


class ContractPaymentTerms(BaseModel):
    advance_payment_percentage: int = Field(..., ge=0)
    interim_payment_percentage: int = Field(..., ge=0)
    final_payment_percentage: int = Field(..., ge=0)
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
            raise ValueError("advance payment timing must not be later than interim or final")
        return self


def create_app() -> FastAPI:
    application = FastAPI(title="AI-TDD AdMarket Contract API")

    @application.get("/", include_in_schema=False)
    def presentation() -> FileResponse:
        return FileResponse(PRESENTATION_PATH)

    @application.get("/assets/tvcf-logo.png", include_in_schema=False)
    def tvcf_logo() -> FileResponse:
        return FileResponse(TVCF_LOGO_PATH, media_type="image/png")

    @application.post(
        "/contracts/payment-terms/validate",
        response_model=ContractPaymentTerms,
    )
    def validate_contract_payment_terms(payload: ContractPaymentTerms) -> ContractPaymentTerms:
        return payload

    @application.post(
        "/contracts/budget/validate",
        response_model=ContractBudget,
        response_model_exclude_none=True,
    )
    def validate_contract_budget(payload: ContractBudget) -> ContractBudget:
        return payload

    @application.post(
        "/contracts/submission-material/validate",
        response_model=ContractSubmissionMaterial,
        response_model_exclude_none=True,
    )
    def validate_contract_submission_material(
        payload: ContractSubmissionMaterial,
    ) -> ContractSubmissionMaterial:
        return payload

    return application


app = create_app()
