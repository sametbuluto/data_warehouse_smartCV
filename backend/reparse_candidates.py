"""Re-parse all stored candidates using the latest NLP extraction rules."""

from app.database import SessionLocal, Candidate, Skill
from app.services.nlp_processor import parse_resume


def main():
    db = SessionLocal()
    try:
        candidates = db.query(Candidate).all()
        updated = 0

        for candidate in candidates:
            if not candidate.raw_text:
                continue

            parsed = parse_resume(candidate.raw_text)
            candidate.name = parsed["name"]
            candidate.email = parsed["email"]
            candidate.phone = parsed["phone"]
            candidate.education = parsed["education"]
            candidate.experience_years = parsed["experience_years"]

            db.query(Skill).filter(Skill.candidate_id == candidate.id).delete()
            for skill_name in parsed["skills"]:
                db.add(Skill(candidate_id=candidate.id, skill_name=skill_name))

            updated += 1

        db.commit()
        print(f"Re-parsed {updated} candidates successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
