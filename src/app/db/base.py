from __future__ import annotations

from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


ModelType = TypeVar("ModelType", bound=Base)
