from datetime import datetime, timedelta, timezone

from app.listeners.base import IntelligenceListener, RawIntelligenceItem
from app.models.enums import SourceType


class MockAgitatorListener(IntelligenceListener):
    @property
    def source_name(self) -> str:
        return "mock_agitator"

    @property
    def source_type(self) -> SourceType:
        return SourceType.AGITATOR

    def fetch_latest(self) -> list[RawIntelligenceItem]:
        now = datetime.now(timezone.utc)

        return [
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-agit-001",
                title="Trump threatens 25% tariffs on all EU goods unless trade deal reached by June",
                body=(
                    "President Trump posted on Truth Social threatening sweeping 25% tariffs on all "
                    "European Union goods if a comprehensive trade agreement is not reached by June 1st. "
                    "The statement sent US futures lower and strengthened the dollar."
                ),
                url="https://example.com/trump-eu-tariffs",
                published_at=now - timedelta(minutes=20),
                content="Full post content about Trump EU tariff threat.",
                agitator_name="Donald Trump",
                platform="Truth Social",
                handle="@realDonaldTrump",
                raw_payload={"mock": True, "source": "mock_agitator", "platform": "truth_social"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-agit-002",
                title="Elon Musk: xAI's Grok 3 outperforms GPT-4o on all benchmarks — Tesla FSD next",
                body=(
                    "Elon Musk posted on X that Grok 3 has surpassed GPT-4o across all major benchmarks "
                    "and will be integrated into Tesla vehicles for Full Self-Driving within 6 months. "
                    "TSLA jumped 5% in after-hours trading."
                ),
                url="https://example.com/musk-grok3-tesla",
                published_at=now - timedelta(minutes=40),
                content="Full post content about Elon Musk xAI and Tesla announcement.",
                agitator_name="Elon Musk",
                platform="X",
                handle="@elonmusk",
                raw_payload={"mock": True, "source": "mock_agitator", "platform": "x"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-agit-003",
                title="Bank of England: rate cut path depends on services inflation trajectory",
                body=(
                    "Bank of England Governor Andrew Bailey stated in a speech that the pace of future "
                    "rate cuts will be determined by the trajectory of services inflation, which remains "
                    "elevated. Sterling fell 0.4% against the dollar on the cautious tone."
                ),
                url="https://example.com/boe-bailey-rates",
                published_at=now - timedelta(hours=1),
                content="Full speech content about Bank of England rate path.",
                agitator_name="Bank of England",
                platform="Official Statement",
                handle=None,
                raw_payload={"mock": True, "source": "mock_agitator", "platform": "official"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-agit-004",
                title="Crypto influencer: BlackRock spot Ethereum ETF approval imminent, sources say",
                body=(
                    "Prominent crypto influencer @WhalePump posted that multiple institutional sources "
                    "indicate BlackRock's spot Ethereum ETF approval is imminent, potentially within "
                    "days. ETH rallied 6% and COIN gained 4% on the rumour."
                ),
                url="https://example.com/eth-etf-rumour",
                published_at=now - timedelta(hours=2),
                content="Full post content about Ethereum ETF rumour.",
                agitator_name="WhalePump",
                platform="X",
                handle="@WhalePump",
                raw_payload={"mock": True, "source": "mock_agitator", "platform": "x"},
            ),
            RawIntelligenceItem(
                source_type=self.source_type,
                source_name=self.source_name,
                external_id="mock-agit-005",
                title="SEC Chair signals stricter oversight of AI-driven trading platforms",
                body=(
                    "SEC Chair Gary Gensler warned in congressional testimony that AI-driven trading "
                    "platforms could pose systemic risks and that the Commission is preparing new "
                    "disclosure requirements for algorithmic trading systems."
                ),
                url="https://example.com/sec-ai-trading-oversight",
                published_at=now - timedelta(hours=3),
                content="Full testimony content about SEC AI trading oversight.",
                agitator_name="SEC",
                platform="Congressional Testimony",
                handle=None,
                raw_payload={"mock": True, "source": "mock_agitator", "platform": "official"},
            ),
        ]
