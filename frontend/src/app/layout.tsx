import type { Metadata } from "next";
import { Plus_Jakarta_Sans, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth/AuthContext";
import { I18nProvider } from "@/lib/i18n";
import { Navbar } from "@/components/shared/Navbar";
import { Footer } from "@/components/shared/Footer";
import { AiAssistantWidget } from "@/features/assistant/components/AiAssistantWidget";

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

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
    <html lang="en" suppressHydrationWarning className={`${plusJakarta.variable} ${jetbrainsMono.variable}`}>
      <body
        className={`${plusJakarta.className} min-h-screen bg-[#F8FAFC] text-[#0F172A] antialiased flex flex-col font-sans`}
        suppressHydrationWarning
      >
        <I18nProvider>
          <AuthProvider>
            <Navbar />
            <main className="flex-1 w-full" suppressHydrationWarning>{children}</main>
            <AiAssistantWidget />
            {/* National Footer */}
            <Footer />
          </AuthProvider>
        </I18nProvider>
      </body>
    </html>
  );
}
