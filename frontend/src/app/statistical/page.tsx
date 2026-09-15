import React from "react";
import Link from "next/link";
import {
  Brain,
  BarChart3,
  BookOpen,
  Award,
  TrendingUp,
  Scale,
  Calculator,
  Building2,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Layers,
  LineChart,
  Binary,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export const metadata = {
  title: "Statistical Competency & Adaptive Engine | iGOT Karmayogi",
  description:
    "Official Indian Civil Service Competency Hub for Consumer Price Index (CPI), 3PL Item Response Theory (IRT), and Econometric Modeling.",
};

const STATISTICAL_PILLARS = [
  {
    icon: Calculator,
    title: "1. Index Number Theory & CPI Compilation",
    description:
      "Laspeyres, Paasche, and Fisher ideal index formulas. Jevons geometric mean aggregations, budget share expenditure weighting, and base year revisions (2012=100).",
    badge: "CPI Methodology",
    color: "from-blue-600 to-indigo-700",
  },
  {
    icon: Brain,
    title: "2. Item Response Theory (3PL Psychometrics)",
    description:
      "Lord's 3-Parameter Logistic (3PL) model. Item discrimination (a), difficulty (b), and guessing (c) parameters driving computerized adaptive branching.",
    badge: "Psychometrics",
    color: "from-teal-600 to-emerald-700",
  },
  {
    icon: Layers,
    title: "3. Survey Sampling & Stratified Estimation",
    description:
      "NSSO multi-stage stratified random sampling, primary sampling units (PSUs), design weight multipliers, and sampling error minimization.",
    badge: "Survey Science",
    color: "from-purple-600 to-violet-800",
  },
  {
    icon: LineChart,
    title: "4. National Macroeconomic Indicators",
    description:
      "Compilation of the Index of Industrial Production (IIP), Wholesale Price Index (WPI), Gross Domestic Product deflators, and System of National Accounts (SNA 2008).",
    badge: "Macroeconomics",
    color: "from-sky-600 to-blue-800",
  },
  {
    icon: Binary,
    title: "5. Microdata Imputation & Outlier Auditing",
    description:
      "Hot-deck imputation, seasonal carryforward modeling, cold-deck substitution, trimmed means, and automated price quote anomaly rejection.",
    badge: "Data Integrity",
    color: "from-amber-600 to-orange-700",
  },
];

export default function StatisticalCompetencyHubPage() {
  return (
    <div className="min-h-[calc(100vh-68px)] flex flex-col bg-[#F8FAFC] text-slate-900">
      {/* Hero Header - Full Edge-to-Edge matching Digital Governance */}
      <section className="hero-gradient relative overflow-hidden py-12 sm:py-16 text-white shadow-md border-b border-blue-900/40">
        <div className="absolute inset-0 hero-mesh opacity-40 pointer-events-none" />
        <div className="absolute -top-20 -right-20 w-96 h-96 rounded-full bg-teal-500/15 blur-[100px] pointer-events-none" />

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full glass-light border border-white/20 text-xs font-bold text-teal-300 uppercase tracking-wider mb-4">
            <Building2 className="h-3.5 w-3.5" />
            Ministry of Statistics &amp; Programme Implementation (MoSPI) • NSSTA
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight text-white">
            Statistical Competency &amp; Adaptive Engine
          </h1>
          <p className="mt-4 text-sm sm:text-base lg:text-lg text-white/70 max-w-3xl leading-relaxed">
            Apex psychometric and econometric capacity-building suite for Indian civil servants. Master official
            Consumer Price Index (CPI) compilations, Item Response Theory (IRT 3PL) psychometrics, and macroeconomic survey pipelines.
          </p>

          {/* Core Interactive Action Buttons */}
          <div className="mt-8 flex flex-wrap items-center gap-4">
            <Link href="/statistical/exam">
              <Button
                size="lg"
                className="h-12 px-6 rounded-xl bg-white hover:bg-slate-100 text-[#1E3A8A] font-bold text-sm shadow-lg border-0 flex items-center gap-2.5 transition-transform hover:scale-105 cursor-pointer"
              >
                <Brain className="h-5 w-5 text-[#1E3A8A]" />
                Launch Adaptive Exam (CAT Engine)
              </Button>
            </Link>

            <Link href="/courses/2">
              <Button
                size="lg"
                variant="outline"
                className="h-12 px-6 rounded-xl border-white/30 hover:bg-white/15 text-white font-semibold text-sm flex items-center gap-2.5 cursor-pointer"
              >
                <BarChart3 className="h-5 w-5 text-teal-300" />
                CPI Methodology Course
              </Button>
            </Link>

            <Link href="/discover?category=statistical">
              <Button
                size="lg"
                variant="ghost"
                className="h-12 px-5 rounded-xl text-white/80 hover:text-white hover:bg-white/10 text-sm font-medium flex items-center gap-2 cursor-pointer"
              >
                <BookOpen className="h-4 w-4" />
                Browse Statistical Courses
              </Button>
            </Link>
          </div>

          {/* Feature Badges */}
          <div className="mt-6 flex flex-wrap gap-3 pt-2">
            <div className="flex items-center gap-2 text-xs text-white/90 glass-light px-3 py-1.5 rounded-xl border border-white/15">
              <Calculator className="h-4 w-4 text-amber-300" />
              <span>CPI Base 2012=100</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-white/90 glass-light px-3 py-1.5 rounded-xl border border-white/15">
              <Brain className="h-4 w-4 text-teal-300" />
              <span>3PL Item Response Theory</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-white/90 glass-light px-3 py-1.5 rounded-xl border border-white/15">
              <ShieldCheck className="h-4 w-4 text-blue-300" />
              <span>National Statistical Commission Standard</span>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content Workspace */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12 space-y-12 flex-1 w-full">
        {/* Two Featured Interactive Hubs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Adaptive CAT Testing Card */}
          <Card className="border-slate-200 bg-white shadow-sm rounded-2xl overflow-hidden card-hover-lift border-t-4 border-t-[#1E3A8A]">
            <CardHeader className="pb-3 border-b border-slate-100">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#1E3A8A] bg-blue-50 px-2.5 py-1 rounded-full border border-blue-100">
                  Item Response Theory (IRT 3PL)
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  Dynamic θ Estimation
                </span>
              </div>
              <CardTitle className="text-lg font-bold text-slate-900 mt-2 flex items-center gap-2.5">
                <Brain className="h-5 w-5 text-[#1E3A8A]" />
                Psychometric Adaptive Examination Engine
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Engage with an intelligent testing environment that measures latent ability (θ) in real time. Items
                dynamically branch based on empirical item difficulty (b), discrimination (a), and guessing parameters (c)
                with instant Fisher information convergence.
              </p>
              <div className="flex flex-wrap gap-2 text-[11px] text-slate-600">
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Price Relatives
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Jevons Geometric Mean
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Laspeyres Formula
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Seasonal Imputation
                </span>
              </div>
              <div className="pt-2">
                <Link href="/statistical/exam" className="inline-block">
                  <Button className="h-10 px-5 rounded-xl navy-teal-gradient text-white text-xs font-bold shadow-sm flex items-center gap-2 cursor-pointer hover:opacity-95">
                    Enter Adaptive Exam Environment <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* CPI Compilation Card */}
          <Card className="border-slate-200 bg-white shadow-sm rounded-2xl overflow-hidden card-hover-lift border-t-4 border-t-teal-600">
            <CardHeader className="pb-3 border-b border-slate-100">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-teal-800 bg-teal-50 px-2.5 py-1 rounded-full border border-teal-100">
                  MoSPI Official Methodology
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  National Accounts Pipeline
                </span>
              </div>
              <CardTitle className="text-lg font-bold text-slate-900 mt-2 flex items-center gap-2.5">
                <BarChart3 className="h-5 w-5 text-teal-600" />
                CPI Compilation &amp; Basket Aggregation
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Master the complete operational pipeline for India&apos;s Consumer Price Index (Rural, Urban, and Combined).
                Compute item weights, validate price quotations against outlier thresholds, apply geometric mean chaining,
                and compile official monthly indices.
              </p>
              <div className="flex flex-wrap gap-2 text-[11px] text-slate-600">
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Base Year 2012=100
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Budget Share Weights
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  Imputation Rules
                </span>
                <span className="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 font-medium">
                  NSSTA Standard
                </span>
              </div>
              <div className="pt-2">
                <Link href="/courses/2" className="inline-block">
                  <Button className="h-10 px-5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold shadow-sm flex items-center gap-2 cursor-pointer">
                    Explore CPI Curriculum <ArrowRight className="h-4 w-4" />
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
              Curriculum Architecture: 5 National Statistical Pillars
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Structured in accordance with MoSPI standards, National Statistical Systems Training Academy (NSSTA)
              guidelines, and Capacity Building Commission competencies.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {STATISTICAL_PILLARS.map((p, idx) => {
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
                  <h4 className="text-sm font-bold text-slate-900">{p.title}</h4>
                  <p className="text-xs text-slate-500 leading-relaxed">{p.description}</p>
                </div>
              );
            })}

            {/* Pillar 6 / Capstone Certification Card */}
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
                  National Statistical Officer Accreditation
                </h4>
                <p className="text-xs text-white/70 leading-relaxed">
                  Computerized Adaptive Testing examination evaluating latent ability across all 5 national statistical pillars.
                </p>
              </div>
              <div className="pt-2">
                <Link href="/statistical/exam">
                  <span className="text-xs font-bold text-teal-300 hover:text-white inline-flex items-center gap-1.5 transition-colors cursor-pointer">
                    Launch Adaptive Examination →
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
