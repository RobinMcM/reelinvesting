from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException

from app.api.schemas import CreateSourceRequest, IntelligenceSourceResponse, UpdateSourceRequest
from app.db import SessionLocal
from app.models.intelligence_source import IntelligenceSource
from app.repositories.intelligence_source_repository import IntelligenceSourceRepository

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[IntelligenceSourceResponse])
def list_sources() -> list[IntelligenceSourceResponse]:
    with SessionLocal() as session:
        repo = IntelligenceSourceRepository(session)
        sources = repo.get_all()
        return [IntelligenceSourceResponse.model_validate(s) for s in sources]


@router.post("", response_model=IntelligenceSourceResponse, status_code=201)
def create_source(body: CreateSourceRequest) -> IntelligenceSourceResponse:
    with SessionLocal() as session:
        repo = IntelligenceSourceRepository(session)
        source = IntelligenceSource(
            name=body.name,
            source_type=body.source_type,
            provider=body.provider,
            base_url=body.base_url,
            auth_required=body.auth_required,
            polling_interval_seconds=body.polling_interval_seconds,
            enabled=body.enabled,
            priority=body.priority,
            config_json=body.config_json,
        )
        repo.insert(source)
        session.commit()
        session.refresh(source)
        return IntelligenceSourceResponse.model_validate(source)


@router.patch("/{source_id}", response_model=IntelligenceSourceResponse)
def update_source(source_id: uuid.UUID, body: UpdateSourceRequest) -> IntelligenceSourceResponse:
    with SessionLocal() as session:
        repo = IntelligenceSourceRepository(session)
        source = repo.get_by_id(source_id)
        if source is None:
            raise HTTPException(status_code=404, detail="Source not found")

        updates = body.model_dump(exclude_none=True)
        repo.update_fields(source, **updates)
        session.commit()
        session.refresh(source)
        return IntelligenceSourceResponse.model_validate(source)
