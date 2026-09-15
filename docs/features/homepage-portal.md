# 🏛️ Homepage & Public Portal: Institutional Learning Gateway

> **Status:** `Implemented` (Phase 0 / Streamlined Public Portal)  
> **Branch:** `homepage`  
> **Primary Route:** `/` (`frontend/src/app/page.tsx`)  
> **Primary Component:** `frontend/src/features/landing/components/EntryLandingPage.tsx`  
> **Navigation & Layout:** `Navbar.tsx`, `Footer.tsx`, `globals.css`  

---

## 1. Executive Summary & Design Vision

The **iGOT Karmayogi (MoSPI) Public Portal** serves as the authoritative, clutter-free entry point for India's civil servants, administrative officers, and statistical personnel under the National Programme for Civil Services Capacity Building (NPCSCB).

In response to user feedback, the portal has been refined into an essentially **bare-bones, dignified, and authentic government portal**:
- **Removal of Artificial AI Telltales:** Eliminated all multi-colored eyebrow pill boxes above headings, fake dashboard progress meters, rainbow gradient lines, and artificial sample query chips.
- **Dignified Navy Blue & Sober Yellow Palette:** Grounded in Government of India **Navy Blue (`#1E3A8A`)** with subtle, **sober warm yellow (`#EAB308` / `#CA8A04`)** accents used exclusively where necessary (e.g. key action buttons and milestone badges).
- **Single Streamlined Navigation Header:** Removed the redundant topmost ministry ribbon; seamlessly integrated the Hindi/English language switcher directly into the main desktop navbar and mobile menu.
- **Direct & High-Contrast Typography:** Headings speak with unpretentious authority (`#0F172A`), supported by readable body copy (`#334155`) with generous leading and zero visual noise.
- **Single-Viewport Scroll Gliding:** Clean section heights calibrated to `scroll-mt-16 sm:scroll-mt-[68px] min-h-[calc(100vh-68px)]` ensuring zero-shift programmatic anchor scrolling.

---

## 2. Page Architecture & Section Inventory

The streamlined portal is organized into five single-viewport sections:

```
┌────────────────────────────────────────────────────────┐
│  1. Hero & Metrics Section (#hero)                     │
│  - Clear, unadorned Government Display Headline        │
│  - Dual Actions: Official Sign In / Explore Catalog    │
│  - Framed Hero Carousel with Clean Minimalist Controls │
│  - 4-Column Clean Statistics Summary                   │
├────────────────────────────────────────────────────────┤
│  2. Institutional Framework & Pillars (#about)         │
│  - Left: Mission Karmayogi & MoSPI Mandate Overview    │
│  - Right: Three Core Competency Pillars (NSS/CPI,      │
│    70% Passing Threshold, Cadre AI Assistance)         │
├────────────────────────────────────────────────────────┤
│  3. How the Journey Works (#how-it-works)              │
│  - Direct 4-Step Milestone Grid (1. Onboard Role,      │
│    2. Discover & Study, 3. Pass Exam, 4. Certificate)  │
├────────────────────────────────────────────────────────┤
│  4. Cadre Resources & Library (#resources)             │
│  - 4 Clean Document Cards (NSSO, CPI, UN-NQAF, CAPI)   │
│  - File format & size metadata with direct download    │
├────────────────────────────────────────────────────────┤
│  5. Help, Support & Closing Banner (#help)             │
│  - 24/7 Civil Service AI Assistant launch trigger      │
│  - Ministry Training Desk (Helpline & Support Email)   │
│  - Cadre FAQs (Certificate verification, 70% threshold)│
│  - Solid Deep Navy Closing Strip with Sober Yellow CTA │
└────────────────────────────────────────────────────────┘
```

---

## 3. Subsystem Specifications

### 3.1 Single-Tier Header & Context-Aware Navigation (`Navbar.tsx`)
- The top ministry ribbon has been removed to conserve vertical viewport height.
- Government attribution is integrated cleanly into the brand title: *"iGOT Karmayogi Bharat • MoSPI • Government of India"*.
- The language toggle button (`हिन्दी / English`) sits directly in the main action cluster alongside Discover and Sign In.
- Fallback header height calibrated to 68px.
- **Context-Aware Institutional Links:**
  - When an **unauthenticated user is on the landing page (`/`)**, the About, How It Works, Resources, and Help links render as anchor links (`/#about`, `/#how-it-works`, etc.) with programmatic smooth-scroll gliding to the corresponding section.
  - When the user is **authenticated or on any other page**, these links navigate to dedicated standalone pages (`/about`, `/how-it-works`, `/resources`, `/help`) with full institutional content.
  - Routing logic: `href={!user && pathname === "/" ? "/#about" : "/about"}`.
  - Active state highlighting uses `isActive("/about")` for page routes and scroll-spy `activeSection === "about"` for anchor mode.

### 3.1.1 Standalone Institutional Pages
When accessed as dedicated routes, each page provides expanded institutional content beyond the landing page summaries:

| Route | Component | Content |
|---|---|---|
| `/about` | `AboutPage.tsx` | 3 competency pillars, rule-to-role paradigm comparison, 6 stakeholder governance cards, verifiable credentials banner |
| `/how-it-works` | `HowItWorksPage.tsx` | 4-stage capacity building breakdown, process guarantee strip, learning FAQ, closing CTA |
| `/resources` | `ResourcesPage.tsx` | Searchable/filterable document library with 6 official manuals, download modals, category chips |
| `/help` | `HelpPage.tsx` | 3-channel support grid, collapsible FAQ accordion, support ticket submission form |

All pages are located in `frontend/src/features/institutional/components/` and follow the institutional design standard (white header banner, `#F8FAFC` slate canvas, Official Navy branding).

### 3.2 Hero & Key Statistics (`#hero`)
- Unadorned headline: *"National Learning Platform for Civil Services"*.
- Actions: Official Sign In (`bg-[#1E3A8A] text-white`) and Explore Catalog outline button.
- Hero Carousel: Clean white framed container without artificial floating category tags.
- Statistics Bar: 4 columns displaying `40,000+` Civil Servants, `100%` Accredited Modules, `UN-NQAF` Quality Assurance, and `Verifiable` Credentials.

### 3.3 Institutional Framework & Core Pillars (`#about`)
- Left: Grounded overview card covering official statistical cadres (NSS, CPI, NAS), 70% accredited passing threshold, and cadre AI assistance.
- Right: Core pillars detailing statistical methodologies, standardized evaluations, and automated circular lookups.

### 3.4 4-Step Progression Flow (`#how-it-works`)
- Clean 4-card milestone grid:
  1. *Onboard Role* (`UserCheck`): Official government email verification and department selection.
  2. *Discover & Study* (`GraduationCap`): Video lectures, field manuals, and CAPI survey simulations.
  3. *Pass Assessment* (`ClipboardCheck`): 70% threshold evaluation with immediate scoring feedback.
  4. *Earn Certificate* (`Award`): Cryptographically verifiable credentials recognized in annual appraisals (APAR).

### 3.5 Cadre Resources & Library (`#resources`)
- 4 official technical handbooks with uniform category labels:
  - *Field Enumerator Manual* (NSSO Guide • PDF 4.2 MB)
  - *CPI & IIP Technical Manual* (Price Statistics • PDF 3.8 MB)
  - *UN-NQAF Quality Rubrics* (Quality Standards • PDF 2.6 MB)
  - *CAPI Operations Manual* (Survey Tech • PDF 5.1 MB)

### 3.6 Help, Support Desk & Solid Closing Banner (`#help`)
- Support channels: AI assistant launcher, Ministry Training Desk hotline (`1800-11-KARM`), official support email, and operational hours (`09:30 – 18:00 IST`).
- Cadre FAQs: Verifiable SHA-256 hash checks and 70% passing threshold rules.
- Closing Banner: Solid deep navy background (`bg-[#0F172A]`) with a sober yellow registration button (`bg-[#EAB308] hover:bg-[#CA8A04] text-slate-950 font-semibold`) and official links.

---

## 5. Bilingual Internationalization (Hindi / English)

The public homepage is 100% bilingual, reacting in real-time to the language toggle in `Navbar.tsx` via `useI18n()`:
- **Comprehensive Key Coverage:** All text elements in [`EntryLandingPage.tsx`](file:///d:/Main_Files/AIMS/Hacks/SIH'26/iGotKarmayogi/frontend/src/features/landing/components/EntryLandingPage.tsx) are mapped to translation keys in [`frontend/src/lib/i18n/index.tsx`](file:///d:/Main_Files/AIMS/Hacks/SIH'26/iGotKarmayogi/frontend/src/lib/i18n/index.tsx):
  - **Hero:** `hero.title` (*"सिविल सेवाओं हेतु राष्ट्रीय शिक्षण मंच"*), `hero.subtitle`, `hero.signIn` (*"आधिकारिक लॉगिन"*), `hero.explore` (*"पाठ्यक्रम सूची देखें"*), `hero.badgeMospi`, `hero.badgeCbc`, `hero.badgeIso`.
  - **Hero Slides:** Dynamic translation of titles and accessibility `alt` texts for `hero.slide1` (*"मिशन कर्मयोगी राष्ट्रीय क्षमता निर्माण"*), `hero.slide2`, `hero.slide3`.
  - **Statistics:** Metric numerals (`stats.trainedCount`: *"४०,०००+"*, `stats.modulesCount`: *"१००%"*), titles, and descriptive subtitles.
  - **About:** Overview card (`about.cardOrg`: *"मिशन कर्मयोगी (एमओएसपीआई)"*), heading (`about.title`: *"क्षमता-आधारित शिक्षण प्रतिमान"*), and 3 core pillar summaries.
  - **How It Works:** Header (`howItWorks.title`: *"कर्मयोगी शिक्षण यात्रा कैसे कार्य करती है"*) and 4 milestone cards (`Onboard Role`, `Discover & Study`, `Pass Assessment`, `Earn Certificate`).
  - **Resources:** Library title (`resources.title`: *"संवर्ग संसाधन एवं सांख्यिकी पुस्तकालय"*), catalog trigger, document cards, and download buttons (`resources.access`: *"देखें"*).
  - **Help & Support:** 24/7 AI assistant launcher (`help.aiLaunch`: *"एआई सहायक प्रारंभ करें"*), Ministry Training Desk, operational hours, and FAQs.
  - **Closing Banner & Footer:** Ready title (`cta.readyTitle`), registration button (`cta.register`: *"नया अधिकारी पंजीकरण"*), copyright, and legal links.
- **Client Persistence:** Language preference persists across sessions via `localStorage.getItem("karmayogi_lang")`.

---

## 6. UI/UX Rules for AI Agents

> [!IMPORTANT]
> **No Artificial Pill Badges or AI Gimmicks:**
> Never add colored eyebrow pill boxes above headings, glowing rainbow lines, or fake query chips. Maintain the bare-bones, authoritative, public-service dignity.

> [!TIP]
> **Sober Yellow Accents Only:**
> Use `--color-gold-primary: #EAB308` and `--color-gold-hover: #CA8A04`. Avoid fluorescent or loud golden gradients.
