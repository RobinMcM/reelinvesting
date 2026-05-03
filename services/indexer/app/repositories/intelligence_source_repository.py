from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.intelligence_source import IntelligenceSource


class IntelligenceSourceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[IntelligenceSource]:
        return list(self.session.execute(select(IntelligenceSource)).scalars())

    def get_enabled(self) -> list[IntelligenceSource]:
        return list(
            self.session.execute(
                select(IntelligenceSource).where(IntelligenceSource.enabled == True)  # noqa: E712
            ).scalars()
        )

    def get_by_id(self, source_id: uuid.UUID) -> IntelligenceSource | None:
        return self.session.get(IntelligenceSource, source_id)

    def insert(self, source: IntelligenceSource) -> IntelligenceSource:
        self.session.add(source)
        self.session.flush()
        return source

    def update_fields(self, source: IntelligenceSource, **fields: Any) -> None:
        for key, value in fields.items():
            setattr(source, key, value)
        self.session.flush()
