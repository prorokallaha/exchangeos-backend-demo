from __future__ import annotations

import abc
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import ModelType
from app.db.repositories.crud import CRUDRepository


class BaseRepository:
    __slots__ = ("_session", "_crud")

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = CRUDRepository(session, self.model)

    @property
    @abc.abstractmethod
    def model(self) -> Type[ModelType]:
        raise NotImplementedError
