"use client";

import React, { useEffect, useState, useCallback } from "react";
import {
  Compass,
  ArrowRight,
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
    <div className="flex flex-col min-h-[calc(100vh-140px)] bg-[#F8FAFC]">
      {/* 1. Hero & Statistics Section */}
      <section className="bg-gradient-to-b from-white via-[#F8FAFC] to-[#F1F5F9] text-[#0F172A] pt-10 sm:pt-14 lg:pt-16 pb-12 sm:pb-16 flex-1">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Two-Column Hero Grid: Left Content (7 cols) and Right Carousel (5 cols), Top-Aligned */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 xl:gap-12 items-start">
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
    </div>
  );
}
