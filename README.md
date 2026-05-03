# ReelInvesting Monorepo

Intelligence-driven film investment. This monorepo contains the public website and the market intelligence indexer service.

## Structure

```
reelinvesting/
├── apps/
│   └── web/                  # Next.js public website (reelinvesting.com)
├── services/
│   └── indexer/              # Python market intelligence indexer (FastAPI)
├── docker-compose.yml        # Runs postgres + indexer together
└── .gitignore
```

---

## Running Locally

### 1. Start the indexer + database

Copy the indexer env file and start Docker Compose:

```bash
cp services/indexer/.env.example services/indexer/.env
# Edit services/indexer/.env if needed

docker compose up -d --build
```

The indexer API will be available at `http://localhost:8000`.  
Swagger docs: `http://localhost:8000/docs`

### 2. Run the web app

```bash
cd apps/web
cp .env.local.example .env.local
# .env.local already points to http://localhost:8000
npm install
npm run dev
```

The website will be at `http://localhost:3000`.

---

## Environment Variables

### `apps/web/.env.local`

| Variable | Description | Default |
|---|---|---|
| `NEXT_PUBLIC_INDEXER_API_URL` | Base URL of the indexer API | `http://localhost:8000` |

### `services/indexer/.env`

See `services/indexer/.env.example` for the full list. Key variables:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `ENABLE_MOCK_NEWS` | Populate feed with mock news events |
| `ENABLE_MOCK_AGITATORS` | Populate feed with mock agitator events |
| `INGESTION_INTERVAL_SECONDS` | How often the indexer polls sources |

---

## Deploying `apps/web` to DigitalOcean App Platform

DigitalOcean App Platform has native Next.js support.

### Steps

1. Push the monorepo to a GitHub repository.

2. In the [DigitalOcean App Platform console](https://cloud.digitalocean.com/apps), click **Create App** and connect your GitHub repo.

3. App Platform will detect the repo root. You need to point it to the `apps/web` subdirectory:
   - **Source directory**: `apps/web`
   - App Platform will auto-detect Next.js.

4. Set the **environment variable** in the App Platform UI:
   ```
   NEXT_PUBLIC_INDEXER_API_URL=https://your-indexer-url.example.com
   ```
   Set this as a plain (non-secret) environment variable so it's baked into the client bundle.

5. Click **Deploy**. App Platform will run:
   ```bash
   npm install
   npm run build
   npm start
   ```

6. For the **indexer service**, deploy it separately as a Docker-based service pointing to `services/indexer/` with the `Dockerfile` in that directory. Connect it to a DigitalOcean Managed PostgreSQL database and set `DATABASE_URL` accordingly.

### CORS

If the Next.js app calls the indexer API directly from the browser (client components), ensure the indexer allows the App Platform domain in its CORS settings. For server-side fetching (Server Components), CORS is not an issue.

---

## Services

### `services/indexer` — Market Intelligence Indexer

FastAPI service that continuously ingests intelligence events from configured sources, classifies them, and stores them in PostgreSQL.

- **API**: `GET /events/recent`, `GET /events/high-impact`, `GET /admin/stats`
- **Docs**: `/docs` (Swagger UI)
- **Auth**: None yet (internal service)

### `apps/web` — Public Website

Next.js 15 App Router website.

| Route | Description |
|---|---|
| `/` | Homepage — brand hero, intelligence preview, film teaser |
| `/films` | Placeholder film projects page |
| `/newsroom` | High-impact events feed + rotating featured event |
| `/newsroom/events` | Full paginated event list with source-type filtering |
| `/admin` | Placeholder private admin (auth coming soon) |
| `/portal` | Placeholder research portal (auth coming soon) |
