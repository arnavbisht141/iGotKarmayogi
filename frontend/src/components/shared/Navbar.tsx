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

  const isActive = (path: string) => pathname === path || pathname?.startsWith(`${path}/`);

  const toggleLanguage = () => {
    setLanguage(language === "en" ? "hi" : "en");
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur-md">
      {/* Top Mission Karmayogi Marquee Announcement (Homepage) */}
      {pathname === "/" && (
        <div className="bg-[#241E20] text-[#C8A8A9] text-[11px] py-1 border-b border-[#965C66]/25 overflow-hidden relative select-none">
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
      <div className="bg-slate-900 text-slate-300 text-[11px] px-4 py-1 flex items-center justify-between border-b border-slate-800">
        <div className="flex items-center gap-2 max-w-7xl mx-auto w-full">
          <div className="flex items-center gap-1.5 font-medium">
            <span className="inline-block w-2 h-2 rounded-full bg-amber-500" />
            <span className="text-white font-semibold">Government of India</span>
            <span className="text-slate-500">|</span>
            <span>Ministry of Statistics & Programme Implementation (MoSPI)</span>
          </div>
          <div className="ml-auto flex items-center gap-4 text-[11px]">
            <span className="hidden md:inline text-slate-400">Mission Karmayogi Digital Learning Portal</span>
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1 text-slate-300 hover:text-white font-medium bg-slate-800 px-2 py-0.5 rounded cursor-pointer transition-colors"
            >
              <Languages className="h-3 w-3 text-amber-400" />
              <span>{language === "en" ? "हिन्दी (HI)" : "English (EN)"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <a href={user ? "/home" : "/"} className="flex items-center gap-3 group">
          <div className="h-10 w-10 rounded-lg bg-slate-900 flex items-center justify-center text-amber-400 shadow-sm border border-slate-800">
            <Award className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-lg font-bold text-slate-900 tracking-tight">
                {t("nav.brand")}
              </span>
              <span className="text-[10px] uppercase font-bold bg-amber-100 text-amber-800 px-1.5 py-0.2 rounded border border-amber-200">
                MoSPI
              </span>
            </div>
            <p className="text-[10px] text-slate-500 font-medium leading-none">
              {t("nav.subBrand")}
            </p>
          </div>
        </a>

        {/* Desktop Links */}
        <nav className="hidden md:flex items-center gap-1">
          {user && (
            <a
              href="/home"
              className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                pathname === "/home"
                  ? "bg-slate-100 text-slate-900 font-semibold"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
              }`}
            >
              Home
            </a>
          )}

          <a
            href="/discover"
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive("/discover") || isActive("/courses")
                ? "bg-slate-100 text-slate-900 font-semibold"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
            }`}
          >
            <Compass className="h-4 w-4 text-slate-500" />
            {t("nav.discover")}
          </a>

          {user && (
            <a
              href="/my-learning"
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive("/my-learning") || isActive("/progress")
                  ? "bg-slate-100 text-slate-900 font-semibold"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
              }`}
            >
              <BookOpen className="h-4 w-4 text-slate-500" />
              {t("nav.myLearning")}
            </a>
          )}

          {isAdmin && (
            <a
              href="/admin"
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive("/admin")
                  ? "bg-amber-50 text-amber-900 font-semibold border border-amber-200"
                  : "text-amber-800 hover:bg-amber-50/50"
              }`}
            >
              <ShieldAlert className="h-4 w-4 text-amber-600" />
              {t("nav.admin")}
            </a>
          )}
        </nav>

        {/* Right Section: Auth & Profile */}
        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <div className="relative">
              <button
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                className="flex items-center gap-2.5 p-1.5 rounded-full hover:bg-slate-100 border border-slate-200 transition-colors cursor-pointer"
              >
                <div className="h-8 w-8 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-xs">
                  {user.full_name?.charAt(0) || "U"}
                </div>
                <div className="text-left pr-2">
                  <p className="text-xs font-semibold text-slate-900 leading-tight">
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
                    <p className="text-xs font-semibold text-slate-900">{user.full_name}</p>
                    <p className="text-[11px] text-slate-500 truncate">{user.email}</p>
                  </div>
                  <a
                    href="/profile"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 hover:text-slate-900"
                  >
                    <User className="h-3.5 w-3.5 text-slate-400" />
                    {t("nav.profile")}
                  </a>
                  <a
                    href="/profile?tab=settings"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 hover:text-slate-900"
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
            <div className="flex items-center gap-2">
              <a href="/login">
                <Button variant="ghost" size="sm">
                  {t("nav.login")}
                </Button>
              </a>
              <a href="/register">
                <Button variant="default" size="sm" className="bg-slate-900 hover:bg-slate-800">
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
            className="p-2 rounded-lg text-slate-600 hover:bg-slate-100"
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
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </a>
          )}
          <a
            href="/discover"
            className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
            onClick={() => setMobileMenuOpen(false)}
          >
            {t("nav.discover")}
          </a>
          {user && (
            <a
              href="/my-learning"
              className="block px-3 py-2 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t("nav.myLearning")}
            </a>
          )}
          {isAdmin && (
            <a
              href="/admin"
              className="block px-3 py-2 rounded-lg text-base font-medium text-amber-800 hover:bg-amber-50"
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
                  <Button variant="outline" className="w-full">
                    {t("nav.login")}
                  </Button>
                </a>
                <a href="/register" className="w-full">
                  <Button variant="default" className="w-full bg-slate-900">
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
