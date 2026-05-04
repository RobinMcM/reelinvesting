# ReelInvesting Market Intelligence Indexer

A pure intelligence indexing service. Gathers, normalises, classifies, and stores market-relevant information from multiple source types.

**This service does NOT:**
- Execute trades
- Generate buy/sell signals
- Connect to brokers or portfolio managers
- Make trading decisions of any kind

**This service ONLY:**
- Gathers market-relevant intelligence from configurable sources
- Stores full raw payloads in DigitalOcean Spaces
- Stores lean searchable metadata in PostgreSQL
- Classifies events descriptively (not prescriptively)
- Exposes read/admin REST APIs for dashboards and downstream services

---

## Source Types

| Type | Description |
|------|-------------|
| `NEWS` | News articles from feeds, APIs, scrapers |
| `AGITATOR` | Statements from influential people/entities |
| `SOCIAL` | Social media posts |
| `MACRO` | Macroeconomic events and data releases |
| `FILING` | Corporate or regulatory filings |
| `EARNINGS` | Earnings reports and guidance |
| `REGULATORY` | Regulatory announcements and actions |
| `UNKNOWN` | Unclassified sources |

---

## Architecture

```
Listeners → Normalizer → Spaces Store → Postgres Index → Classifier → Asset Impact Rows
                              ↑
                    (deduplicated by stable_id)
```

| Component | Responsibility |
|-----------|---------------|
| `listeners/` | Fetch raw intelligence items from external sources |
| `normalizers/` | Clean, validate, deduplicate, generate stable IDs |
| `spaces/` | Store full raw JSON payloads to DO Spaces |
| `repositories/` | Read/write Postgres via SQLAlchemy 2.x |
| `classifiers/` | Descriptive rule-based classification |
| `workers/` | Orchestrate the full pipeline per ingestion cycle |
| `api/` | FastAPI read/admin endpoints |
| `main.py` | FastAPI + APScheduler combined entry point |

---

## Listener System

Each `IntelligenceListener` polls a source and returns `RawIntelligenceItem` objects.

Currently available:
- **MockNewsListener** — sample market news (Nvidia, Fed, OPEC, Apple, crypto ETF)
- **MockAgitatorListener** — sample influence events (Trump tariffs, Musk/Tesla, BoE, SEC)
- **AlpacaNewsListener** — real news articles from the Alpaca market data API

Real listeners (RSS, X API, SEC EDGAR, economic calendar) can be added by implementing `IntelligenceListener`.

---

## Normalizer

`IntelligenceNormalizer` processes each raw item:
- Cleans whitespace from titles
- Generates `body_preview` (≤ 500 chars)
- Ensures UTC timezone on `published_at`
- Generates a deterministic `stable_id` for deduplication:
  - `source_type:source_name:external_id` if available
  - otherwise `sha256(source_type:source_name:url_or_title)`

---

## Classifier

`RuleBasedClassifier` maps keyword patterns to descriptive metadata:
- `event_type`, `asset_type`, `tickers`, `sectors`, `entities`
- Scores: `newsworthiness`, `attention_score`, `virality_score`, `market_relevance`, `impact_rating`, `confidence`

**All output is descriptive only. No trading signals are generated.**

`AIClassifierPlaceholder` provides a clean interface for a future LLM-based classifier — it raises `NotImplementedError` until implemented.

---

## Storage

**DigitalOcean Spaces** — full raw payloads at deterministic keys:
```
intelligence/YYYY/MM/DD/{source_type}/{source_name}/{stable_id}.json
```

**PostgreSQL** — lean index metadata:
- `intelligence_source` — configurable source registry
- `agitator_profile` — influential people/entities registry
- `intelligence_event` — one row per unique intelligence event
- `intelligence_asset_impact` — per-asset descriptive impact rows

Postgres stores only lean metadata. The full payload is always in Spaces.

---

## Running with Docker

```bash
cp .env.example .env
# edit .env — DATABASE_URL required; Spaces credentials optional

docker compose up --build
```

This will:
1. Start PostgreSQL
2. Run `alembic upgrade head` to create all tables
3. Start FastAPI on port **8000**
4. Run the APScheduler ingestion worker in the background

### Stop

```bash
docker compose down
```

---

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env

docker compose up postgres -d   # or use any local Postgres
alembic upgrade head
python -m app.main
```

---

## Running Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Check current revision
alembic current

# Generate a new migration after model changes
alembic revision --autogenerate -m "describe change"

# Roll back one step
alembic downgrade -1
```

---

## API Endpoints

Interactive docs: `http://localhost:8000/docs`

### Health

```
GET  /health          # Service liveness check
GET  /health/db       # Database connectivity check
```

### Events (read)

```
GET  /events/recent                          # Most recent events (default 50)
GET  /events/high-impact?min_score=60        # High market_relevance events
GET  /events/{event_id}                      # Single event + asset impacts
GET  /events/source-type/{source_type}       # Filter by source type
GET  /events/asset/{symbol}                  # Events affecting a ticker symbol
```

### Sources (admin)

```
GET   /sources                    # List all configured intelligence sources
POST  /sources                    # Register a new source
PATCH /sources/{source_id}        # Update a source (e.g. enable/disable)
```

### Admin

```
GET   /admin/agitators                        # List agitator profiles
POST  /admin/agitators                        # Create agitator profile
PATCH /admin/agitators/{agitator_id}          # Update agitator profile
GET   /admin/events                           # All events, paginated
GET   /admin/events/{event_id}                # Full event detail + impacts
PATCH /admin/events/{event_id}/status         # Override event status
GET   /admin/stats                            # Ingestion statistics
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | required | PostgreSQL connection string |
| `DO_SPACES_ENDPOINT` | `""` | DigitalOcean Spaces endpoint URL |
| `DO_SPACES_REGION` | `""` | Spaces region |
| `DO_SPACES_BUCKET` | `""` | Spaces bucket name |
| `DO_SPACES_ACCESS_KEY_ID` | `""` | Spaces access key |
| `DO_SPACES_SECRET_ACCESS_KEY` | `""` | Spaces secret key |
| `INGESTION_INTERVAL_SECONDS` | `300` | Seconds between ingestion cycles |
| `RUN_ON_STARTUP` | `true` | Run ingestion immediately on launch |
| `API_HOST` | `0.0.0.0` | Uvicorn bind host |
| `API_PORT` | `8000` | Uvicorn bind port |
| `ENABLE_MOCK_NEWS` | `true` | Enable the mock news listener |
| `ENABLE_MOCK_AGITATORS` | `true` | Enable the mock agitator listener |
| `ALPACA_API_KEY` | `""` | Alpaca API key (news data only) |
| `ALPACA_SECRET_KEY` | `""` | Alpaca secret key |
| `ALPACA_PAPER` | `true` | Use paper environment (no effect on news) |
| `ENABLE_ALPACA_NEWS` | `false` | Enable the Alpaca news listener |
| `ALPACA_NEWS_SYMBOLS` | `AAPL,MSFT,...` | Comma-separated list of symbols to fetch news for |
| `ALPACA_NEWS_LIMIT` | `20` | Max articles per ingestion cycle |

If Spaces credentials are absent, uploads are silently skipped — events are still indexed in Postgres with an empty `spaces_key`.

---

## Alpaca News Integration

The `AlpacaNewsListener` uses the [alpaca-py](https://github.com/alpacahq/alpaca-py) SDK to fetch real market news articles.

**This integration is for news intelligence only.** It does not initialise a trading client, submit orders, access portfolio data, or generate buy/sell signals.

### Getting Alpaca API Keys

1. Sign up for a free account at [https://alpaca.markets](https://alpaca.markets)
2. Go to **Paper Trading** → **API Keys** (the free data tier works without a funded account)
3. Generate a key pair — copy the API Key ID and Secret Key
4. Add them to your `.env`:

```env
ALPACA_API_KEY=PKXXXXXXXXXXXXXXXXXXXXXXXX
ALPACA_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ENABLE_ALPACA_NEWS=true
```

### Enabling the Alpaca Listener

Set the following in your `.env` (or `services/indexer/.env`):

```env
# Enable real Alpaca news (disable mocks in production if preferred)
ENABLE_ALPACA_NEWS=true
ALPACA_API_KEY=PKXXXXXXXXXXXXXXXXXXXXXXXX
ALPACA_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Symbols to watch — stocks, ETFs, and crypto pairs
ALPACA_NEWS_SYMBOLS=AAPL,MSFT,NVDA,TSLA,SPY,QQQ,BTCUSD,ETHUSD

# Articles fetched per ingestion cycle
ALPACA_NEWS_LIMIT=20

# Keep mocks on for testing alongside real data, or turn them off in production
ENABLE_MOCK_NEWS=false
ENABLE_MOCK_AGITATORS=false
```

### Manual Smoke Test

```bash
# Rebuild and restart with Alpaca enabled
docker compose down
docker compose up -d --build
docker compose logs -f indexer
```

Expected log output (on first ingestion cycle):
```
listener_enabled  listener=AlpacaNewsListener
alpaca_news_fetched  count=20  symbols=[...]
event_indexed  source_name=alpaca_news  ...
ingestion_cycle_complete  processed=N  skipped=0  errors=0
```

Verify via API:
```bash
# Events should include alpaca_news source
curl http://localhost:8000/events/recent

# Stats should show NEWS records
curl http://localhost:8000/admin/stats
```

### Deduplication

Alpaca articles deduplicate using the Alpaca article ID as `external_id`. The stable ID is:

```
sha256("NEWS:alpaca_news:<article_id>")
```

Re-running the ingestion cycle fetches the same articles but skips any already in Postgres — no duplicates are inserted.

### Error Handling

If the Alpaca API is unreachable or returns an error, `AlpacaNewsListener.fetch_latest()` logs the exception and returns an empty list. The scheduler continues running and retries on the next cycle.

---

## Database Schema

### `intelligence_source`

Configurable registry of intelligence sources (feeds, APIs, scrapers).

### `agitator_profile`

Registry of influential people/entities (politicians, central banks, regulators, CEOs, influencers) whose statements can move market attention.

### `intelligence_event`

Primary event index. One row per unique intelligence event.

- `stable_id` — deterministic deduplication hash
- `source_type` — `NEWS | AGITATOR | SOCIAL | MACRO | FILING | EARNINGS | REGULATORY | UNKNOWN`
- `asset_type` — `STOCK | CRYPTO | FOREX | COMMODITY | INDEX | MACRO | UNKNOWN`
- `status` — `RAW → STORED → CLASSIFIED` (or `IGNORED | ERROR`)
- `impact_rating` — -100 to 100, descriptive directional estimate **not a trading signal**
- `spaces_key` — pointer to full payload in DO Spaces

### `intelligence_asset_impact`

Per-symbol descriptive impact rows linked to each event.

- `direction` — `BULLISH | BEARISH | NEUTRAL | UNCERTAIN` — **not a buy/sell recommendation**
- `time_horizon` — `INTRADAY | ONE_DAY | ONE_WEEK | LONG_TERM | UNKNOWN`

---

## Future Newsroom UI

This service backs a Next.js admin dashboard (separate repo). The API provides:
- Source management (enable/disable feeds)
- Agitator profile management
- Real-time event browsing by source type, ticker, or recency
- Asset impact inspection
- Ingestion health statistics

---

## Future Trader Entity

A separate trader service may consume intelligence from this indexer via the read API. That service is responsible for all trading decisions. This indexer will never contain broker connections, order management, or signal generation.

The clean separation ensures:
- Intelligence quality improves independently of trading logic
- The indexer can serve multiple downstream consumers simultaneously
- Regulatory and compliance boundaries remain clear
