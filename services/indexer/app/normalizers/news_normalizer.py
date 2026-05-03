import re
from dataclasses import dataclass
from datetime import datetime, timezone

from app.listeners.base import RawNewsArticle
from app.logging_config import get_logger
from app.utils.hashing import stable_hash

logger = get_logger(__name__)


@dataclass
class NormalizedNewsArticle:
    source: str
    external_id: str | None
    stable_id: str
    headline: str
    summary: str | None
    url: str | None
    published_at: datetime
    content: str | None
    raw_payload: dict
    ingested_at: datetime


def _clean_headline(headline: str) -> str:
    return re.sub(r"\s+", " ", headline).strip()


def _ensure_tz(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _make_stable_id(source: str, external_id: str | None, url: str | None, headline: str) -> str:
    if external_id:
        raw = f"{source}:{external_id}"
    elif url:
        raw = f"{source}:{url}"
    else:
        raw = f"{source}:{headline}"
    return stable_hash(raw)


class NewsNormalizer:
    def normalize(self, raw: RawNewsArticle) -> NormalizedNewsArticle | None:
        try:
            headline = _clean_headline(raw.headline)
            if not headline:
                logger.warning("empty_headline_skipped", source=raw.source)
                return None

            return NormalizedNewsArticle(
                source=raw.source,
                external_id=raw.external_id,
                stable_id=_make_stable_id(raw.source, raw.external_id, raw.url, headline),
                headline=headline,
                summary=raw.summary,
                url=raw.url,
                published_at=_ensure_tz(raw.published_at),
                content=raw.content,
                raw_payload=raw.raw_payload,
                ingested_at=datetime.now(timezone.utc),
            )
        except Exception:
            logger.exception("normalization_failed", source=raw.source, headline=getattr(raw, "headline", ""))
            return None
