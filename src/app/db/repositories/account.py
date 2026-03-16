from __future__ import annotations

import uuid

from app.db.models.account import Account
from app.db.models.enums import AccountType
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.account import AccountCreate, AccountUpdate


class AccountRepository(BaseRepository):
    @property
    def model(self) -> type[Account]:
        return Account

    async def get_by_id(self, account_id: uuid.UUID) -> Account | None:
        return await self._crud.select(Account.id == account_id)

    async def list_by_org(self, organization_id: uuid.UUID) -> list[Account]:
        return list(await self._crud.select_many(Account.organization_id == organization_id))

    async def get_internal_by_currency(
        self,
        organization_id: uuid.UUID,
        currency: str,
    ) -> Account | None:
        return await self._crud.select(
            self.model.organization_id == organization_id,
            self.model.type == AccountType.INTERNAL,
            self.model.currency == currency,
            self.model.is_active.is_(True),
        )

    async def create(self, data: AccountCreate) -> Account | None:
        return await self._crud.insert(**data)

    async def update(self, account_id: uuid.UUID, data: AccountUpdate) -> Account | None:
        rows = await self._crud.update(Account.id == account_id, **data)
        return rows[0] if rows else None