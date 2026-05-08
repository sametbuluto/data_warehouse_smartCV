"""Job Posting API routes — create, list, get, delete jobs."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, JobPosting
from app.schemas.models import JobCreate, JobResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job posting."""
    db_job = JobPosting(
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        min_experience=job.min_experience,
        education_level=job.education_level,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    logger.info(f"Job created: {db_job.title} (ID: {db_job.id})")
    return db_job


@router.get("", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    """Get all job postings."""
    return db.query(JobPosting).order_by(JobPosting.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job posting."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job posting and its match results."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    db.delete(job)
    db.commit()
    return {"message": f"Job {job_id} deleted."}
