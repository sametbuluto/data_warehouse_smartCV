"""Seed diverse candidates with varying skill coverage to create realistic score spreads."""
import sys, os
os.chdir(os.path.dirname(__file__))
sys.path.insert(0, ".")

from app.database import init_db, SessionLocal, Candidate, Skill

init_db()

# Diverse candidates spanning weak → strong for several key job categories
DIVERSE_CANDIDATES = [
    # ── DATA SCIENCE (strong) ─────────────────────────────────────────────────
    {
        "name": "Mei Lin", "email": "mei.lin@email.com", "education": "PhD",
        "experience_years": 6.0,
        "skills": ["machine learning", "python", "r", "data analysis", "numpy", "pandas",
                   "matplotlib", "statistics", "deep learning", "sql", "spark", "tensorflow"],
        "raw_text": "Mei Lin | PhD Data Science | 6 years | Deep learning, NLP, time-series forecasting. "
                    "Built ML pipelines at scale. Python, R, TensorFlow, Spark, SQL. "
                    "Senior ML Engineer at TechCorp. Publications in NeurIPS."
    },
    # ── DATA SCIENCE (partial) ────────────────────────────────────────────────
    {
        "name": "Jake Owens", "email": "jake.owens@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["python", "data analysis", "sql", "excel"],
        "raw_text": "Jake Owens | BSc Computer Science | 2 years | Junior data analyst. "
                    "SQL queries, Excel dashboards, basic Python scripting. "
                    "No formal ML experience yet."
    },
    # ── DATA SCIENCE (weak) ───────────────────────────────────────────────────
    {
        "name": "Sam Bridges", "email": "sam.bridges@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["excel", "powerpoint", "data entry"],
        "raw_text": "Sam Bridges | BA Business | 1 year | Administrative analyst. "
                    "Excel reports, PowerPoint presentations. No programming experience."
    },
    # ── SALES & BD (strong) ───────────────────────────────────────────────────
    {
        "name": "Elena Vasquez", "email": "elena.vasquez@email.com", "education": "Bachelor",
        "experience_years": 7.0,
        "skills": ["b2b sales", "enterprise sales", "salesforce", "crm", "negotiation",
                   "pipeline management", "market research", "business development",
                   "stakeholder management", "sales forecasting"],
        "raw_text": "Elena Vasquez | 7 years enterprise sales | Closed $40M ARR. "
                    "Salesforce CRM power user. B2B SaaS sales to C-suite. "
                    "Territory management, pipeline optimization, team leadership."
    },
    # ── SALES & BD (moderate) ─────────────────────────────────────────────────
    {
        "name": "Ryan Park", "email": "ryan.park@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["b2b sales", "crm", "negotiation", "salesforce"],
        "raw_text": "Ryan Park | 3 years sales | Mid-market account executive. "
                    "HubSpot and Salesforce. $2M annual quota. Negotiation training completed."
    },
    # ── SALES & BD (weak) ────────────────────────────────────────────────────
    {
        "name": "Tom Hadley", "email": "tom.hadley@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["communication", "customer service"],
        "raw_text": "Tom Hadley | 1 year retail sales | Customer service at a retail store. "
                    "No B2B or CRM experience."
    },
    # ── ENGINEERING (strong) ──────────────────────────────────────────────────
    {
        "name": "Lars Eriksson", "email": "lars.eriksson@email.com", "education": "Master",
        "experience_years": 8.0,
        "skills": ["solidworks", "catia", "ansys", "finite element analysis", "mechanical design",
                   "autocad", "lean manufacturing", "fmea", "quality management", "gd&t"],
        "raw_text": "Lars Eriksson | MSc Mechanical Engineering | 8 years | "
                    "Senior mechanical design engineer. SolidWorks, CATIA, ANSYS FEA. "
                    "GD&T tolerancing, DFM reviews, FMEA leadership. ISO 9001 certified."
    },
    # ── ENGINEERING (moderate) ────────────────────────────────────────────────
    {
        "name": "Priya Nair", "email": "priya.nair@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["solidworks", "autocad", "mechanical design", "quality management"],
        "raw_text": "Priya Nair | BE Mechanical | 3 years | Design engineer. "
                    "SolidWorks 3D modeling, AutoCAD drawings, basic FEA. "
                    "No CATIA or ANSYS experience."
    },
    # ── ENGINEERING (weak) ────────────────────────────────────────────────────
    {
        "name": "Greg Mason", "email": "greg.mason@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["autocad", "technical drawing"],
        "raw_text": "Greg Mason | BSc Mechanical | 1 year | Drafting technician. "
                    "AutoCAD 2D drawings only. No FEA, no 3D modeling."
    },
    # ── HR & TRAINING (strong) ────────────────────────────────────────────────
    {
        "name": "Carmen Reyes", "email": "carmen.reyes@email.com", "education": "Master",
        "experience_years": 9.0,
        "skills": ["talent acquisition", "performance management", "employee relations",
                   "change management", "hr analytics", "workday", "employment law",
                   "organizational development", "hris", "recruitment"],
        "raw_text": "Carmen Reyes | MSc HRM | 9 years | HR Business Partner at Fortune 500. "
                    "Full-cycle talent acquisition, Workday HRIS, OD projects, "
                    "employment law compliance across 5 countries."
    },
    # ── HR & TRAINING (moderate) ──────────────────────────────────────────────
    {
        "name": "Ben Foster", "email": "ben.foster@email.com", "education": "Bachelor",
        "experience_years": 4.0,
        "skills": ["recruitment", "talent acquisition", "hris", "onboarding"],
        "raw_text": "Ben Foster | BA Psychology | 4 years | Talent acquisition specialist. "
                    "Full-cycle recruiting for tech roles. ATS management. "
                    "No strategic HR or analytics experience."
    },
    # ── SUPPLY CHAIN (strong) ─────────────────────────────────────────────────
    {
        "name": "Fatou Diallo", "email": "fatou.diallo@email.com", "education": "Master",
        "experience_years": 6.0,
        "skills": ["supply chain management", "procurement", "vendor management",
                   "category management", "contract negotiation", "sap", "rfq",
                   "strategic sourcing", "inventory management", "s&op", "demand planning"],
        "raw_text": "Fatou Diallo | MSc Supply Chain | 6 years | Procurement & sourcing manager. "
                    "Strategic category management, SAP MM/SRM, supplier negotiations, "
                    "S&OP process design. $30M spend under management."
    },
    # ── SUPPLY CHAIN (partial) ────────────────────────────────────────────────
    {
        "name": "Kevin Huang", "email": "kevin.huang@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["supply chain management", "excel", "inventory management"],
        "raw_text": "Kevin Huang | BSc Logistics | 2 years | Supply chain coordinator. "
                    "Inventory tracking in Excel, basic SAP data entry. "
                    "No strategic sourcing or contract negotiation."
    },
    # ── FINANCE (strong) ─────────────────────────────────────────────────────
    {
        "name": "Nadia Petrov", "email": "nadia.petrov@email.com", "education": "Master",
        "experience_years": 5.0,
        "skills": ["financial modeling", "financial analysis", "excel", "sql",
                   "budgeting", "forecasting", "gaap", "bloomberg", "valuation", "dcf"],
        "raw_text": "Nadia Petrov | MSc Finance CFA L3 | 5 years | Senior financial analyst. "
                    "DCF and LBO models, Bloomberg Terminal, GAAP reporting, "
                    "FP&A budgeting for $200M revenue unit."
    },
    # ── FINANCE (moderate) ────────────────────────────────────────────────────
    {
        "name": "Cian Murphy", "email": "cian.murphy@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["financial analysis", "excel", "budgeting", "gaap"],
        "raw_text": "Cian Murphy | BCom Finance | 2 years | Junior financial analyst. "
                    "Variance analysis, budget tracking, Excel models. "
                    "No Bloomberg or advanced modeling."
    },
    # ── FINANCE (weak / career changer) ──────────────────────────────────────
    {
        "name": "Lena Bauer", "email": "lena.bauer@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["excel", "accounting basics"],
        "raw_text": "Lena Bauer | BA Economics | 1 year | Administrative assistant. "
                    "Basic bookkeeping, Excel spreadsheets. "
                    "Career-changing into finance."
    },
    # ── DIGITAL MARKETING (strong) ────────────────────────────────────────────
    {
        "name": "Alex Torres", "email": "alex.torres@email.com", "education": "Bachelor",
        "experience_years": 5.0,
        "skills": ["digital marketing", "seo", "sem", "google ads", "meta ads",
                   "google analytics", "ga4", "hubspot", "email marketing",
                   "a/b testing", "content marketing", "crm"],
        "raw_text": "Alex Torres | BA Marketing | 5 years | Digital marketing manager. "
                    "Managed $3M paid media budget. SEO organic growth 200%. "
                    "HubSpot certified. GA4 migration lead."
    },
    # ── DIGITAL MARKETING (partial) ───────────────────────────────────────────
    {
        "name": "Jess Kim", "email": "jess.kim@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["social media marketing", "canva", "content marketing", "google analytics"],
        "raw_text": "Jess Kim | BA Communications | 2 years | Social media coordinator. "
                    "Instagram and LinkedIn content. Canva designs. "
                    "No paid search or SEO experience."
    },
]


def seed():
    db = SessionLocal()
    try:
        added = 0
        for c in DIVERSE_CANDIDATES:
            existing = db.query(Candidate).filter(Candidate.email == c["email"]).first()
            if existing:
                print(f"  Skip (exists): {c['name']}")
                continue

            cand = Candidate(
                name=c["name"],
                email=c["email"],
                education=c["education"],
                experience_years=c["experience_years"],
                raw_text=c["raw_text"],
            )
            db.add(cand)
            db.flush()

            for skill_name in c["skills"]:
                db.add(Skill(candidate_id=cand.id, skill_name=skill_name))

            added += 1
            print(f"  Added: {c['name']} ({len(c['skills'])} skills, {c['experience_years']} yrs)")

        db.commit()
        print(f"\nDone — {added} new diverse candidates added.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
