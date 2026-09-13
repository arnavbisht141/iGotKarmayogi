"""Human-crafted Web Application SQL Injection & Database Security Template (Module 4)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import hashlib
import random
import sqlite3

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class WebSqliTemplate(BaseChallengeTemplate):
    """
    Template for Corporate Directory SQL Injection & Data Exfiltration Workbench.
    Synthesizes authentic SQLite corporate database (employees, payroll_audit) with
    interactive query runner and parameterized remediation workbench.
    """

    template_id = "04-vulnerable-web-app"
    title = "Corporate Directory: In-Band SQL Injection & Exfiltration Workbench"
    category = "Web Application Security"
    difficulty = "Intermediate"
    base_points = 150
    duration_minutes = 45
    competency_id = "web_security"
    competency_weight = 1.2
    tags = ["sqli", "owasp", "cwe-89", "sqlite", "web-app", "exfiltration", "parameterization"]
    mitre_techniques = ["T1190", "T1005"]

    DEPARTMENTS = ["Finance", "Human Resources", "Executive", "Engineering", "Legal & Compliance"]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "target_app": {"type": "str", "description": "Target web application title"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        slots = {
            "incident_codename": f"Operation BlindSpot-{rng.randint(101, 899)}",
            "target_app": "Corporate Directory & Staff Lookup API",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        h = slots.get("seed_hash", "default")[:6]
        return f"FLAG{{sqli_union_payroll_audit_{h}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Test input with `'`. Observe if SQLite syntax errors leak database implementation details.",
                "penalty": 10,
            },
            {
                "id": 2,
                "content": "Determine column count with UNION SELECT. Try `' UNION SELECT 1, 2, 3, 4 --` until query arity matches.",
                "penalty": 15,
            },
            {
                "id": 3,
                "content": "Query sqlite_master schema: `' UNION SELECT 1, name, sql, 4 FROM sqlite_master WHERE type='table' --` to reveal the secret payroll audit table.",
                "penalty": 20,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            "Probe the employee search endpoint for SQL syntax error disclosures.",
            "Determine the target query column count using UNION SELECT projection.",
            "Enumerate hidden tables via `sqlite_master` catalog extraction.",
            "Exfiltrate the confidential audit finding flag from the `payroll_audit` table.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Emergency Incident Briefing: {slots['incident_codename']}

During an internal penetration test of `{slots['target_app']}`, auditors identified a suspected SQL injection flaw in the directory lookup service.

The search input parameter concatenates unvalidated user input directly into backend SQLite query strings without parameterization.

Your mandate:
1. Probe the query interface in the interactive Marimo notebook.
2. Confirm SQL injection vulnerability and determine column arity.
3. Enumerate the database schema via `sqlite_master`.
4. Extract the secret flag from the restricted `payroll_audit` table and review parameterized defense.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        db_path = data_dir / "corp_directory.db"

        if db_path.exists():
            db_path.unlink()

        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """)

        employees = [
            (1, "Aarav Sharma", "Engineering", "a.sharma@gov.internal"),
            (2, "Priya Patel", "Finance", "p.patel@gov.internal"),
            (3, "Vikram Singh", "Executive", "v.singh@gov.internal"),
            (4, "Ananya Iyer", "Human Resources", "a.iyer@gov.internal"),
            (5, "Rohan Verma", "Engineering", "r.verma@gov.internal"),
            (6, "Neha Gupta", "Legal & Compliance", "n.gupta@gov.internal"),
            (7, "Siddharth Rao", "Engineering", "s.rao@gov.internal"),
            (8, "Kavita Reddy", "Finance", "k.reddy@gov.internal"),
        ]
        cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", employees)

        flag = self.compute_flag(slots)
        cur.execute("""
        CREATE TABLE payroll_audit (
            audit_id INTEGER PRIMARY KEY,
            employee_ref TEXT NOT NULL,
            discrepancy_amount REAL NOT NULL,
            notes TEXT NOT NULL
        )
        """)

        audits = [
            (101, "EMP-0012", 45000.0, "Duplicate disbursement flagged in Q2"),
            (102, "EMP-0044", 128500.0, f"Unauthorized severance bonus {flag}"),
            (103, "EMP-0089", 12000.0, "Travel allowance unreconciled balance"),
        ]
        cur.executemany("INSERT INTO payroll_audit VALUES (?, ?, ?, ?)", audits)

        conn.commit()
        conn.close()

        return {"corp_directory.db": db_path}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"AppSec Assessment: {slots.get('incident_codename', 'Operation AppSec')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'INC-0404-SQLI-PORTAL'))
        code = code.replace("__TARGET_APP__", slots.get('target_app', 'Corporate Directory API'))
        code = code.replace("__TARGET_HASH__", dynamic_hash)

        target_nb.write_text(code, encoding="utf-8")
        return target_nb


_NOTEBOOK_TEMPLATE = r'''import marimo

__generated_with = "0.24.1"
app = marimo.App(width="full", app_title="__APP_TITLE__")


@app.cell(hide_code=True)
def __():
    import hashlib
    import json
    import re
    import sqlite3
    from pathlib import Path
    import marimo as mo
    import pandas as pd

    return Path, hashlib, json, mo, pd, re, sqlite3


@app.cell(hide_code=True)
def __(Path, pd, sqlite3):
    # Connect to the authentic corporate database
    possible_db_paths = [
        Path("data/corp_directory.db"),
        Path("../data/corp_directory.db"),
        Path("/workspace/data/corp_directory.db"),
        Path("challenges/04-vulnerable-web-app/data/corp_directory.db"),
    ]
    if "__file__" in globals():
        possible_db_paths.insert(
            0, Path(__file__).resolve().parent.parent / "data" / "corp_directory.db"
        )
    db_file = next((p for p in possible_db_paths if p.exists()), None)
    conn = sqlite3.connect(db_file if db_file else ":memory:", check_same_thread=False)

    try:
        df_employees = pd.read_sql_query("SELECT id, name, department, email FROM employees", conn)
    except Exception:
        df_employees = pd.DataFrame()

    raw_db_bytes = db_file.read_bytes() if db_file and db_file.exists() else b""

    return conn, db_file, df_employees, possible_db_paths, raw_db_bytes


@app.cell(hide_code=True)
def __(mo):
    # Analyst Sidebar: OWASP Classification, MITRE ATT&CK & Checklist
    check_probe = mo.ui.checkbox(
        label="1. Probe input for SQL syntax errors (single quote)", value=False
    )
    check_bypass = mo.ui.checkbox(
        label="2. Confirm boolean filter bypass (' OR 1=1 --)", value=False
    )
    check_cols = mo.ui.checkbox(
        label="3. Enumerate query column count (UNION SELECT)", value=False
    )
    check_schema = mo.ui.checkbox(
        label="4. Enumerate schema via sqlite_master injection", value=False
    )
    check_flag = mo.ui.checkbox(
        label="5. Exfiltrate secret payroll audit flag", value=False
    )

    hints = mo.accordion(
        {
            "💡 Hint 1: Syntax Probing": mo.md(
                "Test input with a single quote (`'`). If the application returns a syntax error, untrusted input is concatenated directly into the query string without sanitization."
            ),
            "💡 Hint 2: Determining Column Count": mo.md(
                "UNION SELECT injections require the injected query to return the exact same number of columns as the original query (4 columns). Test `' UNION SELECT 1, 2, 3, 4 --` to align arity."
            ),
            "💡 Hint 3: Database Schema Enumeration": mo.md(
                "In SQLite, all table schemas are cataloged in `sqlite_master`. Inject a UNION query: `' UNION SELECT 1, name, sql, 4 FROM sqlite_master --` to uncover hidden internal tables like `payroll_audit`."
            ),
        }
    )

    sidebar_content = mo.vstack(
        [
            mo.md("## 🌐 AppSec Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Target**: `__TARGET_APP__`"),
            mo.md("**Classification**: `OWASP A03:2021` | Severity: **HIGH**"),
            mo.md("---"),
            mo.md("### 🎯 Penetration Testing Checklist"),
            check_probe,
            check_bypass,
            check_cols,
            check_schema,
            check_flag,
            mo.md("---"),
            mo.md("### 🗺️ Vulnerability Mapping"),
            mo.md(
                "- **CWE-89**: Improper Neutralization of Special Elements used in an SQL Command\n"
                "- **OWASP Top 10**: A03:2021 - Injection\n"
                "- **MITRE ATT&CK**: T1190 (Exploit Public-Facing Application)\n"
                "- **CAPEC**: CAPEC-66 (SQL Injection)"
            ),
            mo.md("---"),
            hints,
        ]
    )
    return (
        check_bypass,
        check_cols,
        check_flag,
        check_probe,
        check_schema,
        hints,
        sidebar_content,
    )


@app.cell
def __(mo, sidebar_content):
    return (mo.sidebar(sidebar_content),)


@app.cell(hide_code=True)
def __(df_employees, mo):
    # Tab 1: Alert Triage & Scope View
    triage_view = mo.vstack(
        [
            mo.md("""
            # 🌐 Assessment: __INCIDENT_CODENAME__
            ### Web Application Security: In-Band SQL Injection & Exfiltration Workbench
            """),
            mo.callout(
                mo.md(
                    "**AppSec Penetration Testing Notice**: The Employee Directory search endpoint (`/api/search?q=`) directly concatenates untrusted user queries into SQL commands. As the AppSec assessor, exploit the SQL injection vulnerability to determine query structure, enumerate backend schema objects via `sqlite_master`, extract restricted payroll audit records, and verify parameterized remediation."
                ),
                kind="warn",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value=f"{len(df_employees)} Records",
                        label="Public Directory Size",
                        caption="Legitimate Employees",
                        bordered=True,
                    ),
                    mo.stat(
                        value="CWE-89",
                        label="Primary Vulnerability",
                        caption="In-Band Union SQLi",
                        bordered=True,
                    ),
                    mo.stat(
                        value="HIGH (CVSS 8.6)",
                        label="Risk Assessment",
                        caption="Arbitrary Database Read",
                        bordered=True,
                    ),
                    mo.stat(
                        value="sqlite3",
                        label="DBMS Technology",
                        caption="Embedded Relational Engine",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
            mo.md("---"),
            mo.md("""
            ### 🏛️ Web Application Architecture & Injection Surface
            ```text
            [Browser / Client] ─── HTTP GET /api/search?q=' UNION... ───> [Python / Flask Backend]
                                                                                   │
                                                          [Vulnerable Query Build] │ cur.execute(f"...WHERE name LIKE '%{q}%'")
                                                                                   v
                                                                        [SQLite Database Engine]
                                                                        ├── employees (Public)
                                                                        └── payroll_audit (CONFIDENTIAL)
            ```
            """),
        ]
    )
    return (triage_view,)


@app.cell(hide_code=True)
def __(mo):
    # Tab 2: SQL Injection Interactive Workbench Controls
    payload_presets = mo.ui.dropdown(
        options=[
            "-- Select Injection Methodology Preset --",
            "Single Quote Probe: '",
            "Boolean Tautology: ' OR 1=1 --",
            "Column Arity Probe: ' UNION SELECT 1, 2, 3, 4 --",
            "Schema Enumeration: ' UNION SELECT 1, name, sql, 4 FROM sqlite_master WHERE type='table' --",
            "Audit Exfiltration: ' UNION SELECT audit_id, employee_ref, discrepancy_amount, notes FROM payroll_audit --",
        ],
        value="-- Select Injection Methodology Preset --",
        label="Quick Payloads:",
    )
    search_input = mo.ui.text(
        value="Sharma",
        placeholder="Enter search term or SQL injection payload...",
        label="Search Query Input (`q`):",
    )
    return payload_presets, search_input


@app.cell(hide_code=True)
def __(conn, mo, payload_presets, pd, search_input):
    # Reactive Payload Synchronization
    current_q = search_input.value
    if payload_presets.value != "-- Select Injection Methodology Preset --":
        preset_val = payload_presets.value.split(": ", 1)[-1]
        current_q = preset_val

    raw_sql = f"SELECT id, name, department, email FROM employees WHERE name LIKE '%{current_q}%'"

    error_msg = None
    query_results = []
    columns = ["id", "name", "department", "email"]

    try:
        cur = conn.cursor()
        cur.execute(raw_sql)
        rows = cur.fetchall()
        query_results = rows
        if cur.description:
            columns = [d[0] for d in cur.description]
    except Exception as e:
        error_msg = str(e)

    if error_msg:
        status_badge = mo.callout(
            mo.md(f"⚠️ **SQLite Database Error**: `{error_msg}`"),
            kind="danger",
        )
        res_display = mo.md("No rows returned due to query execution error.")
    else:
        status_badge = mo.callout(
            mo.md(f"✅ **Query Executed Successfully** — `{len(query_results)}` row(s) returned."),
            kind="success",
        )
        df_res = pd.DataFrame(query_results, columns=columns) if query_results else pd.DataFrame()
        res_display = mo.ui.table(df_res, selection=None, pagination=True, page_size=6) if not df_res.empty else mo.md("0 matching records found.")

    sqli_view = mo.vstack(
        [
            mo.md("## 🔬 In-Band SQL Injection Interactive Console"),
            mo.md(
                "Test query parameters against the live `/api/search` endpoint. Select a preset or type arbitrary payloads directly:"
            ),
            mo.hstack([payload_presets, search_input], justify="start", gap=2),
            mo.md("---"),
            mo.md(f"### 📡 Executed Query String:\n```sql\n{raw_sql}\n```"),
            status_badge,
            mo.md("---"),
            mo.md("### 📊 Database Output Table:"),
            res_display,
        ]
    )
    return (
        columns,
        current_q,
        error_msg,
        payload_presets,
        query_results,
        raw_sql,
        res_display,
        sqli_view,
        status_badge,
    )


@app.cell(hide_code=True)
def __(conn, df_employees, mo, pd, raw_db_bytes, re):
    # Tab 3: Python Scratchpad & Database File Export
    download_db = mo.download(
        data=raw_db_bytes,
        filename="corp_directory.db",
        label="📥 Export corp_directory.db",
    )
    scratchpad = mo.ui.code_editor(
        value="# Python AppSec Database Analytics Scratchpad\n# Available: conn (sqlite3 connection), df_employees, pd, re\n\n# Query the internal sqlite_master directly:\npd.read_sql_query('SELECT type, name, sql FROM sqlite_master', conn)\n",
        language="python",
        label="AppSec Python Console:",
    )
    return download_db, scratchpad


@app.cell(hide_code=True)
def __(conn, df_employees, download_db, mo, pd, re, scratchpad):
    # Tab 3: Reactive Python Execution Engine
    code_text = scratchpad.value.strip()
    eval_result = None

    if code_text:
        locs = {
            "conn": conn,
            "df_employees": df_employees,
            "pd": pd,
            "re": re,
        }
        try:
            lines = [
                l
                for l in code_text.splitlines()
                if l.strip() and not l.strip().startswith("#")
            ]
            if lines:
                exec_chunk = "\n".join(lines[:-1])
                last_line = lines[-1]
                if exec_chunk:
                    exec(exec_chunk, {"__builtins__": __builtins__}, locs)
                try:
                    res = eval(last_line, {"__builtins__": __builtins__}, locs)
                except SyntaxError:
                    exec(last_line, {"__builtins__": __builtins__}, locs)
                    res = locs.get("output", locs.get("result", "Script executed successfully."))

                if isinstance(res, pd.DataFrame):
                    eval_result = mo.ui.table(res, selection=None, pagination=True, page_size=6)
                elif isinstance(res, pd.Series):
                    eval_result = mo.ui.table(res.to_frame(), selection=None, pagination=True)
                elif res is not None:
                    eval_result = mo.md(f"```python\n{repr(res)}\n```")
                else:
                    eval_result = mo.md("✅ *Execution completed without output.*")
            else:
                eval_result = mo.md("ℹ️ *Enter Python code above to run interactive queries.*")
        except Exception as e:
            eval_result = mo.callout(
                mo.md(f"**Execution Error**: `{type(e).__name__}: {str(e)}`"),
                kind="danger",
            )
    else:
        eval_result = mo.md("ℹ️ *Analyst scratchpad idle.*")

    scratchpad_view = mo.vstack(
        [
            mo.md("## 💻 Analyst Python AppSec Scratchpad"),
            mo.md(
                "Inspect the database tables directly or download the authentic raw SQLite database file:"
            ),
            mo.hstack([download_db], justify="start"),
            mo.md("---"),
            scratchpad,
            mo.md("---"),
            mo.md("### 📤 Execution Output:"),
            eval_result,
        ]
    )
    return code_text, eval_result, scratchpad_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 4: Secure Remediation & Parameterized Diff View
    remediation_view = mo.vstack(
        [
            mo.md("## 🛡️ Secure Code Remediation: Parameterized Queries"),
            mo.callout(
                mo.md(
                    "**CWE-89 Remediation Standard**: String interpolation (e.g., `f\"... WHERE name LIKE '%{q}%'\"`) compiles untrusted data as executable SQL code. Using parameterized queries ensures user input is strictly treated as literal data, completely neutralizing injection."
                ),
                kind="info",
            ),
            mo.ui.code_editor(
                value="""# --- VULNERABLE CODE ---
def search_employees_insecure(query: str):
    sql = f"SELECT id, name, department, email FROM employees WHERE name LIKE '%{query}%'"
    return conn.cursor().execute(sql).fetchall()

# --- SECURE REMEDIATION (Parameterized Prepared Statement) ---
def search_employees_secure(query: str):
    sql = "SELECT id, name, department, email FROM employees WHERE name LIKE ?"
    pattern = f"%{query}%"
    return conn.cursor().execute(sql, (pattern,)).fetchall()
""",
                language="python",
                label="Vulnerable vs Hardened Parameterized Implementation:",
            ),
        ]
    )
    return (remediation_view,)


@app.cell(hide_code=True)
def __(mo):
    # Tab 5: Flag Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{sqli_union_payroll_audit_...}",
        label="Enter Exfiltrated Payroll Audit Flag to Verify:",
    )
    return (candidate_flag,)


@app.cell(hide_code=True)
def __(candidate_flag, hashlib, mo, re):
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md(
            "Enter the flag exfiltrated from the internal `payroll_audit` records."
        )
        report_view = mo.md("🔒 *Audit Finding Verification Report locked until valid flag is provided.*")
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md(
                "🎉 **FLAG VERIFIED CORRECT!**\n\n"
                "Your exfiltrated payroll audit finding is confirmed! Now submit this flag in the left portal pane to claim 150 points and Web Application Security competency!"
            ),
            kind="success",
        )
        report_view = mo.vstack(
            [
                mo.md("### 📋 Confirmed Vulnerability Assessment Report:"),
                mo.md("""
                | Assessment Parameter | Confirmed Value | Standard Reference |
                | :--- | :--- | :--- |
                | **Vulnerability Class** | In-Band Union-Based SQL Injection | CWE-89 / OWASP A03 |
                | **Vulnerable Parameter** | `q` (GET search query parameter) | RFC 3986 URI Query |
                | **Original Query Arity** | 4 Columns (`id, name, department, email`) | SQLite Engine Arity |
                | **Compromised Table** | `payroll_audit` (Internal Non-Public Vault) | MeitY Data Classification |
                | **Remediation Delivered** | Parameterized query specification verified | OWASP ASVS 4.0 §5.3 |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(
            mo.md(
                "❌ Incorrect flag. Use UNION injection to discover hidden tables in `sqlite_master`, then extract records from the internal `payroll_audit` table."
            ),
            kind="danger",
        )
        report_view = mo.md("🔒 *Audit Finding Verification Report locked until valid flag is provided.*")
    else:
        flag_feedback = mo.callout(
            mo.md(
                "⚠️ Flag format invalid. Flags must begin with `FLAG{` and end with `}`."
            ),
            kind="warn",
        )
        report_view = mo.md("🔒 *Audit Finding Verification Report locked until valid flag is provided.*")

    verification_view = mo.vstack(
        [
            mo.md("## 🏁 Step 5: Verify Exfiltrated Flag & Audit Report"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            report_view,
        ]
    )
    return flag_feedback, report_view, target_hash, val, verification_view


@app.cell
def console_root(
    mo,
    remediation_view,
    scratchpad_view,
    sidebar_content,
    sqli_view,
    triage_view,
    verification_view,
):
    styles = mo.Html("""
    <style>
    /* Ensure Marimo chrome sidebar & inspection panels are visible */
    [data-testid="chrome-sidebar"], #app-chrome-sidebar, #app-chrome-panel, .resize-handle {
        display: block !important;
    }

    /* Un-hide all Marimo cells while keeping action toolbar hidden */
    .marimo-cell:not(:has(.console-topbar)) {
        display: block !important;
    }

    [data-testid="drag-button"],
    [data-testid="cell-actions-button"],
    [data-testid="create-cell-button"],
    [data-testid="run-button"],
    [data-testid="hide-code-button"],
    [data-testid="fullscreen-output-button"],
    [data-testid="expand-output-button"],
    .hover-actions-parent > .hover-action,
    .shoulder-right,
    .cell-actions,
    .cell-actions-button,
    .cell-bottom-menu,
    .add-cell-button {
        display: none !important;
    }

    [data-testid="filename-input"],
    [data-testid="chrome-controls-top-right"],
    [data-testid="chrome-controls-bottom-right"],
    [data-testid="chrome-footer"],
    [data-testid="footer-panel"] {
        display: none !important;
    }

    .marimo-cell:has(.console-topbar) {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 4px !important;
    }

    #App, main, #app-chrome-body, [data-testid="column-container"] {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .console-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 10px;
    }
    .console-topbar .title {
        font-size: 13px;
        font-weight: 700;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .console-topbar .live-badge {
        background: #0284c7;
        color: white;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }
    </style>
    """)

    # Invisible anchor div keeps the .console-topbar CSS selector working
    header = mo.Html(
        '<div class="console-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>'
    )

    console = mo.ui.tabs(
        {
            "📋 Triage & Scope": triage_view,
            "🔬 SQLi Interactive Console": sqli_view,
            "💻 Python AppSec Scratchpad": scratchpad_view,
            "🛡️ Secure Remediation": remediation_view,
            "📌 Assessment Checklist": sidebar_content,
            "🏁 Verify & Audit Report": verification_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
