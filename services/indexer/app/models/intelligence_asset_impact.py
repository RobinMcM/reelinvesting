from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.enums import AssetType, ImpactDirection, TimeHorizon


def _now() -> datetime:
    return datetime.now(timezone.utc)


class IntelligenceAssetImpact(Base):
    __tablename__ = "intelligence_asset_impact"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("intelligence_event.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    # create_type=False: asset_type_enum PG type is already created by intelligence_event
    asset_type: Mapped[AssetType] = mapped_column(
        SAEnum(AssetType, name="asset_type_enum", create_type=False), nullable=False
    )
    # direction describes possible market impact only — NOT a buy/sell recommendation
    direction: Mapped[ImpactDirection] = mapped_column(
        SAEnum(ImpactDirection, name="impact_direction_enum", create_type=False), nullable=False
    )
    impact_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confidence: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time_horizon: Mapped[TimeHorizon] = mapped_column(
        SAEnum(TimeHorizon, name="time_horizon_enum", create_type=False), nullable=False, default=TimeHorizon.UNKNOWN
    )
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
