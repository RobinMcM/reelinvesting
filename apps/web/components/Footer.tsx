import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-brand-navy">
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
          <div>
            <span className="text-lg font-bold text-white">
              Reel<span className="text-amber-400">Investing</span>
            </span>
            <p className="mt-3 text-sm text-slate-400 leading-relaxed">
              Intelligence-driven film investment. Surfacing signals that matter
              for independent film finance.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-widest text-slate-500">Platform</h4>
            <ul className="mt-3 space-y-2">
              {[
                { href: '/films', label: 'Film Projects' },
                { href: '/newsroom', label: 'Newsroom' },
                { href: '/portal', label: 'Research Portal' },
                { href: '/admin', label: 'Admin' },
              ].map(({ href, label }) => (
                <li key={href}>
                  <Link href={href} className="text-sm text-slate-400 hover:text-white transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-widest text-slate-500">Legal</h4>
            <p className="mt-3 text-xs text-slate-500 leading-relaxed">
              ReelInvesting does not provide financial advice, trading signals,
              or investment recommendations. All market intelligence is for
              informational purposes only. Past performance is not indicative of
              future results.
            </p>
          </div>
        </div>

        <div className="mt-10 border-t border-slate-800 pt-6 text-xs text-slate-600">
          © {new Date().getFullYear()} ReelInvesting. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
