from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.enums import AssetType, EventStatus, SourceType


def _now() -> datetime:
    return datetime.now(timezone.utc)


class IntelligenceEvent(Base):
    __tablename__ = "intelligence_event"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("intelligence_source.id", ondelete="SET NULL"),
        nullable=True,
    )
    agitator_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agitator_profile.id", ondelete="SET NULL"),
        nullable=True,
    )
    # create_type=False: source_type_enum PG type is already created by intelligence_source
    source_type: Mapped[SourceType] = mapped_column(
        SAEnum(SourceType, name="source_type_enum", create_type=False), nullable=False
    )
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    stable_id: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    body_preview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    spaces_key: Mapped[str] = mapped_column(String(512), nullable=False, default="")

    # Descriptive classification — not trading signals
    event_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    asset_type: Mapped[AssetType] = mapped_column(
        SAEnum(AssetType, name="asset_type_enum", create_type=False), nullable=False, default=AssetType.UNKNOWN
    )
    tickers: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=list)
    sectors: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=list)
    entities: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=list)

    # Descriptive scores — not trading recommendations
    newsworthiness: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    attention_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    virality_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    market_relevance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    impact_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    confidence: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    status: Mapped[EventStatus] = mapped_column(
        SAEnum(EventStatus, name="event_status_enum", create_type=False), nullable=False, default=EventStatus.RAW
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    __table_args__ = (
        Index(
            "ix_intelligence_event_source_external_id",
            "source_name",
            "external_id",
            unique=True,
            postgresql_where="external_id IS NOT NULL",
        ),
        Index("ix_intelligence_event_source_type", "source_type"),
        Index("ix_intelligence_event_published_at", "published_at"),
        Index("ix_intelligence_event_status", "status"),
    )
