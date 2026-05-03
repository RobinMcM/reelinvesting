interface Props {
  score: number | null;
  label?: string;
}

export default function ImpactBadge({ score, label }: Props) {
  const level =
    score === null ? 'unknown' : score >= 80 ? 'high' : score >= 50 ? 'medium' : 'low';

  const styles: Record<string, string> = {
    high: 'bg-red-900/40 text-red-300 border border-red-700/50',
    medium: 'bg-amber-900/40 text-amber-300 border border-amber-700/50',
    low: 'bg-emerald-900/40 text-emerald-300 border border-emerald-700/50',
    unknown: 'bg-slate-800 text-slate-400 border border-slate-700',
  };

  const text: Record<string, string> = {
    high: label ?? 'High Impact',
    medium: label ?? 'Medium Impact',
    low: label ?? 'Low Impact',
    unknown: label ?? 'Unscored',
  };

  return (
    <span className={`inline-flex items-center rounded px-2 py-0.5 text-xs font-semibold uppercase tracking-wide ${styles[level]}`}>
      {text[level]}
    </span>
  );
}
