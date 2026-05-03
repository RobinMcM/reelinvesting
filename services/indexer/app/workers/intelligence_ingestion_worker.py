from __future__ import annotations

from datetime import datetime, timezone

from app.classifiers.rule_based_classifier import RuleBasedClassifier
from app.db import SessionLocal
from app.listeners.base import IntelligenceListener, RawIntelligenceItem
from app.logging_config import get_logger
from app.models.enums import EventStatus
from app.models.intelligence_asset_impact import IntelligenceAssetImpact
from app.models.intelligence_event import IntelligenceEvent
from app.normalizers.intelligence_normalizer import IntelligenceNormalizer, NormalizedIntelligenceItem
from app.repositories.intelligence_asset_impact_repository import IntelligenceAssetImpactRepository
from app.repositories.intelligence_event_repository import IntelligenceEventRepository
from app.spaces.intelligence_store import IntelligenceStore

logger = get_logger(__name__)


class IntelligenceIngestionWorker:
    def __init__(self, listeners: list[IntelligenceListener]) -> None:
        self._listeners = listeners
        self._normalizer = IntelligenceNormalizer()
        self._classifier = RuleBasedClassifier()
        self._store = IntelligenceStore()

    def run(self) -> None:
        logger.info("ingestion_cycle_started", listener_count=len(self._listeners))
        processed = skipped = errors = 0

        for listener in self._listeners:
            try:
                p, s, e = self._process_listener(listener)
                processed += p
                skipped += s
                errors += e
            except Exception:
                logger.exception("listener_failed", source_name=listener.source_name)
                errors += 1

        logger.info(
            "ingestion_cycle_complete",
            processed=processed,
            skipped=skipped,
            errors=errors,
        )

    def _process_listener(self, listener: IntelligenceListener) -> tuple[int, int, int]:
        raw_items = listener.fetch_latest()
        logger.info(
            "items_fetched",
            source_name=listener.source_name,
            source_type=listener.source_type.value,
            count=len(raw_items),
        )

        processed = skipped = errors = 0

        with SessionLocal() as session:
            event_repo = IntelligenceEventRepository(session)
            impact_repo = IntelligenceAssetImpactRepository(session)

            for raw in raw_items:
                try:
                    result = self._process_item(raw, event_repo, impact_repo)
                    session.commit()
                    if result == "processed":
                        processed += 1
                    elif result == "skipped":
                        skipped += 1
                except Exception:
                    session.rollback()
                    logger.exception(
                        "item_processing_failed",
                        source_name=getattr(raw, "source_name", ""),
                        title=getattr(raw, "title", ""),
                    )
                    errors += 1

        return processed, skipped, errors

    def _process_item(
        self,
        raw: RawIntelligenceItem,
        event_repo: IntelligenceEventRepository,
        impact_repo: IntelligenceAssetImpactRepository,
    ) -> str:
        # Step 1: Normalize
        normalized = self._normalizer.normalize(raw)
        if normalized is None:
            return "skipped"

        # Step 2: Deduplicate
        if event_repo.exists_by_stable_id(normalized.stable_id):
            logger.debug("duplicate_skipped", stable_id=normalized.stable_id)
            return "skipped"

        # Step 3: Store full payload to Spaces
        spaces_key = self._store_to_spaces(normalized)

        # Step 4: Insert IntelligenceEvent row
        event = IntelligenceEvent(
            source_type=normalized.source_type,
            source_name=normalized.source_name,
            external_id=normalized.external_id,
            stable_id=normalized.stable_id,
            title=normalized.title,
            body_preview=normalized.body_preview,
            url=normalized.url,
            published_at=normalized.published_at,
            spaces_key=spaces_key,
            status=EventStatus.STORED if spaces_key else EventStatus.RAW,
        )
        event_repo.insert(event)

        # Step 5: Classify descriptively
        classification = self._classifier.classify(normalized)

        # Step 6: Update classification fields
        event_repo.update_fields(
            event,
            event_type=classification.event_type,
            asset_type=classification.asset_type,
            tickers=classification.tickers,
            sectors=classification.sectors,
            entities=classification.entities,
            newsworthiness=classification.newsworthiness,
            attention_score=classification.attention_score,
            virality_score=classification.virality_score,
            market_relevance=classification.market_relevance,
            impact_rating=classification.impact_rating,
            confidence=classification.confidence,
            status=EventStatus.CLASSIFIED,
        )

        # Step 7: Save asset impact rows
        if classification.asset_impacts:
            impact_repo.insert_many([
                IntelligenceAssetImpact(
                    event_id=event.id,
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
            "event_indexed",
            stable_id=normalized.stable_id,
            source_type=normalized.source_type.value,
            source_name=normalized.source_name,
            title=normalized.title,
            event_type=classification.event_type,
            asset_type=classification.asset_type.value,
            tickers=classification.tickers,
            status=EventStatus.CLASSIFIED.value,
        )
        return "processed"

    def _store_to_spaces(self, normalized: NormalizedIntelligenceItem) -> str:
        try:
            payload = {
                "source_type": normalized.source_type.value,
                "source_name": normalized.source_name,
                "external_id": normalized.external_id,
                "stable_id": normalized.stable_id,
                "title": normalized.title,
                "body_preview": normalized.body_preview,
                "url": normalized.url,
                "published_at": normalized.published_at.isoformat(),
                "content": normalized.content,
                "raw_payload": normalized.raw_payload,
                "agitator_profile": {
                    "name": normalized.agitator_name,
                    "platform": normalized.platform,
                    "handle": normalized.handle,
                }
                if normalized.agitator_name
                else None,
                "ingested_at": normalized.ingested_at.isoformat(),
            }
            return self._store.store(
                stable_id=normalized.stable_id,
                source_type=normalized.source_type,
                source_name=normalized.source_name,
                published_at=normalized.published_at,
                payload=payload,
            )
        except Exception:
            logger.exception("spaces_upload_failed", stable_id=normalized.stable_id)
            return ""
