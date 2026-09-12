import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Karmayogi+ — Intelligence for continuous capacity building",
  description:
    "An AI-enabled Skill Intelligence and Adaptive Learning Platform integrated with the iGOT Karmayogi ecosystem.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
