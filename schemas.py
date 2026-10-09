from datetime import datetime
from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    code: str = Field(min_length=1, max_length=50000)
    filename: str = Field(
        default="submitted_code.py",
        max_length=255
    )


class ReviewResponse(BaseModel):
    id: int
    filename: str
    status: str
    findings: list[dict]
    ai_report: str
    suggested_fix: str
    created_at: datetime


class ReviewSummary(BaseModel):
    id: int
    filename: str
    status: str
    created_at: datetime