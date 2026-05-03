import type { AdminStats, IntelligenceEvent } from './types';

const BASE_URL =
  process.env.NEXT_PUBLIC_INDEXER_API_URL || 'http://localhost:8000';

async function apiFetch<T>(path: string): Promise<T | null> {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return null;
    return res.json() as Promise<T>;
  } catch {
    return null;
  }
}

export async function getRecentEvents(limit = 20): Promise<IntelligenceEvent[]> {
  const data = await apiFetch<IntelligenceEvent[]>(`/events/recent?limit=${limit}`);
  return data ?? [];
}

export async function getHighImpactEvents(
  minScore = 60,
  limit = 10,
): Promise<IntelligenceEvent[]> {
  const data = await apiFetch<IntelligenceEvent[]>(
    `/events/high-impact?min_score=${minScore}&limit=${limit}`,
  );
  return data ?? [];
}

export async function getAdminStats(): Promise<AdminStats | null> {
  return apiFetch<AdminStats>('/admin/stats');
}
