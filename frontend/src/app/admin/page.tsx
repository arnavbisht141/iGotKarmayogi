"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  ShieldAlert,
  Users,
  BookOpen,
  Award,
  TrendingUp,
  UserPlus,
  PlusCircle,
  AlertTriangle,
  CheckCircle2,
  Check,
  Search,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { fetchApi } from "@/lib/api";
import { useAuth } from "@/lib/auth/AuthContext";

export default function AdminDashboardPage() {
  const router = useRouter();
  const { user, isAdmin, isLoading } = useAuth();

  const [adminData, setAdminData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Course Assignment Modal state
  const [assignModalOpen, setAssignModalOpen] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(null);
  const [assignSuccess, setAssignSuccess] = useState<string | null>(null);
  const [assigning, setAssigning] = useState(false);

  // New Course Modal state
  const [courseModalOpen, setCourseModalOpen] = useState(false);
  const [newCourse, setNewCourse] = useState({
    title: "",
    overview: "",
    instructor: "",
    organization: "MoSPI / NSSTA",
    duration_hours: 5.0,
    difficulty: "intermediate",
    category: "Sample Surveys",
    source: "internal",
  });
  const [creatingCourse, setCreatingCourse] = useState(false);

  const loadAdminData = () => {
    setLoading(true);
    fetchApi("/admin/overview")
      .then((data) => setAdminData(data))
      .catch((err) => console.error("Error loading admin data:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!isLoading) {
      if (!user || user.role !== "admin") {
        router.push("/home");
        return;
      }
      loadAdminData();
    }
  }, [user, isAdmin, isLoading, router]);

  const handleAssignCourse = async () => {
    if (!selectedUserId || !selectedCourseId) return;
    setAssigning(true);
    try {
      const res = await fetchApi("/admin/assign-course", {
        method: "POST",
        body: JSON.stringify({
          user_id: selectedUserId,
          course_id: selectedCourseId,
        }),
      });

      setAssignSuccess(res.message);
      loadAdminData();
      setTimeout(() => {
        setAssignSuccess(null);
        setAssignModalOpen(false);
      }, 2000);
    } catch (err: any) {
      alert("Failed to assign course: " + err.message);
    } finally {
      setAssigning(false);
    }
  };

  const handleCreateCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreatingCourse(true);
    try {
      await fetchApi("/admin/courses", {
        method: "POST",
        body: JSON.stringify(newCourse),
      });

      setCourseModalOpen(false);
      loadAdminData();
      alert("Course created successfully in catalogue!");
    } catch (err: any) {
      alert("Error creating course: " + err.message);
    } finally {
      setCreatingCourse(false);
    }
  };

  if (loading || !adminData) {
    return (
      <div className="min-h-[75vh] flex items-center justify-center">
        <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
      </div>
    );
  }

  const summary = adminData.summary || {};
  const usersList = adminData.users || [];
  const courseAnalytics = adminData.course_analytics || [];
  const strugglingQuestions = adminData.struggling_questions || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Banner */}
      <div className="rounded-2xl bg-white border border-slate-200 p-6 sm:p-8 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="h-2 w-2 rounded-full bg-rose-500" />
            <Badge variant="saffron" className="text-[10px]">Administrative Authority</Badge>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <ShieldAlert className="h-7 w-7 text-amber-600" />
            Capacity Building Admin Console
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Supervise cadre training progress, assign official courses, and audit question difficulty
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            size="sm"
            onClick={() => setCourseModalOpen(true)}
            className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold gap-1.5"
          >
            <PlusCircle className="h-4 w-4" /> Add New Course
          </Button>
        </div>
      </div>

      {/* Aggregate Metrics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-5">
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardContent className="p-5 flex items-center gap-3.5">
            <div className="h-11 w-11 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center">
              <Users className="h-6 w-6" />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-900">{summary.total_users}</p>
              <p className="text-[11px] text-slate-500 font-medium">Registered Officials</p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 bg-white shadow-xs">
          <CardContent className="p-5 flex items-center gap-3.5">
            <div className="h-11 w-11 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center">
              <BookOpen className="h-6 w-6" />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-900">{summary.total_courses}</p>
              <p className="text-[11px] text-slate-500 font-medium">Active Curricula</p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 bg-white shadow-xs">
          <CardContent className="p-5 flex items-center gap-3.5">
            <div className="h-11 w-11 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <Award className="h-6 w-6" />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-900">{summary.completion_rate_percent}%</p>
              <p className="text-[11px] text-slate-500 font-medium">Cadre Completion Rate</p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 bg-white shadow-xs">
          <CardContent className="p-5 flex items-center gap-3.5">
            <div className="h-11 w-11 rounded-xl bg-slate-100 text-slate-800 flex items-center justify-center">
              <TrendingUp className="h-6 w-6" />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-900">{summary.overall_pass_rate_percent}%</p>
              <p className="text-[11px] text-slate-500 font-medium">Assessment Pass Rate</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Row 2: User Management & Course Assignment Table */}
      <Card className="border-slate-200 bg-white shadow-xs overflow-hidden">
        <CardHeader className="border-b border-slate-100 p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Users className="h-4 w-4 text-amber-600" />
              Civil Servants Cadre Management & Assignment
            </CardTitle>
            <CardDescription className="text-xs">
              Monitor active enrollments per official and assign mandatory statistical training
            </CardDescription>
          </div>
        </CardHeader>
        <CardContent className="p-0 overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/80 border-b border-slate-200 text-slate-600 font-semibold uppercase text-[10px] tracking-wider">
              <tr>
                <th className="px-6 py-3">Official</th>
                <th className="px-6 py-3">Department & Role</th>
                <th className="px-6 py-3">Onboarded</th>
                <th className="px-6 py-3">Enrolled Courses</th>
                <th className="px-6 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {usersList.map((u: any) => (
                <tr key={u.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-6 py-4">
                    <p className="font-bold text-slate-900">{u.full_name}</p>
                    <p className="text-[11px] text-slate-400">{u.email}</p>
                  </td>
                  <td className="px-6 py-4">
                    <p className="font-semibold text-slate-800">{u.designation}</p>
                    <p className="text-[11px] text-slate-500 truncate max-w-xs">{u.department}</p>
                  </td>
                  <td className="px-6 py-4">
                    {u.onboarding_completed ? (
                      <Badge variant="success" className="text-[10px]">Completed ✓</Badge>
                    ) : (
                      <Badge variant="secondary" className="text-[10px]">Pending</Badge>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      {u.courses.length > 0 ? (
                        u.courses.map((uc: any, idx: number) => (
                          <div key={idx} className="flex items-center gap-2 text-[11px]">
                            <span className="font-medium text-slate-800 truncate max-w-[180px]">
                              {uc.title}
                            </span>
                            <span className="text-slate-400">({uc.progress_percent}%)</span>
                          </div>
                        ))
                      ) : (
                        <span className="text-slate-400 text-[11px]">No active courses</span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setSelectedUserId(u.id);
                        setSelectedCourseId(courseAnalytics[0]?.id || 1);
                        setAssignModalOpen(true);
                      }}
                      className="text-xs h-8"
                    >
                      Assign Course
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>

      {/* Row 3: Question Difficulty Analysis (Struggling questions where learners fail) */}
      <Card className="border-slate-200 bg-white shadow-xs">
        <CardHeader className="border-b border-slate-100 p-6">
          <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-amber-600" />
            Assessment Question Difficulty Analytics
          </CardTitle>
          <CardDescription className="text-xs">
            Pinpoints exact methodology concepts where officials struggle across nationwide exams
          </CardDescription>
        </CardHeader>
        <CardContent className="p-6">
          <div className="space-y-3">
            {strugglingQuestions.map((sq: any) => (
              <div
                key={sq.question_id}
                className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
              >
                <div>
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">
                    {sq.assessment_title}
                  </span>
                  <p className="font-semibold text-slate-900 mt-0.5">{sq.question_text}</p>
                </div>
                <div className="flex items-center gap-4 shrink-0">
                  <div className="text-right">
                    <span className="text-sm font-bold text-slate-900">{sq.accuracy_percent}%</span>
                    <span className="text-[10px] text-slate-500 block">Cadre Accuracy</span>
                  </div>
                  <Badge
                    variant={sq.accuracy_percent < 50 ? "default" : "secondary"}
                    className="text-[10px]"
                  >
                    {sq.difficulty_tag}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Assignment Modal */}
      <Dialog open={assignModalOpen} onOpenChange={setAssignModalOpen}>
        <DialogContent className="max-w-md p-6 bg-white">
          <DialogHeader>
            <DialogTitle>Assign Course to Official</DialogTitle>
            <DialogDescription className="text-xs">
              Assign accredited training to an officer. The course will automatically appear in their active learning queue.
            </DialogDescription>
          </DialogHeader>

          {assignSuccess ? (
            <div className="py-6 text-center text-xs font-semibold text-emerald-800 space-y-2">
              <CheckCircle2 className="h-8 w-8 text-emerald-600 mx-auto" />
              <p>{assignSuccess}</p>
            </div>
          ) : (
            <div className="space-y-4 pt-2 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Select Official</label>
                <select
                  value={selectedUserId || ""}
                  onChange={(e) => setSelectedUserId(parseInt(e.target.value))}
                  className="w-full rounded-lg border border-slate-300 p-2 text-xs bg-white text-slate-900"
                >
                  {usersList.map((u: any) => (
                    <option key={u.id} value={u.id}>
                      {u.full_name} ({u.designation || u.email})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Select Training Course</label>
                <select
                  value={selectedCourseId || ""}
                  onChange={(e) => setSelectedCourseId(parseInt(e.target.value))}
                  className="w-full rounded-lg border border-slate-300 p-2 text-xs bg-white text-slate-900"
                >
                  {courseAnalytics.map((c: any) => (
                    <option key={c.id} value={c.id}>
                      {c.title} ({c.organization})
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
                <Button variant="outline" size="sm" onClick={() => setAssignModalOpen(false)}>
                  Cancel
                </Button>
                <Button
                  size="sm"
                  onClick={handleAssignCourse}
                  disabled={assigning}
                  className="bg-slate-900 text-white"
                >
                  {assigning ? "Assigning..." : "Confirm Assignment"}
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* New Course Modal */}
      <Dialog open={courseModalOpen} onOpenChange={setCourseModalOpen}>
        <DialogContent className="max-w-lg p-6 bg-white">
          <DialogHeader>
            <DialogTitle>Create New Course Curriculum</DialogTitle>
            <DialogDescription className="text-xs">
              Add a new course to the iGOT Karmayogi national statistical catalogue
            </DialogDescription>
          </DialogHeader>

          <form onSubmit={handleCreateCourse} className="space-y-3 pt-2 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Course Title</label>
              <Input
                required
                value={newCourse.title}
                onChange={(e) => setNewCourse({ ...newCourse, title: e.target.value })}
                placeholder="e.g. Sustainable Development Goals (SDG) Statistical Indicators"
                className="text-xs"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Overview Description</label>
              <textarea
                required
                rows={2}
                value={newCourse.overview}
                onChange={(e) => setNewCourse({ ...newCourse, overview: e.target.value })}
                placeholder="Comprehensive guide on SDG indicator tracking..."
                className="w-full rounded-lg border border-slate-300 p-2 text-xs"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Instructor / Faculty</label>
                <Input
                  required
                  value={newCourse.instructor}
                  onChange={(e) => setNewCourse({ ...newCourse, instructor: e.target.value })}
                  placeholder="Dr. S. K. Roy"
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Accredited Body</label>
                <Input
                  required
                  value={newCourse.organization}
                  onChange={(e) => setNewCourse({ ...newCourse, organization: e.target.value })}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Duration (Hours)</label>
                <Input
                  type="number"
                  step="0.5"
                  value={newCourse.duration_hours}
                  onChange={(e) => setNewCourse({ ...newCourse, duration_hours: parseFloat(e.target.value) || 4 })}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Provider Source</label>
                <select
                  value={newCourse.source}
                  onChange={(e) => setNewCourse({ ...newCourse, source: e.target.value })}
                  className="w-full rounded-lg border border-slate-300 p-2 text-xs bg-white"
                >
                  <option value="internal">Internal MoSPI</option>
                  <option value="external">External (ISTM/DoPT)</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
              <Button variant="outline" size="sm" type="button" onClick={() => setCourseModalOpen(false)}>
                Cancel
              </Button>
              <Button size="sm" type="submit" disabled={creatingCourse} className="bg-slate-900 text-white">
                {creatingCourse ? "Publishing..." : "Publish Course to Catalogue"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
