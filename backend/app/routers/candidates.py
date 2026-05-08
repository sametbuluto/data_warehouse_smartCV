"""Candidate API routes — upload CVs, list and get candidate details."""

import os
import logging
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, Candidate, Skill
from app.services.pdf_parser import extract_text_from_pdf
from app.services.nlp_processor import parse_resume
from app.schemas.models import CandidateResponse, CandidateListResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=CandidateResponse)
async def upload_cv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF resume, extract text, parse with NLP, and store in database."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Extract text from PDF
    try:
        raw_text = extract_text_from_pdf(file_path)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Parse resume with NLP
    parsed = parse_resume(raw_text)

    # Create candidate in database
    candidate = Candidate(
        name=parsed["name"],
        email=parsed["email"],
        phone=parsed["phone"],
        education=parsed["education"],
        experience_years=parsed["experience_years"],
        raw_text=raw_text,
        file_path=file_path,
    )
    db.add(candidate)
    db.flush()  # Get the ID

    # Add skills
    for skill_name in parsed["skills"]:
        db.add(Skill(candidate_id=candidate.id, skill_name=skill_name))

    db.commit()
    db.refresh(candidate)

    logger.info(f"Candidate uploaded: {candidate.name} with {len(parsed['skills'])} skills")

    return CandidateResponse(
        id=candidate.id,
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        education=candidate.education,
        experience_years=candidate.experience_years,
        skills=[s.skill_name for s in candidate.skills],
        file_path=candidate.file_path,
        created_at=candidate.created_at,
    )


@router.get("", response_model=list[CandidateListResponse])
def list_candidates(db: Session = Depends(get_db)):
    """Get all candidates with skill counts."""
    candidates = db.query(Candidate).order_by(Candidate.created_at.desc()).all()
    return [
        CandidateListResponse(
            id=c.id,
            name=c.name,
            email=c.email,
            skills_count=len(c.skills),
            experience_years=c.experience_years,
            created_at=c.created_at,
        )
        for c in candidates
    ]


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Get detailed candidate information."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    return CandidateResponse(
        id=candidate.id,
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        education=candidate.education,
        experience_years=candidate.experience_years,
        skills=[s.skill_name for s in candidate.skills],
        file_path=candidate.file_path,
        created_at=candidate.created_at,
    )


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Delete a candidate."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    db.delete(candidate)
    db.commit()
    return {"message": f"Candidate {candidate_id} deleted."}
