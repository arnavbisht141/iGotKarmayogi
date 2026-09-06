"use client";

import React, { useState } from "react";
import { Award, Lock, Mail, ArrowRight, AlertCircle, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { useAuth } from "@/lib/auth/AuthContext";
import { fetchApi } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

export default function LoginPage() {
  const { login } = useAuth();
  const { t } = useI18n();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await fetchApi<{
        access_token: string;
        user_id: number;
        email: string;
        full_name: string;
        role: "learner" | "admin";
        onboarding_completed: boolean;
      }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      login(data.access_token, {
        id: data.user_id,
        email: data.email,
        full_name: data.full_name,
        role: data.role,
        onboarding_completed: data.onboarding_completed,
      });
    } catch (err: any) {
      setError(err.message || "Failed to authenticate. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const fillCredentials = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError(null);
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-[#EEE8E9]">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <div className="inline-flex h-12 w-12 rounded-xl bg-[#241E20] text-[#C8A8A9] border border-[#965C66]/30 items-center justify-center mb-3 shadow-xs">
            <Award className="h-7 w-7" />
          </div>
          <h2 className="text-2xl font-bold text-[#241E20] tracking-tight">Official Sign In</h2>
          <p className="text-xs text-[#5A5052] mt-1">
            Access your iGOT Karmayogi learning profile &amp; statistical records
          </p>
        </div>

        <Card className="border-[#C8A8A9]/50 shadow-md shadow-[#965C66]/5 bg-white rounded-2xl">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-bold text-[#241E20]">Sign In to Your Account</CardTitle>
            <CardDescription className="text-xs text-[#5A5052]">
              Use your government-issued email and password
            </CardDescription>
          </CardHeader>

          <CardContent>
            {error && (
              <div className="mb-4 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-[#241E20] mb-1">
                  Official Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-2.5 h-4 w-4 text-[#965C66]/60" />
                  <Input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@gov.in or name@mospi.gov.in"
                    className="pl-9 text-xs border-[#C8A8A9]/60 focus-visible:ring-[#965C66] focus-visible:border-[#965C66]"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="block text-xs font-semibold text-[#241E20]">
                    Password
                  </label>
                  <a
                    href="/forgot-password"
                    className="text-xs text-[#965C66] hover:text-[#824E57] font-medium"
                  >
                    Forgot password?
                  </a>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-2.5 h-4 w-4 text-[#965C66]/60" />
                  <Input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="pl-9 text-xs border-[#C8A8A9]/60 focus-visible:ring-[#965C66] focus-visible:border-[#965C66]"
                  />
                </div>
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-[#965C66] hover:bg-[#824E57] text-white font-semibold py-2.5 text-xs rounded-lg shadow-xs transition-colors border border-[#965C66]"
              >
                {loading ? "Authenticating..." : "Sign In to Dashboard"}
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex flex-col gap-3 pt-2 border-t border-[#C8A8A9]/30 text-xs">
            <div className="text-center text-[#5A5052]">
              New to Karmayogi?{" "}
              <a href="/register" className="font-semibold text-[#965C66] hover:text-[#824E57]">
                Register account
              </a>
            </div>

            {/* Quick One-Click Demo Credentials */}
            <div className="w-full pt-2 border-t border-[#C8A8A9]/20">
              <p className="text-[11px] font-semibold text-[#5A5052] uppercase tracking-wider mb-2 text-center">
                Quick Demo Logins
              </p>
              <div className="grid grid-cols-3 gap-1.5 text-[11px]">
                <button
                  type="button"
                  onClick={() => fillCredentials("admin@karmayogi.gov.in", "Admin@123")}
                  className="px-2 py-1.5 rounded bg-slate-100 hover:bg-[#965C66]/10 text-[#241E20] hover:text-[#965C66] font-medium border border-[#C8A8A9]/40 cursor-pointer text-center truncate transition-colors"
                  title="Director General Admin"
                >
                  Admin
                </button>
                <button
                  type="button"
                  onClick={() => fillCredentials("rajesh.kumar@mospi.gov.in", "Learner@123")}
                  className="px-2 py-1.5 rounded bg-slate-100 hover:bg-[#965C66]/10 text-[#241E20] hover:text-[#965C66] font-medium border border-[#C8A8A9]/40 cursor-pointer text-center truncate transition-colors"
                  title="Senior Statistical Officer (Onboarded)"
                >
                  Learner (SSO)
                </button>
                <button
                  type="button"
                  onClick={() => fillCredentials("priya.sharma@mospi.gov.in", "Learner@123")}
                  className="px-2 py-1.5 rounded bg-[#965C66]/10 hover:bg-[#965C66]/20 text-[#965C66] font-semibold border border-[#965C66]/30 cursor-pointer text-center truncate transition-colors"
                  title="New Officer (Tests 5-step Onboarding wizard)"
                >
                  New Onboard
                </button>
              </div>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
