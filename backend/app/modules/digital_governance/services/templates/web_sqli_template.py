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
            "incident_codename": f"Operation AppSec-{rng.randint(401, 999)}",
            "target_app": "Corporate Directory & Payroll API",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        return f"FLAG{{sqli_union_payroll_leak_{slots['seed_hash'][:8]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "The search query parameter concatenates untrusted input. Test syntax with a single quote: ' OR 1=1 --",
                "penalty": 20,
            },
            {
                "id": 2,
                "content": "Query arity is 4 columns. Enumerate tables in sqlite_master, then inject: ' UNION SELECT id, employee_id, notes, flag FROM payroll_audit --",
                "penalty": 35,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            "Probe search input for SQL injection vulnerabilities using boolean tautologies and syntax breakers.",
            "Determine column arity using UNION SELECT technique.",
            "Enumerate hidden tables in sqlite_master and exfiltrate the payroll audit secret flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Web Application Security Assessment: {slots['incident_codename']}

The corporate directory search endpoint at `/api/search?q=` directly interpolates user input into backend SQL queries without sanitization.

Your mandate:
1. Exploit the SQL injection vulnerability to determine query structure.
2. Enumerate database schema objects via `sqlite_master`.
3. Extract restricted records from the internal `payroll_audit` table to recover the flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        db_path = data_dir / "corp_directory.db"

        flag = self.compute_flag(slots)

        # Build SQLite database
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS employees")
        cur.execute("DROP TABLE IF EXISTS payroll_audit")
        cur.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, email TEXT)")
        cur.execute("CREATE TABLE payroll_audit (id INTEGER PRIMARY KEY, employee_id INT, notes TEXT, flag TEXT)")

        employees = [
            (1, "Alice Smith", "Engineering", "alice@corp.internal"),
            (2, "Bob Miller", "Human Resources", "bob@corp.internal"),
            (3, "Charlie Davis", "Finance", "charlie@corp.internal"),
            (4, "Dana White", "Executive", "dana@corp.internal"),
            (5, "Elena Rostova", "Legal & Compliance", "elena@corp.internal"),
            (6, "Farhan Khan", "Operations", "farhan@corp.internal"),
        ]
        cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", employees)

        audits = [
            (1, 4, "Executive bonus disbursement verification", flag),
            (2, 3, "Quarterly tax withholding reconciliation", "N/A"),
            (3, 1, "Off-cycle project bonus clearance", "N/A"),
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


@app.cell
def __():
    import hashlib
    import json
    import re
    import sqlite3
    from pathlib import Path
    import marimo as mo
    import pandas as pd

    return Path, hashlib, json, mo, pd, re, sqlite3


@app.cell
def __(Path, sqlite3):
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
    return conn, db_file, possible_db_paths


@app.cell
def __(mo):
    # Analyst Sidebar: OWASP Classification, MITRE ATT&CK & Checklist
    check_probe = mo.ui.checkbox(
        label="1. Probe input for SQL syntax errors (single quote)", value=False
    )
    check_bypass = mo.ui.checkbox(
        label="2. Confirm boolean tautology bypass (' OR 1=1 --)", value=False
    )
    check_cols = mo.ui.checkbox(
        label="3. Enumerate query column count (UNION SELECT)", value=False
    )
    check_schema = mo.ui.checkbox(
        label="4. Enumerate schema via sqlite_master injection", value=False
    )
    check_flag = mo.ui.checkbox(
        label="5. Exfiltrate secret audit records & verify flag", value=False
    )

    hints = mo.accordion(
        {
            "💡 Hint 1: Syntax Probing": mo.md(
                "Test input with a single quote (`'`). If the application returns a syntax error, untrusted input is concatenated directly into the query string without sanitization."
            ),
            "💡 Hint 2: Determining Column Count": mo.md(
                "UNION SELECT injections require the injected query to return the exact same number of columns as the original query. Test `' UNION SELECT 1 --`, `' UNION SELECT 1, 2 --`, etc., until no column mismatch error occurs."
            ),
            "💡 Hint 3: Database Schema Enumeration": mo.md(
                "In SQLite, all table schemas are cataloged in `sqlite_master`. Inject a UNION query selecting `name` and `sql` from `sqlite_master` to uncover hidden internal tables."
            ),
        }
    )

    sidebar_content = mo.vstack(
        [
            mo.md("## 🌐 CyberLab AppSec Console"),
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
                "- **MITRE ATT&CK**: T1190 (Exploit Public-Facing Application)"
            ),
            mo.md("---"),
            hints,
        ]
    )

    mo.sidebar(sidebar_content)
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
def __(conn, mo):
    # Header Banner & Stat KPIs
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM employees")
    emp_count = cur.fetchone()[0]

    header_view = mo.vstack(
        [
            mo.md("""
            # 🌐 Incident: __INCIDENT_CODENAME__
            ### Web Application Security, SQL Injection & Data Exfiltration Workbench
            """),
            mo.callout(
                mo.md(
                    "**AppSec Penetration Testing Notice**: The Employee Directory search endpoint concatenates untrusted user queries directly into SQL commands. Exploit the SQL injection vulnerability to determine query structure, enumerate backend schema objects via `sqlite_master`, extract restricted audit records, and demonstrate secure parameterized remediation."
                ),
                kind="warn",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value="Vulnerable",
                        label="Input Sanitization",
                        caption="Direct String Interpolation",
                        direction="increase",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{emp_count} Records",
                        label="Visible Directory Entries",
                        caption="Public Employees Table",
                        bordered=True,
                    ),
                    mo.stat(
                        value="SQLite 3",
                        label="Database Engine",
                        caption="Backend Relational DBMS",
                        bordered=True,
                    ),
                    mo.stat(
                        value="OWASP A03",
                        label="Risk Classification",
                        caption="Critical SQL Injection Flaw",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
        ]
    )
    return cur, emp_count, header_view


@app.cell
def __(mo):
    # Step 1: Interactive SQL Injection Controls
    payload_preset = mo.ui.dropdown(
        options=[
            "Custom Injection Query",
            "1. Standard Search: 'Alice'",
            "2. Syntax Error Probe: '",
            "3. Boolean Filter Bypass: ' OR 1=1 --",
            "4. Column Count Enumeration: ' UNION SELECT 1, 2, 3, 4 --",
        ],
        value="1. Standard Search: 'Alice'",
        label="Methodology Preset:",
    )

    custom_payload_input = mo.ui.text(
        value="Alice",
        placeholder="Enter search term or SQL injection payload (e.g. ' UNION SELECT ...)...",
        label="SQL Injection Input (Query Parameter `q`):",
        full_width=True,
    )

    return custom_payload_input, payload_preset


@app.cell
def __(conn, custom_payload_input, mo, payload_preset, pd):
    # Step 1: Live Database Query Execution & Results Rendering
    active_query = custom_payload_input.value
    if payload_preset.value == "1. Standard Search: 'Alice'":
        active_query = "Alice"
    elif "Syntax Error Probe" in payload_preset.value:
        active_query = "'"
    elif "Boolean Filter Bypass" in payload_preset.value:
        active_query = "' OR 1=1 --"
    elif "Column Count Enumeration" in payload_preset.value:
        active_query = "' UNION SELECT 1, 2, 3, 4 --"

    constructed_sql = f"SELECT id, name, department, email FROM employees WHERE name LIKE '%{active_query}%'"

    query_success = False
    query_error = ""
    result_rows = []

    try:
        cur_exec = conn.cursor()
        cur_exec.execute(constructed_sql)
        result_rows = cur_exec.fetchall()
        query_success = True
    except Exception as err:
        query_error = str(err)
        query_success = False

    if query_success:
        df_results = pd.DataFrame(
            result_rows,
            columns=[
                "Col 1 (id)",
                "Col 2 (name)",
                "Col 3 (department)",
                "Col 4 (email)",
            ],
        )
        query_status_badge = mo.callout(
            mo.md(
                f"✅ **Database Execution Succeeded**: `{len(df_results)}` row(s) returned."
            ),
            kind="success",
        )
        results_view = mo.ui.table(
            df_results,
            selection=None,
            pagination=True,
            page_size=8,
            show_column_summaries=False,
        )
    else:
        df_results = pd.DataFrame()
        query_status_badge = mo.callout(
            mo.md(
                f"❌ **Database Execution Error**: `{query_error}`\n\n*This error indicates unsanitized SQL syntax injection!*"
            ),
            kind="danger",
        )
        results_view = mo.md("")

    step1_view = mo.vstack(
        [
            mo.md("## 🔬 Step 1: Interactive SQL Injection Console"),
            mo.md(
                "Test search inputs and SQL injection strings against the target employee directory. Observe the generated backend SQL statement and the returned database records:"
            ),
            payload_preset,
            custom_payload_input,
            mo.md("---"),
            mo.md("#### 🖥️ Backend SQL Query Executed:"),
            mo.md(f"```sql\n{constructed_sql}\n```"),
            query_status_badge,
            results_view,
        ]
    )
    return (
        active_query,
        constructed_sql,
        cur_exec,
        df_results,
        query_error,
        query_status_badge,
        query_success,
        result_rows,
        results_view,
        step1_view,
    )


@app.cell
def __(mo):
    # Step 2: Secure Code Remediation
    remediation_view = mo.vstack(
        [
            mo.md("## 🛡️ Step 2: Secure Code Remediation (Parameterized Queries)"),
            mo.md("""
            SQL injection occurs when untrusted input is interpolated directly into SQL syntax.
            """),
            mo.md("""
            #### ❌ Vulnerable Implementation:
            ```python
            # Untrusted input 'q' is formatted directly into the SQL string:
            sql = f"SELECT id, name, department, email FROM employees WHERE name LIKE '%{q}%'"
            cursor.execute(sql)
            ```
            
            #### ✅ Secure Parameterized Implementation:
            ```python
            # The database engine treats the query parameter strictly as literal data:
            sql = "SELECT id, name, department, email FROM employees WHERE name LIKE ?"
            cursor.execute(sql, (f"%{q}%",))
            ```
            """),
            mo.callout(
                mo.md(
                    "**Security Guarantee**: In a parameterized query, SQL metacontrol characters like quotes (`'`) or keywords (`UNION SELECT`) are never interpreted as SQL syntax, neutralizing 100% of injection attacks."
                ),
                kind="success",
            ),
        ]
    )
    return (remediation_view,)


@app.cell
def __(mo):
    # Step 3: Flag Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter Extracted Payroll Audit Flag to Verify:",
    )
    return (candidate_flag,)


@app.cell
def __(candidate_flag, hashlib, mo, re):
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md(
            "Enter the flag exfiltrated from the internal payroll audit records."
        )
        report_view = mo.md("🔒 *Audit Finding Verification Report locked until valid flag is provided.*")
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md(
                "🎉 **FLAG VERIFIED CORRECT!**\n\n"
                "Your exfiltrated payroll audit finding is confirmed! Now copy and submit this flag in the **Submit Flag** box in the left CyberLab portal pane to register your 150 points and Web Application Security competency!"
            ),
            kind="success",
        )
        report_view = mo.vstack(
            [
                mo.md("### 📋 Confirmed Vulnerability Assessment Report:"),
                mo.md("""
                | Vulnerability Factor | Assessment Detail |
                | :--- | :--- |
                | **Vulnerability Class** | In-Band Union-Based SQL Injection (CWE-89) |
                | **Vulnerable Parameter** | `q` (GET request query parameter) |
                | **Original Query Arity** | 4 Columns (`id, name, department, email`) |
                | **Exfiltrated Table** | `payroll_audit` |
                | **Root Cause** | Unsanitized string interpolation in query builder |
                | **Remediation Status** | Parameterized query specification delivered |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(
            mo.md(
                "❌ Incorrect flag. Use UNION injection to discover hidden tables in `sqlite_master`, then extract records from the internal audit table."
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

    step3_view = mo.vstack(
        [
            mo.md("## 🏁 Step 3: Verify Exfiltrated Incident Flag & Audit Report"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            report_view,
        ]
    )
    return flag_feedback, report_view, step3_view, target_hash, val


@app.cell
def console_root(header_view, mo, remediation_view, step1_view, step3_view):
    styles = mo.Html("""
    <style>
    [data-testid="chrome-sidebar"], #app-chrome-sidebar, #app-chrome-panel, .resize-handle { display: none !important; }
    [data-testid="drag-button"], [data-testid="cell-actions-button"], [data-testid="create-cell-button"], [data-testid="run-button"], [data-testid="hide-code-button"], [data-testid="fullscreen-output-button"], [data-testid="expand-output-button"], .hover-actions-parent > .hover-action, .shoulder-right, .cell-actions, .cell-actions-button, .cell-bottom-menu, .add-cell-button { display: none !important; }
    [data-testid="filename-input"], [data-testid="chrome-controls-top-right"], [data-testid="chrome-controls-bottom-right"], [data-testid="chrome-footer"], [data-testid="footer-panel"] { display: none !important; }
    .marimo-cell:not(:has(.cyberlab-topbar)) { display: none !important; }
    .marimo-cell .cm-editor, .marimo-cell .cm-scroller, .marimo-cell .cell-editor, [data-testid="cell-editor"] { display: none !important; height: 0 !important; overflow: hidden !important; }
    .marimo-cell:has(.cyberlab-topbar) { width: 100% !important; max-width: 100% !important; margin: 0 !important; padding: 0 4px !important; }
    #App, main, #app-chrome-body, [data-testid="column-container"] { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
    .cyberlab-topbar { display: flex; align-items: center; justify-content: space-between; background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 10px 16px; margin-bottom: 10px; }
    .cyberlab-topbar .title { font-size: 13px; font-weight: 700; color: #e2e8f0; display: flex; align-items: center; gap: 10px; }
    </style>
    """)
    header = mo.Html('<div class="cyberlab-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>')
    console = mo.ui.tabs(
        {
            "📋 Triage & Scope": header_view,
            "🔬 Step 1: SQLi Console": step1_view,
            "🛡️ Step 2: Secure Remediation": remediation_view,
            "🏁 Step 3: Verify & Audit Report": step3_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
