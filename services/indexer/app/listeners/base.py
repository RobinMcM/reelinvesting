from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from app.models.enums import SourceType


@dataclass
class RawIntelligenceItem:
    source_type: SourceType
    source_name: str
    title: str
    raw_payload: dict = field(default_factory=dict)
    external_id: str | None = None
    body: str | None = None
    body_preview: str | None = None
    url: str | None = None
    published_at: datetime | None = None
    content: str | None = None
    agitator_name: str | None = None
    platform: str | None = None
    handle: str | None = None


class IntelligenceListener(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str: ...

    @property
    @abstractmethod
    def source_type(self) -> SourceType: ...

    @abstractmethod
    def fetch_latest(self) -> list[RawIntelligenceItem]: ...
