"use client";

import React, { useEffect, useState } from "react";
import {
  Compass,
  ArrowRight,
  ShieldCheck,
  Award,
  CheckCircle,
  BarChart3,
  Building2,
  FileCheck2,
  BookOpen,
  Sparkles,
  Users,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { fetchApi } from "@/lib/api";
import { CoursePreview } from "@/lib/types";
import { useAuth } from "@/lib/auth/AuthContext";
import { useRouter } from "next/navigation";

export default function EntryLandingPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [courses, setCourses] = useState<CoursePreview[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // If user is already logged in, redirect directly to home
    if (user) {
      router.push("/home");
      return;
    }

    fetchApi<{ courses: CoursePreview[] }>("/discover/courses?sort=popular")
      .then((data) => {
        setCourses(data.courses.slice(0, 4));
      })
      .catch((err) => console.error("Failed loading preview courses:", err))
      .finally(() => setLoading(false));
  }, [user, router]);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-slate-950 text-white py-20 lg:py-28 border-b border-slate-800">
        {/* Subtle decorative grid */}
        <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:20px_20px] opacity-40" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-700 mb-6 text-xs text-slate-300">
            <span className="h-2 w-2 rounded-full bg-amber-500" />
            <span>Mission Karmayogi • India's National Public Service Learning Infrastructure</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white max-w-4xl leading-tight">
            AI-Enabled Skill Intelligence for India&apos;s Civil Servants
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-2xl leading-relaxed">
            Delivering standardized, accredited professional competencies for the Official Statistical System (MoSPI), Central Ministries, and public administrators.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <a href="/login">
              <Button size="lg" className="bg-amber-600 hover:bg-amber-700 text-white font-semibold px-8 shadow-md">
                Official Sign In <ArrowRight className="h-4 w-4 ml-1" />
              </Button>
            </a>
            <a href="/discover">
              <Button size="lg" variant="outline" className="border-slate-700 text-slate-200 hover:bg-slate-900 px-8">
                <Compass className="h-4 w-4 mr-2 text-amber-400" /> Explore Courses
              </Button>
            </a>
          </div>

          {/* Quick Metrics */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl w-full border-t border-slate-800 pt-8 text-slate-300">
            <div>
              <p className="text-2xl font-bold text-white">40,000+</p>
              <p className="text-xs text-slate-400">Civil Servants Trained</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">100%</p>
              <p className="text-xs text-slate-400">MoSPI Standardized</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">UN-NQAF</p>
              <p className="text-xs text-slate-400">Quality Frameworks</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">Verifiable</p>
              <p className="text-xs text-slate-400">Government Credentials</p>
            </div>
          </div>
        </div>
      </section>

      {/* About Platform Section (Miro: About Platform) */}
      <section id="about" className="py-16 bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <Badge variant="saffron" className="mb-2">About The Initiative</Badge>
            <h2 className="text-3xl font-bold text-slate-900 tracking-tight">
              A Competency-Driven Learning Paradigm
            </h2>
            <p className="mt-3 text-slate-600 text-sm sm:text-base">
              Moving the civil service from rules-based training to roles-based competency mastery, aligned with the National Programme for Civil Services Capacity Building (NPCSCB).
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="border-slate-200 bg-slate-50/50">
              <CardContent className="p-6">
                <div className="h-12 w-12 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center mb-4">
                  <BarChart3 className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">Statistical Integrity</h3>
                <p className="text-sm text-slate-600 leading-relaxed">
                  Rigorous curricula on National Sample Surveys (NSS), Consumer Price Index (CPI), and National Accounts compilation.
                </p>
              </CardContent>
            </Card>

            <Card className="border-slate-200 bg-slate-50/50">
              <CardContent className="p-6">
                <div className="h-12 w-12 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center mb-4">
                  <FileCheck2 className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">Certified Assessments</h3>
                <p className="text-sm text-slate-600 leading-relaxed">
                  Every course concludes with a verified MCQ assessment with minimum 70% passing threshold, awarding official credentials.
                </p>
              </CardContent>
            </Card>

            <Card className="border-slate-200 bg-slate-50/50">
              <CardContent className="p-6">
                <div className="h-12 w-12 rounded-lg bg-slate-900 text-amber-400 flex items-center justify-center mb-4">
                  <Sparkles className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">AI-Orchestrated Assistant</h3>
                <p className="text-sm text-slate-600 leading-relaxed">
                  Built-in LangGraph Copilot providing immediate civil service guidance, regulatory clarifications, and methodology lookups.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Explore Courses Section (Miro: Explore Courses - Unauthenticated Preview) */}
      <section id="explore" className="py-16 bg-slate-50 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10">
            <div>
              <Badge variant="secondary" className="mb-2">Course Catalogue Preview</Badge>
              <h2 className="text-3xl font-bold text-slate-900 tracking-tight">
                Accredited Government Training Modules
              </h2>
              <p className="mt-2 text-sm text-slate-600">
                Preview courses offered by NSSO, CSO, NSSTA, and accredited institutes like ISTM.
              </p>
            </div>
            <a href="/discover" className="mt-4 sm:mt-0 inline-flex items-center text-sm font-semibold text-slate-900 hover:text-amber-700">
              View Complete Catalogue <ArrowRight className="h-4 w-4 ml-1" />
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {courses.map((course) => (
              <Card key={course.id} className="flex flex-col h-full bg-white hover:border-slate-400 transition-all">
                <div className="p-5 flex-1 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-3">
                      <Badge variant={course.source === "external" ? "external" : "secondary"}>
                        {course.source === "external" ? "ISTM Accredited" : "MoSPI Internal"}
                      </Badge>
                      <span className="text-xs text-slate-500 font-medium">{course.duration_hours} hrs</span>
                    </div>

                    <h4 className="font-bold text-slate-900 text-base line-clamp-2 mb-2">
                      {course.title}
                    </h4>

                    <p className="text-xs text-slate-500 line-clamp-3 mb-4 leading-relaxed">
                      {course.overview}
                    </p>
                  </div>

                  <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
                    <span className="font-semibold text-slate-800 truncate max-w-[140px]">
                      {course.organization}
                    </span>
                    <a
                      href={`/courses/${course.id}`}
                      className="text-amber-700 hover:text-amber-800 font-semibold inline-flex items-center"
                    >
                      Overview <ArrowRight className="h-3 w-3 ml-0.5" />
                    </a>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works Section (Miro: How it Works) */}
      <section id="how-it-works" className="py-16 bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <Badge variant="outline" className="mb-2">Operational Roadmap</Badge>
            <h2 className="text-3xl font-bold text-slate-900 tracking-tight">
              How the Karmayogi Learning Journey Works
            </h2>
            <p className="mt-3 text-slate-600 text-sm">
              A structured 4-step progression from role onboarding to recognized certification.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="relative flex flex-col items-center text-center p-6 bg-slate-50 rounded-xl border border-slate-200">
              <span className="h-9 w-9 rounded-full bg-slate-900 text-white font-bold text-sm flex items-center justify-center mb-4">
                1
              </span>
              <h4 className="font-bold text-slate-900 mb-1">Onboard Role</h4>
              <p className="text-xs text-slate-600">
                Specify your ministry, department, cadre, and official assignments during 5-step onboarding.
              </p>
            </div>

            <div className="relative flex flex-col items-center text-center p-6 bg-slate-50 rounded-xl border border-slate-200">
              <span className="h-9 w-9 rounded-full bg-slate-900 text-white font-bold text-sm flex items-center justify-center mb-4">
                2
              </span>
              <h4 className="font-bold text-slate-900 mb-1">Discover & Study</h4>
              <p className="text-xs text-slate-600">
                Consume video lectures, CAPI field simulation labs, and in-lesson concept practice tasks.
              </p>
            </div>

            <div className="relative flex flex-col items-center text-center p-6 bg-slate-50 rounded-xl border border-slate-200">
              <span className="h-9 w-9 rounded-full bg-slate-900 text-white font-bold text-sm flex items-center justify-center mb-4">
                3
              </span>
              <h4 className="font-bold text-slate-900 mb-1">Pass Assessment</h4>
              <p className="text-xs text-slate-600">
                Complete objective MCQ tests with immediate correctness feedback and answer breakdowns.
              </p>
            </div>

            <div className="relative flex flex-col items-center text-center p-6 bg-slate-50 rounded-xl border border-slate-200">
              <span className="h-9 w-9 rounded-full bg-slate-900 text-white font-bold text-sm flex items-center justify-center mb-4">
                4
              </span>
              <h4 className="font-bold text-slate-900 mb-1">Earn Certificate</h4>
              <p className="text-xs text-slate-600">
                Receive verifiable digital credentials stored in your permanent civil service profile.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Bar */}
      <section className="bg-slate-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
          <div>
            <h3 className="text-2xl font-bold">Ready to advance your official statistical expertise?</h3>
            <p className="text-sm text-slate-400 mt-1">
              Sign in with your official government email or create your employee credentials today.
            </p>
          </div>
          <div className="flex gap-3">
            <a href="/login">
              <Button variant="outline" className="text-white border-slate-700 hover:bg-slate-800">
                Sign In
              </Button>
            </a>
            <a href="/register">
              <Button variant="saffron">
                Register New Official
              </Button>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
