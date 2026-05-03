interface Props {
  label: string;
  value: string | number;
  subtitle?: string;
}

export default function StatCard({ label, value, subtitle }: Props) {
  return (
    <div className="rounded-lg border border-slate-700/50 bg-slate-800/50 p-5">
      <p className="text-sm text-slate-400 uppercase tracking-wide">{label}</p>
      <p className="mt-1 text-3xl font-bold text-white">{value}</p>
      {subtitle && <p className="mt-1 text-xs text-slate-500">{subtitle}</p>}
    </div>
  );
}
