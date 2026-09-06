import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth/AuthContext";
import { I18nProvider } from "@/lib/i18n";
import { Navbar } from "@/components/shared/Navbar";
import { AiAssistantWidget } from "@/components/shared/AiAssistantWidget";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "iGOT Karmayogi Bharat | National Learning Platform for Civil Services (MoSPI)",
  description:
    "Integrated Government Online Training platform for Indian civil servants and statisticians, powered by Mission Karmayogi.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.className} min-h-screen bg-[#F8FAFC] text-[#0F172A] antialiased flex flex-col`}
        suppressHydrationWarning
      >
        <I18nProvider>
          <AuthProvider>
            <Navbar />
            <main className="flex-1 w-full" suppressHydrationWarning>{children}</main>
            <AiAssistantWidget />
            {/* National Footer */}
            <footer className="border-t border-slate-200 bg-white py-8 text-center text-xs text-slate-500" suppressHydrationWarning>
              <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4" suppressHydrationWarning>
                <p>
                  © 2026 iGOT Karmayogi Bharat • Capacity Building Commission • Ministry of Statistics and Programme Implementation
                </p>
                <div className="flex gap-6 text-slate-400">
                  <a href="#" className="hover:text-slate-600">Privacy Policy</a>
                  <a href="#" className="hover:text-slate-600">Terms of Service</a>
                  <a href="#" className="hover:text-slate-600">National Data Governance</a>
                  <a href="#" className="hover:text-slate-600">Helpdesk</a>
                </div>
              </div>
            </footer>
          </AuthProvider>
        </I18nProvider>
      </body>
    </html>
  );
}
