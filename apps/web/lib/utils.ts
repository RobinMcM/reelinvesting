export function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const minutes = Math.floor(diff / 60_000);
  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export function scoreLabel(score: number | null): string {
  if (score === null) return '—';
  if (score >= 80) return 'High';
  if (score >= 50) return 'Medium';
  return 'Low';
}

export function scoreColor(score: number | null): string {
  if (score === null) return 'text-slate-400';
  if (score >= 80) return 'text-red-400';
  if (score >= 50) return 'text-amber-400';
  return 'text-emerald-400';
}

export function formatSourceType(s: string): string {
  return s.charAt(0) + s.slice(1).toLowerCase();
}
