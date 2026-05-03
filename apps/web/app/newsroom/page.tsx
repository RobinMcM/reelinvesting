import type { Metadata } from 'next';
import Link from 'next/link';
import { getHighImpactEvents, getRecentEvents } from '@/lib/indexer-api';
import EventCard from '@/components/EventCard';
import FeaturedEventRotator from '@/components/FeaturedEventRotator';
import StatCard from '@/components/StatCard';

export const metadata: Metadata = {
  title: 'Newsroom',
  description:
    'Market intelligence newsroom — high-impact events indexed from news, regulatory filings, and macro sources.',
};

export const revalidate = 60;

export default async function NewsroomPage() {
  const [highImpact, recent] = await Promise.all([
    getHighImpactEvents(60, 5),
    getRecentEvents(12),
  ]);

  const hasData = highImpact.length > 0 || recent.length > 0;

  return (
    <>
      {/* Hero */}
      <section className="border-b border-slate-800 bg-brand-navy py-16">
        <div className="mx-auto max-w-7xl px-6">
          <p className="text-xs font-semibold uppercase tracking-widest text-amber-500">
            Market Intelligence
          </p>
          <h1 className="mt-3 text-4xl font-bold text-white sm:text-5xl">Newsroom</h1>
          <p className="mt-4 max-w-2xl text-slate-400">
            Continuously indexed intelligence from news sources, regulatory filings,
            macro indicators, and influential voices. Scored for market relevance
            and potential impact — not buy/sell signals.
          </p>

          {/* Stats strip */}
          <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4 sm:gap-6 max-w-2xl">
            <StatCard label="High impact" value={highImpact.length} subtitle="last 24h" />
            <StatCard label="Recent events" value={recent.length} subtitle="indexed" />
            <StatCard label="Min. score" value="60" subtitle="impact threshold" />
            <StatCard label="Revalidates" value="60s" subtitle="auto-refresh" />
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-7xl px-6 py-12 space-y-16">
        {/* Featured rotating event */}
        {highImpact.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-semibold text-white">Featured — High Impact</h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Rotating through top-scored events. Potential impact only — not investment advice.
                </p>
              </div>
              <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-amber-700/40 bg-amber-900/20 px-3 py-1 text-xs font-semibold text-amber-400">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-400 animate-pulse" />
                Live
              </span>
            </div>
            <FeaturedEventRotator events={highImpact} />
          </section>
        )}

        {/* Recent events grid */}
        <section>
          <div className="flex items-end justify-between mb-6">
            <div>
              <h2 className="text-lg font-semibold text-white">Recent Intelligence</h2>
              <p className="text-xs text-slate-500 mt-0.5">Latest indexed events, all source types.</p>
            </div>
            <Link
              href="/newsroom/events"
              className="text-sm font-medium text-amber-400 hover:text-amber-300 transition-colors"
            >
              View all →
            </Link>
          </div>

          {recent.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {recent.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          ) : (
            <EmptyState />
          )}
        </section>

        {!hasData && (
          <section className="py-8">
            <EmptyState />
          </section>
        )}

        {/* Disclaimer */}
        <section className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
          <p className="text-xs text-slate-500 leading-relaxed">
            <span className="font-semibold text-slate-400">Disclaimer:</span>{' '}
            Intelligence events on this page are sourced from third-party news providers,
            regulatory bodies, and public data feeds. ReelInvesting does not provide
            financial advice, trading signals, or investment recommendations.
            Affected assets and potential impact assessments are informational only.
            Always conduct your own research before making investment decisions.
          </p>
        </section>
      </div>
    </>
  );
}

function EmptyState() {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-12 text-center">
      <p className="text-slate-500">No intelligence events available yet.</p>
      <p className="mt-1 text-xs text-slate-600">
        Start the indexer service to populate the feed.
      </p>
      <p className="mt-4 text-xs font-mono text-slate-700">
        docker compose up -d
      </p>
    </div>
  );
}
