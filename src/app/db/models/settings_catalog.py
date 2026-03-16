from __future__ import annotations

import uuid

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.enums import SettingScope, SettingValueType
from app.db.models.mixins import TimestampMixin


class SettingsCatalog(Base, TimestampMixin):
    __tablename__ = "settings_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    key: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    scope: Mapped[SettingScope] = mapped_column(Enum(SettingScope, name="setting_scope"), nullable=False, default=SettingScope.ORGANIZATION)
    value_type: Mapped[SettingValueType] = mapped_column(Enum(SettingValueType, name="setting_value_type"), nullable=False)

    default_value: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    description: Mapped[str] = mapped_column(String(255), nullable=False, default="")