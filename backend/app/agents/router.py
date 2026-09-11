import os
from typing import TypedDict, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from app.core.config import settings

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentChatRequest(BaseModel):
    message: str
    context: Optional[str] = None  # e.g., current course name or module

class AgentChatResponse(BaseModel):
    response: str
    source: str  # "langgraph-gemini", "langgraph-openai", or "langgraph-karmayogi-engine"

# Define LangGraph State
class AgentState(TypedDict):
    input_message: str
    context: Optional[str]
    output_message: str
    source: str

def process_query_node(state: AgentState) -> AgentState:
    user_query = state["input_message"].strip()
    query_lower = user_query.lower()
    ctx = state.get("context") or "iGot Karmayogi Learning Ecosystem"

    # Attempt 1: If Groq API key is present (Primary)
    if settings.GROQ_API_KEY:
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(
                model_name=settings.GROQ_MODEL,
                api_key=settings.GROQ_API_KEY,
                temperature=0.3
            )
            prompt = f"""You are the official iGot Karmayogi AI Learning Copilot for Indian civil servants and statisticians (MoSPI).
Context: {ctx}
User Question: {user_query}

Provide a concise, authoritative, professional civil-service guidance response in 2-4 sentences."""
            res = llm.invoke([HumanMessage(content=prompt)])
            return {
                "input_message": user_query,
                "context": ctx,
                "output_message": res.content,
                "source": "langgraph-groq"
            }
        except Exception as e:
            print(f"Groq call fallback: {e}")

    # Attempt 2: If OpenAI API key is present (Fallback 1)
    if settings.OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=0.3
            )
            prompt = f"""You are the official iGot Karmayogi AI Learning Copilot for Indian civil servants. Context: {ctx}. Question: {user_query}. Concise, clear answer."""
            res = llm.invoke([HumanMessage(content=prompt)])
            return {
                "input_message": user_query,
                "context": ctx,
                "output_message": res.content,
                "source": "langgraph-openai"
            }
        except Exception as e:
            print(f"OpenAI call fallback: {e}")

    # Attempt 3: If Google Gemini API key is present (Fallback 2)
    if settings.GOOGLE_API_KEY:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.3
            )
            prompt = f"""You are the official iGot Karmayogi AI Learning Copilot for Indian civil servants and statisticians (MoSPI).
Context: {ctx}
User Question: {user_query}

Provide a concise, authoritative, professional civil-service guidance response in 2-4 sentences."""
            res = llm.invoke([HumanMessage(content=prompt)])
            return {
                "input_message": user_query,
                "context": ctx,
                "output_message": res.content,
                "source": "langgraph-gemini"
            }
        except Exception as e:
            print(f"Gemini call fallback: {e}")

    # Built-in civil service statistical domain knowledge responder (deterministic LangGraph fallback)
    response_text = ""
    if any(k in query_lower for k in ["cpi", "inflation", "price", "consumer price"]):
        response_text = (
            "The Consumer Price Index (CPI) in India is compiled by the Central Statistics Office (CSO), MoSPI, using a Modified Laspeyres formula with base year 2012=100. "
            "Item weights reflect the Household Consumer Expenditure Survey, and elementary quotations use the Geometric Mean (Jevons Index) to minimize substitution bias."
        )
    elif any(k in query_lower for k in ["nss", "sample", "survey", "fsus", "hamlet"]):
        response_text = (
            "National Sample Surveys (NSSO) employ a multi-stage stratified sampling design where First Stage Units (FSUs) are census villages (rural) or UFS blocks (urban). "
            "Hamlet-group or sub-block formation is compulsory when the unit population exceeds 1,200 persons or 300 households."
        )
    elif any(k in query_lower for k in ["pfms", "dbt", "treasury", "tsa", "finance"]):
        response_text = (
            "The Public Financial Management System (PFMS) administers the Treasury Single Account (TSA) system, ensuring central scheme funds remain in the Consolidated Fund of India until real-time electronic disbursement via the Aadhaar Payment Bridge."
        )
    elif any(k in query_lower for k in ["assessment", "pass", "certificate", "exam"]):
        response_text = (
            "Karmayogi assessments require a minimum score of 70% to pass and earn an official verifiable certificate. "
            "Under Phase 0 policy, unlimited retakes are permitted, and your highest attempt status updates your official competency profile."
        )
    elif any(k in query_lower for k in ["python", "pandas", "data", "code"]):
        response_text = (
            "For public sector microdata analysis, vectorized Pandas routines should always be preferred over iterative Python loops, as they execute in optimized compiled C routines up to 100x faster."
        )
    else:
        response_text = (
            f"Hello! I am your iGot Karmayogi AI Assistant. I can assist you with statistical methodologies (NSS surveys, CPI calculation), "
            f"government financial systems (PFMS), official standards (UN-NQAF), and navigating your current learning modules in '{ctx}'."
        )

    return {
        "input_message": user_query,
        "context": ctx,
        "output_message": response_text,
        "source": "langgraph-karmayogi-engine"
    }

# Build LangGraph workflow
workflow = StateGraph(AgentState)
workflow.add_node("process_query", process_query_node)
workflow.set_entry_point("process_query")
workflow.add_edge("process_query", END)
agent_graph = workflow.compile()

@router.post("/chat", response_model=AgentChatResponse)
def agent_chat(req: AgentChatRequest):
    initial_state: AgentState = {
        "input_message": req.message,
        "context": req.context,
        "output_message": "",
        "source": "pending"
    }
    
    result = agent_graph.invoke(initial_state)
    
    return AgentChatResponse(
        response=result["output_message"],
        source=result["source"]
    )
