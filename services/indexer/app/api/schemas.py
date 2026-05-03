from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import (
    AssetType,
    EventStatus,
    InfluenceCategory,
    ImpactDirection,
    SourceType,
    TimeHorizon,
)


# ---------------------------------------------------------------------------
# Shared config
# ---------------------------------------------------------------------------

class _Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# IntelligenceSource
# ---------------------------------------------------------------------------

class IntelligenceSourceResponse(_Base):
    id: uuid.UUID
    name: str
    source_type: SourceType
    provider: Optional[str]
    base_url: Optional[str]
    auth_required: bool
    polling_interval_seconds: int
    enabled: bool
    priority: int
    config_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class CreateSourceRequest(BaseModel):
    name: str
    source_type: SourceType
    provider: Optional[str] = None
    base_url: Optional[str] = None
    auth_required: bool = False
    polling_interval_seconds: int = 300
    enabled: bool = True
    priority: int = 50
    config_json: Dict[str, Any] = {}


class UpdateSourceRequest(BaseModel):
    name: Optional[str] = None
    source_type: Optional[SourceType] = None
    provider: Optional[str] = None
    base_url: Optional[str] = None
    auth_required: Optional[bool] = None
    polling_interval_seconds: Optional[int] = None
    enabled: Optional[bool] = None
    priority: Optional[int] = None
    config_json: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# AgitatorProfile
# ---------------------------------------------------------------------------

class AgitatorProfileResponse(_Base):
    id: uuid.UUID
    name: str
    platform: str
    handle: Optional[str]
    influence_category: InfluenceCategory
    default_asset_scope: List[Any]
    enabled: bool
    priority: int
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class CreateAgitatorRequest(BaseModel):
    name: str
    platform: str
    handle: Optional[str] = None
    influence_category: InfluenceCategory
    default_asset_scope: List[Any] = []
    enabled: bool = True
    priority: int = 50
    notes: Optional[str] = None


class UpdateAgitatorRequest(BaseModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    handle: Optional[str] = None
    influence_category: Optional[InfluenceCategory] = None
    default_asset_scope: Optional[List[Any]] = None
    enabled: Optional[bool] = None
    priority: Optional[int] = None
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# IntelligenceAssetImpact
# ---------------------------------------------------------------------------

class AssetImpactResponse(_Base):
    id: uuid.UUID
    event_id: uuid.UUID
    symbol: str
    asset_type: AssetType
    direction: ImpactDirection
    impact_score: int
    confidence: int
    time_horizon: TimeHorizon
    reason: Optional[str]
    created_at: datetime


# ---------------------------------------------------------------------------
# IntelligenceEvent
# ---------------------------------------------------------------------------

class IntelligenceEventResponse(_Base):
    id: uuid.UUID
    source_type: SourceType
    source_name: str
    external_id: Optional[str]
    stable_id: str
    title: str
    body_preview: Optional[str]
    url: Optional[str]
    published_at: datetime
    spaces_key: str
    event_type: Optional[str]
    asset_type: AssetType
    tickers: List[Any]
    sectors: List[Any]
    entities: List[Any]
    newsworthiness: Optional[int]
    attention_score: Optional[int]
    virality_score: Optional[int]
    market_relevance: Optional[int]
    impact_rating: Optional[int]
    confidence: Optional[int]
    status: EventStatus
    created_at: datetime
    updated_at: datetime


class IntelligenceEventDetailResponse(IntelligenceEventResponse):
    asset_impacts: List[AssetImpactResponse] = []


class UpdateEventStatusRequest(BaseModel):
    status: EventStatus


# ---------------------------------------------------------------------------
# Admin stats
# ---------------------------------------------------------------------------

class AdminStatsResponse(BaseModel):
    total_events: int
    events_by_status: Dict[str, int]
    events_by_source_type: Dict[str, int]
    last_published_at: Optional[datetime]
