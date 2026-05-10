"""
Remove the 97 generic all-tech candidates from resumes.json,
then add a balanced pool across Finance, Sales, HR, Supply Chain,
Engineering, Healthcare, Marketing, Legal, and Tech.

Safe to run multiple times — skips if email already exists.
"""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")

from app.database import init_db, SessionLocal, Candidate, Skill, MatchResult

init_db()

# ── Names to REMOVE (generic all-tech crowd from original resumes.json) ──────
REMOVE_NAMES = {
    "David Anderson","Abigail Scott","Sadie Garcia","Jack Chen","Genesis Hill",
    "James King","Benjamin Williams","Lily Thompson","Adrian Lopez","William Nelson",
    "Charlotte Garcia","Eva Park","Robert Clark","Audrey Flores","Harper Mitchell",
    "Genesis Hernandez","Audrey Sanchez","Riley Torres","Aria Patel","Daniel Thompson",
    "Skylar Anderson","Jacob Kim","Jack Ramirez","Gabriel Sullivan","Sebastian Clark",
    "Cameron Young","Dylan Garcia","Noah Jackson","Hannah Flores","James Cox",
    "Naomi Garcia","Hannah Jackson","Christian Young","David Kim","Emily Murphy",
    "Claire Singh","Naomi Carter","Samantha Cox","Sebastian Cox","Eleanor Harris",
    "Aria Ward","Caleb Baker","William Cohen","Lincoln Garcia","Lucas Johnson",
    "Sophia Brooks","Christian Williams","Henry Chen","Adrian Flores","Ryan Sullivan",
    "Noah Flores","Skylar Thomas","David Hernandez","Joshua Rivera","Abigail Torres",
    "Julian Lewis","Thomas Hernandez","Benjamin White","Claire Gonzalez","Avery Garcia",
    "Matthew Torres","Evelyn Lee","Riley White","Ava Clark","Christopher Kim",
    "Hailey Kumar","Chloe Patel","Avery Nguyen","Naomi Lewis","Aaron Nelson",
    "Ava Garcia","Nora Flores","Bella Baker","Amelia Nguyen","Emma Smith",
    "Caleb Johnson","Brooklyn Johnson","Cameron Nelson","Aaron Carter","Genesis Baker",
    "Andrew Kim","Samantha Rodriguez","Natalie Allen","Charles Adams","Liam Carter",
    "Jack Taylor","David Campbell","Paisley King","Grace Moore","Alexander Smith",
    "Evelyn Hill","Logan Torres","Jayden Johnson","Sadie Martin","Emma Carter",
    "Sadie Kumar","Isaac Reed","Chloe Nelson","Eva Perez","Benjamin Jackson",
}

# ── Balanced candidate pool ────────────────────────────────────────────────────

BALANCED_CANDIDATES = [

    # ════════════════════════════════════════════════════════
    # FINANCE  (Financial Analyst, Risk, IB, Treasury, AML, Equity Research)
    # ════════════════════════════════════════════════════════
    {"name":"Léa Martin","email":"lea.martin@cv.com","education":"Master",
     "experience_years":5.0,
     "skills":["financial modeling","financial analysis","excel","bloomberg","valuation","dcf","equity research","gaap","sql","powerpoint"],
     "raw_text":"Léa Martin | MSc Finance CFA | 5y | Equity research analyst at BNP Paribas. DCF/LBO models, Bloomberg Terminal, sector coverage reports."},
    {"name":"Nico Bauer","email":"nico.bauer@cv.com","education":"Bachelor",
     "experience_years":2.0,
     "skills":["financial analysis","excel","budgeting","forecasting","gaap","financial reporting","variance analysis"],
     "raw_text":"Nico Bauer | BCom Finance | 2y | FP&A analyst. Excel models, budget variance, GAAP reporting."},
    {"name":"Preethi Nair","email":"preethi.nair@cv.com","education":"Bachelor",
     "experience_years":0.5,
     "skills":["excel","accounting basics","financial reporting","microsoft office"],
     "raw_text":"Preethi Nair | Finance graduate | 6m internship | Excel bookkeeping, basic financial reports."},
    {"name":"Jonas Klein","email":"jonas.klein@cv.com","education":"Master",
     "experience_years":8.0,
     "skills":["risk management","credit risk","market risk","var","stress testing","regulatory reporting","python","r","basel iii","frm","financial modeling","sql"],
     "raw_text":"Jonas Klein | MSc Quant Finance FRM | 8y | Head of Market Risk at Deutsche Bank. VaR models, Basel III, Python/R risk engines."},
    {"name":"Amara Osei","email":"amara.osei@cv.com","education":"Bachelor",
     "experience_years":4.0,
     "skills":["aml","kyc","compliance","regulatory compliance","risk management","financial analysis","excel"],
     "raw_text":"Amara Osei | BCom | 4y | AML compliance officer. Transaction monitoring, SAR filing, KYC onboarding."},
    {"name":"Chiara Russo","email":"chiara.russo@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["treasury management","cash management","fx hedging","sap","financial modeling","excel","forecasting"],
     "raw_text":"Chiara Russo | 3y | Treasury analyst. FX hedging, SAP Treasury, cash positioning."},
    {"name":"Damien Leclerc","email":"damien.leclerc@cv.com","education":"Bachelor",
     "experience_years":1.0,
     "skills":["financial modeling","valuation","dcf","excel","powerpoint","financial analysis"],
     "raw_text":"Damien Leclerc | IB internship | 1y | M&A pitch books, DCF models, comparable company analysis."},
    {"name":"Hana Patel","email":"hana.patel@cv.com","education":"Bachelor",
     "experience_years":2.0,
     "skills":["equity research","financial modeling","excel","bloomberg","investment analysis","financial reporting"],
     "raw_text":"Hana Patel | 2y | Junior equity research analyst. Bloomberg, earnings models, investment notes."},
    {"name":"Sven Lindqvist","email":"sven.lindqvist@cv.com","education":"Master",
     "experience_years":6.0,
     "skills":["financial modeling","valuation","dcf","lbo","merger & acquisition","excel","bloomberg","financial analysis","powerpoint"],
     "raw_text":"Sven Lindqvist | MSc Finance | 6y | VP M&A at KPMG. LBO/DCF modeling, deal execution, due diligence."},
    {"name":"Mia Hoffmann","email":"mia.hoffmann@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["excel","accounting basics","microsoft office","gaap"],
     "raw_text":"Mia Hoffmann | Finance BSc | 0y | Entry-level, strong academics, Excel, basic GAAP knowledge."},

    # ════════════════════════════════════════════════════════
    # SALES & BUSINESS DEVELOPMENT
    # ════════════════════════════════════════════════════════
    {"name":"Connor Walsh","email":"connor.walsh@cv.com","education":"Bachelor",
     "experience_years":7.0,
     "skills":["b2b sales","enterprise sales","sales management","salesforce","pipeline management","negotiation","sales forecasting","crm","stakeholder management"],
     "raw_text":"Connor Walsh | 7y | Enterprise Sales Director. $25M ARR closed. Salesforce, C-suite relationships, team of 8 AEs."},
    {"name":"Ifeoma Eze","email":"ifeoma.eze@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["b2b sales","crm","salesforce","negotiation","market research","business development","stakeholder management"],
     "raw_text":"Ifeoma Eze | 3y | Account executive, B2B SaaS. Salesforce, outbound prospecting, $1.2M quota."},
    {"name":"Matteo Greco","email":"matteo.greco@cv.com","education":"Bachelor",
     "experience_years":1.0,
     "skills":["b2b sales","crm","negotiation","customer service","communication"],
     "raw_text":"Matteo Greco | 1y | SDR at tech company. Outbound calls, CRM hygiene, pipeline qualification."},
    {"name":"Zara Phillips","email":"zara.phillips@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["customer service","communication","microsoft office","negotiation"],
     "raw_text":"Zara Phillips | 0y | Seeking entry sales role. Retail customer service background, strong communication."},
    {"name":"Bruno Fernandes","email":"bruno.fernandes@cv.com","education":"Bachelor",
     "experience_years":5.0,
     "skills":["customer success","account management","salesforce","crm","upselling","stakeholder management","client relationship management"],
     "raw_text":"Bruno Fernandes | 5y | Senior CSM. 120% NRR, QBRs, Salesforce, 40-account portfolio."},
    {"name":"Leila Abbasi","email":"leila.abbasi@cv.com","education":"Bachelor",
     "experience_years":2.0,
     "skills":["customer success","salesforce","crm","account management","client relationship management"],
     "raw_text":"Leila Abbasi | 2y | Customer Success Associate. Onboarding, renewal management, Salesforce."},
    {"name":"Patrick O'Brien","email":"patrick.obrien@cv.com","education":"Bachelor",
     "experience_years":9.0,
     "skills":["business development","b2b sales","market research","negotiation","crm","strategic planning","stakeholder management","salesforce","enterprise sales","pipeline management"],
     "raw_text":"Patrick O'Brien | 9y | VP Business Development. Partnership deals, go-to-market strategy, $50M pipeline."},

    # ════════════════════════════════════════════════════════
    # HR & PEOPLE
    # ════════════════════════════════════════════════════════
    {"name":"Nina Kowalczyk","email":"nina.kowalczyk@cv.com","education":"Master",
     "experience_years":8.0,
     "skills":["talent acquisition","performance management","employee relations","change management","hr analytics","workday","employment law","organizational development","hris","recruitment"],
     "raw_text":"Nina Kowalczyk | MSc HRM | 8y | Senior HRBP at Unilever. OD projects, Workday, employment law, 5-country scope."},
    {"name":"Kwame Asante","email":"kwame.asante@cv.com","education":"Bachelor",
     "experience_years":4.0,
     "skills":["talent acquisition","recruitment","linkedin recruiter","sourcing","hris","hr analytics","onboarding","stakeholder management"],
     "raw_text":"Kwame Asante | 4y | Talent Acquisition Manager. Senior tech recruiting, LinkedIn Recruiter, ATS."},
    {"name":"Sofie Berg","email":"sofie.berg@cv.com","education":"Bachelor",
     "experience_years":2.0,
     "skills":["recruitment","talent acquisition","hris","onboarding","sourcing"],
     "raw_text":"Sofie Berg | 2y | Recruiter. Full-cycle recruiting, job board management, candidate screening."},
    {"name":"Omar Diallo","email":"omar.diallo@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["communication","microsoft office","hr basics","administration"],
     "raw_text":"Omar Diallo | 0y | HR graduate. Seeking entry HR role. University HR club leadership."},
    {"name":"Valentina Cruz","email":"valentina.cruz@cv.com","education":"Master",
     "experience_years":5.0,
     "skills":["learning & development","instructional design","e-learning","articulate storyline","lms","moodle","training delivery","content creation","facilitation"],
     "raw_text":"Valentina Cruz | MSc Education | 5y | L&D Specialist. ADDIE methodology, Articulate Storyline, Moodle LMS."},
    {"name":"Felix Wagner","email":"felix.wagner@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["compensation & benefits","hr analytics","excel","financial modeling","workday","hris"],
     "raw_text":"Felix Wagner | 3y | Compensation & Benefits Analyst. Job grading, pay benchmarking, Workday."},
    {"name":"Amelia Johansson","email":"amelia.johansson@cv.com","education":"Master",
     "experience_years":6.0,
     "skills":["training delivery","learning & development","instructional design","lms","facilitation","coaching","stakeholder management","hr analytics"],
     "raw_text":"Amelia Johansson | MSc L&D | 6y | L&D Manager. Leadership programs, LMS governance, Kirkpatrick evaluation."},

    # ════════════════════════════════════════════════════════
    # SUPPLY CHAIN & LOGISTICS
    # ════════════════════════════════════════════════════════
    {"name":"Erica Fontaine","email":"erica.fontaine@cv.com","education":"Master",
     "experience_years":6.0,
     "skills":["supply chain management","procurement","vendor management","category management","contract negotiation","sap","rfq","strategic sourcing","s&op","demand planning"],
     "raw_text":"Erica Fontaine | MSc Supply Chain | 6y | Procurement Manager. $25M spend, SAP MM/SRM, strategic sourcing."},
    {"name":"Tobias Müller","email":"tobias.muller@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["supply chain management","demand planning","inventory management","sap scm","sql","excel","data analysis","s&op"],
     "raw_text":"Tobias Müller | 3y | Supply Chain Analyst. SAP SCM, S&OP process, demand forecasting."},
    {"name":"Adaeze Okonkwo","email":"adaeze.okonkwo@cv.com","education":"Bachelor",
     "experience_years":1.0,
     "skills":["supply chain management","excel","inventory management","data analysis"],
     "raw_text":"Adaeze Okonkwo | 1y | Logistics coordinator. Excel tracking, inventory counts, basic SAP."},
    {"name":"Rafael Morales","email":"rafael.morales@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["excel","microsoft office","data entry","supply chain management"],
     "raw_text":"Rafael Morales | 0y | Supply chain graduate. Excel, academic coursework in logistics."},
    {"name":"Ingrid Svensson","email":"ingrid.svensson@cv.com","education":"Bachelor",
     "experience_years":5.0,
     "skills":["logistics","warehousing","inventory management","3pl","import/export","customs","supply chain management","vendor management"],
     "raw_text":"Ingrid Svensson | 5y | Logistics Manager. 3PL management, customs compliance (Incoterms), WMS implementation."},
    {"name":"Kwabena Mensah","email":"kwabena.mensah@cv.com","education":"Bachelor",
     "experience_years":4.0,
     "skills":["procurement","strategic sourcing","vendor management","category management","contract negotiation","sap","supply chain management"],
     "raw_text":"Kwabena Mensah | 4y | Procurement Specialist. Supplier negotiation, SAP, category management."},

    # ════════════════════════════════════════════════════════
    # MECHANICAL / ELECTRICAL ENGINEERING
    # ════════════════════════════════════════════════════════
    {"name":"Markus Braun","email":"markus.braun@cv.com","education":"Master",
     "experience_years":7.0,
     "skills":["solidworks","catia","finite element analysis","ansys","mechanical design","autocad","lean manufacturing","fmea","quality management","gd&t"],
     "raw_text":"Markus Braun | MSc Mechanical | 7y | Senior mechanical design engineer. CATIA V5, ANSYS FEA, GD&T, FMEA. Automotive tier-1."},
    {"name":"Lena Fischer","email":"lena.fischer@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["solidworks","autocad","mechanical design","quality management","fmea"],
     "raw_text":"Lena Fischer | 3y | Mechanical design engineer. SolidWorks, AutoCAD, FMEA, DFM reviews."},
    {"name":"Youssef El-Amin","email":"youssef.elamin@cv.com","education":"Bachelor",
     "experience_years":1.0,
     "skills":["autocad","solidworks","mechanical design","technical drawing"],
     "raw_text":"Youssef El-Amin | 1y | Junior engineer. AutoCAD 2D/3D, SolidWorks models, BOM creation."},
    {"name":"Petra Novak","email":"petra.novak@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["autocad","solidworks","technical drawing","engineering basics"],
     "raw_text":"Petra Novak | 0y | Mechanical engineering graduate. AutoCAD, SolidWorks, university FEA projects."},
    {"name":"Álvaro Jiménez","email":"alvaro.jimenez@cv.com","education":"Bachelor",
     "experience_years":5.0,
     "skills":["electrical engineering","plc programming","scada","instrumentation","control systems","autocad","quality management","dcs"],
     "raw_text":"Álvaro Jiménez | 5y | E&I engineer. PLC/DCS programming, SCADA, P&ID, oil & gas."},
    {"name":"Caitlin Moore","email":"caitlin.moore@cv.com","education":"Bachelor",
     "experience_years":4.0,
     "skills":["lean manufacturing","six sigma","quality management","fmea","root cause analysis","process improvement","spc"],
     "raw_text":"Caitlin Moore | 4y | Process improvement engineer. Lean Six Sigma Black Belt. Kaizen, SPC, 5S."},
    {"name":"Erik Andersen","email":"erik.andersen@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["civil engineering","structural analysis","autocad","revit","bim","construction management"],
     "raw_text":"Erik Andersen | 3y | Civil/structural engineer. ETABS, Revit BIM, Eurocode structural design."},

    # ════════════════════════════════════════════════════════
    # HEALTHCARE
    # ════════════════════════════════════════════════════════
    {"name":"Beatriz Santos","email":"beatriz.santos@cv.com","education":"PhD",
     "experience_years":6.0,
     "skills":["clinical research","clinical trials","biostatistics","r","clinical data management","redcap","gcp","fda regulations","medical writing"],
     "raw_text":"Beatriz Santos | PhD Biostatistics | 6y | Principal biostatistician. Phase III oncology trials, CDISC, SAS/R, NDA submissions."},
    {"name":"Lukas Berger","email":"lukas.berger@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["emr","ehr","epic","hl7","fhir","hipaa","healthcare interoperability","sql"],
     "raw_text":"Lukas Berger | 3y | Healthcare IT analyst. Epic implementation, HL7/FHIR integrations, HIPAA."},
    {"name":"Aditi Sharma","email":"aditi.sharma@cv.com","education":"Master",
     "experience_years":4.0,
     "skills":["pharmacovigilance","drug safety","adverse event reporting","fda regulations","gcp","medical writing","regulatory submissions"],
     "raw_text":"Aditi Sharma | MSc Pharmacology | 4y | PV specialist. SAE processing, PSURs, EudraVigilance."},
    {"name":"François Dubois","email":"francois.dubois@cv.com","education":"Master",
     "experience_years":5.0,
     "skills":["hospital administration","healthcare operations","project management","lean manufacturing","six sigma","budgeting","stakeholder management"],
     "raw_text":"François Dubois | MSc Health Management | 5y | Hospital Operations Director. Lean, 400-bed hospital, budget €60M."},

    # ════════════════════════════════════════════════════════
    # DIGITAL MARKETING
    # ════════════════════════════════════════════════════════
    {"name":"Marta Kowalska","email":"marta.kowalska@cv.com","education":"Bachelor",
     "experience_years":5.0,
     "skills":["digital marketing","seo","sem","google ads","meta ads","google analytics","ga4","hubspot","email marketing","a/b testing","content marketing"],
     "raw_text":"Marta Kowalska | 5y | Digital Marketing Manager. €4M paid media, SEO 150% organic growth, GA4 implementation."},
    {"name":"Dimitri Papadopoulos","email":"dimitri.papadopoulos@cv.com","education":"Bachelor",
     "experience_years":2.0,
     "skills":["seo","content marketing","copywriting","ahrefs","semrush","google analytics","content strategy","a/b testing"],
     "raw_text":"Dimitri Papadopoulos | 2y | SEO specialist. Ahrefs, SEMrush, keyword research, on-page optimization."},
    {"name":"Yemi Adeyemi","email":"yemi.adeyemi@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["brand management","social media marketing","content marketing","canva","adobe creative suite","community management","copywriting","influencer marketing"],
     "raw_text":"Yemi Adeyemi | 3y | Brand & social media manager. Instagram 300K followers, influencer campaigns 6x ROAS."},
    {"name":"Elena Morozova","email":"elena.morozova@cv.com","education":"Master",
     "experience_years":4.0,
     "skills":["crm","hubspot","email marketing","marketing automation","salesforce","customer lifecycle","sql","a/b testing"],
     "raw_text":"Elena Morozova | MSc Marketing | 4y | CRM manager. HubSpot journeys, Salesforce MC, 35 automated flows."},
    {"name":"Sébastien Blanc","email":"sebastien.blanc@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["performance marketing","ppc","google ads","meta ads","a/b testing","google analytics","sql","tableau","conversion rate optimization"],
     "raw_text":"Sébastien Blanc | 3y | Performance marketing analyst. Google Ads, Meta, attribution modeling, CPA optimization."},
    {"name":"Rina Watanabe","email":"rina.watanabe@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["social media marketing","canva","content marketing","copywriting"],
     "raw_text":"Rina Watanabe | 0y | Marketing graduate. Social media internship, Canva, basic copywriting."},

    # ════════════════════════════════════════════════════════
    # LEGAL
    # ════════════════════════════════════════════════════════
    {"name":"Isabel Ferreira","email":"isabel.ferreira@cv.com","education":"Master",
     "experience_years":7.0,
     "skills":["corporate law","contract drafting","contract negotiation","merger & acquisition","legal research","legal writing","compliance","due diligence"],
     "raw_text":"Isabel Ferreira | LLM Corporate Law | 7y | Senior associate at Slaughter and May. M&A, SPAs, JVAs."},
    {"name":"Antoine Bernard","email":"antoine.bernard@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["data privacy","gdpr","ccpa","regulatory compliance","legal research","legal writing","compliance"],
     "raw_text":"Antoine Bernard | Law | 3y | Data privacy counsel. GDPR/CCPA compliance, DPIAs, data subject requests."},
    {"name":"Yuki Yamamoto","email":"yuki.yamamoto@cv.com","education":"Master",
     "experience_years":5.0,
     "skills":["intellectual property","patent law","trademark","copyright","contract drafting","legal research","licensing"],
     "raw_text":"Yuki Yamamoto | LLM IP | 5y | IP counsel. Patent prosecution, licensing agreements, 1500+ portfolio."},
    {"name":"Amira Hassan","email":"amira.hassan@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["legal research","legal writing","microsoft office","communication"],
     "raw_text":"Amira Hassan | Law graduate | 0y | Seeking first legal role. Legal research, moot court, law review."},
    {"name":"Kai Andersen","email":"kai.andersen@cv.com","education":"Master",
     "experience_years":4.0,
     "skills":["corporate law","contract drafting","legal research","compliance","due diligence","merger & acquisition","legal writing","contract negotiation"],
     "raw_text":"Kai Andersen | LLM | 4y | Associate at Clifford Chance. Corporate transactions, regulatory compliance."},

    # ════════════════════════════════════════════════════════
    # TECH — targeted, not generic (keep Python where real)
    # ════════════════════════════════════════════════════════
    {"name":"Anouk de Vries","email":"anouk.devries@cv.com","education":"Bachelor",
     "experience_years":3.0,
     "skills":["javascript","react","typescript","css","html","git","rest api","storybook"],
     "raw_text":"Anouk de Vries | 3y | React / TypeScript frontend developer. Design systems, Storybook, REST APIs."},
    {"name":"Brendan O'Connor","email":"brendan.oconnor@cv.com","education":"Bachelor",
     "experience_years":5.0,
     "skills":["python","fastapi","postgresql","docker","kubernetes","redis","celery","aws","git","rest api"],
     "raw_text":"Brendan O'Connor | 5y | Senior Python/FastAPI backend engineer. Async APIs, PostgreSQL, Kubernetes."},
    {"name":"Zara Ali","email":"zara.ali@cv.com","education":"Master",
     "experience_years":4.0,
     "skills":["machine learning","python","tensorflow","pytorch","nlp","sql","docker","mlops","data analysis","statistics"],
     "raw_text":"Zara Ali | MSc ML | 4y | ML engineer. NLP models, TensorFlow/PyTorch, MLOps pipelines."},
    {"name":"Marcus Johnson","email":"marcus.johnson@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["javascript","html","css","react","git"],
     "raw_text":"Marcus Johnson | 0y | Frontend bootcamp grad. React projects, responsive CSS, GitHub portfolio."},
    {"name":"Hana Kim","email":"hana.kim@cv.com","education":"Bachelor",
     "experience_years":2.0,
     "skills":["java","spring boot","sql","oop","api","git","docker"],
     "raw_text":"Hana Kim | 2y | Java backend developer. Spring Boot APIs, MySQL, Docker, unit testing."},
    {"name":"Diego Moreno","email":"diego.moreno@cv.com","education":"Bachelor",
     "experience_years":6.0,
     "skills":["javascript","typescript","node.js","react","postgresql","redis","docker","kubernetes","aws","microservices","ci/cd","git"],
     "raw_text":"Diego Moreno | 6y | Staff full stack engineer. Node.js microservices, React, AWS, Kafka, CI/CD."},
    {"name":"Aiko Tanaka","email":"aiko.tanaka@cv.com","education":"Bachelor",
     "experience_years":1.0,
     "skills":["python","sql","data analysis","pandas","excel","git"],
     "raw_text":"Aiko Tanaka | 1y | Junior data analyst. Python/pandas, SQL, Excel dashboards."},
    {"name":"Lasse Eriksen","email":"lasse.eriksen@cv.com","education":"Master",
     "experience_years":5.0,
     "skills":["devops","kubernetes","docker","ci/cd","aws","terraform","linux","python","git","monitoring","bash"],
     "raw_text":"Lasse Eriksen | MSc CS | 5y | DevOps/SRE. Kubernetes, Terraform, GitHub Actions, Datadog."},
    {"name":"Camille Dupont","email":"camille.dupont@cv.com","education":"Bachelor",
     "experience_years":0.0,
     "skills":["python","sql","statistics","excel","data analysis"],
     "raw_text":"Camille Dupont | 0y | Data science student. Python, SQL, statistics coursework, Kaggle beginner."},
]


def run():
    db = SessionLocal()
    try:
        # ── Step 1: Delete generic tech candidates ────────────────────────────
        deleted = 0
        for name in REMOVE_NAMES:
            cand = db.query(Candidate).filter(Candidate.name == name).first()
            if cand:
                db.delete(cand)
                deleted += 1
        db.commit()
        print(f"Deleted {deleted} generic tech candidates.\n")

        # ── Step 2: Add balanced candidates ──────────────────────────────────
        added = 0
        skipped = 0
        for c in BALANCED_CANDIDATES:
            if db.query(Candidate).filter(Candidate.email == c["email"]).first():
                skipped += 1
                continue
            cand = Candidate(
                name=c["name"], email=c["email"],
                education=c["education"], experience_years=c["experience_years"],
                raw_text=c["raw_text"],
            )
            db.add(cand)
            db.flush()
            for skill in c["skills"]:
                db.add(Skill(candidate_id=cand.id, skill_name=skill))
            added += 1
            print(f"  + {c['name']:30s} | {c['experience_years']:4.1f}y | {len(c['skills'])} skills")

        db.commit()
        print(f"\nAdded: {added} | Skipped (already exist): {skipped}")

        # ── Step 3: Report new distribution ──────────────────────────────────
        from sqlalchemy import func
        total = db.query(Candidate).count()
        skill_counts = (
            db.query(Skill.skill_name, func.count(Skill.candidate_id).label("n"))
            .group_by(Skill.skill_name)
            .order_by(func.count(Skill.candidate_id).desc())
            .limit(15)
            .all()
        )
        print(f"\nNew total: {total} candidates")
        print("\nTop 15 skills:")
        for s, n in skill_counts:
            print(f"  {n:3d} ({n/total*100:4.1f}%)  {s}")

    finally:
        db.close()


if __name__ == "__main__":
    run()
