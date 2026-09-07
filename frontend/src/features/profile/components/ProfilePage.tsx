"use client";

import React, { useEffect, useState } from "react";
import {
  User,
  ShieldCheck,
  Settings,
  Award,
  CheckCircle2,
  Save,
  Languages,
  Moon,
  Sun,
  Target,
  Briefcase,
  GraduationCap,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { fetchApi } from "@/lib/api";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const { language, setLanguage, t } = useI18n();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  const [formData, setFormData] = useState({
    full_name: "",
    phone: "",
    bio: "",
    education: "",
    work_experience_years: 0,
    prior_training: "",
    designation: "",
    department: "",
    job_role: "",
    current_assignment: "",
    areas_of_interest: [] as string[],
    language_pref: "en",
    appearance_pref: "light",
    daily_goal_minutes: 30,
  });

  useEffect(() => {
    fetchApi("/profile/")
      .then((data) => {
        setFormData({
          full_name: data.full_name || "",
          phone: data.profile.phone || "",
          bio: data.profile.bio || "",
          education: data.profile.education || "",
          work_experience_years: data.profile.work_experience_years || 0,
          prior_training: data.profile.prior_training || "",
          designation: data.profile.designation || "",
          department: data.profile.department || "",
          job_role: data.profile.job_role || "",
          current_assignment: data.profile.current_assignment || "",
          areas_of_interest: data.profile.areas_of_interest || [],
          language_pref: data.profile.language_pref || "en",
          appearance_pref: data.profile.appearance_pref || "light",
          daily_goal_minutes: data.profile.daily_goal_minutes || 30,
        });
      })
      .catch((err) => console.error("Error loading profile:", err))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSavedSuccess(false);

    try {
      await fetchApi("/profile/", {
        method: "PUT",
        body: JSON.stringify(formData),
      });

      updateUser({ full_name: formData.full_name });
      setLanguage(formData.language_pref as "en" | "hi");
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err: any) {
      alert("Failed to update profile: " + err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="rounded-2xl bg-white border border-slate-200 p-6 sm:p-8 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="h-16 w-16 rounded-2xl bg-slate-900 text-white flex items-center justify-center text-2xl font-bold border border-slate-800 shadow-sm">
            {formData.full_name?.charAt(0) || "U"}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-slate-900">{formData.full_name}</h1>
              <Badge variant="saffron" className="text-[10px] capitalize">
                {user?.role} Official
              </Badge>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              {formData.designation} • {formData.department}
            </p>
          </div>
        </div>

        {savedSuccess && (
          <div className="p-2.5 px-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            Profile Updated Successfully
          </div>
        )}
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Personal & Professional Info */}
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100">
            <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Briefcase className="h-4 w-4 text-amber-600" />
              Official Role & Organizational Placement
            </CardTitle>
            <CardDescription className="text-xs">
              Sourced from your 5-step onboarding; fully editable as responsibilities evolve
            </CardDescription>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Full Name
                </label>
                <Input
                  type="text"
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Phone / WhatsApp
                </label>
                <Input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Official Designation
                </label>
                <Input
                  type="text"
                  value={formData.designation}
                  onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Ministry / Department
                </label>
                <Input
                  type="text"
                  value={formData.department}
                  onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Job Role
                </label>
                <Input
                  type="text"
                  value={formData.job_role}
                  onChange={(e) => setFormData({ ...formData, job_role: e.target.value })}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Years in Service
                </label>
                <Input
                  type="number"
                  value={formData.work_experience_years}
                  onChange={(e) => setFormData({ ...formData, work_experience_years: parseInt(e.target.value) || 0 })}
                  className="text-xs"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Current Active Project / Assignment
              </label>
              <Input
                type="text"
                value={formData.current_assignment}
                onChange={(e) => setFormData({ ...formData, current_assignment: e.target.value })}
                className="text-xs"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Academic Qualifications & Prior Training
              </label>
              <Input
                type="text"
                value={formData.education}
                onChange={(e) => setFormData({ ...formData, education: e.target.value })}
                className="text-xs"
              />
            </div>
          </CardContent>
        </Card>

        {/* Section 2: Settings & Preferences */}
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100">
            <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Settings className="h-4 w-4 text-slate-600" />
              {t("nav.settings")} & Preferences
            </CardTitle>
            <CardDescription className="text-xs">
              Configure interface language, appearance, and study targets
            </CardDescription>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Portal Interface Language
                </label>
                <select
                  value={formData.language_pref}
                  onChange={(e) => setFormData({ ...formData, language_pref: e.target.value })}
                  className="w-full rounded-lg border border-slate-300 p-2 text-xs bg-white text-slate-900"
                >
                  <option value="en">English (Official Civil Services)</option>
                  <option value="hi">हिन्दी (राजभाषा)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Daily Study Goal (Minutes)
                </label>
                <Input
                  type="number"
                  min={10}
                  max={180}
                  value={formData.daily_goal_minutes}
                  onChange={(e) => setFormData({ ...formData, daily_goal_minutes: parseInt(e.target.value) || 30 })}
                  className="text-xs"
                />
              </div>
            </div>
          </CardContent>

          <CardFooter className="flex justify-end border-t border-slate-100 pt-4">
            <Button
              type="submit"
              disabled={saving}
              className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold px-6"
            >
              <Save className="h-3.5 w-3.5 mr-1.5" />
              {saving ? "Saving Changes..." : "Save Profile Settings"}
            </Button>
          </CardFooter>
        </Card>
      </form>
    </div>
  );
}
