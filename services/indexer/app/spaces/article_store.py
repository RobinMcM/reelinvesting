import json
from datetime import datetime

from app.config import settings
from app.logging_config import get_logger
from app.spaces.client import get_spaces_client

logger = get_logger(__name__)


class ArticleStore:
    def __init__(self) -> None:
        self._configured = bool(
            settings.DO_SPACES_BUCKET
            and settings.DO_SPACES_ACCESS_KEY_ID
            and settings.DO_SPACES_ENDPOINT
        )
        if self._configured:
            self._client = get_spaces_client()
        self._bucket = settings.DO_SPACES_BUCKET

    def store(self, stable_id: str, source: str, published_at: datetime, payload: dict) -> str:
        if not self._configured:
            logger.debug("spaces_not_configured_skipping", stable_id=stable_id)
            return ""

        date_path = published_at.strftime("%Y/%m/%d")
        key = f"articles/{date_path}/{source}/{stable_id}.json"

        self._client.put_object(
            Bucket=self._bucket,
            Key=key,
            Body=json.dumps(payload, default=str, ensure_ascii=False).encode("utf-8"),
            ContentType="application/json",
        )

        logger.info("article_stored_to_spaces", key=key)
        return key
