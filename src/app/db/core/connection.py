from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

SessionFactory = async_sessionmaker[AsyncSession]


def create_engine(db_url: str, **kwargs: Any) -> AsyncEngine:
    return create_async_engine(db_url, **kwargs)


def create_session_factory(engine: AsyncEngine) -> SessionFactory:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
