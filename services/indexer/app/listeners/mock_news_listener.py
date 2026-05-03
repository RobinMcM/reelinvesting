from datetime import datetime, timedelta, timezone

from app.listeners.base import IntelligenceListener, RawIntelligenceItem
from app.models.enums import SourceType


class MockNewsListener(IntelligenceListener):
    @property
    def source_name(self) -> str:
        return "mock_news"

    @property
    def source_type(self) -> SourceType:
        return SourceType.NEWS

    def fetch_latest(self) -> list[RawIntelligenceItem]:
        now = datetime.now(timezone.utc)

        return [
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-news-001",
                title="Nvidia raises Q4 earnings guidance on surging AI chip demand",
                body=(
                    "Nvidia has raised its Q4 earnings guidance, citing record demand for its H100 and "
                    "upcoming H200 AI accelerators. CEO Jensen Huang attributed the surge to hyperscaler "
                    "spending on AI infrastructure."
                ),
                url="https://example.com/nvidia-earnings-guidance",
                published_at=now - timedelta(minutes=15),
                content="Full article content about Nvidia earnings guidance.",
                raw_payload={"mock": True, "source": "mock_news"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-news-002",
                title="OPEC+ announces surprise 1 million barrel per day oil output cut",
                body=(
                    "OPEC+ has announced an unexpected reduction of 1 million barrels per day, citing "
                    "concerns over global demand weakness and US inventory builds. Oil prices jumped 4% "
                    "on the news."
                ),
                url="https://example.com/opec-oil-cut",
                published_at=now - timedelta(minutes=45),
                content="Full article content about oil supply disruption.",
                raw_payload={"mock": True, "source": "mock_news"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-news-003",
                title="Federal Reserve holds rates steady, signals two cuts in 2025",
                body=(
                    "The Federal Reserve kept its benchmark interest rate unchanged at 5.25%-5.50%, "
                    "but the dot plot now indicates two 25 basis point cuts expected in 2025, "
                    "sending bond yields lower and equities higher."
                ),
                url="https://example.com/fed-rate-decision",
                published_at=now - timedelta(hours=2),
                content="Full article content about Federal Reserve rate decision.",
                raw_payload={"mock": True, "source": "mock_news"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-news-004",
                title="Apple faces supply chain disruption as Taiwan supplier halts production",
                body=(
                    "A key Apple supplier in Taiwan has halted production at two facilities due to "
                    "equipment failures, raising concerns over iPhone 16 component availability "
                    "ahead of the holiday season."
                ),
                url="https://example.com/apple-supply-disruption",
                published_at=now - timedelta(hours=3),
                content="Full article content about Apple supply chain disruption.",
                raw_payload={"mock": True, "source": "mock_news"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-news-005",
                title="SEC reportedly considering approval of spot Bitcoin ETF in Q1 2025",
                body=(
                    "Sources familiar with SEC deliberations indicate the regulator is close to "
                    "approving a spot Bitcoin ETF, with multiple asset managers submitting final "
                    "amended filings. Bitcoin surged 8% on the report."
                ),
                url="https://example.com/bitcoin-etf-rumour",
                published_at=now - timedelta(hours=4),
                content="Full article content about Bitcoin ETF rumour.",
                raw_payload={"mock": True, "source": "mock_news"},
            ),
        ]
