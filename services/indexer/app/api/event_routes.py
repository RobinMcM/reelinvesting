from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, Query

from app.api.schemas import AssetImpactResponse, IntelligenceEventDetailResponse, IntelligenceEventResponse
from app.db import SessionLocal
from app.models.enums import SourceType
from app.repositories.intelligence_asset_impact_repository import IntelligenceAssetImpactRepository
from app.repositories.intelligence_event_repository import IntelligenceEventRepository

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/recent", response_model=list[IntelligenceEventResponse])
def get_recent_events(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[IntelligenceEventResponse]:
    with SessionLocal() as session:
        repo = IntelligenceEventRepository(session)
        events = repo.get_recent(limit=limit, offset=offset)
        return [IntelligenceEventResponse.model_validate(e) for e in events]


@router.get("/high-impact", response_model=list[IntelligenceEventResponse])
def get_high_impact_events(
    min_score: int = Query(60, ge=0, le=100),
    limit: int = Query(50, ge=1, le=200),
) -> list[IntelligenceEventResponse]:
    with SessionLocal() as session:
        repo = IntelligenceEventRepository(session)
        events = repo.get_high_impact(min_score=min_score, limit=limit)
        return [IntelligenceEventResponse.model_validate(e) for e in events]


@router.get("/source-type/{source_type}", response_model=list[IntelligenceEventResponse])
def get_events_by_source_type(
    source_type: SourceType,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[IntelligenceEventResponse]:
    with SessionLocal() as session:
        repo = IntelligenceEventRepository(session)
        events = repo.get_by_source_type(source_type=source_type, limit=limit, offset=offset)
        return [IntelligenceEventResponse.model_validate(e) for e in events]


@router.get("/asset/{symbol}", response_model=list[IntelligenceEventResponse])
def get_events_by_asset(
    symbol: str,
    limit: int = Query(50, ge=1, le=200),
) -> list[IntelligenceEventResponse]:
    with SessionLocal() as session:
        repo = IntelligenceEventRepository(session)
        events = repo.get_by_symbol(symbol=symbol.upper(), limit=limit)
        return [IntelligenceEventResponse.model_validate(e) for e in events]


@router.get("/{event_id}", response_model=IntelligenceEventDetailResponse)
def get_event(event_id: uuid.UUID) -> IntelligenceEventDetailResponse:
    with SessionLocal() as session:
        event_repo = IntelligenceEventRepository(session)
        impact_repo = IntelligenceAssetImpactRepository(session)

        event = event_repo.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        impacts = impact_repo.get_by_event_id(event_id)
        response = IntelligenceEventDetailResponse.model_validate(event)
        response.asset_impacts = [AssetImpactResponse.model_validate(i) for i in impacts]
        return response
