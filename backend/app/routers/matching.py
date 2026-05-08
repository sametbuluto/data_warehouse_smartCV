"""Matching API routes — trigger matching, get results, explain scores."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, Candidate, JobPosting, MatchResult
from app.services.matching_engine import calculate_final_score, generate_explanation
from app.schemas.models import MatchResultResponse, MatchExplanation

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/match", tags=["Matching"])


def serialize_match_result(result: MatchResult, db: Session) -> MatchResultResponse:
    """Convert a MatchResult ORM object into the API response model."""
    candidate = db.query(Candidate).filter(Candidate.id == result.candidate_id).first()
    job = db.query(JobPosting).filter(JobPosting.id == result.job_id).first()

    return MatchResultResponse(
        id=result.id,
        candidate_id=result.candidate_id,
        candidate_name=candidate.name if candidate else "Unknown",
        job_id=result.job_id,
        job_title=job.title if job else "Unknown",
        skill_score=result.skill_score,
        experience_score=result.experience_score,
        education_score=result.education_score,
        semantic_score=result.semantic_score,
        final_score=result.final_score,
        matched_skills=result.matched_skills or [],
        missing_skills=result.missing_skills or [],
        created_at=result.created_at,
    )


@router.post("/{job_id}")
def run_matching(job_id: int, db: Session = Depends(get_db)):
    """Match ALL candidates against a specific job posting.

    This triggers the full ML pipeline:
    1. Load job requirements
    2. For each candidate: compute TF-IDF similarity + weighted score
    3. Save results and return ranked list
    """
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    candidates = db.query(Candidate).all()
    if not candidates:
        raise HTTPException(status_code=404, detail="No candidates found. Upload CVs first.")

    # Clear previous match results for this job
    db.query(MatchResult).filter(MatchResult.job_id == job_id).delete()

    results = []
    for candidate in candidates:
        candidate_skills = [s.skill_name for s in candidate.skills]

        scores = calculate_final_score(
            candidate_skills=candidate_skills,
            required_skills=job.required_skills or [],
            candidate_experience=candidate.experience_years,
            required_experience=job.min_experience,
            candidate_education=candidate.education or "Unknown",
            required_education=job.education_level or "Bachelor",
            cv_text=candidate.raw_text or "",
            job_text=job.description,
        )

        match_result = MatchResult(
            candidate_id=candidate.id,
            job_id=job.id,
            skill_score=scores["skill_score"],
            experience_score=scores["experience_score"],
            education_score=scores["education_score"],
            semantic_score=scores["semantic_score"],
            final_score=scores["final_score"],
            matched_skills=scores["matched_skills"],
            missing_skills=scores["missing_skills"],
        )
        db.add(match_result)
        results.append({
            "candidate_name": candidate.name,
            "final_score": scores["final_score"],
        })

    db.commit()

    # Sort by final_score descending
    results.sort(key=lambda x: x["final_score"], reverse=True)
    logger.info(f"Matching complete for job '{job.title}': {len(results)} candidates scored")

    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates": len(results),
        "results": results,
    }


@router.get("/{job_id}/results", response_model=list[MatchResultResponse])
def get_match_results(job_id: int, db: Session = Depends(get_db)):
    """Get ranked match results for a job posting."""
    results = (
        db.query(MatchResult)
        .filter(MatchResult.job_id == job_id)
        .order_by(MatchResult.final_score.desc())
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail="No match results found. Run matching first.")

    return [serialize_match_result(result, db) for result in results]


@router.post("/candidate/{candidate_id}")
def run_candidate_matching(candidate_id: int, db: Session = Depends(get_db)):
    """Match one candidate against ALL active job postings and store the results."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    jobs = db.query(JobPosting).all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No job postings found. Create jobs first.")

    candidate_skills = [skill.skill_name for skill in candidate.skills]
    results = []

    for job in jobs:
        db.query(MatchResult).filter(
            MatchResult.candidate_id == candidate.id,
            MatchResult.job_id == job.id,
        ).delete()

        scores = calculate_final_score(
            candidate_skills=candidate_skills,
            required_skills=job.required_skills or [],
            candidate_experience=candidate.experience_years,
            required_experience=job.min_experience,
            candidate_education=candidate.education or "Unknown",
            required_education=job.education_level or "Bachelor",
            cv_text=candidate.raw_text or "",
            job_text=job.description,
        )

        match_result = MatchResult(
            candidate_id=candidate.id,
            job_id=job.id,
            skill_score=scores["skill_score"],
            experience_score=scores["experience_score"],
            education_score=scores["education_score"],
            semantic_score=scores["semantic_score"],
            final_score=scores["final_score"],
            matched_skills=scores["matched_skills"],
            missing_skills=scores["missing_skills"],
        )
        db.add(match_result)
        results.append({"job_title": job.title, "final_score": scores["final_score"]})

    db.commit()
    results.sort(key=lambda item: item["final_score"], reverse=True)

    logger.info(f"Candidate matching complete for '{candidate.name}': {len(results)} jobs scored")

    return {
        "candidate_id": candidate.id,
        "candidate_name": candidate.name,
        "total_jobs": len(results),
        "results": results,
    }


@router.get("/candidate/{candidate_id}/results", response_model=list[MatchResultResponse])
def get_candidate_match_results(candidate_id: int, db: Session = Depends(get_db)):
    """Get all stored job-match results for a specific candidate."""
    results = (
        db.query(MatchResult)
        .filter(MatchResult.candidate_id == candidate_id)
        .order_by(MatchResult.final_score.desc())
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail="No match results found for candidate.")

    return [serialize_match_result(result, db) for result in results]


@router.get("/explain/{match_id}", response_model=MatchExplanation)
def explain_match(match_id: int, db: Session = Depends(get_db)):
    """Get a detailed explanation of a specific match result."""
    result = db.query(MatchResult).filter(MatchResult.id == match_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Match result not found.")

    candidate = db.query(Candidate).filter(Candidate.id == result.candidate_id).first()
    job = db.query(JobPosting).filter(JobPosting.id == result.job_id).first()

    explanation_text = generate_explanation(
        {
            "skill_score": result.skill_score,
            "experience_score": result.experience_score,
            "education_score": result.education_score,
            "semantic_score": result.semantic_score,
            "final_score": result.final_score,
            "matched_skills": result.matched_skills or [],
            "missing_skills": result.missing_skills or [],
        },
        candidate.name if candidate else "Unknown",
        job.title if job else "Unknown",
    )

    return MatchExplanation(
        candidate_name=candidate.name if candidate else "Unknown",
        job_title=job.title if job else "Unknown",
        final_score=result.final_score,
        skill_score=result.skill_score,
        experience_score=result.experience_score,
        education_score=result.education_score,
        semantic_score=result.semantic_score,
        matched_skills=result.matched_skills or [],
        missing_skills=result.missing_skills or [],
        explanation=explanation_text,
    )
