# Aarna — Contribution & Activity Log

> **Name:** Aarna  
> **GitHub Handle:** [@aarna605-dot](https://github.com/aarna605-dot)  
> **Role:** UI/UX Design Lead & Visual Identity Architect  
> **Primary Subsystems:** UI Design System Iterations, Two-Column Hero Architecture, Aspect-Ratio Media Integrity, AI Assistant Widget Redesign, Auth Flows (`/login`, `/register`)  

---

## 1. Summary of Responsibilities
Lead visual and UI/UX designer for the **iGOT Karmayogi (MoSPI)** platform. Spearheaded initial visual identity explorations, prototyping the Muted Rose design system before aligning with the official Government of India Navy & Slate aesthetic. Architected core layout foundations that remain across the platform: the responsive two-column hero, strict photographic aspect-ratio preservation engine, circular Karmayogi AI assistant launcher, and statistics grid alignment.

---

## 2. Visible Deliverables (Code & Repository Artifacts)

### 2.1 Design System Iteration & CSS Token Architecture (`frontend/src/app/globals.css`, `65dbe6e`, `4380504`)
- **Muted Rose Design Prototype (Iteration 1):** Built and mapped custom design tokens (`--color-rose-*`) in Tailwind CSS v4 `@theme inline` as an initial exploration of low-fatigue civil-service palettes.
- **Continuous Marquee Animation:** Authored 35s continuous linear horizontal ticker (`@keyframes marquee`) with hover-pause and `@media (prefers-reduced-motion: reduce)` accessibility compliance.
- **Aesthetic Evolution:** Collaborated on transitioning color tokens to the official Government of India Navy (`#1E3A8A`) and Slate standard while preserving all structural layout rules.

### 2.2 Two-Column Hero Architecture & Photographic Aspect-Ratio Integrity (`frontend/src/app/page.tsx`, `65dbe6e`, `4380504`)
- **Balanced Layout:** Re-architected landing hero from a single-column block into an asymmetrical two-column layout (institutional badge, headline, and CTAs on the left; framed carousel on the right).
- **Official Media Assets:** Sourced and integrated official photography into `frontend/public/`: `/karmayogi.jpg`, `/government-meeting.jpg`, and `/ai-daksh.jpg`.
- **Aspect-Ratio Preservation Engine:** Built framed containers (`bg-white rounded-xl border border-slate-200 shadow-xs p-2 sm:p-2.5`) enforcing `object-contain` and exact native aspect ratios (`657/301`, `673/290`, `716/395`), eliminating distortion and face-cropping in official media.
- **Interactive Carousel:** Implemented 5s auto-rotation, hover pause-lock (`isPaused`), manual navigation triggers, and slide indicator dots.

### 2.3 Homepage Statistics Grid & Boundary Alignment (`frontend/src/app/page.tsx`, `65dbe6e`, `4380504`)
- Streamlined statistics bar directly beneath the hero within `max-w-6xl mx-auto`.
- Standardized strict left-alignment across all four metrics (`40,000+ Learners`, `100% Accredited Curriculum`, `UN-NQAF Standard`, `Verifiable Certificates`).
- Aligned grid boundaries flush with hero text (left) and carousel card (right), separated by subtle dividers.

### 2.4 Karmayogi AI Assistant Widget Redesign (`frontend/src/components/shared/AiAssistantWidget.tsx`, `4380504`)
- **Circular Launcher:** Redesigned floating trigger from an intrusive rectangular box into an ergonomic circular launcher (`h-14 w-14 rounded-full text-white shadow-lg`).
- **Civil-Service Rebranding:** Completely purged vendor-specific "LangGraph" engine labels across collapsed and expanded states; rebranded to *"Karmayogi AI - Civil Service Intelligence Assistant"*.
- Added real-time pulsing online status indicator and styled the chat modal container.

### 2.5 Top Announcement Ticker & Navigation Flow (`frontend/src/components/shared/Navbar.tsx`, `65dbe6e`, `4380504`)
- Styled top Mission Karmayogi announcement marquee ticker.
- Re-architected navigation ordering: `[Logo] ... [About] [Resources] [Help] [Discover] [Sign In] [Register]`.
- Styled primary authentication CTAs and refined the bilingual language toggle pill.

### 2.6 Authentication Experience Visual Pass (`login/page.tsx`, `register/page.tsx`, `4380504`)
- Elevated `/register` and `/login` cards with clean rounded borders, subtle elevation, and responsive focus rings.
- Redesigned role-based customization callout into a distinguished informational box.
- Delivered through merged **[Pull Request #2](https://github.com/arnavbisht141/iGotKarmayogi/pull/2)** (*"Redesign homepage hero and statistics"*).

---

## 3. "Invisible" & Offline Contributions

### 3.1 Civil-Service Visual Research & Aesthetic Benchmarking
- Benchmarked global public-service platforms (UK Civil Service Learning, Singapore Civil Service College, India's iGOT Karmayogi) to balance public-service solemnity with modern UI ergonomics.
- Researched low-fatigue background tones to enhance readability during long training sessions.

### 3.2 Photographic Quality & Framing Guidelines
- Analyzed Government of India media releases to establish repository-wide image standards, identifying that naive `object-cover` sheared delegate faces and cropped official insignia.

### 3.3 WCAG AA/AAA Accessibility Verification
- Audited contrast ratios across UI elements: verified 11.4:1 contrast for charcoal text on light backgrounds (WCAG AAA) and 4.7:1 for primary action buttons (WCAG AA).
- Verified keyboard accessibility for carousel controls and the AI assistant launcher.

### 3.4 Wireframing & Responsive Prototyping
- Drafted initial layout wireframes for two-column hero responsiveness, carousel framing, and mobile drawer adaptations.

---

## 4. Chronological Activity Log

| Date | Activity | Category | Notes / Deliverables |
|---|---|---|---|
| `2026-09-06` | Authored hero redesign, image carousel, and statistics alignment | `Code` / `UI` | Commits `65dbe6e`, `4380504` (PR #2 merged into `main`) |
| `2026-09-06` | Built CSS tokens and continuous marquee animation | `Code` / `UI` | Keyframe animation and tokens in `globals.css` (`65dbe6e`) |
| `2026-09-06` | Redesigned Karmayogi AI assistant widget & de-branded vendor tags | `Code` / `UI` | Circular launcher, institutional branding (`AiAssistantWidget.tsx`) |
| `2026-09-06` | Styled login and registration authentication cards | `Code` / `UI` | Elevated card surfaces and focus ring states (`4380504`) |
| `2026-09-06` | Restyled shared navbar announcement ticker & auth button hierarchy | `Code` / `UI` | Navigation flow reordering and CTAs (`65dbe6e`) |
| `2026-09-05` | WCAG accessibility audit & contrast ratio calculations | `Design` / `UX` | Validated 11.4:1 text contrast standard |
| `2026-09-05` | Public-service visual benchmarking & design system prototyping | `Design` | Researched UK CSL, Singapore CSC, and iGOT Karmayogi |
| `2026-09-05` | Wireframed two-column hero layout and carousel framing specifications | `Design` | Defined native aspect ratios (`657/301`, `673/290`, `716/395`) |

---

## 5. Notes & Context for Future AI Coding Agents
- **Active Color Standard:** The platform uses the official Government of India **Navy (`#1E3A8A` / `#1D3557`) and Slate** aesthetic. Do NOT re-apply Muted Rose or introduce generic neon accents.
- **Strict Photographic Framing:** Never apply unconstrained `object-cover` to official institutional photographs. Always wrap images in framed containers with `object-contain` and explicit native aspect ratios to prevent distortion or clipping.
- **AI Assistant Branding:** Maintain the circular launcher trigger and institutional title *"Karmayogi AI - Civil Service Intelligence Assistant"*. Do not re-introduce third-party vendor tags (e.g., LangGraph).
- **Motion Accessibility:** Preserve `.animate-marquee:hover { animation-play-state: paused; }` and `@media (prefers-reduced-motion: reduce)` compliance on any animated ticker components.
