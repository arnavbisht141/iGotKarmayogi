"use client";

import React, { useState, useEffect, useRef } from "react";
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

  const isProgrammaticScrollRef = useRef(false);
  const scrollTimerRef = useRef<NodeJS.Timeout | null>(null);

  const isActive = (path: string) => pathname === path || pathname?.startsWith(`${path}/`);

  const toggleLanguage = () => {
    setLanguage(language === "en" ? "hi" : "en");
  };

  // Cleanup programmatic scroll timer
  useEffect(() => {
    return () => {
      if (scrollTimerRef.current) {
        clearTimeout(scrollTimerRef.current);
      }
    };
  }, []);

  // Track active section via scroll position on homepage
  useEffect(() => {
    if (pathname !== "/") {
      setActiveSection("");
      return;
    }

    const sectionIds = ["hero", "about", "how-it-works", "resources", "help"];

    const updateActiveSection = () => {
      // If a programmatic scroll is currently animating from a user click, don't flicker tabs
      if (isProgrammaticScrollRef.current) return;

      const header = document.querySelector("header");
      const headerHeight = header ? Math.round(header.getBoundingClientRect().height) : 68;
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
    if (!user && pathname === "/") {
      e.preventDefault();
      e.stopPropagation();

      // Lock active state immediately to avoid tab blinking during the glide
      isProgrammaticScrollRef.current = true;
      setActiveSection(targetId);

      if (scrollTimerRef.current) {
        clearTimeout(scrollTimerRef.current);
      }
      scrollTimerRef.current = setTimeout(() => {
        isProgrammaticScrollRef.current = false;
      }, 750);

      if (targetId === "hero") {
        window.scrollTo({ top: 0, behavior: "smooth" });
        return;
      }
      const el = document.getElementById(targetId);
      if (el) {
        const header = document.querySelector("header");
        const headerHeight = header ? Math.round(header.getBoundingClientRect().height) : 68;
        const targetTop = Math.round(el.getBoundingClientRect().top + window.scrollY - headerHeight);
        window.scrollTo({ top: Math.max(0, targetTop), behavior: "smooth" });
      }
    }
  };

  const handleMobileAnchorClick = (e: React.MouseEvent<HTMLAnchorElement>, targetId: string) => {
    setMobileMenuOpen(false);
    handleAnchorClick(e, targetId);
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/98 backdrop-blur-md shadow-sm" suppressHydrationWarning>
      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link
          href={user ? "/home" : "/"}
          scroll={false}
          prefetch={false}
          onClick={(e) => {
            if (!user && pathname === "/") {
              handleAnchorClick(e, "hero");
            }
          }}
          className="flex items-center gap-3 group cursor-pointer"
        >
          <div className="h-9 w-9 rounded-xl navy-teal-gradient flex items-center justify-center text-white shadow-sm">
            <Award className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-base sm:text-lg font-bold text-[#0F172A] tracking-tight group-hover:text-[#1E3A8A] transition-colors">
                {t("nav.brand")}
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-semibold leading-none tracking-wide uppercase">
              MoSPI • Government of India
            </p>
          </div>
        </Link>

        {/* Desktop Navigation & Actions */}
        <div className="hidden md:flex items-center gap-1.5">
          {/* Institutional Section Navigation Links */}
          {/* ── Institutional anchor/page links ── */}
          {["about", "how-it-works", "resources", "help"].map((section) => {
            const isActiveLink = isActive(`/${section}`) || (pathname === "/" && activeSection === section);
            const label = section === "about" ? t("nav.about")
              : section === "how-it-works" ? t("nav.howItWorks")
              : section === "resources" ? t("nav.resources")
              : t("nav.help");
            return (
              <Link key={section}
                href={!user && pathname === "/" ? `/#${section}` : `/${section}`}
                scroll={false} prefetch={false}
                onClick={(e) => handleAnchorClick(e, section)}
                className={`relative px-3.5 py-2 text-sm font-medium transition-all duration-200 cursor-pointer ${
                  isActiveLink ? "text-[#1E3A8A] font-bold" : "text-slate-600 hover:text-[#1E3A8A]"
                }`}
              >
                {label}
                {/* Bottom-bar active indicator */}
                <span className={`absolute bottom-0 left-3.5 right-3.5 h-0.5 rounded-full transition-all duration-300 ${
                  isActiveLink ? "navy-teal-gradient opacity-100" : "opacity-0 bg-[#1E3A8A]"
                }`} style={isActiveLink ? { background: "linear-gradient(90deg,#1E3A8A,#0D9488)" } : {}} />
              </Link>
            );
          })}

          {/* ── Authenticated user links ── */}
          {user && (
            <>
              {[{ href: "/home", label: "Home" }, { href: "/my-learning", label: t("nav.myLearning") }].map(({ href, label }) => (
                <Link key={href} href={href}
                  className={`relative px-3.5 py-2 text-sm font-medium transition-all duration-200 ${
                    isActive(href) ? "text-[#1E3A8A] font-bold" : "text-slate-600 hover:text-[#1E3A8A]"
                  }`}>
                  {label}
                  <span className={`absolute bottom-0 left-3.5 right-3.5 h-0.5 rounded-full transition-all duration-300 ${
                    isActive(href) ? "opacity-100" : "opacity-0"
                  }`} style={{ background: "linear-gradient(90deg,#1E3A8A,#0D9488)" }} />
                </Link>
              ))}
              {isAdmin && (
                <Link href="/admin"
                  className={`relative px-3.5 py-2 text-sm font-medium transition-all duration-200 ${
                    isActive("/admin") ? "text-[#1E3A8A] font-bold" : "text-slate-600 hover:text-[#1E3A8A]"
                  }`}>
                  {t("nav.admin")}
                  <span className={`absolute bottom-0 left-3.5 right-3.5 h-0.5 rounded-full transition-all duration-300 ${
                    isActive("/admin") ? "opacity-100" : "opacity-0"
                  }`} style={{ background: "linear-gradient(90deg,#1E3A8A,#0D9488)" }} />
                </Link>
              )}
            </>
          )}

          {/* ── Discover ── */}
          <Link href="/discover"
            className={`relative flex items-center gap-1.5 px-3.5 py-2 text-sm font-medium transition-all duration-200 ${
              isActive("/discover") || isActive("/courses") ? "text-[#1E3A8A] font-bold" : "text-slate-600 hover:text-[#1E3A8A]"
            }`}>
            <Compass className="h-4 w-4" />
            {t("nav.discover")}
            <span className={`absolute bottom-0 left-3.5 right-3.5 h-0.5 rounded-full transition-all duration-300 ${
              isActive("/discover") || isActive("/courses") ? "opacity-100" : "opacity-0"
            }`} style={{ background: "linear-gradient(90deg,#1E3A8A,#0D9488)" }} />
          </Link>

          {/* Language Switcher */}
          <button
            type="button"
            onClick={toggleLanguage}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-slate-200 text-xs font-bold text-slate-600 hover:text-[#1E3A8A] hover:border-[#1E3A8A]/40 hover:bg-blue-50/50 transition-all cursor-pointer"
            title={language === "en" ? "हिन्दी में बदलें" : "Switch to English"}
          >
            <Languages className="h-3.5 w-3.5 text-[#0D9488]" />
            <span>{language === "en" ? "हिन्दी" : "English"}</span>
          </button>

          {/* Auth Actions: Sign In immediately left of Register */}
          {user ? (
            <div className="relative ml-2">
              <button
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                className="flex items-center gap-2.5 p-1 rounded-full hover:bg-slate-50 border border-slate-200 hover:border-[#1E3A8A]/30 transition-all cursor-pointer group"
              >
                {/* Gradient ring avatar */}
                <div className="h-9 w-9 rounded-full p-[2px] navy-teal-gradient shadow-sm">
                  <div className="h-full w-full rounded-full bg-[#0C1B3D] text-white flex items-center justify-center font-extrabold text-xs">
                    {user.full_name?.charAt(0) || "U"}
                  </div>
                </div>
                <div className="text-left pr-2">
                  <p className="text-xs font-bold text-slate-900 leading-tight">
                    {user.full_name}
                  </p>
                  <p className="text-[10px] text-slate-400 capitalize font-medium">
                    {user.role}
                  </p>
                </div>
              </button>

              {/* Profile Dropdown */}
              {profileDropdownOpen && (
                <div className="absolute right-0 mt-2 w-60 rounded-2xl border border-slate-200 bg-white py-1 shadow-xl z-50" style={{ boxShadow: "0 12px 40px rgba(0,0,0,0.12), 0 0 0 1px rgba(0,0,0,0.04)" }}>
                  <div className="px-4 py-2 border-b border-slate-100">
                    <p className="text-xs font-semibold text-[#0F172A]">{user.full_name}</p>
                    <p className="text-[11px] text-slate-500 truncate">{user.email}</p>
                  </div>
                  <Link
                    href="/profile"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-blue-50 hover:text-[#1E3A8A]"
                  >
                    <User className="h-3.5 w-3.5 text-slate-400" />
                    {t("nav.profile")}
                  </Link>
                  <Link
                    href="/profile?tab=settings"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-blue-50 hover:text-[#1E3A8A]"
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
            <div className="flex items-center gap-2.5 ml-2">
              <Link href="/login">
                <Button
                  variant="ghost"
                  size="md"
                  className="text-slate-800 hover:text-[#1E3A8A] hover:bg-slate-100 font-semibold px-4 h-10 text-sm rounded-lg cursor-pointer"
                >
                  {t("nav.login")}
                </Button>
              </Link>
              <Link href="/register">
                <Button
                  size="md"
                  className="navy-teal-gradient text-white font-bold shadow-sm rounded-xl px-5 h-10 text-sm border-0 transition-all cursor-pointer hover:opacity-90 hover:scale-105"
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
            className="p-2 rounded-lg text-slate-600 hover:bg-slate-100 cursor-pointer"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1">
          {user && (
            <Link
              href="/home"
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-blue-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
          )}
          <Link
            href="/discover"
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-900 hover:bg-blue-50"
            onClick={() => setMobileMenuOpen(false)}
          >
            <Compass className="h-4 w-4 text-[#1E3A8A]" />
            {t("nav.discover")}
          </Link>
          <Link
            href={!user && pathname === "/" ? "/#about" : "/about"}
            className={`block px-3 py-2 rounded-lg text-sm font-medium border transition-all duration-200 cursor-pointer ${
              isActive("/about") || (pathname === "/" && activeSection === "about")
                ? "bg-blue-50 text-[#1E3A8A] font-semibold border-blue-200"
                : "text-slate-700 hover:bg-blue-50 border-transparent"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "about")}
          >
            {t("nav.about")}
          </Link>
          <Link
            href={!user && pathname === "/" ? "/#how-it-works" : "/how-it-works"}
            className={`block px-3 py-2 rounded-lg text-sm font-medium border transition-all duration-200 cursor-pointer ${
              isActive("/how-it-works") || (pathname === "/" && activeSection === "how-it-works")
                ? "bg-blue-50 text-[#1E3A8A] font-semibold border-blue-200"
                : "text-slate-700 hover:bg-blue-50 border-transparent"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "how-it-works")}
          >
            {t("nav.howItWorks")}
          </Link>
          <Link
            href={!user && pathname === "/" ? "/#resources" : "/resources"}
            className={`block px-3 py-2 rounded-lg text-sm font-medium border transition-all duration-200 cursor-pointer ${
              isActive("/resources") || (pathname === "/" && activeSection === "resources")
                ? "bg-blue-50 text-[#1E3A8A] font-semibold border-blue-200"
                : "text-slate-700 hover:bg-blue-50 border-transparent"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "resources")}
          >
            {t("nav.resources")}
          </Link>
          <Link
            href={!user && pathname === "/" ? "/#help" : "/help"}
            className={`block px-3 py-2 rounded-lg text-sm font-medium border transition-all duration-200 cursor-pointer ${
              isActive("/help") || (pathname === "/" && activeSection === "help")
                ? "bg-blue-50 text-[#1E3A8A] font-semibold border-blue-200"
                : "text-slate-700 hover:bg-blue-50 border-transparent"
            }`}
            onClick={(e) => handleMobileAnchorClick(e, "help")}
          >
            {t("nav.help")}
          </Link>
          {user && (
            <Link
              href="/my-learning"
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-blue-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("nav.myLearning")}
            </Link>
          )}
          {isAdmin && (
            <Link
              href="/admin"
              className="block px-3 py-2 rounded-lg text-base font-medium text-[#1E3A8A] hover:bg-blue-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("nav.admin")}
            </Link>
          )}

          {/* Mobile Language Switcher */}
          <div className="pt-2 pb-1">
            <button
              type="button"
              onClick={() => {
                toggleLanguage();
                setMobileMenuOpen(false);
              }}
              className="w-full flex items-center justify-between px-3 py-2 rounded-lg border border-slate-200 text-sm font-semibold text-slate-700 hover:bg-slate-50 cursor-pointer"
            >
              <span className="flex items-center gap-2">
                <Languages className="h-4 w-4 text-slate-500" />
                <span>{language === "en" ? "भाषा: हिन्दी" : "Language: English"}</span>
              </span>
              <span className="text-xs text-[#1E3A8A] font-bold">
                {language === "en" ? "बदलें" : "Switch"}
              </span>
            </button>
          </div>

          <div className="pt-3 border-t border-slate-100">
            {user ? (
              <div className="space-y-1">
                <Link
                  href="/profile"
                  className="block px-3 py-2 text-sm text-slate-600"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {t("nav.profile")}
                </Link>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    logout();
                  }}
                  className="w-full text-left px-3 py-2 text-sm text-rose-600 cursor-pointer"
                >
                  {t("nav.logout")}
                </button>
              </div>
            ) : (
              <div className="flex flex-col gap-2 pt-2">
                <Link href="/login" className="w-full">
                  <Button variant="outline" className="w-full border-slate-300 text-slate-800">
                    {t("nav.login")}
                  </Button>
                </Link>
                <Link href="/register" className="w-full">
                  <Button className="w-full bg-[#1E3A8A] hover:bg-[#1D3557] text-white">
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
