from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agitator_profile import AgitatorProfile


class AgitatorProfileRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[AgitatorProfile]:
        return list(self.session.execute(select(AgitatorProfile)).scalars())

    def get_enabled(self) -> list[AgitatorProfile]:
        return list(
            self.session.execute(
                select(AgitatorProfile).where(AgitatorProfile.enabled == True)  # noqa: E712
            ).scalars()
        )

    def get_by_id(self, agitator_id: uuid.UUID) -> AgitatorProfile | None:
        return self.session.get(AgitatorProfile, agitator_id)

    def get_by_name(self, name: str) -> AgitatorProfile | None:
        return self.session.execute(
            select(AgitatorProfile).where(AgitatorProfile.name == name)
        ).scalar_one_or_none()

    def insert(self, profile: AgitatorProfile) -> AgitatorProfile:
        self.session.add(profile)
        self.session.flush()
        return profile

    def update_fields(self, profile: AgitatorProfile, **fields: Any) -> None:
        for key, value in fields.items():
            setattr(profile, key, value)
        self.session.flush()
