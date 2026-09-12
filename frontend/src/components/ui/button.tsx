import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "outline" | "ghost" | "danger" | "saffron" | "white";
  size?: "sm" | "md" | "lg" | "icon";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "md", children, ...props }, ref) => {
    const variants = {
      default:
        "bg-[#347D51] text-white hover:bg-[#244A37] border border-[#244A37] shadow-xs focus-visible:ring-[#347D51]",
      secondary:
        "bg-slate-100 text-slate-900 hover:bg-slate-200 border border-slate-200/80 focus-visible:ring-slate-400",
      outline:
        "border border-slate-300 text-slate-800 bg-white hover:bg-slate-50 hover:border-slate-400 shadow-2xs focus-visible:ring-slate-400",
      ghost:
        "text-slate-700 hover:bg-slate-100 hover:text-slate-900 focus-visible:ring-slate-400",
      danger:
        "bg-rose-700 text-white hover:bg-rose-800 border border-rose-800 shadow-xs focus-visible:ring-rose-500",
      saffron:
        "bg-[#B45309] text-white hover:bg-[#92400E] border border-[#92400E] shadow-xs focus-visible:ring-amber-500 font-semibold",
      white:
        "bg-white text-slate-900 hover:bg-slate-100 border border-slate-200 shadow-xs focus-visible:ring-white font-semibold",
    };

    const sizes = {
      sm: "h-8 px-3 text-xs rounded-md",
      md: "h-9 px-4 text-xs font-semibold rounded-lg",
      lg: "h-11 px-5 text-sm font-semibold rounded-lg",
      icon: "h-9 w-9 p-0 rounded-lg flex items-center justify-center",
    };

    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center gap-2 font-medium tracking-tight transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50 cursor-pointer select-none active:translate-y-[1px]",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
