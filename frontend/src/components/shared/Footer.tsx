"use client";

import { usePathname } from "next/navigation";

export function Footer() {
  const pathname = usePathname();

  // On homepage (/), the Help section contains the comprehensive integrated institutional footer
  if (pathname === "/") {
    return null;
  }

  return (
    <footer className="border-t border-slate-200 bg-white py-8 text-center text-xs text-slate-500" suppressHydrationWarning>
      <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4" suppressHydrationWarning>
        <p>
          © 2026 iGOT Karmayogi Bharat • Capacity Building Commission • Ministry of Statistics and Programme Implementation
        </p>
        <div className="flex gap-6 text-slate-400">
          <a href="/discover" className="hover:text-slate-600 transition-colors">Privacy Policy</a>
          <a href="/discover" className="hover:text-slate-600 transition-colors">Terms of Service</a>
          <a href="/discover" className="hover:text-slate-600 transition-colors">National Data Governance</a>
          <a href="/#help" className="hover:text-slate-600 transition-colors">Helpdesk</a>
        </div>
      </div>
    </footer>
  );
}
