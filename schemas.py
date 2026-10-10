
from typing import Literal

from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):
    in_scope: bool = Field(
        description="True only for non-clinical hospital operations requests."
    )

    scope_reason: str = Field(
        description="Short reason the request is in or out of CareFlow scope."
    )

    plain_language_explanation: str = Field(
        description=(
            "A natural-language response for the user. "
            "For in-scope requests, explain the issue and next step. "
            "For out-of-scope requests, politely decline and invite "
            "a hospital operations request."
        )
    )

    category: Literal[
        "Equipment",
        "Bed and Transfer",
        "Staffing",
        "Facilities",
        "Supplies",
        "Other",
    ] = "Other"

    summary: str = Field(
        description="Short factual summary of the operational request."
    )

    urgency: Literal["Low", "Medium", "High"] = "Low"

    reason: str = Field(
        description="Evidence supporting the suggested operational urgency."
    )

    missing_information: list[str] = Field(default_factory=list)

    suggested_action: str = Field(
        description="Suggested non-clinical operational action."
    )

    requires_human_review: bool = True
