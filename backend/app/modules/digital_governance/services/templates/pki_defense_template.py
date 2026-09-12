"""Digital Signatures, PKI & GeM e-Procurement Dispute Template (Domain 3)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
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
                "content": "Compare the submission timestamp in `gem_tender_submission.json` against the certificate revocation timestamp in `crl_revocation_list.json`.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": "Under Section 3A of the IT Act, a digital signature created prior to the published CRL revocation timestamp remains legally non-repudiable. Inspect the OCSP response token for the flag.",
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

Following commodity price fluctuations, the contractor filed a legal dispute claiming their USB cryptographic token was stolen and revoked before bid closing.

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

        # 1. gem_tender_submission.json
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

        # 2. crl_revocation_list.json
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

        code = f'''import marimo

__generated_with = "0.17.6"
app = marimo.App(width="full", app_title="PKI Dispute: {slots.get('incident_codename', 'Mudra')}")


@app.cell(hide_code=True)
def __():
    import json
    import hashlib
    from pathlib import Path
    import pandas as pd
    import marimo as mo
    return Path, hashlib, json, mo, pd


@app.cell(hide_code=True)
def __(Path, json):
    p_sub = next((p for p in [Path("data/gem_tender_submission.json"), Path("../data/gem_tender_submission.json")] if p.exists()), None)
    p_crl = next((p for p in [Path("data/crl_revocation_list.json"), Path("../data/crl_revocation_list.json")] if p.exists()), None)

    sub_data = json.loads(p_sub.read_text()) if p_sub else {{}}
    crl_data = json.loads(p_crl.read_text()) if p_crl else {{}}
    return crl_data, p_crl, p_sub, sub_data


@app.cell
def __(crl_data, mo, sub_data):
    mo.md(f"""
    # ✒️ GeM Tender PKI Audit: {slots.get('incident_codename', 'Investigation')}
    Contractor: **{slots.get('contractor_name', 'M/s Bharat InfraTech')}** | Tender: `{slots.get('tender_id', '')}`

    ### 📜 Bid Submission Timestamp Authority (TSA):
    - **Signed At:** `{{sub_data.get('bid_submission_time', 'N/A')}}`
    - **Signer DSC Serial:** `{{sub_data.get('signer_dsc_serial', 'N/A')}}`
    - **Signature Status:** `{{sub_data.get('digital_signature_valid', False)}}`

    ### 🔏 CA Revocation List (CRL):
    - **Revocation Published At:** `{{crl_data.get('published_at', 'N/A')}}`
    """)
    return


@app.cell
def __(crl_data, mo, pd):
    # CRL Inspection
    revoked = crl_data.get("revoked_certificates", [])
    df_rev = pd.DataFrame(revoked)
    mo.ui.table(df_rev)
    return df_rev, revoked


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
        result = mo.md("### 🎯 FLAG ACCEPTED! Statutory non-repudiation upheld under IT Act Section 3A.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Locate the evidentiary_token in the CRL revocation record.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
        target_nb.write_text(code, encoding="utf-8")
        return target_nb
