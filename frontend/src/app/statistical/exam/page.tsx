import React, { Suspense } from "react";
import { Metadata } from "next";
import StatisticalExamPage from "@/features/statistical/components/StatisticalExamPage";

export const metadata: Metadata = {
  title: "Adaptive Statistical Examination | iGot Karmayogi",
  description: "Computerized Adaptive Testing (CAT) dynamic item-branching examination for statistical competencies and indices."
};

export default function StatisticalExamRoute() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-white">
          <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4" />
          <p className="text-slate-400 text-sm font-medium">Loading Adaptive Statistical Testing Engine...</p>
        </div>
      }
    >
      <StatisticalExamPage />
    </Suspense>
  );
}
