import type { IntelligenceEvent } from '@/lib/types';
import { relativeTime, formatSourceType } from '@/lib/utils';
import ImpactBadge from './ImpactBadge';
import TickerPill from './TickerPill';

interface Props {
  event: IntelligenceEvent;
  featured?: boolean;
}

export default function EventCard({ event, featured = false }: Props) {
  const tickers = Array.isArray(event.tickers) ? event.tickers.slice(0, 5) : [];

  return (
    <article
      className={`flex flex-col rounded-xl border bg-slate-900 transition-colors hover:border-amber-700/60 ${
        featured
          ? 'border-amber-700/40 p-6'
          : 'border-slate-700/50 p-5'
      }`}
    >
      {/* Header row */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="rounded bg-slate-800 px-2 py-0.5 text-xs font-medium text-slate-300 border border-slate-700">
          {formatSourceType(event.source_type)}
        </span>
        {event.event_type && (
          <span className="text-xs text-slate-500">{event.event_type}</span>
        )}
        <span className="ml-auto text-xs text-slate-500 shrink-0">
          {relativeTime(event.published_at)}
        </span>
      </div>

      {/* Title */}
      <h3
        className={`mt-3 font-semibold leading-snug text-slate-100 ${
          featured ? 'text-xl' : 'text-base'
        }`}
      >
        {event.url ? (
          <a
            href={event.url}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-amber-400 transition-colors"
          >
            {event.title}
          </a>
        ) : (
          event.title
        )}
      </h3>

      {/* Preview */}
      {event.body_preview && (
        <p className="mt-2 text-sm text-slate-400 line-clamp-2">
          {event.body_preview}
        </p>
      )}

      {/* Tickers */}
      {tickers.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          <span className="text-xs text-slate-500 self-center">Affected assets:</span>
          {tickers.map((t) => (
            <TickerPill key={t} symbol={String(t)} />
          ))}
        </div>
      )}

      {/* Scores */}
      <div className="mt-4 flex items-center gap-3 flex-wrap">
        <ImpactBadge score={event.impact_rating} />
        <ScorePill label="Market relevance" value={event.market_relevance} />
        <ScorePill label="Confidence" value={event.confidence} />
        {featured && <ScorePill label="Newsworthiness" value={event.newsworthiness} />}
      </div>

      {/* Source */}
      <p className="mt-3 text-xs text-slate-600">
        Source: {event.source_name}
      </p>
    </article>
  );
}

function ScorePill({ label, value }: { label: string; value: number | null }) {
  if (value === null) return null;
  return (
    <span className="text-xs text-slate-400">
      {label}:{' '}
      <span className="font-semibold text-slate-200">{value}</span>
      <span className="text-slate-600">/100</span>
    </span>
  );
}
