import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.news_article import AssetType


class ImpactDirection(str, enum.Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    UNCERTAIN = "UNCERTAIN"


class TimeHorizon(str, enum.Enum):
    INTRADAY = "INTRADAY"
    ONE_DAY = "ONE_DAY"
    ONE_WEEK = "ONE_WEEK"
    LONG_TERM = "LONG_TERM"
    UNKNOWN = "UNKNOWN"


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ArticleAssetImpact(Base):
    __tablename__ = "article_asset_impact"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("news_article_index.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(
        SAEnum(AssetType, name="asset_type"), nullable=False
    )
    direction: Mapped[ImpactDirection] = mapped_column(
        SAEnum(ImpactDirection, name="impact_direction"), nullable=False
    )
    impact_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confidence: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time_horizon: Mapped[TimeHorizon] = mapped_column(
        SAEnum(TimeHorizon, name="time_horizon"), nullable=False, default=TimeHorizon.UNKNOWN
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
