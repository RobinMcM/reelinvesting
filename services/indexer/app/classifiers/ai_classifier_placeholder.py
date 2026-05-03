from app.classifiers.rule_based_classifier import ClassificationResult
from app.logging_config import get_logger
from app.normalizers.intelligence_normalizer import NormalizedIntelligenceItem

logger = get_logger(__name__)


class AIClassifierPlaceholder:
    """
    Placeholder for a future AI-powered intelligence classifier.

    When implemented, this will call an external AI model to produce richer
    descriptive classifications. It will NOT generate trading signals or
    buy/sell recommendations — classification remains purely informational.

    Usage:
        classifier = AIClassifierPlaceholder()
        result = classifier.classify(item)  # currently raises NotImplementedError

    Future implementation notes:
        - Call an LLM (e.g. Claude) with structured output
        - Extract entities, tickers, sectors, event_type from free text
        - Score newsworthiness, attention, virality, market_relevance descriptively
        - Prompt must explicitly state: output is informational, not financial advice
        - Cache results to avoid redundant API calls
        - Respect rate limits and cost budgets
    """

    def classify(self, item: NormalizedIntelligenceItem) -> ClassificationResult:
        raise NotImplementedError(
            "AIClassifierPlaceholder is not yet implemented. "
            "Use RuleBasedClassifier for production classification."
        )

    def is_available(self) -> bool:
        return False
