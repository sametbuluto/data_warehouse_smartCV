"""
For every job that lacks an 80+ scoring candidate, create one 'champion' (expert-level)
candidate whose skills fully cover the role's requirements, plus a 'near-miss' candidate
who covers ~70-80% of skills to keep rankings realistic.

Run from: /Users/samet/Desktop/datawarehouse/backend/
  source venv/bin/activate && python seed_champions.py
"""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")

import requests
import random

from app.database import init_db, SessionLocal, Candidate, Skill, JobPosting

init_db()

BASE = "http://localhost:8000"

# ── Role-aware name pool (avoids duplicate names in DB) ──────────────────────
NAME_POOL = [
    # Finance
    ("Lucie Moreau", "lucie.moreau@cv.com", "Master"),
    ("Andrei Popescu", "andrei.popescu@cv.com", "Bachelor"),
    ("Nkechi Obi", "nkechi.obi@cv.com", "Master"),
    ("Florian Roth", "florian.roth@cv.com", "Bachelor"),
    ("Giulia Mancini", "giulia.mancini@cv.com", "Master"),
    # Tech
    ("Takeshi Ono", "takeshi.ono@cv.com", "Bachelor"),
    ("Emilia Nowak", "emilia.nowak@cv.com", "Bachelor"),
    ("Remy Laurent", "remy.laurent@cv.com", "Bachelor"),
    ("Arjun Mehta", "arjun.mehta@cv.com", "Master"),
    ("Siobhan Murphy", "siobhan.murphy@cv.com", "Bachelor"),
    ("Kwasi Boateng", "kwasi.boateng@cv.com", "Bachelor"),
    ("Miroslav Novak", "miroslav.novak@cv.com", "Master"),
    ("Ingeborg Hansen", "ingeborg.hansen@cv.com", "Bachelor"),
    ("Tariq Al-Farsi", "tariq.alfarsi@cv.com", "Bachelor"),
    ("Yuna Park", "yuna.park@cv.com", "Master"),
    ("Olumide Adeyemi", "olumide.adeyemi@cv.com", "Bachelor"),
    ("Anastasia Volkov", "anastasia.volkov@cv.com", "Master"),
    ("Cedric Fontaine", "cedric.fontaine@cv.com", "Bachelor"),
    ("Mei Chen", "mei.chen@cv.com", "Master"),
    ("Reza Ahmadi", "reza.ahmadi@cv.com", "Bachelor"),
    # Domain
    ("Beatrix Varga", "beatrix.varga@cv.com", "Bachelor"),
    ("Kweku Mensah", "kweku.mensah@cv.com", "Bachelor"),
    ("Fatou Camara", "fatou.camara@cv.com", "Master"),
    ("Luciano Ricci", "luciano.ricci@cv.com", "Bachelor"),
    ("Zoe Papadaki", "zoe.papadaki@cv.com", "Bachelor"),
    ("Hamid Karimi", "hamid.karimi@cv.com", "Bachelor"),
    ("Astrid Larsen", "astrid.larsen@cv.com", "Master"),
    ("Chidi Okafor", "chidi.okafor@cv.com", "Bachelor"),
    ("Mireille Dubois", "mireille.dubois@cv.com", "Master"),
    ("Sebastián Torres", "sebastian.torres@cv.com", "Bachelor"),
    ("Pham Thi Lan", "pham.lan@cv.com", "Bachelor"),
    ("Dario Esposito", "dario.esposito@cv.com", "Bachelor"),
    ("Fiona O'Sullivan", "fiona.osullivan@cv.com", "Master"),
    ("Goran Petrović", "goran.petrovic@cv.com", "Bachelor"),
    ("Nadia Aziz", "nadia.aziz@cv.com", "Bachelor"),
    ("Tobias Keller", "tobias.keller@cv.com", "Master"),
    ("Amandine Leclerc", "amandine.leclerc@cv.com", "Bachelor"),
    ("Farida Yusupova", "farida.yusupova@cv.com", "Bachelor"),
    ("Willem de Bruin", "willem.debruin@cv.com", "Bachelor"),
    ("Soraya Khalil", "soraya.khalil@cv.com", "Master"),
    ("Nils Bergström", "nils.bergstrom@cv.com", "Bachelor"),
    ("Chiamaka Eze", "chiamaka.eze@cv.com", "Bachelor"),
    ("Vladislav Petrov", "vladislav.petrov@cv.com", "Bachelor"),
    ("Céleste Dupont", "celeste.dupont@cv.com", "Master"),
    ("Rohan Sharma", "rohan.sharma@cv.com", "Bachelor"),
    ("Linh Nguyen", "linh.nguyen@cv.com", "Bachelor"),
    ("Kasimir Wolf", "kasimir.wolf@cv.com", "Bachelor"),
    ("Yewande Adegoke", "yewande.adegoke@cv.com", "Bachelor"),
    ("Maxime Bertrand", "maxime.bertrand@cv.com", "Bachelor"),
    ("Irina Sokolova", "irina.sokolova@cv.com", "Master"),
    # Extended pool — round 2
    ("Dmitri Kozlov", "dmitri.kozlov@cv.com", "Master"),
    ("Amara Diallo", "amara.diallo@cv.com", "Bachelor"),
    ("Henrik Johansson", "henrik.johansson@cv.com", "Master"),
    ("Priya Krishnan", "priya.krishnan@cv.com", "Bachelor"),
    ("Tomasz Wiśniewski", "tomasz.wisniewski@cv.com", "Master"),
    ("Olusegun Bello", "olusegun.bello@cv.com", "Bachelor"),
    ("Valentina Romano", "valentina.romano@cv.com", "Master"),
    ("Jae-Won Kim", "jaewon.kim@cv.com", "Bachelor"),
    ("Mariana Ferreira", "mariana.ferreira@cv.com", "Master"),
    ("Alexei Morozov", "alexei.morozov@cv.com", "Bachelor"),
    ("Chioma Agu", "chioma.agu@cv.com", "Master"),
    ("Sven Lindqvist", "sven.lindqvist@cv.com", "Bachelor"),
    ("Dilnoza Yusupova", "dilnoza.yusupova@cv.com", "Bachelor"),
    ("Marco Pellegrini", "marco.pellegrini@cv.com", "Master"),
    ("Adaeze Nwosu", "adaeze.nwosu@cv.com", "Bachelor"),
    ("Bogdan Ionescu", "bogdan.ionescu@cv.com", "Master"),
    ("Ximena Castillo", "ximena.castillo@cv.com", "Bachelor"),
    ("Yuki Tanaka", "yuki.tanaka@cv.com", "Master"),
    ("Kofi Asante", "kofi.asante@cv.com", "Bachelor"),
    ("Lara Hoffmann", "lara.hoffmann@cv.com", "Master"),
    ("Babatunde Ogunleye", "babatunde.ogunleye@cv.com", "Bachelor"),
    ("Svetlana Ivanova", "svetlana.ivanova@cv.com", "Master"),
    ("Cédric Beaumont", "cedric.beaumont@cv.com", "Bachelor"),
    ("Ngozi Adichie", "ngozi.adichie@cv.com", "Master"),
    ("Rasmus Holm", "rasmus.holm@cv.com", "Bachelor"),
    ("Faisal Al-Rashid", "faisal.alrashid@cv.com", "Master"),
    ("Ekaterina Smirnova", "ekaterina.smirnova@cv.com", "Bachelor"),
    ("Javier Mendoza", "javier.mendoza@cv.com", "Master"),
    ("Abena Mensah", "abena.mensah@cv.com", "Bachelor"),
    ("Oskar Lindgren", "oskar.lindgren@cv.com", "Master"),
    ("Deepa Nair", "deepa.nair@cv.com", "Bachelor"),
    ("Erkan Yıldız", "erkan.yildiz@cv.com", "Master"),
    ("Nathalie Bouchard", "nathalie.bouchard@cv.com", "Bachelor"),
    ("Seun Adesanya", "seun.adesanya@cv.com", "Master"),
    ("Pavel Horák", "pavel.horak@cv.com", "Bachelor"),
    ("Laila Hassan", "laila.hassan@cv.com", "Master"),
    ("Tristan Moreau", "tristan.moreau@cv.com", "Bachelor"),
    ("Aiko Watanabe", "aiko.watanabe@cv.com", "Master"),
    ("Emeka Okonkwo", "emeka.okonkwo@cv.com", "Bachelor"),
    ("Sigrid Andersen", "sigrid.andersen@cv.com", "Master"),
    ("Rafael Carvalho", "rafael.carvalho@cv.com", "Bachelor"),
    ("Miriam Goldberg", "miriam.goldberg@cv.com", "Master"),
    ("Tunde Adewale", "tunde.adewale@cv.com", "Bachelor"),
    ("Zuzanna Kowalczyk", "zuzanna.kowalczyk@cv.com", "Master"),
    ("Nicolás Vargas", "nicolas.vargas@cv.com", "Bachelor"),
    ("Amina Traoré", "amina.traore@cv.com", "Master"),
    ("Benedikt Müller", "benedikt.muller@cv.com", "Bachelor"),
    ("Ye-Jin Cho", "yejin.cho@cv.com", "Master"),
    ("Oluwafemi Adeyinka", "oluwafemi.adeyinka@cv.com", "Bachelor"),
    ("Francisca Gomes", "francisca.gomes@cv.com", "Master"),
]

# Extra skills that complement each category (added to champion to boost semantic)
CATEGORY_CONTEXT = {
    "tech": ["software engineering","agile","code review","system design","rest api","ci/cd"],
    "finance": ["financial reporting","stakeholder reporting","excel","powerpoint","presentation"],
    "sales": ["account management","pipeline management","client relationship management","crm"],
    "hr": ["talent management","stakeholder management","onboarding","hris"],
    "supply": ["supply chain management","vendor management","excel","sap","data analysis"],
    "engineering": ["project management","quality management","autocad","technical drawing"],
    "healthcare": ["gcp","regulatory compliance","data analysis","medical writing"],
    "marketing": ["google analytics","content strategy","a/b testing","data analysis"],
    "legal": ["legal research","legal writing","compliance","due diligence"],
}

# Near-miss extra skill sets per category (drop 2 random required + add tangential)
NEAR_MISS_EXTRAS = {
    "tech": ["agile","unit testing","code review"],
    "finance": ["excel","powerpoint","microsoft office"],
    "sales": ["communication","customer service","microsoft office"],
    "hr": ["microsoft office","communication","administration"],
    "supply": ["excel","data analysis","microsoft office"],
    "engineering": ["technical drawing","project management","autocad"],
    "healthcare": ["data analysis","microsoft office","communication"],
    "marketing": ["canva","content creation","copywriting"],
    "legal": ["microsoft office","communication","administration"],
}


def category_of(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ["financial","risk","banking","treasury","aml","equity","investment","compliance officer"]):
        return "finance"
    if any(k in t for k in ["sales","business dev","customer success"]):
        return "sales"
    if any(k in t for k in ["hr","talent","learning","compensation","training","instructional"]):
        return "hr"
    if any(k in t for k in ["supply","procurement","logistics"]):
        return "supply"
    if any(k in t for k in ["mechanical","civil","electrical","manufacturing","engineer"]):
        return "engineering"
    if any(k in t for k in ["clinical","healthcare","hospital","pharma"]):
        return "healthcare"
    if any(k in t for k in ["marketing","seo","brand","crm & market"]):
        return "marketing"
    if any(k in t for k in ["legal","lawyer","gdpr","privacy","ip &"]):
        return "legal"
    return "tech"


def make_raw_text(name: str, title: str, skills: list, exp: float, edu: str) -> str:
    skill_str = ", ".join(s.title() for s in skills[:8])
    return (
        f"{name} | {edu} | {exp:.0f} years | {title} professional. "
        f"Core competencies: {skill_str}. "
        f"Experienced in {skills[0] if skills else 'the field'} and {skills[1] if len(skills)>1 else 'related tools'}. "
        f"Proven track record in {title.lower()} roles."
    )


def seed():
    db = SessionLocal()
    existing_emails = {row[0] for row in db.query(Candidate.email).all()}
    available_names = [entry for entry in NAME_POOL if entry[1] not in existing_emails]
    name_iter = iter(available_names)
    added_total = 0

    try:
        jobs = requests.get(f"{BASE}/api/jobs").json()
        print(f"Checking {len(jobs)} jobs...\n")

        for job in jobs:
            jid = job["id"]
            title = job["title"]
            req_skills = [s.lower() for s in job["required_skills"]]
            min_exp = job["min_experience"]
            edu_req = job["education_level"]

            # Check current top score
            try:
                r = requests.post(f"{BASE}/api/match/{jid}")
                results = r.json().get("results", [])
                top_score = results[0]["final_score"] if results else 0
            except Exception:
                top_score = 0

            if top_score >= 80:
                print(f"  ✓  {top_score:5.1f}  {title}")
                continue

            cat = category_of(title)
            ctx_skills = CATEGORY_CONTEXT.get(cat, [])

            # ── Champion: all required + some context skills ──────────────────
            try:
                champ_name, champ_email, champ_edu = next(name_iter)
            except StopIteration:
                print("  ⚠ Ran out of names — increase NAME_POOL")
                break

            # education: use job requirement unless candidate's is higher
            edu_map = {"high school": 1, "associate": 2, "bachelor": 3, "master": 4, "phd": 5, "mba": 4}
            req_edu_rank = edu_map.get(edu_req.lower(), 3)
            champ_edu_rank = edu_map.get(champ_edu.lower(), 3)
            final_edu = champ_edu if champ_edu_rank >= req_edu_rank else edu_req.capitalize()

            champ_exp = max(min_exp * 1.4, min_exp + 1.5)
            champ_skills = list(req_skills)
            # add a few context skills (not duplicating req)
            for s in ctx_skills:
                if s not in champ_skills and len(champ_skills) < len(req_skills) + 4:
                    champ_skills.append(s)

            if not db.query(Candidate).filter(Candidate.email == champ_email).first():
                c = Candidate(
                    name=champ_name, email=champ_email,
                    education=final_edu, experience_years=champ_exp,
                    raw_text=make_raw_text(champ_name, title, champ_skills, champ_exp, final_edu),
                )
                db.add(c); db.flush()
                for sk in champ_skills:
                    db.add(Skill(candidate_id=c.id, skill_name=sk))
                added_total += 1

            # ── Near-miss: drop 2 required skills, add tangential ─────────────
            try:
                nm_name, nm_email, nm_edu = next(name_iter)
            except StopIteration:
                db.commit()
                break

            nm_exp = max(min_exp * 0.85, min_exp - 0.5)
            nm_skills = list(req_skills)
            # drop up to 2 required skills
            drop_count = min(2, len(nm_skills) - 2)
            if drop_count > 0:
                for _ in range(drop_count):
                    nm_skills.pop(random.randrange(len(nm_skills)))
            # add near-miss extras
            for s in NEAR_MISS_EXTRAS.get(cat, []):
                if s not in nm_skills:
                    nm_skills.append(s)

            if not db.query(Candidate).filter(Candidate.email == nm_email).first():
                nm_edu_rank = edu_map.get(nm_edu.lower(), 3)
                nm_final_edu = nm_edu if nm_edu_rank >= req_edu_rank else edu_req.capitalize()
                c = Candidate(
                    name=nm_name, email=nm_email,
                    education=nm_final_edu, experience_years=nm_exp,
                    raw_text=make_raw_text(nm_name, title, nm_skills, nm_exp, nm_final_edu),
                )
                db.add(c); db.flush()
                for sk in nm_skills:
                    db.add(Skill(candidate_id=c.id, skill_name=sk))
                added_total += 1

            db.commit()
            print(f"  + champion+near-miss added for [{jid:3d}] {title}  (was {top_score:.1f})")

        db.commit()
        print(f"\nDone — {added_total} candidates added.")
        print(f"Total candidates now: {db.query(Candidate).count()}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
