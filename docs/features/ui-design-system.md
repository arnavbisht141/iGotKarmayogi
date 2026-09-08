# UI/UX Design System: Navy Blue & Yellow/Gold Institutional Standard

> **Status:** `Implemented` (Phase 0 / Design System v2.0)  
> **Primary Files:**  
> - Styles: `frontend/src/app/globals.css`  
> - Components: `Navbar.tsx`, `Footer.tsx`, `AiAssistantWidget.tsx`, `EntryLandingPage.tsx`  

---

## 1. Executive Summary & Design Philosophy

The **iGOT Karmayogi (MoSPI)** platform adheres to an authoritative institutional design standard tailored for the National Programme for Civil Services Capacity Building (NPCSCB):
- **Constitutional & Administrative Dignity:** Grounded in official Government of India **Navy Blue (`#1E3A8A`)** and **Gold / Yellow (`#F59E0B`)**, embodying public-service prestige, meritocracy, and official accreditation.
- **No Gimmicky Cybernetics:** Avoid fluorescent cyan/purple neon washes or floating cybernetic bots. All graphical accents (meters, badges, icon containers) are purposeful and refined.
- **High Readability & Scannability:** Generous line heights (`leading-relaxed`), visual chunking with cards and tags, WCAG AAA compliant text contrasts (`#0F172A` headlines, `#334155` body on light surfaces; `#FFFFFF` on navy surfaces).
- **Zero-Shift Single-Viewport Gliding:** Programmatic smooth scrolling with trackpad inertia preservation and fixed 1px zero-blink navigation borders.
- **Asset Integrity:** Never crop or distort official photographs or infographics. Use `object-contain` within framed, elevated cards.

---

## 2. Design System Color Tokens

| Token Name | CSS Variable / Utility | Hex Code | Purpose & Application |
|---|---|---|---|
| **Official Navy Primary** | `--color-navy-primary` | `#1E3A8A` | Primary brand actions, navbar ribbon, official sign-in buttons, key badges. |
| **Navy Hover / Active** | `--color-navy-hover` | `#172554` | Hover and active states for primary interactive elements. |
| **Deep Navy Canvas** | `--color-navy-deep` | `#0F2C59` | Dark visual surfaces (About card, closing CTA banner). |
| **Darkest Navy** | `--color-navy-darkest` | `#0B1930` | Root background gradient anchor for institutional cards and ribbons. |
| **Sober Yellow Primary** | `--color-gold-primary` | `#EAB308` | Milestone numbers, subtle button accents, verified highlights. |
| **Sober Yellow Hover** | `--color-gold-hover` | `#CA8A04` | Interactive hover transitions for yellow action buttons. |
| **Light Yellow Fill** | `--color-gold-light` | `#FEF9C3` | Background tint for subtle yellow callouts. |
| **Yellow Border Accent** | `--color-gold-border` | `#FDE047` | Delicate borders for active indicators and milestone badges. |
| **Slate Heading** | `--foreground` | `#0F172A` | Crisp, high-contrast headings and primary labels. |
| **Slate Body Text** | `--color-slate-text` | `#334155` | Reader-friendly paragraphs, descriptions, and feature bullet text. |
| **Slate Muted** | `--color-slate-muted` | `#64748B` | Subtitles, helper text, and secondary timestamps. |
| **Clean Background** | `--background` | `#F8FAFC` | Light off-white neutral canvas for readability across all device screens. |

---

## 3. Structural & Interaction Patterns

### 3.1 Single-Viewport Section Architecture (`frontend/src/features/landing/components/EntryLandingPage.tsx`)
Landing page sections (`#hero`, `#about`, `#how-it-works`, `#resources`, `#help`) are styled with:
```tsx
className="scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)] flex flex-col justify-center"
```
Clicking any navigation item glides directly to and frames that section cleanly in the viewport without awkward cutoffs or extra blank spaces.

### 3.2 Precision Smooth Scrolling & Trackpad Momentum
- **Elimination of Compounding Offsets:** Rely solely on `scroll-mt-[120px]` matching the sticky header height.
- **Inertia Physics Preservation:** Programmatic transitions use `window.scrollTo({ behavior: "smooth" })` on anchor clicks while avoiding global CSS scroll-behavior that interferes with macOS trackpad inertia.
- **Scroll-Spy Lock:** Employs `isProgrammaticScrollRef` during anchor gliding to prevent intermediate tabs from flickering mid-flight.

### 3.3 Zero-Blink & Zero-Shift Tab Navigation (`Navbar.tsx`)
- Standardized fixed 1px borders (`border-transparent` on inactive, `border-blue-200` on active) to eliminate 2–3px box-model layout shifts when toggling tabs.
- Maintained constant `font-medium` across active and inactive states to avoid font-metric width jumps.
- Anchor links configure `scroll={false}` and `prefetch={false}` to prevent Next.js router full-page flickers.

### 3.4 Context-Aware Institutional Footer (`Footer.tsx`)
- Dynamic client component rendering:
  - Omitted on the landing page (`pathname === "/"`) so that `#help`'s integrated dark CTA and legal ribbon sits flush at the bottom.
  - Automatically rendered on all inner views (`/discover`, `/login`, `/register`, `/home`, etc.).

### 3.5 Catalogue Workspace Architecture (`DiscoverPage.tsx` & `CourseDetailPage.tsx`)
- **Full-Width Institutional Header (`bg-white border-b border-slate-200`):** Replaced isolated floating widget cards with full-bleed institutional banners featuring clean letter-spaced ministry eyebrow text and Lucide `Building2` iconography.
- **Slate Workspace Canvas (`bg-[#F8FAFC]`):** The catalog grid and filter ribbon live directly on the clean `#F8FAFC` slate canvas with crisp white course cards (`bg-white border border-slate-200 shadow-2xs`).
- **Unified Action Buttons:** All primary course exploration and enrollment CTAs standardize on Official Navy Primary (`bg-[#1E3A8A] hover:bg-[#172554] text-white`).
- **Complete Bilingual i18n Integration:** Every text element, filter option, search input, topic badge, and course title dynamically responds to the Navbar's `useI18n()` language toggle.

### 3.6 Post-Login Dashboard & All Pages Standardization (`/home`, `/my-learning`, `/profile`, `/admin`)
- **Seamless White Institutional Headers:** Replaced nested floating widget cards with full-width white institutional banners across the entire post-login application.
- **Continuous Slate Canvas (`#F8FAFC`):** Workspaces sit on a continuous `#F8FAFC` neutral canvas, eliminating fragmented multi-colored boxes and dark hero gradients.
- **Strict Elimination of Artificial "AI Telltales":** Removed decorative unicode emojis (`🔥`, `✨`, `★`, `🎉`), text checkmarks (`Completed ✓`), and colored rectangular pill badges above headings. Status indicators use semantic Lucide SVG icons (`CheckCircle2`, `XCircle`, `ShieldCheck`).
- **Primary Navy Brand Standardization:** Standardized interactive buttons and action controls across all pages and modals onto Official Navy Primary (`bg-[#1E3A8A] hover:bg-[#172554]`).
- **100% Bilingual Hindi/English Support:** Full dictionary coverage in `frontend/src/lib/i18n/index.tsx` for post-login dashboard, learning transcript, official profile, and administrative console.

### 3.7 Standalone Institutional Pages (`/about`, `/how-it-works`, `/resources`, `/help`)
- **Feature Components:** `frontend/src/features/institutional/components/` contains `AboutPage.tsx`, `HowItWorksPage.tsx`, `ResourcesPage.tsx`, and `HelpPage.tsx`.
- **Route Files:** `frontend/src/app/{about,how-it-works,resources,help}/page.tsx` each import and render their respective institutional component.
- **Consistent Layout Pattern:** Every page follows the same structure:
  1. **White Institutional Header Banner** (`bg-white border-b border-slate-200 py-8 sm:py-12`): Ministry eyebrow text with `Building2` icon, `h1` title via `useI18n()`, subtitle, and action buttons (Explore Catalogue + Dashboard if authenticated).
  2. **Continuous Slate Canvas** (`bg-[#F8FAFC]`): Main content area with `max-w-6xl mx-auto` grid sections.
- **Content Architecture:**
  - **About:** 3 competency pillar cards, rule-based vs. role-based paradigm comparison, 6 stakeholder governance cards (MoSPI, CBC, NSSTA, NSSO, CSO, ISTM), verifiable credentials dark banner.
  - **How It Works:** 4-stage capacity building cards with full explanations and key standard operations, 3-column process guarantee strip, 2-column FAQ grid, dark closing CTA banner.
  - **Resources:** Search + category filter bar, 6 official document cards with metadata tables and download modals, empty-state handling.
  - **Help:** 3-channel support grid (AI Assistant, Training Desk, Nodal Coordinators), collapsible FAQ accordion, support ticket form with tracking ID simulation.

### 3.8 Context-Aware Navbar Navigation Routing (`Navbar.tsx`)
- **Unauthenticated users on `/` (landing page):** Navbar links render as anchor links (`/#about`, `/#how-it-works`, etc.) with programmatic smooth-scroll via `handleAnchorClick()` and scroll-spy active state tracking.
- **Authenticated users or any non-landing page:** Navbar links render as page routes (`/about`, `/how-it-works`, etc.) navigating to the dedicated standalone institutional pages.
- **Routing Logic:** `href={!user && pathname === "/" ? "/#about" : "/about"}` pattern used across all 4 institutional links in both desktop and mobile menus.
- **Active State Highlighting:** Uses `isActive("/about")` for page routes and `pathname === "/" && activeSection === "about"` for anchor scroll-spy, ensuring correct visual feedback in both modes.

---

## 4. Graphical & Iconography Guidelines

1. **Dual-Tone Icon Badges:** Use curated `lucide-react` icons wrapped in high-contrast dual-tone containers:
   - Primary: `bg-blue-50 text-[#1E3A8A] border border-blue-200`
   - Accent: `bg-amber-50 text-amber-700 border border-amber-200`
2. **Progressive Flow Lines:** Connected workflows utilize smooth gradients (`from-[#1E3A8A] via-blue-400 to-[#F59E0B]`) with numbered step pins.
3. **Aspect Ratio Preservation:** Official institutional media (`/karmayogi.jpg`, `/government-meeting.jpg`, `/ai-daksh.jpg`) MUST retain natural aspect ratios using `object-contain` within framed containers.
4. **Strict Elimination of Emojis & AI Telltales:** All decorative unicode emojis (`🔥`, `✨`, `★`, `🎉`) and artificial rectangular colored pill boxes above headings are strictly disallowed. Use semantic Lucide SVG icons (e.g. `CheckCircle2`, `Building2`, `Clock`, `TrendingUp`) and official typography to maintain constitutional and civil service gravitas.

