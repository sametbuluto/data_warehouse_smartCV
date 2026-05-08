# SmartCV — AI Candidate Matching Platform

AI-powered recruitment platform using NLP and ML for resume analysis and candidate matching.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite, spaCy, scikit-learn
- **Frontend:** React, Vite, TailwindCSS, Recharts, Framer Motion
- **ML Pipeline:** TF-IDF + Cosine Similarity, Weighted Scoring

## Quick Start

### Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python seed_data.py
python -m uvicorn app.main:app --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Scoring Formula
```
Final = 40% Skill Match + 30% Experience + 20% Education + 10% Semantic Similarity
```

## Dataset
- 100 synthetic resumes (9 categories)
- 20 job postings (diverse tech roles)
