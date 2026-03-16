from __future__ import annotations

from app.db.gateway import DBGateway
from app.services.rbac.constants import PERMISSIONS


async def seed_permissions(gw: DBGateway) -> None:
    repo = gw.permissions()

    for code, description in PERMISSIONS:
        existing = await repo.get_by_code(code)
        if existing:
            continue

        await repo.create(
            {
                "code": code,
                "description": description,
            }
        )