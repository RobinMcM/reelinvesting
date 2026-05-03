import enum
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Enum as SAEnum, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AssetType(str, enum.Enum):
    STOCK = "STOCK"
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    COMMODITY = "COMMODITY"
    INDEX = "INDEX"
    MACRO = "MACRO"
    UNKNOWN = "UNKNOWN"


class ArticleStatus(str, enum.Enum):
    RAW = "RAW"
    STORED = "STORED"
    CLASSIFIED = "CLASSIFIED"
    IGNORED = "IGNORED"
    ERROR = "ERROR"


def _now() -> datetime:
    return datetime.now(timezone.utc)


class NewsArticleIndex(Base):
    __tablename__ = "news_article_index"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    external_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    stable_id: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    headline: Mapped[str] = mapped_column(String(1024), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    spaces_key: Mapped[str | None] = mapped_column(String(512), nullable=True)

    asset_type: Mapped[AssetType] = mapped_column(
        SAEnum(AssetType, name="asset_type"), nullable=False, default=AssetType.UNKNOWN
    )
    tickers: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=list)
    sectors: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=list)

    newsworthiness: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    market_relevance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    impact_rating: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confidence: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    status: Mapped[ArticleStatus] = mapped_column(
        SAEnum(ArticleStatus, name="article_status"), nullable=False, default=ArticleStatus.RAW
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)

    __table_args__ = (
        Index(
            "ix_news_article_source_external_id",
            "source",
            "external_id",
            unique=True,
            postgresql_where="external_id IS NOT NULL",
        ),
    )
