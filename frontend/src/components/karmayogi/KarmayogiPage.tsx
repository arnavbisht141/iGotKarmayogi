"use client";

import { useEffect, useRef, useState } from "react";
import { ArrowRight, ArrowUpRight, BarChart3, BrainCircuit, ChevronDown, ChevronRight, CircleCheck, CircleAlert, Code2, FlaskConical, Landmark, LockKeyhole, Mail, Menu, Network, Play, Route, ScanLine, ShieldCheck, Sparkles, Target, UserRound, Users, X } from "lucide-react";
import { Marquee } from "./Marquee";
import { AnimatedNumber } from "./AnimatedNumber";

const loopWords = ["Understand", "Assess", "Recommend", "Improve"];
type SmallIcon = React.ComponentType<{ size?: number }>;
const sources: Array<[string, SmallIcon]> = [
  ["iGOT courses", BookIcon],
  ["NSSTA / TPAC", Landmark],
  ["Adaptive assessment", ScanLine],
  ["Technical labs", Code2],
  ["Behavioural scenarios", Users],
];
const experiences = [
  { title: "Competency profile", tag: "PROFILE", icon: UserRound, text: "A living view of role needs, current evidence and target-role readiness.", tone: "green" },
  { title: "Knowledge tracing", tag: "TRACE", icon: BrainCircuit, text: "Mastery updates as questions, hints, courses and labs create new evidence.", tone: "deep-green" },
  { title: "Explainable pathway", tag: "RECOMMEND", icon: Route, text: "Every next action shows the gap it addresses and why it belongs now.", tone: "cream" },
  { title: "Practical validation", tag: "APPLY", icon: FlaskConical, text: "Practice statistical reasoning and technical skills in governed experiences.", tone: "green" },
];
const recommendations: Array<[string, string, string, SmallIcon]> = [
  ["iGOT course", "Advanced SQL for Official Statistics", "Addresses SQL Joins, the highest current-role gap", BookIcon],
  ["Technical lab", "District data: groupby + joins", "Builds on recent SQL SELECT evidence", Code2],
  ["Micro-assessment", "Interpreting sampling distributions", "Checks a prerequisite for the target role", BarChart3],
];
const faqs = [
  ["Is this replacing iGOT Karmayogi?", "No. Karmayogi+ is presented as an intelligence layer that can extend the iGOT learning ecosystem with competency evidence, adaptive practice and reassessment."],
  ["How are recommendations explained?", "Each prototype recommendation names the role requirement, the current gap, the prerequisite context and the expected next evidence."],
  ["Can the system decide promotions?", "No. It supports development and analytics. Consequential employment decisions remain with authorized human processes."],
  ["Where does the AI fit?", "Language generation and evidence extraction can use AI, while numerical truth, lab validation, permissions and analytics remain deterministic or governed."],
  ["What is live today?", "This public page is an SIH prototype with synthetic demonstration data. Official iGOT contracts, approved content and production integrations are future requirements."],
];

function BookIcon({ size = 16 }: { size?: number }) { return <span className="book-icon" style={{ fontSize: size }} aria-hidden="true">▦</span>; }
type Modal = { title: string; text: string };

function StatusBadge({ children, tone = "prototype" }: { children: React.ReactNode; tone?: "prototype" | "mock" | "vision" }) {
  return <span className={`status-badge status-${tone}`}><span className="status-dot" />{children}</span>;
}

function ProductPanel({ kind }: { kind: "profile" | "trace" | "path" | "lab" }) {
  if (kind === "profile") return <div className="ui-panel profile-ui"><div className="ui-top"><small>OFFICER PROFILE</small><StatusBadge tone="mock">Synthetic</StatusBadge></div><div className="ui-person"><div className="avatar">AS</div><div><strong>Ananya Sharma</strong><span>Assistant Statistical Officer</span><span>Labour Statistics · 5 years</span></div></div><div className="ui-role"><span>Current role</span><b>Labour Statistics</b><ArrowRight size={13} /><span>Target</span><b>Deputy Director</b></div><div className="ui-bars"><span><i style={{ width: "74%" }} />Statistical reasoning</span><span><i style={{ width: "61%" }} />Data engineering</span><span><i style={{ width: "68%" }} />Digital governance</span></div></div>;
  if (kind === "trace") return <div className="ui-panel trace-ui"><div className="ui-top"><small>MASTERY OVER TIME</small><span className="ui-value">61 <em>/ 75</em></span></div><div className="ui-line-chart"><svg viewBox="0 0 500 150" preserveAspectRatio="none"><path d="M0 127 C50 115 65 120 99 106 S148 112 184 99 S231 106 268 78 S312 97 343 68 S404 77 431 49 S467 48 500 24" fill="none" stroke="#4f9b64" strokeWidth="3" vectorEffect="non-scaling-stroke" /><path d="M0 127 C50 115 65 120 99 106 S148 112 184 99 S231 106 268 78 S312 97 343 68 S404 77 431 49 S467 48 500 24 L500 150 L0 150Z" fill="#4f9b6422" /></svg><div className="ui-axis"><span>Baseline</span><span>Course</span><span>Lab</span><span>Today</span></div></div><div className="ui-events"><span><i className="dot-green" />Assessment A17 <b>+8</b></span><span><i className="dot-deep-green" />Lab completed <b>+5</b></span><span><i className="dot-orange" />Hint used <b>−2</b></span></div></div>;
  if (kind === "path") return <div className="ui-panel path-ui"><div className="ui-top"><small>NEXT BEST ACTION</small><StatusBadge>Evidence-backed</StatusBadge></div><strong>Complete the Advanced JOIN micro-lab</strong><p>45 min · addresses SQL Joins · prerequisite met</p><div className="path-meter"><span style={{ width: "68%" }} /><b>68% relevant</b></div><div className="why-row"><Sparkles size={14} /> Why now? Your target role requires stronger data engineering evidence.</div></div>;
  return <div className="ui-panel lab-ui"><div className="ui-top"><small>TECHNICAL LAB · PY_GROUPBY_01</small><StatusBadge tone="mock">Sandbox</StatusBadge></div><div className="code-block"><span><i>01</i> df.groupby(<b>&apos;state&apos;</b>)</span><span><i>02</i> .employment_rate.mean()</span><span><i>03</i> .reset_index()</span><span className="muted-code"><i>04</i> # run validation</span></div><div className="lab-status"><CircleCheck size={15} /> 4 / 4 deterministic tests passed <strong>Valid dataframe output</strong></div></div>;
}

function HeroSummary({ openModal }: { openModal: (modal: Modal) => void }) {
  return <div className="impact-summary">
    <div className="reach"><div className="summary-label"><UserRound size={15} /> Officer profile</div><strong>Ananya</strong><p>Assistant Statistical Officer<br />Labour Statistics · 5 years</p><button className="text-link" onClick={() => openModal({ title: "Synthetic officer profile", text: "Ananya Sharma is the synthetic demonstration persona used across this prototype: Assistant Statistical Officer in Labour Statistics, with a target role of Deputy Director. Production profiles require authorized data and policy." })}>View profile</button></div>
    <div className="next-goal"><div className="summary-label"><Target size={15} /> Priority skill gap</div><h2>SQL Joins</h2><div className="summary-gap"><span>61%</span><i><b style={{ width: "61%" }} /></i><span>75% target</span></div><button className="text-link" onClick={() => openModal({ title: "Skill gap intelligence", text: "The prototype compares current mastery with target-role requirements. SQL Joins is shown as a synthetic high-priority gap, with evidence and confidence attached." })}>Inspect evidence <ArrowUpRight size={14} /></button></div>
    <div className="hero-quote"><div className="summary-action"><Sparkles size={21} /></div><div><div className="summary-label">Next best action</div><p>Complete the Advanced JOIN micro-lab</p><small>45 min · addresses SQL Joins · prerequisite met</small><button className="summary-action-link" onClick={() => openModal({ title: "Recommended next action", text: "Complete the Advanced JOIN micro-lab. This synthetic recommendation is relevant because SQL Joins is below the target-role requirement and its prerequisite evidence is already present." })}>Open recommendation <ArrowRight size={14} /></button></div></div>
  </div>;
}

function GoalList() {
  return <div className="goal-list"><p><strong>Assess</strong> current competency</p><p><strong>Identify</strong> the role gap</p><p><strong>Recommend</strong> the next action</p><p><strong>Update</strong> the competency profile</p></div>;
}

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [modal, setModal] = useState<Modal | null>(null);
  const [heroWord, setHeroWord] = useState(0);
  const [scrolled, setScrolled] = useState(false);
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const dialog = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const timer = reduced ? undefined : window.setInterval(() => setHeroWord((value) => (value + 1) % loopWords.length), 2800);
    const onScroll = () => setScrolled(window.scrollY > 40);
    const onKey = (event: KeyboardEvent) => { if (event.key === "Escape" && menuOpen) { setMenuOpen(false); menuButtonRef.current?.focus(); } };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    document.addEventListener("keydown", onKey);
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("is-visible"); observer.unobserve(entry.target); } }), { threshold: .14, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll("[data-reveal]").forEach((node) => observer.observe(node));
    return () => { if (timer) window.clearInterval(timer); window.removeEventListener("scroll", onScroll); document.removeEventListener("keydown", onKey); observer.disconnect(); };
  }, [menuOpen]);

  function openModal(next: Modal) { setModal(next); dialog.current?.showModal(); }
  function closeModal() { dialog.current?.close(); setModal(null); }
  const loopCards: Array<[string, string, SmallIcon, string]> = [
    ["01", "Understand the officer", UserRound, "Role, context, prior evidence and career goals establish the starting point."],
    ["02", "Measure what changes", ScanLine, "Knowledge tracing and practical assessment update competency with confidence."],
    ["03", "Recommend what matters", Route, "The next course, lab or scenario is tied to a gap and explained."],
  ];

  return <>
    <a className="skip-link" href="#main">Skip to content</a>
    <div className={`cream header-shell ${scrolled ? "is-scrolled" : ""}`}>
      <header className="site-header wrap">
        <a className="brand" href="#top" aria-label="Karmayogi+ home"><span className="brand-mark">K<span>+</span></span><span className="brand-name">Karmayogi<span>+</span></span></a>
        <button ref={menuButtonRef} className="mobile-toggle" aria-expanded={menuOpen} aria-controls="navigation" aria-label={menuOpen ? "Close navigation" : "Open navigation"} onClick={() => setMenuOpen((value) => !value)}>{menuOpen ? <X size={19} /> : <Menu size={19} />}</button>
        <nav id="navigation" aria-label="Main navigation" className={`navigation ${menuOpen ? "is-open" : ""}`} onClick={(event) => { if ((event.target as HTMLElement).closest("a")) setMenuOpen(false); }}>
          <details className="nav-group"><summary>How it works <ChevronDown size={14} /></summary><div className="dropdown"><a href="#about">The gap</a><a href="#loop">Intelligence loop</a><a href="#facts">Dashboards</a><a href="#blueprint">Integration</a></div></details>
          <a href="#intelligence">Skill Intelligence</a><a href="#experiences">Learning Experiences</a><a href="#facts">Dashboards</a><a href="#blueprint">Integration</a>
          <a className="pill dark" href="#facts">Explore Prototype <ArrowUpRight size={14} /></a>
        </nav>
      </header>
    </div>
    <main id="main">
      <div className="cream">
        <section className="hero wrap" id="top" aria-labelledby="hero-title">
          <h1 id="hero-title"><span>Learn what <span className="hero-word" key={heroWord}>{loopWords[heroWord]}</span></span><span>every officer needs next.</span></h1>
          <div className="hero-intro"><p>Helping government officials build the right skills through <strong>continuous competency intelligence, adaptive learning and measured improvement.</strong></p><a className="pill" href="#loop"><Route size={19} /> See the intelligence loop</a></div>
          <HeroSummary openModal={openModal} />
          <div className="partners"><p>Learning sources and signals</p><Marquee className="partner-logos" label="Learning sources and signals"><div className="source-list">{sources.map(([label, SourceIcon]) => <span className="source-chip" key={label}><SourceIcon size={16} /> {label}</span>)}</div></Marquee></div>
        </section>
      </div>
      <section className="about wrap" id="about" aria-label="Why competency intelligence matters">
        <div className="about-tabs" role="tablist" aria-label="Platform story"><button id="impact-tab" role="tab" aria-selected={activeTab === 0} aria-controls="mission-panel" onClick={() => setActiveTab(0)}>Why course access<br />is not enough</button><button id="values-tab" role="tab" aria-selected={activeTab === 1} aria-controls="mission-panel" onClick={() => setActiveTab(1)}>What continuous intelligence<br />changes</button></div>
        <p id="mission-panel" className="mission-copy" role="tabpanel" aria-labelledby={activeTab === 0 ? "impact-tab" : "values-tab"}>{activeTab === 0 ? "A course catalogue can show access and completion. It cannot see whether an officer can apply a concept in the current role, what the next role requires, or whether learning actually changed competency." : "Profile → Assess → Trace → Identify gap → Recommend → Learn + apply → Reassess. Every new piece of evidence changes the next action."}</p>
        <div className="values">{["Profile the officer", "Measure competency", "Find the gap", "Verify improvement"].map((label) => <a className="pill outline" href={label === "Find the gap" ? "#intelligence" : "#loop"} key={label}>{label}</a>)}</div>
        <div className="community-strip"><Marquee className="community-images" label="Product signal carousel"><div className="signal-card"><ProductPanel kind="profile" /></div><div className="signal-card"><ProductPanel kind="trace" /></div><div className="signal-card"><ProductPanel kind="path" /></div><div className="signal-card"><ProductPanel kind="lab" /></div></Marquee><div className="poverty"><strong><AnimatedNumber value={8} /></strong><p>states in one continuous loop from profile to updated competency profile</p><a className="text-link" href="#loop">See the loop <ArrowRight size={13} /></a></div></div>
      </section>
      <section className="campaigns wrap" id="intelligence" aria-labelledby="campaign-title"><h2 className="section-title" id="campaign-title">The right learning<br />starts with the right gap.</h2><div className="three-grid">{recommendations.map(([type, title, note, Icon], i) => <article className="campaign-card" key={title} data-reveal><div className="campaign-icon"><Icon size={26} /></div><small>{type}</small><h3>{title}</h3><p className="fund-label">{note}</p><div className="fund-progress" role="progressbar" aria-label={`${title} relevance`} aria-valuenow={[91, 84, 68][i]} aria-valuemin={0} aria-valuemax={100}><span style={{ width: `${[91, 84, 68][i]}%` }} /></div><div className="fund-amounts"><span>{["High relevance", "Practice next", "Confidence check"][i]}</span><span>{["SQL gap", "Prerequisite", "Target role"][i]}</span></div><button className="pill" onClick={() => openModal({ title, text: `${note}. This is a synthetic recommendation preview; source availability and production eligibility require authorized integration.` })}>Why this action <ArrowRight size={15} /></button></article>)}</div><a className="pill outline" href="#experiences">Explore learning experiences</a></section>
      <section className="successes" id="experiences" aria-labelledby="success-title"><div className="wrap"><h2 className="section-title" id="success-title" data-reveal>Learn by <span>doing.</span></h2><div className="impact-feature" data-reveal><div className="feature-left"><div className="feature-orb"><BrainCircuit size={76} /></div><p>Courses become more useful when the system can generate targeted questions, safe labs and job-relevant scenarios around the competency gap.</p></div><div className="feature-right"><button className="watch" onClick={() => openModal({ title: "Adaptive practice", text: "The prototype combines adaptive MCQs, deterministic statistical questions, coding/data labs, Digital Governance simulations and CTF-style security challenges. Each experience returns evidence to the competency loop." })}><span className="watch-icon"><Play size={18} /></span><span>See how learning experiences return evidence <ArrowRight size={15} /></span></button><GoalList /></div></div><div className="three-grid stories">{experiences.slice(1).map((story) => { const StoryIcon = story.icon; return <button className="story" key={story.title} onClick={() => openModal({ title: story.title, text: story.text })}><div className={`story-visual ${story.tone}`}><StoryIcon size={38} /><span>{story.tag}</span></div><span className="story-default"><span className="category">{story.tag}</span><h3>{story.title}</h3></span><span className="story-reveal"><span className="category">{story.tag}</span><strong>{story.text}</strong><span className="text-link">Inspect preview <ArrowUpRight size={13} /></span></span></button>; })}</div></div></section>
      <section className="testimonials wrap" id="loop" aria-labelledby="testimonials-title"><p className="eyebrow">THE INTELLIGENCE LOOP</p><h2 className="section-title" id="testimonials-title" data-reveal>Assess. Learn.<br /><span>Improve.</span></h2><div className="three-grid">{loopCards.map(([number, title, Icon, text], i) => <article className="quote-card" key={title} data-reveal style={{ transitionDelay: `${i * 100}ms` }}><div className="quote-number">{number}</div><Icon size={24} /><h3>{title}</h3><p>{text}</p><a href={i === 0 ? "#intelligence" : i === 1 ? "#facts" : "#experiences"} className="text-button">Explore <ArrowRight size={14} /></a></article>)}</div><a className="pill dark" href="#facts">Open dashboard concepts <ArrowRight size={16} /></a></section>
      <section className="facts wrap" id="facts" aria-labelledby="facts-title" data-reveal><div className="facts-grid-bg" /><div className="facts-heading"><span>LEARNER + WORKFORCE INTELLIGENCE</span><h2 id="facts-title">See the <em>change</em><br />with evidence.</h2></div><div className="fact fact-one"><strong>72<span>/100</span></strong><p>Ananya&apos;s current readiness in this synthetic learner view.</p><div className="fact-bar"><span style={{ width: "72%" }} /></div></div><div className="fact fact-two"><strong>03</strong><p>Priority skill gaps surfaced for the next intervention.</p><div className="fact-bars"><i style={{ height: "42%" }} /><i style={{ height: "68%" }} /><i style={{ height: "53%" }} /><i style={{ height: "78%" }} /><i style={{ height: "61%" }} /></div></div><div className="fact fact-three"><strong>+11 pts</strong><p>Illustrative pre/post competency change in a prototype pathway.</p><span className="fact-status"><CircleCheck size={14} /> synthetic demonstration</span></div><a className="pill facts-action" href="#blueprint">Inspect the architecture <ArrowUpRight size={15} /></a></section>
      <section className="faq wrap" id="faq" aria-label="Frequently asked questions"><h2 className="faq-label">Questions that matter</h2><div className="faq-list">{faqs.map(([question, answer]) => <details className="faq-item" key={question}><summary>{question}<span><ChevronRight size={20} /></span></summary><p>{answer}</p></details>)}</div></section>
      <section className="blueprint wrap" id="blueprint" aria-labelledby="blueprint-title"><h2 className="section-title" id="blueprint-title">Designed to extend<br />the ecosystem.</h2><div className="blueprint-grid"><div className="blueprint-copy"><StatusBadge tone="mock">Mock adapter</StatusBadge><h3>iGOT provides the learning ecosystem. Karmayogi+ provides the intelligence layer.</h3><div><p>Authorized identity, catalogue, enrolment and learning-history fields can flow through an adapter into role mapping, competency evidence and personalized learning.</p><a className="pill dark" href="#integration">Read integration boundaries <ArrowRight size={15} /></a></div></div><div className="blueprint-photo blueprint-ui"><div className="arch-node"><Landmark size={23} /><strong>iGOT ecosystem</strong><small>courses · history</small></div><ArrowRight size={16} /><div className="arch-node core"><BrainCircuit size={23} /><strong>Karmayogi+</strong><small>gaps · pathways</small></div><ArrowRight size={16} /><div className="arch-node output"><FlaskConical size={23} /><strong>Learning</strong><small>course · lab</small></div><div className="arch-note"><LockKeyhole size={13} /> Official contracts required for production</div></div></div></section>
      <section id="integration" className="integration-anchor" aria-labelledby="integration-title"><div className="wrap"><h2 id="integration-title">Government-ready by design.</h2><p>RBAC, SSO readiness, audit trails, evidence provenance, privacy boundaries and low-bandwidth behavior are part of the product direction.</p><div className="integration-pills"><span><ShieldCheck size={15} /> RBAC</span><span><LockKeyhole size={15} /> Audit trail</span><span><Network size={15} /> Portable data</span><span><CircleAlert size={15} /> Human review</span></div></div></section>
    </main>
    <a className="floating-prototype" href="#facts">Explore prototype <ArrowUpRight size={15} /></a>
    <footer className="footer" id="contact"><div className="wrap"><div className="footer-top"><div><h2>Karmayogi<span>+</span></h2><p>The intelligence layer for continuous government capacity building.</p><StatusBadge>SIH prototype</StatusBadge></div><div className="footer-links"><h3>Product</h3><a href="#about">The gap</a><a href="#loop">Intelligence loop</a><a href="#intelligence">Skill intelligence</a><a href="#experiences">Learning experiences</a></div><div className="footer-links"><h3>Readiness</h3><a href="#facts">Dashboards</a><a href="#blueprint">Integration</a><a href="#faq">Questions</a><a href="#integration">Responsible AI</a></div></div><div className="footer-middle"><div><p>Prototype status</p><div className="footer-statuses"><span><i /> Synthetic data</span><span><i /> Mock integration</span><span><i /> Production vision</span></div></div><a className="text-link newsletter" href="#faq"><Mail size={18} /> Read prototype boundaries</a></div><div className="footer-bottom"><p>SIH project prototype · 2026</p><div><a href="#faq">Privacy and governance</a><a href="#faq">Accessibility</a><a href="#blueprint">Architecture</a></div></div></div></footer>
    <dialog ref={dialog} className="action-dialog" aria-labelledby="dialog-title" onClick={(event) => { if (event.target === event.currentTarget) closeModal(); }} onClose={() => setModal(null)}><button className="dialog-close" onClick={closeModal} aria-label="Close dialog"><X size={19} /></button>{modal && <><div className="dialog-kicker">KARMAYOGI+ · PROTOTYPE</div><h2 id="dialog-title">{modal.title}</h2><p>{modal.text}</p><button className="pill dark" onClick={closeModal}>Back to prototype <ArrowRight size={15} /></button></>}</dialog>
  </>;
}

export function KarmayogiPage() { return <App />; }
