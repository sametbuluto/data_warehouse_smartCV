"""Seed the database with sample jobs and resumes for demo."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import init_db, SessionLocal, JobPosting, Candidate, Skill

DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")

def seed():
    init_db()
    db = SessionLocal()
    try:
        if db.query(Candidate).count() > 0:
            print("DB already seeded. Skipping.")
            return

        # Seed jobs
        with open(os.path.join(DATA_DIR, "jobs.json")) as f:
            jobs = json.load(f)
        for j in jobs:
            db.add(JobPosting(**j))
        db.commit()
        print(f"✅ Seeded {len(jobs)} job postings")

        # Seed resumes
        with open(os.path.join(DATA_DIR, "resumes.json")) as f:
            resumes = json.load(f)
        for r in resumes:
            c = Candidate(
                name=r["name"], email=r["email"], phone=r["phone"],
                education=r["education"], experience_years=r["experience_years"],
                raw_text=r["raw_text"], file_path=None,
            )
            db.add(c)
            db.flush()
            for skill in r["skills"]:
                db.add(Skill(candidate_id=c.id, skill_name=skill))
        db.commit()
        print(f"✅ Seeded {len(resumes)} candidates")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
