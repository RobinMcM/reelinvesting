from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.enums import AssetType, EventStatus, SourceType
from app.models.intelligence_event import IntelligenceEvent


class IntelligenceEventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def exists_by_stable_id(self, stable_id: str) -> bool:
        return (
            self.session.execute(
                select(IntelligenceEvent.id).where(IntelligenceEvent.stable_id == stable_id)
            ).first()
            is not None
        )

    def insert(self, event: IntelligenceEvent) -> IntelligenceEvent:
        self.session.add(event)
        self.session.flush()
        return event

    def update_fields(self, event: IntelligenceEvent, **fields: Any) -> None:
        for key, value in fields.items():
            setattr(event, key, value)
        self.session.flush()

    def get_by_id(self, event_id: uuid.UUID) -> IntelligenceEvent | None:
        return self.session.get(IntelligenceEvent, event_id)

    def get_recent(self, limit: int = 50, offset: int = 0) -> list[IntelligenceEvent]:
        return list(
            self.session.execute(
                select(IntelligenceEvent)
                .order_by(desc(IntelligenceEvent.published_at))
                .limit(limit)
                .offset(offset)
            ).scalars()
        )

    def get_high_impact(self, min_score: int = 60, limit: int = 50) -> list[IntelligenceEvent]:
        return list(
            self.session.execute(
                select(IntelligenceEvent)
                .where(IntelligenceEvent.market_relevance >= min_score)
                .order_by(desc(IntelligenceEvent.market_relevance))
                .limit(limit)
            ).scalars()
        )

    def get_by_source_type(
        self, source_type: SourceType, limit: int = 50, offset: int = 0
    ) -> list[IntelligenceEvent]:
        return list(
            self.session.execute(
                select(IntelligenceEvent)
                .where(IntelligenceEvent.source_type == source_type)
                .order_by(desc(IntelligenceEvent.published_at))
                .limit(limit)
                .offset(offset)
            ).scalars()
        )

    def get_by_symbol(self, symbol: str, limit: int = 50) -> list[IntelligenceEvent]:
        upper = symbol.upper()
        return list(
            self.session.execute(
                select(IntelligenceEvent)
                .where(IntelligenceEvent.tickers.contains([upper]))
                .order_by(desc(IntelligenceEvent.published_at))
                .limit(limit)
            ).scalars()
        )

    def get_all_admin(self, limit: int = 100, offset: int = 0) -> list[IntelligenceEvent]:
        return list(
            self.session.execute(
                select(IntelligenceEvent)
                .order_by(desc(IntelligenceEvent.created_at))
                .limit(limit)
                .offset(offset)
            ).scalars()
        )

    def count_by_status(self) -> dict[str, int]:
        rows = self.session.execute(
            select(IntelligenceEvent.status, func.count(IntelligenceEvent.id))
            .group_by(IntelligenceEvent.status)
        ).all()
        return {str(row[0].value): row[1] for row in rows}

    def count_by_source_type(self) -> dict[str, int]:
        rows = self.session.execute(
            select(IntelligenceEvent.source_type, func.count(IntelligenceEvent.id))
            .group_by(IntelligenceEvent.source_type)
        ).all()
        return {str(row[0].value): row[1] for row in rows}

    def get_latest_published_at(self) -> datetime | None:
        result = self.session.execute(
            select(func.max(IntelligenceEvent.published_at))
        ).scalar()
        return result
