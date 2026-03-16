from __future__ import annotations

from typing import NotRequired, TypedDict
import uuid

from app.db.models.enums import AccountType


class AccountCreate(TypedDict):
    organization_id: uuid.UUID
    type: AccountType
    currency: str
    name: str
    meta: dict
    is_active: bool


class AccountUpdate(TypedDict, total=False):
    name: NotRequired[str]
    meta: NotRequired[dict]
    is_active: NotRequired[bool]