from __future__ import annotations

from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest

from app.config import settings
from app.listeners.base import IntelligenceListener, RawIntelligenceItem
from app.logging_config import get_logger
from app.models.enums import SourceType

logger = get_logger(__name__)


class AlpacaNewsListener(IntelligenceListener):
    """Fetches recent news articles from the Alpaca market data API.

    Uses news/data endpoints only. No trading client, no orders, no broker access.
    """

    @property
    def source_name(self) -> str:
        return "alpaca_news"

    @property
    def source_type(self) -> SourceType:
        return SourceType.NEWS

    def __init__(self) -> None:
        self._client = NewsClient(
            api_key=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
        )
        self._symbols: list[str] = [
            s.strip() for s in settings.ALPACA_NEWS_SYMBOLS.split(",") if s.strip()
        ]
        self._limit = settings.ALPACA_NEWS_LIMIT

    def fetch_latest(self) -> list[RawIntelligenceItem]:
        try:
            request = NewsRequest(
                symbols=",".join(self._symbols),
                limit=self._limit,
            )
            response = self._client.get_news(request)
            articles = self._extract_articles(response)
        except Exception:
            logger.exception(
                "alpaca_news_fetch_failed",
                source_name=self.source_name,
            )
            return []

        items: list[RawIntelligenceItem] = []
        for article in articles:
            item = self._to_raw_item(article)
            if item is not None:
                items.append(item)

        logger.info(
            "alpaca_news_fetched",
            count=len(items),
            symbols=self._symbols,
        )
        return items

    def _extract_articles(self, response: object) -> list[object]:
        """Pull the list of News objects out of whatever NewsSet shape alpaca-py returns."""
        # NewsSet.data is a dict with key 'news'
        if hasattr(response, "data") and isinstance(response.data, dict):
            return response.data.get("news", [])
        # Fallback: dict-like
        if isinstance(response, dict):
            return response.get("news", [])
        # Fallback: iterable (older SDK versions)
        try:
            return list(response)
        except TypeError:
            return []

    def _to_raw_item(self, article: object) -> RawIntelligenceItem | None:
        try:
            headline: str = getattr(article, "headline", "") or ""
            if not headline.strip():
                return None

            external_id: str | None = None
            raw_id = getattr(article, "id", None)
            if raw_id is not None:
                external_id = str(raw_id)

            summary: str | None = getattr(article, "summary", None) or None
            url: str | None = getattr(article, "url", None) or None
            published_at = getattr(article, "created_at", None)
            symbols: list[str] = getattr(article, "symbols", None) or []
            author: str | None = getattr(article, "author", None) or None
            source: str | None = getattr(article, "source", None) or None
            content: str | None = getattr(article, "content", None) or None

            raw_payload: dict = {
                "id": raw_id,
                "headline": headline,
                "summary": summary,
                "url": url,
                "author": author,
                "source": source,
                "symbols": symbols,
                "created_at": published_at.isoformat() if published_at else None,
            }

            return RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id=external_id,
                title=headline,
                body=content or None,
                body_preview=summary,
                url=url,
                published_at=published_at,
                raw_payload=raw_payload,
            )
        except Exception:
            logger.exception(
                "alpaca_news_article_conversion_failed",
                source_name=self.source_name,
                article_id=getattr(article, "id", None),
            )
            return None
