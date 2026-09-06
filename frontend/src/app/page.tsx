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
    <div className="flex flex-col min-h-[calc(100vh-140px)] bg-[#EEE8E9]">
      {/* 1. Hero & Statistics Section: Unified in consistent container with #EEE8E9 background */}
      <section className="bg-[#EEE8E9] text-[#241E20] pt-10 sm:pt-14 lg:pt-16 pb-12 sm:pb-16 flex-1">
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
    </div>
  );
}

