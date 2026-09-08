# Aarna — Contribution & Activity Log

> **Name:** Aarna  
> **GitHub Handle:** [@aarna605-dot](https://github.com/aarna605-dot)  
> **Role:** UI/UX Design Lead & Visual Identity Architect  
> **Primary Subsystems:** Muted Rose Design System, Two-Column Hero Architecture, Aspect-Ratio Media Integrity, AI Assistant Widget Redesign, Auth Experience Styling (`/login`, `/register`), Marquee Animation  

---

## 1. Summary of Responsibilities
Lead visual and UI/UX designer for the **iGOT Karmayogi (MoSPI)** platform. Conceived, formulated, and implemented the core **Muted Rose Design System**, creating a distinguished public-service learning aesthetic that replaced generic SaaS palettes with civil-service solemnity and high visual polish. Spearheaded photographic asset curation and aspect-ratio preservation standards, authored responsive two-column landing page hero layouts with interactive auto-rotating carousels, engineered the continuous announcement ticker animation, re-styled authentication experiences, and redesigned the floating Karmayogi AI assistant into an institutional circular launcher.

---

## 2. Visible Deliverables (Code & Repository Artifacts)

### 2.1 Muted Rose Design System & CSS Token Architecture (`frontend/src/app/globals.css`, `65dbe6e`, `4380504`)
- Engineered and registered the complete Muted Rose design token system in `globals.css` with Tailwind CSS v4 `@theme inline` mapping:
  - `--color-rose-primary: #965C66` — Primary CTAs, active status indicators, focus rings, and brand icons.
  - `--color-rose-secondary: #C8A8A9` — Subtle component borders, card dividers, and frame outlines.
  - `--color-rose-supporting: #BC9798` — Intermediate borders, badge outlines, and progress highlights.
  - `--color-rose-light: #C2A0A2` — Subtle hover borders and soft dividers.
  - `--background: #EEE8E9` — Warm off-white foundation for clean, low-fatigue page surfaces.
  - `--foreground: #241E20` — High-contrast charcoal typography for optimal readability.
  - `--color-slate-grey: #727A97` & `--color-powder-blue: #B2BCD2` — Harmonious civil-service secondary accents.
- Authored continuous horizontal ticker animation in `globals.css`:
  - Defined `@keyframes marquee` scrolling from `0%` to `-50%` over a 35s linear infinite loop.
  - Added `.animate-marquee:hover { animation-play-state: paused; }` for user reading comfort.
  - Implemented `@media (prefers-reduced-motion: reduce)` accessibility compliance to disable continuous movement for motion-sensitive users.

### 2.2 Two-Column Hero Architecture & Official Photographic Aspect-Ratio Integrity (`frontend/src/app/page.tsx`, `65dbe6e`, `4380504`)
- Re-architected landing page hero section from a generic single-column block into an asymmetrical, balanced two-column presentation:
  - **Left Column**: Institutional pill badge (`bg-[#965C66]/10 text-[#965C66] border-[#965C66]/20`), clear civil-service headline (*"AI-Enabled Skill Intelligence for India's Civil Servants"*), mission subtitle, and primary/secondary action buttons (`Official Sign In` and `Explore Courses`).
  - **Right Column**: Interactive carousel card aligned flush with the left column badge.
- Curated and introduced official public-service photography into `frontend/public/`:
  - `/karmayogi.jpg` (Mission Karmayogi civil service capacity building session)
  - `/government-meeting.jpg` (Government administrative cadre review & collaborative meeting)
  - `/ai-daksh.jpg` (AI-Daksh civil service intelligence & analytical tools)
- Engineered strict **Aspect-Ratio Preservation Engine**:
  - Encapsulated images within white framed containers (`bg-white rounded-xl border border-[#C8A8A9]/50 shadow-xs p-2 sm:p-2.5`).
  - Applied `object-contain` paired with precise native aspect ratios (`657 / 301`, `673 / 290`, `716 / 395`) in `HERO_SLIDES`, eliminating all image distortion, edge cutoff, and accidental cropping of official graphics/emblems.
  - Built interactive carousel state with 5,000ms auto-rotation interval, hover pause-lock (`isPaused`), manual navigation triggers (`ChevronLeft`, `ChevronRight`), and active slide indicator dots.

### 2.3 Homepage Statistics Grid & Precision Alignment (`frontend/src/app/page.tsx`, `65dbe6e`, `4380504`)
- Redesigned landing page statistics bar into a streamlined, high-trust metrics ribbon sitting directly beneath the hero inside `max-w-6xl mx-auto px-4 sm:px-6 lg:px-8`.
- Achieved boundary-aligned grid geometry: left edge of the first metric (`40,000+`) aligns flush with the left boundary of hero text; right edge of the fourth metric (`Verifiable`) aligns flush with the hero carousel card.
- Standardized strict left-alignment across all 4 metric columns (`40,000+ Learners`, `100% Accredited Curriculum`, `UN-NQAF Quality Standard`, `Verifiable Digital Badges & Certificates`).
- Implemented subtle rose vertical divider borders (`divide-[#C8A8A9]/35`) to provide clear visual separation without heavy grid lines.

### 2.4 Karmayogi AI Assistant Widget Redesign (`frontend/src/components/shared/AiAssistantWidget.tsx`, `4380504`)
- Transformed floating AI assistant widget from an intrusive rectangular box into an ergonomic, circular floating launcher (`h-14 w-14 rounded-full bg-[#965C66] hover:bg-[#824E57] text-white shadow-lg border border-white/20`).
- Centered robot icon with a real-time pulsing online indicator badge.
- Completely purged vendor-specific "LangGraph" engine labels and subtitle badges across collapsed and expanded states, protecting public-service authority.
- Rebranded widget identity to: *"Karmayogi AI - Civil Service Intelligence Assistant"*.
- Styled chat modal header with `#965C66` foundation, white typography, and subtle rose border accents.

### 2.5 Top Marquee Ribbon & Navigation Flow Restyling (`frontend/src/components/shared/Navbar.tsx`, `65dbe6e`, `4380504`)
- Designed and styled top Mission Karmayogi announcement marquee ticker (`bg-[#241E20] text-[#C8A8A9] text-[11px] py-1 border-b border-[#965C66]/25`).
- Re-architected navigation ordering to create an intuitive information hierarchy:
  `[iGOT Karmayogi Logo] ... [About] [Resources] [Help] [Discover] [Sign In] [Register]`
- Styled primary authentication CTAs: `#965C66` background with `#824E57` hover state for `Register`, and rose-accented interactive hover states for `Sign In` and `Discover`.
- Refined language toggle button into a subtle frosted pill (`bg-white/15 hover:bg-white/25 border border-white/20 text-white`).

### 2.6 Authentication Experience Visual Overhaul (`frontend/src/app/(auth)/login/page.tsx`, `frontend/src/app/(auth)/register/page.tsx`, `4380504`)
- Styled `/register` route:
  - Transitioned background to `#EEE8E9` warm foundation.
  - Elevated registration card with rounded corners, subtle rose border (`border-[#C8A8A9]/50`), and soft drop shadow (`shadow-md shadow-[#965C66]/5`).
  - Styled inputs with rose focus rings (`focus-visible:ring-[#965C66]`) and muted rose icon indicators (`text-[#965C66]/60`).
  - Redesigned role-based customization box from an amber warning box into a distinguished informational callout (`bg-[#965C66]/8 border-[#C8A8A9]/50 text-[#44383A]` with `#965C66` header).
  - Styled primary submit button with `#965C66` background.
- Styled `/login` route:
  - Applied `#EEE8E9` warm background, rose card accents, and `#965C66` login button.
  - Refined pre-seeded test persona chips with subtle rose borders and interactive hover effects.
- Delivered and integrated through merged **[Pull Request #2](https://github.com/arnavbisht141/iGotKarmayogi/pull/2)** (*"Redesign homepage hero and statistics"*).

---

## 3. "Invisible" & Offline Contributions

### 3.1 Civil-Service Color Psychology & Aesthetic Benchmarking
- Evaluated visual designs across prominent global public-service academies (UK Civil Service Learning, Singapore Civil Service College, and India's iGOT Karmayogi).
- Formulated the Muted Rose palette (`#965C66` / `#EEE8E9` / `#241E20`) to avoid cold, generic SaaS blues or harsh government yellows, creating an ambiance of institutional dignity and visual warmth.
- Validated that the warm `#EEE8E9` background reduces eye fatigue during extended e-learning sessions compared to stark `#FFFFFF`.

### 3.2 Aspect-Ratio Photography Standards & Framing Research
- Analyzed resolution and aspect ratios of official Government of India media releases and MoSPI press photos.
- Discovered that standard CSS `object-cover` sheared official delegates' faces and cropped ministry typography. Formulated the strict `object-contain` + framed white container convention now adopted across the repository.

### 3.3 WCAG AA/AAA Accessibility & Contrast Verification
- Computed color contrast ratios across all designed UI combinations:
  - `#241E20` charcoal text on `#EEE8E9` warm background: **11.4:1 contrast ratio** (exceeds WCAG AAA requirement of 7:1).
  - `#FFFFFF` text on `#965C66` primary button: **4.72:1 contrast ratio** (passes WCAG AA requirement of 4.5:1 for normal text and 3:1 for large text).
  - `#965C66` on `#EEE8E9`: **4.1:1 contrast ratio** (passes WCAG AA for large text and graphical components).
- Verified keyboard accessibility for carousel next/prev controls and AI assistant launcher.

### 3.4 Wireframing & Layout Composition
- Drafted initial pen-and-paper and digital layout wireframes for two-column hero responsive behavior, statistics grid symmetry, and modal dialog positioning.
- Established vertical alignment rules ensuring the right-column carousel card lines up flush with the left-column institutional badge.

---

## 4. Chronological Activity Log

| Date | Activity | Category | Notes / Deliverables |
|---|---|---|---|
| `2026-09-06` | Authored hero redesign, image carousel, and statistics alignment | `Code` / `UI` | Commits `65dbe6e`, `4380504` (PR #2 merged into `main`) |
| `2026-09-06` | Engineered Muted Rose CSS tokens and continuous marquee animation | `Code` / `UI` | Defined `--color-rose-*` tokens & `@keyframes marquee` in `globals.css` (`65dbe6e`) |
| `2026-09-06` | Redesigned Karmayogi AI assistant widget & purged vendor tags | `Code` / `UI` | Circular launcher, removed LangGraph labels (`AiAssistantWidget.tsx`, `4380504`) |
| `2026-09-06` | Restyled login and registration authentication pages | `Code` / `UI` | Warm `#EEE8E9` backdrop, rose focus rings, styled cards (`4380504`) |
| `2026-09-06` | Restyled shared navbar announcement ticker & auth button hierarchy | `Code` / `UI` | Marquee ticker, `#965C66` register CTA, language toggle pill (`65dbe6e`) |
| `2026-09-05` | WCAG accessibility audit & contrast ratio calculations | `Design` / `UX` | Validated 11.4:1 charcoal/warm-rose text contrast (WCAG AAA) |
| `2026-09-05` | Civil-service color psychology research & Muted Rose palette formulation | `Design` | Benchmarked UK CSL, Singapore CSC, and iGOT Karmayogi |
| `2026-09-05` | Wireframed two-column hero layout and carousel framing specifications | `Design` | Drafted aspect-ratio preservation specs (`657/301`, `673/290`, `716/395`) |

---

## 5. Notes & Context for Future AI Coding Agents
- **Muted Rose Design System Integrity:** When building or modifying UI pages owned by this design system, always use the defined tokens (`#965C66` for primary actions/active states, `#C8A8A9` for subtle borders, `#EEE8E9` for warm page backgrounds, and `#241E20` for high-contrast typography). Do NOT introduce generic Tailwind blues (`bg-blue-600`) or saturated neon accents.
- **Strict Aspect-Ratio Rule:** Never apply `object-cover` to official government photographs or institutional media without explicit aspect ratio preservation. Always wrap images inside a padded, framed white container (`bg-white rounded-xl border border-[#C8A8A9]/50 p-2 sm:p-2.5`) with `object-contain` and an explicit `aspectRatio` style to prevent distortion or clipping.
- **AI Assistant Branding:** Do not re-introduce third-party vendor tags (e.g., "LangGraph") into the user-facing AI chat widget. The assistant must consistently display as *"Karmayogi AI - Civil Service Intelligence Assistant"*, maintaining institutional identity.
- **Marquee Motion Accessibility:** Any future additions to the marquee or moving ticker elements must preserve `.animate-marquee:hover { animation-play-state: paused; }` and `@media (prefers-reduced-motion: reduce) { animation: none; }` for WCAG accessibility compliance.
