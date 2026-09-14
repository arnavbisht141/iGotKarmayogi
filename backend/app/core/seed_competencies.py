from sqlalchemy.orm import Session
from app.models.models import CompetencyDomain, Competency

DOMAINS = [
    ("statistical", "Statistical Competencies", "Survey design, sampling, national accounts, and official statistics methodology."),
    ("technical", "Technical Competencies", "Programming, data tooling, cloud, and AI/ML skills."),
    ("digital_governance", "Digital Governance", "Cybersecurity, data privacy, and government digital infrastructure."),
    ("behavioural", "Behavioural & Managerial", "Leadership, communication, ethics, and decision making."),
]

COMPETENCIES = {
    "statistical": [
        ("statistical_survey_design", "Survey Design"),
        ("statistical_sampling", "Sampling"),
        ("statistical_national_accounts", "National Accounts"),
        ("statistical_price_statistics", "Price Statistics"),
        ("statistical_labour_statistics", "Labour Statistics"),
        ("statistical_agricultural_statistics", "Agricultural Statistics"),
        ("statistical_industrial_statistics", "Industrial Statistics"),
        ("statistical_sdg_indicators", "SDG Indicators"),
        ("statistical_metadata_standards", "Metadata Standards"),
        ("statistical_data_quality", "Data Quality Frameworks"),
    ],
    "technical": [
        ("technical_python", "Python"),
        ("technical_r", "R"),
        ("technical_sql", "SQL"),
        ("technical_stata", "Stata"),
        ("technical_spss", "SPSS"),
        ("technical_sas", "SAS"),
        ("technical_gis", "GIS"),
        ("technical_data_visualization", "Data Visualization"),
        ("technical_ai_ml", "AI/ML"),
        ("technical_cloud_computing", "Cloud Computing"),
        ("technical_apis", "APIs"),
        ("technical_open_data", "Open Data"),
    ],
    "digital_governance": [
        ("digital_governance_cybersecurity", "Cybersecurity"),
        ("digital_governance_data_privacy", "Data Privacy"),
        ("digital_governance_digital_signatures", "Digital Signatures"),
        ("digital_governance_gov_cloud", "Government Cloud"),
        ("digital_governance_dpi", "Digital Public Infrastructure"),
    ],
    "behavioural": [
        ("behavioural_leadership", "Leadership"),
        ("behavioural_communication", "Communication"),
        ("behavioural_project_management", "Project Management"),
        ("behavioural_ethics", "Ethics"),
        ("behavioural_decision_making", "Decision Making"),
        ("behavioural_change_management", "Change Management"),
    ],
}


def seed_competency_taxonomy(db: Session) -> None:
    """Seeds the 4 competency domains and their competencies. Idempotent."""
    for code, name, description in DOMAINS:
        existing = db.query(CompetencyDomain).filter_by(code=code).first()
        if existing:
            continue
        domain = CompetencyDomain(code=code, name=name, description=description)
        db.add(domain)
        db.flush()
        for comp_code, comp_name in COMPETENCIES[code]:
            db.add(Competency(domain_id=domain.id, code=comp_code, name=comp_name, max_level=5))
    db.commit()
