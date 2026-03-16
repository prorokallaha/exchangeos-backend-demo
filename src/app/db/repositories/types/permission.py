from __future__ import annotations

from typing import NotRequired, TypedDict


class PermissionCreate(TypedDict):
    code: str
    description: str


class PermissionUpdate(TypedDict, total=False):
    description: NotRequired[str]