export type SourceType =
  | 'NEWS'
  | 'AGITATOR'
  | 'SOCIAL'
  | 'MACRO'
  | 'FILING'
  | 'EARNINGS'
  | 'REGULATORY'
  | 'UNKNOWN';

export type AssetType =
  | 'STOCK'
  | 'CRYPTO'
  | 'FOREX'
  | 'COMMODITY'
  | 'INDEX'
  | 'MACRO'
  | 'UNKNOWN';

export type EventStatus = 'RAW' | 'STORED' | 'CLASSIFIED' | 'IGNORED' | 'ERROR';

export type ImpactDirection = 'BULLISH' | 'BEARISH' | 'NEUTRAL' | 'UNCERTAIN';

export type TimeHorizon =
  | 'INTRADAY'
  | 'ONE_DAY'
  | 'ONE_WEEK'
  | 'LONG_TERM'
  | 'UNKNOWN';

export interface AssetImpact {
  id: string;
  event_id: string;
  symbol: string;
  asset_type: AssetType;
  direction: ImpactDirection;
  impact_score: number;
  confidence: number;
  time_horizon: TimeHorizon;
  reason: string | null;
  created_at: string;
}

export interface IntelligenceEvent {
  id: string;
  source_type: SourceType;
  source_name: string;
  external_id: string | null;
  stable_id: string;
  title: string;
  body_preview: string | null;
  url: string | null;
  published_at: string;
  spaces_key: string;
  event_type: string | null;
  asset_type: AssetType;
  tickers: string[];
  sectors: string[];
  entities: string[];
  newsworthiness: number | null;
  attention_score: number | null;
  virality_score: number | null;
  market_relevance: number | null;
  impact_rating: number | null;
  confidence: number | null;
  status: EventStatus;
  created_at: string;
  updated_at: string;
  asset_impacts?: AssetImpact[];
}

export interface AdminStats {
  total_events: number;
  events_by_status: Record<string, number>;
  events_by_source_type: Record<string, number>;
  last_published_at: string | null;
}
