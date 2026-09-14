"use client";

import React from "react";
import Link from "next/link";
import {
  FlaskConical,
  Sparkles,
  Terminal,
  ArrowRight,
  BookOpen,
} from "lucide-react";
import { Button } from "@/components/ui/button";

interface LabLauncherBannerProps {
  title?: string;
  labId?: string | number;
  description?: string;
}

export function LabLauncherBanner({
  title = "Interactive Practice Lab",
  labId = "1001",
  description = "Isolated Python 3.11 execution sandbox with reactive Marimo extensions and automatic test case grading.",
}: LabLauncherBannerProps) {
  return (
    <div className="hero-gradient relative overflow-hidden rounded-2xl p-6 text-white border border-slate-800/40 shadow-md space-y-4">
      <div className="absolute inset-0 hero-mesh opacity-30 pointer-events-none" />
      <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-light text-teal-300 border border-white/20 text-[11px] font-bold uppercase tracking-wider">
            <FlaskConical className="h-3.5 w-3.5 text-teal-300" /> Hands-on Jupyter &amp; Marimo Lab
          </div>
          <h3 className="text-base font-bold text-white">{title}</h3>
          <p className="text-xs text-white/80 max-w-xl leading-relaxed">
            {description}
          </p>
        </div>

        <Link href={`/labs/${labId}`} target="_blank" rel="noopener noreferrer">
          <Button
            size="sm"
            className="navy-teal-gradient text-white text-xs font-bold px-5 h-10 rounded-xl shadow-sm hover:opacity-95 transition-all cursor-pointer"
          >
            Launch Lab Workspace <ArrowRight className="h-3.5 w-3.5 ml-1" />
          </Button>
        </Link>
      </div>

      <div className="relative z-10 grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 text-xs border-t border-white/10 text-white/80">
        <div className="flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-amber-300" />
          <span>Jupyter Cell Runner</span>
        </div>
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-teal-300" />
          <span>Marimo Reactive DAG</span>
        </div>
        <div className="flex items-center gap-2">
          <Terminal className="h-4 w-4 text-blue-300" />
          <span>Docker Sandbox Console</span>
        </div>
      </div>
    </div>
  );
}

export default LabLauncherBanner;
