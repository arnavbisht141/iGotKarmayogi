import React from "react";
import Link from "next/link";
import {
  ShieldAlert,
  Zap,
  BookOpen,
  Award,
  Lock,
  Cloud,
  FileCode2,
  Building2,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export const metadata = {
  title: "Digital Governance & Cybersecurity Competency | iGOT Karmayogi",
  description:
    "Official Indian Civil Service Competency Hub for Cyber Defense, Incident Response, and Digital Governance compliance.",
};

const PILLARS = [
  {
    icon: ShieldAlert,
    title: "1. Cybersecurity & CERT-In Directives",
    description:
      "Mandatory 6-hour incident reporting, log retention rules, and defensive incident response triage for government systems.",
    badge: "SOC & DFIR",
    color: "from-blue-600 to-indigo-700",
  },
  {
    icon: Lock,
    title: "2. Data Privacy & DPDP Act 2023",
    description:
      "Digital Personal Data Protection Act compliance, consent frameworks, data principal rights, and significant data fiduciary obligations.",
    badge: "Compliance",
    color: "from-teal-600 to-emerald-700",
  },
  {
    icon: ShieldCheck,
    title: "3. PKI & Digital Signatures",
    description:
      "IT Act 2000 Section 3A/65B evidentiary integrity, CCA licensed Certifying Authorities, and CRL certificate revocation verification.",
    badge: "Evidentiary Law",
    color: "from-purple-600 to-violet-800",
  },
  {
    icon: Cloud,
    title: "4. MeghRaj Cloud Governance",
    description:
      "MeitY-empanelled CSP auditing, cross-border data transfer restrictions, Service Control Policies (SCPs), and STQC compliance.",
    badge: "Cloud SecOps",
    color: "from-sky-600 to-blue-800",
  },
  {
    icon: FileCode2,
    title: "5. Digital Public Infrastructure (DPI)",
    description:
      "India Stack, API Setu gateway replay protection, HMAC signature verification, and secure citizen service interoperability.",
    badge: "API Security",
    color: "from-amber-600 to-orange-700",
  },
];

export default function DigitalGovernanceHubPage() {
  return (
    <div className="min-h-[calc(100vh-68px)] flex flex-col bg-[#F8FAFC] text-slate-900">
      {/* Hero Header */}
      <section className="hero-gradient relative overflow-hidden py-12 sm:py-16 text-white">
        <div className="absolute inset-0 hero-mesh opacity-40 pointer-events-none" />
        <div className="absolute -top-20 -right-20 w-96 h-96 rounded-full bg-teal-500/15 blur-[100px] pointer-events-none" />

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full glass-light border border-white/20 text-xs font-bold text-teal-300 uppercase tracking-wider mb-4">
            <Building2 className="h-3.5 w-3.5" />
            Ministry of Statistics & Programme Implementation (MoSPI)
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
            Digital Governance & Cybersecurity
          </h1>
          <p className="mt-4 text-sm sm:text-base lg:text-lg text-white/70 max-w-3xl leading-relaxed">
            Apex capacity building track for civil servants administering
            digital public infrastructure, incident command, and national cyber
            defense under MeitY and CERT-In mandates.
          </p>

          {/* Core Interactive Action Buttons */}
          <div className="mt-8 flex flex-wrap items-center gap-4">
            <Link href="/digital-governance/sandbox">
              <Button
                size="lg"
                className="h-12 px-6 rounded-xl bg-white hover:bg-slate-100 text-[#1E3A8A] font-bold text-sm shadow-lg border-0 flex items-center gap-2.5 transition-transform hover:scale-105 cursor-pointer"
              >
                <ShieldAlert className="h-5 w-5 text-[#1E3A8A]" />
                Launch Cyber Sandbox (8 CTF Labs)
              </Button>
            </Link>

            <Link href="/digital-governance/scenarios">
              <Button
                size="lg"
                variant="outline"
                className="h-12 px-6 rounded-xl border-white/30 hover:bg-white/15 text-white font-semibold text-sm flex items-center gap-2.5 cursor-pointer"
              >
                <Zap className="h-5 w-5 text-amber-300" />
                Tabletop Crisis Simulations
              </Button>
            </Link>

            <Link href="/discover?category=digital-governance">
              <Button
                size="lg"
                variant="ghost"
                className="h-12 px-5 rounded-xl text-white/80 hover:text-white hover:bg-white/10 text-sm font-medium flex items-center gap-2 cursor-pointer"
              >
                <BookOpen className="h-4 w-4" />
                Browse Governance Courses
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Main Content Workspace */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12 space-y-12 flex-1 w-full">
        {/* Two Featured Interactive Hubs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Cyber Sandbox Card */}
          <Card className="border-slate-200 bg-white shadow-sm rounded-2xl overflow-hidden card-hover-lift border-t-4 border-t-[#1E3A8A]">
            <CardHeader className="pb-3 border-b border-slate-100">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#1E3A8A] bg-blue-50 px-2.5 py-1 rounded-full border border-blue-100">
                  Interactive Marimo Console
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  600–800 Lines / Lab
                </span>
              </div>
              <CardTitle className="text-lg font-bold text-slate-900 mt-2 flex items-center gap-2.5">
                <ShieldAlert className="h-5 w-5 text-[#1E3A8A]" />
                Cyber Defense CTF Sandbox
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Step into authentic Digital Forensic and Incident Response
                (DFIR) investigations. Analyze raw RFC 822 emails, GTFOBins sudo
                escalations, SQLi vulnerabilities, and CloudTrail telemetry
                directly inside an interactive, code-hidden analysis console.
              </p>
              <div className="flex flex-wrap gap-2 text-[11px] text-slate-600">
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  SOC Auth Anomaly
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Phishing Carving
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  PKI Dispute
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  API Setu Replay
                </span>
              </div>
              <div className="pt-2">
                <Link
                  href="/digital-governance/sandbox"
                  className="inline-block"
                >
                  <Button className="h-10 px-5 rounded-xl navy-teal-gradient text-white text-xs font-bold shadow-sm flex items-center gap-2 cursor-pointer hover:opacity-95">
                    Enter Sandbox Labs <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Tabletop Scenarios Card */}
          <Card className="border-slate-200 bg-white shadow-sm rounded-2xl overflow-hidden card-hover-lift border-t-4 border-t-amber-500">
            <CardHeader className="pb-3 border-b border-slate-100">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-800 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">
                  National Incident Command
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  Multi-Turn Injects
                </span>
              </div>
              <CardTitle className="text-lg font-bold text-slate-900 mt-2 flex items-center gap-2.5">
                <Zap className="h-5 w-5 text-amber-500" />
                Tabletop Crisis Simulations
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Experience high-stakes cyber crisis simulations facing Indian
                government infrastructure. Make critical executive decisions
                under strict countdown clocks, navigate CERT-In 6-hour reporting
                mandates, and minimize national impact across branching injects.
              </p>
              <div className="flex flex-wrap gap-2 text-[11px] text-slate-600">
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  PFMS Breach
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  GeM Ransomware
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  State Portal Defacement
                </span>
              </div>
              <div className="pt-2">
                <Link
                  href="/digital-governance/scenarios"
                  className="inline-block"
                >
                  <Button className="h-10 px-5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white text-xs font-bold shadow-sm flex items-center gap-2 cursor-pointer">
                    Start Simulation <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 5 Pillars Curriculum Overview */}
        <div className="space-y-6">
          <div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
              Curriculum Architecture: 5 National Pillars
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Structured directly in accordance with Indian cybersecurity
              frameworks, statutory mandates, and Capacity Building Commission
              standards.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {PILLARS.map((p, idx) => {
              const IconComp = p.icon;
              return (
                <div
                  key={idx}
                  className="p-5 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-3 hover:border-[#1E3A8A]/40 transition-all group"
                >
                  <div className="flex items-center justify-between">
                    <div className="p-2 rounded-xl bg-slate-100 text-[#1E3A8A] group-hover:bg-[#1E3A8A] group-hover:text-white transition-colors">
                      <IconComp className="h-4 w-4" />
                    </div>
                    <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                      {p.badge}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-slate-900">
                    {p.title}
                  </h4>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    {p.description}
                  </p>
                </div>
              );
            })}

            {/* Pillar 6 / Capstone Card */}
            <div className="p-5 rounded-2xl bg-gradient-to-br from-[#0C1B3D] to-[#1E3A8A] text-white shadow-2xs space-y-3 flex flex-col justify-between">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="p-2 rounded-xl bg-white/10 text-teal-300">
                    <Award className="h-4 w-4" />
                  </div>
                  <span className="text-[10px] font-bold text-teal-300 bg-white/10 px-2 py-0.5 rounded">
                    Official Certification
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white">
                  National Cyber Defense Exam
                </h4>
                <p className="text-xs text-white/70 leading-relaxed">
                  15-question official competency examination evaluating mastery
                  across all 5 digital governance pillars.
                </p>
              </div>
              <div className="pt-2">
                <Link href="/digital-governance/sandbox">
                  <span className="text-xs font-bold text-teal-300 hover:text-white inline-flex items-center gap-1.5 transition-colors cursor-pointer">
                    Complete Labs to Qualify →
                  </span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
