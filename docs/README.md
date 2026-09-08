# iGOT Karmayogi (MoSPI) — Project Documentation

Welcome to the centralized documentation hub for the **iGOT Karmayogi (MoSPI)** platform, built for the **Smart India Hackathon (SIH '26)**.

This directory provides structured, decentralized knowledge bases for software engineers, evaluators, and AI coding agents.

---

## Documentation Navigation

### 1. [Master Changelog](changelog.md)
The single source of truth for all repository changes made across team members and AI coding agents. Structured chronologically with module attribution (`[frontend]`, `[backend]`, `[devops]`, `[docs]`, `[architecture]`).

---

### 2. [Feature Specifications (`docs/features/`)](features/README.md)
In-depth functional and technical specifications for each subsystem:
- [AI Copilot](features/ai-copilot.md) — LangGraph state machine, provider routing (Gemini/OpenAI), deterministic MoSPI fallback engine, and circular launcher widget.
- [Course Management](features/course-management.md) — Discovery catalog, syllabus hierarchy, Coursera-style split-screen player, in-lesson practice concept checks, and full Hindi compatibility.
- [Assessment & Certification](features/assessment-certification.md) — Timed exams, 70% passing threshold, automatic explanatory grading, celebratory confetti, and verifiable print/PDF certificates.
- [Auth, RBAC & Onboarding](features/auth-rbac.md) — NIST PBKDF2-HMAC security, JWT sessions, pre-seeded evaluation personas, and the 5-step onboarding wizard.
- [Analytics & Dashboards](features/analytics-dashboard.md) — 10-widget learner home dashboard, admin supervisory console, officer roster, and question difficulty analytics.
- [UI/UX Design System](features/ui-design-system.md) — Official Navy Blue (`#1E3A8A`) and Sober Yellow (`#EAB308`) design standard, slate neutral tokens, single-viewport scroll gliding, zero-shift tab navigation, and zero-emoji compliance.
- [Homepage & Public Portal](features/homepage-portal.md) — Institutional landing page (`/`), single-viewport section layout, official photography carousel, connected milestones, and bilingual support.

---

### 3. [Teammate Contribution Logs (`docs/team/`)](team/README.md)
Persistent records tracking both visible repository commits and "invisible" non-code contributions (research, Miro user flows, prompt engineering, system design, and pitch preparation):
- [Arnav Bisht](team/arnav-bisht.md) — Full-Stack Architecture, DevOps/Docker, Domain Boundaries, Backend Security (PBKDF2), Auth & RBAC.
- [Diwakar Ujjwal](team/diwakar-ujjwal.md) — Frontend UX Architecture, Viewport Scroll Physics, Zero-Shift Tabs, Dynamic Navigation & Footer.
- [Aarna](team/aarna605.md) — UI/UX Design System, Muted Rose Palette Tokens, Aspect-Ratio Media Integrity, AI Assistant Widget.
- [Ravish Kansal](team/ravish-kansal.md) — Frontend UI Implementation, Landing Page Layout Assembly, Responsive Testing & QA.

---

### 4. 🏛️ Architecture & Standards
- [architecture.md](architecture.md) — System architecture diagram, responsibilities table, 17 database models schema, and mandatory operational guidelines for AI agents.
- [domain-boundaries.md](domain-boundaries.md) — Modular monolith domain boundaries (`backend/app/modules/`) and LMS data ownership principles.
- [development.md](development.md) — Quick start runbook, Docker development/production commands, local environment setup, and verification tests.
- [adr/](adr/) — Architectural Decision Records:
  - [`0001-modular-monolith-and-ai-boundary.md`](adr/0001-modular-monolith-and-ai-boundary.md)
  - [`0002-backend-owns-lms-data.md`](adr/0002-backend-owns-lms-data.md)

---

## 📌 Rules for AI Coding Agents
AI coding agents working in this repository must consult [architecture.md](architecture.md) and the relevant [features/](features/) document before introducing architectural modifications, schema changes, or UI adjustments.
