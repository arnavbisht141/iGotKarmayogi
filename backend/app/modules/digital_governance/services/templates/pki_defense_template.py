"""Digital Signatures, PKI & GeM e-Procurement Dispute Template (Domain 3)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import hashlib
import json
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class PkiDefenseTemplate(BaseChallengeTemplate):
    """
    Template for Digital Signatures, PKI, and GeM e-Tender Dispute Forensics.
    Synthesizes X.509 certificate metadata, CRL revocation logs, and OCSP timestamps
    under IT Act 2000 Section 3, 3A, and 42 (Controller of Certifying Authorities).
    """

    template_id = "06-pki-token-dispute"
    title = "PKI Defense: GeM e-Tender Dispute & Class 3 DSC Non-Repudiation"
    category = "Digital Signatures / PKI"
    difficulty = "Intermediate"
    base_points = 140
    duration_minutes = 45
    competency_id = "pki_signatures"
    competency_weight = 1.1
    tags = ["pki", "digital-signatures", "gem", "it-act", "dsc", "ocsp", "crl", "cca"]
    mitre_techniques = ["T1588.003", "T1552.004", "T1565"]

    CONTRACTORS = [
        ("M/s Bharat InfraTech Ltd", "TENDER-GEM-2026-9041"),
        ("M/s Apex Sovereign Solutions", "TENDER-GEM-2026-7732"),
        ("M/s National Digital Network", "TENDER-GEM-2026-5120"),
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "contractor_name": {"type": "str", "description": "Disputing tender contractor"},
            "tender_id": {"type": "str", "description": "GeM procurement tender ID"},
            "dsc_serial": {"type": "str", "description": "Class 3 DSC serial number"},
            "tender_value_crores": {"type": "int", "description": "Contract value in crores"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        contractor, tender_id = rng.choice(self.CONTRACTORS)

        slots = {
            "incident_codename": f"Operation Mudra-{rng.randint(601, 999)}",
            "contractor_name": contractor,
            "tender_id": tender_id,
            "dsc_serial": f"CCA-IN-DSC3-{rng.randint(100000, 999999)}",
            "tender_value_crores": rng.choice([35, 48, 75, 120]),
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        return f"FLAG{{pki_non_repudiation_valid_{slots['seed_hash'][:8]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Compare the submission timestamp in gem_tender_submission.json against the certificate revocation timestamp in crl_revocation_list.json.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": "Under Section 3A of the IT Act, a digital signature created prior to the published CRL revocation timestamp remains legally binding and non-repudiable. Inspect the evidentiary_token in crl_revocation_list.json.",
                "penalty": 25,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Audit the GeM tender submission timestamp for {slots['contractor_name']}.",
            f"Cross-reference DSC serial '{slots['dsc_serial']}' against the Certifying Authority CRL revocation timeline.",
            "Confirm statutory non-repudiation and extract the High Court evidentiary certification flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### High-Value GeM Tender Dispute: {slots['incident_codename']}

`{slots['contractor_name']}` submitted a winning ₹{slots['tender_value_crores']} crore bid for `{slots['tender_id']}` on the Government e-Marketplace (GeM) using their Class 3 Digital Signature Certificate (DSC).

Following commodity price fluctuations, the contractor filed a legal dispute claiming their cryptographic token was compromised and revoked before bid closing.

Your mandate:
1. Examine `gem_tender_submission.json` to verify cryptographic hash and Timestamp Authority (TSA) records.
2. Query `crl_revocation_list.json` to determine exact revocation publishing timing.
3. Validate non-repudiation under IT Act Sections 3 & 3A and recover the legal certification flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)

        submission_data = {
            "tender_id": slots["tender_id"],
            "contractor": slots["contractor_name"],
            "value_inr_crores": slots["tender_value_crores"],
            "bid_submission_time": "2026-09-12T14:45:10+05:30",
            "tsa_timestamp": "2026-09-12T14:45:10.421+05:30",
            "signer_dsc_serial": slots["dsc_serial"],
            "cert_issuer": "CN=eMudhra Consumer Services CA, O=CCA, C=IN",
            "digest_algorithm": "SHA-256 with RSA-2048",
            "digital_signature_valid": True,
        }
        sub_file = data_dir / "gem_tender_submission.json"
        sub_file.write_text(json.dumps(submission_data, indent=2), encoding="utf-8")

        crl_data = {
            "ca_issuer": "CN=eMudhra Consumer Services CA, O=CCA, C=IN",
            "crl_number": 8921,
            "published_at": "2026-09-12T17:30:00+05:30",
            "revoked_certificates": [
                {
                    "serial_number": slots["dsc_serial"],
                    "revocation_time": "2026-09-12T17:15:00+05:30",
                    "reason": "keyCompromise",
                    "ocsp_validation_status": "SIGNATURE_VALID_AT_SUBMISSION_TIME",
                    "evidentiary_token": flag,
                },
                {
                    "serial_number": "CCA-IN-DSC3-991042",
                    "revocation_time": "2026-09-11T09:00:00+05:30",
                    "reason": "affiliationChanged",
                },
            ],
        }
        crl_file = data_dir / "crl_revocation_list.json"
        crl_file.write_text(json.dumps(crl_data, indent=2), encoding="utf-8")

        return {
            "gem_tender_submission.json": sub_file,
            "crl_revocation_list.json": crl_file,
        }

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"PKI Dispute: {slots.get('incident_codename', 'Operation Mudra')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'INC-0606-PKI-DISPUTE'))
        code = code.replace("__CONTRACTOR__", slots.get('contractor_name', 'M/s Bharat InfraTech Ltd'))
        code = code.replace("__TENDER_ID__", slots.get('tender_id', 'TENDER-GEM-2026-9041'))
        code = code.replace("__DSC_SERIAL__", slots.get('dsc_serial', 'CCA-IN-DSC3-449102'))
        code = code.replace("__TENDER_CRORES__", str(slots.get('tender_value_crores', 48)))
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
    from pathlib import Path
    import re
    import marimo as mo
    import pandas as pd

    return Path, hashlib, json, mo, pd, re


@app.cell(hide_code=True)
def __(Path, json, pd):
    possible_sub = [
        Path("data/gem_tender_submission.json"),
        Path("../data/gem_tender_submission.json"),
        Path("/workspace/data/gem_tender_submission.json"),
    ]
    possible_crl = [
        Path("data/crl_revocation_list.json"),
        Path("../data/crl_revocation_list.json"),
        Path("/workspace/data/crl_revocation_list.json"),
    ]
    if "__file__" in globals():
        base = Path(__file__).resolve().parent.parent / "data"
        possible_sub.insert(0, base / "gem_tender_submission.json")
        possible_crl.insert(0, base / "crl_revocation_list.json")

    p_sub = next((p for p in possible_sub if p.exists()), None)
    p_crl = next((p for p in possible_crl if p.exists()), None)

    sub_data = json.loads(p_sub.read_text()) if p_sub else {}
    crl_data = json.loads(p_crl.read_text()) if p_crl else {}

    revoked_list = crl_data.get("revoked_certificates", [])
    df_crl = pd.DataFrame(revoked_list) if revoked_list else pd.DataFrame()

    return crl_data, df_crl, p_crl, p_sub, revoked_list, sub_data


@app.cell(hide_code=True)
def __(mo):
    # Sidebar
    check_tsa = mo.ui.checkbox(label="1. Audit TSA cryptographic timestamp", value=False)
    check_crl = mo.ui.checkbox(label="2. Query Certifying Authority CRL revocation timing", value=False)
    check_chronology = mo.ui.checkbox(label="3. Reconstruct execution chronology", value=False)
    check_sec3a = mo.ui.checkbox(label="4. Affirm non-repudiation under IT Act Sec 3A", value=False)
    check_flag = mo.ui.checkbox(label="5. Extract evidentiary certification token", value=False)

    sidebar_content = mo.vstack(
        [
            mo.md("## ✒️ GeM PKI Forensics Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Tender ID**: `__TENDER_ID__`"),
            mo.md("**Contractor**: `__CONTRACTOR__`"),
            mo.md("**Value**: `₹__TENDER_CRORES__ Crores`"),
            mo.md("---"),
            mo.md("### 🎯 Audit Checklist"),
            check_tsa,
            check_crl,
            check_chronology,
            check_sec3a,
            check_flag,
            mo.md("---"),
            mo.md("### 📜 Statutory Reference"),
            mo.md(
                "- **IT Act 2000 Section 3**: Authentication of Electronic Records\n"
                "- **IT Act 2000 Section 3A**: Electronic Signature & Legal Recognition\n"
                "- **Evidence Act Section 65B**: Admissibility of Electronic Records"
            ),
        ]
    )
    mo.sidebar(sidebar_content)
    return check_chronology, check_crl, check_flag, check_sec3a, check_tsa, sidebar_content


@app.cell(hide_code=True)
def __(mo, sub_data):
    # Tab 1: Scope & KPIs
    tab1_view = mo.vstack(
        [
            mo.md("""
            # ✒️ High-Value GeM Tender Dispute: __INCIDENT_CODENAME__
            ### Digital Signatures, PKI Revocation & Non-Repudiation Audit
            """),
            mo.callout(
                mo.md(
                    "**Legal Dispute Referral**: Contractor `__CONTRACTOR__` won tender `__TENDER_ID__` with a bid of ₹`__TENDER_CRORES__` Crores. The contractor subsequently sought repudiation of the contract, asserting their Class 3 DSC token was revoked. Examine the cryptographic submission timestamp authority (TSA) records versus CA Revocation List (CRL) publication timestamps to determine contract enforceability."
                ),
                kind="warn",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value=f"₹{sub_data.get('value_inr_crores', '__TENDER_CRORES__')} Cr",
                        label="Tender Value",
                        caption="Contract Commitment",
                        bordered=True,
                    ),
                    mo.stat(
                        value="14:45:10 IST",
                        label="Bid TSA Timestamp",
                        caption="Cryptographically Signed",
                        bordered=True,
                    ),
                    mo.stat(
                        value="17:15:00 IST",
                        label="Revocation Request",
                        caption="2 Hours 30 Min AFTER Bid",
                        direction="decrease",
                        bordered=True,
                    ),
                    mo.stat(
                        value="LEGALLY VALID",
                        label="IT Act Status",
                        caption="Sec 3A Non-Repudiable",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
        ]
    )
    return (tab1_view,)


@app.cell(hide_code=True)
def __(mo, sub_data):
    # Tab 2: Submission Metadata
    tab2_view = mo.vstack(
        [
            mo.md("## 📜 Bid Submission Cryptographic Metadata (`gem_tender_submission.json`)"),
            mo.md(f"""
            | Parameter | Signed Evidence Value |
            | :--- | :--- |
            | **Tender Reference** | `{sub_data.get('tender_id', 'N/A')}` |
            | **Contractor Name** | `{sub_data.get('contractor', 'N/A')}` |
            | **Submission Timestamp (TSA)** | `{sub_data.get('tsa_timestamp', 'N/A')}` |
            | **Signer DSC Serial** | `{sub_data.get('signer_dsc_serial', 'N/A')}` |
            | **Certificate Issuer** | `{sub_data.get('cert_issuer', 'N/A')}` |
            | **Digest Algorithm** | `{sub_data.get('digest_algorithm', 'N/A')}` |
            | **Digital Signature Valid** | `{sub_data.get('digital_signature_valid', False)}` |
            """),
        ]
    )
    return (tab2_view,)


@app.cell(hide_code=True)
def __(crl_data, df_crl, mo):
    # Tab 3: CRL Explorer
    crl_table = mo.ui.table(df_crl, selection=None, pagination=True, page_size=6) if not df_crl.empty else mo.md("No CRL records.")
    tab3_view = mo.vstack(
        [
            mo.md("## 🔏 Certifying Authority Revocation List (`crl_revocation_list.json`)"),
            mo.md(f"**CA Issuer**: `{crl_data.get('ca_issuer', 'N/A')}` | **Published At**: `{crl_data.get('published_at', 'N/A')}`"),
            crl_table,
        ]
    )
    return crl_table, tab3_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 4: Legal Timeline Comparison
    tab4_view = mo.vstack(
        [
            mo.md("## ⚖️ Chronological Timeline & Non-Repudiation Verdict"),
            mo.callout(
                mo.md(
                    "### 🏛️ High Court Legal Finding\n\n"
                    "1. **14:45:10 IST**: The bid was cryptographically sealed using Class 3 DSC `__DSC_SERIAL__`.\n"
                    "2. **17:15:00 IST**: The contractor requested certificate revocation (2h 30m after submission).\n"
                    "3. **17:30:00 IST**: Certifying Authority published CRL #8921.\n\n"
                    "**Statutory Precedent (Section 3A IT Act 2000)**: *A cryptographic signature affixed prior to the official revocation timestamp constitutes a valid and binding electronic commitment. The plea of token compromise is repudiated as an afterthought.*"
                ),
                kind="success",
            ),
        ]
    )
    return (tab4_view,)


@app.cell(hide_code=True)
def __(mo):
    # Tab 5: Flag Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter Evidentiary Token from CRL to Certify:",
    )
    return (candidate_flag,)


@app.cell(hide_code=True)
def __(candidate_flag, hashlib, mo, re):
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md("Enter the evidentiary_token found in the CRL record for this DSC.")
        report_view = mo.md("🔒 *Section 65B Electronic Evidentiary Certificate locked until flag verified.*")
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md("🎉 **EVIDENTIARY TOKEN CONFIRMED CORRECT!**\n\nSubmit this flag in the left portal pane to claim 140 points and PKI Defense competency!"),
            kind="success",
        )
        report_view = mo.vstack(
            [
                mo.md("### 🏛️ Indian Evidence Act Section 65B Certificate Generated:"),
                mo.md("""
                | Certificate Property | Evidentiary Attestation |
                | :--- | :--- |
                | **Statutory Provision** | Section 65B(4) Indian Evidence Act 1872 & IT Act 2000 |
                | **Certified Hash** | SHA-256 Validated Signature Timestamp |
                | **Enforceability** | **Upheld in Full** — Contractor forfeit liability affirmed |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(mo.md("❌ Incorrect token. Locate the `evidentiary_token` in the CRL Revocation tab."), kind="danger")
        report_view = mo.md("🔒 *Locked.*")
    else:
        flag_feedback = mo.callout(mo.md("⚠️ Format must begin with `FLAG{` and end with `}`."), kind="warn")
        report_view = mo.md("🔒 *Locked.*")

    tab5_view = mo.vstack(
        [
            mo.md("## 🏁 Section 65B Certification & Case Closure"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            report_view,
        ]
    )
    return flag_feedback, report_view, tab5_view, target_hash, val


@app.cell
def console_root(mo, tab1_view, tab2_view, tab3_view, tab4_view, tab5_view):
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
            "📋 Dispute Scope": tab1_view,
            "📜 Submission Metadata": tab2_view,
            "🔏 CRL Revocation": tab3_view,
            "⚖️ Legal Verdict (Sec 3A)": tab4_view,
            "🏁 Verify & Sec 65B": tab5_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
