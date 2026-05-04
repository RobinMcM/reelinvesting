from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str

    DO_SPACES_ENDPOINT: str = ""
    DO_SPACES_REGION: str = ""
    DO_SPACES_BUCKET: str = ""
    DO_SPACES_ACCESS_KEY_ID: str = ""
    DO_SPACES_SECRET_ACCESS_KEY: str = ""

    NEWS_INGESTION_MODE: str = "mock"
    INGESTION_INTERVAL_SECONDS: int = 300
    RUN_ON_STARTUP: bool = True

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    ENABLE_MOCK_NEWS: bool = True
    ENABLE_MOCK_AGITATORS: bool = True

    # Alpaca — news/intelligence data only, no trading
    ALPACA_API_KEY: str = ""
    ALPACA_SECRET_KEY: str = ""
    ALPACA_PAPER: bool = True
    ENABLE_ALPACA_NEWS: bool = False
    ALPACA_NEWS_SYMBOLS: str = "AAPL,MSFT,NVDA,TSLA,SPY,QQQ,BTCUSD,ETHUSD"
    ALPACA_NEWS_LIMIT: int = 20


settings = Settings()
