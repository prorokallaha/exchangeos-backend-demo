from __future__ import annotations

from types import TracebackType
from typing import Optional, Type, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction, async_sessionmaker


class CommitError(Exception):
    pass


class RollbackError(Exception):
    pass


class TransactionManager:
    __slots__ = ("session", "_transaction")

    def __init__(self, session_or_factory: Union[AsyncSession, async_sessionmaker[AsyncSession]]) -> None:
        if isinstance(session_or_factory, async_sessionmaker):
            self.session = session_or_factory()
        else:
            self.session = session_or_factory

        self._transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> "TransactionManager":
        if not self.session.in_transaction() and self.session.is_active:
            self._transaction = await self.session.begin()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        except SQLAlchemyError as err:
            if exc_type:
                raise RollbackError from err
            raise CommitError from err
        finally:
            if self.session.is_active:
                await self.session.close()
