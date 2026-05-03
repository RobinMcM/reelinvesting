from dataclasses import dataclass, field

from app.models.article_asset_impact import ImpactDirection, TimeHorizon
from app.models.news_article import AssetType


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
    asset_type: AssetType
    tickers: list[str]
    sectors: list[str]
    newsworthiness: int
    market_relevance: int
    impact_rating: int
    confidence: int
    asset_impacts: list[AssetImpactResult] = field(default_factory=list)


_RULES: list[dict] = [
    {
        "keywords": ["nvidia", "nvda"],
        "tickers": ["NVDA"],
        "sectors": ["technology", "semiconductors"],
        "asset_type": AssetType.STOCK,
        "newsworthiness": 75,
        "market_relevance": 80,
        "impact_rating": 60,
        "confidence": 85,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.ONE_DAY,
    },
    {
        "keywords": ["apple", "aapl", "iphone", "supplier disruption", "supply chain"],
        "tickers": ["AAPL"],
        "sectors": ["technology", "consumer electronics"],
        "asset_type": AssetType.STOCK,
        "newsworthiness": 70,
        "market_relevance": 75,
        "impact_rating": -40,
        "confidence": 80,
        "direction": ImpactDirection.BEARISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": ["oil", "opec", "crude", "barrel", "energy supply"],
        "tickers": ["XOM", "CVX", "USO"],
        "sectors": ["energy", "commodities"],
        "asset_type": AssetType.COMMODITY,
        "newsworthiness": 80,
        "market_relevance": 85,
        "impact_rating": 55,
        "confidence": 78,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": ["interest rate", "federal reserve", "fed", "rate cut", "rate hike", "dot plot"],
        "tickers": ["SPY", "QQQ", "XLF", "TLT"],
        "sectors": ["macro", "financials"],
        "asset_type": AssetType.MACRO,
        "newsworthiness": 95,
        "market_relevance": 95,
        "impact_rating": 50,
        "confidence": 90,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.ONE_WEEK,
    },
    {
        "keywords": ["bitcoin", "btc", "crypto etf", "spot etf", "cryptocurrency"],
        "tickers": ["BTC", "COIN", "MSTR"],
        "sectors": ["crypto", "digital assets"],
        "asset_type": AssetType.CRYPTO,
        "newsworthiness": 70,
        "market_relevance": 72,
        "impact_rating": 65,
        "confidence": 70,
        "direction": ImpactDirection.BULLISH,
        "time_horizon": TimeHorizon.INTRADAY,
    },
]


class EventClassifier:
    def classify(self, headline: str, summary: str | None) -> ClassificationResult:
        text = f"{headline} {summary or ''}".lower()

        matched: dict | None = None
        for rule in _RULES:
            if any(kw in text for kw in rule["keywords"]):
                matched = rule
                break

        if matched is None:
            return ClassificationResult(
                asset_type=AssetType.UNKNOWN,
                tickers=[],
                sectors=[],
                newsworthiness=10,
                market_relevance=10,
                impact_rating=0,
                confidence=20,
            )

        asset_impacts = [
            AssetImpactResult(
                symbol=ticker,
                asset_type=matched["asset_type"],
                direction=matched["direction"],
                impact_score=matched["market_relevance"],
                confidence=matched["confidence"],
                time_horizon=matched["time_horizon"],
                reason=f"Matched keyword rule for {ticker}",
            )
            for ticker in matched["tickers"]
        ]

        return ClassificationResult(
            asset_type=matched["asset_type"],
            tickers=matched["tickers"],
            sectors=matched["sectors"],
            newsworthiness=matched["newsworthiness"],
            market_relevance=matched["market_relevance"],
            impact_rating=matched["impact_rating"],
            confidence=matched["confidence"],
            asset_impacts=asset_impacts,
        )
