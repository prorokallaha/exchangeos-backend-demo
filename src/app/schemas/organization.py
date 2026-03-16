from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class OrganizationOut(BaseModel):
    id: UUID
    name: str