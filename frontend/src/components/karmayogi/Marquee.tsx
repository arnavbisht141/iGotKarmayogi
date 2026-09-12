"use client";

import { useState, type ReactNode } from "react";
import { Pause, Play } from "lucide-react";

/** Two equal tracks keep the last frame of a loop aligned with its first. */
export function Marquee({ children, className, label }: {
  children: ReactNode;
  className: string;
  label: string;
}) {
  const [paused, setPaused] = useState(false);

  return (
    <div className={`marquee ${className}`} role="region" aria-label={label} data-paused={paused}>
      <div className="marquee-viewport" tabIndex={0} aria-label={`${label}. Focus or hover to pause scrolling.`}>
        <div className="marquee-track">
          <div className="marquee-group">{children}</div>
          <div className="marquee-group" aria-hidden="true">{children}</div>
        </div>
      </div>
      <button className="marquee-toggle" type="button" aria-label={`${paused ? "Play" : "Pause"} ${label.toLowerCase()}`} aria-pressed={paused} onClick={() => setPaused(!paused)}>
        {paused ? <Play size={14} /> : <Pause size={14} />}
      </button>
    </div>
  );
}
