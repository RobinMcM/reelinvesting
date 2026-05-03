from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

from app.listeners.base import RawIntelligenceItem
from app.logging_config import get_logger
from app.models.enums import SourceType
from app.utils.hashing import stable_hash

logger = get_logger(__name__)

_PREVIEW_MAX_LEN = 500


@dataclass
class NormalizedIntelligenceItem:
    source_type: SourceType
    source_name: str
    stable_id: str
    title: str
    external_id: str | None
    body_preview: str | None
    url: str | None
    published_at: datetime
    content: str | None
    raw_payload: dict
    agitator_name: str | None
    platform: str | None
    handle: str | None
    ingested_at: datetime


def _clean_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip()


def _make_preview(body: str | None, preview: str | None, title: str) -> str | None:
    text = body or preview
    if not text:
        return None
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= _PREVIEW_MAX_LEN:
        return cleaned
    return cleaned[:_PREVIEW_MAX_LEN].rsplit(" ", 1)[0] + "…"


def _ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _make_stable_id(
    source_type: SourceType,
    source_name: str,
    external_id: str | None,
    url: str | None,
    title: str,
    body_preview: str | None,
) -> str:
    if external_id:
        raw = f"{source_type.value}:{source_name}:{external_id}"
    elif url:
        raw = f"{source_type.value}:{source_name}:{url}"
    else:
        raw = f"{source_type.value}:{source_name}:{title}:{body_preview or ''}"
    return stable_hash(raw)


class IntelligenceNormalizer:
    def normalize(self, raw: RawIntelligenceItem) -> NormalizedIntelligenceItem | None:
        try:
            title = _clean_title(raw.title)
            if not title:
                logger.warning("empty_title_skipped", source_name=raw.source_name)
                return None

            body_preview = _make_preview(raw.body, raw.body_preview, title)
            published_at = _ensure_utc(raw.published_at) if raw.published_at else datetime.now(timezone.utc)
            stable_id = _make_stable_id(
                raw.source_type, raw.source_name, raw.external_id, raw.url, title, body_preview
            )

            return NormalizedIntelligenceItem(
                source_type=raw.source_type,
                source_name=raw.source_name,
                external_id=raw.external_id,
                stable_id=stable_id,
                title=title,
                body_preview=body_preview,
                url=raw.url,
                published_at=published_at,
                content=raw.content,
                raw_payload=raw.raw_payload,
                agitator_name=raw.agitator_name,
                platform=raw.platform,
                handle=raw.handle,
                ingested_at=datetime.now(timezone.utc),
            )
        except Exception:
            logger.exception(
                "normalization_failed",
                source_name=getattr(raw, "source_name", ""),
                title=getattr(raw, "title", ""),
            )
            return None
