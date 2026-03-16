from __future__ import annotations

from app.db.gateway import DBGateway

PERMISSIONS: list[tuple[str, str]] = [
    ("org.members.manage", "Manage organization members"),
    ("org.roles.manage", "Manage organization roles"),
    ("org.settings.manage", "Manage organization settings"),
    ("stats.org.read", "Read organization statistics"),
    ("orders.create", "Create orders"),
    ("orders.read_own", "Read own orders"),
    ("orders.read_all", "Read all organization orders"),
    ("orders.update_own", "Update own orders"),
    ("orders.update_all", "Update all organization orders"),
    ("requisites.read", "Read payment requisites"),
    ("requisites.manage", "Manage payment requisites"),
    ("ledger.read", "Read ledger data"),
]


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