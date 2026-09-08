"use client";

import React, { useEffect, useState, useCallback, useMemo } from "react";
import {
  Compass,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  BarChart3,
  FileCheck2,
  Sparkles,
  UserCheck,
  GraduationCap,
  ClipboardCheck,
  Award,
  BookOpen,
  HelpCircle,
  FileText,
  MessageSquare,
  Download,
  PhoneCall,
  Mail,
  CheckCircle2,
  Clock,
  Building2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";
import { useRouter } from "next/navigation";

export default function EntryLandingPage() {
  const { user } = useAuth();
  const router = useRouter();
  const { t, language } = useI18n();

  // Carousel slides with dynamic translation
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

  // Carousel state
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    // If user is already logged in, redirect directly to dashboard home
    if (user) {
      router.push("/home");
    }
  }, [user, router]);

  // Handle initial scroll if URL has a hash target
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

  // Automatic slide rotation (5s interval)
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
    <div className="flex flex-col bg-[#F8FAFC] w-full text-slate-900">
      {/* 1. Hero & Statistics Section */}
      <section
        id="hero"
        className="scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)] flex flex-col justify-center bg-white border-b border-slate-200 py-8 sm:py-12"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          {/* Two-Column Hero Grid: Left Content (7 cols) and Right Carousel (5 cols) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
            {/* Left Column */}
            <div className="lg:col-span-7 flex flex-col justify-start text-left">
              {/* Portal Title - Fully localized */}
              <h1 className="text-3xl sm:text-4xl lg:text-[40px] font-bold tracking-tight text-slate-900 leading-tight">
                {t("hero.title")}
              </h1>

              {/* Subtitle */}
              <p className="mt-4 text-base sm:text-lg text-slate-600 font-normal leading-relaxed max-w-xl">
                {t("hero.subtitle")}
              </p>

              {/* Primary Actions */}
              <div className="mt-8 flex flex-wrap items-center gap-3.5">
                <a href="/login">
                  <Button
                    size="lg"
                    className="h-11 px-6 rounded-lg bg-[#1E3A8A] hover:bg-[#172554] text-white font-medium text-sm shadow-xs transition-colors flex items-center gap-2 cursor-pointer border border-[#1E3A8A]"
                  >
                    {t("hero.signIn")} <ArrowRight className="h-4 w-4" />
                  </Button>
                </a>
                <a href="/discover">
                  <Button
                    size="lg"
                    variant="outline"
                    className="h-11 px-6 rounded-lg border-slate-300 text-slate-700 hover:bg-slate-50 hover:border-slate-400 font-medium text-sm transition-colors flex items-center gap-2 bg-white cursor-pointer"
                  >
                    <Compass className="h-4 w-4 text-[#1E3A8A]" /> {t("hero.explore")}
                  </Button>
                </a>
              </div>

              {/* Institutional Notes */}
              <div className="mt-8 pt-4 border-t border-slate-100 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-slate-500">
                <span className="flex items-center gap-1.5 font-medium text-slate-600">
                  <CheckCircle2 className="h-3.5 w-3.5 text-slate-500" /> {t("hero.badgeMospi")}
                </span>
                <span className="flex items-center gap-1.5 font-medium text-slate-600">
                  <CheckCircle2 className="h-3.5 w-3.5 text-slate-500" /> {t("hero.badgeCbc")}
                </span>
                <span className="flex items-center gap-1.5 font-medium text-slate-600">
                  <CheckCircle2 className="h-3.5 w-3.5 text-slate-500" /> {t("hero.badgeIso")}
                </span>
              </div>
            </div>

            {/* Right Column: Clean Framed Hero Image Carousel */}
            <div className="lg:col-span-5 w-full flex flex-col items-end">
              <div className="w-full">
                {/* Standard Framed Container */}
                <div
                  className="relative w-full h-[220px] sm:h-[240px] bg-white rounded-xl border border-slate-200 shadow-xs p-2 overflow-hidden group"
                  onMouseEnter={() => setIsPaused(true)}
                  onMouseLeave={() => setIsPaused(false)}
                >
                  {heroSlides.map((slide, idx) => (
                    <div
                      key={slide.src}
                      className={`absolute inset-0 p-2 flex items-center justify-center transition-opacity duration-500 ease-in-out ${
                        idx === currentSlide ? "opacity-100 z-10" : "opacity-0 z-0 pointer-events-none"
                      }`}
                    >
                      <img
                        src={slide.src}
                        alt={slide.alt}
                        className="w-full h-full object-contain block select-none rounded"
                        loading={idx === 0 ? "eager" : "lazy"}
                      />
                    </div>
                  ))}

                  {/* Clean Previous/Next Buttons */}
                  <button
                    type="button"
                    onClick={handlePrev}
                    aria-label="Previous slide"
                    className="absolute left-2 top-1/2 -translate-y-1/2 z-20 h-7 w-7 rounded-full bg-white/95 hover:bg-white text-slate-700 hover:text-[#1E3A8A] flex items-center justify-center shadow-xs border border-slate-200 transition-opacity opacity-0 group-hover:opacity-100 cursor-pointer"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  <button
                    type="button"
                    onClick={handleNext}
                    aria-label="Next slide"
                    className="absolute right-2 top-1/2 -translate-y-1/2 z-20 h-7 w-7 rounded-full bg-white/95 hover:bg-white text-slate-700 hover:text-[#1E3A8A] flex items-center justify-center shadow-xs border border-slate-200 transition-opacity opacity-0 group-hover:opacity-100 cursor-pointer"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>

                {/* Minimal Slide Controls */}
                <div className="mt-2.5 flex items-center justify-between px-1">
                  <span className="text-xs text-slate-500 truncate max-w-[220px]">
                    {heroSlides[currentSlide]?.title}
                  </span>

                  <div className="flex items-center gap-1.5">
                    {heroSlides.map((_, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setCurrentSlide(idx)}
                        aria-label={`Slide ${idx + 1}`}
                        className={`transition-all duration-200 rounded-full cursor-pointer ${
                          idx === currentSlide
                            ? "w-4 h-1.5 bg-[#1E3A8A]"
                            : "w-1.5 h-1.5 bg-slate-300 hover:bg-slate-400"
                        }`}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Statistics Bar - Fully Localized */}
          <div className="mt-10 sm:mt-12 pt-6 sm:pt-8 border-t border-slate-200">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-0 md:divide-x md:divide-slate-200">
              <div className="text-left md:pr-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1E3A8A]">{t("stats.trainedCount")}</p>
                <p className="text-xs sm:text-sm font-semibold text-slate-900 mt-0.5">{t("stats.trainedLabel")}</p>
                <p className="text-xs text-slate-500 mt-0.5">{t("stats.trainedSub")}</p>
              </div>

              <div className="text-left md:px-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1E3A8A]">{t("stats.modulesCount")}</p>
                <p className="text-xs sm:text-sm font-semibold text-slate-900 mt-0.5">{t("stats.modulesLabel")}</p>
                <p className="text-xs text-slate-500 mt-0.5">{t("stats.modulesSub")}</p>
              </div>

              <div className="text-left md:px-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1E3A8A]">{t("stats.qualityCount")}</p>
                <p className="text-xs sm:text-sm font-semibold text-slate-900 mt-0.5">{t("stats.qualityLabel")}</p>
                <p className="text-xs text-slate-500 mt-0.5">{t("stats.qualitySub")}</p>
              </div>

              <div className="text-left md:pl-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1E3A8A]">{t("stats.certCount")}</p>
                <p className="text-xs sm:text-sm font-semibold text-slate-900 mt-0.5">{t("stats.certLabel")}</p>
                <p className="text-xs text-slate-500 mt-0.5">{t("stats.certSub")}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. About Section: Grounded Institutional Framework */}
      <section
        id="about"
        className="scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)] flex flex-col justify-center bg-slate-50/60 border-b border-slate-200 py-8 sm:py-12"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
            {/* Left: Clean Institutional Overview Card */}
            <div className="lg:col-span-5">
              <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-xs">
                <div className="flex items-center gap-3 border-b border-slate-100 pb-4 mb-4">
                  <div className="h-9 w-9 rounded-lg bg-blue-50 text-[#1E3A8A] flex items-center justify-center">
                    <Building2 className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">{t("about.cardOrg")}</h3>
                    <p className="text-xs text-slate-500">{t("about.cardSub")}</p>
                  </div>
                </div>

                <div className="space-y-3 text-xs text-slate-600">
                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <span className="font-semibold text-slate-800 block text-xs">{t("about.item1Title")}</span>
                    <span className="text-slate-500 mt-0.5 block">{t("about.item1Desc")}</span>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <span className="font-semibold text-slate-800 block text-xs">{t("about.item2Title")}</span>
                    <span className="text-slate-500 mt-0.5 block">{t("about.item2Desc")}</span>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <span className="font-semibold text-slate-800 block text-xs">{t("about.item3Title")}</span>
                    <span className="text-slate-500 mt-0.5 block">{t("about.item3Desc")}</span>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>MoSPI • CSO • NSSO • NSSTA</span>
                  <span className="font-medium text-slate-700">{t("hero.badgeIso")}</span>
                </div>
              </div>
            </div>

            {/* Right: Pillars Description */}
            <div className="lg:col-span-7">
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 tracking-tight leading-tight">
                {t("about.title")}
              </h2>
              <p className="mt-3 text-slate-600 text-sm sm:text-base leading-relaxed font-normal">
                {t("about.desc")}
              </p>

              <div className="mt-6 space-y-4">
                <div className="flex items-start gap-3.5 p-3 rounded-lg border border-slate-200/80 bg-white">
                  <div className="h-9 w-9 rounded-lg bg-blue-50 text-[#1E3A8A] flex items-center justify-center shrink-0 mt-0.5">
                    <BarChart3 className="h-4.5 w-4.5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900">{t("about.pillar1Title")}</h3>
                    <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">
                      {t("about.pillar1Desc")}
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5 p-3 rounded-lg border border-slate-200/80 bg-white">
                  <div className="h-9 w-9 rounded-lg bg-amber-50 text-[#CA8A04] flex items-center justify-center shrink-0 mt-0.5">
                    <FileCheck2 className="h-4.5 w-4.5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900">{t("about.pillar2Title")}</h3>
                    <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">
                      {t("about.pillar2Desc")}
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5 p-3 rounded-lg border border-slate-200/80 bg-white">
                  <div className="h-9 w-9 rounded-lg bg-blue-50 text-[#1E3A8A] flex items-center justify-center shrink-0 mt-0.5">
                    <Sparkles className="h-4.5 w-4.5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900">{t("about.pillar3Title")}</h3>
                    <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">
                      {t("about.pillar3Desc")}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. How It Works Section: Clean 4-Step Progression */}
      <section
        id="how-it-works"
        className="scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)] flex flex-col justify-center bg-white border-b border-slate-200 py-8 sm:py-12"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="text-center max-w-2xl mx-auto mb-8">
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {t("howItWorks.title")}
            </h2>
            <p className="mt-2 text-slate-600 text-xs sm:text-sm">
              {t("howItWorks.subtitle")}
            </p>
          </div>

          {/* 4 Clean Steps Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 sm:gap-6">
            {/* Step 1 */}
            <div className="p-4 sm:p-5 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="h-7 w-7 rounded-full bg-[#1E3A8A] text-white font-bold text-xs flex items-center justify-center">
                    1
                  </span>
                  <UserCheck className="h-4 w-4 text-slate-500" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">{t("howItWorks.step1Title")}</h3>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                  {t("howItWorks.step1Desc")}
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="p-4 sm:p-5 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="h-7 w-7 rounded-full bg-[#1E3A8A] text-white font-bold text-xs flex items-center justify-center">
                    2
                  </span>
                  <GraduationCap className="h-4 w-4 text-slate-500" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">{t("howItWorks.step2Title")}</h3>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                  {t("howItWorks.step2Desc")}
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="p-4 sm:p-5 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="h-7 w-7 rounded-full bg-[#1E3A8A] text-white font-bold text-xs flex items-center justify-center">
                    3
                  </span>
                  <ClipboardCheck className="h-4 w-4 text-slate-500" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">{t("howItWorks.step3Title")}</h3>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                  {t("howItWorks.step3Desc")}
                </p>
              </div>
            </div>

            {/* Step 4 */}
            <div className="p-4 sm:p-5 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="h-7 w-7 rounded-full bg-[#CA8A04] text-white font-bold text-xs flex items-center justify-center">
                    4
                  </span>
                  <Award className="h-4 w-4 text-[#CA8A04]" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">{t("howItWorks.step4Title")}</h3>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                  {t("howItWorks.step4Desc")}
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Resources Section: Cadre Library */}
      <section
        id="resources"
        className="scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)] flex flex-col justify-center bg-slate-50/60 border-b border-slate-200 py-8 sm:py-12"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-7">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                {t("resources.title")}
              </h2>
              <p className="mt-1.5 text-slate-600 text-xs sm:text-sm max-w-2xl">
                {t("resources.subtitle")}
              </p>
            </div>
            <a href="/discover" className="mt-3 md:mt-0">
              <Button
                variant="outline"
                size="sm"
                className="border-slate-300 text-slate-700 hover:text-[#1E3A8A] hover:bg-white rounded-lg text-xs font-medium cursor-pointer"
              >
                {t("resources.browseCatalog")} <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
              </Button>
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
            {/* Resource Card 1 */}
            <div className="bg-white rounded-xl p-4 sm:p-5 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    {t("resources.doc1Tag")}
                  </span>
                  <FileText className="h-4 w-4 text-slate-400" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">
                  {t("resources.doc1Title")}
                </h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {t("resources.doc1Desc")}
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span className="font-mono text-[11px]">PDF • 4.2 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#1E3A8A] hover:underline flex items-center gap-1"
                >
                  <Download className="h-3 w-3" /> {t("resources.access")}
                </a>
              </div>
            </div>

            {/* Resource Card 2 */}
            <div className="bg-white rounded-xl p-4 sm:p-5 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    {t("resources.doc2Tag")}
                  </span>
                  <FileText className="h-4 w-4 text-slate-400" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">
                  {t("resources.doc2Title")}
                </h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {t("resources.doc2Desc")}
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span className="font-mono text-[11px]">PDF • 3.8 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#1E3A8A] hover:underline flex items-center gap-1"
                >
                  <Download className="h-3 w-3" /> {t("resources.access")}
                </a>
              </div>
            </div>

            {/* Resource Card 3 */}
            <div className="bg-white rounded-xl p-4 sm:p-5 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    {t("resources.doc3Tag")}
                  </span>
                  <FileText className="h-4 w-4 text-slate-400" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">
                  {t("resources.doc3Title")}
                </h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {t("resources.doc3Desc")}
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span className="font-mono text-[11px]">PDF • 2.6 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#1E3A8A] hover:underline flex items-center gap-1"
                >
                  <Download className="h-3 w-3" /> {t("resources.access")}
                </a>
              </div>
            </div>

            {/* Resource Card 4 */}
            <div className="bg-white rounded-xl p-4 sm:p-5 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    {t("resources.doc4Tag")}
                  </span>
                  <FileText className="h-4 w-4 text-slate-400" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">
                  {t("resources.doc4Title")}
                </h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {t("resources.doc4Desc")}
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span className="font-mono text-[11px]">PDF • 5.1 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#1E3A8A] hover:underline flex items-center gap-1"
                >
                  <Download className="h-3 w-3" /> {t("resources.access")}
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Help & Support Section */}
      <section
        id="help"
        className="scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)] flex flex-col justify-between bg-white pt-8 pb-0"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex-1 flex flex-col justify-center py-4">
          <div className="text-center max-w-2xl mx-auto mb-7">
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {t("help.title")}
            </h2>
            <p className="mt-1.5 text-slate-600 text-xs sm:text-sm">
              {t("help.subtitle")}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Help Card 1: AI Copilot */}
            <div className="bg-slate-50/50 rounded-xl p-5 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="h-8 w-8 rounded-lg bg-blue-50 text-[#1E3A8A] flex items-center justify-center mb-3">
                  <Sparkles className="h-4 w-4" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">{t("help.aiTitle")}</h3>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                  {t("help.aiDesc")}
                </p>
              </div>
              <div className="mt-5 pt-3 border-t border-slate-200/70">
                <a href="/login" className="inline-flex items-center text-xs font-semibold text-[#1E3A8A] hover:underline">
                  <MessageSquare className="mr-1.5 h-3.5 w-3.5" /> {t("help.aiLaunch")} <ArrowRight className="ml-1 h-3 w-3" />
                </a>
              </div>
            </div>

            {/* Help Card 2: Training Desk */}
            <div className="bg-slate-50/50 rounded-xl p-5 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="h-8 w-8 rounded-lg bg-blue-50 text-[#1E3A8A] flex items-center justify-center mb-3">
                  <PhoneCall className="h-4 w-4" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">{t("help.deskTitle")}</h3>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                  {t("help.deskDesc")}
                </p>
                <div className="mt-3 space-y-1 text-xs text-slate-700">
                  <p className="flex items-center gap-2">
                    <Mail className="h-3.5 w-3.5 text-slate-500" /> support-karmayogi@gov.in
                  </p>
                  <p className="flex items-center gap-2">
                    <PhoneCall className="h-3.5 w-3.5 text-slate-500" /> 1800-11-KARM
                  </p>
                </div>
              </div>
              <div className="mt-5 pt-3 border-t border-slate-200/70 flex items-center text-xs text-slate-500">
                <span className="flex items-center gap-1.5">
                  <Clock className="h-3.5 w-3.5 text-slate-400" /> {t("help.hours")}
                </span>
              </div>
            </div>

            {/* Help Card 3: FAQs */}
            <div className="bg-slate-50/50 rounded-xl p-5 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="h-8 w-8 rounded-lg bg-blue-50 text-[#1E3A8A] flex items-center justify-center mb-3">
                  <HelpCircle className="h-4 w-4" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">{t("help.faqTitle")}</h3>
                <div className="mt-2.5 space-y-2 text-xs">
                  <div>
                    <p className="font-medium text-slate-800">{t("help.faq1Q")}</p>
                    <p className="text-slate-500 mt-0.5">{t("help.faq1A")}</p>
                  </div>
                  <div>
                    <p className="font-medium text-slate-800">{t("help.faq2Q")}</p>
                    <p className="text-slate-500 mt-0.5">{t("help.faq2A")}</p>
                  </div>
                </div>
              </div>
              <div className="mt-5 pt-3 border-t border-slate-200/70">
                <a href="/login" className="inline-flex items-center text-xs font-semibold text-[#1E3A8A] hover:underline">
                  {t("help.knowledgeBase")} <ArrowRight className="ml-1 h-3 w-3" />
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Integrated Closing Banner in Dignified Solid Deep Navy */}
        <div className="bg-[#0F172A] text-white py-6 border-t border-slate-800 w-full mt-auto">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
              <div>
                <h3 className="text-base sm:text-lg font-semibold text-white">
                  {t("cta.readyTitle")}
                </h3>
                <p className="text-xs text-slate-400 mt-0.5 max-w-xl">
                  {t("cta.readyDesc")}
                </p>
              </div>
              <div className="flex flex-wrap items-center justify-center gap-3 shrink-0">
                <a href="/login">
                  <Button
                    variant="outline"
                    size="sm"
                    className="rounded-lg text-white border-slate-600 hover:bg-slate-800 hover:text-white px-4 py-2 text-xs font-medium cursor-pointer"
                  >
                    {t("hero.signIn")}
                  </Button>
                </a>
                <a href="/register">
                  <Button
                    size="sm"
                    className="rounded-lg bg-[#EAB308] hover:bg-[#CA8A04] text-slate-950 font-semibold px-4 py-2 text-xs cursor-pointer border border-[#EAB308] transition-colors"
                  >
                    {t("cta.register")}
                  </Button>
                </a>
              </div>
            </div>

            {/* Legal Strip */}
            <div className="mt-5 pt-4 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-2 text-[11px] text-slate-400 text-center sm:text-left">
              <p>{t("cta.copyright")}</p>
              <div className="flex items-center justify-center gap-4 text-slate-400">
                <a href="/discover" className="hover:text-white transition-colors">{t("cta.privacy")}</a>
                <span>•</span>
                <a href="/discover" className="hover:text-white transition-colors">{t("cta.terms")}</a>
                <span>•</span>
                <a href="/discover" className="hover:text-white transition-colors">{t("cta.dataGov")}</a>
                <span>•</span>
                <a href="/#help" className="hover:text-white transition-colors">{t("cta.helpdesk")}</a>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
