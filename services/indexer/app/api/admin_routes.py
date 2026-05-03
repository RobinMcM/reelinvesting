from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, Query

from app.api.schemas import (
    AdminStatsResponse,
    AgitatorProfileResponse,
    AssetImpactResponse,
    CreateAgitatorRequest,
    IntelligenceEventDetailResponse,
    IntelligenceEventResponse,
    UpdateAgitatorRequest,
    UpdateEventStatusRequest,
)
from app.db import SessionLocal
from app.models.agitator_profile import AgitatorProfile
from app.repositories.agitator_profile_repository import AgitatorProfileRepository
from app.repositories.intelligence_asset_impact_repository import IntelligenceAssetImpactRepository
from app.repositories.intelligence_event_repository import IntelligenceEventRepository

router = APIRouter(prefix="/admin", tags=["admin"])


# ---------------------------------------------------------------------------
# Agitator profiles
# ---------------------------------------------------------------------------

@router.get("/agitators", response_model=list[AgitatorProfileResponse])
def list_agitators() -> list[AgitatorProfileResponse]:
    with SessionLocal() as session:
        repo = AgitatorProfileRepository(session)
        profiles = repo.get_all()
        return [AgitatorProfileResponse.model_validate(p) for p in profiles]


@router.post("/agitators", response_model=AgitatorProfileResponse, status_code=201)
def create_agitator(body: CreateAgitatorRequest) -> AgitatorProfileResponse:
    with SessionLocal() as session:
        repo = AgitatorProfileRepository(session)
        profile = AgitatorProfile(
            name=body.name,
            platform=body.platform,
            handle=body.handle,
            influence_category=body.influence_category,
            default_asset_scope=body.default_asset_scope,
            enabled=body.enabled,
            priority=body.priority,
            notes=body.notes,
        )
        repo.insert(profile)
        session.commit()
        session.refresh(profile)
        return AgitatorProfileResponse.model_validate(profile)


@router.patch("/agitators/{agitator_id}", response_model=AgitatorProfileResponse)
def update_agitator(agitator_id: uuid.UUID, body: UpdateAgitatorRequest) -> AgitatorProfileResponse:
    with SessionLocal() as session:
        repo = AgitatorProfileRepository(session)
        profile = repo.get_by_id(agitator_id)
        if profile is None:
            raise HTTPException(status_code=404, detail="Agitator not found")

        updates = body.model_dump(exclude_none=True)
        repo.update_fields(profile, **updates)
        session.commit()
        session.refresh(profile)
        return AgitatorProfileResponse.model_validate(profile)


# ---------------------------------------------------------------------------
# Events (admin view — all statuses, full detail)
# ---------------------------------------------------------------------------

@router.get("/events", response_model=list[IntelligenceEventResponse])
def list_events_admin(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> list[IntelligenceEventResponse]:
    with SessionLocal() as session:
        repo = IntelligenceEventRepository(session)
        events = repo.get_all_admin(limit=limit, offset=offset)
        return [IntelligenceEventResponse.model_validate(e) for e in events]


@router.get("/events/{event_id}", response_model=IntelligenceEventDetailResponse)
def get_event_admin(event_id: uuid.UUID) -> IntelligenceEventDetailResponse:
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


@router.patch("/events/{event_id}/status", response_model=IntelligenceEventResponse)
def update_event_status(
    event_id: uuid.UUID, body: UpdateEventStatusRequest
) -> IntelligenceEventResponse:
    with SessionLocal() as session:
        repo = IntelligenceEventRepository(session)
        event = repo.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        repo.update_fields(event, status=body.status)
        session.commit()
        session.refresh(event)
        return IntelligenceEventResponse.model_validate(event)


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

@router.get("/stats", response_model=AdminStatsResponse)
def get_stats() -> AdminStatsResponse:
    with SessionLocal() as session:
        repo = IntelligenceEventRepository(session)
        by_status = repo.count_by_status()
        by_source_type = repo.count_by_source_type()
        total = sum(by_status.values())
        last_published_at = repo.get_latest_published_at()

    return AdminStatsResponse(
        total_events=total,
        events_by_status=by_status,
        events_by_source_type=by_source_type,
        last_published_at=last_published_at,
    )
