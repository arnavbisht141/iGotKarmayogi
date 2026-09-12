# Diwakar Ujjwal — Contribution & Activity Log

> **Name:** Diwakar Ujjwal  
> **GitHub Handle:** [@diwakarujjwal](https://github.com/diwakarujjwal)  
> **Role:** Frontend UX & Interaction Engineer  
> **Primary Subsystems:** Landing Page Section Architecture, Smooth Scroll Mechanics, Dynamic Navigation, Viewport Layout Stability, Footer System  

---

## 1. Summary of Responsibilities
Frontend engineering lead for landing page navigation, viewport layout stability, scroll mechanics, and responsive interaction design. Focused on creating an institutional, fluid, and glitch-free navigation experience matching official Government of India portal standards.

---

## 2. Visible Deliverables (Code & Repository Artifacts)

### 2.1 Single-Viewport Section Gliding Architecture (`fdab73f`, `78c166c`, `44c8e92`)
- Implemented single-viewport landing page architecture across `#hero`, `#about`, `#how-it-works`, `#resources`, and `#help`.
- Configured `scroll-mt-[120px] min-h-[calc(100vh-120px)] flex flex-col justify-center` ensuring sections land flush beneath the sticky navbar.

### 2.2 Precision Smooth Scrolling & Native Momentum Optimization (`fdab73f`, `44c8e92`)
- Eliminated compounding scroll offset bug caused by simultaneous `scroll-padding-top: 120px` in `globals.css` and section `scroll-mt-[120px]`.
- Removed global `html { scroll-behavior: smooth; }` from CSS so smooth scrolling is executed purely programmatically via `window.scrollTo({ behavior: "smooth" })`, restoring fluid native kinetic momentum and eliminating browser stutter during manual scrolling.
- Built programmatic scroll handler with `isProgrammaticScrollRef` lock to prevent the scroll-spy listener from cycling intermediate tabs during flight.

### 2.3 Zero-Blink & Zero-Shift Tab Navigation (`b3d3e92`)
- Fixed layout jitter and button width shifts during hover and active state toggling by standardizing constant 1px borders (`border-transparent` vs `border-blue-200`) and uniform `font-medium`.
- Applied `scroll={false}` and `prefetch={false}` to anchor Links, preventing Next.js router full-page flickers and route reload latency.

### 2.4 Context-Aware Dynamic Footer Architecture (`frontend/src/components/shared/Footer.tsx`, `78c166c`)
- Engineered dynamic client `<Footer />` component that automatically suppresses duplicate footers on the landing page (allowing `#help`'s integrated dark CTA bar to sit flush at the bottom) while auto-rendering on inner portal pages.

### 2.5 Navbar Brand & Statistics Polish (`65453e4`, `a5e73e6`, `5562fdd`)
- Refined top navbar brand layout, Government of India ribbon, and active indicators.
- Aligned hero headline and statistics section with the official navy aesthetic (`#1E3A8A`).
- Delivered through merged **[Pull Request #6](https://github.com/arnavbisht141/iGotKarmayogi/pull/6)** (*"Merged UI changes from aarna and arnav"*).

### 2.6 Digital Governance & Cybersecurity Curriculum Architecture (`cgp/digital-governance` Milestone 1)
- Formulated and seeded official Government of India curriculum: *"Digital Governance, Cyber Defense & Public Digital Architecture"* accredited by NeGD and CERT-In (`backend/app/core/seed_data.py`).
- Implemented 5 comprehensive modules spanning the 5 core national digital governance pillars:
  1. **Cybersecurity**: CERT-In 6-hour mandatory reporting under IT Act Section 70B, Critical Information Infrastructure (NCIIPC), SOC telemetry & brute-force triage.
  2. **Data Privacy**: Digital Personal Data Protection Act 2023 (DPDP), Data Fiduciary obligations, Consent Managers, and Data Protection Board of India penalty regimes.
  3. **Digital Signatures & PKI**: IT Act Sections 3 & 3A, Controller of Certifying Authorities (CCA), Class 3 DSC tokens, Aadhaar eSign in e-Office, and non-repudiation under Indian Evidence Act Section 65B.
  4. **Government Cloud (MeghRaj / GI Cloud)**: MeitY CSP empanelment, STQC security audits, sovereign data localization, and Government Community Cloud isolation.
  5. **Digital Public Infrastructure (DPI / India Stack)**: Aadhaar e-KYC authentication, DigiLocker Rule 9A legal parity, PFMS Direct Benefit Transfer (DBT), and API Setu interoperability.
- Embedded interactive practice MCQs with detailed statutory explanations across all 10 lessons in `CourseLearningPlayerPage.tsx`.
- Engineered the 15-question end-of-course Certification Examination with automated scoring, 70% pass threshold, and verifiable credential certificate generation via `AssessmentTestPage.tsx`.
- Authored automated test suite `backend/tests/test_digital_governance.py` validating metadata, lesson activities, 15 examination questions, and skill relationships.

### 2.7 Multi-Stage Incident Response Tabletop Engine (`cgp/digital-governance` Milestone 2)
- Architected and implemented the interactive incident response tabletop simulation engine in `backend/app/modules/digital_governance/services/scenario_service.py` and `router.py`.
- Formulated 5 realistic multi-stage branching case scenarios covering the 5 national pillars for Indian civil servants:
  1. **Cybersecurity**: *Operation Vajra* — Critical ransomware outbreak on state treasury payment gateway (PFMS), live network segmentation, CERT-In mandatory 6-hour reporting window under Section 70B, and volatile RAM preservation under Section 65B of the Indian Evidence Act.
  2. **Data Privacy**: *Operation Raksha* — Aadhaar-linked DBT citizen pension registry exposure on public cloud, statutory Data Fiduciary notice to the Data Protection Board of India under Section 8(6) of DPDP Act 2023, Aadhaar masking, and Significant Data Fiduciary (SDF) appointment.
  3. **Digital Signatures & PKI**: *Operation Mudra* — Disputed ₹45 crore e-procurement tender on GeM, Class 3 DSC token revocation defense, OCSP/CRL cryptographic timestamp inspection, and legal non-repudiation under IT Act Sections 3 & 3A.
  4. **Government Cloud (MeghRaj / GI Cloud)**: *Operation Megh* — Unauthorized foreign region workload migration during peak traffic, STQC audit enforcement, sovereign data localization, and Government Community Cloud (GCC) tenant isolation.
  5. **Digital Public Infrastructure (DPI / India Stack)**: *Operation Setu* — High-volume cryptographic replay attack on citizen e-KYC and API Setu highway, nonce validation, rate-limiting, and NCCC threat intelligence sharing.
- Built interactive client interface `CyberScenariosPage.tsx` at `/digital-governance/scenarios` matching the `dev` institutional design tokens (Navy `#1E3A8A`, Gold `#EAB308`, Slate `#F8FAFC`).
- Implemented real-time procedural compliance scoring, decision trail audit log, and executive debrief report.
- Authored automated unit test suite `backend/tests/test_scenarios.py` validating all 5 domains, multi-stage branching, scoring calculations, and summary retrieval.

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
| `2026-09-12` | Multi-Stage Tabletop Simulation Engine | `Code` / `UX` | Branch `cgp/digital-governance` Milestone 2: 5 branching scenarios across 5 domains, backend session engine, CyberScenariosPage UI, and unit tests |
| `2026-09-12` | Digital Governance Curriculum & MCQs Architecture | `Code` / `Curriculum` | Branch `cgp/digital-governance` Milestone 1: 5-module course, in-lesson MCQs, 15-Q certification exam, seed data, and unit tests |
| `2026-09-07` | Aligned hero and statistics with navy aesthetic | `Code` / `UI` | PR #6 merged into `main` (`5562fdd`) |
| `2026-09-07` | Refined navbar brand and ministry ribbon | `Code` / `UI` | Commit `65453e4` |
| `2026-09-07` | Reconciled branch merge and scroll mechanics | `Code` / `UX` | Commit `44c8e92` |
| `2026-09-06` | Git repository cleanup | `DevOps` | Purged 10,590 tracked `backend/venv` files (`56d954b`) |
| `2026-09-06` | Fixed button blink and layout shift during scroll | `Code` / `UX` | Standardized 1px borders and scroll-spy lock (`b3d3e92`) |
| `2026-09-06` | Dynamic footer implementation | `Code` / `UI` | Context-aware footer component (`78c166c`) |
| `2026-09-06` | Viewport-snap landing page navigation & smooth scroll | `Code` / `UX` | Restored all 4 missing sections & scroll logic (`fdab73f`, `78c166c`) |

---

## 5. Notes & Context for Future AI Coding Agents
- **Smooth Scroll Standard:** Do NOT re-add `html { scroll-behavior: smooth; }` or `scroll-padding-top` to `globals.css`. Smooth scrolling must remain purely programmatic via `window.scrollTo({ behavior: "smooth" })` to avoid double-offset bugs and breaking native browser momentum scrolling.
- **Navbar Layout Shift Prevention:** Maintain identical padding and 1px border widths on active and inactive tab classes to prevent box-model jitter.
- **Landing Page Section Registration:** Landing page sections (`#hero`, `#about`, `#how-it-works`, `#resources`, `#help`) rely on programmatic offset scrolling; when adding new sections to the landing page, ensure they include `scroll-mt-[120px]` and are registered in `Navbar.tsx`.
