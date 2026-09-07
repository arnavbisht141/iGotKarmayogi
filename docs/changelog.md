# 📜 Repository Changelog

All notable changes to the **iGOT Karmayogi (MoSPI)** platform are documented in this file.

This changelog serves as the authoritative source of change history for **engineering team members** and **AI coding agents** to provide context for upcoming features, bug fixes, and architectural evolutions.

---

## 📌 Format Guide for New Entries

When contributing changes, append entries at the top of the appropriate version/date block following this convention:

```markdown
### [YYYY-MM-DD] - Short Title of Change
- **Author**: Name (@github-username)
- **Scope**: `[frontend]` | `[backend]` | `[ai-service]` | `[docs]` | `[devops]` | `[architecture]`
- **Description**: Concise explanation of what was changed and the rationale.
- **Affected Files / Routes**:
  - `path/to/file.tsx`
  - `POST /api/endpoint`
- **Agent Context / Rules**: Any architectural constraints or edge cases future agents must respect.
```

---

## 🔄 Change History

### [2026-09-08] - Documentation Hierarchy Revamp & Knowledge Decentralization
- **Author**: Antigravity AI & Arnav Bisht (@arnavbisht141)
- **Scope**: `[docs]`
- **Description**:
  - Decomposed redundant monolithic documentation (`PROJECT_CONTEXT_AND_PROGRESS.md`, `HOMEPAGE_UI_REFINEMENTS.md`, `UI_UX_CHANGES.md`) into a modular structure.
  - Established `docs/features/` with in-depth specifications for AI Copilot, Course Management, Assessments & Certificates, Auth/RBAC, Analytics & Dashboards, and the UI Design System.
  - Established `docs/team/` for recording visible and invisible (research, design, architecture) contributions by teammates.
  - Established unified `docs/changelog.md` for team and AI agent operational context.
  - Updated root `docs/README.md` as the centralized documentation hub.
- **Affected Files**:
  - `docs/changelog.md`
  - `docs/features/*`
  - `docs/team/*`
  - `docs/README.md`
  - Removed redundant legacy files.

---

### [2026-09-07] - Domain Boundary Reorganization & Modular Monolith Transition
- **Author**: Arnav Bisht (@arnavbisht141)
- **Scope**: `[backend]` `[architecture]`
- **Description**:
  - Reorganized backend into clean domain modules under `backend/app/modules/` (`auth`, `onboarding`, `profile`, `discover`, `courses`, `learning`, `assessments`, `dashboard`, `admin`).
  - Integrated latest landing page and layout features into the modular structure.
  - Created ADRs (`adr/0001-modular-monolith-and-ai-boundary.md` and `adr/0002-backend-owns-lms-data.md`) establishing boundaries between LMS data ownership and future AI services.
- **Affected Files**:
  - `backend/app/modules/*`
  - `backend/app/main.py`
  - `docs/domain-boundaries.md`
  - `docs/architecture.md`
  - `docs/adr/*`

---

### [2026-09-07] - Hero, Navbar Brand & Statistics Polish (Navy Aesthetic)
- **Author**: Diwakar Ujjwal (@diwakarujjwal)
- **Scope**: `[frontend]`
- **Description**:
  - Aligned hero headline and statistics section with the official dark navy (`#1E3A8A`) and slate aesthetic.
  - Refined top navbar brand container, Government of India ribbon, and active indicators.
  - Merged pull request #6 from branch `aarna` into `main`.
- **Affected Files**:
  - `frontend/src/app/page.tsx`
  - `frontend/src/components/shared/Navbar.tsx`

---

### [2026-09-06] - Viewport-Snap Navigation, Scroll-Spy Lock & Dynamic Footer Architecture
- **Author**: Diwakar Ujjwal (@diwakarujjwal)
- **Scope**: `[frontend]`
- **Description**:
  - **Single-Viewport Section Architecture**: Configured landing page sections (`#hero`, `#about`, `#how-it-works`, `#resources`, `#help`) with `scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center`.
  - **Trackpad Inertia Restoration**: Removed global `html { scroll-behavior: smooth; }` and eliminated duplicate `scroll-padding-top: 120px` in `globals.css` that was compounding with section offsets. Smooth scrolling is handled programmatically via `window.scrollTo({ behavior: "smooth" })`.
  - **Programmatic Scroll Lock**: Implemented `isProgrammaticScrollRef` lock during anchor scrolling to prevent intermediate tabs from cycling mid-flight.
  - **Zero-Blink Tabs**: Standardized 1px fixed borders (`border-transparent` vs `border-blue-200`) and constant `font-medium` to eliminate box-model layout shifts when toggling tabs. Added `scroll={false}` and `prefetch={false}` to anchor Links.
  - **Dynamic Footer**: Replaced static layout footer with context-aware client `<Footer />` component that is omitted on the landing page (to avoid duplicate white footers below `#help`) and auto-rendered on inner pages.
  - Cleaned untracked `.venv` directory from git tracking.
- **Affected Files**:
  - `frontend/src/app/globals.css`
  - `frontend/src/components/shared/Navbar.tsx`
  - `frontend/src/components/shared/Footer.tsx`
  - `frontend/src/app/layout.tsx`
  - `frontend/src/app/page.tsx`

---

### [2026-09-06] - Header & Landing Page Aesthetic Parity Refinements
- **Author**: Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[docs]`
- **Description**:
  - Removed top scrolling announcement marquee from `Navbar.tsx` to eliminate visual noise.
  - Removed redundant `[MoSPI]` pill badge in header logo and eyebrow badge in landing hero.
  - Unified typography across navigation links (`About`, `Resources`, `Help` match `Discover` at `text-sm font-medium`).
  - Enlarged authentication CTAs: `Sign In` (`h-10 px-4`) and `Register` (`h-10 px-5 bg-[#1E3A8A]`).
  - Elevated landing hero headline (`text-3xl sm:text-4xl lg:text-[36px] font-extrabold text-slate-900`) and enlarged CTA buttons (`h-11 px-7`).
  - Refined statistics section to `100% Accredited Curriculum` with `text-3xl sm:text-4xl font-extrabold text-[#1E3A8A]`.
  - Merged PR #4 (`arnav` branch).
- **Affected Files**:
  - `frontend/src/components/shared/Navbar.tsx`
  - `frontend/src/app/page.tsx`

---

### [2026-09-06] - Official iGOT Karmayogi Navy & Slate Aesthetic Refinement
- **Author**: Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]`
- **Description**:
  - Aligned the application with official Government of India iGOT Karmayogi standards, transitioning primary accents to `#1E3A8A` / `#1D3557` and layout neutrals to slate.
  - Removed excessive AI branding and overbearing neon elements in favor of dignified institutional aesthetics.
- **Affected Files**:
  - `frontend/src/app/globals.css`
  - `frontend/src/components/shared/*`
  - `frontend/src/app/(auth)/*`

---

### [2026-09-06] - Muted Rose Design System & Floating AI Assistant Redesign
- **Author**: Aarna (@aarna605-dot), Ravish Kansal (@RavishKansal), Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]`
- **Description**:
  - Implemented the **Muted Rose Design System** palette tokens (`#965C66` primary, `#C8A8A9` secondary, `#EEE8E9` warm background, `#241E20` charcoal text).
  - Redesigned landing page hero layout and statistics bar with aspect-ratio-preserved official photographs (`/karmayogi.jpg`, `/government-meeting.jpg`, `/ai-daksh.jpg`).
  - Redesigned floating AI assistant widget (`AiAssistantWidget.tsx`) into a sleek circular launcher (`h-14 w-14 rounded-full bg-[#965C66]`), removed LangGraph vendor branding, and established civil-service identity: *"Karmayogi AI - Civil Service Intelligence Assistant"*.
  - Merged PR #2 (`Aarna` branch).
- **Affected Files**:
  - `frontend/src/app/page.tsx`
  - `frontend/src/components/shared/AiAssistantWidget.tsx`
  - `frontend/src/app/(auth)/login/page.tsx`
  - `frontend/src/app/(auth)/register/page.tsx`

---

### [2026-09-06] - Dockerization & Multi-Stage Deployment Architecture
- **Author**: Arnav Bisht (@arnavbisht141)
- **Scope**: `[devops]` `[infra]`
- **Description**:
  - Production-grade multi-stage Docker build for Next.js 16 (`base` ➔ `deps` ➔ `builder` ➔ `runner`) generating an unprivileged ~150MB standalone container.
  - FastAPI Python 3.12 Docker container with automated health check probes.
  - Dual Compose configurations:
    - `docker-compose.yml`: Standalone production profiles with persistent SQLite volume (`backend-data:/app/data`).
    - `docker-compose.dev.yml`: Live-reload development setup with host volume binds (`./frontend:/app`, `./backend:/app`).
- **Affected Files**:
  - `frontend/Dockerfile`, `frontend/Dockerfile.dev`, `frontend/.dockerignore`
  - `backend/Dockerfile`, `backend/.dockerignore`
  - `docker-compose.yml`, `docker-compose.dev.yml`
  - `README.md`

---

### [2026-09-06] - Initial Codebase & LMS Domain Implementation
- **Author**: Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[backend]`
- **Description**:
  - Initial repository creation implementing the full Miro LMS user flow for Smart India Hackathon SIH '26 (MoSPI).
  - 17 normalized SQLAlchemy models covering users, roles, courses, modules, lessons, skills, enrollments, progress, assessments, questions, attempts, and learning histories.
  - NIST-standard PBKDF2-HMAC-SHA256 authentication replacing problematic `passlib` bcrypt dependencies.
  - LangGraph StateGraph assistant workflow with Google Gemini, OpenAI, and deterministic MoSPI domain fallback.
  - Coursera-style split learning player, timed MCQ assessment engine, verifiable PDF/printable certificate modal, and 5-step onboarding wizard.
