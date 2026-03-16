from __future__ import annotations

from collections.abc import AsyncIterator

from app.core.config import settings
from app.db.core.connection import create_engine, create_session_factory
from app.db.core.manager import TransactionManager
from app.db.gateway import DBGateway

engine = create_engine(settings.db_url, pool_pre_ping=True)
SessionFactory = create_session_factory(engine)


async def get_gateway() -> AsyncIterator[DBGateway]:
    async with DBGateway(TransactionManager(SessionFactory)) as gateway:
        yield gateway
