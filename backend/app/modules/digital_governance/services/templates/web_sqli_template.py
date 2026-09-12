"""Upgraded Web Application Security & Citizen Directory SQLi Template (Module 4)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
import hashlib
import json
import random
import sqlite3

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class WebSqliTemplate(BaseChallengeTemplate):
    """
    Template for Citizen Welfare Directory SQL Injection & DPDP Act Breach.
    Synthesizes an authentic SQLite database with citizen records and a Marimo notebook
    supporting live SQL queries and UNION injection analysis.
    """

    template_id = "04-vulnerable-web-app"
    title = "Citizen Portal: SQLi & DPDP Act Citizen Records Breach"
    category = "Web Application Security / Data Privacy"
    difficulty = "Intermediate"
    base_points = 150
    duration_minutes = 45
    competency_id = "web_security"
    competency_weight = 1.2
    tags = ["web", "sqli", "data-privacy", "dpdp", "aadhaar", "sql", "owasp", "cert-in"]
    mitre_techniques = ["T1190", "T1059.007", "T1505.003"]

    DEPARTMENTS = ["Civil Supplies", "Social Welfare", "State Transport", "Revenue Department"]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "department": {"type": "str", "description": "Vulnerable government portal department"},
            "database_name": {"type": "str", "description": "SQLite database file name"},
            "vulnerable_param": {"type": "str", "description": "Vulnerable query parameter"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        dept = rng.choice(self.DEPARTMENTS)

        slots = {
            "incident_codename": f"Operation Suraksha-{rng.randint(401, 999)}",
            "department": dept,
            "database_name": "corp_directory.db",
            "vulnerable_param": "citizen_name",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        return f"FLAG{{sqli_union_citizen_leak_{slots['seed_hash'][:8]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "The search parameter string-concatenates input directly: `SELECT * FROM citizens WHERE name LIKE '%{input}%'`. Test standard SQL escape injection like `' OR 1=1 --`.",
                "penalty": 20,
            },
            {
                "id": 2,
                "content": "Use `UNION SELECT` to dump the hidden `dpdp_compliance_vault` table: `' UNION SELECT 1, category, dpo_notes, flag_token FROM dpdp_compliance_vault --`.",
                "penalty": 35,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Audit the search endpoint query in the {slots['department']} Citizen Welfare Directory.",
            "Craft a SQL injection payload to bypass authentication and dump schema tables.",
            "Extract the Data Protection Officer (DPO) incident recovery flag from the audit vault.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Citizen Welfare Portal Breach Briefing: {slots['incident_codename']}

Under Section 8 of the Digital Personal Data Protection Act 2023 (DPDP Act), a Data Fiduciary must implement reasonable security safeguards.

A critical SQL injection flaw was reported in the `{slots['department']}` citizen portal, allowing unauthenticated adversaries to execute arbitrary SQL queries against `{slots['database_name']}`.

Your mandate:
1. Examine the SQLite database schema and citizen directory queries.
2. Execute a UNION-based SQL injection to enumerate hidden compliance tables.
3. Exfiltrate the DPO remediation flag to verify exploitability and containment.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)
        db_path = data_dir / slots["database_name"]

        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 1. Public table: citizens
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            ration_card_no TEXT NOT NULL,
            subsidy_amount REAL NOT NULL
        )
        """)
        sample_citizens = [
            (1, "Ramesh Chandra Sharma", "RC-DEL-10492", 2400.0),
            (2, "Sunita Devi Patel", "RC-UP-88392", 3600.0),
            (3, "Ananya Banerjee", "RC-WB-44910", 1800.0),
            (4, "Mohd. Tariq Ansari", "RC-BIH-30291", 4200.0),
            (5, "Gurpreet Singh", "RC-PUN-99201", 2900.0),
        ]
        cursor.executemany("INSERT INTO citizens VALUES (?, ?, ?, ?)", sample_citizens)

        # 2. Hidden table: dpdp_compliance_vault
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dpdp_compliance_vault (
            id INTEGER PRIMARY KEY,
            compliance_category TEXT NOT NULL,
            dpo_notes TEXT NOT NULL,
            flag_token TEXT NOT NULL
        )
        """)
        cursor.execute(
            "INSERT INTO dpdp_compliance_vault VALUES (?, ?, ?, ?)",
            (1, "DPDP_ACT_2023_AUDIT", "Significant Data Fiduciary (SDF) security assessment token", flag),
        )

        conn.commit()
        conn.close()

        return {slots["database_name"]: db_path}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = f'''import marimo

__generated_with = "0.17.6"
app = marimo.App(width="full", app_title="Citizen Portal SQLi: {slots.get('incident_codename', 'Suraksha')}")


@app.cell(hide_code=True)
def __():
    import json
    import sqlite3
    import hashlib
    from pathlib import Path
    import pandas as pd
    import marimo as mo
    return Path, hashlib, json, mo, pd, sqlite3


@app.cell(hide_code=True)
def __(Path, sqlite3):
    p_db = next((p for p in [Path("data/{slots.get('database_name', 'corp_directory.db')}"), Path("../data/{slots.get('database_name', 'corp_directory.db')}")] if p.exists()), None)
    conn = sqlite3.connect(str(p_db)) if p_db else None
    return conn, p_db


@app.cell
def __(conn, mo):
    mo.md(f"""
    # 🏛️ Citizen Portal: {slots.get('incident_codename', 'Investigation')}
    Department: **{slots.get('department', 'Social Welfare')}** | Database: `{slots.get('database_name', 'corp_directory.db')}`

    The portal search query vulnerability:
    ```sql
    SELECT id, full_name, ration_card_no, subsidy_amount 
    FROM citizens 
    WHERE full_name LIKE '%<USER_INPUT>%'
    ```
    """)
    return


@app.cell
def __(mo):
    search_input = mo.ui.text(placeholder="Enter search term or SQL payload e.g. Sharma or ' OR 1=1 --", label="Citizen Search Box")
    return search_input,


@app.cell
def __(conn, mo, pd, search_input):
    val = search_input.value.strip()
    if not val or not conn:
        df_res = pd.DataFrame()
        err_msg = ""
    else:
        # Vulnerable simulated execution
        query = f"SELECT id, full_name, ration_card_no, subsidy_amount FROM citizens WHERE full_name LIKE '%{{val}}%'"
        try:
            df_res = pd.read_sql_query(query, conn)
            err_msg = ""
        except Exception as e:
            df_res = pd.DataFrame()
            err_msg = str(e)

    mo.vstack([
        search_input,
        mo.md(f"**Executing Query:** `SELECT id, full_name, ration_card_no, subsidy_amount FROM citizens WHERE full_name LIKE '%{{val}}%'`") if val else mo.md(""),
        mo.md(f"⚠️ **SQL Error:** `{{err_msg}}`") if err_msg else mo.ui.table(df_res) if not df_res.empty else mo.md("*(No records returned)*")
    ])
    return df_res, err_msg, query, val


@app.cell
def __(hashlib, mo):
    target_hash = "{dynamic_hash}"
    flag_input = mo.ui.text(placeholder="Enter flag e.g. FLAG{{...}}", label="Submit Verified Flag")
    return flag_input, target_hash


@app.cell
def __(flag_input, hashlib, mo, target_hash):
    user_flag = flag_input.value.strip()
    if not user_flag:
        result = mo.md("*(Enter flag above to verify solution)*")
    elif hashlib.sha256(user_flag.encode()).hexdigest() == target_hash:
        result = mo.md("### 🎯 FLAG ACCEPTED! SQLi vulnerability verified and reported under DPDP Act.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Use UNION SELECT to dump dpdp_compliance_vault.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
        target_nb.write_text(code, encoding="utf-8")
        return target_nb

