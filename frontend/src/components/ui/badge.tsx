import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "outline" | "success" | "warning" | "external" | "saffron" | "cadre";
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variants = {
    default: "border-transparent bg-slate-900 text-white font-medium",
    secondary: "border-slate-200 bg-slate-100 text-slate-800 font-medium",
    outline: "text-slate-800 border-slate-300 bg-white font-medium",
    success: "border-emerald-300 bg-emerald-50 text-emerald-900 font-medium",
    warning: "border-amber-300 bg-amber-50 text-amber-900 font-medium",
    external: "border-slate-300 bg-slate-100 text-slate-700 font-medium",
    saffron: "border-amber-300 bg-amber-50 text-amber-900 font-medium",
    cadre: "border-blue-200 bg-blue-50 text-[#1E3A8A] font-semibold",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 text-[11px] font-medium tracking-tight transition-colors focus:outline-none",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}
