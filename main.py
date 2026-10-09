
import json
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from agent_workflow import build_review_graph
from database import Base, engine, get_db
from models import Review
from scanner import scan_python_code
from schemas import ReviewRequest, ReviewResponse, ReviewSummary


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Autonomous AI Code Review & Security Audit Platform",
    description="AI agents for code analysis and security auditing",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "message": "AI Code Review Platform is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reviews", response_model=ReviewResponse)
def create_review(
    payload: ReviewRequest,
    db: Session = Depends(get_db),
):
    if not payload.filename.lower().endswith(".py"):
        raise HTTPException(
            status_code=400,
            detail="Please submit a Python (.py) filename.",
        )

    findings = scan_python_code(payload.code)

    try:
        graph = build_review_graph()
        result = graph.invoke({
            "code": payload.code,
            "filename": payload.filename,
            "findings": findings,
        })
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"AI review failed: {error}",
        ) from error

    review = Review(
        filename=payload.filename,
        status="completed",
        findings_json=json.dumps(findings),
        ai_report=result.get("final_report", ""),
        suggested_fix=result.get("suggested_fix", ""),
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "id": review.id,
        "filename": review.filename,
        "status": review.status,
        "findings": findings,
        "ai_report": review.ai_report,
        "suggested_fix": review.suggested_fix,
        "created_at": review.created_at,
    }


@app.get("/reviews", response_model=list[ReviewSummary])
def list_reviews(db: Session = Depends(get_db)):
    return (
        db.query(Review)
        .order_by(Review.created_at.desc())
        .limit(100)
        .all()
    )


@app.get("/reviews/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    review = (
        db.query(Review)
        .filter(Review.id == review_id)
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return {
        "id": review.id,
        "filename": review.filename,
        "status": review.status,
        "findings": json.loads(review.findings_json or "[]"),
        "ai_report": review.ai_report,
        "suggested_fix": review.suggested_fix,
        "created_at": review.created_at,
    }
