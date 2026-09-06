"use client";

import React, { useEffect, useState } from "react";
import {
  BookOpen,
  Award,
  PlayCircle,
  CheckCircle2,
  Calendar,
  Sparkles,
  ArrowRight,
  TrendingUp,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { CertificateModal } from "@/components/certificate/CertificateModal";
import { fetchApi } from "@/lib/api";
import { CertificateItem } from "@/lib/types";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";

export default function MyLearningPage() {
  const { user } = useAuth();
  const { t } = useI18n();
  const [activeTab, setActiveTab] = useState<"in_progress" | "completed" | "skills" | "planned">("in_progress");
  const [profileData, setProfileData] = useState<any>(null);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Certificate Modal
  const [selectedCert, setSelectedCert] = useState<CertificateItem | null>(null);
  const [certModalOpen, setCertModalOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      fetchApi("/profile/"),
      fetchApi("/dashboard/summary"),
    ])
      .then(([prof, dash]) => {
        setProfileData(prof);
        setDashboardData(dash);
      })
      .catch((err) => console.error("Error loading learning data:", err))
      .finally(() => setLoading(false));
  }, []);

  const openCertificate = (cert: CertificateItem) => {
    setSelectedCert(cert);
    setCertModalOpen(true);
  };

  if (loading) {
    return (
      <div className="min-h-[75vh] flex items-center justify-center">
        <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
      </div>
    );
  }

  const continueCourse = dashboardData?.continue_learning;
  const certificates: CertificateItem[] = profileData?.certificates || [];
  const skills = profileData?.skills || [];
  const plannedCourses = dashboardData?.future_planned || [];
  const progressStats = dashboardData?.my_learning_progress || { in_progress_count: 1, completed_count: 0 };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Banner */}
      <div className="rounded-2xl bg-white border border-slate-200 p-6 sm:p-8 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <Badge variant="saffron" className="mb-2">Official Learning Transcript</Badge>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              {t("nav.myLearning")} & Records
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Personalized training ledger, competency growth, and verified credentials
            </p>
          </div>

          <div className="flex items-center gap-4 text-center">
            <div className="px-4 py-2 bg-slate-50 rounded-xl border border-slate-100">
              <p className="text-xl font-bold text-slate-900">{progressStats.in_progress_count}</p>
              <p className="text-[10px] text-slate-500 uppercase font-semibold">In Progress</p>
            </div>
            <div className="px-4 py-2 bg-emerald-50 rounded-xl border border-emerald-100">
              <p className="text-xl font-bold text-emerald-800">{progressStats.completed_count}</p>
              <p className="text-[10px] text-emerald-700 uppercase font-semibold">Completed</p>
            </div>
            <div className="px-4 py-2 bg-indigo-50 rounded-xl border border-indigo-100">
              <p className="text-xl font-bold text-indigo-800">{skills.length}</p>
              <p className="text-[10px] text-indigo-700 uppercase font-semibold">Skills</p>
            </div>
          </div>
        </div>

        {/* Tab Controls (Miro Section 7: In Progress, Completed, Skills, Planned) */}
        <div className="mt-8 flex border-b border-slate-200 gap-6 text-xs font-semibold">
          <button
            onClick={() => setActiveTab("in_progress")}
            className={`pb-3 transition-colors cursor-pointer flex items-center gap-1.5 ${
              activeTab === "in_progress"
                ? "border-b-2 border-slate-900 text-slate-900 font-bold"
                : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <PlayCircle className="h-4 w-4 text-amber-600" />
            In Progress ({progressStats.in_progress_count})
          </button>

          <button
            onClick={() => setActiveTab("completed")}
            className={`pb-3 transition-colors cursor-pointer flex items-center gap-1.5 ${
              activeTab === "completed"
                ? "border-b-2 border-slate-900 text-slate-900 font-bold"
                : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <Award className="h-4 w-4 text-emerald-600" />
            Completed & Certificates ({certificates.length})
          </button>

          <button
            onClick={() => setActiveTab("skills")}
            className={`pb-3 transition-colors cursor-pointer flex items-center gap-1.5 ${
              activeTab === "skills"
                ? "border-b-2 border-slate-900 text-slate-900 font-bold"
                : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <Sparkles className="h-4 w-4 text-indigo-600" />
            Acquired Competencies ({skills.length})
          </button>

          <button
            onClick={() => setActiveTab("planned")}
            className={`pb-3 transition-colors cursor-pointer flex items-center gap-1.5 ${
              activeTab === "planned"
                ? "border-b-2 border-slate-900 text-slate-900 font-bold"
                : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <Calendar className="h-4 w-4 text-slate-500" />
            Planned Courses ({plannedCourses.length})
          </button>
        </div>
      </div>

      {/* Tab 1: In Progress Courses */}
      {activeTab === "in_progress" && (
        <div className="space-y-4">
          {continueCourse ? (
            <Card className="border-slate-200 bg-white shadow-xs">
              <CardContent className="p-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <Badge variant="success" className="mb-1 text-[10px]">Active Enrolled Module</Badge>
                    <h3 className="text-lg font-bold text-slate-900">
                      {continueCourse.course_title}
                    </h3>
                    <p className="text-xs text-slate-500">
                      Current: {continueCourse.current_module} • {continueCourse.current_lesson}
                    </p>
                  </div>
                  <a href={`/learn/${continueCourse.course_id}`}>
                    <Button size="sm" className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold px-5">
                      Resume Course <ArrowRight className="h-3.5 w-3.5 ml-1" />
                    </Button>
                  </a>
                </div>

                <div className="mt-5 space-y-1.5 pt-4 border-t border-slate-100">
                  <div className="flex justify-between text-xs font-bold text-slate-700">
                    <span>Progress: {continueCourse.progress_percent}%</span>
                    <span>Accredited by {continueCourse.organization}</span>
                  </div>
                  <Progress value={continueCourse.progress_percent} indicatorClassName="bg-amber-600" />
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="py-16 text-center bg-white rounded-2xl border border-slate-200">
              <BookOpen className="h-10 w-10 text-slate-400 mx-auto mb-2" />
              <h3 className="text-sm font-bold text-slate-900">No courses in progress</h3>
              <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                Explore the national statistical catalogue and enroll in foundational training.
              </p>
              <a href="/discover">
                <Button size="sm" className="mt-4 bg-slate-900 text-xs">
                  Discover Courses
                </Button>
              </a>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Completed Courses & Verified Certificates */}
      {activeTab === "completed" && (
        <div className="space-y-4">
          {certificates.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {certificates.map((cert) => (
                <Card key={cert.certificate_id} className="border-slate-200 bg-white shadow-xs flex flex-col justify-between">
                  <CardHeader className="pb-3 border-b border-slate-100">
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <Badge variant="success" className="text-[10px]">Completed</Badge>
                      <span className="text-[11px] font-mono text-slate-400">{cert.certificate_id}</span>
                    </div>
                    <CardTitle className="text-base font-bold text-slate-900">
                      {cert.course_title}
                    </CardTitle>
                    <CardDescription className="text-xs">
                      {cert.organization} • Completed on {cert.issued_date}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-5 flex items-center justify-between">
                    <div>
                      <span className="text-xs text-slate-500 block">Assessment Score</span>
                      <span className="text-base font-extrabold text-emerald-800">{cert.score_percent}%</span>
                    </div>
                    <Button
                      size="sm"
                      onClick={() => openCertificate(cert)}
                      className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold gap-1.5"
                    >
                      <Award className="h-4 w-4 text-amber-400" /> View Certificate
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="py-16 text-center bg-white rounded-2xl border border-slate-200">
              <Award className="h-10 w-10 text-slate-400 mx-auto mb-2" />
              <h3 className="text-sm font-bold text-slate-900">No completed courses yet</h3>
              <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                Once you achieve 70% or higher on an end-of-course assessment, your official verifiable credentials appear here.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Tab 3: Acquired Competencies */}
      {activeTab === "skills" && (
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100">
            <CardTitle className="text-base font-bold text-slate-900">
              Verified Civil Service Competencies
            </CardTitle>
            <CardDescription className="text-xs">
              Demonstrated proficiencies earned through completed official assessments
            </CardDescription>
          </CardHeader>
          <CardContent className="p-6">
            {skills.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {skills.map((s: any) => (
                  <div
                    key={s.id}
                    className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-1.5"
                  >
                    <Badge variant="saffron" className="text-[10px]">{s.category}</Badge>
                    <h4 className="text-xs font-bold text-slate-900">{s.name}</h4>
                    <p className="text-[11px] text-slate-500">
                      Earned via {s.source_course}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 text-center py-8">
                No competencies recorded yet. Complete course assessments to earn certified skill badges.
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Tab 4: Planned Courses */}
      {activeTab === "planned" && (
        <div className="space-y-4">
          {plannedCourses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {plannedCourses.map((pc: any) => (
                <Card key={pc.id} className="border-slate-200 bg-white shadow-xs">
                  <CardContent className="p-5 flex items-center justify-between">
                    <div>
                      <Badge variant="secondary" className="text-[10px] mb-1">Target: {pc.planned_for}</Badge>
                      <h4 className="text-sm font-bold text-slate-900">{pc.course_title}</h4>
                      <p className="text-xs text-slate-500 mt-0.5">{pc.organization} • {pc.duration_hours}h</p>
                    </div>
                    <a href={`/courses/${pc.course_id}`}>
                      <Button variant="outline" size="sm" className="text-xs">
                        View Details
                      </Button>
                    </a>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="py-16 text-center bg-white rounded-2xl border border-slate-200">
              <Calendar className="h-10 w-10 text-slate-400 mx-auto mb-2" />
              <h3 className="text-sm font-bold text-slate-900">No planned courses in queue</h3>
              <p className="text-xs text-slate-500 mt-1">Browse the catalogue to queue upcoming coursework.</p>
            </div>
          )}
        </div>
      )}

      {/* Certificate Modal */}
      <CertificateModal
        certificate={selectedCert}
        open={certModalOpen}
        onClose={() => setCertModalOpen(false)}
      />
    </div>
  );
}
