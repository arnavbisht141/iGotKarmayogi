# 🎨 UI/UX Design System: The Muted Rose & Institutional Standard

> **Status:** `Implemented` (Phase 0)  
> **Primary Files:**  
> - Styles: `frontend/src/app/globals.css`, `frontend/tailwind.config.ts`  
> - Components: `Navbar.tsx`, `Footer.tsx`, `AiAssistantWidget.tsx`, `frontend/src/app/page.tsx`  

---

## 1. Executive Summary & Design Philosophy

The **iGOT Karmayogi (MoSPI)** platform adheres to an institutional design standard that reflects public-service dignity:
- **No Overbearing AI Gimmicks:** Avoid glowing neon cyan/purple gradients or floating cybernetic bots. Styling is clean, authoritative, and dignified.
- **Harmonious Color Palette:** Built upon the **Muted Rose Standard** paired with official Government of India **Navy and Slate tokens**.
- **Visual Stability:** Zero-shift navigation tabs, macOS trackpad momentum preservation, and single-viewport landing page section gliding.
- **Asset Integrity:** Never crop or distort official photographs or infographics. Use `object-contain` within rounded, framed cards.

---

## 2. Design System Color Tokens

| Token Name | Hex Code | Purpose & Application |
|---|---|---|
| **Primary (Muted Rose)** | `#965C66` | Key CTAs, active indicators, borders, brand icons. |
| **Secondary** | `#C8A8A9` | Subtle borders, secondary accents, frame dividers. |
| **Supporting** | `#BC9798` | Intermediate accents, badge outlines, progress highlights. |
| **Light Supporting** | `#C2A0A2` | Delicate borders, hover accents, subtle dividers. |
| **Main Warm Background** | `#EEE8E9` | Warm off-white foundation for hero, register, and main pages. |
| **Charcoal Text** | `#241E20` | High-contrast readable typography for headings and body. |
| **Muted Charcoal** | `#5A5052` / `#7A4E57` | Subtitles, helper text, breadcrumbs, and secondary labels. |
| **Official Navy** | `#1E3A8A` / `#1D3557` | Official Government of India ribbon, primary buttons, active links. |
| **Official Slate / Neutral** | `#0F172A` / `#F8FAFC` | Authoritative titles, clean neutral layout surfaces. |

---

## 3. Structural & Interaction Patterns

### 3.1 Single-Viewport Section Architecture (`frontend/src/app/page.tsx`)
Landing page sections (`#hero`, `#about`, `#how-it-works`, `#resources`, `#help`) are styled with:
```tsx
className="scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center"
```
Clicking any navigation item glides directly to and frames that section cleanly in the viewport without awkward cutoffs or extra blank spaces.

### 3.2 Precision Smooth Scrolling & Trackpad Momentum
- **Elimination of Compounding Offsets:** Removed `scroll-padding-top: 120px` from `globals.css` and rely solely on `scroll-mt-[120px]`.
- **macOS Inertia Restoration:** Removed global `html { scroll-behavior: smooth; }` to prevent browser collisions with macOS trackpad inertial physics. Smooth transitions are handled programmatically via `window.scrollTo({ behavior: "smooth" })` on anchor clicks.
- **Scroll-Spy Lock:** Employs `isProgrammaticScrollRef` during programmatic anchor scrolling to prevent intermediate tabs from flickering mid-flight.

### 3.3 Zero-Blink & Zero-Shift Tab Navigation (`Navbar.tsx`)
- Standardized fixed 1px borders (`border-transparent` on inactive, `border-blue-200` on active) to eliminate 2–3px box-model layout shifts when toggling tabs.
- Maintained constant `font-medium` across active and inactive states to avoid font-metric width jumps.
- Anchor links configure `scroll={false}` and `prefetch={false}` to prevent Next.js router full-page flickers.

### 3.4 Context-Aware Institutional Footer (`Footer.tsx`)
- Dynamic client component rendering:
  - Omitted on the landing page (`pathname === "/"`) so that `#help`'s integrated dark CTA and legal ribbon sits flush at the bottom.
  - Automatically rendered on all inner views (`/discover`, `/login`, `/register`, `/home`, etc.).

---

## 4. Rules & Operational Guidelines for AI Coding Agents

> [!CAUTION]
> **No Generic Neon Colors:**
> Do NOT introduce generic bright blues (`bg-blue-600`), neon emeralds, or purples. All accents must strictly use the curated tokens above.

> [!IMPORTANT]
> **Aspect Ratio Preservation:**
> All official institutional media (such as `/karmayogi.jpg`, `/government-meeting.jpg`, `/ai-daksh.jpg`) MUST retain natural aspect ratios using `object-contain` within framed white containers. Never distort images with `object-cover` without review.
