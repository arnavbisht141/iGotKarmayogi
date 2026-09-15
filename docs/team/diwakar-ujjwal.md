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
- Delivered through merged **[Pull Request #6](https://github.com/arnavbisht141/iGotKarmayogi/pull/6)** (_"Merged UI changes from aarna and arnav"_).

### 2.6 Digital Governance & Cybersecurity Curriculum Architecture (`cgp/digital-governance` Milestone 1)

- Formulated and seeded official Government of India curriculum: _"Digital Governance, Cyber Defense & Public Digital Architecture"_ accredited by NeGD and CERT-In (`backend/app/core/seed_data.py`).
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
  1. **Cybersecurity**: _Operation Vajra_ — Critical ransomware outbreak on state treasury payment gateway (PFMS), live network segmentation, CERT-In mandatory 6-hour reporting window under Section 70B, and volatile RAM preservation under Section 65B of the Indian Evidence Act.
  2. **Data Privacy**: _Operation Raksha_ — Aadhaar-linked DBT citizen pension registry exposure on public cloud, statutory Data Fiduciary notice to the Data Protection Board of India under Section 8(6) of DPDP Act 2023, Aadhaar masking, and Significant Data Fiduciary (SDF) appointment.
  3. **Digital Signatures & PKI**: _Operation Mudra_ — Disputed ₹45 crore e-procurement tender on GeM, Class 3 DSC token revocation defense, OCSP/CRL cryptographic timestamp inspection, and legal non-repudiation under IT Act Sections 3 & 3A.
  4. **Government Cloud (MeghRaj / GI Cloud)**: _Operation Megh_ — Unauthorized foreign region workload migration during peak traffic, STQC audit enforcement, sovereign data localization, and Government Community Cloud (GCC) tenant isolation.
  5. **Digital Public Infrastructure (DPI / India Stack)**: _Operation Setu_ — High-volume cryptographic replay attack on citizen e-KYC and API Setu highway, nonce validation, rate-limiting, and NCCC threat intelligence sharing.
- Built interactive client interface `CyberScenariosPage.tsx` at `/digital-governance/scenarios` matching the `dev` institutional design tokens (Navy `#1E3A8A`, Gold `#EAB308`, Slate `#F8FAFC`).
- Implemented real-time procedural compliance scoring, decision trail audit log, and executive debrief report.
- Authored automated unit test suite `backend/tests/test_scenarios.py` validating all 5 domains, multi-stage branching, scoring calculations, and summary retrieval.

### 2.8 Upgraded 8-Sandbox Suite, SQLAlchemy Persistence & Supabase Integration (`cgp/digital-governance` Milestone 3)

- Upgraded all 5 original sandboxes and built 3 new governance domain challenges into the complete 8-module procedural range:
  1. **`01-soc-auth-investigation`**: _Operation NightShift_ (SOC Investigation) — Windows Security Event telemetry (4624, 4625, 4688) with brute-force triage and LOLBin staging.
  2. **`02-phishing-dfir`**: _Executive Spearphish & Invoice Fraud_ (DFIR / Phishing) — Raw MIME `.eml` with SPF/DKIM spoofing and DNS C2 beacon correlation.
  3. **`03-compromised-linux-server`**: _Operation Shakti_ (Linux IR) — `auth.log`, `crontab.txt`, `backup_sync.sh`, and `bash_history` for privilege escalation and malicious cron persistence.
  4. **`04-vulnerable-web-app`**: _Operation Suraksha_ (Citizen DB) — `corp_directory.db` (SQLite citizen registry) with UNION SQL injection vulnerability and DPDP Act breach triage.
  5. **`05-threat-hunting-lotl`**: _Operation Garuda_ (Threat Hunting) — Sysmon process trees and high-entropy DNS tunneling exfiltration analysis.
  6. **`06-pki-token-dispute`**: _Operation Mudra_ (PKI Defense) — GeM e-tender submission timestamping vs. CA revocation lists (CRL/OCSP) under IT Act Section 3 & 3A.
  7. **`07-meghraj-cloud-audit`**: _Operation Megh_ (Sovereign Cloud) — Cloud audit logs detecting unauthorized cross-border container migrations violating MeitY data localization.
  8. **`08-dpi-apisetu-replay`**: _Operation Setu_ (API Setu Defense) — e-KYC gateway logs with duplicate cryptographic nonces and WAF rate-limiting mitigations.
- **SQLAlchemy Database Persistence Architecture**:
  - Implemented `CyberSandboxChallenge`, `CyberSandboxSession`, and `UserCyberCompetency` in `backend/app/models/models.py`.
  - Stored all challenge definitions, evidence telemetry artifacts (`artifacts_json`), and Marimo Python notebooks (`notebook_code`) directly in the database.
  - Completely purged `backend/content/` from the repository, achieving zero git file sprawl.
  - Ephemeral runtime materialization into `backend/scratch/sandboxes/<session_id>/` (gitignored) on session launch with automated cleanup upon termination.
- **Live Supabase Knowledge Base Integration (Strictly Read-Only GET)**:
  - Engineered `supabase_service.py` to query scraped Wikipedia articles and YouTube curricula from `https://tdcrpjlpvkqjptvsndnp.supabase.co` across the 5 official Digital Governance topics (`cybersecurity`, `data-privacy`, `digital-signatures`, `government-cloud`, `digital-public-infrastructure`).
  - Exposed `GET /api/digital-governance/sandbox/knowledge-base` and `POST /api/digital-governance/sandbox/generate-from-topic`.
- **Client Console & Navigation**:
  - Enhanced `CyberSandboxPage.tsx` with a 3-tab generator modal (Live Supabase Knowledge Base, Lecture Presets, Custom Transcripts), 9-category filter pills, live Marimo console embed, and CTFd flag verification.
  - Added "Digital Governance" navigation link in `Navbar.tsx` (desktop and mobile) and bilingual English/Hindi translations in `frontend/src/lib/i18n/index.tsx`.
- **Verification**:
  - Full backend test suite passing (15 tests total: 4 curriculum, 4 tabletop scenarios, 7 sandbox suite tests).
  - `npx tsc --noEmit` and `npm run build` compiled all 20 pages with 0 errors.

### 2.9 Core 6-Challenge Range Alignment, Marimo App Run Mode & Hint Session Resiliency (`cgp/digital-governance` Milestone 4)

- **Active Challenge Range Alignment**:
  - Aligned active hands-on sandboxes strictly to the 6 core default challenges:
    1. `01-soc-auth-investigation` (SOC Authentication Triage & Credential Stuffing)
    2. `03-compromised-linux-server` (State Data Centre Linux Server Persistence & IR)
    3. `04-vulnerable-web-app` (Corporate Directory SQL Injection & Exfiltration)
    4. `05-threat-hunting-lotl` (Living-off-the-Land & High-Entropy DNS Tunneling Hunt)
    5. `06-pki-token-dispute` (GeM e-Tender Dispute & Class 3 DSC Non-Repudiation)
    6. `07-meghraj-cloud-audit` (MeghRaj Cloud Audit & Cross-Border Sovereignty)
  - Purged non-default challenges (`02-phishing-dfir`, `08-dpi-apisetu-replay`) and temporary generated sandboxes from SQLite databases and disk.
  - Stripped all legacy "CyberLab" branding across templates and eliminated "FLAGSHIP" tags across UI and backend.
- **Marimo App / Run Execution Mode (`marimo run`)**:
  - Replaced `marimo edit` with `marimo run` in `sandbox_manager.py` to serve notebooks as interactive web applications in read-only App Mode (`mode="read"`).
  - Completely hides Python code cells, editor gutters, and developer controls, exposing solely the clean institutional analysis console with interactive widgets (sliders, filters, tables, buttons, markdown scenario briefings).
- **Hint Session Resiliency & DB Re-hydration**:
  - Implemented `_restore_session_from_db(session_id, db)` in `sandbox_manager.py` to eliminate "Session not found" errors when server restarts clear in-memory state.
  - Added direct challenge fallback lookup using `challenge_id` to ensure hint unlocks and flag submissions remain robust across client simulation fallbacks (`sim_...`).
  - Implemented `CHALLENGE_HINTS_CATALOG` in `CyberSandboxPage.tsx` providing client-side fallback hints for all 6 active modules.
- **LLM Model Alignment & UI Streamlining**:
  - Aligned default LLM model configs with `cgp/technical` (`llama-3.3-70b-versatile`, `gpt-4o-mini`, `gemini-1.5-flash`, `meta/llama-3.1-70b-instruct`).
  - Streamlined UI by temporarily shelving the generation pipeline modal and transcript compiler button.
- **Verification**:
  - Added `test_08_hint_unlock_after_server_reload_and_fallback` to `backend/tests/test_sandbox.py`.
  - Full backend test suite passing (16/16 tests passing).
  - Frontend production build (`npm run build`) passing with 0 errors across all 20 routes.

---

## 3. "Invisible" & Offline Contributions

### 3.1 Interaction Physics Prototyping & Browser Profiling

- Profiled scrolling frame rates and tab switching performance across Chromium and WebKit engines to diagnose micro-stutter and scroll offset compounding.
- Iterated on bounding-box calculation algorithms to determine optimal viewport-center proximity math for the active navigation indicator.

### 3.2 Landing Page Compact Footprint Design

- Re-architected `#how-it-works` content density to fit cleanly within standard 768px/900px laptop vertical viewports without internal scrollbars.

---

## 4. Chronological Activity Log

| Date         | Activity                                                                   | Category                | Notes / Deliverables                                                                                                                                                                                                                                            |
| ------------ | -------------------------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `2026-09-13` | Core 6 Range Alignment, Marimo App Run Mode & Hint Session Resiliency       | `Code` / `Architecture` | Branch `cgp/digital-governance`: Marimo app/run mode (code hidden, analysis console visible), session re-hydration & hint fix, 6-challenge range alignment, CyberLab/FLAGSHIP purge, UI streamlining, and 16 passing backend tests                           |
| `2026-09-13` | Upgraded 8-Sandbox Suite, SQLAlchemy Persistence & Supabase Integration    | `Code` / `Architecture` | Branch `cgp/digital-governance` Milestone 3: 8 upgraded procedural templates, SQLAlchemy DB models & seeding, zero file sprawl (purged backend/content), strictly read-only Supabase knowledge base integration, Navbar link, and 15 passing backend unit tests |
| `2026-09-12` | Multi-Stage Tabletop Simulation Engine                                     | `Code` / `UX`           | Branch `cgp/digital-governance` Milestone 2: 5 branching scenarios across 5 domains, backend session engine, CyberScenariosPage UI, and unit tests                                                                                                              |
| `2026-09-12` | Digital Governance Curriculum & MCQs Architecture                          | `Code` / `Curriculum`   | Branch `cgp/digital-governance` Milestone 1: 5-module course, in-lesson MCQs, 15-Q certification exam, seed data, and unit tests                                                                                                                                |
| `2026-09-07` | Aligned hero and statistics with navy aesthetic                            | `Code` / `UI`           | PR #6 merged into `main` (`5562fdd`)                                                                                                                                                                                                                            |
| `2026-09-07` | Refined navbar brand and ministry ribbon                                   | `Code` / `UI`           | Commit `65453e4`                                                                                                                                                                                                                                                |
| `2026-09-07` | Reconciled branch merge and scroll mechanics                               | `Code` / `UX`           | Commit `44c8e92`                                                                                                                                                                                                                                                |
| `2026-09-06` | Git repository cleanup                                                     | `DevOps`                | Purged 10,590 tracked `backend/venv` files (`56d954b`)                                                                                                                                                                                                          |
| `2026-09-06` | Fixed button blink and layout shift during scroll                          | `Code` / `UX`           | Standardized 1px borders and scroll-spy lock (`b3d3e92`)                                                                                                                                                                                                        |
| `2026-09-06` | Dynamic footer implementation                                              | `Code` / `UI`           | Context-aware footer component (`78c166c`)                                                                                                                                                                                                                      |
| `2026-09-06` | Viewport-snap landing page navigation & smooth scroll                      | `Code` / `UX`           | Restored all 4 missing sections & scroll logic (`fdab73f`, `78c166c`)                                                                                                                                                                                           |

---

## 5. Notes & Context for Future AI Coding Agents

- **Smooth Scroll Standard:** Do NOT re-add `html { scroll-behavior: smooth; }` or `scroll-padding-top` to `globals.css`. Smooth scrolling must remain purely programmatic via `window.scrollTo({ behavior: "smooth" })` to avoid double-offset bugs and breaking native browser momentum scrolling.
- **Navbar Layout Shift Prevention:** Maintain identical padding and 1px border widths on active and inactive tab classes to prevent box-model jitter.
- **Landing Page Section Registration:** Landing page sections (`#hero`, `#about`, `#how-it-works`, `#resources`, `#help`) rely on programmatic offset scrolling; when adding new sections to the landing page, ensure they include `scroll-mt-[120px]` and are registered in `Navbar.tsx`.
