from __future__ import annotations

import signal
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from app.api.admin_routes import router as admin_router
from app.api.event_routes import router as event_router
from app.api.health_routes import router as health_router
from app.api.source_routes import router as source_router
from app.config import settings
from app.listeners.mock_agitator_listener import MockAgitatorListener
from app.listeners.mock_news_listener import MockNewsListener
from app.logging_config import configure_logging, get_logger
from app.workers.intelligence_ingestion_worker import IntelligenceIngestionWorker

configure_logging()
logger = get_logger(__name__)


def _build_worker() -> IntelligenceIngestionWorker:
    listeners = []

    if settings.ENABLE_MOCK_NEWS:
        listeners.append(MockNewsListener())
        logger.info("listener_enabled", listener="MockNewsListener")

    if settings.ENABLE_MOCK_AGITATORS:
        listeners.append(MockAgitatorListener())
        logger.info("listener_enabled", listener="MockAgitatorListener")

    if not listeners:
        logger.warning("no_listeners_configured")

    return IntelligenceIngestionWorker(listeners=listeners)


def _run_ingestion(worker: IntelligenceIngestionWorker) -> None:
    try:
        worker.run()
    except Exception:
        logger.exception("ingestion_cycle_error")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    worker = _build_worker()
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        _run_ingestion,
        args=[worker],
        trigger="interval",
        seconds=settings.INGESTION_INTERVAL_SECONDS,
        id="intelligence_ingestion",
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
    logger.info(
        "scheduler_started",
        interval_seconds=settings.INGESTION_INTERVAL_SECONDS,
    )

    if settings.RUN_ON_STARTUP:
        logger.info("running_ingestion_on_startup")
        _run_ingestion(worker)

    yield

    logger.info("indexer_shutting_down")
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="ReelInvesting Market Intelligence Indexer",
    description=(
        "Pure intelligence indexing service. "
        "Gathers, stores, and classifies market-relevant information. "
        "Does NOT execute trades, generate buy/sell signals, or connect to brokers."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(event_router)
app.include_router(source_router)
app.include_router(admin_router)


def _handle_signal(signum: int, frame: object) -> None:
    logger.info("signal_received", signum=signum)
    sys.exit(0)


signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGINT, _handle_signal)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False,
        log_config=None,
    )
