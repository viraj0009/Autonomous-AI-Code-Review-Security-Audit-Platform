
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

load_dotenv()


class ReviewState(TypedDict, total=False):
    code: str
    filename: str
    findings: list[dict]
    analysis: str
    security_review: str
    suggested_fix: str
    final_report: str


def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("Add GOOGLE_API_KEY to your .env file.")

    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        google_api_key=api_key,
        temperature=0.1,
    )


def code_analyzer(state: ReviewState):
    prompt = f"""
    You are the Code Analyzer Agent.
    Analyze the code's purpose, possible bugs, and logic issues.

    Code:
    {state['code']}
    """
    response = get_llm().invoke(prompt)
    return {"analysis": str(response.content)}


def security_auditor(state: ReviewState):
    prompt = f"""
    You are the Security Auditor Agent.
    Identify possible security risks and suggest mitigations.
    Static scanner findings:
    {state.get('findings', [])}

    Code:
    {state['code']}
    """
    response = get_llm().invoke(prompt)
    return {"security_review": str(response.content)}


def fix_generator(state: ReviewState):
    prompt = f"""
    You are the Fix Generator Agent.
    Suggest corrected Python code and explain the changes.
    Do not claim the code was tested.

    Code:
    {state['code']}

    Security review:
    {state.get('security_review', '')}
    """
    response = get_llm().invoke(prompt)
    return {"suggested_fix": str(response.content)}


def review_reporter(state: ReviewState):
    prompt = f"""
    You are the Review Reporter Agent.
    Create a concise report with:
    1. Summary
    2. Key findings
    3. Recommended actions
    4. Limitations

    Static findings: {state.get('findings', [])}
    Code analysis: {state.get('analysis', '')}
    Security review: {state.get('security_review', '')}
    """
    response = get_llm().invoke(prompt)
    return {"final_report": str(response.content)}


def build_review_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("code_analyzer", code_analyzer)
    graph.add_node("security_auditor", security_auditor)
    graph.add_node("fix_generator", fix_generator)
    graph.add_node("review_reporter", review_reporter)

    graph.add_edge(START, "code_analyzer")
    graph.add_edge("code_analyzer", "security_auditor")
    graph.add_edge("security_auditor", "fix_generator")
    graph.add_edge("fix_generator", "review_reporter")
    graph.add_edge("review_reporter", END)

    return graph.compile()