from app.classifiers.event_classifier import EventClassifier
from app.db import SessionLocal
from app.listeners.base import NewsListener, RawNewsArticle
from app.logging_config import get_logger
from app.models.article_asset_impact import ArticleAssetImpact
from app.models.news_article import ArticleStatus, NewsArticleIndex
from app.normalizers.news_normalizer import NewsNormalizer
from app.repositories.article_impact_repository import ArticleImpactRepository
from app.repositories.news_article_repository import NewsArticleRepository
from app.spaces.article_store import ArticleStore

logger = get_logger(__name__)


class NewsIngestionWorker:
    def __init__(self, listeners: list[NewsListener]) -> None:
        self._listeners = listeners
        self._normalizer = NewsNormalizer()
        self._classifier = EventClassifier()
        self._store = ArticleStore()

    def run(self) -> None:
        logger.info("ingestion_cycle_started")
        for listener in self._listeners:
            try:
                self._process_listener(listener)
            except Exception:
                logger.exception("listener_failed", source=listener.source_name)
        logger.info("ingestion_cycle_complete")

    def _process_listener(self, listener: NewsListener) -> None:
        raw_articles = listener.fetch_latest()
        logger.info("articles_fetched", source=listener.source_name, count=len(raw_articles))

        with SessionLocal() as session:
            repo = NewsArticleRepository(session)
            impact_repo = ArticleImpactRepository(session)

            for raw in raw_articles:
                try:
                    self._process_article(raw, repo, impact_repo)
                    session.commit()
                except Exception:
                    session.rollback()
                    logger.exception("article_processing_failed", headline=getattr(raw, "headline", ""))

    def _process_article(
        self,
        raw: RawNewsArticle,
        repo: NewsArticleRepository,
        impact_repo: ArticleImpactRepository,
    ) -> None:
        normalized = self._normalizer.normalize(raw)
        if normalized is None:
            return

        if repo.exists_by_stable_id(normalized.stable_id):
            logger.debug("article_duplicate_skipped", stable_id=normalized.stable_id)
            return

        spaces_key: str | None = None
        try:
            payload = {
                "source": normalized.source,
                "external_id": normalized.external_id,
                "stable_id": normalized.stable_id,
                "headline": normalized.headline,
                "summary": normalized.summary,
                "url": normalized.url,
                "published_at": normalized.published_at.isoformat(),
                "content": normalized.content,
                "raw_payload": normalized.raw_payload,
                "ingested_at": normalized.ingested_at.isoformat(),
            }
            result = self._store.store(
                stable_id=normalized.stable_id,
                source=normalized.source,
                published_at=normalized.published_at,
                payload=payload,
            )
            spaces_key = result or None
        except Exception:
            logger.exception("spaces_upload_failed", stable_id=normalized.stable_id)

        article = NewsArticleIndex(
            source=normalized.source,
            external_id=normalized.external_id,
            stable_id=normalized.stable_id,
            headline=normalized.headline,
            summary=normalized.summary,
            url=normalized.url,
            published_at=normalized.published_at,
            spaces_key=spaces_key,
            status=ArticleStatus.STORED if spaces_key else ArticleStatus.RAW,
        )
        repo.insert(article)

        classification = self._classifier.classify(normalized.headline, normalized.summary)

        repo.update_classification(
            article,
            asset_type=classification.asset_type,
            tickers=classification.tickers,
            sectors=classification.sectors,
            newsworthiness=classification.newsworthiness,
            market_relevance=classification.market_relevance,
            impact_rating=classification.impact_rating,
            confidence=classification.confidence,
            status=ArticleStatus.CLASSIFIED,
        )

        impact_repo.insert_many([
            ArticleAssetImpact(
                article_id=article.id,
                symbol=impact.symbol,
                asset_type=impact.asset_type,
                direction=impact.direction,
                impact_score=impact.impact_score,
                confidence=impact.confidence,
                time_horizon=impact.time_horizon,
                reason=impact.reason,
            )
            for impact in classification.asset_impacts
        ])

        logger.info(
            "article_indexed",
            stable_id=normalized.stable_id,
            headline=normalized.headline,
            asset_type=classification.asset_type.value,
            tickers=classification.tickers,
            status=ArticleStatus.CLASSIFIED.value,
        )
