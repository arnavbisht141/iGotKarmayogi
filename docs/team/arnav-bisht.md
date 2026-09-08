# Arnav Bisht — Contribution & Activity Log

> **Name:** Arnav Bisht  
> **GitHub Handle:** [@arnavbisht141](https://github.com/arnavbisht141)  
> **Role:** Full-Stack Architect & DevOps Lead  
> **Primary Subsystems:** System Architecture, Dockerization, Domain Boundaries, Backend Security (PBKDF2), Auth & RBAC, LMS Player, Assessment Engine  

---

## 1. Summary of Responsibilities
Lead full-stack engineer and repository architect for the Smart India Hackathon (SIH '26) iGOT Karmayogi (MoSPI) platform. Responsible for translating the validated Miro user flow into a production-ready, containerized multi-service platform. Designed database schemas, implemented core FastAPI endpoints and Next.js frontend pages, engineered containerization lifecycles, and refactored the backend into modular-monolith domain boundaries.

---

## 2. Visible Deliverables (Code & Repository Artifacts)

### 2.1 Multi-Stage Dockerization & DevOps (`79cc29f`)
- Built Next.js 16 4-stage unprivileged standalone container (~150MB).
- Built Python 3.12 FastAPI backend container with automated health check probe (`/api/health`).
- Configured dual Docker Compose setups:
  - `docker-compose.yml`: Production standalone with volume-persisted SQLite database.
  - `docker-compose.dev.yml`: Live-reload development setup with host volume binds and protected node_modules/venv volumes.

### 2.2 Backend Domain Reorganization (`630e065`, `d2513d7`)
- Modularized backend into `backend/app/modules/` (`auth`, `onboarding`, `profile`, `discover`, `courses`, `learning`, `assessments`, `dashboard`, `admin`).
- Maintained clean separation of LMS data ownership from future AI services.
- Authored Architecture Decision Records:
  - `docs/adr/0001-modular-monolith-and-ai-boundary.md`
  - `docs/adr/0002-backend-owns-lms-data.md`

### 2.3 Backend Security & NIST PBKDF2 Migration
- Removed fragile `passlib[bcrypt]` dependency due to Python 3.12 runtime errors.
- Built native PBKDF2-HMAC-SHA256 password hashing utility in `backend/app/core/security.py`.
- Configured JWT session generation, expiry, and role verification.

### 2.4 Header & Landing Page Aesthetic Parity (`f3116b2`, `e679256`)
- Removed scrolling marquee banner and MoSPI badge clutter.
- Standardized navigation typography across `About`, `Resources`, and `Help` to match `Discover`.
- Enlarged authentication buttons and aligned hero typography with official iGOT Karmayogi navy standards (`#1E3A8A`).

### 2.5 Homepage Aesthetic Unification & Streamlined Government Portal (branch: `homepage`)
- Completely unified the portal landing page (`EntryLandingPage.tsx`) under the official **Navy Blue (`#1E3A8A`) & Sober Yellow (`#EAB308`) Institutional Standard**, systematically replacing fragmented legacy rose/charcoal hues.
- Streamlined the header by removing the redundant top ministry ribbon and cleanly integrating the bilingual (Hindi/English) language switcher directly into the desktop navbar and mobile menu.
- Eliminated artificial "AI telltale" elements: removed multi-colored eyebrow pill boxes above section titles, discarded fake progress meters, rainbow gradient lines, and synthetic query chips.
- Transitioned to sober warm yellow accents (`#EAB308` / `#CA8A04`) on milestone step indicators, certificate badges, and registration CTAs.
- Preserved single-viewport layout physics with updated header metrics (`scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)]`) and zero-shift programmatic glide scrolling.
- Engineered full bilingual internationalization (Hindi/English) across all homepage sections (`hero`, `about`, `howItWorks`, `resources`, `help`, `footer`) via `useI18n()` and persistent client state.
- Authored the feature specification `docs/features/homepage-portal.md` and updated `ui-design-system.md`.

### 2.6 Discover Page & Course Catalogue Overhaul (branch: `discover`)
- Resolved background container fragmentation on `/discover`: replaced nested floating widget box with full-width institutional white header (`bg-white border-b border-slate-200`) and continuous `#F8FAFC` slate catalogue canvas.
- Stripped all decorative unicode emojis (`🔥`, `✨`, `★`) and artificial rectangular colored eyebrow pills across all categories, filters, trending topics, and course cards.
- Engineered 100% full bilingual (Hindi/English) translation parity across search inputs, buttons, trending tags, discipline tabs, filter options, sort order, and dynamic course card title/overview metadata via `useI18n()`.
- Standardized interactive buttons and badges onto the official Navy `#1E3A8A` / Sober Yellow `#EAB308` design system.
- Added institutional accreditation trust ribbon affirming MoSPI accreditation, CBC competency guidelines, and verifiable cryptographic credentials.
- Harmonized `CourseDetailPage.tsx` with clean layout, Lucide `Star` rating icons, and bilingual string lookup.
- Updated documentation in `docs/features/course-management.md`, `docs/features/ui-design-system.md`, `docs/team/arnav-bisht.md`, and `docs/changelog.md`.

### 2.7 Post-Login Dashboard & Repository-Wide Non-AI Institutional Standardization (branch: `postlogin`)
- Overhauled the post-login homepage (`/home`), my learning (`/my-learning`), officer profile (`/profile`), and admin dashboard (`/admin`) to adhere to the clean institutional standard established in Discover.
- Replaced floating card boxes and dark gradients with seamless full-width white institutional headers (`bg-white border-b border-slate-200`) and a continuous `#F8FAFC` workspace canvas.
- Stripped all remaining decorative unicode emojis (`🔥`, `✨`, `★`, `🎉`) and text checkmarks (`Completed ✓`) across the entire repository, replacing them with semantic Lucide SVG icons (`CheckCircle2`, `Building2`, `Clock`, `ShieldCheck`).
- Eliminated artificial rectangular saffron/colored eyebrow pills above section titles in favor of crisp, letter-spaced central ministry subheadings.
- Standardized interactive action buttons and focus rings onto Official Navy Primary (`#1E3A8A` / `#172554`).
- Expanded `frontend/src/lib/i18n/index.tsx` to provide 100% bilingual (Hindi/English) translation parity across the post-login dashboard, learning transcript, profile editor, and admin console.
- Synchronized documentation across `docs/features/ui-design-system.md`, `docs/features/analytics-dashboard.md`, `docs/team/arnav-bisht.md`, and `docs/changelog.md`.

### 2.8 Dedicated Institutional Pages & Context-Aware Navigation (branch: `postlogin`)
- Built 4 standalone institutional pages (`/about`, `/how-it-works`, `/resources`, `/help`) under `frontend/src/features/institutional/components/`, each following the established institutional design standard (white header banner, `#F8FAFC` slate canvas, Official Navy `#1E3A8A` branding).
- **About Page:** 3 competency pillar cards, rule-based vs. role-based paradigm comparison, 6 institutional stakeholder cards (MoSPI, CBC, NSSTA, NSSO, CSO, ISTM), and verifiable credentials banner.
- **How It Works Page:** Detailed 4-stage capacity building path with full explanations, key standard operations, process guarantees (self-paced, 70% threshold, cryptographic verification), and learning FAQ.
- **Resources Page:** Searchable/filterable official statistical library with 6 cadre document cards, category chips, download modal with authentication badges, and related course links.
- **Help Page:** 3-channel support grid (AI Assistant, Training Desk, Nodal Coordinators), collapsible FAQ accordion, and full support ticket submission form with simulated tracking IDs.
- Implemented context-aware navigation in `Navbar.tsx`: unauthenticated users on `/` get smooth-scroll anchor links, all other users get dedicated page routes.
- All pages include bilingual (Hindi/English) support via `useI18n()`.

---

## 3. "Invisible" & Offline Contributions

### 3.1 Miro Flow Realization & Requirements Mapping
- Deconstructed the SIH '26 Miro board user flow into discrete, measurable frontend routes and backend domain modules.
- Established the 10-widget learner home dashboard inventory and 5-step onboarding wizard.

### 3.2 MoSPI Domain Dataset & Curriculum Research
- Researched Ministry of Statistics & Programme Implementation (MoSPI) datasets, National Sample Survey (NSS) sampling stages, Consumer Price Index (CPI) Laspeyres formulas, and UN-NQAF statistical quality rubrics to build realistic seed data in `backend/app/core/seed_data.py`.

### 3.3 Evaluation Strategy & Demo Scripting
- Designed the 3 pre-seeded test personas (`admin@karmayogi.gov.in`, `rajesh.kumar@mospi.gov.in`, `priya.sharma@mospi.gov.in`) with 1-click login buttons on `/login` to ensure seamless live demonstrations for hackathon evaluators.

---

## 4. Chronological Activity Log

| Date | Activity | Category | Notes / Deliverables |
|---|---|---|---|
| `2026-09-09` | Institutional pages & context-aware navbar routing | `Code` / `UI` / `Routing` | Created `/about`, `/how-it-works`, `/resources`, `/help` standalone pages; smart anchor/page routing in Navbar |
| `2026-09-09` | Post-login dashboard & repository-wide non-AI redesign | `Code` / `UI` / `Docs` | Seamless white headers, removed emojis/boxes, Navy branding, 100% bilingual Hindi on `/home`, `/my-learning`, `/profile`, `/admin` |
| `2026-09-08` | Discover page overhaul, background fix & bilingual localization | `Code` / `UI` / `Docs` | Fixed background color layout, removed emojis/boxes, added 100% Hindi compatibility on `/discover` |
| `2026-09-08` | Homepage overhaul & Navy/Gold design unification | `Code` / `UI` / `Docs` | Unified `EntryLandingPage.tsx`, added graphical timeline, rich icons, authored `homepage-portal.md` |
| `2026-09-08` | Revamped docs hierarchy into modular changelog, features, and team logs | `Docs` / `Arch` | Established clean agent-ready documentation structure |
| `2026-09-07` | Domain boundaries backend refactor | `Code` / `Arch` | Reorganized `backend/app/modules/` and authored ADRs |
| `2026-09-06` | Header & landing page aesthetic parity pass | `Code` / `UI` | PR #4 merged, unified nav typography, enlarged CTAs |
| `2026-09-06` | Navy & slate aesthetic alignment | `Code` / `UI` | Replaced flashy AI styles with official iGOT standards |
| `2026-09-06` | Authored master project context and progress documentation | `Docs` | Comprehensive Phase 0 system reference |
| `2026-09-06` | Multi-stage Dockerization and compose environments | `DevOps` | Production standalone and live-dev Docker configurations |
| `2026-09-06` | Initial repository scaffolding and LMS user flow implementation | `Code` | 17 models, FastAPI backend, Next.js frontend, LangGraph |

---

## 5. Notes & Context for Future AI Coding Agents
- **Next.js Standalone Runner:** Always test client components with `useSearchParams()` inside `<Suspense>` boundaries.
- **Database Migrations / Seeds:** Whenever adding model fields, always update `backend/app/core/seed_data.py` so demo personas remain fully hydrated on container reset.
- **Security:** Do not re-install `passlib`. Use `backend/app/core/security.py`.
