from fastapi import APIRouter
from sqlalchemy import text

from app.db import SessionLocal
from app.logging_config import get_logger

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "reelinvesting-market-intelligence-indexer"}


@router.get("/health/db")
def health_db() -> dict:
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as exc:
        logger.error("db_health_check_failed", error=str(exc))
        return {"status": "error", "db": "unreachable", "detail": str(exc)}
