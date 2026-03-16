from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.db.models.enums import RequisiteKind


class PaymentRequisiteCreateIn(BaseModel):
    kind: RequisiteKind
    label: str = Field(min_length=1, max_length=128)
    currency: str = Field(min_length=1, max_length=16)
    details: dict
    limits: dict


class PaymentRequisiteUpdateIn(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=128)
    details: dict | None = None
    limits: dict | None = None
    is_active: bool | None = None


class PaymentRequisiteOut(BaseModel):
    id: UUID
    organization_id: UUID
    kind: RequisiteKind
    label: str
    currency: str
    details: dict
    limits: dict
    is_active: bool
    created_by_member_id: UUID | None