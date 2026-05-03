'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navLinks = [
  { href: '/films', label: 'Films' },
  { href: '/newsroom', label: 'Newsroom' },
  { href: '/portal', label: 'Portal' },
];

export default function Header() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-brand-navy/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2 group">
          <span className="text-xl font-bold tracking-tight text-white group-hover:text-amber-400 transition-colors">
            Reel<span className="text-amber-400">Investing</span>
          </span>
        </Link>

        <nav className="hidden sm:flex items-center gap-6">
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`text-sm font-medium transition-colors ${
                pathname?.startsWith(href)
                  ? 'text-amber-400'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              {label}
            </Link>
          ))}
          <Link
            href="/admin"
            className="rounded border border-slate-700 px-3 py-1.5 text-xs font-medium text-slate-400 transition-colors hover:border-amber-700/60 hover:text-amber-400"
          >
            Admin
          </Link>
        </nav>

        {/* Mobile nav */}
        <nav className="flex sm:hidden items-center gap-4">
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`text-sm font-medium transition-colors ${
                pathname?.startsWith(href)
                  ? 'text-amber-400'
                  : 'text-slate-300'
              }`}
            >
              {label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
