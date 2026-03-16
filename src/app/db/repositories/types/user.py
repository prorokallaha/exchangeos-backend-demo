from __future__ import annotations
from typing import NotRequired, TypedDict
import uuid

from app.db.models.enums import UserStatus


class UserCreate(TypedDict):
    login: str
    display_name: str
    password_hash: str
    is_platform_admin: bool


class UserUpdate(TypedDict, total=False):
    display_name: NotRequired[str]
    password_hash: NotRequired[str]
    status: NotRequired[UserStatus]