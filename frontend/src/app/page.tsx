"use client";

import React, { useEffect, useState, useCallback } from "react";
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
  ShieldCheck,
  FileText,
  MessageSquare,
  Download,
  PhoneCall,
  Mail,
  CheckCircle2,
  TrendingUp,
  Layers,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth/AuthContext";
import { useRouter } from "next/navigation";

// Extensible hero carousel slides from public directory with their natural aspect ratios
const HERO_SLIDES = [
  {
    src: "/karmayogi.jpg",
    alt: "Mission Karmayogi civil service capacity building session",
    aspectRatio: "657 / 301",
  },
  {
    src: "/government-meeting.jpg",
    alt: "Government administrative cadre review and collaborative meeting",
    aspectRatio: "673 / 290",
  },
  {
    src: "/ai-daksh.jpg",
    alt: "AI-Daksh civil service intelligence and analytical tools",
    aspectRatio: "716 / 395",
  },
];

export default function EntryLandingPage() {
  const { user } = useAuth();
  const router = useRouter();

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
          const headerHeight = header ? Math.round(header.getBoundingClientRect().height) : 120;
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
      setCurrentSlide((prev) => (prev + 1) % HERO_SLIDES.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [isPaused]);

  const handlePrev = useCallback(() => {
    setCurrentSlide((prev) => (prev - 1 + HERO_SLIDES.length) % HERO_SLIDES.length);
  }, []);

  const handleNext = useCallback(() => {
    setCurrentSlide((prev) => (prev + 1) % HERO_SLIDES.length);
  }, []);

  return (
    <div className="flex flex-col bg-[#F8FAFC] w-full">
      {/* 1. Hero & Statistics Section: Sized to full viewport height minus navbar */}
      <section
        id="hero"
        className="scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center bg-gradient-to-b from-white via-[#F8FAFC] to-[#F1F5F9] text-[#0F172A] py-8 sm:py-10 lg:py-12 border-b border-slate-200"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          {/* Two-Column Hero Grid: Left Content (7 cols) and Right Carousel (5 cols), Top-Aligned */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 xl:gap-12 items-center">
            {/* Left Column: Top-Aligned */}
            <div className="lg:col-span-7 xl:col-span-7 flex flex-col justify-start text-left">
              {/* Official Portal Title */}
              <h1 className="text-3xl sm:text-4xl lg:text-[36px] font-extrabold tracking-tight text-slate-900 leading-tight">
                National Learning Platform for Civil Services
              </h1>

              {/* Clear subtitle directly underneath */}
              <p className="mt-4 text-base sm:text-lg text-slate-600 font-normal leading-relaxed max-w-xl">
                Standardized competency frameworks, accredited modules, and verified certifications for India&apos;s public administrators.
              </p>

              {/* Action buttons in official Karmayogi styling */}
              <div className="mt-8 flex flex-wrap items-center gap-4">
                <a href="/login">
                  <Button
                    size="lg"
                    className="h-11 px-7 rounded-lg bg-[#1E3A8A] hover:bg-[#1D3557] text-white font-semibold text-sm shadow-sm transition-all flex items-center gap-2 border border-[#1E3A8A] cursor-pointer"
                  >
                    Official Sign In <ArrowRight className="h-4 w-4" />
                  </Button>
                </a>
                <a href="/discover">
                  <Button
                    size="lg"
                    variant="outline"
                    className="h-11 px-7 rounded-lg border-slate-300 text-slate-700 hover:bg-slate-50 hover:border-slate-400 hover:text-[#1E3A8A] font-semibold text-sm transition-all flex items-center gap-2 bg-white cursor-pointer"
                  >
                    <Compass className="h-4 w-4 text-[#1E3A8A]" /> Explore Courses
                  </Button>
                </a>
              </div>
            </div>

            {/* Right Column: Hero Image Carousel (~35-40% width) */}
            <div className="lg:col-span-5 xl:col-span-5 w-full flex flex-col items-end">
              <div className="w-full">
                {/* Clean White Frame */}
                <div
                  className="relative w-full h-[200px] sm:h-[225px] bg-white rounded-xl border border-slate-200 shadow-sm p-2 sm:p-2.5 overflow-hidden group"
                  onMouseEnter={() => setIsPaused(true)}
                  onMouseLeave={() => setIsPaused(false)}
                >
                  {HERO_SLIDES.map((slide, idx) => (
                    <div
                      key={slide.src}
                      className={`absolute inset-0 p-2 flex items-center justify-center transition-opacity duration-700 ease-in-out ${
                        idx === currentSlide ? "opacity-100 z-10" : "opacity-0 z-0 pointer-events-none"
                      }`}
                    >
                      <img
                        src={slide.src}
                        alt={slide.alt}
                        className="w-full h-full object-contain block select-none"
                        loading={idx === 0 ? "eager" : "lazy"}
                      />
                    </div>
                  ))}

                  {/* Subtle previous/next hover buttons on frame */}
                  <button
                    type="button"
                    onClick={handlePrev}
                    aria-label="Previous slide"
                    className="absolute left-1.5 top-1/2 -translate-y-1/2 z-20 h-6 w-6 rounded-full bg-white/95 hover:bg-white text-slate-600 hover:text-[#1E3A8A] flex items-center justify-center shadow-xs border border-slate-200 transition-opacity opacity-0 group-hover:opacity-100 cursor-pointer"
                  >
                    <ChevronLeft className="h-3.5 w-3.5" />
                  </button>
                  <button
                    type="button"
                    onClick={handleNext}
                    aria-label="Next slide"
                    className="absolute right-1.5 top-1/2 -translate-y-1/2 z-20 h-6 w-6 rounded-full bg-white/95 hover:bg-white text-slate-600 hover:text-[#1E3A8A] flex items-center justify-center shadow-xs border border-slate-200 transition-opacity opacity-0 group-hover:opacity-100 cursor-pointer"
                  >
                    <ChevronRight className="h-3.5 w-3.5" />
                  </button>
                </div>

                {/* Small pagination indicators & controls */}
                <div className="mt-2.5 flex items-center justify-center gap-1.5">
                  <button
                    type="button"
                    onClick={handlePrev}
                    aria-label="Previous slide"
                    className="h-5 w-5 rounded-full bg-white hover:bg-slate-100 text-slate-600 hover:text-[#1E3A8A] flex items-center justify-center border border-slate-200 shadow-2xs transition-colors cursor-pointer"
                  >
                    <ChevronLeft className="h-3 w-3" />
                  </button>

                  <div className="flex items-center gap-1.5 px-2.5 py-1 bg-white rounded-full border border-slate-200 shadow-2xs">
                    {HERO_SLIDES.map((_, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setCurrentSlide(idx)}
                        aria-label={`Slide ${idx + 1}`}
                        className={`transition-all duration-300 rounded-full cursor-pointer ${
                          idx === currentSlide
                            ? "w-4 h-1.5 bg-[#1E3A8A]"
                            : "w-1.5 h-1.5 bg-slate-300 hover:bg-slate-400"
                        }`}
                      />
                    ))}
                  </div>

                  <button
                    type="button"
                    onClick={handleNext}
                    aria-label="Next slide"
                    className="h-5 w-5 rounded-full bg-white hover:bg-slate-100 text-slate-600 hover:text-[#1E3A8A] flex items-center justify-center border border-slate-200 shadow-2xs transition-colors cursor-pointer"
                  >
                    <ChevronRight className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Statistics Bar: In the EXACT same container, visually aligned with hero content left and right edges */}
          <div className="mt-12 sm:mt-14 pt-7 sm:pt-8 border-t border-slate-200">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-0 md:divide-x md:divide-slate-200">
              {/* Item 1: Aligns directly with the left edge of the hero content */}
              <div className="text-left md:pr-6">
                <p className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#1E3A8A]">40,000+</p>
                <p className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Civil Servants Trained</p>
              </div>

              {/* Item 2 */}
              <div className="text-left md:px-6">
                <p className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#1E3A8A]">100%</p>
                <p className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Accredited Curriculum</p>
              </div>

              {/* Item 3 */}
              <div className="text-left md:px-6">
                <p className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#1E3A8A]">UN-NQAF</p>
                <p className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Quality Frameworks</p>
              </div>

              {/* Item 4: Left-aligned within column matching items 1-3 */}
              <div className="text-left md:pl-6">
                <p className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#1E3A8A]">Verifiable</p>
                <p className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Government Credentials</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. About Section: Sized to full viewport height minus navbar */}
      <section
        id="about"
        className="scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center bg-white border-b border-[#C8A8A9]/30 py-8 sm:py-12"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
            {/* LEFT: Institutional Visual Card styled with Rose and Charcoal Palette */}
            <div className="lg:col-span-5">
              <div className="bg-[#241E20] rounded-2xl p-6 text-white border border-[#965C66]/30 shadow-lg relative overflow-hidden">
                {/* Visual header */}
                <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-4">
                  <div className="flex items-center gap-2.5">
                    <div className="h-9 w-9 rounded-lg bg-[#965C66]/25 border border-[#C8A8A9]/40 flex items-center justify-center text-[#C8A8A9]">
                      <Award className="h-5 w-5" />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-white leading-none">NPCSCB Framework</p>
                      <p className="text-[10px] text-[#C8A8A9]/80 mt-0.5">Capacity Building Commission</p>
                    </div>
                  </div>
                  <span className="text-[10px] uppercase font-semibold tracking-wider text-white bg-[#965C66] px-2.5 py-0.5 rounded-full border border-[#C8A8A9]/30">
                    Verified
                  </span>
                </div>

                {/* Structured Competency Matrix */}
                <div className="space-y-3">
                  <div className="bg-white/5 rounded-xl p-3 border border-white/10">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-white font-medium flex items-center gap-2">
                        <BarChart3 className="h-4 w-4 text-[#C8A8A9]" />
                        Official Statistical Cadre
                      </span>
                      <span className="text-[11px] text-[#C8A8A9] font-mono">NSS • CPI • NAS</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-[#965C66] h-full rounded-full w-[88%]" />
                    </div>
                  </div>

                  <div className="bg-white/5 rounded-xl p-3 border border-white/10">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-white font-medium flex items-center gap-2">
                        <FileCheck2 className="h-4 w-4 text-[#C8A8A9]" />
                        Accredited Assessments
                      </span>
                      <span className="text-[11px] text-[#C8A8A9] font-mono">70% Threshold</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-[#BC9798] h-full rounded-full w-[94%]" />
                    </div>
                  </div>

                  <div className="bg-white/5 rounded-xl p-3 border border-white/10">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-white font-medium flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-[#C8A8A9]" />
                        Civil Service AI Copilot
                      </span>
                      <span className="text-[11px] text-[#C8A8A9] font-mono">24/7 Active</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-[#965C66] h-full rounded-full w-[100%]" />
                    </div>
                  </div>
                </div>

                {/* Institutional Footer note */}
                <div className="mt-5 pt-3.5 border-t border-white/10 flex items-center justify-between text-[11px] text-[#C8A8A9]/80">
                  <span>MoSPI • CSO • NSSO • NSSTA</span>
                  <span className="text-[#C8A8A9] font-medium flex items-center gap-1.5">
                    <ShieldCheck className="h-4 w-4" /> ISO/IEC Aligned
                  </span>
                </div>
              </div>
            </div>

            {/* RIGHT: Section Title and Descriptive Core Pillars */}
            <div className="lg:col-span-7">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#965C66]/10 text-[#965C66] text-xs font-semibold mb-2.5 border border-[#965C66]/20">
                <Layers className="h-3.5 w-3.5" />
                Core Institutional Pillars
              </div>
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#241E20] tracking-tight leading-tight">
                A Competency-Driven Learning Paradigm
              </h2>
              <p className="mt-2.5 text-[#5A5052] text-sm sm:text-base leading-relaxed font-normal">
                Transitioning India&apos;s civil service from traditional procedural rules to dynamic, roles-based competency mastery—aligned with the National Programme for Civil Services Capacity Building (NPCSCB).
              </p>

              {/* Three Core Pillars Content */}
              <div className="mt-5 space-y-3.5">
                <div className="flex items-start gap-3.5 p-2.5 rounded-xl hover:bg-[#FAF8F8] transition-colors border border-transparent hover:border-[#C8A8A9]/20">
                  <div className="h-9 w-9 rounded-lg bg-[#965C66]/10 text-[#965C66] border border-[#965C66]/20 flex items-center justify-center shrink-0 mt-0.5">
                    <BarChart3 className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-[#241E20]">Statistical Integrity &amp; Methodologies</h3>
                    <p className="text-xs sm:text-sm text-[#5A5052] mt-0.5 leading-normal">
                      Rigorous curricula on National Sample Surveys (NSS), Consumer Price Index (CPI), IIP, and National Accounts compilation standards.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5 p-2.5 rounded-xl hover:bg-[#FAF8F8] transition-colors border border-transparent hover:border-[#C8A8A9]/20">
                  <div className="h-9 w-9 rounded-lg bg-[#965C66]/10 text-[#965C66] border border-[#965C66]/20 flex items-center justify-center shrink-0 mt-0.5">
                    <FileCheck2 className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-[#241E20]">Certified Standardized Assessments</h3>
                    <p className="text-xs sm:text-sm text-[#5A5052] mt-0.5 leading-normal">
                      Verified evaluations with a rigorous 70% passing threshold, awarding tamper-proof digital credentials to your official civil service record.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5 p-2.5 rounded-xl hover:bg-[#FAF8F8] transition-colors border border-transparent hover:border-[#C8A8A9]/20">
                  <div className="h-9 w-9 rounded-lg bg-[#965C66]/10 text-[#965C66] border border-[#965C66]/20 flex items-center justify-center shrink-0 mt-0.5">
                    <Sparkles className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-[#241E20]">AI-Orchestrated Cadre Assistant</h3>
                    <p className="text-xs sm:text-sm text-[#5A5052] mt-0.5 leading-normal">
                      Built-in civil service intelligence providing immediate guidance on survey methodologies, regulatory circulars, and departmental lookups.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. How It Works Section: Sized to full viewport height minus navbar */}
      <section
        id="how-it-works"
        className="scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center bg-[#FAF8F8] border-b border-[#C8A8A9]/30 py-6 sm:py-8 lg:py-10"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="text-center max-w-3xl mx-auto mb-5 sm:mb-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#965C66]/10 text-[#965C66] text-xs font-semibold mb-2 border border-[#965C66]/20">
              <Compass className="h-3.5 w-3.5" />
              Structured Progression
            </div>
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#241E20] tracking-tight">
              How the Karmayogi Journey Works
            </h2>
            <p className="mt-1.5 text-[#5A5052] text-xs sm:text-sm">
              A structured 4-step progression from cadre onboarding to recognized national civil service certification.
            </p>
          </div>

          {/* Single Horizontal Progression Container */}
          <div className="bg-white rounded-2xl border border-[#C8A8A9]/40 p-4 sm:p-5 lg:p-6 shadow-xs">
            <div className="relative">
              {/* Connected horizontal track line on desktop */}
              <div className="hidden md:block absolute top-4 left-6 right-6 h-0.5 bg-gradient-to-r from-[#965C66] via-[#BC9798] to-[#C8A8A9] z-0" />

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 md:gap-5 relative z-10">
                {/* Step 1 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-2">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    1
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <UserCheck className="h-4 w-4 text-[#965C66] shrink-0" /> Onboard Role
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-0.5 leading-relaxed">
                      Authenticate with official government email and specify your ministry and cadre roles.
                    </p>
                  </div>
                </div>

                {/* Step 2 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-2">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    2
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <GraduationCap className="h-4 w-4 text-[#965C66] shrink-0" /> Discover &amp; Study
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-0.5 leading-relaxed">
                      Study video modules, practical CAPI survey simulations, and field methodology guides.
                    </p>
                  </div>
                </div>

                {/* Step 3 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-2">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    3
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <ClipboardCheck className="h-4 w-4 text-[#965C66] shrink-0" /> Pass Assessment
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-0.5 leading-relaxed">
                      Complete 70% threshold MCQ examinations with automated scoring and explanations.
                    </p>
                  </div>
                </div>

                {/* Step 4 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-2">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    4
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <Award className="h-4 w-4 text-[#965C66] shrink-0" /> Earn Certificate
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-0.5 leading-relaxed">
                      Receive cryptographically verifiable digital credentials linked to your personnel records.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* How Karmayogi Helps Officials */}
          <div className="mt-5 pt-4 border-t border-[#C8A8A9]/30">
            <h3 className="text-sm sm:text-base font-bold text-[#241E20] text-center mb-3">
              How iGOT Karmayogi Helps Public Servants
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
              <div className="bg-white rounded-xl p-3 sm:p-3.5 border border-[#C8A8A9]/40 shadow-xs hover:border-[#965C66]/40 transition-colors">
                <div className="h-7 w-7 rounded-lg bg-[#965C66]/10 text-[#965C66] flex items-center justify-center mb-2">
                  <TrendingUp className="h-3.5 w-3.5" />
                </div>
                <h4 className="font-semibold text-[#241E20] text-xs sm:text-sm">Career Progression &amp; APAR</h4>
                <p className="text-[11px] sm:text-xs text-[#5A5052] mt-0.5 leading-relaxed">
                  Demonstrated competencies and completed courses are recognized during annual appraisal cycles and postings.
                </p>
              </div>

              <div className="bg-white rounded-xl p-3 sm:p-3.5 border border-[#C8A8A9]/40 shadow-xs hover:border-[#965C66]/40 transition-colors">
                <div className="h-7 w-7 rounded-lg bg-[#965C66]/10 text-[#965C66] flex items-center justify-center mb-2">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                </div>
                <h4 className="font-semibold text-[#241E20] text-xs sm:text-sm">Standardized National Training</h4>
                <p className="text-[11px] sm:text-xs text-[#5A5052] mt-0.5 leading-relaxed">
                  Field staff and analysts access unified guidelines eliminating methodological discrepancies across states.
                </p>
              </div>

              <div className="bg-white rounded-xl p-3 sm:p-3.5 border border-[#C8A8A9]/40 shadow-xs hover:border-[#965C66]/40 transition-colors">
                <div className="h-7 w-7 rounded-lg bg-[#965C66]/10 text-[#965C66] flex items-center justify-center mb-2">
                  <Sparkles className="h-3.5 w-3.5" />
                </div>
                <h4 className="font-semibold text-[#241E20] text-xs sm:text-sm">Autonomous On-Demand Learning</h4>
                <p className="text-[11px] sm:text-xs text-[#5A5052] mt-0.5 leading-relaxed">
                  Learn at your own pace from any device with progress persistence, offline briefs, and built-in AI assistance.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Resources Section: Sized to full viewport height minus navbar */}
      <section
        id="resources"
        className="scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center bg-white border-b border-[#C8A8A9]/30 py-8 sm:py-12"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-7 sm:mb-8">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#965C66]/10 text-[#965C66] text-xs font-semibold mb-2 border border-[#965C66]/20">
                <BookOpen className="h-3.5 w-3.5" />
                Knowledge Repositories
              </div>
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#241E20] tracking-tight">
                Cadre Resources &amp; Statistical Library
              </h2>
              <p className="mt-1.5 text-[#5A5052] text-xs sm:text-sm max-w-2xl">
                Official survey manuals, quality frameworks, and technical reference handbooks curated by MoSPI, CSO, and NSSO.
              </p>
            </div>
            <a href="/discover" className="mt-3 md:mt-0">
              <Button
                variant="outline"
                size="sm"
                className="border-[#965C66]/40 text-[#965C66] hover:bg-[#965C66]/10 hover:border-[#965C66] rounded-full text-xs font-medium cursor-pointer"
              >
                Browse Full Catalogue <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
              </Button>
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
            {/* Resource Card 1 */}
            <div className="bg-[#FAF8F8] rounded-xl p-4 sm:p-5 border border-[#C8A8A9]/40 hover:border-[#965C66]/50 flex flex-col justify-between transition-all hover:shadow-xs group">
              <div>
                <div className="flex items-center justify-between mb-2.5">
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[#965C66]/10 text-[#965C66]">
                    NSSO Guide
                  </span>
                  <FileText className="h-4 w-4 text-[#5A5052] group-hover:text-[#965C66] transition-colors" />
                </div>
                <h4 className="font-semibold text-[#241E20] text-sm group-hover:text-[#965C66] transition-colors">
                  Field Enumerator Manual
                </h4>
                <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                  Concepts, household sampling frameworks, and standardized definitions for socio-economic survey rounds.
                </p>
              </div>
              <div className="mt-4 pt-2.5 border-t border-[#C8A8A9]/30 flex items-center justify-between text-xs text-[#5A5052]">
                <span className="font-mono text-[11px]">PDF • 4.2 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#965C66] hover:text-[#824E57] flex items-center gap-1 hover:underline"
                >
                  <Download className="h-3 w-3" /> Access
                </a>
              </div>
            </div>

            {/* Resource Card 2 */}
            <div className="bg-[#FAF8F8] rounded-xl p-4 sm:p-5 border border-[#C8A8A9]/40 hover:border-[#965C66]/50 flex flex-col justify-between transition-all hover:shadow-xs group">
              <div>
                <div className="flex items-center justify-between mb-2.5">
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[#965C66]/10 text-[#965C66]">
                    Price Statistics
                  </span>
                  <FileText className="h-4 w-4 text-[#5A5052] group-hover:text-[#965C66] transition-colors" />
                </div>
                <h4 className="font-semibold text-[#241E20] text-sm group-hover:text-[#965C66] transition-colors">
                  CPI &amp; IIP Technical Manual
                </h4>
                <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                  Retail price collection routines, item basket weighting diagrams, and index compilation methodologies.
                </p>
              </div>
              <div className="mt-4 pt-2.5 border-t border-[#C8A8A9]/30 flex items-center justify-between text-xs text-[#5A5052]">
                <span className="font-mono text-[11px]">PDF • 3.8 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#965C66] hover:text-[#824E57] flex items-center gap-1 hover:underline"
                >
                  <Download className="h-3 w-3" /> Access
                </a>
              </div>
            </div>

            {/* Resource Card 3 */}
            <div className="bg-[#FAF8F8] rounded-xl p-4 sm:p-5 border border-[#C8A8A9]/40 hover:border-[#965C66]/50 flex flex-col justify-between transition-all hover:shadow-xs group">
              <div>
                <div className="flex items-center justify-between mb-2.5">
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[#965C66]/10 text-[#965C66]">
                    Quality Standards
                  </span>
                  <FileText className="h-4 w-4 text-[#5A5052] group-hover:text-[#965C66] transition-colors" />
                </div>
                <h4 className="font-semibold text-[#241E20] text-sm group-hover:text-[#965C66] transition-colors">
                  UN-NQAF Quality Rubrics
                </h4>
                <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                  United Nations National Quality Assurance Framework guidelines adapted for Indian official statistics.
                </p>
              </div>
              <div className="mt-4 pt-2.5 border-t border-[#C8A8A9]/30 flex items-center justify-between text-xs text-[#5A5052]">
                <span className="font-mono text-[11px]">PDF • 2.6 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#965C66] hover:text-[#824E57] flex items-center gap-1 hover:underline"
                >
                  <Download className="h-3 w-3" /> Access
                </a>
              </div>
            </div>

            {/* Resource Card 4 */}
            <div className="bg-[#FAF8F8] rounded-xl p-4 sm:p-5 border border-[#C8A8A9]/40 hover:border-[#965C66]/50 flex flex-col justify-between transition-all hover:shadow-xs group">
              <div>
                <div className="flex items-center justify-between mb-2.5">
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[#965C66]/10 text-[#965C66]">
                    Survey Tech
                  </span>
                  <FileText className="h-4 w-4 text-[#5A5052] group-hover:text-[#965C66] transition-colors" />
                </div>
                <h4 className="font-semibold text-[#241E20] text-sm group-hover:text-[#965C66] transition-colors">
                  CAPI Operations Manual
                </h4>
                <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                  Tablet-based interview setup, encrypted geo-tag synchronization, and automated logic validation procedures.
                </p>
              </div>
              <div className="mt-4 pt-2.5 border-t border-[#C8A8A9]/30 flex items-center justify-between text-xs text-[#5A5052]">
                <span className="font-mono text-[11px]">PDF • 5.1 MB</span>
                <a
                  href="/discover"
                  className="font-medium text-[#965C66] hover:text-[#824E57] flex items-center gap-1 hover:underline"
                >
                  <Download className="h-3 w-3" /> Access
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Help & Support Section: Sized to full viewport height minus navbar with integrated CTA and Institutional Ribbon */}
      <section
        id="help"
        className="scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-between bg-[#FAF8F8] pt-6 sm:pt-8 pb-0"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex-1 flex flex-col justify-center py-2 sm:py-3">
          <div className="text-center max-w-3xl mx-auto mb-5 sm:mb-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#965C66]/10 text-[#965C66] text-xs font-semibold mb-2 border border-[#965C66]/20">
              <HelpCircle className="h-3.5 w-3.5" />
              Assistance &amp; Support
            </div>
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#241E20] tracking-tight">
              Help &amp; Official Training Support
            </h2>
            <p className="mt-1 text-[#5A5052] text-xs sm:text-sm">
              Dedicated institutional support channels for central civil servants, state statisticians, and ministry nodal officers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-5">
            {/* Help Card 1: AI Copilot */}
            <div className="bg-white rounded-2xl p-4 sm:p-5 border border-[#C8A8A9]/40 shadow-xs flex flex-col justify-between">
              <div>
                <div className="h-8 w-8 rounded-xl bg-[#965C66]/10 text-[#965C66] flex items-center justify-center mb-2.5">
                  <Sparkles className="h-4 w-4" />
                </div>
                <h4 className="font-bold text-[#241E20] text-sm sm:text-base">24/7 Civil Service AI Copilot</h4>
                <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                  Have an urgent question on survey sampling or course rules? The AI copilot provides instant, cited answers from official training manuals.
                </p>
              </div>
              <div className="mt-3.5 pt-2.5 border-t border-[#C8A8A9]/30">
                <a href="/login" className="inline-flex items-center text-xs font-semibold text-[#965C66] hover:text-[#824E57]">
                  <MessageSquare className="mr-1.5 h-3.5 w-3.5" /> Launch AI Assistant <ArrowRight className="ml-1 h-3 w-3" />
                </a>
              </div>
            </div>

            {/* Help Card 2: Nodal Officers & Support Desk */}
            <div className="bg-white rounded-2xl p-4 sm:p-5 border border-[#C8A8A9]/40 shadow-xs flex flex-col justify-between">
              <div>
                <div className="h-8 w-8 rounded-xl bg-[#965C66]/10 text-[#965C66] flex items-center justify-center mb-2.5">
                  <PhoneCall className="h-4 w-4" />
                </div>
                <h4 className="font-bold text-[#241E20] text-sm sm:text-base">Ministry Training Desk</h4>
                <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                  For cadre verification, department approvals, or official nomination queries, reach out to the Central Training Division.
                </p>
                <div className="mt-2.5 space-y-1 text-xs text-[#5A5052]">
                  <p className="flex items-center gap-2">
                    <Mail className="h-3.5 w-3.5 text-[#965C66]" /> support-karmayogi@gov.in
                  </p>
                  <p className="flex items-center gap-2">
                    <PhoneCall className="h-3.5 w-3.5 text-[#965C66]" /> 1800-11-KARM (Toll-Free)
                  </p>
                </div>
              </div>
              <div className="mt-3.5 pt-2.5 border-t border-[#C8A8A9]/30">
                <span className="text-[11px] text-[#5A5052]">Mon – Fri, 09:30 – 18:00 IST</span>
              </div>
            </div>

            {/* Help Card 3: Frequently Asked Questions */}
            <div className="bg-white rounded-2xl p-4 sm:p-5 border border-[#C8A8A9]/40 shadow-xs flex flex-col justify-between">
              <div>
                <div className="h-8 w-8 rounded-xl bg-[#965C66]/10 text-[#965C66] flex items-center justify-center mb-2.5">
                  <HelpCircle className="h-4 w-4" />
                </div>
                <h4 className="font-bold text-[#241E20] text-sm sm:text-base">Key Cadre Questions</h4>
                <div className="mt-2 space-y-1.5 text-xs text-[#5A5052]">
                  <div className="p-2 rounded-lg bg-[#FAF8F8] border border-[#C8A8A9]/30">
                    <p className="font-medium text-[#241E20]">How do I verify certificates?</p>
                    <p className="text-[11px] text-[#5A5052] mt-0.5">Every certificate includes a verification hash verifiable at /certificates.</p>
                  </div>
                  <div className="p-2 rounded-lg bg-[#FAF8F8] border border-[#C8A8A9]/30">
                    <p className="font-medium text-[#241E20]">What is the pass mark for modules?</p>
                    <p className="text-[11px] text-[#5A5052] mt-0.5">MoSPI accredited certifications require a 70% aggregate score.</p>
                  </div>
                </div>
              </div>
              <div className="mt-3.5 pt-2.5 border-t border-[#C8A8A9]/30">
                <a href="/login" className="inline-flex items-center text-xs font-semibold text-[#965C66] hover:text-[#824E57]">
                  View Knowledge Base <ArrowRight className="ml-1 h-3 w-3" />
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Integrated Call to Action & Institutional Closing Bar */}
        <div className="bg-[#241E20] text-white py-4 sm:py-5 border-t border-[#965C66]/30 w-full mt-auto">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
              <div>
                <h3 className="text-base sm:text-lg lg:text-xl font-bold tracking-tight">Ready to advance your official competencies?</h3>
                <p className="text-xs text-[#C8A8A9] mt-0.5 max-w-xl">
                  Sign in with your official government credentials or register with your nodal department officer today.
                </p>
              </div>
              <div className="flex flex-wrap items-center justify-center gap-3 shrink-0">
                <a href="/login">
                  <Button
                    variant="outline"
                    size="sm"
                    className="rounded-full text-[#C8A8A9] border-[#C8A8A9]/60 hover:bg-[#965C66]/20 hover:text-white px-5 py-2 text-xs cursor-pointer"
                  >
                    Official Sign In
                  </Button>
                </a>
                <a href="/register">
                  <Button
                    size="sm"
                    className="rounded-full bg-[#965C66] hover:bg-[#824E57] text-white border border-[#C8A8A9]/40 px-5 py-2 text-xs font-medium shadow-xs cursor-pointer"
                  >
                    Register New Official
                  </Button>
                </a>
              </div>
            </div>

            {/* Institutional Legal & Copyright Strip */}
            <div className="mt-3.5 pt-3 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-2 text-[11px] text-[#C8A8A9]/80 text-center sm:text-left">
              <p>© 2026 iGOT Karmayogi Bharat • Capacity Building Commission • Ministry of Statistics and Programme Implementation</p>
              <div className="flex items-center justify-center gap-4 text-[#C8A8A9]/80">
                <a href="/discover" className="hover:text-white transition-colors">Privacy Policy</a>
                <span>•</span>
                <a href="/discover" className="hover:text-white transition-colors">Terms of Service</a>
                <span>•</span>
                <a href="/discover" className="hover:text-white transition-colors">Data Governance</a>
                <span>•</span>
                <a href="/#help" className="hover:text-white transition-colors">Helpdesk</a>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
