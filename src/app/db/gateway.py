from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.core.manager import TransactionManager
from app.db.repositories.member import OrganizationMemberRepository
from app.db.repositories.organization import OrganizationRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.account import AccountRepository
from app.db.repositories.audit_log import AuditLogRepository
from app.db.repositories.ledger_entry import LedgerEntryRepository
from app.db.repositories.ledger_transaction import LedgerTransactionRepository
from app.db.repositories.order import OrderRepository
from app.db.repositories.organization_setting import OrganizationSettingRepository
from app.db.repositories.permission import PermissionRepository
from app.db.repositories.role import RoleRepository
from app.db.repositories.role_permission import RolePermissionRepository
from app.db.repositories.member_permission import MemberPermissionRepository
from app.db.repositories.payment_requisite import PaymentRequisiteRepository


class DBGateway:
    __slots__ = ("manager",)

    def __init__(self, manager: TransactionManager) -> None:
        self.manager = manager

    async def __aenter__(self) -> "DBGateway":
        await self.manager.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.manager.__aexit__(*args)

    @property
    def session(self) -> AsyncSession:
        return self.manager.session

    def users(self) -> UserRepository:
        return UserRepository(self.session)

    def organizations(self) -> OrganizationRepository:
        return OrganizationRepository(self.session)

    def members(self) -> OrganizationMemberRepository:
        return OrganizationMemberRepository(self.session)

    def roles(self) -> RoleRepository:
        return RoleRepository(self.session)

    def permissions(self) -> PermissionRepository:
        return PermissionRepository(self.session)

    def organization_settings(self) -> OrganizationSettingRepository:
        return OrganizationSettingRepository(self.session)

    def accounts(self) -> AccountRepository:
        return AccountRepository(self.session)

    def orders(self) -> OrderRepository:
        return OrderRepository(self.session)

    def ledger_transactions(self) -> LedgerTransactionRepository:
        return LedgerTransactionRepository(self.session)

    def ledger_entries(self) -> LedgerEntryRepository:
        return LedgerEntryRepository(self.session)

    def audit_logs(self) -> AuditLogRepository:
        return AuditLogRepository(self.session)

    def role_permissions(self) -> RolePermissionRepository:
        return RolePermissionRepository(self.session)

    def member_permissions(self) -> MemberPermissionRepository:
        return MemberPermissionRepository(self.session)

    def payment_requisites(self) -> PaymentRequisiteRepository:
        return PaymentRequisiteRepository(self.session)
