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

### [2026-09-11] - Technical Course Content Generation Pipeline Backend
- **Author**: Antigravity AI & Ravish Kansal (@ravishkansal22)
- **Scope**: `[backend]` `[ai-service]` `[architecture]` `[docs]`
- **Branch**: `technical-course-pipeline`
- **Description**:
  - Implemented the complete backend pipeline for Technical Course content generation in iGOT Karmayogi under `backend/app/modules/technical_courses/`.
  - **Transcript Ingestion & Chunking (`transcript_service.py`):** Cleaning WebVTT/SRT timestamps, audio cues, whitespace normalization, token estimation, and overlapping semantic chunking.
  - **Structured Learning Objective Extraction (`objective_extractor.py`):** Schema-driven extraction (skill, difficulty, action, mode) with Gemini/OpenAI support and deterministic testing fallbacks.
  - **Quiz vs. Lab Decision Layer (`decision_service.py`):** Extensible Bloom taxonomy classifier determining whether objectives require interactive sandbox labs or multiple-choice quizzes.
  - **Human-Controlled Lab Templates (`template_service.py`):** Enforces human instructional boundaries; templates define starter code structure, constraints, and unit test suites before LLM filling.
  - **Controlled Lab Generation (`lab_generator.py`):** Generates concrete labs conforming strictly to `GeneratedLabSchema`.
  - **Reference Solution Generation (`solution_generator.py`):** Synthesizes reference solutions marked untrusted until validated.
  - **Isolated Sandbox Validation (`sandbox_service.py`):** Primary Docker container execution (`--network none`, 128MB limit, timeout, non-root) with isolated subprocess fallback for development/testing.
  - **Full Pipeline Orchestrator (`pipeline_orchestrator.py`):** Coordinates transcript ingestion -> objectives -> lab decision -> template matching -> lab generation -> solution generation -> sandbox validation -> SQLite persistence.
  - **Database Models (`models.py`):** Added `TechnicalTranscript`, `TechnicalLearningObjective`, `TechnicalLabTemplate`, `TechnicalGeneratedLab`, `TechnicalLabSolution`, and `TechnicalLabValidationResult`.
  - **Automated Test Suite (`backend/tests/test_technical_pipeline.py`):** 22 unit & integration tests validating all pipeline components, sandbox isolation, error modes, and REST APIs.
- **Affected Files / Routes**:
  - `backend/app/modules/technical_courses/` [NEW]
  - `backend/app/models/models.py`
  - `backend/app/core/seed_data.py`
  - `backend/app/main.py`
  - `backend/tests/test_technical_pipeline.py` [NEW]
  - `docs/features/technical-course-pipeline.md` [NEW]
  - `POST /api/technical-courses/process`
  - `POST /api/technical-courses/objectives`
  - `POST /api/technical-courses/decide-mode`
  - `GET /api/technical-courses/templates`
  - `POST /api/technical-courses/match-template`
  - `POST /api/technical-courses/labs/generate`
  - `POST /api/technical-courses/labs/{id}/solution`
  - `POST /api/technical-courses/labs/{id}/validate`
  - `GET /api/technical-courses/labs/{id}`
  - `POST /api/technical-courses/pipeline/run-full`
- **Agent Context / Rules**:
  - Code generation must always be validated in Docker/isolated sandbox before marking a lab as deployable.
  - Keep domain modules strictly isolated so teammates working on Statistical, Governance, and Behavioural pipelines face zero merge conflicts.

---

### [2026-09-09] - Comprehensive Visual Design Overhaul (design branch)
- **Author**: Antigravity AI & Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[ui]` `[css]` `[design]`
- **Branch**: `design`
- **Description**:
  - **Design Foundation (`globals.css`):** Expanded the design token system with an extended palette — navy scale (`#070E20` → `#1E3A8A`), teal accents (`#0D9488`, `#14B8A6`), ochre (`#B45309`), sage (`#059669`). Added 8 CSS keyframe animations (`fadeInUp`, `pulseGlow`, `shimmer`, `floatDot`, `slideLine`, `cardHover`) and utility classes (`.hero-gradient`, `.navy-teal-gradient`, `.glass-light`, `.glass-card`, `.card-hover-lift`, `.hero-mesh`, `.animate-pulse-glow`, `.animate-float-dot*`).
  - **Landing Page (`EntryLandingPage.tsx`):** Transformed hero section to a dramatic `hero-gradient` (dark navy-to-teal) with CSS mesh-grid pattern overlay and two radial glow orbs. Stats bar moved into the hero as frosted glass cards. Carousel now uses full `object-cover` with gradient overlay and teal dot controls. About section: unique icon backgrounds per pillar (navy/teal/ochre) with left-border accent cards. How It Works: horizontal timeline with gradient connecting line and colored step circles (navy/teal/amber/ochre) — stacked mobile version. Resources: top-stripe colored cards per document category. Help: 3 gradient-accent support cards with distinct top stripes (navy/teal/ochre). Closing CTA banner reuses hero-gradient with mesh overlay.
  - **Home Page Dashboard (`HomePage.tsx`):** Welcome header becomes a full hero-gradient section with CSS mesh, two glow orbs, gradient avatar ring with online pulse, and glassmorphic secondary button. Teal left-border on "Continue Learning" card; gradient horizontal progress bars replacing flat navy; amber-gradient streak card when streak ≥ 3; difficulty-colored left-border course cards (green=beginner, blue=intermediate, amber=advanced). All card section icons upgraded to colored rounded-xl icon containers (navy/teal/amber/sage). Stats grid uses color-coded cells (slate/teal/blue).
  - **Discover Page (`DiscoverPage.tsx`):** Header becomes hero-gradient with glassmorphic search input (glass-light class), gradient send button, and glass trending topic pills. Category tabs use navy-teal-gradient for active state. Course cards get category-colored accent top stripe, colored difficulty dots, gradient "View Course" button, and card-hover-lift animation. Empty state and loading spinner upgraded.
  - **AI Assistant Widget (`AiAssistantWidget.tsx`):** Floating button uses navy-teal-gradient with `animate-pulse-glow`, ping online indicator, and hover tooltip. Chat panel: gradient header with mesh overlay, assistant messages with teal left-border, user messages with gradient bubble, animated typing indicator (3 bouncing dots using `animate-float-dot*`), gradient send button, auto-scroll to latest message.
  - **Navbar (`Navbar.tsx`):** Brand icon upgraded to rounded-xl navy-teal-gradient. Active nav link indicators changed from bg-blue-50 rectangle to bottom-bar gradient underline (`linear-gradient(navy→teal)`). Profile avatar upgraded to gradient ring with dark center. Profile dropdown upgraded to `rounded-2xl` with enhanced shadow. Register button upgraded to navy-teal gradient. Language switcher gets teal icon and rounded-full style.
- **Design Principles Enforced:**
  - No emojis, no colored pill boxes above headings
  - All animations use CSS-only keyframes (no JS animation libraries)
  - `prefers-reduced-motion` media query kills all animations for accessibility
  - Hindi/English i18n completely preserved — no translation keys changed
  - All routing logic untouched
- **Affected Files**:
  - `frontend/src/app/globals.css`
  - `frontend/src/features/landing/components/EntryLandingPage.tsx`
  - `frontend/src/features/dashboard/components/HomePage.tsx`
  - `frontend/src/features/catalog/components/DiscoverPage.tsx`
  - `frontend/src/features/assistant/components/AiAssistantWidget.tsx`
  - `frontend/src/components/shared/Navbar.tsx`
  - `docs/changelog.md`
  - `docs/team/arnav-bisht.md`
  - `docs/features/ui-design-system.md`

---

### [2026-09-09] - Dedicated Institutional Pages & Context-Aware Navbar Routing
- **Author**: Antigravity AI & Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[ui]` `[i18n]` `[routing]` `[docs]`
- **Branch**: `postlogin`
- **Description**:
  - Created 4 dedicated institutional pages (`/about`, `/how-it-works`, `/resources`, `/help`) as standalone routes with full-page components under `frontend/src/features/institutional/components/`.
  - **About Page (`/about`):** Institutional framework overview featuring 3 competency pillars (Statistical Methodology, Standardized Evaluation, Cadre AI Assistant), a paradigm shift comparison (Rule-Based vs. Role-Based learning), 6 institutional stakeholder cards (MoSPI, CBC, NSSTA, NSSO, CSO, ISTM), and a verifiable credentials banner.
  - **How It Works Page (`/how-it-works`):** Detailed 4-stage capacity building breakdown (Authenticate & Onboard, Study Accredited Curriculum, Standardized Assessment, Earn Verified Credential) with full explanations, key standard operations, process guarantee stats, and learning process FAQ section.
  - **Resources Page (`/resources`):** Searchable and filterable official statistical library with 6 cadre document cards (NSSO Field Manual, CPI Technical Manual, UN-NQAF Rubrics, CAPI Operations Manual, NAS Handbook, PFMS Guide), download modal with authentication badges, and category/search filtering.
  - **Help Page (`/help`):** 3-channel support grid (24/7 AI Assistant, Central Training Division Desk, Nodal Cadre Coordinators), collapsible FAQ accordion with 5 common queries, and full support ticket submission form with simulated tracking IDs.
  - **Context-Aware Navbar Routing:** Updated `Navbar.tsx` to differentiate between unauthenticated landing page users (smooth-scroll anchor links to `/#about`, `/#how-it-works`, etc.) and authenticated/inner-page users (dedicated page routes to `/about`, `/how-it-works`, etc.).
  - All 4 pages follow the institutional design standard: white header banner (`bg-white border-b border-slate-200`), continuous `#F8FAFC` slate canvas, Official Navy `#1E3A8A` branding, and Lucide SVG iconography.
  - Each page includes bilingual (Hindi/English) support via `useI18n()` for all translated keys.
- **Affected Files**:
  - `frontend/src/features/institutional/components/AboutPage.tsx` [NEW]
  - `frontend/src/features/institutional/components/HowItWorksPage.tsx` [NEW]
  - `frontend/src/features/institutional/components/ResourcesPage.tsx` [NEW]
  - `frontend/src/features/institutional/components/HelpPage.tsx` [NEW]
  - `frontend/src/app/about/page.tsx` [NEW]
  - `frontend/src/app/how-it-works/page.tsx` [NEW]
  - `frontend/src/app/resources/page.tsx` [NEW]
  - `frontend/src/app/help/page.tsx` [NEW]
  - `frontend/src/components/shared/Navbar.tsx`
  - `docs/changelog.md`
  - `docs/team/arnav-bisht.md`
  - `docs/features/ui-design-system.md`
  - `docs/features/homepage-portal.md`

---

### [2026-09-09] - Post-Login Homepage & Repository-Wide Non-AI Institutional Redesign
- **Author**: Antigravity AI & Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[ui]` `[i18n]` `[docs]`
- **Branch**: `postlogin`
- **Description**:
  - Extended the non-AI, white background institutional standard from Discover across the post-login homepage (`/home`), my learning (`/my-learning`), officer profile (`/profile`), and administration console (`/admin`).
  - Replaced isolated floating widget cards and dark gradients with seamless full-width white institutional headers (`bg-white border-b border-slate-200 py-8 sm:py-10`) and a continuous `#F8FAFC` slate canvas.
  - Stripped all remaining decorative unicode emojis (`🔥`, `✨`, `★`, `🎉`) and text checkmarks (`Completed ✓`) across all pages (`CourseLearningPlayerPage.tsx`, `AssessmentTestPage.tsx`, `OnboardingWizardPage.tsx`, `AdminDashboardPage.tsx`), replacing them with semantic Lucide SVG icons (`CheckCircle2`, `XCircle`, `Check`).
  - Eliminated artificial colored/saffron eyebrow pill boxes above headings; standardized on letter-spaced ministry headers with Lucide `Building2` iconography.
  - Standardized interactive buttons across the application on Official Navy Primary (`#1E3A8A` / hover `#172554`).
  - Implemented 100% full bilingual (Hindi/English) translation parity across `home.*`, `learning.*`, `profile.*`, and `admin.*` keys in `frontend/src/lib/i18n/index.tsx`.
  - Updated documentation across `docs/features/ui-design-system.md`, `docs/features/analytics-dashboard.md`, `docs/team/arnav-bisht.md`, and `docs/changelog.md`.
- **Affected Files**:
  - `frontend/src/features/dashboard/components/HomePage.tsx`
  - `frontend/src/features/progress/components/MyLearningPage.tsx`
  - `frontend/src/features/profile/components/ProfilePage.tsx`
  - `frontend/src/features/administration/components/AdminDashboardPage.tsx`
  - `frontend/src/features/learning/components/CourseLearningPlayerPage.tsx`
  - `frontend/src/features/assessments/components/AssessmentTestPage.tsx`
  - `frontend/src/features/onboarding/components/OnboardingWizardPage.tsx`
  - `frontend/src/features/auth/components/ForgotPasswordPage.tsx`
  - `frontend/src/lib/i18n/index.tsx`
  - `docs/features/ui-design-system.md`
  - `docs/features/analytics-dashboard.md`
  - `docs/team/arnav-bisht.md`
  - `docs/changelog.md`

---

### [2026-09-08] - Discover Page Overhaul, Background Fix & Full Hindi Localization
- **Author**: Antigravity AI & Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[ui]` `[i18n]` `[docs]`
- **Branch**: `discover`
- **Description**:
  - Solved the background color and container problem on `/discover`: replaced the nested, floating widget box layout with a seamless full-width institutional white header banner (`bg-white border-b border-slate-200`) and a unified `#F8FAFC` slate catalog canvas.
  - Eliminated all artificial "AI telltale" indicators: removed unicode emojis (`🔥`, `✨`, `★`) from category tabs, trending pills, and course cards, and replaced rectangular colored pill boxes above headings with clean, letter-spaced ministry eyebrow text and Lucide `Building2` iconography.
  - Implemented 100% full bilingual (Hindi/English) compatibility: expanded `frontend/src/lib/i18n/index.tsx` dictionary with translations for search inputs, search/clear buttons, trending topics (*National Sample Survey*, *CPI*, *PFMS*, etc.), discipline categories, filter options, sort order, and dynamic course card title/overview metadata.
  - Elevated course card presentation: integrated official MoSPI/ISTM badges, Lucide `Clock` duration counters, Lucide `Star` ratings with enrolled counts, structured metadata lists, and official Navy `#1E3A8A` primary buttons.
  - Added an institutional accreditation trust ribbon affirming MoSPI accreditation, CBC competency guidelines, and verifiable cryptographic credentials.
  - Harmonized `CourseDetailPage.tsx` with clean layout, Lucide `Star` rating icons, and bilingual string lookup.
  - Updated documentation across `docs/features/course-management.md`, `docs/features/ui-design-system.md`, `docs/team/arnav-bisht.md`, and `docs/changelog.md`.
- **Affected Files**:
  - `frontend/src/features/catalog/components/DiscoverPage.tsx`
  - `frontend/src/features/catalog/components/CourseDetailPage.tsx`
  - `frontend/src/lib/i18n/index.tsx`
  - `docs/features/course-management.md`
  - `docs/features/ui-design-system.md`
  - `docs/team/arnav-bisht.md`
  - `docs/changelog.md`

---

### [2026-09-08] - Homepage Streamlining, Sober Yellow Accents & Hindi Toggle Migration
- **Author**: Antigravity AI & Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[ui]` `[docs]`
- **Branch**: `homepage`
- **Description**:
  - Removed top ministry ribbon from `Navbar.tsx`; integrated language toggle button (`हिन्दी / English`) directly into main navbar action bar and mobile drawer.
  - Eliminated artificial "AI telltale" elements: stripped out multi-colored eyebrow pill boxes above section titles, removed fake progress meters, rainbow gradient lines, and synthetic query chips.
  - Transitioned from saturated amber-gold to sober warm yellow accents (`#EAB308` / `#CA8A04` / `#FEF9C3`), keeping it restrained, dignified, and authentic to Indian public-service standards.
  - Streamlined page architecture to a bare-bones, highly focused portal: clean hero with framed carousel, clean 4-metric statistics strip, grounded institutional overview card, direct 4-step milestone cards, uniform document cards, and solid deep navy closing banner.
  - Recalibrated section scroll offsets and viewports to `scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)]`.
  - Implemented full bilingual internationalization (Hindi/English) across all homepage sections (`hero`, `about`, `howItWorks`, `resources`, `help`, `footer`, and carousel slides) via `useI18n()`.
  - Updated `docs/features/homepage-portal.md`, `docs/features/ui-design-system.md`, and `docs/team/arnav-bisht.md`.
- **Affected Files**:
  - `frontend/src/components/shared/Navbar.tsx`
  - `frontend/src/features/landing/components/EntryLandingPage.tsx`
  - `frontend/src/lib/i18n/index.tsx`
  - `frontend/src/app/globals.css`
  - `docs/features/homepage-portal.md`
  - `docs/features/ui-design-system.md`
  - `docs/team/arnav-bisht.md`
  - `docs/changelog.md`

---

### [2026-09-08] - Homepage Aesthetic Unification & Navy/Gold Design System
- **Author**: Antigravity AI & Arnav Bisht (@arnavbisht141)
- **Scope**: `[frontend]` `[ui]` `[docs]`
- **Branch**: `homepage`
- **Description**:
  - Completely unified the portal landing page (`EntryLandingPage.tsx`) under the official **Navy Blue (`#1E3A8A`) & Gold/Yellow (`#F59E0B`) Institutional Standard**, systematically replacing fragmented legacy rose/charcoal hues.
  - Introduced rich graphical elements: connected horizontal progression line with navy-to-gold gradient, competency progress meters, dual-tone icon containers, and ambient backdrop lighting.
  - Integrated comprehensive `lucide-react` iconography across metrics, milestones, resource cards, and interactive support channels.
  - Enhanced text readability with relaxed line-heights, high contrast WCAG AAA ratios, interactive AI Copilot sample prompt chips, and scannable cadre FAQ cards.
  - Preserved single-viewport layout physics (`scroll-mt-[120px] min-h-[calc(100vh-120px)]`) and zero-shift programmatic glide scrolling.
  - Added new feature specification `docs/features/homepage-portal.md`, updated `docs/features/ui-design-system.md`, and logged contributor activity in `docs/team/arnav-bisht.md`.
- **Affected Files**:
  - `frontend/src/features/landing/components/EntryLandingPage.tsx`
  - `frontend/src/app/globals.css`
  - `docs/features/homepage-portal.md`
  - `docs/features/ui-design-system.md`
  - `docs/features/README.md`
  - `docs/team/arnav-bisht.md`
  - `docs/changelog.md`
- **Agent Context / Rules**:
  - Maintain the Navy Blue & Gold color tokens (`--color-navy-primary`, `--color-gold-primary`) and avoid reintroducing legacy rose tones (`#965C66`).
  - Keep single-viewport section heights (`min-h-[calc(100vh-120px)]`) and ID anchors intact for smooth navbar gliding.

---

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
