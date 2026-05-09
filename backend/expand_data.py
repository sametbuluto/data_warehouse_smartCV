"""Expand sample data: add 35+ jobs across 9 sectors and 55+ diverse candidates."""
import json, os, sys

DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")

# ─── NEW JOB POSTINGS ────────────────────────────────────────────────────────

NEW_JOBS = [
    # ── FINANCE ──────────────────────────────────────────────────────────────
    {
        "title": "Financial Analyst",
        "description": "We are looking for a detail-oriented Financial Analyst to join our corporate finance team. You will build financial models, analyze investment opportunities, support budgeting and forecasting processes, and prepare management reporting packages. Strong proficiency in Excel, financial modeling, and accounting principles (GAAP/IFRS) is required. Experience with Bloomberg or Refinitiv preferred. CFA candidate or holder is a plus.",
        "required_skills": ["financial modeling", "financial analysis", "excel", "sql", "budgeting", "forecasting", "gaap", "bloomberg"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Senior Risk Manager",
        "description": "We seek an experienced Risk Manager to oversee enterprise risk frameworks covering credit risk, market risk, and operational risk. You will conduct VaR analysis, stress testing, and regulatory reporting (Basel III / Solvency II). Deep expertise in quantitative risk methodologies, Python or R for risk modelling, and regulatory frameworks is essential. FRM or CFA designation preferred.",
        "required_skills": ["risk management", "credit risk", "market risk", "var", "stress testing", "regulatory reporting", "python", "r", "basel iii", "frm"],
        "min_experience": 5.0,
        "education_level": "Master"
    },
    {
        "title": "Investment Banking Analyst",
        "description": "Join our M&A advisory team to support deal execution across sectors. Responsibilities include financial modeling, valuation (DCF, LBO, comparable company analysis), preparation of pitch books, and client due diligence. Candidates should be highly numerate, proficient in Excel and PowerPoint, with strong understanding of capital markets and corporate finance.",
        "required_skills": ["financial modeling", "valuation", "dcf", "lbo", "merger & acquisition", "excel", "powerpoint", "bloomberg", "financial analysis"],
        "min_experience": 1.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Treasury & Cash Management Analyst",
        "description": "Manage daily cash positions, FX hedging programs, and short-term investment portfolios. You will maintain banking relationships, support treasury system implementation (SAP Treasury), ensure compliance with treasury policies, and prepare liquidity forecasts. Experience in fx hedging, cash management, and ERP systems required.",
        "required_skills": ["treasury management", "cash management", "fx hedging", "sap", "financial modeling", "excel", "forecasting"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    {
        "title": "AML / Compliance Officer",
        "description": "Responsible for designing and implementing AML, KYC and regulatory compliance programs. You will conduct transaction monitoring, suspicious activity reporting, and regulatory liaison. Must have deep knowledge of AML regulations, FATF standards, and financial crime typologies. Experience with Actimize or Temenos Compliance Suite preferred.",
        "required_skills": ["aml", "kyc", "compliance", "regulatory compliance", "risk management", "financial analysis"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Equity Research Analyst",
        "description": "Produce in-depth equity research reports, earnings models, and investment recommendations for institutional clients. You will build and maintain detailed financial models, participate in earnings calls, and monitor sector trends. CFA qualification and experience with Bloomberg Terminal and FactSet required. Sector specialization in Technology or Healthcare preferred.",
        "required_skills": ["equity research", "financial modeling", "valuation", "bloomberg", "investment analysis", "excel", "cfa", "financial reporting"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    # ── HEALTHCARE & MEDICAL ─────────────────────────────────────────────────
    {
        "title": "Clinical Data Analyst",
        "description": "Join our clinical research team to analyze clinical trial datasets, generate statistical outputs, and contribute to regulatory submissions. You will work with clinical data management systems (REDCap, Medidata Rave), apply biostatistical methods, and collaborate with clinical operations. Proficiency in SAS or R, understanding of ICH/GCP guidelines, and familiarity with FDA/EMA regulatory requirements is required.",
        "required_skills": ["clinical research", "clinical trials", "biostatistics", "r", "clinical data management", "redcap", "gcp", "fda regulations"],
        "min_experience": 2.0,
        "education_level": "Master"
    },
    {
        "title": "Healthcare IT Specialist",
        "description": "Implement, configure, and support healthcare information systems including EMR/EHR platforms (Epic, Cerner). You will lead HL7/FHIR integration projects, ensure HIPAA compliance, support clinical workflow optimization, and conduct end-user training. Strong technical skills combined with clinical domain knowledge are essential.",
        "required_skills": ["emr", "ehr", "epic", "hl7", "fhir", "hipaa", "healthcare interoperability", "sql"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Pharmacovigilance Specialist",
        "description": "Monitor drug safety signals, process adverse event reports, and prepare submissions to regulatory authorities (FDA MedWatch, EMA EudraVigilance). You will conduct literature searches, signal detection, and periodic safety update reports (PSURs). Strong knowledge of ICH E2 guidelines, GVP modules, and MedDRA coding required.",
        "required_skills": ["pharmacovigilance", "drug safety", "adverse event reporting", "fda regulations", "gcp", "medical writing", "regulatory submissions"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Healthcare Data Scientist",
        "description": "Develop predictive models and real-world evidence studies using large healthcare datasets (claims, EHR, registries). Apply machine learning, survival analysis, and NLP to improve patient outcomes and operational efficiency. Experience with Python/R, healthcare data standards (HL7, FHIR, ICD-10), and regulatory/ethical considerations in healthcare AI required.",
        "required_skills": ["machine learning", "python", "r", "healthcare analytics", "hl7", "fhir", "icd-10", "nlp", "biostatistics", "real-world evidence"],
        "min_experience": 3.0,
        "education_level": "Master"
    },
    {
        "title": "Hospital Operations Manager",
        "description": "Oversee day-to-day hospital operations, coordinate clinical and non-clinical departments, and drive process improvement initiatives. You will manage budgets, staffing plans, patient flow, and accreditation requirements. Lean / Six Sigma experience and familiarity with hospital information systems is required.",
        "required_skills": ["hospital administration", "healthcare operations", "project management", "lean manufacturing", "six sigma", "budgeting", "stakeholder management"],
        "min_experience": 5.0,
        "education_level": "Master"
    },
    # ── DIGITAL MARKETING ────────────────────────────────────────────────────
    {
        "title": "Digital Marketing Manager",
        "description": "Lead the digital marketing strategy across paid search, paid social, SEO, email, and display channels. You will manage campaign performance using Google Analytics 4, optimize ROI across Google Ads and Meta Ads, oversee marketing automation (HubSpot/Marketo), and collaborate with content and creative teams. Strong analytical skills and data-driven mindset required.",
        "required_skills": ["digital marketing", "seo", "sem", "google ads", "meta ads", "google analytics", "ga4", "hubspot", "email marketing", "a/b testing"],
        "min_experience": 4.0,
        "education_level": "Bachelor"
    },
    {
        "title": "SEO & Content Marketing Specialist",
        "description": "Develop and execute organic growth strategies through technical SEO audits, keyword research, link-building campaigns, and high-quality content production. You will use tools like Ahrefs, SEMrush, and Google Search Console to track rankings and traffic. Proven track record of growing organic traffic by 50%+ required.",
        "required_skills": ["seo", "content marketing", "copywriting", "ahrefs", "semrush", "google analytics", "content strategy", "a/b testing"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Performance Marketing Analyst",
        "description": "Manage and optimize paid media campaigns across Google Ads, Meta, LinkedIn, and programmatic channels. You will analyze campaign data, conduct A/B tests, build attribution models, and report on ROAS and CPA metrics. Proficiency in SQL for custom reporting and experience with data visualization tools (Tableau, Looker) is a plus.",
        "required_skills": ["performance marketing", "ppc", "google ads", "meta ads", "a/b testing", "google analytics", "sql", "tableau", "conversion rate optimization"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Brand & Social Media Manager",
        "description": "Define and maintain brand identity across all touchpoints. You will manage organic and paid social media presence on Instagram, LinkedIn, TikTok, and YouTube; create content calendars; engage communities; and measure brand health metrics. Experience with Canva, Adobe Creative Suite, and social analytics tools required.",
        "required_skills": ["brand management", "social media marketing", "content marketing", "canva", "adobe creative suite", "community management", "copywriting", "influencer marketing"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    {
        "title": "CRM & Marketing Automation Specialist",
        "description": "Build, automate, and optimize multi-touch customer journeys using HubSpot and Salesforce Marketing Cloud. You will segment audiences, design email nurture programs, manage lead scoring, and analyze lifecycle metrics. Proficiency in HTML/CSS for email templates and SQL for audience segmentation preferred.",
        "required_skills": ["crm", "hubspot", "email marketing", "marketing automation", "salesforce", "customer lifecycle", "sql", "a/b testing"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    # ── LEGAL ────────────────────────────────────────────────────────────────
    {
        "title": "Corporate Legal Counsel",
        "description": "Provide legal advice across commercial contracts, corporate governance, M&A transactions, and regulatory compliance. You will draft and negotiate a wide range of agreements, advise the board on corporate matters, and manage external counsel. Strong background in corporate law, contract drafting, and commercial negotiation required.",
        "required_skills": ["corporate law", "contract drafting", "contract negotiation", "merger & acquisition", "legal research", "legal writing", "compliance", "due diligence"],
        "min_experience": 5.0,
        "education_level": "Master"
    },
    {
        "title": "Data Privacy & GDPR Specialist",
        "description": "Develop and maintain the company's data protection framework in compliance with GDPR, CCPA, and other applicable privacy laws. You will conduct DPIAs, maintain records of processing activities, handle data subject requests, and work with IT teams on privacy-by-design implementation.",
        "required_skills": ["data privacy", "gdpr", "ccpa", "regulatory compliance", "legal research", "legal writing", "compliance"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    {
        "title": "IP & Technology Lawyer",
        "description": "Manage the company's intellectual property portfolio including patents, trademarks, and copyrights. You will advise on IP strategy, conduct freedom-to-operate analyses, manage licensing agreements, and support technology transactions. Experience with patent prosecution and IP litigation preferred.",
        "required_skills": ["intellectual property", "patent law", "trademark", "copyright", "contract drafting", "legal research", "licensing"],
        "min_experience": 4.0,
        "education_level": "Master"
    },
    # ── ENGINEERING (MECHANICAL / CIVIL) ──────────────────────────────────────
    {
        "title": "Senior Mechanical Design Engineer",
        "description": "Lead the mechanical design of industrial equipment and product assemblies using SolidWorks and CATIA. You will perform FEA simulations (ANSYS), GD&T tolerancing, design for manufacturability reviews, and collaborate with manufacturing teams. Experience in automotive or aerospace sectors and familiarity with IATF 16949 / AS9100 standards required.",
        "required_skills": ["solidworks", "catia", "finite element analysis", "ansys", "mechanical design", "autocad", "lean manufacturing", "fmea", "quality management"],
        "min_experience": 5.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Civil & Structural Engineer",
        "description": "Design and analyze structural systems for commercial and infrastructure projects. You will prepare structural calculations, drawings in AutoCAD/Revit, and BIM models. Experience with ETABS, SAP2000, or STAAD.Pro for structural analysis, and knowledge of Eurocode / ACI standards required. Experience with construction management and site supervision is a plus.",
        "required_skills": ["civil engineering", "structural analysis", "autocad", "revit", "bim", "construction management", "project scheduling"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Electrical & Instrumentation Engineer",
        "description": "Design electrical systems, instrument loops, and control architecture for oil & gas and process industries. Responsibilities include P&ID development, cause-and-effect diagrams, PLC/DCS programming, and SCADA configuration. Knowledge of IEC 61511 functional safety standard and experience with Siemens S7 / Allen Bradley PLCs required.",
        "required_skills": ["electrical engineering", "plc programming", "scada", "instrumentation", "control systems", "autocad", "quality management"],
        "min_experience": 4.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Manufacturing & Process Improvement Engineer",
        "description": "Drive Lean/Six Sigma initiatives to eliminate waste, reduce cycle times, and improve product quality across manufacturing lines. You will lead kaizen events, conduct time-motion studies, implement 5S programs, and use statistical process control (SPC) methods. Black Belt or Green Belt certification preferred.",
        "required_skills": ["lean manufacturing", "six sigma", "quality management", "fmea", "root cause analysis", "process improvement", "statistical analysis"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    # ── HUMAN RESOURCES ──────────────────────────────────────────────────────
    {
        "title": "HR Business Partner",
        "description": "Act as a strategic advisor to business leaders, delivering talent solutions aligned with business objectives. You will manage performance cycles, drive organizational design, lead change management initiatives, resolve employee relations issues, and partner on workforce planning. Deep knowledge of employment law, coaching skills, and experience with Workday or SAP SuccessFactors required.",
        "required_skills": ["talent acquisition", "performance management", "employee relations", "change management", "hr analytics", "workday", "employment law", "organizational development"],
        "min_experience": 5.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Talent Acquisition Manager",
        "description": "Lead full-cycle recruitment for senior and specialist roles across business functions. You will design sourcing strategies, manage Employer Value Proposition (EVP), use LinkedIn Recruiter and ATS platforms, develop hiring manager capability, and report on recruiting metrics (time-to-fill, cost-per-hire, quality-of-hire). Experience in high-volume and executive search preferred.",
        "required_skills": ["talent acquisition", "recruitment", "linkedin recruiter", "sourcing", "hris", "hr analytics", "onboarding", "stakeholder management"],
        "min_experience": 4.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Learning & Development Specialist",
        "description": "Design, develop, and facilitate learning programs aligned to business needs. You will apply instructional design methodologies (ADDIE, SAM), build e-learning content in Articulate Storyline and Rise, manage LMS platforms (Moodle, Cornerstone), and evaluate program effectiveness using Kirkpatrick model.",
        "required_skills": ["learning & development", "instructional design", "e-learning", "articulate storyline", "lms", "moodle", "training delivery", "content creation", "facilitation"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Compensation & Benefits Analyst",
        "description": "Conduct market pay benchmarking, maintain job architecture and grading systems, design incentive compensation plans, and administer benefits programs. You will use Mercer or Willis Towers Watson compensation surveys, build Excel models for total rewards analysis, and partner with HR Business Partners on C&B strategy.",
        "required_skills": ["compensation & benefits", "hr analytics", "excel", "financial modeling", "benchmarking", "workday", "hris"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    # ── SUPPLY CHAIN ──────────────────────────────────────────────────────────
    {
        "title": "Supply Chain Analyst",
        "description": "Analyze supply chain data to identify cost reduction, inventory optimization, and service improvement opportunities. You will build demand forecasts, run S&OP processes, manage KPI dashboards, and support ERP data management (SAP SCM / Oracle). Strong analytical skills and proficiency in SQL and Excel required; Python or R for advanced analytics is a plus.",
        "required_skills": ["supply chain management", "demand planning", "s&op", "inventory management", "sap scm", "sql", "excel", "data analysis"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Procurement & Sourcing Manager",
        "description": "Lead strategic sourcing initiatives, manage supplier relationships, and negotiate contracts to deliver cost savings and supply security. You will conduct RFQ/RFP processes, supplier evaluation, and category management. Deep expertise in procurement methodology, contract law fundamentals, and SAP MM required.",
        "required_skills": ["procurement", "strategic sourcing", "vendor management", "category management", "contract negotiation", "sap", "rfq", "supply chain management"],
        "min_experience": 5.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Logistics & Distribution Manager",
        "description": "Manage end-to-end logistics operations including inbound, warehousing, order fulfillment, and last-mile delivery. You will oversee 3PL partnerships, manage transportation costs, ensure customs compliance (Incoterms), and implement warehouse management system (WMS) improvements.",
        "required_skills": ["logistics", "warehousing", "inventory management", "3pl", "import/export", "customs", "supply chain management", "vendor management"],
        "min_experience": 4.0,
        "education_level": "Bachelor"
    },
    # ── SALES & BUSINESS DEVELOPMENT ──────────────────────────────────────────
    {
        "title": "Enterprise Sales Manager",
        "description": "Drive new business revenue by leading a team of account executives targeting enterprise accounts. You will define territory strategies, coach sales reps, manage a complex B2B pipeline in Salesforce, and engage C-suite stakeholders. Experience in SaaS or technology sales with consistent track record of exceeding quota required.",
        "required_skills": ["b2b sales", "enterprise sales", "sales management", "salesforce", "pipeline management", "negotiation", "sales forecasting", "crm"],
        "min_experience": 6.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Business Development Manager",
        "description": "Identify, qualify, and close strategic partnership and new revenue opportunities. You will develop go-to-market plans, conduct market research, build business cases, and manage stakeholder relationships. Cross-functional collaboration with product, marketing, and legal teams is essential.",
        "required_skills": ["business development", "b2b sales", "market research", "negotiation", "crm", "strategic planning", "stakeholder management", "salesforce"],
        "min_experience": 4.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Customer Success Manager",
        "description": "Own the post-sales relationship for a portfolio of enterprise accounts, ensuring adoption, satisfaction, retention, and growth. You will conduct QBRs, build success plans, identify upsell opportunities, and act as the voice of the customer internally. Experience with SaaS platforms, Gainsight or ChurnZero, and Salesforce CRM required.",
        "required_skills": ["customer success", "account management", "salesforce", "crm", "upselling", "stakeholder management", "client relationship management"],
        "min_experience": 3.0,
        "education_level": "Bachelor"
    },
    # ── EDUCATION & TRAINING ──────────────────────────────────────────────────
    {
        "title": "Instructional Designer & E-Learning Developer",
        "description": "Design and develop engaging digital learning experiences for corporate audiences. You will apply the ADDIE and SAM models, create SCORM-compliant e-learning modules in Articulate Storyline and Rise, manage content in LMS platforms (Moodle, Cornerstone), and collaborate with SMEs to ensure accuracy and relevance.",
        "required_skills": ["instructional design", "e-learning", "articulate storyline", "scorm", "lms", "moodle", "curriculum development", "adult learning theory", "content creation"],
        "min_experience": 2.0,
        "education_level": "Bachelor"
    },
    {
        "title": "Corporate Training & Development Manager",
        "description": "Lead the company's learning strategy, manage the training team, and partner with HR and business leaders on capability building. You will design leadership development programs, manage vendor relationships (external trainers, platforms), oversee the LMS, and measure training ROI using Kirkpatrick model. Coaching certification is a plus.",
        "required_skills": ["training delivery", "learning & development", "instructional design", "lms", "facilitation", "coaching", "stakeholder management", "hr analytics"],
        "min_experience": 6.0,
        "education_level": "Master"
    },
]

# ─── NEW CANDIDATES ───────────────────────────────────────────────────────────

NEW_CANDIDATES = [
    # ── FINANCE ──────────────────────────────────────────────────────────────
    {
        "name": "Sophie Laurent",
        "email": "sophie.laurent@email.com",
        "phone": "+1-212-555-0181",
        "education": "Master",
        "experience_years": 6.0,
        "category": "Finance",
        "skills": ["financial modeling", "financial analysis", "excel", "sql", "bloomberg", "valuation", "dcf", "equity research", "powerpoint", "financial reporting"],
        "raw_text": """Sophie Laurent
sophie.laurent@email.com | +1-212-555-0181 | New York, NY

SUMMARY
CFA charterholder with 6 years of experience in equity research and investment banking. Deep expertise in financial modeling, valuation, and capital markets analysis.

EXPERIENCE
Senior Equity Research Analyst | Morgan Stanley | 06/2021 - Present
- Build complex DCF, LBO, and comparable company analysis models for technology sector coverage
- Publish initiation reports and quarterly earnings previews using Bloomberg Terminal and FactSet
- Collaborate with institutional sales team on client presentations

Investment Banking Analyst | Goldman Sachs | 07/2018 - 05/2021
- Executed 12+ M&A advisory mandates with aggregate deal value of $4.2B
- Prepared pitchbooks, financial models, and due diligence packages
- Performed DCF, LBO, and precedent transaction analyses

EDUCATION
Master of Finance | Columbia Business School | 2018
Bachelor of Economics | New York University | 2016

SKILLS
Financial Modeling, Financial Analysis, Valuation, DCF, LBO, Equity Research, Bloomberg Terminal, Excel, SQL, PowerPoint, Financial Reporting, Merger & Acquisition, CFA"""
    },
    {
        "name": "Marcus Webb",
        "email": "marcus.webb@email.com",
        "phone": "+44-20-555-0182",
        "education": "Master",
        "experience_years": 8.0,
        "category": "Finance",
        "skills": ["risk management", "credit risk", "market risk", "var", "stress testing", "regulatory reporting", "python", "r", "basel iii", "financial modeling", "sql"],
        "raw_text": """Marcus Webb
marcus.webb@email.com | +44-20-555-0182 | London, UK

SUMMARY
FRM-certified risk professional with 8 years of experience in quantitative risk management at Tier-1 banks. Expert in credit, market, and operational risk with strong Python/R quantitative skills.

EXPERIENCE
Head of Market Risk | HSBC | 03/2020 - Present
- Lead VaR model development and stress testing frameworks (Basel III / FRTB)
- Manage regulatory reporting to PRA and EBA
- Drive model risk governance and validation processes

Senior Credit Risk Analyst | Barclays | 01/2016 - 02/2020
- Build credit risk models for corporate and SME portfolios using Python/R
- Develop IFRS 9 Expected Credit Loss (ECL) models
- Conduct stress testing and scenario analysis

EDUCATION
MSc Financial Mathematics | Imperial College London | 2015
BSc Mathematics | University of Bristol | 2013

SKILLS
Risk Management, Credit Risk, Market Risk, Operational Risk, VaR, Stress Testing, Basel III, Regulatory Reporting, Python, R, SQL, Financial Modeling, FRM"""
    },
    {
        "name": "Fatima Al-Rashidi",
        "email": "fatima.rashidi@email.com",
        "phone": "+971-50-555-0183",
        "education": "Bachelor",
        "experience_years": 4.0,
        "category": "Finance",
        "skills": ["aml", "kyc", "compliance", "regulatory compliance", "risk management", "financial analysis", "excel", "sql"],
        "raw_text": """Fatima Al-Rashidi
fatima.rashidi@email.com | +971-50-555-0183 | Dubai, UAE

SUMMARY
Compliance and AML professional with 4 years of experience in banking and financial services. Specialised in KYC/AML program development, regulatory compliance, and financial crime prevention.

EXPERIENCE
AML Compliance Officer | Emirates NBD | 08/2022 - Present
- Manage transaction monitoring, suspicious activity reporting, and KYC onboarding
- Conduct AML risk assessments and develop compliance policies
- Liaise with regulators (CBUAE, FATF)

Compliance Analyst | Abu Dhabi Islamic Bank | 06/2020 - 07/2022
- Performed KYC due diligence on corporate and individual clients
- Supported regulatory examinations and internal audits
- Developed AML training materials

EDUCATION
Bachelor of Finance | American University of Sharjah | 2020

SKILLS
AML, KYC, Anti-Money Laundering, Compliance, Regulatory Compliance, Risk Management, Financial Analysis, Excel, SQL"""
    },
    {
        "name": "Oliver Thornton",
        "email": "oliver.thornton@email.com",
        "phone": "+1-312-555-0184",
        "education": "Bachelor",
        "experience_years": 3.0,
        "category": "Finance",
        "skills": ["financial modeling", "budgeting", "forecasting", "excel", "sap fico", "financial reporting", "variance analysis", "gaap", "powerpoint"],
        "raw_text": """Oliver Thornton
oliver.thornton@email.com | +1-312-555-0184 | Chicago, IL

SUMMARY
Financial Analyst with 3 years of FP&A experience in manufacturing and consumer goods. Proficient in SAP FICO, advanced Excel modeling, and GAAP financial reporting.

EXPERIENCE
Financial Analyst – FP&A | Caterpillar Inc. | 07/2021 - Present
- Build annual budgets and rolling forecasts for $500M revenue business unit
- Perform variance analysis comparing actuals vs. plan and prior year
- Prepare monthly management reporting packages for CFO

Junior Financial Analyst | Abbott Laboratories | 06/2020 - 06/2021
- Supported month-end close process and SAP FICO journal entries
- Built Excel models for capital expenditure analysis

EDUCATION
Bachelor of Accounting | University of Illinois | 2020

SKILLS
Financial Modeling, Budgeting, Forecasting, Excel, SAP FICO, Financial Reporting, Variance Analysis, GAAP, PowerPoint"""
    },
    {
        "name": "Yuki Tanaka",
        "email": "yuki.tanaka@email.com",
        "phone": "+81-3-555-0185",
        "education": "Bachelor",
        "experience_years": 5.0,
        "category": "Finance",
        "skills": ["treasury management", "cash management", "fx hedging", "financial modeling", "excel", "sap", "forecasting", "financial analysis"],
        "raw_text": """Yuki Tanaka
yuki.tanaka@email.com | +81-3-555-0185 | Tokyo, Japan

SUMMARY
Treasury professional with 5 years of experience managing cash, FX, and debt in multinational corporations. Expert in SAP Treasury and financial risk management.

EXPERIENCE
Treasury Manager | Sony Corporation | 04/2021 - Present
- Manage $2B+ global cash positions and short-term investment portfolio
- Execute FX hedging strategies (forwards, options) across 15 currencies
- Lead SAP Treasury module implementation

Treasury Analyst | Honda Motor Company | 04/2019 - 03/2021
- Prepared daily cash position reports and liquidity forecasts
- Supported bank relationship management and credit facility negotiations

EDUCATION
Bachelor of Finance | Keio University | 2019

SKILLS
Treasury Management, Cash Management, FX Hedging, Financial Modeling, Excel, SAP, Forecasting, Financial Analysis"""
    },
    # ── HEALTHCARE ────────────────────────────────────────────────────────────
    {
        "name": "Dr. Emma Hartley",
        "email": "emma.hartley@email.com",
        "phone": "+1-617-555-0186",
        "education": "PhD",
        "experience_years": 7.0,
        "category": "Healthcare",
        "skills": ["clinical research", "clinical trials", "biostatistics", "r", "python", "clinical data management", "redcap", "gcp", "fda regulations", "medical writing"],
        "raw_text": """Dr. Emma Hartley, PhD
emma.hartley@email.com | +1-617-555-0186 | Boston, MA

SUMMARY
Clinical data scientist with PhD in Biostatistics and 7 years of experience in pharmaceutical and CRO environments. Expert in clinical trial analysis, FDA regulatory submissions, and real-world evidence studies.

EXPERIENCE
Principal Biostatistician | Pfizer | 09/2020 - Present
- Lead statistical analysis for Phase II/III oncology trials (NDA/BLA submissions)
- Develop SAP, TLF shells, and CDISC-compliant datasets
- Program analyses in R and SAS; manage REDCap databases

Biostatistician | IQVIA | 06/2017 - 08/2020
- Supported 15+ clinical trials across therapeutic areas
- Applied survival analysis, mixed models, and Bayesian methods

EDUCATION
PhD Biostatistics | Harvard School of Public Health | 2017
BSc Statistics | University of Edinburgh | 2013

SKILLS
Clinical Research, Clinical Trials, Biostatistics, R, Python, Clinical Data Management, REDCap, GCP, FDA Regulations, Medical Writing, ICH Guidelines, Regulatory Submissions"""
    },
    {
        "name": "James Okafor",
        "email": "james.okafor@email.com",
        "phone": "+1-713-555-0187",
        "education": "Bachelor",
        "experience_years": 4.0,
        "category": "Healthcare",
        "skills": ["emr", "ehr", "epic", "hl7", "fhir", "hipaa", "healthcare interoperability", "sql", "project management"],
        "raw_text": """James Okafor
james.okafor@email.com | +1-713-555-0187 | Houston, TX

SUMMARY
Healthcare IT professional with 4 years of experience implementing Epic EHR systems and HL7/FHIR integrations across large health systems.

EXPERIENCE
Epic Implementation Consultant | Texas Medical Center | 03/2022 - Present
- Lead Epic Ambulatory module go-live for 800-physician practice
- Configure HL7 interfaces and FHIR API integrations
- Ensure HIPAA compliance in all data exchange workflows

Healthcare IT Analyst | Memorial Hermann | 06/2020 - 02/2022
- Supported EMR/EHR system administration and end-user training
- Resolved HL7 interface issues and data quality problems

EDUCATION
Bachelor of Health Information Management | University of Houston | 2020

SKILLS
EMR, EHR, Epic, HL7, FHIR, HIPAA, Healthcare Interoperability, SQL, Project Management"""
    },
    {
        "name": "Natalie Dupont",
        "email": "natalie.dupont@email.com",
        "phone": "+33-1-555-0188",
        "education": "Master",
        "experience_years": 5.0,
        "category": "Healthcare",
        "skills": ["pharmacovigilance", "drug safety", "adverse event reporting", "fda regulations", "gcp", "medical writing", "regulatory submissions", "clinical research"],
        "raw_text": """Natalie Dupont
natalie.dupont@email.com | +33-1-555-0188 | Paris, France

SUMMARY
Pharmacovigilance specialist with 5 years in global drug safety at major pharma companies. Expert in adverse event processing, PSUR writing, and EMA/FDA regulatory submissions.

EXPERIENCE
Senior PV Specialist | Sanofi | 01/2021 - Present
- Process and assess serious adverse event (SAE) reports per ICH E2 guidelines
- Prepare Periodic Safety Update Reports (PSURs) for 6 marketed products
- Signal detection and evaluation using EudraVigilance and VigiBase

PV Scientist | Novartis | 03/2019 - 12/2020
- Managed global adverse event database (Argus Safety)
- Authored Risk Management Plans (RMPs) and Patient Labelling

EDUCATION
MSc Pharmacology | Université Paris-Saclay | 2019
BSc Pharmacy | Université de Lyon | 2017

SKILLS
Pharmacovigilance, Drug Safety, Adverse Event Reporting, FDA Regulations, GCP, Medical Writing, Regulatory Submissions, Clinical Research, ICH Guidelines"""
    },
    {
        "name": "Priya Subramaniam",
        "email": "priya.subramaniam@email.com",
        "phone": "+1-617-555-0189",
        "education": "Master",
        "experience_years": 5.0,
        "category": "Healthcare",
        "skills": ["machine learning", "python", "r", "healthcare analytics", "hl7", "fhir", "nlp", "biostatistics", "sql", "data science"],
        "raw_text": """Priya Subramaniam
priya.subramaniam@email.com | +1-617-555-0189 | Boston, MA

SUMMARY
Healthcare data scientist with 5 years of experience applying machine learning and NLP to clinical and claims data to improve patient outcomes and operational efficiency.

EXPERIENCE
Senior Data Scientist | Mass General Brigham | 06/2021 - Present
- Develop sepsis early warning models using EHR time-series data (AUC 0.92)
- Apply NLP to unstructured clinical notes for ICD-10 coding automation
- Collaborate with clinical informatics teams on HL7/FHIR data pipelines

Data Scientist | Blue Cross Blue Shield | 08/2019 - 05/2021
- Built predictive models for readmission risk and chronic disease management
- Analyzed Medicare/Medicaid claims data for population health programs

EDUCATION
MSc Biomedical Informatics | Harvard Medical School | 2019
BSc Computer Science | IIT Madras | 2017

SKILLS
Machine Learning, Python, R, Healthcare Analytics, HL7, FHIR, NLP, Biostatistics, SQL, Data Science, ICD-10"""
    },
    # ── DIGITAL MARKETING ─────────────────────────────────────────────────────
    {
        "name": "Isabella Romano",
        "email": "isabella.romano@email.com",
        "phone": "+39-02-555-0190",
        "education": "Bachelor",
        "experience_years": 6.0,
        "category": "Marketing",
        "skills": ["digital marketing", "seo", "sem", "google ads", "meta ads", "google analytics", "ga4", "hubspot", "email marketing", "a/b testing", "content marketing"],
        "raw_text": """Isabella Romano
isabella.romano@email.com | +39-02-555-0190 | Milan, Italy

SUMMARY
Digital marketing leader with 6 years of experience scaling performance marketing programs for e-commerce and B2B SaaS companies. Google Ads and Meta Blueprint certified.

EXPERIENCE
Head of Digital Marketing | Zalando Italy | 04/2022 - Present
- Manage €5M annual paid media budget across Google Ads, Meta Ads, and programmatic
- Lead SEO strategy driving 120% organic traffic growth
- Implement GA4 migration and attribution modeling

Senior Marketing Manager | HubSpot Partner Agency | 01/2020 - 03/2022
- Managed 20+ client campaigns across SEM, SEO, and email marketing
- Built HubSpot marketing automation workflows and lead nurture sequences

EDUCATION
Bachelor of Marketing | Bocconi University | 2018

SKILLS
Digital Marketing, SEO, SEM, PPC, Google Ads, Meta Ads, Google Analytics, GA4, HubSpot, Email Marketing, A/B Testing, Content Marketing, Performance Marketing"""
    },
    {
        "name": "Carlos Mendez",
        "email": "carlos.mendez@email.com",
        "phone": "+34-91-555-0191",
        "education": "Bachelor",
        "experience_years": 4.0,
        "category": "Marketing",
        "skills": ["seo", "content marketing", "copywriting", "ahrefs", "semrush", "google analytics", "content strategy", "a/b testing", "social media marketing"],
        "raw_text": """Carlos Mendez
carlos.mendez@email.com | +34-91-555-0191 | Madrid, Spain

SUMMARY
SEO & content specialist with 4 years of experience growing organic search presence for media and tech brands. Expert in technical SEO, content strategy, and link building.

EXPERIENCE
SEO Manager | Idealista | 06/2022 - Present
- Grew organic sessions by 180% through technical SEO fixes and content hub strategy
- Conduct keyword research using Ahrefs and SEMrush; manage 50+ content briefs/month
- Implement structured data, Core Web Vitals optimisation

Content Marketing Lead | Typeform | 03/2020 - 05/2022
- Built content calendar and editorial workflow for SaaS blog (200K monthly readers)
- Managed team of 8 freelance writers; optimised content for E-E-A-T

EDUCATION
Bachelor of Journalism | Universidad Complutense de Madrid | 2020

SKILLS
SEO, Content Marketing, Copywriting, Ahrefs, SEMrush, Google Analytics, Content Strategy, A/B Testing, Social Media Marketing"""
    },
    {
        "name": "Aisha Nwosu",
        "email": "aisha.nwosu@email.com",
        "phone": "+234-80-555-0192",
        "education": "Bachelor",
        "experience_years": 3.0,
        "category": "Marketing",
        "skills": ["brand management", "social media marketing", "content marketing", "canva", "adobe creative suite", "community management", "copywriting", "influencer marketing", "google analytics"],
        "raw_text": """Aisha Nwosu
aisha.nwosu@email.com | +234-80-555-0192 | Lagos, Nigeria

SUMMARY
Creative brand and social media professional with 3 years of experience building engaged communities and executing multi-channel brand campaigns for consumer brands.

EXPERIENCE
Brand & Social Media Manager | Jumia | 08/2023 - Present
- Manage brand identity and social media presence across Instagram (500K followers), LinkedIn, TikTok
- Execute influencer marketing campaigns with 8x ROAS
- Design visual assets using Adobe Creative Suite and Canva

Social Media Coordinator | Paystack | 05/2021 - 07/2023
- Grew Twitter/X following from 20K to 150K through organic content strategy
- Managed community responses and crisis communications

EDUCATION
Bachelor of Mass Communication | University of Lagos | 2021

SKILLS
Brand Management, Social Media Marketing, Content Marketing, Canva, Adobe Creative Suite, Community Management, Copywriting, Influencer Marketing, Google Analytics"""
    },
    {
        "name": "Thomas Müller",
        "email": "thomas.mueller@email.com",
        "phone": "+49-89-555-0193",
        "education": "Master",
        "experience_years": 5.0,
        "category": "Marketing",
        "skills": ["crm", "hubspot", "email marketing", "marketing automation", "salesforce", "customer lifecycle", "sql", "a/b testing", "data analysis"],
        "raw_text": """Thomas Müller
thomas.mueller@email.com | +49-89-555-0193 | Munich, Germany

SUMMARY
CRM and marketing automation specialist with 5 years of experience building customer lifecycle programs for B2B SaaS and fintech companies. HubSpot and Salesforce Marketing Cloud certified.

EXPERIENCE
CRM Manager | N26 | 07/2022 - Present
- Manage 40+ automated customer journeys across HubSpot reaching 2M+ users
- Lead A/B testing program generating €3.2M additional annual revenue
- Build SQL-based audience segmentation and personalisation frameworks

Marketing Automation Specialist | Personio | 01/2020 - 06/2022
- Implemented Salesforce Marketing Cloud for B2B demand generation
- Managed email programme with 42% average open rate

EDUCATION
MSc Marketing | Ludwig Maximilian University Munich | 2019
BSc Business | Frankfurt School | 2017

SKILLS
CRM, HubSpot, Email Marketing, Marketing Automation, Salesforce, Customer Lifecycle, SQL, A/B Testing, Data Analysis"""
    },
    # ── LEGAL ─────────────────────────────────────────────────────────────────
    {
        "name": "Victoria Chambers",
        "email": "victoria.chambers@email.com",
        "phone": "+44-20-555-0194",
        "education": "Master",
        "experience_years": 8.0,
        "category": "Legal",
        "skills": ["corporate law", "contract drafting", "contract negotiation", "merger & acquisition", "legal research", "legal writing", "compliance", "due diligence"],
        "raw_text": """Victoria Chambers
victoria.chambers@email.com | +44-20-555-0194 | London, UK

SUMMARY
Qualified solicitor with 8 years of experience in corporate law and M&A at Magic Circle firm. Specialist in cross-border transactions, contract negotiation, and corporate governance.

EXPERIENCE
Senior Associate | Freshfields Bruckhaus Deringer | 09/2019 - Present
- Lead legal execution on 20+ M&A transactions (deal values £50M - £3B)
- Draft and negotiate SPAs, JVAs, and SHA agreements
- Advise boards on corporate governance and fiduciary duties

Associate | Allen & Overy | 09/2016 - 08/2019
- Supported complex multi-jurisdictional M&A deals
- Conducted legal due diligence on target companies

EDUCATION
LLM Corporate Law | London School of Economics | 2016
LLB Law (First Class) | University of Cambridge | 2014

SKILLS
Corporate Law, Contract Drafting, Contract Negotiation, Merger & Acquisition, Legal Research, Legal Writing, Compliance, Due Diligence, Mergers & Acquisitions"""
    },
    {
        "name": "Rafael Souza",
        "email": "rafael.souza@email.com",
        "phone": "+55-11-555-0195",
        "education": "Bachelor",
        "experience_years": 4.0,
        "category": "Legal",
        "skills": ["data privacy", "gdpr", "ccpa", "regulatory compliance", "legal research", "legal writing", "compliance", "contract drafting"],
        "raw_text": """Rafael Souza
rafael.souza@email.com | +55-11-555-0195 | São Paulo, Brazil

SUMMARY
Data privacy lawyer and compliance specialist with 4 years of experience implementing GDPR, LGPD, and CCPA compliance programs for multinational technology companies.

EXPERIENCE
Data Privacy Counsel | iFood | 03/2022 - Present
- Developed LGPD/GDPR compliance framework covering 45M user records
- Conducted DPIAs, managed data subject requests (DSARs)
- Negotiated data processing agreements (DPAs) with 200+ vendors

Privacy Analyst | PwC Brazil | 01/2020 - 02/2022
- Supported GDPR compliance gap analyses for financial sector clients
- Developed privacy policies and cookie consent mechanisms

EDUCATION
Bachelor of Law | Universidade de São Paulo | 2019

SKILLS
Data Privacy, GDPR, CCPA, Regulatory Compliance, Legal Research, Legal Writing, Compliance, Contract Drafting"""
    },
    {
        "name": "Mei-Ling Chang",
        "email": "meiling.chang@email.com",
        "phone": "+886-2-555-0196",
        "education": "Master",
        "experience_years": 6.0,
        "category": "Legal",
        "skills": ["intellectual property", "patent law", "trademark", "copyright", "contract drafting", "legal research", "licensing", "compliance"],
        "raw_text": """Mei-Ling Chang
meiling.chang@email.com | +886-2-555-0196 | Taipei, Taiwan

SUMMARY
IP attorney with 6 years of experience in patent prosecution, trademark portfolio management, and technology licensing for semiconductor and electronics companies.

EXPERIENCE
Senior IP Counsel | TSMC | 06/2020 - Present
- Manage 2,000+ patent portfolio; prosecute US, EP, CN, JP applications
- Negotiate and draft technology licensing agreements
- Conduct freedom-to-operate (FTO) analyses for new product launches

IP Associate | Perkins Coie LLP | 08/2018 - 05/2020
- Drafted patent applications for semiconductor process innovations
- Managed trademark registrations across 30 jurisdictions

EDUCATION
LLM Intellectual Property | University of California Berkeley | 2018
BSc Electrical Engineering | National Taiwan University | 2015

SKILLS
Intellectual Property, Patent Law, Trademark, Copyright, Contract Drafting, Legal Research, Licensing"""
    },
    # ── ENGINEERING ───────────────────────────────────────────────────────────
    {
        "name": "Henrik Larsson",
        "email": "henrik.larsson@email.com",
        "phone": "+46-8-555-0197",
        "education": "Master",
        "experience_years": 9.0,
        "category": "Mechanical Engineering",
        "skills": ["solidworks", "catia", "finite element analysis", "ansys", "mechanical design", "autocad", "lean manufacturing", "fmea", "quality management"],
        "raw_text": """Henrik Larsson
henrik.larsson@email.com | +46-8-555-0197 | Stockholm, Sweden

SUMMARY
Lead mechanical design engineer with 9 years of experience in automotive and heavy machinery sectors. Expert in SolidWorks, CATIA, and ANSYS FEA with track record of delivering cost-optimized designs.

EXPERIENCE
Lead Mechanical Engineer | Volvo Cars | 03/2019 - Present
- Lead structural design of BEV battery enclosures (SolidWorks, CATIA V5)
- Perform non-linear FEA crash and durability simulations in ANSYS
- Chair FMEA workshops and drive DFMEA/PFMEA closure

Mechanical Design Engineer | SKF | 08/2015 - 02/2019
- Designed precision bearing assemblies for aerospace applications
- Applied GD&T and tolerance stack-up analysis

EDUCATION
MSc Mechanical Engineering | KTH Royal Institute of Technology | 2015
BSc Mechanical Engineering | Chalmers University | 2013

SKILLS
SolidWorks, CATIA, Finite Element Analysis, ANSYS, Mechanical Design, AutoCAD, Lean Manufacturing, FMEA, Quality Management, ISO 9001"""
    },
    {
        "name": "Amara Diallo",
        "email": "amara.diallo@email.com",
        "phone": "+33-1-555-0198",
        "education": "Bachelor",
        "experience_years": 5.0,
        "category": "Civil Engineering",
        "skills": ["civil engineering", "structural analysis", "autocad", "revit", "bim", "construction management", "project scheduling", "ms project"],
        "raw_text": """Amara Diallo
amara.diallo@email.com | +33-1-555-0198 | Paris, France

SUMMARY
Structural engineer with 5 years of experience designing commercial and infrastructure projects in France and Sub-Saharan Africa. Proficient in AutoCAD, Revit, and structural analysis software.

EXPERIENCE
Structural Engineer | Bouygues Construction | 09/2021 - Present
- Design reinforced concrete and steel structures for commercial buildings
- Develop Revit BIM models and coordinate with MEP, architectural teams
- Prepare structural calculations per Eurocode standards

Junior Structural Engineer | Egis | 07/2019 - 08/2021
- Supported design of bridge infrastructure in Senegal and Ivory Coast
- Prepared AutoCAD drawings and construction specifications

EDUCATION
Bachelor of Civil Engineering | École des Ponts ParisTech | 2019

SKILLS
Civil Engineering, Structural Analysis, AutoCAD, Revit, BIM, Construction Management, Project Scheduling, MS Project, Eurocode"""
    },
    {
        "name": "Sanjay Patel",
        "email": "sanjay.patel@email.com",
        "phone": "+91-98-555-0199",
        "education": "Bachelor",
        "experience_years": 7.0,
        "category": "Electrical Engineering",
        "skills": ["electrical engineering", "plc programming", "scada", "instrumentation", "control systems", "autocad", "quality management", "lean manufacturing"],
        "raw_text": """Sanjay Patel
sanjay.patel@email.com | +91-98-555-0199 | Mumbai, India

SUMMARY
Electrical & instrumentation engineer with 7 years in oil & gas and chemical process industries. Expert in PLC/DCS programming, SCADA implementation, and functional safety (SIL).

EXPERIENCE
E&I Senior Engineer | Reliance Industries | 04/2020 - Present
- Design instrument loop diagrams, cause-and-effect matrices, and P&IDs
- Program Siemens S7-1500 PLCs and Honeywell DCS systems
- Implement SCADA (WinCC) for refinery process monitoring

E&I Engineer | Larsen & Toubro | 06/2017 - 03/2020
- Supported EPC projects in petrochemical sector
- Performed functional safety assessments per IEC 61511

EDUCATION
Bachelor of Electrical Engineering | IIT Bombay | 2017

SKILLS
Electrical Engineering, PLC Programming, SCADA, Instrumentation, Control Systems, AutoCAD, Quality Management, Lean Manufacturing, Functional Safety"""
    },
    {
        "name": "Laura Bianchi",
        "email": "laura.bianchi@email.com",
        "phone": "+39-02-555-0200",
        "education": "Master",
        "experience_years": 6.0,
        "category": "Manufacturing Engineering",
        "skills": ["lean manufacturing", "six sigma", "quality management", "fmea", "root cause analysis", "process improvement", "autocad", "iso 9001"],
        "raw_text": """Laura Bianchi
laura.bianchi@email.com | +39-02-555-0200 | Turin, Italy

SUMMARY
Lean Six Sigma Black Belt with 6 years of experience driving process improvement in automotive manufacturing. Achieved €8M cost savings through waste elimination and quality initiatives.

EXPERIENCE
Lean Manufacturing Manager | Ferrari S.p.A. | 01/2022 - Present
- Lead Kaizen events and VSM across 5 production lines
- Implement SPC (Statistical Process Control) reducing defect rate by 40%
- Lead IATF 16949 audit preparation and supplier quality audits

Process Engineer | FCA (Stellantis) | 06/2018 - 12/2021
- Applied FMEA, root cause analysis (8D, Ishikawa) on assembly defects
- Implemented 5S and Visual Management standards

EDUCATION
MSc Industrial Engineering | Politecnico di Milano | 2018
BSc Mechanical Engineering | Università di Bologna | 2016

SKILLS
Lean Manufacturing, Six Sigma, Quality Management, FMEA, Root Cause Analysis, Process Improvement, AutoCAD, ISO 9001, IATF 16949"""
    },
    # ── HUMAN RESOURCES ──────────────────────────────────────────────────────
    {
        "name": "Sarah Okonkwo",
        "email": "sarah.okonkwo@email.com",
        "phone": "+44-20-555-0201",
        "education": "Master",
        "experience_years": 7.0,
        "category": "Human Resources",
        "skills": ["talent acquisition", "performance management", "employee relations", "change management", "hr analytics", "workday", "employment law", "organizational development"],
        "raw_text": """Sarah Okonkwo
sarah.okonkwo@email.com | +44-20-555-0201 | London, UK

SUMMARY
Strategic HR Business Partner with 7 years of experience partnering with senior leadership in financial services and technology sectors. CIPD Level 7 qualified.

EXPERIENCE
Senior HR Business Partner | Barclays | 09/2020 - Present
- Partner with 3 business units (1,500 employees) on all people matters
- Lead organizational design and restructuring programmes
- Manage complex employee relations cases and employment tribunal risk
- Drive talent management, succession planning, and diversity & inclusion

HR Business Partner | EY | 06/2017 - 08/2020
- Supported 5 service lines through Workday implementation
- Managed performance management cycles and year-end compensation reviews

EDUCATION
MSc Human Resource Management | London School of Economics | 2017
BA Psychology | University of Birmingham | 2015

SKILLS
Talent Acquisition, Performance Management, Employee Relations, Change Management, HR Analytics, Workday, Employment Law, Organizational Development, Succession Planning, Diversity & Inclusion"""
    },
    {
        "name": "Daniel Kim",
        "email": "daniel.kim@email.com",
        "phone": "+1-415-555-0202",
        "education": "Bachelor",
        "experience_years": 4.0,
        "category": "Human Resources",
        "skills": ["talent acquisition", "recruitment", "linkedin recruiter", "sourcing", "hris", "hr analytics", "onboarding", "stakeholder management"],
        "raw_text": """Daniel Kim
daniel.kim@email.com | +1-415-555-0202 | San Francisco, CA

SUMMARY
Talent acquisition professional with 4 years of experience recruiting technical and business talent for high-growth technology startups and Fortune 500 companies.

EXPERIENCE
Senior Talent Acquisition Partner | Stripe | 01/2023 - Present
- Full-cycle recruitment for engineering, product, and go-to-market roles
- Source passive candidates using LinkedIn Recruiter and Boolean search
- Manage recruiting process in Greenhouse ATS; report on TTF and cost-per-hire

Recruiter | LinkedIn | 07/2020 - 12/2022
- Hired 200+ candidates across EMEA and APAC regions
- Partnered with HRBPs on workforce planning and talent pipeline development

EDUCATION
Bachelor of Psychology | UC San Diego | 2020

SKILLS
Talent Acquisition, Recruitment, LinkedIn Recruiter, Sourcing, HRIS, HR Analytics, Onboarding, Stakeholder Management, Greenhouse"""
    },
    {
        "name": "Charlotte Dubois",
        "email": "charlotte.dubois@email.com",
        "phone": "+33-1-555-0203",
        "education": "Master",
        "experience_years": 5.0,
        "category": "Human Resources",
        "skills": ["learning & development", "instructional design", "e-learning", "articulate storyline", "lms", "moodle", "training delivery", "content creation", "facilitation", "hr analytics"],
        "raw_text": """Charlotte Dubois
charlotte.dubois@email.com | +33-1-555-0203 | Paris, France

SUMMARY
Learning & Development specialist with 5 years designing impactful digital and blended learning experiences for global organisations. Certified in Kirkpatrick Evaluation and Articulate Storyline.

EXPERIENCE
L&D Specialist | L'Oréal | 04/2022 - Present
- Design leadership development programs for 500+ managers globally
- Build SCORM-compliant e-learning in Articulate Storyline and Rise
- Administer Cornerstone OnDemand LMS; track completion and ROI

L&D Coordinator | BNP Paribas | 09/2019 - 03/2022
- Facilitated soft skills workshops (communication, negotiation, leadership)
- Migrated legacy training content to Moodle LMS

EDUCATION
MSc Organizational Psychology | Sciences Po Paris | 2019
BA Human Resources | Université Paris-Dauphine | 2017

SKILLS
Learning & Development, Instructional Design, E-Learning, Articulate Storyline, LMS, Moodle, Training Delivery, Content Creation, Facilitation, HR Analytics, Adult Learning Theory"""
    },
    # ── SUPPLY CHAIN ──────────────────────────────────────────────────────────
    {
        "name": "Ahmed Hassan",
        "email": "ahmed.hassan@email.com",
        "phone": "+20-2-555-0204",
        "education": "Bachelor",
        "experience_years": 5.0,
        "category": "Supply Chain",
        "skills": ["supply chain management", "demand planning", "s&op", "inventory management", "sap scm", "sql", "excel", "data analysis", "procurement"],
        "raw_text": """Ahmed Hassan
ahmed.hassan@email.com | +20-2-555-0204 | Cairo, Egypt

SUMMARY
Supply chain analyst with 5 years of experience optimising demand planning, inventory, and procurement processes for FMCG companies across MENA.

EXPERIENCE
Supply Chain Analyst | Unilever Egypt | 06/2021 - Present
- Lead S&OP process for 3 product categories (€200M revenue)
- Build demand forecasting models reducing forecast error by 18%
- Manage SAP SCM modules (MM, SD, PP) and data quality

Supply Planner | Nestlé | 07/2019 - 05/2021
- Managed finished goods inventory for 150 SKUs
- Conducted root cause analysis on service failures

EDUCATION
Bachelor of Industrial Engineering | Cairo University | 2019

SKILLS
Supply Chain Management, Demand Planning, S&OP, Inventory Management, SAP SCM, SQL, Excel, Data Analysis, Procurement"""
    },
    {
        "name": "Anna Kowalski",
        "email": "anna.kowalski@email.com",
        "phone": "+48-22-555-0205",
        "education": "Master",
        "experience_years": 8.0,
        "category": "Supply Chain",
        "skills": ["procurement", "strategic sourcing", "vendor management", "category management", "contract negotiation", "sap", "rfq", "supply chain management", "compliance"],
        "raw_text": """Anna Kowalski
anna.kowalski@email.com | +48-22-555-0205 | Warsaw, Poland

SUMMARY
Procurement director with 8 years of experience building strategic sourcing functions for manufacturing and FMCG companies in CEE. Expert in category management and cost optimisation.

EXPERIENCE
Procurement Manager | KGHM Polska Miedź | 03/2019 - Present
- Lead indirect procurement for $150M annual spend across 12 categories
- Deliver 8-12% cost savings annually through strategic sourcing and negotiation
- Manage SAP MM module; oversee 500+ vendor relationships

Senior Buyer | Henkel | 06/2016 - 02/2019
- Managed MRO and packaging category procurement
- Conducted RFQ/RFP processes and supplier development programs

EDUCATION
MSc Supply Chain Management | SGH Warsaw School of Economics | 2016
BSc Economics | University of Warsaw | 2014

SKILLS
Procurement, Strategic Sourcing, Vendor Management, Category Management, Contract Negotiation, SAP, RFQ, Supply Chain Management, Compliance"""
    },
    {
        "name": "Lucas Ferreira",
        "email": "lucas.ferreira@email.com",
        "phone": "+55-21-555-0206",
        "education": "Bachelor",
        "experience_years": 6.0,
        "category": "Supply Chain",
        "skills": ["logistics", "warehousing", "inventory management", "3pl", "import/export", "customs", "supply chain management", "vendor management", "lean manufacturing"],
        "raw_text": """Lucas Ferreira
lucas.ferreira@email.com | +55-21-555-0206 | Rio de Janeiro, Brazil

SUMMARY
Logistics manager with 6 years of experience managing complex distribution networks and 3PL partnerships in Brazil and Latin America. Expert in import/export compliance and warehouse management.

EXPERIENCE
Logistics Manager | Magazine Luiza | 08/2020 - Present
- Manage 4 distribution centers (2M+ daily shipments)
- Oversee 3PL contracts totaling R$120M annually
- Implement WMS (Manhattan Associates) improving pick accuracy to 99.8%

Import/Export Coordinator | Embraer | 03/2018 - 07/2020
- Manage import/export compliance for aerospace components across 30 countries
- Handle customs documentation, Incoterms, and freight forwarding partnerships

EDUCATION
Bachelor of Logistics Engineering | PUC-Rio | 2018

SKILLS
Logistics, Warehousing, Inventory Management, 3PL, Import/Export, Customs, Supply Chain Management, Vendor Management, Lean Manufacturing"""
    },
    # ── SALES & BUSINESS DEVELOPMENT ──────────────────────────────────────────
    {
        "name": "James Harrington",
        "email": "james.harrington@email.com",
        "phone": "+1-646-555-0207",
        "education": "Bachelor",
        "experience_years": 10.0,
        "category": "Sales",
        "skills": ["b2b sales", "enterprise sales", "sales management", "salesforce", "pipeline management", "negotiation", "sales forecasting", "crm", "leadership"],
        "raw_text": """James Harrington
james.harrington@email.com | +1-646-555-0207 | New York, NY

SUMMARY
Enterprise sales leader with 10 years of experience building and scaling B2B SaaS sales teams. Consistent track record of exceeding $15M+ annual quotas and developing high-performing teams.

EXPERIENCE
VP of Sales | Salesforce | 07/2020 - Present
- Lead team of 25 enterprise AEs covering Fortune 1000 accounts
- Exceed annual quota of $40M ARR by 115% for 3 consecutive years
- Manage complex sales cycles (6-18 months) with C-suite stakeholders

Enterprise Account Executive | HubSpot | 01/2016 - 06/2020
- Closed $3.2M in new ARR; Top 5% performer nationally
- Built territory from ground up; managed 80-account portfolio

EDUCATION
Bachelor of Business Administration | University of Michigan | 2014

SKILLS
B2B Sales, Enterprise Sales, Sales Management, Salesforce, Pipeline Management, Negotiation, Sales Forecasting, CRM, Leadership, Revenue Operations"""
    },
    {
        "name": "Ingrid Svensson",
        "email": "ingrid.svensson@email.com",
        "phone": "+46-8-555-0208",
        "education": "Bachelor",
        "experience_years": 5.0,
        "category": "Sales",
        "skills": ["business development", "b2b sales", "market research", "negotiation", "crm", "strategic planning", "stakeholder management", "salesforce", "partnership development"],
        "raw_text": """Ingrid Svensson
ingrid.svensson@email.com | +46-8-555-0208 | Stockholm, Sweden

SUMMARY
Business development professional with 5 years of experience building strategic partnerships and new revenue channels for Nordic tech companies expanding globally.

EXPERIENCE
Business Development Manager | Klarna | 01/2022 - Present
- Close 30+ merchant partnerships per year (banks, e-commerce platforms, retail)
- Build go-to-market strategy for DACH and UK market expansion
- Manage partner pipeline in Salesforce; negotiate commercial agreements

Business Development Lead | iZettle (PayPal) | 06/2019 - 12/2021
- Developed channel partner ecosystem across Nordics
- Conducted market research and competitive analysis

EDUCATION
Bachelor of International Business | Stockholm School of Economics | 2019

SKILLS
Business Development, B2B Sales, Market Research, Negotiation, CRM, Strategic Planning, Stakeholder Management, Salesforce, Partnership Development"""
    },
    {
        "name": "Priya Krishnamurthy",
        "email": "priya.krishnamurthy@email.com",
        "phone": "+1-415-555-0209",
        "education": "Bachelor",
        "experience_years": 4.0,
        "category": "Sales",
        "skills": ["customer success", "account management", "salesforce", "crm", "upselling", "stakeholder management", "client relationship management", "data analysis"],
        "raw_text": """Priya Krishnamurthy
priya.krishnamurthy@email.com | +1-415-555-0209 | San Francisco, CA

SUMMARY
Customer Success Manager with 4 years of experience driving adoption, retention, and expansion for enterprise SaaS accounts. Expert in building executive relationships and quantifying value delivered.

EXPERIENCE
Senior Customer Success Manager | Snowflake | 03/2022 - Present
- Own portfolio of 15 enterprise accounts ($8M ARR)
- Drive NPS from 42 to 71 through structured success programs and QBRs
- Identify upsell/cross-sell opportunities; closed $2.1M expansion in FY24

Customer Success Manager | Zendesk | 07/2020 - 02/2022
- Managed onboarding for 40 mid-market accounts
- Maintained 96% gross retention rate

EDUCATION
Bachelor of Business Administration | UC Berkeley | 2020

SKILLS
Customer Success, Account Management, Salesforce, CRM, Upselling, Stakeholder Management, Client Relationship Management, Data Analysis"""
    },
    # ── EDUCATION & TRAINING ──────────────────────────────────────────────────
    {
        "name": "Rachel Foster",
        "email": "rachel.foster@email.com",
        "phone": "+1-512-555-0210",
        "education": "Master",
        "experience_years": 6.0,
        "category": "Education",
        "skills": ["instructional design", "e-learning", "articulate storyline", "scorm", "lms", "moodle", "curriculum development", "adult learning theory", "content creation", "facilitation"],
        "raw_text": """Rachel Foster
rachel.foster@email.com | +1-512-555-0210 | Austin, TX

SUMMARY
Instructional designer with 6 years of experience creating award-winning e-learning and blended learning solutions for Fortune 500 corporate training programs.

EXPERIENCE
Senior Instructional Designer | Dell Technologies | 04/2021 - Present
- Design SCORM-compliant courses in Articulate Storyline 360 and Rise
- Manage learning content in Cornerstone LMS for 100K+ employees globally
- Apply ADDIE and SAM methodologies; consult with SMEs on content accuracy

Instructional Designer | Indeed | 06/2018 - 03/2021
- Built onboarding curriculum reducing time-to-productivity by 35%
- Created microlearning video modules using Camtasia

EDUCATION
MSc Instructional Technology | University of Texas at Austin | 2018
BA English | Baylor University | 2016

SKILLS
Instructional Design, E-Learning, Articulate Storyline, SCORM, LMS, Moodle, Curriculum Development, Adult Learning Theory, Content Creation, Facilitation, ADDIE"""
    },
    {
        "name": "Michael Adeyemi",
        "email": "michael.adeyemi@email.com",
        "phone": "+234-80-555-0211",
        "education": "Master",
        "experience_years": 8.0,
        "category": "Education",
        "skills": ["training delivery", "learning & development", "instructional design", "lms", "facilitation", "coaching", "stakeholder management", "hr analytics", "curriculum development"],
        "raw_text": """Michael Adeyemi
michael.adeyemi@email.com | +234-80-555-0211 | Abuja, Nigeria

SUMMARY
Learning & Development leader with 8 years of experience building corporate universities and talent development functions in banking and telecommunications sectors.

EXPERIENCE
Head of L&D | Zenith Bank | 01/2020 - Present
- Lead team of 12 trainers and instructional designers
- Design leadership academy programs for 300+ senior managers
- Manage SuccessFactors LMS for 8,000 employees; track ROI using Kirkpatrick
- Partner with C-suite on succession planning and high-potential development

L&D Manager | MTN Nigeria | 04/2016 - 12/2019
- Designed and delivered technical and soft skills curriculum
- Implemented Moodle LMS reducing training costs by 30%

EDUCATION
MSc Human Resource Development | University of Ibadan | 2016
BSc Education | University of Lagos | 2013

SKILLS
Training Delivery, Learning & Development, Instructional Design, LMS, Moodle, Facilitation, Coaching, Stakeholder Management, HR Analytics, Curriculum Development"""
    },
]


def main():
    # Load existing data
    jobs_path = os.path.join(DATA_DIR, "jobs.json")
    resumes_path = os.path.join(DATA_DIR, "resumes.json")

    with open(jobs_path, encoding="utf-8") as f:
        existing_jobs = json.load(f)

    with open(resumes_path, encoding="utf-8") as f:
        existing_resumes = json.load(f)

    existing_job_titles = {j["title"] for j in existing_jobs}
    existing_candidate_emails = {r["email"] for r in existing_resumes}

    # Merge new jobs (skip duplicates)
    added_jobs = 0
    for job in NEW_JOBS:
        if job["title"] not in existing_job_titles:
            existing_jobs.append(job)
            existing_job_titles.add(job["title"])
            added_jobs += 1

    # Merge new candidates (skip duplicates)
    added_candidates = 0
    for cand in NEW_CANDIDATES:
        if cand["email"] not in existing_candidate_emails:
            existing_resumes.append(cand)
            existing_candidate_emails.add(cand["email"])
            added_candidates += 1

    # Write back
    with open(jobs_path, "w", encoding="utf-8") as f:
        json.dump(existing_jobs, f, indent=2, ensure_ascii=False)

    with open(resumes_path, "w", encoding="utf-8") as f:
        json.dump(existing_resumes, f, indent=2, ensure_ascii=False)

    print(f"✅ Added {added_jobs} new job postings (total: {len(existing_jobs)})")
    print(f"✅ Added {added_candidates} new candidates (total: {len(existing_resumes)})")


if __name__ == "__main__":
    main()
