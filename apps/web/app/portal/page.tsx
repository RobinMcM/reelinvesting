import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Research Portal',
};

export default function PortalPage() {
  return (
    <section className="flex min-h-[70vh] items-center justify-center bg-slate-950">
      <div className="mx-auto max-w-lg px-6 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border border-slate-700 bg-slate-900 text-2xl">
          🔬
        </div>
        <h1 className="mt-6 text-2xl font-bold text-white">Research &amp; Analytics Portal</h1>
        <p className="mt-3 text-slate-400">
          The private portal for accredited investors and research subscribers.
          Advanced analytics, curated intelligence, and film project deep-dives
          will be available here.
        </p>
        <div className="mt-8 rounded-lg border border-slate-700/50 bg-slate-900 p-4 text-left">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Planned features
          </p>
          <ul className="mt-3 space-y-1.5 text-sm text-slate-400">
            <li>• Personalised intelligence dashboard</li>
            <li>• Asset impact analysis &amp; trend tracking</li>
            <li>• Film project financials &amp; documents</li>
            <li>• Sector &amp; macro watchlists</li>
            <li>• Export &amp; reporting tools</li>
          </ul>
        </div>
        <p className="mt-6 text-xs text-slate-600">
          Trading tools, broker integrations, and buy/sell signals are not part of
          this platform.
        </p>
        <Link
          href="/"
          className="mt-6 inline-flex text-sm font-medium text-amber-400 hover:text-amber-300 transition-colors"
        >
          ← Back to homepage
        </Link>
      </div>
    </section>
  );
}
