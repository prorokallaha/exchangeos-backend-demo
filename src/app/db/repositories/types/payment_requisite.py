from __future__ import annotations

from typing import NotRequired, TypedDict
import uuid

from app.db.models.enums import RequisiteKind


class PaymentRequisiteCreate(TypedDict):
    organization_id: uuid.UUID
    kind: RequisiteKind
    label: str
    currency: str
    details: dict
    limits: dict
    is_active: bool
    created_by_member_id: NotRequired[uuid.UUID | None]


class PaymentRequisiteUpdate(TypedDict, total=False):
    label: NotRequired[str]
    details: NotRequired[dict]
    limits: NotRequired[dict]
    is_active: NotRequired[bool]