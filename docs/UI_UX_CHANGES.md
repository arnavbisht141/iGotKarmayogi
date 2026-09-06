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
- **Top Announcement / Marquee Bar:**
  - Restyled to a subtle muted rose / warm dusty-rose container (`bg-[#EAE2E3] text-[#7A4E57] border-b border-[#C8A8A9]/50`).
  - Preserved continuous smooth scrolling marquee animation.
- **Government / Ministry Ribbon:**
  - Transitioned from navy (`bg-slate-900`) to muted rose (`bg-[#965C66] text-white`).
  - Replaced bright amber dot with a subtle palette-consistent indicator (`bg-[#EEE8E9]/90`).
  - Restyled Hindi/English language switcher button to a clean dusty-rose pill (`bg-white/15 hover:bg-white/25 text-white border border-white/20`).
- **Main Navigation Bar:**
  - Clean light background (`bg-white/95 backdrop-blur-md border-b border-[#C8A8A9]/40`).
  - Logo container styled in dark charcoal (`#241E20`) with `#C8A8A9` award icon and `#965C66` MoSPI badge.
  - **Reordered Navigation Flow:**
    `[iGOT Karmayogi Logo] ... [About] [Resources] [Help] [Discover] [Sign In] [Register]`
  - Added subtle placeholder navigation items (`About`, `Resources`, `Help`) with non-functional placeholder links (`#`).
  - Positioned `Discover` immediately to the left of `Sign In`, which is immediately to the left of `Register`.
  - Styled `Register` button with `#965C66` background, white text, and `#824E57` hover state.
  - Styled `Sign In` and `Discover` with rose interactive highlights.
  - Updated mobile navigation menu to match the rose palette and item ordering.

---

### 2. Homepage Hero (`frontend/src/app/page.tsx`)
- **Two-Column Hero Layout:**
  - **Left Column:** Institutional badge (`bg-[#965C66]/10 text-[#965C66] border-[#965C66]/20`), concise headline (*"National Learning Platform for Civil Services"*), clear subtitle, and pill-shaped action buttons (`Official Sign In` and `Explore Courses`).
  - **Right Column:** Compact hero image carousel vertically aligned so its top edge aligns with the left column badge.
  - Clear spacing prevents any text overlap or underlap.
- **Hero Image Carousel & Complete Image Visibility:**
  - Restricted strictly to existing assets: `/karmayogi.jpg`, `/government-meeting.jpg`, and `/ai-daksh.jpg`.
  - Preserved 100% full aspect ratios using `object-contain` inside a clean white frame (`bg-white rounded-xl border border-[#C8A8A9]/50 shadow-xs p-2 sm:p-2.5`).
  - Complete `karmayogi.jpg` image is fully visible (including right-side graphics and text) without aggressive cropping or distortion.
  - Maintained 5-second auto-rotation, smooth fade transitions, previous/next controls, and pagination indicators.

---

### 3. Homepage Statistics (`frontend/src/app/page.tsx`)
- Placed directly beneath the hero inside the **exact same container** (`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8`).
- **Alignment:**
  - Left edge of `40,000+` aligns directly with the left boundary of the hero text content.
  - Right edge of `Verifiable` aligns with the right boundary of the hero carousel card.
  - All four statistics (`40,000+`, `100%`, `UN-NQAF`, `Verifiable`) are strictly **left-aligned** within their respective columns (not centered).
  - Divided by subtle rose dividers (`divide-[#C8A8A9]/35`).

---

### 4. Registration Page (`frontend/src/app/(auth)/register/page.tsx`)
- **Background:** Updated from `bg-slate-50` to `#EEE8E9` warm off-white foundation.
- **Registration Card:** White surface with rounded corners, subtle rose border (`border-[#C8A8A9]/50`), and soft elevation (`shadow-md shadow-[#965C66]/5`).
- **Form Inputs:** Styled with white backgrounds, rose-accented focus rings (`focus-visible:ring-[#965C66]`), and muted rose icons (`text-[#965C66]/60`).
- **Role-Based Customization Callout:** Replaced former amber/orange warning-like styling with a subtle dusty-rose informational box (`bg-[#965C66]/8 border-[#C8A8A9]/50 text-[#44383A]` and `#965C66` header).
- **Submit CTA:** Updated `Create Account & Proceed to Onboarding` button to `#965C66` background, white text, and `#824E57` hover state.
- **Sign In Link:** Updated to `#965C66 hover:text-[#824E57]`.

---

### 5. Official Sign In Page (`frontend/src/app/(auth)/login/page.tsx`)
- Updated background to `#EEE8E9`.
- Refined card elevation, rose focus rings, `#965C66` primary login button, and rose links.
- Updated quick demo credential pills with rose accents.

---

### 6. Floating Karmayogi AI Chatbot Widget (`frontend/src/components/shared/AiAssistantWidget.tsx`)
- **Circular Chatbot Icon:**
  - Collapsed trigger updated to a **perfect circular button** (`h-14 w-14 rounded-full bg-[#965C66] hover:bg-[#824E57] text-white shadow-lg border border-white/20`).
  - Centered Bot robot icon (`h-6 w-6 text-white`) with online status badge.
- **Removal of LangGraph Branding:**
  - Removed all `LangGraph` badges, labels, subtitle strings, and engine labels across both collapsed and open states.
  - Clean user-facing label: `Karmayogi AI` with subtitle *"Civil Service Intelligence Assistant"*.
  - Chat window header styled in `#965C66` with white text.
  - All chat functionality, query handling, and API integration (`/agents/chat`) preserved intact.

---

### 7. Global Layout & Theme Tokens (`frontend/src/app/layout.tsx`, `frontend/src/app/globals.css`)
- Configured `layout.tsx` `<body>` to default to `bg-[#EEE8E9] text-[#241E20]`.
- Registered palette variables in CSS theme tokens.
