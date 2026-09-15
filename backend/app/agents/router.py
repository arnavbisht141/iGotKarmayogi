import logging
from typing import List, Optional, TypedDict

from fastapi import APIRouter, Depends
from langgraph.graph import END, StateGraph
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import GapAnalysis, GeneratedQuiz, Recommendation, User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentChatRequest(BaseModel):
    message: str
    context: Optional[str] = None  # e.g., current course name or module


class AgentAction(BaseModel):
    label: str
    href: str


class AgentChatResponse(BaseModel):
    response: str
    source: str
    intent: str = "tutor"
    actions: List[AgentAction] = []


class AgentState(TypedDict, total=False):
    input_message: str
    context: Optional[str]
    user_id: Optional[int]
    db: Session
    intent: str
    output_message: str
    source: str
    actions: List[dict]


INTENT_KEYWORDS = {
    "gap_analysis": ["skill gap", "gap analysis", "my gap", "competency gap", "competency profile", "weak area", "where am i weak", "assess my skills", "my competenc"],
    "recommendations": ["recommend", "which course", "what should i learn", "suggest a course", "learning path", "next course", "courses for me"],
    "quiz": ["quiz", "mcq", "practice question", "test me", "generate questions", "self assessment", "self-assessment"],
}

SIGN_IN_ACTION = {"label": "Sign in", "href": "/login"}


def supervisor_node(state: AgentState) -> AgentState:
    text = state["input_message"].lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(k in text for k in keywords):
            return {"intent": intent}
    return {"intent": "tutor"}


def _route(state: AgentState) -> str:
    return state["intent"]


def _deterministic_answer(query_lower: str, ctx: str) -> str:
    if any(k in query_lower for k in ["cpi", "inflation", "price", "consumer price"]):
        return (
            "The Consumer Price Index (CPI) in India is compiled by the National Statistics Office, MoSPI, using a Modified Laspeyres formula with base year 2012=100. "
            "Item weights reflect the Household Consumer Expenditure Survey, and elementary quotations use the Geometric Mean (Jevons Index) to minimize substitution bias."
        )
    if any(k in query_lower for k in ["nss", "sample", "survey", "fsus", "hamlet"]):
        return (
            "National Sample Surveys employ a multi-stage stratified sampling design where First Stage Units (FSUs) are census villages (rural) or UFS blocks (urban). "
            "Hamlet-group or sub-block formation is compulsory when the unit population exceeds 1,200 persons or 300 households."
        )
    if any(k in query_lower for k in ["pfms", "dbt", "treasury", "tsa", "finance"]):
        return (
            "The Public Financial Management System (PFMS) administers the Treasury Single Account system, keeping central scheme funds in the Consolidated Fund of India until real-time electronic disbursement via the Aadhaar Payment Bridge."
        )
    if any(k in query_lower for k in ["assessment", "pass", "certificate", "exam"]):
        return (
            "Karmayogi assessments require a minimum score of 70% to pass and earn a verifiable certificate. "
            "Retakes are permitted, and your highest attempt updates your competency profile."
        )
    if any(k in query_lower for k in ["python", "pandas", "data", "code"]):
        return "For public sector microdata analysis, prefer vectorized Pandas operations over Python loops; they run in optimized compiled code and are far faster."
    return (
        "I am your iGOT Karmayogi AI Assistant. Ask me about statistical methods (NSS surveys, CPI), your skill gaps, course recommendations, "
        f"or generating a practice quiz from your study material. Current context: {ctx}."
    )


def tutor_node(state: AgentState) -> AgentState:
    from app.agents.recommendation.agent import get_llm_client

    query = state["input_message"].strip()
    ctx = state.get("context") or "iGOT Karmayogi Learning Ecosystem"
    llm = get_llm_client()
    if llm is not None:
        try:
            prompt = (
                "You are the official iGOT Karmayogi AI Learning Copilot for officials of India's Official Statistical System (MoSPI).\n"
                f"Context: {ctx}\nQuestion: {query}\n\n"
                "Give a concise, accurate, practical answer in 2-4 sentences."
            )
            return {"output_message": llm.invoke(prompt).content, "source": "langgraph-tutor-llm", "actions": []}
        except Exception as e:
            logger.warning("Tutor LLM call failed, using deterministic responder: %s", e)
    return {"output_message": _deterministic_answer(query.lower(), ctx), "source": "langgraph-tutor-engine", "actions": []}


def gap_analysis_node(state: AgentState) -> AgentState:
    from app.agents.competency.gap_agent import run_gap_analysis

    if not state.get("user_id"):
        return {"output_message": "Sign in so I can analyse your competency profile across the four domains.", "source": "langgraph-gap-agent", "actions": [SIGN_IN_ACTION]}
    result = run_gap_analysis(state["db"], state["user_id"])
    gaps = sorted(result["gaps"], key=lambda g: g.gap, reverse=True)
    open_gaps = [g for g in gaps if g.gap > 0]
    if not open_gaps:
        message = "You currently meet the target level in all four competency domains. Consider an advanced quiz to keep your skills sharp."
    else:
        lines = [f"{g.domain.name}: level {g.current_level:.1f} of target {g.target_level:.1f}" for g in open_gaps[:3]]
        message = "I ran a fresh competency gap analysis. Your largest gaps are: " + "; ".join(lines) + ". I can recommend courses to close them."
    return {
        "output_message": message,
        "source": "langgraph-gap-agent",
        "actions": [{"label": "View competency profile", "href": "/competency"}, {"label": "Get recommendations", "href": "/recommendations"}],
    }


def recommendations_node(state: AgentState) -> AgentState:
    from app.agents.competency.gap_agent import run_gap_analysis
    from app.agents.recommendation.agent import generate_recommendations, get_llm_client

    if not state.get("user_id"):
        return {"output_message": "Sign in so I can recommend courses based on your competency gaps.", "source": "langgraph-recommendation-agent", "actions": [SIGN_IN_ACTION]}
    db, user_id = state["db"], state["user_id"]
    recs = db.query(Recommendation).filter_by(user_id=user_id, status="pending").order_by(Recommendation.score.desc()).all()
    if not recs:
        if not db.query(GapAnalysis).filter_by(user_id=user_id).first():
            run_gap_analysis(db, user_id)
        try:
            from app.agents.recommendation.indexer import get_real_pinecone_index
            pinecone_index = get_real_pinecone_index()
        except Exception as e:
            logger.warning("Pinecone unavailable for chat recommendations: %s", e)
            pinecone_index = None
        recs = generate_recommendations(db, user_id, pinecone_index=pinecone_index, llm_client=get_llm_client())
    if not recs:
        message = "You have no open competency gaps with matching courses right now. Great work."
    else:
        titles = [r.course.title for r in recs[:3] if r.course]
        message = "Based on your competency gaps, start with: " + "; ".join(titles) + "."
    return {"output_message": message, "source": "langgraph-recommendation-agent", "actions": [{"label": "See all recommendations", "href": "/recommendations"}]}


def quiz_node(state: AgentState) -> AgentState:
    actions = [{"label": "Generate a quiz from material", "href": "/quiz"}]
    latest = state["db"].query(GeneratedQuiz).order_by(GeneratedQuiz.created_at.desc()).first()
    if latest:
        actions.append({"label": f"Take: {latest.title[:40]}", "href": f"/quiz/{latest.id}"})
    return {
        "output_message": (
            "I can turn any learning material into a quiz. Upload a PDF, PowerPoint, Word document, or a video transcript, "
            "choose the number of questions and difficulty, and I will generate MCQs with explanations and instant feedback."
        ),
        "source": "langgraph-quiz-agent",
        "actions": actions,
    }


workflow = StateGraph(AgentState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("tutor", tutor_node)
workflow.add_node("gap_analysis", gap_analysis_node)
workflow.add_node("recommendations", recommendations_node)
workflow.add_node("quiz", quiz_node)
workflow.set_entry_point("supervisor")
workflow.add_conditional_edges(
    "supervisor", _route,
    {"tutor": "tutor", "gap_analysis": "gap_analysis", "recommendations": "recommendations", "quiz": "quiz"},
)
for node in ("tutor", "gap_analysis", "recommendations", "quiz"):
    workflow.add_edge(node, END)
agent_graph = workflow.compile()


@router.post("/chat", response_model=AgentChatResponse)
def agent_chat(
    req: AgentChatRequest,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = agent_graph.invoke({
        "input_message": req.message,
        "context": req.context,
        "user_id": current_user.id if current_user else None,
        "db": db,
    })
    return AgentChatResponse(
        response=result["output_message"],
        source=result["source"],
        intent=result["intent"],
        actions=[AgentAction(**a) for a in result.get("actions", [])],
    )
