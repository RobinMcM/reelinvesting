import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Admin',
};

export default function AdminPage() {
  return (
    <section className="flex min-h-[70vh] items-center justify-center bg-slate-950">
      <div className="mx-auto max-w-lg px-6 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border border-slate-700 bg-slate-900 text-2xl">
          🔒
        </div>
        <h1 className="mt-6 text-2xl font-bold text-white">Private Admin Area</h1>
        <p className="mt-3 text-slate-400">
          This area is restricted to ReelInvesting administrators. Authentication
          and role-based access control will be added in a future release.
        </p>
        <div className="mt-8 rounded-lg border border-amber-700/30 bg-amber-900/10 p-4 text-left">
          <p className="text-xs font-semibold uppercase tracking-wide text-amber-500">
            Coming soon
          </p>
          <ul className="mt-3 space-y-1.5 text-sm text-slate-400">
            <li>• Intelligence source management</li>
            <li>• Event review &amp; classification</li>
            <li>• Agitator profile configuration</li>
            <li>• Ingestion monitoring &amp; stats</li>
          </ul>
        </div>
        <Link
          href="/"
          className="mt-8 inline-flex text-sm font-medium text-amber-400 hover:text-amber-300 transition-colors"
        >
          ← Back to homepage
        </Link>
      </div>
    </section>
  );
}
