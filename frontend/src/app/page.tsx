"use client";

import React, { useEffect, useState, useCallback } from "react";
import {
  Compass,
  ArrowRight,
  ShieldCheck,
  Award,
  BarChart3,
  FileCheck2,
  Sparkles,
  GraduationCap,
  ClipboardCheck,
  UserCheck,
  ChevronLeft,
  ChevronRight,
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
    <div className="flex flex-col min-h-screen bg-[#EEE8E9]">
      {/* 1. Hero & Statistics Section: Unified in consistent container with #EEE8E9 background */}
      <section className="bg-[#EEE8E9] text-[#241E20] pt-10 sm:pt-14 lg:pt-16 pb-8 sm:pb-10 border-b border-[#C8A8A9]/40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Two-Column Hero Grid: Left Content (7 cols) and Right Carousel (5 cols), Top-Aligned */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 xl:gap-12 items-start">
            {/* Left Column: Top-Aligned with Badge at Top */}
            <div className="lg:col-span-7 xl:col-span-7 flex flex-col justify-start text-left">
              {/* Institutional Eyebrow Badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#965C66]/10 text-[#965C66] text-xs font-semibold mb-3 w-fit border border-[#965C66]/20">
                <span className="w-1.5 h-1.5 rounded-full bg-[#965C66]" />
                Mission Karmayogi Bharat • MoSPI
              </div>

              {/* Concise Title fitting on ONE LINE on desktop */}
              <h1 className="text-2xl sm:text-3xl lg:text-[28px] xl:text-[32px] font-bold tracking-tight text-[#241E20] leading-tight lg:whitespace-nowrap">
                National Learning Platform for Civil Services
              </h1>

              {/* Short, clear subtitle directly underneath */}
              <p className="mt-3 text-sm sm:text-base text-[#5A5052] font-normal leading-relaxed max-w-xl">
                Standardized competency frameworks, accredited modules, and verified certifications for India&apos;s public administrators.
              </p>

              {/* Pill-shaped action buttons in consistent Muted Rose styling */}
              <div className="mt-7 flex flex-wrap items-center gap-3.5">
                <a href="/login">
                  <Button
                    size="lg"
                    className="rounded-full bg-[#965C66] hover:bg-[#824E57] text-white font-medium text-sm px-6 py-2.5 shadow-xs transition-all flex items-center gap-2 border border-[#965C66] cursor-pointer"
                  >
                    Official Sign In <ArrowRight className="h-4 w-4" />
                  </Button>
                </a>
                <a href="/discover">
                  <Button
                    size="lg"
                    variant="outline"
                    className="rounded-full border-[#965C66]/40 text-[#965C66] hover:bg-[#965C66]/10 hover:border-[#965C66] hover:text-[#824E57] font-medium text-sm px-6 py-2.5 transition-all flex items-center gap-2 bg-transparent cursor-pointer"
                  >
                    <Compass className="h-4 w-4 text-[#965C66]" /> Explore Courses
                  </Button>
                </a>
              </div>
            </div>

            {/* Right Column: Hero Image Carousel (~35-40% width), Top-Aligned with Badge, Right-Edge Aligned */}
            <div className="lg:col-span-5 xl:col-span-5 w-full flex flex-col items-end">
              <div className="w-full">
                {/* Clean White Frame: Top edge aligned with Badge, object-contain to NEVER crop any image */}
                <div
                  className="relative w-full h-[195px] sm:h-[215px] bg-white rounded-xl border border-[#C8A8A9]/50 shadow-xs p-2 sm:p-2.5 overflow-hidden group"
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
                    className="absolute left-1.5 top-1/2 -translate-y-1/2 z-20 h-6 w-6 rounded-full bg-white/90 hover:bg-white text-[#5A5052] hover:text-[#965C66] flex items-center justify-center shadow-xs border border-[#C8A8A9]/40 transition-opacity opacity-0 group-hover:opacity-100 cursor-pointer"
                  >
                    <ChevronLeft className="h-3.5 w-3.5" />
                  </button>
                  <button
                    type="button"
                    onClick={handleNext}
                    aria-label="Next slide"
                    className="absolute right-1.5 top-1/2 -translate-y-1/2 z-20 h-6 w-6 rounded-full bg-white/90 hover:bg-white text-[#5A5052] hover:text-[#965C66] flex items-center justify-center shadow-xs border border-[#C8A8A9]/40 transition-opacity opacity-0 group-hover:opacity-100 cursor-pointer"
                  >
                    <ChevronRight className="h-3.5 w-3.5" />
                  </button>
                </div>

                {/* Small, subtle pagination indicators & controls underneath */}
                <div className="mt-2 flex items-center justify-center gap-1.5">
                  <button
                    type="button"
                    onClick={handlePrev}
                    aria-label="Previous slide"
                    className="h-5 w-5 rounded-full bg-white/90 hover:bg-white text-[#5A5052] hover:text-[#965C66] flex items-center justify-center border border-[#C8A8A9]/40 shadow-2xs transition-colors cursor-pointer"
                  >
                    <ChevronLeft className="h-3 w-3" />
                  </button>

                  <div className="flex items-center gap-1.5 px-2 py-0.5 bg-white/90 rounded-full border border-[#C8A8A9]/40 shadow-2xs">
                    {HERO_SLIDES.map((_, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setCurrentSlide(idx)}
                        aria-label={`Slide ${idx + 1}`}
                        className={`transition-all duration-300 rounded-full cursor-pointer ${
                          idx === currentSlide
                            ? "w-3.5 h-1 bg-[#965C66]"
                            : "w-1 h-1 bg-[#C8A8A9]/70 hover:bg-[#965C66]/60"
                        }`}
                      />
                    ))}
                  </div>

                  <button
                    type="button"
                    onClick={handleNext}
                    aria-label="Next slide"
                    className="h-5 w-5 rounded-full bg-white/90 hover:bg-white text-[#5A5052] hover:text-[#965C66] flex items-center justify-center border border-[#C8A8A9]/40 shadow-2xs transition-colors cursor-pointer"
                  >
                    <ChevronRight className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Statistics Bar: In the EXACT same container, visually aligned with hero content left and right edges */}
          <div className="mt-10 sm:mt-12 pt-6 sm:pt-7 border-t border-[#C8A8A9]/35">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-0 md:divide-x md:divide-[#C8A8A9]/35">
              {/* Item 1: Aligns directly with the left edge of the hero content */}
              <div className="text-left md:pr-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#965C66]">40,000+</p>
                <p className="text-xs font-medium text-[#5A5052] mt-0.5">Civil Servants Trained</p>
              </div>

              {/* Item 2 */}
              <div className="text-left md:px-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#965C66]">100%</p>
                <p className="text-xs font-medium text-[#5A5052] mt-0.5">MoSPI Standardized</p>
              </div>

              {/* Item 3 */}
              <div className="text-left md:px-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#965C66]">UN-NQAF</p>
                <p className="text-xs font-medium text-[#5A5052] mt-0.5">Quality Frameworks</p>
              </div>

              {/* Item 4: Left-aligned within column matching items 1-3 */}
              <div className="text-left md:pl-6">
                <p className="text-2xl sm:text-3xl font-bold tracking-tight text-[#965C66]">Verifiable</p>
                <p className="text-xs font-medium text-[#5A5052] mt-0.5">Government Credentials</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. About Section: Retained Institutional Overview */}
      <section id="about" className="py-12 sm:py-16 bg-white border-b border-[#C8A8A9]/30">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-center">
            {/* LEFT: Institutional Visual Card styled with Rose and Charcoal Palette */}
            <div className="lg:col-span-5">
              <div className="bg-[#241E20] rounded-xl p-6 text-white border border-[#965C66]/30 shadow-xs relative overflow-hidden">
                {/* Visual header */}
                <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-5">
                  <div className="flex items-center gap-2.5">
                    <div className="h-8 w-8 rounded-lg bg-[#965C66]/25 border border-[#C8A8A9]/40 flex items-center justify-center text-[#C8A8A9]">
                      <Award className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-white leading-none">NPCSCB Framework</p>
                      <p className="text-[10px] text-[#C8A8A9]/80 mt-0.5">Capacity Building Commission</p>
                    </div>
                  </div>
                  <span className="text-[10px] uppercase font-semibold tracking-wider text-white bg-[#965C66] px-2 py-0.5 rounded">
                    Verified
                  </span>
                </div>

                {/* Structured Competency Matrix */}
                <div className="space-y-3">
                  <div className="bg-white/5 rounded-lg p-3 border border-white/10">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-white font-medium flex items-center gap-1.5">
                        <BarChart3 className="h-3.5 w-3.5 text-[#C8A8A9]" />
                        Official Statistical Cadre
                      </span>
                      <span className="text-[11px] text-[#C8A8A9]">NSS • CPI • NAS</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-[#965C66] h-full rounded-full w-[88%]" />
                    </div>
                  </div>

                  <div className="bg-white/5 rounded-lg p-3 border border-white/10">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-white font-medium flex items-center gap-1.5">
                        <FileCheck2 className="h-3.5 w-3.5 text-[#C8A8A9]" />
                        Accredited Assessments
                      </span>
                      <span className="text-[11px] text-[#C8A8A9]">70% Threshold</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-[#BC9798] h-full rounded-full w-[94%]" />
                    </div>
                  </div>

                  <div className="bg-white/5 rounded-lg p-3 border border-white/10">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-white font-medium flex items-center gap-1.5">
                        <Sparkles className="h-3.5 w-3.5 text-[#C8A8A9]" />
                        LangGraph Copilot Intelligence
                      </span>
                      <span className="text-[11px] text-[#C8A8A9]">Active</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-[#965C66] h-full rounded-full w-[100%]" />
                    </div>
                  </div>
                </div>

                {/* Institutional Footer note */}
                <div className="mt-5 pt-3.5 border-t border-white/10 flex items-center justify-between text-[11px] text-[#C8A8A9]/80">
                  <span>MoSPI • CSO • NSSO • NSSTA</span>
                  <span className="text-[#C8A8A9] font-medium flex items-center gap-1">
                    <ShieldCheck className="h-3.5 w-3.5" /> ISO/IEC Aligned
                  </span>
                </div>
              </div>
            </div>

            {/* RIGHT: Section Title and Descriptive Text */}
            <div className="lg:col-span-7">
              <h2 className="text-2xl sm:text-3xl font-bold text-[#241E20] tracking-tight leading-tight">
                A Competency-Driven Learning Paradigm
              </h2>
              <p className="mt-3 text-[#5A5052] text-sm sm:text-base leading-relaxed font-normal">
                Moving the civil service from traditional rules-based procedures to roles-based competency mastery, aligned with the National Programme for Civil Services Capacity Building (NPCSCB).
              </p>

              {/* Three Core Pillars Content */}
              <div className="mt-6 space-y-4">
                <div className="flex items-start gap-3.5">
                  <div className="h-8 w-8 rounded-lg bg-[#965C66]/10 text-[#965C66] border border-[#965C66]/20 flex items-center justify-center shrink-0 mt-0.5">
                    <BarChart3 className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-[#241E20]">Statistical Integrity</h3>
                    <p className="text-xs sm:text-sm text-[#5A5052] mt-0.5 leading-normal">
                      Rigorous curricula on National Sample Surveys (NSS), Consumer Price Index (CPI), and National Accounts compilation.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5">
                  <div className="h-8 w-8 rounded-lg bg-[#965C66]/10 text-[#965C66] border border-[#965C66]/20 flex items-center justify-center shrink-0 mt-0.5">
                    <FileCheck2 className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-[#241E20]">Certified Assessments</h3>
                    <p className="text-xs sm:text-sm text-[#5A5052] mt-0.5 leading-normal">
                      Verified evaluations with minimum 70% passing threshold, awarding official digital credentials to your employee record.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5">
                  <div className="h-8 w-8 rounded-lg bg-[#965C66]/10 text-[#965C66] border border-[#965C66]/20 flex items-center justify-center shrink-0 mt-0.5">
                    <Sparkles className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-[#241E20]">AI-Orchestrated Assistant</h3>
                    <p className="text-xs sm:text-sm text-[#5A5052] mt-0.5 leading-normal">
                      Built-in civil service copilot providing immediate guidance on methodologies, regulatory clarifications, and lookups.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Learning Journey: Single Unified Horizontal Progression Flow */}
      <section id="how-it-works" className="py-12 sm:py-14 bg-[#FAF8F8] border-b border-[#C8A8A9]/30">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-8">
            <h2 className="text-2xl sm:text-3xl font-bold text-[#241E20] tracking-tight">
              How the Karmayogi Learning Journey Works
            </h2>
            <p className="mt-2 text-[#5A5052] text-xs sm:text-sm">
              A structured 4-step progression from role onboarding to recognized certification.
            </p>
          </div>

          {/* Single Horizontal Progression Container */}
          <div className="bg-white rounded-xl border border-[#C8A8A9]/40 p-5 sm:p-7 shadow-xs">
            <div className="relative">
              {/* Connected horizontal track line on desktop */}
              <div className="hidden md:block absolute top-4 left-6 right-6 h-0.5 bg-gradient-to-r from-[#965C66] via-[#BC9798] to-[#C8A8A9] z-0" />

              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 md:gap-5 relative z-10">
                {/* Step 1 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-3">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    1
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <UserCheck className="h-4 w-4 text-[#965C66] shrink-0" /> Onboard Role
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                      Specify your ministry, department, cadre, and official assignments during onboarding.
                    </p>
                  </div>
                </div>

                {/* Step 2 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-3">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    2
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <GraduationCap className="h-4 w-4 text-[#965C66] shrink-0" /> Discover &amp; Study
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                      Consume video lectures, CAPI field simulation labs, and interactive concept lessons.
                    </p>
                  </div>
                </div>

                {/* Step 3 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-3">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    3
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <ClipboardCheck className="h-4 w-4 text-[#965C66] shrink-0" /> Pass Assessment
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                      Complete objective MCQ tests with immediate correctness feedback and answer breakdowns.
                    </p>
                  </div>
                </div>

                {/* Step 4 */}
                <div className="flex md:flex-col items-start gap-3 md:gap-3">
                  <div className="h-8 w-8 rounded-full bg-[#965C66] text-white font-bold text-xs flex items-center justify-center shrink-0 ring-4 ring-white shadow-xs">
                    4
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-[#241E20] text-sm flex items-center gap-1.5">
                      <Award className="h-4 w-4 text-[#965C66] shrink-0" /> Earn Certificate
                    </h4>
                    <p className="text-xs text-[#5A5052] mt-1 leading-relaxed">
                      Receive verifiable digital credentials stored permanently in your civil service profile.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Call to Action Bar: Retained Footer Section */}
      <section className="bg-[#241E20] text-white py-10 sm:py-12 border-t border-[#965C66]/30">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
          <div>
            <h3 className="text-xl sm:text-2xl font-bold tracking-tight">Ready to advance your official competencies?</h3>
            <p className="text-xs sm:text-sm text-[#C8A8A9] mt-1">
              Sign in with your official government email or register your employee credentials today.
            </p>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-3 shrink-0">
            <a href="/login">
              <Button
                variant="outline"
                className="rounded-full text-[#C8A8A9] border-[#C8A8A9]/60 hover:bg-[#965C66]/20 hover:text-white px-6 text-sm cursor-pointer"
              >
                Sign In
              </Button>
            </a>
            <a href="/register">
              <Button
                className="rounded-full bg-[#965C66] hover:bg-[#824E57] text-white border border-[#C8A8A9]/40 px-6 text-sm font-medium shadow-xs cursor-pointer"
              >
                Register New Official
              </Button>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
