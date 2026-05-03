import type { Metadata } from 'next';
import Link from 'next/link';
import { getRecentEvents } from '@/lib/indexer-api';
import EventCard from '@/components/EventCard';
import type { SourceType } from '@/lib/types';

export const metadata: Metadata = {
  title: 'All Intelligence Events',
  description: 'Full list of indexed market intelligence events.',
};

export const revalidate = 60;

const SOURCE_TYPES: SourceType[] = [
  'NEWS', 'AGITATOR', 'SOCIAL', 'MACRO', 'FILING', 'EARNINGS', 'REGULATORY',
];

export default async function EventsListPage({
  searchParams,
}: {
  searchParams: Promise<{ source?: string; limit?: string }>;
}) {
  const params = await searchParams;
  const limit = Math.min(Number(params.limit) || 50, 200);
  const events = await getRecentEvents(limit);

  const sourceFilter = params.source?.toUpperCase() as SourceType | undefined;
  const filtered = sourceFilter
    ? events.filter((e) => e.source_type === sourceFilter)
    : events;

  return (
    <>
      {/* Header */}
      <section className="border-b border-slate-800 bg-brand-navy py-12">
        <div className="mx-auto max-w-7xl px-6">
          <nav className="text-xs text-slate-500 mb-3">
            <Link href="/newsroom" className="hover:text-slate-300 transition-colors">
              Newsroom
            </Link>{' '}
            <span className="mx-1">/</span> All Events
          </nav>
          <h1 className="text-3xl font-bold text-white">Intelligence Events</h1>
          <p className="mt-2 text-slate-400 text-sm">
            {filtered.length} event{filtered.length !== 1 ? 's' : ''} indexed
            {sourceFilter ? ` · filtered by ${sourceFilter}` : ''}
          </p>
        </div>
      </section>

      {/* Filter bar */}
      <section className="border-b border-slate-800 bg-slate-900 sticky top-[65px] z-40">
        <div className="mx-auto max-w-7xl px-6 py-3">
          <div className="flex items-center gap-2 overflow-x-auto pb-1">
            <span className="shrink-0 text-xs text-slate-500">Source:</span>
            <Link
              href="/newsroom/events"
              className={`shrink-0 rounded px-2.5 py-1 text-xs font-medium transition-colors ${
                !sourceFilter
                  ? 'bg-amber-500 text-slate-900'
                  : 'border border-slate-700 text-slate-400 hover:border-amber-700/60 hover:text-amber-400'
              }`}
            >
              All
            </Link>
            {SOURCE_TYPES.map((type) => (
              <Link
                key={type}
                href={`/newsroom/events?source=${type.toLowerCase()}`}
                className={`shrink-0 rounded px-2.5 py-1 text-xs font-medium transition-colors ${
                  sourceFilter === type
                    ? 'bg-amber-500 text-slate-900'
                    : 'border border-slate-700 text-slate-400 hover:border-amber-700/60 hover:text-amber-400'
                }`}
              >
                {type.charAt(0) + type.slice(1).toLowerCase()}
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Events */}
      <section className="bg-slate-950 py-10">
        <div className="mx-auto max-w-7xl px-6">
          {filtered.length > 0 ? (
            <>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {filtered.map((event) => (
                  <EventCard key={event.id} event={event} />
                ))}
              </div>

              {/* Load more hint */}
              {events.length >= limit && (
                <div className="mt-10 text-center">
                  <Link
                    href={`/newsroom/events?limit=${limit + 50}${sourceFilter ? `&source=${sourceFilter}` : ''}`}
                    className="inline-flex rounded-lg border border-slate-700 px-5 py-2.5 text-sm font-medium text-slate-300 transition-colors hover:border-amber-600 hover:text-amber-400"
                  >
                    Load more events
                  </Link>
                </div>
              )}
            </>
          ) : (
            <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-12 text-center">
              <p className="text-slate-500">
                {sourceFilter
                  ? `No ${sourceFilter} events indexed yet.`
                  : 'No events indexed yet.'}
              </p>
              <Link
                href="/newsroom/events"
                className="mt-4 inline-flex text-sm text-amber-400 hover:text-amber-300"
              >
                Clear filters
              </Link>
            </div>
          )}
        </div>
      </section>
    </>
  );
}
