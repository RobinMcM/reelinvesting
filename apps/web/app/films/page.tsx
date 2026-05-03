import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Film Projects',
  description: 'Curated independent film investment opportunities from ReelInvesting.',
};

const PLACEHOLDER_FILMS = [
  { id: 1, title: 'Project Atlas', genre: 'Drama', status: 'In Development', stage: 'Pre-Production' },
  { id: 2, title: 'Project Meridian', genre: 'Thriller', status: 'In Development', stage: 'Script Phase' },
  { id: 3, title: 'Project Nova', genre: 'Documentary', status: 'Coming Soon', stage: 'Greenlit' },
  { id: 4, title: 'Project Zenith', genre: 'Action', status: 'Coming Soon', stage: 'Development' },
  { id: 5, title: 'Project Solstice', genre: 'Drama', status: 'Coming Soon', stage: 'Pre-Production' },
  { id: 6, title: 'Project Horizon', genre: 'Sci-Fi', status: 'Coming Soon', stage: 'Script Phase' },
];

export default function FilmsPage() {
  return (
    <>
      {/* Hero */}
      <section className="border-b border-slate-800 bg-brand-navy py-20">
        <div className="mx-auto max-w-7xl px-6">
          <p className="text-xs font-semibold uppercase tracking-widest text-amber-500">
            Film Portfolio
          </p>
          <h1 className="mt-3 text-4xl font-bold text-white sm:text-5xl">
            Film Projects
          </h1>
          <p className="mt-4 max-w-2xl text-slate-400">
            We're curating a slate of independent film investment opportunities from
            established producers and emerging directors. Projects will be available
            for qualified investors upon platform launch.
          </p>
        </div>
      </section>

      {/* Filter bar — placeholder */}
      <section className="border-b border-slate-800 bg-slate-900">
        <div className="mx-auto max-w-7xl px-6 py-4">
          <div className="flex items-center gap-3 flex-wrap">
            <span className="text-xs text-slate-500">Filter by:</span>
            {['All', 'Drama', 'Thriller', 'Documentary', 'Action', 'Sci-Fi'].map((genre) => (
              <button
                key={genre}
                className={`rounded px-3 py-1 text-xs font-medium transition-colors ${
                  genre === 'All'
                    ? 'bg-amber-500 text-slate-900'
                    : 'border border-slate-700 text-slate-400 hover:border-amber-700/60 hover:text-amber-400'
                }`}
              >
                {genre}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Films grid */}
      <section className="bg-slate-950 py-16">
        <div className="mx-auto max-w-7xl px-6">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {PLACEHOLDER_FILMS.map((film) => (
              <FilmCard key={film.id} film={film} />
            ))}
          </div>

          {/* CTA */}
          <div className="mt-16 rounded-xl border border-amber-700/30 bg-amber-900/10 p-8 text-center">
            <h2 className="text-xl font-semibold text-white">
              Interested in film investment opportunities?
            </h2>
            <p className="mt-2 text-slate-400 text-sm max-w-md mx-auto">
              Full project details, financials, and investment terms will be available
              to registered investors when projects go live.
            </p>
            <button className="mt-6 rounded-lg bg-amber-500 px-6 py-2.5 text-sm font-semibold text-slate-900 transition-colors hover:bg-amber-400">
              Register Interest
            </button>
            <p className="mt-3 text-xs text-slate-600">
              No commitment required. We'll notify you when projects open for investment.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}

function FilmCard({
  film,
}: {
  film: { id: number; title: string; genre: string; status: string; stage: string };
}) {
  return (
    <div className="group rounded-xl border border-slate-800 bg-slate-900 overflow-hidden transition-colors hover:border-amber-700/40">
      {/* Poster placeholder */}
      <div className="relative h-48 bg-gradient-to-br from-slate-800 to-slate-900 flex items-center justify-center">
        <span className="text-5xl opacity-30">🎬</span>
        <div className="absolute top-3 right-3">
          <span className={`rounded px-2 py-0.5 text-xs font-semibold ${
            film.status === 'In Development'
              ? 'bg-amber-900/60 text-amber-300 border border-amber-700/50'
              : 'bg-slate-800 text-slate-400 border border-slate-700'
          }`}>
            {film.status}
          </span>
        </div>
      </div>

      {/* Info */}
      <div className="p-5">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-white group-hover:text-amber-400 transition-colors">
            {film.title}
          </h3>
          <span className="shrink-0 rounded bg-slate-800 px-2 py-0.5 text-xs text-slate-400 border border-slate-700">
            {film.genre}
          </span>
        </div>
        <p className="mt-1 text-xs text-slate-500">{film.stage}</p>

        <div className="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between">
          <span className="text-xs text-slate-600">Investment details TBA</span>
          <button className="text-xs text-amber-500 hover:text-amber-400 font-medium transition-colors">
            Register interest →
          </button>
        </div>
      </div>
    </div>
  );
}
