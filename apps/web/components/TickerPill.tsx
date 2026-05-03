interface Props {
  symbol: string;
}

export default function TickerPill({ symbol }: Props) {
  return (
    <span className="inline-flex items-center rounded bg-brand-navy border border-amber-700/40 px-2 py-0.5 text-xs font-mono font-semibold text-amber-400">
      {symbol}
    </span>
  );
}
