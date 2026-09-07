# Aarna — Contribution & Activity Log

> **Name:** Aarna  
> **GitHub Handle:** [@aarna605-dot](https://github.com/aarna605-dot)  
> **Role:** UI/UX Design Lead & Visual Identity Architect  
> **Primary Subsystems:** Design System (Muted Rose Standard), Landing Page Visuals, AI Chatbot Widget Design, Media Asset Framing  

---

## 1. Summary of Responsibilities
Lead visual and UI/UX designer for the project. Established the core **Muted Rose Design System** that eliminated generic, harsh color palettes in favor of public-service dignity and high visual polish. Spearheaded component styling, photograph aspect-ratio integrity, and the visual identity of the Karmayogi AI assistant.

---

## 2. Visible Deliverables (Code & Repository Artifacts)

### 2.1 Muted Rose Design System Foundations (`4380504`, `65dbe6e`)
- Crafted and implemented the core Muted Rose design tokens in Tailwind:
  - Primary `#965C66` for institutional actions and active indicators.
  - Secondary `#C8A8A9` and `#BC9798` for subtle borders and dividers.
  - `#EEE8E9` warm foundation for clean page backgrounds.
  - `#241E20` charcoal text for accessible, high-contrast readability.
- Re-styled login (`/login`) and registration (`/register`) pages with elevated cards, soft rose focus rings (`focus-visible:ring-[#965C66]`), and muted callouts.

### 2.2 Landing Page Hero & Media Integrity (`65dbe6e`)
- Redesigned landing page hero layout into a balanced two-column presentation.
- Implemented auto-rotating image carousel (`/karmayogi.jpg`, `/government-meeting.jpg`, `/ai-daksh.jpg`) with strict `object-contain` framing to protect official photographs from cropping or distortion.
- Styled the left-aligned statistics section with subtle rose dividers (`divide-[#C8A8A9]/35`).

### 2.3 Karmayogi AI Assistant Widget Redesign (`frontend/src/components/shared/AiAssistantWidget.tsx`)
- Redesigned the floating chat assistant from an obtrusive rectangular box into a circular floating launcher (`h-14 w-14 rounded-full bg-[#965C66]`).
- Replaced vendor-specific "LangGraph" engine labels with clean civil-service identity: *"Karmayogi AI - Civil Service Intelligence Assistant"*.

---

## 3. "Invisible" & Offline Contributions

### 3.1 Color Psychology & Civil-Service Aesthetic Research
- Conducted comparative visual research across global civil-service training portals (UK Civil Service Learning, Singapore Civil Service College, and India's iGOT Karmayogi).
- Formulated the Muted Rose palette to strike an optimal balance between official solemnity and modern SaaS elegance.

### 3.2 UI Wireframing & Design Reviews
- Created initial Figma/pen-and-paper wireframes for landing page sections, course card layouts, and mobile drawer views.
- Conducted visual QA across different display resolutions to ensure contrast ratios meet WCAG AA standards.

---

## 4. Chronological Activity Log

| Date | Activity | Category | Notes / Deliverables |
|---|---|---|---|
| `2026-09-06` | Redesigned homepage hero, carousel, and statistics | `Code` / `UI` | Clean two-column layout, preserved photo aspect ratios |
| `2026-09-06` | Redesigned floating AI assistant widget | `Code` / `UI` | Circular launcher, removed third-party vendor labels |
| `2026-09-06` | Merged Muted Rose UI design system pass | `Code` / `UI` | PR #2 merged into `main` |
| `2026-09-05` | Wireframed user flows and created design tokens | `Design` | Defined palette tokens and visual guidelines |

---

## 5. Notes & Context for Future AI Coding Agents
- **Design System Rule:** Always use `#965C66` for primary CTAs and active states. Do not introduce generic Tailwind blues (`bg-blue-600`) or neon accents.
- **Media Rule:** Never apply `object-cover` to official government photographs without verifying aspect ratio; use `object-contain` within framed white containers.
