'use client';

import { useEffect, useState } from 'react';
import type { IntelligenceEvent } from '@/lib/types';
import EventCard from './EventCard';

interface Props {
  events: IntelligenceEvent[];
}

export default function FeaturedEventRotator({ events }: Props) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (events.length <= 1) return;
    const id = setInterval(() => {
      setIndex((i) => (i + 1) % events.length);
    }, 8000);
    return () => clearInterval(id);
  }, [events.length]);

  if (events.length === 0) return null;

  return (
    <div>
      <EventCard event={events[index]} featured />
      {events.length > 1 && (
        <div className="mt-3 flex items-center justify-center gap-1.5">
          {events.map((_, i) => (
            <button
              key={i}
              onClick={() => setIndex(i)}
              className={`h-1.5 rounded-full transition-all ${
                i === index ? 'w-6 bg-amber-500' : 'w-1.5 bg-slate-700 hover:bg-slate-600'
              }`}
              aria-label={`Show event ${i + 1}`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
