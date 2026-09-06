"use client";

import React, { useState } from "react";
import Link from "next/navigation";
import { usePathname } from "next/navigation";
import {
  Compass,
  BookOpen,
  Search,
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
  const [mounted, setMounted] = useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const isActive = (path: string) => pathname === path || pathname?.startsWith(`${path}/`);

  const toggleLanguage = () => {
    setLanguage(language === "en" ? "hi" : "en");
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur-md" suppressHydrationWarning>
      {/* Top Ministry Ribbon */}
      <div className="bg-[#1E3A8A] text-white text-[11px] px-4 py-1.5 flex items-center justify-between border-b border-blue-900">
        <div className="flex items-center gap-2 max-w-7xl mx-auto w-full">
          <div className="flex items-center gap-1.5 font-medium">
            <span className="inline-block w-2 h-2 rounded-full bg-amber-400" />
            <span className="text-white font-semibold">Government of India</span>
            <span className="text-white/40">|</span>
            <span className="text-white/90">Ministry of Statistics &amp; Programme Implementation (MoSPI)</span>
          </div>
          <div className="ml-auto flex items-center gap-4 text-[11px]">
            <span className="hidden md:inline text-white/80">Mission Karmayogi Digital Learning Portal</span>
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 text-white hover:text-white font-medium bg-white/10 hover:bg-white/20 px-2.5 py-0.5 rounded cursor-pointer transition-colors border border-white/20"
            >
              <Languages className="h-3 w-3 text-white/90" />
              <span>{language === "en" ? "हिन्दी (HI)" : "English (EN)"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <a href={user ? "/home" : "/"} className="flex items-center gap-3 group">
          <div className="h-10 w-10 rounded-lg bg-[#1E3A8A] flex items-center justify-center text-white shadow-xs border border-blue-900">
            <Award className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-lg font-bold text-[#0F172A] tracking-tight">
                {t("nav.brand")}
              </span>
            </div>
            <p className="text-[10px] text-slate-500 font-medium leading-none">
              {t("nav.subBrand")}
            </p>
          </div>
        </a>

        {/* Desktop Navigation & Actions */}
        <div className="hidden md:flex items-center gap-1.5">
          {/* Institutional Navigation Links - Identical font & design to Discover */}
          <a
            href="#about"
            className="px-3.5 py-2 rounded-lg text-sm font-medium text-slate-700 hover:text-[#1E3A8A] hover:bg-slate-50 transition-colors"
          >
            About
          </a>
          <a
            href="#resources"
            className="px-3.5 py-2 rounded-lg text-sm font-medium text-slate-700 hover:text-[#1E3A8A] hover:bg-slate-50 transition-colors"
          >
            Resources
          </a>
          <a
            href="#help"
            className="px-3.5 py-2 rounded-lg text-sm font-medium text-slate-700 hover:text-[#1E3A8A] hover:bg-slate-50 transition-colors"
          >
            Help
          </a>

          {user && (
            <>
              <a
                href="/home"
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  pathname === "/home"
                    ? "bg-blue-50 text-[#1E3A8A] font-semibold border border-blue-200"
                    : "text-slate-600 hover:text-[#1E3A8A] hover:bg-slate-50"
                }`}
              >
                Home
              </a>
              <a
                href="/my-learning"
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  isActive("/my-learning") || isActive("/progress")
                    ? "bg-blue-50 text-[#1E3A8A] font-semibold border border-blue-200"
                    : "text-slate-600 hover:text-[#1E3A8A] hover:bg-slate-50"
                }`}
              >
                <BookOpen className="h-3.5 w-3.5" />
                {t("nav.myLearning")}
              </a>
              {isAdmin && (
                <a
                  href="/admin"
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    isActive("/admin")
                      ? "bg-blue-50 text-[#1E3A8A] font-semibold border border-blue-200"
                      : "text-[#1E3A8A] hover:bg-blue-50"
                  }`}
                >
                  <ShieldAlert className="h-3.5 w-3.5 text-[#1E3A8A]" />
                  {t("nav.admin")}
                </a>
              )}
            </>
          )}

          {/* Discover placed immediately to the left of Sign In */}
          <a
            href="/discover"
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive("/discover") || isActive("/courses")
                ? "bg-blue-50 text-[#1E3A8A] font-semibold border border-blue-200"
                : "text-slate-700 hover:text-[#1E3A8A] hover:bg-slate-50"
            }`}
          >
            <Compass className="h-4 w-4 text-[#1E3A8A]" />
            {t("nav.discover")}
          </a>

          {/* Auth Actions: Sign In immediately left of Register */}
          {user ? (
            <div className="relative ml-2">
              <button
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                className="flex items-center gap-2.5 p-1.5 rounded-full hover:bg-slate-100 border border-slate-200 transition-colors cursor-pointer"
              >
                <div className="h-8 w-8 rounded-full bg-[#1E3A8A] text-white flex items-center justify-center font-bold text-xs">
                  {user.full_name?.charAt(0) || "U"}
                </div>
                <div className="text-left pr-2">
                  <p className="text-xs font-semibold text-[#0F172A] leading-tight">
                    {user.full_name}
                  </p>
                  <p className="text-[10px] text-slate-500 capitalize">
                    {user.role}
                  </p>
                </div>
              </button>

              {/* Profile Dropdown */}
              {profileDropdownOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-xl border border-slate-200 bg-white py-1 shadow-lg z-50 animate-in fade-in zoom-in-95">
                  <div className="px-4 py-2 border-b border-slate-100">
                    <p className="text-xs font-semibold text-[#0F172A]">{user.full_name}</p>
                    <p className="text-[11px] text-slate-500 truncate">{user.email}</p>
                  </div>
                  <a
                    href="/profile"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-blue-50 hover:text-[#1E3A8A]"
                  >
                    <User className="h-3.5 w-3.5 text-slate-400" />
                    {t("nav.profile")}
                  </a>
                  <a
                    href="/profile?tab=settings"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-blue-50 hover:text-[#1E3A8A]"
                  >
                    <Settings className="h-3.5 w-3.5 text-slate-400" />
                    {t("nav.settings")}
                  </a>
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
              <a href="/login">
                <Button
                  variant="ghost"
                  size="md"
                  className="text-slate-800 hover:text-[#1E3A8A] hover:bg-slate-100 font-semibold px-4 h-10 text-sm rounded-lg cursor-pointer"
                >
                  {t("nav.login")}
                </Button>
              </a>
              <a href="/register">
                <Button
                  size="md"
                  className="bg-[#1E3A8A] hover:bg-[#1D3557] text-white font-semibold shadow-sm rounded-lg px-5 h-10 text-sm border border-[#1E3A8A] transition-all cursor-pointer"
                >
                  {t("nav.register")}
                </Button>
              </a>
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
            <a
              href="/home"
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-blue-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </a>
          )}
          <a
            href="/discover"
            className="block px-3 py-2 rounded-lg text-base font-medium text-slate-900 hover:bg-blue-50"
            onClick={() => setMobileMenuOpen(false)}
          >
            {t("nav.discover")}
          </a>
          <a
            href="#about"
            className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
            onClick={() => setMobileMenuOpen(false)}
          >
            About
          </a>
          <a
            href="#resources"
            className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
            onClick={() => setMobileMenuOpen(false)}
          >
            Resources
          </a>
          <a
            href="#help"
            className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
            onClick={() => setMobileMenuOpen(false)}
          >
            Help
          </a>
          {user && (
            <a
              href="/my-learning"
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-blue-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("nav.myLearning")}
            </a>
          )}
          {isAdmin && (
            <a
              href="/admin"
              className="block px-3 py-2 rounded-lg text-base font-medium text-[#1E3A8A] hover:bg-blue-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("nav.admin")}
            </a>
          )}
          <div className="pt-4 border-t border-slate-100">
            {user ? (
              <div className="space-y-1">
                <a
                  href="/profile"
                  className="block px-3 py-2 text-sm text-slate-600"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {t("nav.profile")}
                </a>
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
                <a href="/login" className="w-full">
                  <Button variant="outline" className="w-full border-slate-300 text-slate-800">
                    {t("nav.login")}
                  </Button>
                </a>
                <a href="/register" className="w-full">
                  <Button className="w-full bg-[#1E3A8A] hover:bg-[#1D3557] text-white">
                    {t("nav.register")}
                  </Button>
                </a>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

