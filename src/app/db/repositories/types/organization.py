from __future__ import annotations
from typing import NotRequired, TypedDict

from app.db.models.enums import OrganizationStatus


class OrganizationCreate(TypedDict):
    name: str


class OrganizationUpdate(TypedDict, total=False):
    name: NotRequired[str]
    status: NotRequired[OrganizationStatus]