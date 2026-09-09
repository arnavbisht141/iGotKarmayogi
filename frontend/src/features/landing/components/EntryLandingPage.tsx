"use client";

import React, { useEffect, useState, useCallback, useMemo } from "react";
import {
  Compass,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  BarChart3,
  FileCheck2,
  Award,
  BookOpen,
  HelpCircle,
  FileText,
  Download,
  PhoneCall,
  Mail,
  CheckCircle2,
  Clock,
  Building2,
  Shield,
  Layers,
  Search,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";
import { useRouter } from "next/navigation";

export default function EntryLandingPage() {
  const { user } = useAuth();
  const router = useRouter();
  const { t, language } = useI18n();

  const heroSlides = useMemo(
    () => [
      {
        src: "/karmayogi.jpg",
        alt: language === "hi" ? "मिशन कर्मयोगी राष्ट्रीय क्षमता निर्माण" : "Mission Karmayogi civil service capacity building session",
        title: t("hero.slide1"),
      },
      {
        src: "/government-meeting.jpg",
        alt: language === "hi" ? "प्रशासनिक संवर्ग समीक्षा एवं नीति समन्वय" : "Government administrative cadre review and collaborative meeting",
        title: t("hero.slide2"),
      },
      {
        src: "/ai-daksh.jpg",
        alt: language === "hi" ? "एआई-दक्ष आधिकारिक सांख्यिकी एवं विश्लेषणात्मक उपकरण" : "AI-Daksh civil service intelligence and analytical tools",
        title: t("hero.slide3"),
      },
    ],
    [t, language]
  );

  const [currentSlide, setCurrentSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    if (user) router.push("/home");
  }, [user, router]);

  useEffect(() => {
    if (typeof window !== "undefined" && window.location.hash) {
      const id = window.location.hash.replace("#", "");
      const el = document.getElementById(id);
      if (el) {
        const timer = setTimeout(() => {
          const header = document.querySelector("header");
          const headerHeight = header ? Math.round(header.getBoundingClientRect().height) : 68;
          const targetTop = Math.round(el.getBoundingClientRect().top + window.scrollY - headerHeight);
          window.scrollTo({ top: Math.max(0, targetTop), behavior: "smooth" });
        }, 120);
        return () => clearTimeout(timer);
      }
    }
  }, []);

  useEffect(() => {
    if (isPaused) return;
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [isPaused, heroSlides.length]);

  const handlePrev = useCallback(() => {
    setCurrentSlide((prev) => (prev - 1 + heroSlides.length) % heroSlides.length);
  }, [heroSlides.length]);

  const handleNext = useCallback(() => {
    setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
  }, [heroSlides.length]);

  return (
    <div className="flex flex-col w-full text-slate-900 bg-[#F8FAFC]">

      {/* ════════════════════════════════════════════════
          1. HERO: Sovereign Executive Navy Canvas
          ════════════════════════════════════════════════ */}
      <section
        id="hero"
        className="scroll-mt-16 sm:scroll-mt-[68px] bg-[#0B132B] text-white py-12 sm:py-16 border-b border-slate-800 relative overflow-hidden"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10">
          {/* Two-Column Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">

            {/* Left Column: Authoritative Editorial Header */}
            <div className="lg:col-span-7 flex flex-col justify-start text-left">
              {/* Sovereign Masthead Tagline */}
              <div className="flex items-center gap-2 mb-4 text-xs font-semibold text-amber-400 tracking-wider uppercase">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
                <span>MoSPI • Capacity Building Commission • NPCSCB</span>
              </div>

              {/* Headline */}
              <h1 className="text-3xl sm:text-4xl lg:text-[44px] font-bold tracking-tight text-white leading-[1.15]">
                {t("hero.title")}
              </h1>

              {/* Subtitle */}
              <p className="mt-4 text-sm sm:text-base text-slate-300 font-normal leading-relaxed max-w-xl">
                {t("hero.subtitle")}
              </p>

              {/* CTAs: Solid, tactile actions without bouncy scaling */}
              <div className="mt-8 flex flex-wrap items-center gap-3">
                <a href="/login">
                  <Button
                    size="lg"
                    className="h-11 px-6 rounded-lg bg-white hover:bg-slate-100 text-slate-950 font-semibold text-xs shadow-xs border border-white transition-colors flex items-center gap-2 cursor-pointer active:translate-y-[1px]"
                  >
                    {t("hero.signIn")} <ArrowRight className="h-4 w-4" />
                  </Button>
                </a>
                <a href="/discover">
                  <Button
                    size="lg"
                    className="h-11 px-6 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium text-xs transition-colors flex items-center gap-2 cursor-pointer border border-slate-700 active:translate-y-[1px]"
                  >
                    <Compass className="h-4 w-4 text-amber-400" /> {t("hero.explore")}
                  </Button>
                </a>
              </div>

              {/* Verified Trust Strip */}
              <div className="mt-8 pt-5 border-t border-slate-800 flex flex-wrap items-center gap-x-6 gap-y-2.5">
                <span className="flex items-center gap-2 text-xs text-slate-300 font-medium">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> {t("hero.badgeMospi")}
                </span>
                <span className="flex items-center gap-2 text-xs text-slate-300 font-medium">
                  <Shield className="h-4 w-4 text-amber-400 shrink-0" /> {t("hero.badgeCbc")}
                </span>
                <span className="flex items-center gap-2 text-xs text-slate-300 font-medium">
                  <Award className="h-4 w-4 text-slate-400 shrink-0" /> {t("hero.badgeIso")}
                </span>
              </div>
            </div>

            {/* Right Column: Institutional Documentary Carousel */}
            <div className="lg:col-span-5 w-full flex flex-col items-end">
              <div className="w-full">
                <div
                  className="relative w-full h-[240px] sm:h-[280px] rounded-xl overflow-hidden border border-slate-700 shadow-xl bg-slate-900 group"
                  onMouseEnter={() => setIsPaused(true)}
                  onMouseLeave={() => setIsPaused(false)}
                >
                  {heroSlides.map((slide, idx) => (
                    <div
                      key={slide.src}
                      className={`absolute inset-0 flex items-center justify-center transition-opacity duration-500 ease-in-out ${
                        idx === currentSlide ? "opacity-100 z-10" : "opacity-0 z-0 pointer-events-none"
                      }`}
                    >
                      <img
                        src={slide.src}
                        alt={slide.alt}
                        className="w-full h-full object-cover block select-none"
                        loading={idx === 0 ? "eager" : "lazy"}
                      />
                      {/* Documented Caption Overlay */}
                      <div className="absolute inset-x-0 bottom-0 bg-slate-950/80 border-t border-slate-800 p-3">
                        <p className="text-white text-xs font-medium line-clamp-1">
                          {slide.title}
                        </p>
                      </div>
                    </div>
                  ))}

                  {/* Prev/Next Controls */}
                  <button
                    type="button"
                    onClick={handlePrev}
                    aria-label="Previous slide"
                    className="absolute left-3 top-1/2 -translate-y-1/2 z-20 h-8 w-8 rounded-lg bg-slate-950/70 border border-slate-700 text-white flex items-center justify-center transition-colors hover:bg-slate-900 cursor-pointer active:translate-y-[1px]"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  <button
                    type="button"
                    onClick={handleNext}
                    aria-label="Next slide"
                    className="absolute right-3 top-1/2 -translate-y-1/2 z-20 h-8 w-8 rounded-lg bg-slate-950/70 border border-slate-700 text-white flex items-center justify-center transition-colors hover:bg-slate-900 cursor-pointer active:translate-y-[1px]"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>

                {/* Stepper Indicators */}
                <div className="mt-3 flex items-center justify-center gap-1.5">
                  {heroSlides.map((_, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setCurrentSlide(idx)}
                      aria-label={`Slide ${idx + 1}`}
                      className={`transition-all rounded-full cursor-pointer ${
                        idx === currentSlide ? "w-6 h-1.5 bg-amber-400" : "w-1.5 h-1.5 bg-slate-700 hover:bg-slate-500"
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* ── Official Statistics Bar: Solid High-Precision Metric Ledger ── */}
          <div className="mt-12 sm:mt-14">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 bg-[#0F1D3D] border border-slate-800 rounded-xl p-4 sm:p-5">
              {[
                { num: t("stats.trainedCount"), label: t("stats.trainedLabel"), sub: t("stats.trainedSub") },
                { num: t("stats.modulesCount"), label: t("stats.modulesLabel"), sub: t("stats.modulesSub") },
                { num: t("stats.qualityCount"), label: t("stats.qualityLabel"), sub: t("stats.qualitySub") },
                { num: t("stats.certCount"), label: t("stats.certLabel"), sub: t("stats.certSub") },
              ].map((s, i) => (
                <div key={i} className="px-3 py-2 border-r border-slate-800/80 last:border-r-0">
                  <p className="text-2xl sm:text-3xl font-extrabold text-white font-tabular tracking-tight">{s.num}</p>
                  <p className="text-xs font-semibold text-slate-200 mt-1">{s.label}</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">{s.sub}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════════
          2. ABOUT: Institutional Cadre Governance & Standards
          ════════════════════════════════════════════════ */}
      <section
        id="about"
        className="scroll-mt-16 sm:scroll-mt-[68px] bg-white border-b border-slate-200 py-12 sm:py-16"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-start">

            {/* Left Column: Official Institutional Charter */}
            <div className="lg:col-span-5">
              <div className="rounded-xl border border-slate-200 bg-white shadow-xs overflow-hidden">
                <div className="bg-[#0B132B] px-5 py-3 border-b border-slate-800 flex items-center justify-between">
                  <span className="text-xs font-bold text-white uppercase tracking-wider">
                    {t("about.cardOrg")}
                  </span>
                  <span className="text-[10px] font-mono text-amber-400 font-semibold">
                    GOV.IN / MoSPI
                  </span>
                </div>
                <div className="p-5 space-y-4">
                  <div className="border-b border-slate-100 pb-3">
                    <p className="text-xs font-semibold text-slate-900">{t("about.cardSub")}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">National apex authority for official statistical competency accreditation</p>
                  </div>

                  <div className="space-y-2.5">
                    {[
                      { code: "CSO", name: "Central Statistics Office", role: t("about.item1Title"), detail: t("about.item1Desc") },
                      { code: "NSSO", name: "National Sample Survey Office", role: t("about.item2Title"), detail: t("about.item2Desc") },
                      { code: "NSSTA", name: "National Statistical Systems Training Academy", role: t("about.item3Title"), detail: t("about.item3Desc") },
                    ].map((item, i) => (
                      <div key={i} className="p-3 rounded-lg border border-slate-200 bg-slate-50/70">
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-xs font-bold text-[#1E3A8A]">{item.code}</span>
                          <span className="text-[10px] font-semibold text-slate-500 uppercase">{item.role}</span>
                        </div>
                        <p className="text-xs font-bold text-slate-900 mt-1">{item.name}</p>
                        <p className="text-[11px] text-slate-600 mt-1 leading-relaxed">{item.detail}</p>
                      </div>
                    ))}
                  </div>

                  <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span className="font-mono text-[11px]">ISO 9001:2015 Accredited</span>
                    <span className="font-semibold text-[#1E3A8A] text-[11px]">{t("hero.badgeIso")}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column: Mandate & Dual-Track Competency System */}
            <div className="lg:col-span-7">
              <div className="flex items-center gap-2 mb-2 text-xs font-semibold text-[#1E3A8A] tracking-wider uppercase">
                <span>Civil Services Capacity Building (NPCSCB)</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight leading-tight">
                {t("about.title")}
              </h2>
              <p className="mt-3 text-slate-600 text-sm leading-relaxed">
                {t("about.desc")}
              </p>

              {/* Asymmetrical Content Dossier instead of 3 icon boxes */}
              <div className="mt-8 space-y-4">
                <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-bold text-slate-900">{t("about.pillar1Title")}</h3>
                    <span className="text-[11px] font-mono font-semibold text-[#1E3A8A] bg-blue-50 border border-blue-200 px-2 py-0.5 rounded">
                      Domain Standard
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 leading-relaxed">{t("about.pillar1Desc")}</p>
                </div>

                <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-bold text-slate-900">{t("about.pillar2Title")}</h3>
                    <span className="text-[11px] font-mono font-semibold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded">
                      Verifiable 70% Pass
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 leading-relaxed">{t("about.pillar2Desc")}</p>
                </div>

                <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-bold text-slate-900">{t("about.pillar3Title")}</h3>
                    <span className="text-[11px] font-mono font-semibold text-amber-800 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
                      Cadre Assistance
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 leading-relaxed">{t("about.pillar3Desc")}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════════
          3. HOW IT WORKS: 4-Stage National Competency Pathway
          ════════════════════════════════════════════════ */}
      <section
        id="how-it-works"
        className="scroll-mt-16 sm:scroll-mt-[68px] bg-slate-50 border-b border-slate-200 py-12 sm:py-16"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#1E3A8A] uppercase tracking-wider mb-2">
              <span>National Learning Architecture</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {t("howItWorks.title")}
            </h2>
            <p className="mt-2 text-slate-600 text-xs sm:text-sm leading-relaxed">
              {t("howItWorks.subtitle")}
            </p>
          </div>

          {/* 4-Stage Pathway with Solid Clean Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {[
              {
                num: "01",
                stage: "Stage 01",
                title: t("howItWorks.step1Title"),
                desc: t("howItWorks.step1Desc"),
                status: "Authentication & Cadre Mapping",
              },
              {
                num: "02",
                stage: "Stage 02",
                title: t("howItWorks.step2Title"),
                desc: t("howItWorks.step2Desc"),
                status: "Accredited NSSTA Modules",
              },
              {
                num: "03",
                stage: "Stage 03",
                title: t("howItWorks.step3Title"),
                desc: t("howItWorks.step3Desc"),
                status: "70% Examination Gate",
              },
              {
                num: "04",
                stage: "Stage 04",
                title: t("howItWorks.step4Title"),
                desc: t("howItWorks.step4Desc"),
                status: "Cryptographic SHA-256 Record",
              },
            ].map((step, i) => (
              <div
                key={i}
                className="bg-white rounded-xl border border-slate-200 p-5 flex flex-col justify-between shadow-xs transition-colors hover:border-slate-300"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-mono text-xs font-bold text-[#1E3A8A] bg-blue-50 border border-blue-200 px-2 py-0.5 rounded">
                      {step.stage}
                    </span>
                    <span className="font-mono text-xs font-bold text-slate-400">
                      #{step.num}
                    </span>
                  </div>
                  <h3 className="font-bold text-slate-900 text-sm mb-2">{step.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{step.desc}</p>
                </div>
                <div className="mt-5 pt-3 border-t border-slate-100 text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
                  {step.status}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════════
          4. RESOURCES: Official Cadre Library & Documentation
          ════════════════════════════════════════════════ */}
      <section
        id="resources"
        className="scroll-mt-16 sm:scroll-mt-[68px] bg-white border-b border-slate-200 py-12 sm:py-16"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-8">
            <div>
              <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#1E3A8A] uppercase tracking-wider mb-2">
                <span>Official Repository</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                {t("resources.title")}
              </h2>
              <p className="mt-2 text-slate-600 text-xs sm:text-sm max-w-xl leading-relaxed">
                {t("resources.subtitle")}
              </p>
            </div>
            <a href="/discover" className="mt-4 md:mt-0">
              <Button
                variant="outline"
                size="sm"
                className="rounded-lg text-xs font-semibold cursor-pointer"
              >
                {t("resources.browseCatalog")} <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
              </Button>
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {[
              { tag: t("resources.doc1Tag"), title: t("resources.doc1Title"), desc: t("resources.doc1Desc"), size: "4.2 MB", code: "MoSPI-METH-01" },
              { tag: t("resources.doc2Tag"), title: t("resources.doc2Title"), desc: t("resources.doc2Desc"), size: "3.8 MB", code: "CSO-CPI-2024" },
              { tag: t("resources.doc3Tag"), title: t("resources.doc3Title"), desc: t("resources.doc3Desc"), size: "2.6 MB", code: "NSSTA-COR-04" },
              { tag: t("resources.doc4Tag"), title: t("resources.doc4Title"), desc: t("resources.doc4Desc"), size: "5.1 MB", code: "NSSO-FLD-79" },
            ].map((doc, i) => (
              <div key={i} className="bg-white rounded-xl border border-slate-200 p-5 flex flex-col justify-between shadow-xs transition-colors hover:border-slate-300">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-mono text-[10px] font-bold uppercase text-slate-500 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                      {doc.tag}
                    </span>
                    <span className="font-mono text-[10px] text-slate-400 font-semibold">
                      {doc.code}
                    </span>
                  </div>
                  <h3 className="font-bold text-slate-900 text-sm leading-snug">{doc.title}</h3>
                  <p className="text-xs text-slate-600 mt-2 leading-relaxed line-clamp-3">{doc.desc}</p>
                </div>

                <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="font-mono text-slate-500 text-[11px]">PDF • {doc.size}</span>
                  <a href="/discover" className="font-semibold text-[#1E3A8A] hover:underline flex items-center gap-1 cursor-pointer">
                    <Download className="h-3.5 w-3.5" /> {t("resources.access")}
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════════
          5. HELP: Departmental Support & Cadre Guidance
          ════════════════════════════════════════════════ */}
      <section
        id="help"
        className="scroll-mt-16 sm:scroll-mt-[68px] bg-slate-50 border-b border-slate-200 py-12 sm:py-16"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="text-center max-w-2xl mx-auto mb-10">
            <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#1E3A8A] uppercase tracking-wider mb-2">
              <span>Departmental Assistance</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {t("help.title")}
            </h2>
            <p className="mt-2 text-slate-600 text-xs sm:text-sm leading-relaxed">
              {t("help.subtitle")}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Card 1: Official Cadre Support Desk */}
            <div className="rounded-xl border border-slate-200 bg-white p-5 flex flex-col justify-between shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-bold text-[#1E3A8A] bg-blue-50 border border-blue-200 px-2 py-0.5 rounded">
                    Operational
                  </span>
                  <BookOpen className="h-4 w-4 text-[#1E3A8A]" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">{t("help.aiTitle")}</h3>
                <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t("help.aiDesc")}</p>
              </div>
              <div className="mt-5 pt-3 border-t border-slate-100">
                <a href="/login" className="inline-flex items-center text-xs font-semibold text-[#1E3A8A] hover:underline">
                  {t("help.aiLaunch")} <ArrowRight className="ml-1 h-3.5 w-3.5" />
                </a>
              </div>
            </div>

            {/* Card 2: Training Administration Desk */}
            <div className="rounded-xl border border-slate-200 bg-white p-5 flex flex-col justify-between shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded">
                    Direct Contact
                  </span>
                  <PhoneCall className="h-4 w-4 text-emerald-700" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">{t("help.deskTitle")}</h3>
                <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t("help.deskDesc")}</p>
                <div className="mt-3 space-y-1 text-xs text-slate-700 font-mono">
                  <p className="flex items-center gap-2"><Mail className="h-3.5 w-3.5 text-slate-400" /> support-karmayogi@gov.in</p>
                  <p className="flex items-center gap-2"><PhoneCall className="h-3.5 w-3.5 text-slate-400" /> 1800-11-KARM</p>
                </div>
              </div>
              <div className="mt-5 pt-3 border-t border-slate-100 flex items-center text-xs text-slate-500">
                <Clock className="h-3.5 w-3.5 mr-1.5 text-slate-400" /> {t("help.hours")}
              </div>
            </div>

            {/* Card 3: Frequently Consulted Regulations */}
            <div className="rounded-xl border border-slate-200 bg-white p-5 flex flex-col justify-between shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-bold text-amber-800 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
                    Regulations
                  </span>
                  <HelpCircle className="h-4 w-4 text-amber-700" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">{t("help.faqTitle")}</h3>
                <div className="mt-3 space-y-2 text-xs">
                  <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                    <p className="font-semibold text-slate-900">{t("help.faq1Q")}</p>
                    <p className="text-slate-600 mt-0.5 text-[11px] leading-relaxed">{t("help.faq1A")}</p>
                  </div>
                  <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                    <p className="font-semibold text-slate-900">{t("help.faq2Q")}</p>
                    <p className="text-slate-600 mt-0.5 text-[11px] leading-relaxed">{t("help.faq2A")}</p>
                  </div>
                </div>
              </div>
              <div className="mt-5 pt-3 border-t border-slate-100">
                <a href="/login" className="inline-flex items-center text-xs font-semibold text-[#1E3A8A] hover:underline">
                  {t("help.knowledgeBase")} <ArrowRight className="ml-1 h-3.5 w-3.5" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════════
          6. CLOSING CTA: Sovereign Executive Banner
          ════════════════════════════════════════════════ */}
      <section className="bg-[#0B132B] text-white py-10 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
            <div>
              <h3 className="text-lg sm:text-xl font-bold text-white tracking-tight">
                {t("cta.readyTitle")}
              </h3>
              <p className="text-xs text-slate-300 mt-1 max-w-xl leading-relaxed">{t("cta.readyDesc")}</p>
            </div>
            <div className="flex flex-wrap items-center gap-3 shrink-0">
              <a href="/login">
                <Button
                  variant="outline"
                  size="sm"
                  className="rounded-lg text-white border-slate-700 bg-slate-900 hover:bg-slate-800 px-5 text-xs font-semibold cursor-pointer active:translate-y-[1px]"
                >
                  {t("hero.signIn")}
                </Button>
              </a>
              <a href="/register">
                <Button
                  size="sm"
                  className="rounded-lg bg-[#1E3A8A] hover:bg-[#162E70] text-white font-semibold px-5 text-xs border border-[#162E70] cursor-pointer shadow-xs active:translate-y-[1px]"
                >
                  {t("cta.register")}
                </Button>
              </a>
            </div>
          </div>

          {/* Legal and Compliance Strip */}
          <div className="mt-8 pt-4 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-400">
            <p>{t("cta.copyright")}</p>
            <div className="flex items-center gap-4 text-slate-400">
              <a href="/discover" className="hover:text-slate-200 transition-colors">{t("cta.privacy")}</a>
              <span>•</span>
              <a href="/discover" className="hover:text-slate-200 transition-colors">{t("cta.terms")}</a>
              <span>•</span>
              <a href="/discover" className="hover:text-slate-200 transition-colors">{t("cta.dataGov")}</a>
              <span>•</span>
              <a href="/#help" className="hover:text-slate-200 transition-colors">{t("cta.helpdesk")}</a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
