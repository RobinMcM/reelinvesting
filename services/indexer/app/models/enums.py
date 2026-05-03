import enum


class SourceType(str, enum.Enum):
    NEWS = "NEWS"
    AGITATOR = "AGITATOR"
    SOCIAL = "SOCIAL"
    MACRO = "MACRO"
    FILING = "FILING"
    EARNINGS = "EARNINGS"
    REGULATORY = "REGULATORY"
    UNKNOWN = "UNKNOWN"


class AssetType(str, enum.Enum):
    STOCK = "STOCK"
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    COMMODITY = "COMMODITY"
    INDEX = "INDEX"
    MACRO = "MACRO"
    UNKNOWN = "UNKNOWN"


class EventStatus(str, enum.Enum):
    RAW = "RAW"
    STORED = "STORED"
    CLASSIFIED = "CLASSIFIED"
    IGNORED = "IGNORED"
    ERROR = "ERROR"


class ImpactDirection(str, enum.Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    UNCERTAIN = "UNCERTAIN"


class TimeHorizon(str, enum.Enum):
    INTRADAY = "INTRADAY"
    ONE_DAY = "ONE_DAY"
    ONE_WEEK = "ONE_WEEK"
    LONG_TERM = "LONG_TERM"
    UNKNOWN = "UNKNOWN"


class InfluenceCategory(str, enum.Enum):
    POLITICAL = "POLITICAL"
    CENTRAL_BANK = "CENTRAL_BANK"
    REGULATOR = "REGULATOR"
    CEO = "CEO"
    COMPANY = "COMPANY"
    AI = "AI"
    CRYPTO = "CRYPTO"
    GEOPOLITICAL = "GEOPOLITICAL"
    MEDIA = "MEDIA"
    OTHER = "OTHER"
