from __future__ import annotations

from app.db.models.audit_log import AuditLog
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.audit_log import AuditLogCreate


class AuditLogRepository(BaseRepository):
    @property
    def model(self) -> type[AuditLog]:
        return AuditLog

    async def create(self, data: AuditLogCreate) -> AuditLog | None:
        return await self._crud.insert(**data)