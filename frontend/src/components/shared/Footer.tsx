"use client";

import { usePathname } from "next/navigation";

export function Footer() {
  const pathname = usePathname();

  // On landing page (/), the bottom section contains the integrated legal strip
  if (pathname === "/") {
    return null;
  }

  return (
    <footer className="border-t border-slate-800 bg-[#0B132B] py-8 text-xs text-slate-400" suppressHydrationWarning>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4" suppressHydrationWarning>
        <div className="flex flex-col sm:flex-row items-center gap-2 text-center sm:text-left">
          <span className="font-semibold text-slate-200">iGOT Karmayogi Bharat</span>
          <span className="hidden sm:inline text-slate-600">•</span>
          <span>Ministry of Statistics and Programme Implementation (MoSPI)</span>
          <span className="hidden sm:inline text-slate-600">•</span>
          <span>National Programme for Civil Services Capacity Building</span>
        </div>
        <div className="flex items-center gap-5 text-slate-400 text-[11px]">
          <a href="/discover" className="hover:text-slate-200 transition-colors">Privacy Policy</a>
          <span className="text-slate-700">•</span>
          <a href="/discover" className="hover:text-slate-200 transition-colors">Terms of Use</a>
          <span className="text-slate-700">•</span>
          <a href="/resources" className="hover:text-slate-200 transition-colors">Cadre Documents</a>
          <span className="text-slate-700">•</span>
          <a href="/help" className="hover:text-slate-200 transition-colors">Support Desk</a>
        </div>
      </div>
    </footer>
  );
}
