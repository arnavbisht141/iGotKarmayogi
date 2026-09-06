import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth/AuthContext";
import { I18nProvider } from "@/lib/i18n";
import { Navbar } from "@/components/shared/Navbar";
import { Footer } from "@/components/shared/Footer";
import { AiAssistantWidget } from "@/components/shared/AiAssistantWidget";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "iGOT Karmayogi | Skill Intelligence Platform (MoSPI)",
  description:
    "National digital learning platform for Indian civil servants and statisticians, powered by Mission Karmayogi.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.className} min-h-screen bg-[#EEE8E9] text-[#241E20] antialiased flex flex-col`}
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
