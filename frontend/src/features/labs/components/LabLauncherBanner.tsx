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
    <div className="rounded-2xl bg-gradient-to-r from-slate-950 via-[#0F172A] to-[#1E3A8A] p-6 text-white border border-slate-800 shadow-md space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[11px] font-bold">
            <FlaskConical className="h-3.5 w-3.5" /> Hands-on Jupyter &amp; Marimo Lab
          </div>
          <h3 className="text-base font-bold text-white">{title}</h3>
          <p className="text-xs text-slate-300 max-w-xl">
            {description}
          </p>
        </div>

        <Link href={`/labs/${labId}`} target="_blank" rel="noopener noreferrer">
          <Button
            size="sm"
            className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-5 shadow-xs cursor-pointer"
          >
            Launch Lab Workspace <ArrowRight className="h-3.5 w-3.5 ml-1" />
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs border-t border-slate-800 text-slate-300">
        <div className="flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-amber-400" />
          <span>Jupyter Cell Runner</span>
        </div>
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-emerald-400" />
          <span>Marimo Reactive DAG</span>
        </div>
        <div className="flex items-center gap-2">
          <Terminal className="h-4 w-4 text-cyan-400" />
          <span>Docker Sandbox Console</span>
        </div>
      </div>
    </div>
  );
}

export default LabLauncherBanner;
