from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import AccountType

DEFAULT_ACCOUNTS: list[tuple[AccountType, str, str, dict]] = [
    (AccountType.INTERNAL, "RUB", "Internal RUB", {}),
    (AccountType.INTERNAL, "USDT", "Internal USDT", {}),
]


async def ensure_default_accounts(
    gw: DBGateway,
    organization_id: uuid.UUID,
) -> None:
    repo = gw.accounts()
    existing_accounts = await repo.list_by_org(organization_id)

    existing_pairs = {(account.type.value, account.currency, account.name) for account in existing_accounts}

    for account_type, currency, name, meta in DEFAULT_ACCOUNTS:
        key = (account_type.value, currency, name)
        if key in existing_pairs:
            continue

        await repo.create(
            {
                "organization_id": organization_id,
                "type": account_type,
                "currency": currency,
                "name": name,
                "meta": meta,
                "is_active": True,
            }
        )