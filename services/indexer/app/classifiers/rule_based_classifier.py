from __future__ import annotations

from dataclasses import dataclass, field

from app.models.enums import AssetType, ImpactDirection, TimeHorizon
from app.normalizers.intelligence_normalizer import NormalizedIntelligenceItem

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class AssetImpactResult:
    symbol: str
    asset_type: AssetType
    direction: ImpactDirection
    impact_score: int
    confidence: int
    time_horizon: TimeHorizon
    reason: str | None = None


@dataclass
class ClassificationResult:
    event_type: str
    asset_type: AssetType
    tickers: list[str]
    sectors: list[str]
    entities: list[str]
    newsworthiness: int
    attention_score: int
    virality_score: int
    market_relevance: int
    # impact_rating: directional magnitude estimate only, NOT a trading signal
    impact_rating: int
    confidence: int
    asset_impacts: list[AssetImpactResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Rule table
# Each rule maps keyword triggers to descriptive classification metadata.
# None of these constitute buy/sell signals or trading recommendations.
# ---------------------------------------------------------------------------

_RULES: list[dict] = [
    {
        "keywords": ["nvidia", "nvda", "jensen huang", "h100", "h200"],
        "event_type": "earnings_guidance",
        "tickers": ["NVDA"],
        "sectors": ["technology", "semiconductors"],
        "entities": ["Nvidia"],
        "asset_type": AssetType.STOCK,
        "newsworthiness": 80,
        "attention_score": 85,
        "virality_score": 75,
        "market_relevance": 85,
        "impact_rating": 60,
        "confidence": 85,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.ONE_DAY,
    },
    {
        "keywords": ["apple", "aapl", "iphone", "supplier disruption", "supply chain", "foxconn", "tsmc"],
        "event_type": "supply_disruption",
        "tickers": ["AAPL"],
        "sectors": ["technology", "consumer electronics"],
        "entities": ["Apple"],
        "asset_type": AssetType.STOCK,
        "newsworthiness": 72,
        "attention_score": 75,
        "virality_score": 68,
        "market_relevance": 78,
        "impact_rating": -40,
        "confidence": 80,
        "direction": ImpactDirection.BEARISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": ["oil", "opec", "crude", "barrel", "energy supply", "wti", "brent"],
        "event_type": "commodity_supply_event",
        "tickers": ["XOM", "CVX", "USO"],
        "sectors": ["energy", "commodities"],
        "entities": ["OPEC+"],
        "asset_type": AssetType.COMMODITY,
        "newsworthiness": 80,
        "attention_score": 82,
        "virality_score": 70,
        "market_relevance": 85,
        "impact_rating": 55,
        "confidence": 78,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": [
            "interest rate", "federal reserve", "fed", "rate cut", "rate hike", "dot plot",
            "fomc", "powell", "basis point",
        ],
        "event_type": "central_bank_policy",
        "tickers": ["SPY", "QQQ", "XLF", "TLT"],
        "sectors": ["macro", "financials"],
        "entities": ["Federal Reserve"],
        "asset_type": AssetType.MACRO,
        "newsworthiness": 95,
        "attention_score": 95,
        "virality_score": 88,
        "market_relevance": 95,
        "impact_rating": 50,
        "confidence": 90,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": ["bank of england", "boe", "bailey", "sterling", "gbp"],
        "event_type": "central_bank_policy",
        "tickers": ["GBP", "EWU"],
        "sectors": ["macro", "financials"],
        "entities": ["Bank of England"],
        "asset_type": AssetType.MACRO,
        "newsworthiness": 88,
        "attention_score": 85,
        "virality_score": 70,
        "market_relevance": 88,
        "impact_rating": -20,
        "confidence": 82,
        "direction": ImpactDirection.BEARISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": ["bitcoin", "btc", "crypto etf", "spot etf", "ethereum", "eth", "cryptocurrency"],
        "event_type": "crypto_market_event",
        "tickers": ["BTC", "ETH", "COIN", "MSTR"],
        "sectors": ["crypto", "digital assets"],
        "entities": [],
        "asset_type": AssetType.CRYPTO,
        "newsworthiness": 72,
        "attention_score": 78,
        "virality_score": 85,
        "market_relevance": 74,
        "impact_rating": 65,
        "confidence": 70,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.INTRADAY,
    },
    {
        "keywords": ["tariff", "trade war", "import duties", "trade deal", "eu goods"],
        "event_type": "trade_policy",
        "tickers": ["SPY", "QQQ", "DXY"],
        "sectors": ["industrials", "macro"],
        "entities": [],
        "asset_type": AssetType.MACRO,
        "newsworthiness": 85,
        "attention_score": 88,
        "virality_score": 82,
        "market_relevance": 88,
        "impact_rating": -35,
        "confidence": 75,
        "direction": ImpactDirection.BEARISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": ["tesla", "tsla", "elon", "musk", "fsd", "full self-driving", "electric vehicle", "ev"],
        "event_type": "company_announcement",
        "tickers": ["TSLA"],
        "sectors": ["automotive", "technology"],
        "entities": ["Tesla", "Elon Musk"],
        "asset_type": AssetType.STOCK,
        "newsworthiness": 78,
        "attention_score": 90,
        "virality_score": 92,
        "market_relevance": 80,
        "impact_rating": 55,
        "confidence": 75,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.INTRADAY,
    },
    {
        "keywords": ["ai", "artificial intelligence", "xai", "grok", "openai", "chatgpt", "chips", "semiconductor"],
        "event_type": "ai_technology_event",
        "tickers": ["NVDA", "AMD", "MSFT", "GOOGL"],
        "sectors": ["technology", "semiconductors"],
        "entities": [],
        "asset_type": AssetType.STOCK,
        "newsworthiness": 75,
        "attention_score": 82,
        "virality_score": 80,
        "market_relevance": 78,
        "impact_rating": 50,
        "confidence": 72,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.ONE_DAY,
    },
    {
        "keywords": ["sec", "regulator", "oversight", "enforcement", "investigation", "compliance"],
        "event_type": "regulatory_action",
        "tickers": ["SPY"],
        "sectors": ["regulatory", "macro"],
        "entities": ["SEC"],
        "asset_type": AssetType.MACRO,
        "newsworthiness": 70,
        "attention_score": 72,
        "virality_score": 60,
        "market_relevance": 70,
        "impact_rating": -25,
        "confidence": 65,
        "direction": ImpactDirection.BEARISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
]

_DEFAULT_RESULT = ClassificationResult(
    event_type="unknown",
    asset_type=AssetType.UNKNOWN,
    tickers=[],
    sectors=[],
    entities=[],
    newsworthiness=10,
    attention_score=10,
    virality_score=10,
    market_relevance=10,
    impact_rating=0,
    confidence=20,
)


class RuleBasedClassifier:
    """
    Descriptive rule-based classifier.

    Produces classification metadata for intelligence events.
    Output is informational only — no trading signals, no buy/sell recommendations.
    """

    def classify(self, item: NormalizedIntelligenceItem) -> ClassificationResult:
        text = f"{item.title} {item.body_preview or ''}".lower()

        matched: dict | None = None
        for rule in _RULES:
            if any(kw in text for kw in rule["keywords"]):
                matched = rule
                break

        if matched is None:
            return _DEFAULT_RESULT

        asset_impacts = [
            AssetImpactResult(
                symbol=ticker,
                asset_type=matched["asset_type"],
                direction=matched["direction"],
                impact_score=matched["market_relevance"],
                confidence=matched["confidence"],
                time_horizon=matched["time_horizon"],
                reason=f"Descriptive rule match for {ticker} — not a trading signal",
            )
            for ticker in matched["tickers"]
        ]

        return ClassificationResult(
            event_type=matched["event_type"],
            asset_type=matched["asset_type"],
            tickers=matched["tickers"],
            sectors=matched["sectors"],
            entities=matched["entities"],
            newsworthiness=matched["newsworthiness"],
            attention_score=matched["attention_score"],
            virality_score=matched["virality_score"],
            market_relevance=matched["market_relevance"],
            impact_rating=matched["impact_rating"],
            confidence=matched["confidence"],
            asset_impacts=asset_impacts,
        )
