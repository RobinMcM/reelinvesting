import Link from 'next/link';
import { getHighImpactEvents } from '@/lib/indexer-api';
import EventCard from '@/components/EventCard';

export default async function HomePage() {
  const featuredEvents = await getHighImpactEvents(60, 3);

  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden bg-brand-navy">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-brand-navy to-slate-950" />
        <div className="absolute inset-0 opacity-5"
          style={{ backgroundImage: 'radial-gradient(circle at 25% 60%, #F59E0B 0%, transparent 50%)' }}
        />
        <div className="relative mx-auto max-w-7xl px-6 py-28 sm:py-40">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-500">
              Film Investment Intelligence
            </p>
            <h1 className="mt-4 text-5xl font-bold leading-tight tracking-tight text-white sm:text-6xl lg:text-7xl">
              Where Film{' '}
              <span className="text-amber-400">Meets</span>{' '}
              Finance
            </h1>
            <p className="mt-6 text-lg text-slate-300 leading-relaxed max-w-2xl">
              ReelInvesting is the intelligence platform for independent film finance.
              We surface macro signals, regulatory shifts, and market-moving events so
              you never miss what matters.
            </p>
            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                href="/films"
                className="rounded-lg bg-amber-500 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg transition-colors hover:bg-amber-400"
              >
                View Films
              </Link>
              <Link
                href="/newsroom"
                className="rounded-lg border border-slate-600 px-6 py-3 text-sm font-semibold text-slate-200 transition-colors hover:border-amber-600 hover:text-amber-400"
              >
                Open Newsroom
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Value props */}
      <section className="border-y border-slate-800 bg-slate-950">
        <div className="mx-auto max-w-7xl px-6 py-20">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
            <ValueProp
              icon="🎬"
              title="Curated Film Projects"
              body="Access vetted independent film investment opportunities sourced from established producers and emerging directors."
            />
            <ValueProp
              icon="📡"
              title="Market Intelligence"
              body="Real-time signals from news, regulatory filings, macro events, and influential voices — indexed and scored for relevance."
            />
            <ValueProp
              icon="🔒"
              title="Private Research Portal"
              body="Deep-dive analytics and curated intelligence for accredited investors. Private access with enhanced data layers."
              comingSoon
            />
          </div>
        </div>
      </section>

      {/* Live intelligence preview */}
      <section className="bg-slate-900">
        <div className="mx-auto max-w-7xl px-6 py-20">
          <div className="flex items-end justify-between mb-10">
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-amber-500">
                Live Intelligence Feed
              </p>
              <h2 className="mt-2 text-3xl font-bold text-white">
                Market signals, right now
              </h2>
              <p className="mt-2 text-slate-400 max-w-xl">
                Our indexer continuously monitors news sources, regulatory filings,
                and macro indicators. Here's a snapshot of recent high-impact events.
              </p>
            </div>
            <Link
              href="/newsroom"
              className="hidden sm:inline-flex items-center gap-1 text-sm font-medium text-amber-400 hover:text-amber-300 transition-colors"
            >
              Full newsroom →
            </Link>
          </div>

          {featuredEvents.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {featuredEvents.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          ) : (
            <div className="rounded-xl border border-slate-700/50 bg-slate-800/30 p-12 text-center">
              <p className="text-slate-500">Intelligence feed warming up…</p>
              <p className="mt-1 text-xs text-slate-600">
                Start the indexer to populate live events.
              </p>
            </div>
          )}

          <div className="mt-8 sm:hidden text-center">
            <Link href="/newsroom" className="text-sm font-medium text-amber-400 hover:text-amber-300">
              View full newsroom →
            </Link>
          </div>
        </div>
      </section>

      {/* Film projects teaser */}
      <section className="border-t border-slate-800 bg-slate-950">
        <div className="mx-auto max-w-7xl px-6 py-20">
          <div className="text-center max-w-2xl mx-auto">
            <p className="text-xs font-semibold uppercase tracking-widest text-amber-500">
              Coming Soon
            </p>
            <h2 className="mt-2 text-3xl font-bold text-white">
              Featured Film Projects
            </h2>
            <p className="mt-4 text-slate-400">
              We're curating our first slate of independent film investment
              opportunities. Register your interest to be notified when projects go live.
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-center"
              >
                <div className="mx-auto h-24 w-24 rounded-full bg-slate-800 flex items-center justify-center text-3xl">
                  🎬
                </div>
                <p className="mt-4 text-sm font-semibold text-slate-300">
                  Project {String.fromCharCode(64 + i)}
                </p>
                <p className="mt-1 text-xs text-slate-600">Details coming soon</p>
              </div>
            ))}
          </div>

          <div className="mt-10 text-center">
            <Link
              href="/films"
              className="inline-flex rounded-lg border border-slate-700 px-6 py-3 text-sm font-semibold text-slate-300 transition-colors hover:border-amber-600 hover:text-amber-400"
            >
              Explore All Projects
            </Link>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-amber-500">
        <div className="mx-auto max-w-7xl px-6 py-16 text-center">
          <h2 className="text-3xl font-bold text-slate-900">
            Ready to invest in the future of film?
          </h2>
          <p className="mt-3 text-slate-800 max-w-xl mx-auto">
            Join the platform where financial intelligence meets creative capital.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link
              href="/newsroom"
              className="rounded-lg bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-slate-800"
            >
              Open Newsroom
            </Link>
            <Link
              href="/portal"
              className="rounded-lg border border-slate-700 bg-transparent px-6 py-3 text-sm font-semibold text-slate-900 transition-colors hover:bg-slate-900/10"
            >
              Access Portal
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}

function ValueProp({
  icon,
  title,
  body,
  comingSoon = false,
}: {
  icon: string;
  title: string;
  body: string;
  comingSoon?: boolean;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
      <div className="text-3xl">{icon}</div>
      <div className="mt-4 flex items-center gap-2">
        <h3 className="font-semibold text-white">{title}</h3>
        {comingSoon && (
          <span className="rounded bg-slate-800 px-1.5 py-0.5 text-xs text-slate-500 border border-slate-700">
            Soon
          </span>
        )}
      </div>
      <p className="mt-2 text-sm text-slate-400 leading-relaxed">{body}</p>
    </div>
  );
}
