import type { ComponentType } from "react";
import { BarChart3, Code, ShieldCheck, Users } from "lucide-react";
import type { DomainCode } from "@/lib/types/competency";

export interface DomainMeta {
  code: DomainCode;
  label: string;
  description: string;
  icon: ComponentType<{ className?: string; "aria-hidden"?: boolean | "true" | "false" }>;
  practice: { label: string; href: string }[];
}

export const LEVEL_MAX = 5;

export const DOMAIN_ORDER: DomainCode[] = ["statistical", "technical", "digital_governance", "behavioural"];

export const DOMAINS: Record<DomainCode, DomainMeta> = {
  statistical: {
    code: "statistical",
    label: "Statistical",
    description:
      "Survey design, sampling, national accounts, price, labour, agricultural and industrial statistics, SDG indicators, metadata standards and data quality frameworks.",
    icon: BarChart3,
    practice: [{ label: "Adaptive statistics exam", href: "/statistical" }],
  },
  technical: {
    code: "technical",
    label: "Technical",
    description:
      "Python, R, SQL, Stata, SPSS, SAS, GIS, data visualization, AI and machine learning, cloud computing, APIs and open data.",
    icon: Code,
    practice: [{ label: "Hands-on virtual labs", href: "/labs" }],
  },
  digital_governance: {
    code: "digital_governance",
    label: "Digital Governance",
    description:
      "Cybersecurity, data privacy, digital signatures, government cloud and digital public infrastructure.",
    icon: ShieldCheck,
    practice: [
      { label: "Cyber defense sandbox", href: "/digital-governance/sandbox" },
      { label: "Governance scenarios", href: "/digital-governance/scenarios" },
    ],
  },
  behavioural: {
    code: "behavioural",
    label: "Behavioural & Managerial",
    description:
      "Leadership, communication, project management, ethics, decision making, situational awareness, accountability and change management.",
    icon: Users,
    practice: [
      { label: "AI oral board interview", href: "/behavioural/interview" },
      { label: "Case-based decision simulations", href: "/behavioural/cases" },
    ],
  },
};

export function isDomainCode(value: string): value is DomainCode {
  return (DOMAIN_ORDER as string[]).includes(value);
}

export function levelLabel(level: number): string {
  if (level >= 4.5) return "Expert";
  if (level >= 3.5) return "Advanced";
  if (level >= 2.5) return "Proficient";
  if (level >= 1.5) return "Developing";
  if (level > 0) return "Foundational";
  return "Not yet assessed";
}
