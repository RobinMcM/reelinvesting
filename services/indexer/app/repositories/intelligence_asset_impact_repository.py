from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.intelligence_asset_impact import IntelligenceAssetImpact


class IntelligenceAssetImpactRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def insert_many(self, impacts: list[IntelligenceAssetImpact]) -> None:
        for impact in impacts:
            self.session.add(impact)
        self.session.flush()

    def get_by_event_id(self, event_id: uuid.UUID) -> list[IntelligenceAssetImpact]:
        return list(
            self.session.execute(
                select(IntelligenceAssetImpact).where(
                    IntelligenceAssetImpact.event_id == event_id
                )
            ).scalars()
        )
