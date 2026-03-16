from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.enums import UserStatus


class UserCreateIn(BaseModel):
    login: str = Field(min_length=3, max_length=64)
    display_name: str = Field(min_length=1, max_length=128)
    password_hash: str = Field(min_length=1, max_length=255)
    is_platform_admin: bool = False


class UserUpdateIn(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=128)
    status: UserStatus | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    login: str
    display_name: str
    status: UserStatus
    is_platform_admin: bool