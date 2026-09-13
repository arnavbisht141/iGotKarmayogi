"""SQLAlchemy Database Models for Digital Governance & Cybersecurity Module.

Includes CTF sandbox templates, challenges, active sessions, and user competencies.
"""

import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CyberSandboxTemplate(Base):
    __tablename__ = "cyber_sandbox_templates"

    id = Column(String(100), primary_key=True, index=True)  # Human-created template identifier
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="intermediate")
    competency_id = Column(String(100), default="soc_investigation")
    points = Column(Integer, default=100)
    duration_minutes = Column(Integer, default=45)
    tags_json = Column(Text, default="[]")
    mitre_techniques_json = Column(Text, default="[]")
    scenario_template = Column(Text, nullable=False)
    instructions_template = Column(Text, nullable=False)
    hints_template_json = Column(Text, default="[]")
    artifacts_spec_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    challenges = relationship("CyberSandboxChallenge", back_populates="template")


class CyberSandboxChallenge(Base):
    __tablename__ = "cyber_sandbox_challenges"

    id = Column(String(100), primary_key=True, index=True)
    template_id = Column(String(100), ForeignKey("cyber_sandbox_templates.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="intermediate")
    points = Column(Integer, default=100)
    duration_minutes = Column(Integer, default=45)
    competency_id = Column(String(100), default="soc_investigation")
    is_flagship = Column(Boolean, default=False)
    tags_json = Column(Text, default="[]")
    mitre_techniques_json = Column(Text, default="[]")
    objectives_json = Column(Text, default="[]")
    scenario_markdown = Column(Text, nullable=False)
    flag = Column(String(255), nullable=False)
    hints_json = Column(Text, default="[]")  # JSON list of hints with point penalties
    artifacts_json = Column(Text, default="{}")  # JSON map of telemetry and evidence files
    notebook_code = Column(Text, nullable=False)  # Full interactive Marimo Python notebook code
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    template = relationship("CyberSandboxTemplate", back_populates="challenges")
    sessions = relationship("CyberSandboxSession", back_populates="challenge", cascade="all, delete-orphan")


class CyberSandboxSession(Base):
    __tablename__ = "cyber_sandbox_sessions"

    id = Column(String(100), primary_key=True, index=True)  # session_id e.g. "sess_..."
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    challenge_id = Column(String(100), ForeignKey("cyber_sandbox_challenges.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="running")  # running, stopped, expired, solved
    assigned_port = Column(Integer, nullable=False)
    flag = Column(String(255), nullable=False)  # unique dynamic flag for this session
    unlocked_hints_json = Column(Text, default="[]")
    total_penalties = Column(Integer, default=0)
    final_score = Column(Integer, default=0)
    is_solved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    solved_at = Column(DateTime, nullable=True)

    challenge = relationship("CyberSandboxChallenge", back_populates="sessions")
    user = relationship("User", back_populates="cyber_sessions")


class UserCyberCompetency(Base):
    __tablename__ = "user_cyber_competencies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    soc_investigation = Column(Integer, default=0)
    phishing_analysis = Column(Integer, default=0)
    cloud_security = Column(Integer, default=0)
    dpi_security = Column(Integer, default=0)
    digital_forensics = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    solved_challenges_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="cyber_competency")

