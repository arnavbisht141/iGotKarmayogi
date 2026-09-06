# Coordinated UI/UX Refinement Changelog

## 🎨 Overview & Design System

A visual redesign was implemented across the frontend of **iGOT Karmayogi (MoSPI)** to create a clean, focused public-service learning platform. The redesign eliminates old navy-heavy surfaces and bright amber/yellow accents in favor of a **muted rose design system**.

### Design Palette Tokens
| Token | Color Code | Role / Usage |
|---|---|---|
| **Primary** | `#965C66` | Key CTAs, active indicators, borders, icon accents, brand highlights |
| **Secondary** | `#C8A8A9` | Subtle borders, secondary accents, frame dividers |
| **Supporting** | `#BC9798` | Intermediate accents, badge outlines, progress highlights |
| **Light Supporting** | `#C2A0A2` | Delicate borders, hover accents, subtle dividers |
| **Main Warm Background** | `#EEE8E9` | Warm off-white foundation for hero, register, and main pages |
| **Charcoal Text** | `#241E20` | High-contrast readable typography for headings and body |
| **Muted Charcoal** | `#5A5052` / `#7A4E57` | Subtitles, helper text, and secondary copy |

---

## 📋 Detailed Changes by Component & Scope

### 1. Shared Header & Top Navigation (`frontend/src/components/shared/Navbar.tsx`)
- **Top Announcement Bar:**
  - Restyled to a subtle muted rose container (`bg-[#EAE2E3] text-[#7A4E57] border-b border-[#C8A8A9]/50`).
  - Preserved continuous smooth scrolling marquee animation.
- **Government Ribbon:**
  - Transitioned from navy (`bg-slate-900`) to muted rose (`bg-[#965C66] text-white`).
  - Replaced bright amber dot with a subtle indicator (`bg-[#EEE8E9]/90`).
  - Restyled Hindi/English language switcher button to a dusty-rose pill (`bg-white/15 hover:bg-white/25 text-white border border-white/20`).
- **Main Navigation Bar & Functional Flow:**
  - Clean light background (`bg-white/95 backdrop-blur-md border-b border-[#C8A8A9]/40`).
  - Logo container styled in dark charcoal (`#241E20`) with `#C8A8A9` award icon and `#965C66` MoSPI badge.
  - Complete navigation order: `[iGOT Karmayogi Logo] ... [About] [How it Works] [Resources] [Help] [Discover] [Sign In] [Register]`.
  - Reconnected all navbar links to their respective landing page sections (`#about`, `#how-it-works`, `#resources`, `#help`).
- **Zero-Blink & Zero-Shift Tab States:**
  - Standardized fixed 1px borders (`border-transparent` on inactive, `border-[#965C66]/20` on active) to eliminate 2–3px box-model layout shifts when toggling tabs.
  - Maintained consistent `font-medium` across all states to prevent font-metric width jumps.
  - Added `transition-all duration-200 ease-out` for soft color transitions.
  - Added `scroll={false}` and `prefetch={false}` to anchor `<Link>` elements, eliminating Next.js router transitions and screen flicker.
- **Action Buttons:**
  - `Discover`: Positioned directly left of `Sign In` with proportional compact sizing (`text-xs`, `py-1.5`, `h-3.5 w-3.5` Compass icon).
  - `Sign In`: Styled with subtle rose hover highlights.
  - `Register`: Primary CTA styled with `#965C66` background, white text, and `#824E57` hover state.
- **Bilingual & Mobile Support:**
  - Full Hindi/English translation coverage (`nav.about`, `nav.howItWorks`, `nav.resources`, `nav.help`).
  - Mobile drawer mirrors all desktop anchor links, styling, and zero-shift borders.

---

### 2. Landing Page Full-Height Section Architecture (`frontend/src/app/page.tsx`)
- **Single-Viewport Section Architecture:**
  - Configured each landing section with `scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center`.
  - Clicking any navigation item smoothly glides to and frames only that section in the viewport without cutoffs or blank spaces.
- **Hero & Statistical Dashboard (`#hero`):**
  - **Two-Column Hero Layout:**
    - Left Column: Institutional badge (`bg-[#965C66]/10 text-[#965C66] border-[#965C66]/20`), concise headline (*"National Learning Platform for Civil Services"*), subtitle, and pill-shaped action buttons (`Official Sign In` and `Explore Courses`).
    - Right Column: Compact hero image carousel vertically aligned with the left badge. Restricted strictly to existing MoSPI assets (`/karmayogi.jpg`, `/government-meeting.jpg`, `/ai-daksh.jpg`) with full aspect ratio visibility (`object-contain`), white frame, 5s auto-rotation, and pagination indicators.
  - **Aligned Statistics Bar:**
    - Placed directly beneath the hero in the exact same container (`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8`).
    - Left edge of `40,000+` aligns with the hero text boundary; right edge of `Verifiable` aligns with the carousel card.
    - All four statistics (`40,000+`, `100%`, `UN-NQAF`, `Verifiable`) are left-aligned within their respective columns and separated by subtle rose dividers (`divide-[#C8A8A9]/35`).
- **Institutional Overview & Competency Framework (`#about`):**
  - Left: Dark charcoal card with NPCSCB Framework verified badge and 3 real-time competency matrix bars (Official Statistical Cadre, Accredited Assessments, AI Copilot).
  - Right: Core Institutional Pillars title, subtitle, and 3 icon-driven pillar rows (Statistical Integrity, Certified Standardized Assessments, AI-Orchestrated Assistant).
- **Structured Karmayogi Journey (`#how-it-works`):**
  - 4-Step connected horizontal progression track: `1. Onboard Role` ➔ `2. Discover & Study` ➔ `3. Pass Assessment` ➔ `4. Earn Certificate`.
  - 3 Public Servant Benefit cards (Career Progression & APAR, Standardized National Training, Autonomous On-Demand Learning).
  - Compacted vertical footprint (~450px content height) ensuring the progression track and all 3 cards fit cleanly within the viewport on laptop displays without internal scrolling.
- **Official Cadre Reference Manuals (`#resources`):**
  - 4 Institutional technical cards (NSSO Field Enumerator Manual, CPI & IIP Technical Manual, UN-NQAF Quality Rubrics, CAPI Operations Manual) with metadata tags, file format indicators, and direct catalogue access buttons.
- **Official Training Helpdesk & Integrated Closing (`#help`):**
  - 3 Support channels: 24/7 AI Copilot, Ministry Training Desk (with MoSPI email, toll-free number, and operating hours), and FAQ questions card.
  - Full-width dark charcoal closing CTA bar (*"Ready to advance your official competencies?"*) with Sign In and Register actions.
  - Integrated MoSPI legal and copyright ribbon (`Privacy Policy • Terms of Service • Data Governance • Helpdesk`), making `#help` a self-contained closing screen.

---

### 3. Precision Smooth Scrolling & Trackpad Momentum (`frontend/src/app/globals.css`, `frontend/src/components/shared/Navbar.tsx`)
- **Elimination of Dual Offset Collision:**
  - Removed `scroll-padding-top: 120px` from `globals.css` and relied solely on section `scroll-mt-[120px]`.
  - Prevents browsers from compounding both rules (240px offset), ensuring sections land flush directly beneath the 120px sticky navbar.
- **macOS Trackpad Inertia Restoration:**
  - Removed global `html { scroll-behavior: smooth; }` from CSS.
  - Eliminates conflicts between CSS smooth scrolling and macOS trackpad inertial physics, restoring silky 120Hz momentum scrolling.
  - Smooth animation is handled purely programmatically via `window.scrollTo({ behavior: "smooth" })` on anchor clicks.
- **Programmatic Scroll Lock & Proximity Tracking:**
  - Added an `isProgrammaticScrollRef` lock during programmatic scrolling to prevent the scroll-spy listener from cycling intermediate tabs mid-flight.
  - Active section during manual scroll is calculated by finding the section whose center is closest to the viewport's center, eliminating tab flickering.
  - Includes edge locks for `#hero` (top < 80px) and `#help` (bottom within 60px of document height).

---

### 4. Context-Aware Institutional Footer Architecture (`frontend/src/components/shared/Footer.tsx`, `frontend/src/app/layout.tsx`)
- **Dynamic `<Footer />` Rendering:**
  - Replaced hardcoded `<footer>` in `layout.tsx` with a context-aware client `<Footer />` component.
  - Omitted on the landing page (`pathname === "/"`) to avoid rendering a duplicate white footer below `#help`'s integrated dark CTA bar, allowing `#help` to sit flush at the bottom.
  - Automatically rendered on all inner pages (`/discover`, `/login`, `/register`, `/home`, etc.) to maintain standard government footer guidelines.

---

### 5. Registration Page (`frontend/src/app/(auth)/register/page.tsx`)
- **Background:** Updated from `bg-slate-50` to `#EEE8E9` warm off-white foundation.
- **Registration Card:** White surface with rounded corners, subtle rose border (`border-[#C8A8A9]/50`), and soft elevation (`shadow-md shadow-[#965C66]/5`).
- **Form Inputs:** Styled with white backgrounds, rose-accented focus rings (`focus-visible:ring-[#965C66]`), and muted rose icons (`text-[#965C66]/60`).
- **Role-Based Customization Callout:** Replaced former amber/orange warning-like styling with a subtle dusty-rose informational box (`bg-[#965C66]/8 border-[#C8A8A9]/50 text-[#44383A]` and `#965C66` header).
- **Submit CTA:** Updated `Create Account & Proceed to Onboarding` button to `#965C66` background, white text, and `#824E57` hover state.
- **Sign In Link:** Updated to `#965C66 hover:text-[#824E57]`.

---

### 6. Official Sign In Page (`frontend/src/app/(auth)/login/page.tsx`)
- Updated background to `#EEE8E9`.
- Refined card elevation, rose focus rings, `#965C66` primary login button, and rose links.
- Updated quick demo credential pills with rose accents.

---

### 7. Floating Karmayogi AI Chatbot Widget (`frontend/src/components/shared/AiAssistantWidget.tsx`)
- **Circular Chatbot Icon:**
  - Collapsed trigger updated to a circular button (`h-14 w-14 rounded-full bg-[#965C66] hover:bg-[#824E57] text-white shadow-lg border border-white/20`).
  - Centered Bot robot icon (`h-6 w-6 text-white`) with online status badge.
- **Removal of LangGraph Branding:**
  - Removed all `LangGraph` badges, labels, subtitle strings, and engine labels across both collapsed and open states.
  - Clean user-facing label: `Karmayogi AI` with subtitle *"Civil Service Intelligence Assistant"*.
  - Chat window header styled in `#965C66` with white text.
  - All chat functionality, query handling, and API integration (`/agents/chat`) preserved intact.

---

### 8. Global Layout & Theme Tokens (`frontend/src/app/layout.tsx`, `frontend/src/app/globals.css`)
- Configured `layout.tsx` `<body>` to default to `bg-[#EEE8E9] text-[#241E20]`.
- Registered palette variables in CSS theme tokens.
