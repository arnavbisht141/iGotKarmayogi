# Diwakar Ujjwal — Contribution & Activity Log

> **Name:** Diwakar Ujjwal  
> **GitHub Handle:** [@diwakarujjwal](https://github.com/diwakarujjwal)  
> **Role:** Frontend UX & Interaction Engineer  
> **Primary Subsystems:** Landing Page Section Architecture, Smooth Scroll Mechanics, Trackpad Inertia, Dynamic Navigation, Footer System  

---

## 1. Summary of Responsibilities
Frontend engineering lead for landing page navigation, viewport layout stability, scroll mechanics, and responsive interaction design. Focused on creating an institutional, fluid, and glitch-free navigation experience matching official Government of India portal standards.

---

## 2. Visible Deliverables (Code & Repository Artifacts)

### 2.1 Single-Viewport Section Gliding Architecture (`44c8e92`, `78c166c`)
- Implemented single-viewport landing page architecture across `#hero`, `#about`, `#how-it-works`, `#resources`, and `#help`.
- Configured `scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center` ensuring sections land flush beneath the sticky navbar.

### 2.2 Smooth Scrolling Optimization & macOS Trackpad Inertia (`44c8e92`)
- Eliminated compounding scroll offset bug caused by simultaneous `scroll-padding-top: 120px` in `globals.css` and section `scroll-mt-[120px]`.
- Removed global `html { scroll-behavior: smooth; }` to restore native macOS trackpad inertia and eliminate 120Hz momentum conflicts.
- Built programmatic scroll handler with `isProgrammaticScrollRef` lock to prevent the scroll-spy listener from cycling intermediate tabs during flight.

### 2.3 Zero-Blink & Zero-Shift Tab Navigation (`b3d3e92`)
- Fixed layout jitter and button width shifts during hover and active state toggling by standardizing constant 1px borders (`border-transparent` vs `border-blue-200`) and uniform `font-medium`.
- Applied `scroll={false}` and `prefetch={false}` to anchor Links, preventing Next.js router full-page flickers.

### 2.4 Context-Aware Dynamic Footer Architecture (`frontend/src/components/shared/Footer.tsx`)
- Engineered dynamic client `<Footer />` component that automatically suppresses duplicate footers on the landing page (allowing `#help`'s integrated dark CTA bar to sit flush at the bottom) while auto-rendering on inner portal pages.

### 2.5 Navbar Brand & Statistics Polish (`65453e4`, `a5e73e6`, `5562fdd`)
- Refined top navbar brand layout, Government of India ribbon, and active indicators.
- Aligned hero headline and statistics section with the official navy aesthetic (`#1E3A8A`).

---

## 3. "Invisible" & Offline Contributions

### 3.1 Interaction Physics Prototyping & Browser Profiling
- Profiled scrolling frame rates and tab switching performance across Chromium and WebKit engines to diagnose micro-stutter and scroll offset compounding.
- Iterated on bounding-box calculation algorithms to determine optimal viewport-center proximity math for the active navigation indicator.

### 3.2 Landing Page Compact Footprint Design
- Re-architected `#how-it-works` content density to fit cleanly within standard 768px/900px laptop vertical viewports without internal scrollbars.

---

## 4. Chronological Activity Log

| Date | Activity | Category | Notes / Deliverables |
|---|---|---|---|
| `2026-09-07` | Aligned hero and statistics with navy aesthetic | `Code` / `UI` | PR #6 merged into `main` |
| `2026-09-07` | Refined navbar brand and ministry ribbon | `Code` / `UI` | Clean institutional branding |
| `2026-09-06` | Viewport-snap navigation and scroll refinement merge | `Code` / `UX` | Restored trackpad inertia, fixed offset compounding |
| `2026-09-06` | Fixed button blink and layout shift during scroll | `Code` / `UX` | Standardized 1px borders and scroll-spy lock |
| `2026-09-06` | Dynamic footer implementation | `Code` / `UI` | Context-aware footer rendering |
| `2026-09-06` | Git repository cleanup | `DevOps` | Removed untracked `.venv` directory from git tracking |

---

## 5. Notes & Context for Future AI Coding Agents
- **Smooth Scroll Standard:** Do NOT re-add `html { scroll-behavior: smooth; }` or `scroll-padding-top` to `globals.css`. Smooth scrolling must remain purely programmatic via `window.scrollTo({ behavior: "smooth" })` to avoid breaking trackpad physics.
- **Navbar Layout Shift Prevention:** Maintain identical padding and 1px border widths on active and inactive tab classes to prevent box-model jitter.
