"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Compass,
  BookOpen,
  ShieldAlert,
  User,
  LogOut,
  Settings,
  Languages,
  Menu,
  X,
  Award,
} from "lucide-react";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";
import { Button } from "@/components/ui/button";

export function Navbar() {
  const { user, logout, isAdmin } = useAuth();
  const { language, setLanguage, t } = useI18n();
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);
  const [activeSection, setActiveSection] = useState<string>("");

  const isActive = (path: string) => pathname === path || pathname?.startsWith(`${path}/`);

  const toggleLanguage = () => {
    setLanguage(language === "en" ? "hi" : "en");
  };

  // Track active section via scroll position on homepage
  useEffect(() => {
    if (pathname !== "/") {
      setActiveSection("");
      return;
    }

    const sectionIds = ["hero", "about", "how-it-works", "resources", "help"];

    const updateActiveSection = () => {
      const header = document.querySelector("header");
      const headerHeight = header ? Math.round(header.getBoundingClientRect().height) : 120;
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;
      const docHeight = document.documentElement.scrollHeight;

      // Bottom of the page: Help is active
      if (scrollY + windowHeight >= docHeight - 60) {
        setActiveSection("help");
        return;
      }

      // Top of the page: Hero is active
      if (scrollY < 80) {
        setActiveSection("hero");
        return;
      }

      // Find section closest to viewport center
      const viewportCenter = scrollY + headerHeight + (windowHeight - headerHeight) / 2;
      let closestId = "hero";
      let minDistance = Infinity;

      for (const id of sectionIds) {
        const el = document.getElementById(id);
        if (el) {
          const rect = el.getBoundingClientRect();
          const elCenter = scrollY + rect.top + rect.height / 2;
          const distance = Math.abs(viewportCenter - elCenter);
          if (distance < minDistance) {
            minDistance = distance;
            closestId = id;
          }
        }
      }

      setActiveSection(closestId);
    };

    window.addEventListener("scroll", updateActiveSection, { passive: true });
    updateActiveSection();

    return () => window.removeEventListener("scroll", updateActiveSection);
  }, [pathname]);

  // Precision smooth scroll handler for anchor links
  const handleAnchorClick = (e: React.MouseEvent<HTMLAnchorElement>, targetId: string) => {
    if (pathname === "/") {
      e.preventDefault();
      if (targetId === "hero") {
        window.scrollTo({ top: 0, behavior: "smooth" });
        window.history.replaceState(null, "", "/");
        setActiveSection("hero");
        return;
      }
      const el = document.getElementById(targetId);
      if (el) {
        const header = document.querySelector("header");
        const headerHeight = header ? Math.round(header.getBoundingClientRect().height) : 120;
        const targetTop = Math.round(el.getBoundingClientRect().top + window.scrollY - headerHeight);
        window.scrollTo({ top: Math.max(0, targetTop), behavior: "smooth" });
        window.history.replaceState(null, "", `/#${targetId}`);
        setActiveSection(targetId);
      }
    }
  };

  const handleMobileAnchorClick = (e: React.MouseEvent<HTMLAnchorElement>, targetId: string) => {
    setMobileMenuOpen(false);
    handleAnchorClick(e, targetId);
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#C8A8A9]/40 bg-white/95 backdrop-blur-md" suppressHydrationWarning>
      {/* Top Mission Karmayogi Marquee Announcement (Homepage) */}
      {pathname === "/" && (
        <div className="bg-[#EAE2E3] text-[#7A4E57] text-[11px] py-1 border-b border-[#C8A8A9]/50 overflow-hidden relative select-none">
          <div className="flex w-full overflow-hidden">
            <div className="animate-marquee flex items-center gap-16 font-medium tracking-wide">
              <span>Mission Karmayogi • India&apos;s National Public Service Learning Infrastructure</span>
              <span>Mission Karmayogi • India&apos;s National Public Service Learning Infrastructure</span>
              <span>Mission Karmayogi • India&apos;s National Public Service Learning Infrastructure</span>
              <span>Mission Karmayogi • India&apos;s National Public Service Learning Infrastructure</span>
            </div>
          </div>
        </div>
      )}

      {/* Top Ministry Ribbon */}
      <div className="bg-[#965C66] text-white text-[11px] px-4 py-1.5 flex items-center justify-between border-b border-[#824E57]">
        <div className="flex items-center gap-2 max-w-7xl mx-auto w-full">
          <div className="flex items-center gap-1.5 font-medium">
            <span className="inline-block w-2 h-2 rounded-full bg-[#EEE8E9]/90" />
            <span className="text-white font-semibold">Government of India</span>
            <span className="text-white/40">|</span>
            <span className="text-white/90">Ministry of Statistics &amp; Programme Implementation (MoSPI)</span>
          </div>
          <div className="ml-auto flex items-center gap-4 text-[11px]">
            <span className="hidden md:inline text-white/80">Mission Karmayogi Digital Learning Portal</span>
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 text-white hover:text-white font-medium bg-white/15 hover:bg-white/25 px-2.5 py-0.5 rounded cursor-pointer transition-colors border border-white/20"
            >
              <Languages className="h-3 w-3 text-[#EEE8E9]" />
              <span>{language === "en" ? "हिन्दी (HI)" : "English (EN)"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link
          href={user ? "/home" : "/"}
          onClick={(e) => {
            if (!user && pathname === "/") {
              handleAnchorClick(e, "hero");
            }
          }}
          className="flex items-center gap-3 group"
        >
          <div className="h-10 w-10 rounded-lg bg-[#241E20] flex items-center justify-center text-[#C8A8A9] shadow-xs border border-[#965C66]/30">
            <Award className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-lg font-bold text-[#241E20] tracking-tight">
                {t("nav.brand")}
              </span>
              <span className="text-[10px] uppercase font-bold bg-[#965C66]/10 text-[#965C66] px-1.5 py-0.2 rounded border border-[#965C66]/20">
                MoSPI
              </span>
            </div>
            <p className="text-[10px] text-[#5A5052] font-medium leading-none">
              {t("nav.subBrand")}
            </p>
          </div>
        </Link>

        {/* Desktop Navigation & Actions */}
        <div className="hidden md:flex items-center gap-1.5">
          <Link
            href="/#about"
            onClick={(e) => handleAnchorClick(e, "about")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeSection === "about"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                : "text-[#5A5052] hover:text-[#965C66] hover:bg-[#965C66]/5"
            }`}
          >
            {t("nav.about")}
          </Link>
          <Link
            href="/#how-it-works"
            onClick={(e) => handleAnchorClick(e, "how-it-works")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeSection === "how-it-works"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                : "text-[#5A5052] hover:text-[#965C66] hover:bg-[#965C66]/5"
            }`}
          >
            {t("nav.howItWorks")}
          </Link>
          <Link
            href="/#resources"
            onClick={(e) => handleAnchorClick(e, "resources")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeSection === "resources"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                : "text-[#5A5052] hover:text-[#965C66] hover:bg-[#965C66]/5"
            }`}
          >
            {t("nav.resources")}
          </Link>
          <Link
            href="/#help"
            onClick={(e) => handleAnchorClick(e, "help")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeSection === "help"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                : "text-[#5A5052] hover:text-[#965C66] hover:bg-[#965C66]/5"
            }`}
          >
            {t("nav.help")}
          </Link>

          {user && (
            <>
              <Link
                href="/home"
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  pathname === "/home"
                    ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                    : "text-[#5A5052] hover:text-[#965C66] hover:bg-[#965C66]/5"
                }`}
              >
                Home
              </Link>
              <Link
                href="/my-learning"
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  isActive("/my-learning") || isActive("/progress")
                    ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                    : "text-[#5A5052] hover:text-[#965C66] hover:bg-[#965C66]/5"
                }`}
              >
                <BookOpen className="h-3.5 w-3.5" />
                {t("nav.myLearning")}
              </Link>
              {isAdmin && (
                <Link
                  href="/admin"
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    isActive("/admin")
                      ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                      : "text-[#965C66] hover:bg-[#965C66]/10"
                  }`}
                >
                  <ShieldAlert className="h-3.5 w-3.5 text-[#965C66]" />
                  {t("nav.admin")}
                </Link>
              )}
            </>
          )}

          {/* Discover placed immediately to the left of Sign In */}
          <Link
            href="/discover"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              isActive("/discover") || isActive("/courses")
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold border border-[#965C66]/20"
                : "text-[#5A5052] hover:text-[#965C66] hover:bg-[#965C66]/5"
            }`}
          >
            <Compass className="h-3.5 w-3.5 text-[#965C66]" />
            {t("nav.discover")}
          </Link>

          {/* Auth Actions: Sign In immediately left of Register */}
          {user ? (
            <div className="relative ml-2">
              <button
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                className="flex items-center gap-2.5 p-1.5 rounded-full hover:bg-[#965C66]/10 border border-[#C8A8A9]/40 transition-colors cursor-pointer"
              >
                <div className="h-8 w-8 rounded-full bg-[#965C66] text-white flex items-center justify-center font-bold text-xs">
                  {user.full_name?.charAt(0) || "U"}
                </div>
                <div className="text-left pr-2">
                  <p className="text-xs font-semibold text-[#241E20] leading-tight">
                    {user.full_name}
                  </p>
                  <p className="text-[10px] text-[#5A5052] capitalize">
                    {user.role}
                  </p>
                </div>
              </button>

              {/* Profile Dropdown */}
              {profileDropdownOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-xl border border-[#C8A8A9]/40 bg-white py-1 shadow-lg z-50 animate-in fade-in zoom-in-95">
                  <div className="px-4 py-2 border-b border-slate-100">
                    <p className="text-xs font-semibold text-[#241E20]">{user.full_name}</p>
                    <p className="text-[11px] text-[#5A5052] truncate">{user.email}</p>
                  </div>
                  <Link
                    href="/profile"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-[#965C66]/5 hover:text-[#965C66]"
                  >
                    <User className="h-3.5 w-3.5 text-slate-400" />
                    {t("nav.profile")}
                  </Link>
                  <Link
                    href="/profile?tab=settings"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-[#965C66]/5 hover:text-[#965C66]"
                  >
                    <Settings className="h-3.5 w-3.5 text-slate-400" />
                    {t("nav.settings")}
                  </Link>
                  <div className="border-t border-slate-100 my-1" />
                  <button
                    onClick={() => {
                      setProfileDropdownOpen(false);
                      logout();
                    }}
                    className="w-full flex items-center gap-2 px-4 py-2 text-xs text-rose-600 hover:bg-rose-50 text-left cursor-pointer"
                  >
                    <LogOut className="h-3.5 w-3.5 text-rose-500" />
                    {t("nav.logout")}
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-2 ml-1">
              <Link href="/login">
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-[#241E20] hover:text-[#965C66] hover:bg-[#965C66]/10 font-medium px-3.5"
                >
                  {t("nav.login")}
                </Button>
              </Link>
              <Link href="/register">
                <Button
                  size="sm"
                  className="bg-[#965C66] hover:bg-[#824E57] text-white font-medium shadow-xs rounded-lg px-4 border border-[#965C66] transition-colors"
                >
                  {t("nav.register")}
                </Button>
              </Link>
            </div>
          )}
        </div>

        {/* Mobile menu trigger */}
        <div className="flex md:hidden items-center gap-2">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg text-[#5A5052] hover:bg-[#965C66]/10"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-[#C8A8A9]/40 bg-white px-4 pt-2 pb-4 space-y-1">
          {user && (
            <Link
              href="/home"
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-[#965C66]/5"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
          )}
          <Link
            href="/discover"
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-[#241E20] hover:bg-[#965C66]/5"
            onClick={() => setMobileMenuOpen(false)}
          >
            <Compass className="h-4 w-4 text-[#965C66]" />
            {t("nav.discover")}
          </Link>
          <Link
            href="/#about"
            className={`block px-3 py-2 rounded-lg text-sm font-medium ${
              activeSection === "about"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold"
                : "text-[#5A5052] hover:bg-[#965C66]/5"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "about")}
          >
            {t("nav.about")}
          </Link>
          <Link
            href="/#how-it-works"
            className={`block px-3 py-2 rounded-lg text-sm font-medium ${
              activeSection === "how-it-works"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold"
                : "text-[#5A5052] hover:bg-[#965C66]/5"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "how-it-works")}
          >
            {t("nav.howItWorks")}
          </Link>
          <Link
            href="/#resources"
            className={`block px-3 py-2 rounded-lg text-sm font-medium ${
              activeSection === "resources"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold"
                : "text-[#5A5052] hover:bg-[#965C66]/5"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "resources")}
          >
            {t("nav.resources")}
          </Link>
          <Link
            href="/#help"
            className={`block px-3 py-2 rounded-lg text-sm font-medium ${
              activeSection === "help"
                ? "bg-[#965C66]/10 text-[#965C66] font-semibold"
                : "text-[#5A5052] hover:bg-[#965C66]/5"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "help")}
          >
            {t("nav.help")}
          </Link>
          {user && (
            <Link
              href="/my-learning"
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-[#965C66]/5"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("nav.myLearning")}
            </Link>
          )}
          {isAdmin && (
            <Link
              href="/admin"
              className="block px-3 py-2 rounded-lg text-base font-medium text-[#965C66] hover:bg-[#965C66]/5"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("nav.admin")}
            </Link>
          )}
          <div className="pt-4 border-t border-slate-100">
            {user ? (
              <div className="space-y-1">
                <Link
                  href="/profile"
                  className="block px-3 py-2 text-sm text-[#5A5052]"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {t("nav.profile")}
                </Link>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    logout();
                  }}
                  className="w-full text-left px-3 py-2 text-sm text-rose-600"
                >
                  {t("nav.logout")}
                </button>
              </div>
            ) : (
              <div className="flex flex-col gap-2 pt-2">
                <Link href="/login" className="w-full">
                  <Button variant="outline" className="w-full border-[#C8A8A9]/60 text-[#241E20]">
                    {t("nav.login")}
                  </Button>
                </Link>
                <Link href="/register" className="w-full">
                  <Button className="w-full bg-[#965C66] hover:bg-[#824E57] text-white">
                    {t("nav.register")}
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
