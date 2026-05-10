"""
Seed junior/intern job postings and 80+ diverse candidates.

Run from: /Users/samet/Desktop/datawarehouse/backend/
  source venv/bin/activate && python seed_junior_jobs_and_candidates.py
"""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")

from app.database import init_db, SessionLocal, JobPosting, Candidate, Skill

init_db()

# ── Junior / Intern Job Postings ──────────────────────────────────────────────
JUNIOR_JOBS = [
    {
        "title": "Junior Frontend Developer",
        "description": "Join our product team as a junior frontend developer. You will build React components, implement responsive UI designs, write clean HTML/CSS, and collaborate with designers. Basic JavaScript and React knowledge required. No prior professional experience needed — strong portfolio or personal projects are highly valued.",
        "required_skills": ["javascript", "react", "html", "css", "git"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Junior Backend Developer",
        "description": "We are looking for a junior backend developer to join our engineering team. You will build REST APIs, work with databases, and contribute to Python or Node.js backend services. Basic understanding of HTTP, SQL, and version control required. Bootcamp graduates and self-taught developers welcome.",
        "required_skills": ["python", "sql", "rest api", "git", "node.js"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Junior Full Stack Developer",
        "description": "Entry-level full stack role working on React frontend and Node.js or Python backend. You will contribute to features end-to-end, write unit tests, and participate in code reviews. Skills in JavaScript, React, and any backend language required.",
        "required_skills": ["javascript", "react", "node.js", "sql", "git", "html", "css"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Software Developer Intern",
        "description": "6-month paid internship for students or recent graduates. You will work alongside senior developers on real product features, participate in agile ceremonies, and ship code to production. We accept candidates from any background — curiosity and a willingness to learn matter most.",
        "required_skills": ["python", "javascript", "git", "api"],
        "min_experience": 0.0,
        "education_level": "High School",
    },
    {
        "title": "Junior Java Developer",
        "description": "We need a junior Java developer to contribute to our enterprise backend services. You will work with Spring Boot, write unit tests (JUnit), and interact with SQL databases. Basic Java, OOP, and SQL knowledge required. C# experience is also welcome.",
        "required_skills": ["java", "sql", "git", "oop", "api"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Junior React Developer",
        "description": "Build modern web UIs with React and TypeScript. You will implement designs from Figma, manage state with hooks and context, and integrate REST APIs. Good understanding of JavaScript ES6+, React, and CSS required.",
        "required_skills": ["react", "javascript", "typescript", "css", "git", "html"],
        "min_experience": 1.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Junior Data Analyst",
        "description": "Entry-level data analyst position on our business intelligence team. You will write SQL queries, create dashboards in Power BI or Tableau, and support reporting needs. Excel proficiency and basic SQL required.",
        "required_skills": ["sql", "excel", "data analysis", "python"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Junior DevOps / Cloud Intern",
        "description": "Intern role focused on CI/CD pipelines, cloud infrastructure (AWS or GCP), and automation scripting. You will assist senior engineers in maintaining deployments, writing bash/Python scripts, and managing GitHub Actions workflows.",
        "required_skills": ["ci/cd", "git", "python", "linux", "docker"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "QA Engineer Intern",
        "description": "Internship on our quality assurance team. You will write test cases, execute manual and automated tests, report bugs, and contribute to our Selenium or Cypress test suite. Basic programming and analytical thinking required.",
        "required_skills": ["javascript", "python", "git", "api", "sql"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Junior C# / .NET Developer",
        "description": "Entry-level .NET developer to work on our Windows desktop and web applications. You will build features in C#, work with SQL Server, and contribute to ASP.NET APIs. Good understanding of C#, OOP principles, and SQL required.",
        "required_skills": ["c#", "sql", "oop", "git", "api", ".net"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Junior Mobile Developer (React Native)",
        "description": "Build cross-platform mobile apps with React Native. You will implement screens from design specs, integrate REST APIs, and test on iOS and Android simulators. React, JavaScript, and basic mobile concepts required.",
        "required_skills": ["react", "javascript", "node.js", "git", "api"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
    {
        "title": "Data Science Intern",
        "description": "Work with our data science team on machine learning experiments, data cleaning, and model evaluation. You will use Python, pandas, scikit-learn, and Jupyter notebooks. Strong Python and math/statistics fundamentals required.",
        "required_skills": ["python", "sql", "data analysis", "statistics", "git"],
        "min_experience": 0.0,
        "education_level": "Bachelor",
    },
]

# ── 80+ Diverse Candidates ────────────────────────────────────────────────────
# Spread across: tech (frontend/backend/mobile/data), sales, hr, finance, engineering
# Skill coverage: 0-15 skills, experience: 0-10 years
DIVERSE_CANDIDATES = [
    # ── TECH — 0-1 year (students / bootcamp grads) ──────────────────────────
    {
        "name": "Ali Demirci", "email": "ali.demirci@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["javascript", "react", "html", "css", "git"],
        "raw_text": "Ali Demirci | Computer Engineering student | 0 years. "
                    "Built personal portfolio with React and CSS. GitHub active. Bootcamp graduate."
    },
    {
        "name": "Zeynep Arslan", "email": "zeynep.arslan@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["python", "sql", "data analysis", "excel", "git"],
        "raw_text": "Zeynep Arslan | Statistics graduate | 0 years. "
                    "Pandas, Matplotlib, SQL projects. Kaggle competitions. Python data analysis."
    },
    {
        "name": "Emirhan Yıldız", "email": "emirhan.yildiz@email.com", "education": "High School",
        "experience_years": 0.0,
        "skills": ["java", "python", "git", "api", "sql"],
        "raw_text": "Emirhan Yıldız | Self-taught developer | High school graduate. "
                    "Java Spring Boot tutorial projects, Python scripts, REST API basics. GitHub portfolio."
    },
    {
        "name": "Selin Özdemir", "email": "selin.ozdemir@email.com", "education": "Bachelor",
        "experience_years": 0.5,
        "skills": ["react", "javascript", "typescript", "html", "css", "git"],
        "raw_text": "Selin Özdemir | Web Development bootcamp | 6 months internship. "
                    "React hooks, TypeScript basics, responsive CSS. Deployed 2 personal projects."
    },
    {
        "name": "Burak Koç", "email": "burak.koc@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["c#", "java", "sql", "oop", "git"],
        "raw_text": "Burak Koç | Computer Science student | University projects in C# and Java. "
                    "OOP principles, SQL databases, GitHub version control. Final year project in ASP.NET."
    },
    {
        "name": "Naz Şahin", "email": "naz.sahin@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["python", "javascript", "git", "html", "css"],
        "raw_text": "Naz Şahin | Computer Science grad | Personal web projects. "
                    "Django REST backend, JavaScript frontend. Seeking first job."
    },
    {
        "name": "Mert Aydın", "email": "mert.aydin@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["react", "javascript", "node.js", "git", "api", "css", "html"],
        "raw_text": "Mert Aydın | 1 year | Frontend developer at startup. "
                    "React SPA development, Node.js microservices, REST API integration."
    },
    {
        "name": "Deniz Polat", "email": "deniz.polat@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["c#", ".net", "sql", "oop", "git", "api"],
        "raw_text": "Deniz Polat | .NET developer student | University C# projects. "
                    "ASP.NET Core basics, SQL Server, OOP design patterns."
    },
    {
        "name": "Cansu Kaya", "email": "cansu.kaya@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["python", "data analysis", "statistics", "sql", "jupyter"],
        "raw_text": "Cansu Kaya | Statistics graduate | Data science bootcamp. "
                    "Python pandas, statistical modeling, Jupyter notebooks, SQL basics."
    },
    {
        "name": "Furkan Çelik", "email": "furkan.celik@email.com", "education": "Bachelor",
        "experience_years": 0.5,
        "skills": ["java", "c#", "oop", "sql", "git", "api"],
        "raw_text": "Furkan Çelik | 6 months internship | Backend intern at fintech. "
                    "Java Spring, C# basics, OOP, SQL queries. Strong academics."
    },
    # ── TECH — 1-3 years (junior developers) ─────────────────────────────────
    {
        "name": "Oğuz Turhan", "email": "oguz.turhan@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["javascript", "react", "typescript", "node.js", "css", "git", "docker", "sql"],
        "raw_text": "Oğuz Turhan | 2 years | Full stack developer. "
                    "React + TypeScript frontend, Node.js APIs, PostgreSQL, Docker containers."
    },
    {
        "name": "İpek Güneş", "email": "ipek.gunes@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["python", "django", "sql", "rest api", "docker", "git", "javascript"],
        "raw_text": "İpek Güneş | 2 years | Python backend developer. "
                    "Django REST Framework, PostgreSQL, Docker, Redis. API design and documentation."
    },
    {
        "name": "Sercan Demir", "email": "sercan.demir@email.com", "education": "Bachelor",
        "experience_years": 1.5,
        "skills": ["react", "javascript", "html", "css", "git", "figma"],
        "raw_text": "Sercan Demir | 1.5 years | Frontend developer. "
                    "React, CSS animations, Figma-to-code. No backend experience."
    },
    {
        "name": "Büşra Aktaş", "email": "busra.aktas@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["java", "spring boot", "sql", "oop", "api", "git", "docker", "microservices"],
        "raw_text": "Büşra Aktaş | 3 years | Java backend developer. "
                    "Spring Boot microservices, MySQL, Docker, JUnit testing. REST API design."
    },
    {
        "name": "Görkem Yılmaz", "email": "gorkem.yilmaz@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["python", "machine learning", "sql", "pandas", "scikit-learn", "git"],
        "raw_text": "Görkem Yılmaz | 2 years | Junior ML engineer. "
                    "scikit-learn models, pandas pipelines, SQL feature engineering. Kaggle silver."
    },
    {
        "name": "Tuba Yıldırım", "email": "tuba.yildirim@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["c#", ".net", "sql", "oop", "git", "api", "azure"],
        "raw_text": "Tuba Yıldırım | 1 year | Junior .NET developer. "
                    "ASP.NET Core APIs, SQL Server, Azure deployment basics."
    },
    {
        "name": "Kerem Şimşek", "email": "kerem.simsek@email.com", "education": "Bachelor",
        "experience_years": 2.5,
        "skills": ["node.js", "javascript", "mongodb", "rest api", "docker", "git", "redis"],
        "raw_text": "Kerem Şimşek | 2.5 years | Node.js backend developer. "
                    "Express.js APIs, MongoDB, Redis caching, Docker. Event-driven architecture."
    },
    {
        "name": "Ayla Demir", "email": "ayla.demir@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["react", "javascript", "typescript", "css", "html", "git", "api"],
        "raw_text": "Ayla Demir | 1 year | React developer at agency. "
                    "TypeScript + React, REST API consumption, responsive UI."
    },
    {
        "name": "Onur Kılıç", "email": "onur.kilic@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["python", "fastapi", "sql", "docker", "git", "rest api", "postgresql"],
        "raw_text": "Onur Kılıç | 2 years | Python API developer. "
                    "FastAPI, PostgreSQL, SQLAlchemy, Docker, pytest. Async Python."
    },
    {
        "name": "Merve Çiftçi", "email": "merve.ciftci@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["javascript", "react", "node.js", "typescript", "sql", "git", "aws", "docker", "css", "html"],
        "raw_text": "Merve Çiftçi | 3 years | Full stack developer at SaaS company. "
                    "React + TypeScript frontend, Node.js microservices, PostgreSQL, AWS deployment."
    },
    # ── TECH — 3-6 years (mid-senior) ────────────────────────────────────────
    {
        "name": "Tolga Erdoğan", "email": "tolga.erdogan@email.com", "education": "Bachelor",
        "experience_years": 5.0,
        "skills": ["python", "fastapi", "django", "sql", "postgresql", "docker", "kubernetes",
                   "aws", "redis", "celery", "rest api", "microservices"],
        "raw_text": "Tolga Erdoğan | 5 years | Senior Python engineer. "
                    "FastAPI and Django microservices, PostgreSQL, Kubernetes, AWS EKS. "
                    "Led backend architecture for 500K+ user platform."
    },
    {
        "name": "Elif Yılmaz", "email": "elif.yilmaz@email.com", "education": "Master",
        "experience_years": 4.0,
        "skills": ["machine learning", "python", "tensorflow", "pytorch", "sql", "docker",
                   "kubernetes", "mlops", "data analysis", "deep learning"],
        "raw_text": "Elif Yılmaz | MSc AI | 4 years | ML engineer at tech unicorn. "
                    "Production ML pipelines, TensorFlow/PyTorch, MLOps with Kubeflow. "
                    "Computer vision and NLP projects."
    },
    {
        "name": "Cem Korkmaz", "email": "cem.korkmaz@email.com", "education": "Bachelor",
        "experience_years": 6.0,
        "skills": ["javascript", "typescript", "react", "node.js", "graphql", "postgresql",
                   "redis", "docker", "aws", "microservices", "ci/cd", "git"],
        "raw_text": "Cem Korkmaz | 6 years | Staff frontend/full stack engineer. "
                    "React + TypeScript at scale, GraphQL APIs, AWS, CI/CD pipelines."
    },
    {
        "name": "Pınar Kaya", "email": "pinar.kaya@email.com", "education": "Bachelor",
        "experience_years": 4.0,
        "skills": ["java", "spring boot", "microservices", "sql", "kafka", "docker",
                   "kubernetes", "api", "git", "oop"],
        "raw_text": "Pınar Kaya | 4 years | Java microservices engineer. "
                    "Spring Boot, Kafka event streaming, Kubernetes, PostgreSQL. "
                    "Domain-driven design and clean architecture."
    },
    {
        "name": "Hasan Aksoy", "email": "hasan.aksoy@email.com", "education": "Bachelor",
        "experience_years": 5.0,
        "skills": ["devops", "kubernetes", "docker", "ci/cd", "aws", "terraform",
                   "linux", "python", "git", "monitoring", "bash"],
        "raw_text": "Hasan Aksoy | 5 years | DevOps/SRE engineer. "
                    "Kubernetes cluster management, Terraform IaC, AWS, GitHub Actions CI/CD. "
                    "99.9% uptime SLA delivery."
    },
    # ── DATA SCIENCE / ML ─────────────────────────────────────────────────────
    {
        "name": "Eda Koç", "email": "eda.koc@email.com", "education": "Master",
        "experience_years": 3.0,
        "skills": ["python", "machine learning", "sql", "pandas", "numpy", "scikit-learn",
                   "data analysis", "statistics", "tableau"],
        "raw_text": "Eda Koç | MSc Data Science | 3 years | Data scientist at e-commerce company. "
                    "Recommendation systems, A/B testing, pandas/scikit-learn pipelines, Tableau dashboards."
    },
    {
        "name": "Barış Kılıç", "email": "baris.kilic@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["python", "sql", "excel", "data analysis", "power bi", "statistics"],
        "raw_text": "Barış Kılıç | 2 years | Business intelligence analyst. "
                    "Power BI dashboards, SQL queries, Python for data manipulation. "
                    "No ML experience yet."
    },
    {
        "name": "Şeyma Doğan", "email": "seyma.dogan@email.com", "education": "PhD",
        "experience_years": 5.0,
        "skills": ["machine learning", "deep learning", "python", "tensorflow", "pytorch",
                   "nlp", "statistics", "r", "sql", "data analysis", "research"],
        "raw_text": "Şeyma Doğan | PhD AI | 5 years | AI research scientist. "
                    "NLP, computer vision, PyTorch, TensorFlow. Published in NeurIPS, ICLR."
    },
    # ── MOBILE ────────────────────────────────────────────────────────────────
    {
        "name": "Arda Öztürk", "email": "arda.ozturk@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["react", "javascript", "node.js", "git", "api", "react native", "typescript"],
        "raw_text": "Arda Öztürk | 3 years | React Native mobile developer. "
                    "Cross-platform iOS/Android apps, REST API integration, TypeScript."
    },
    {
        "name": "Melis Sönmez", "email": "melis.sonmez@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["react", "javascript", "html", "css", "api", "git"],
        "raw_text": "Melis Sönmez | 1 year | React developer, learning React Native. "
                    "Web frontend with React, basic REST API consumption."
    },
    # ── CYBERSECURITY / INFRA ─────────────────────────────────────────────────
    {
        "name": "Emre Güler", "email": "emre.guler@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["cybersecurity", "penetration testing", "python", "linux", "networking",
                   "sql", "git", "docker", "owasp"],
        "raw_text": "Emre Güler | 3 years | Security engineer. "
                    "Penetration testing, OWASP top 10, Python scripting, Docker hardening."
    },
    # ── SALES / BD ────────────────────────────────────────────────────────────
    {
        "name": "Berkay Arslan", "email": "berkay.arslan@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["communication", "customer service", "microsoft office"],
        "raw_text": "Berkay Arslan | No experience | Seeking entry-level sales role. "
                    "Strong communication, customer service background from retail."
    },
    {
        "name": "Gizem Yıldız", "email": "gizem.yildiz@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["b2b sales", "crm", "salesforce", "negotiation", "market research"],
        "raw_text": "Gizem Yıldız | 2 years | Inside sales rep. "
                    "Salesforce CRM, outbound prospecting, B2B SaaS sales."
    },
    {
        "name": "Efe Altan", "email": "efe.altan@email.com", "education": "Bachelor",
        "experience_years": 5.0,
        "skills": ["b2b sales", "enterprise sales", "salesforce", "crm", "negotiation",
                   "pipeline management", "business development", "stakeholder management",
                   "sales forecasting", "market research"],
        "raw_text": "Efe Altan | 5 years | Enterprise account executive. "
                    "Closed $15M+ ARR, C-suite relationships, Salesforce power user."
    },
    # ── HR ────────────────────────────────────────────────────────────────────
    {
        "name": "Hülya Çetin", "email": "hulya.cetin@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["hr basics", "microsoft office", "communication"],
        "raw_text": "Hülya Çetin | HR Management graduate | No work experience. "
                    "University HR projects, soft skills training."
    },
    {
        "name": "Serdar Bozkurt", "email": "serdar.bozkurt@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["recruitment", "talent acquisition", "hris", "onboarding", "sourcing",
                   "linkedin recruiter", "stakeholder management"],
        "raw_text": "Serdar Bozkurt | 3 years | Talent acquisition specialist. "
                    "Full-cycle tech recruiting, LinkedIn Recruiter, ATS management."
    },
    {
        "name": "Aylin Özkan", "email": "aylin.ozkan@email.com", "education": "Master",
        "experience_years": 7.0,
        "skills": ["talent acquisition", "performance management", "employee relations",
                   "change management", "hr analytics", "workday", "employment law",
                   "organizational development", "hris", "recruitment"],
        "raw_text": "Aylin Özkan | MSc HRM | 7 years | Senior HR Business Partner. "
                    "Strategic HR, Workday, OD projects, employment law, talent programs."
    },
    # ── FINANCE ───────────────────────────────────────────────────────────────
    {
        "name": "Mehmet Uzun", "email": "mehmet.uzun@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["excel", "accounting basics", "microsoft office"],
        "raw_text": "Mehmet Uzun | Finance graduate | No experience. "
                    "Basic bookkeeping, Excel, academic finance coursework."
    },
    {
        "name": "Dilara Çakır", "email": "dilara.cakir@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["financial analysis", "excel", "sql", "budgeting", "financial reporting"],
        "raw_text": "Dilara Çakır | 2 years | FP&A analyst. "
                    "Budget variance analysis, Excel financial models, SQL reporting."
    },
    {
        "name": "Yusuf Bülbül", "email": "yusuf.bulbul@email.com", "education": "Master",
        "experience_years": 6.0,
        "skills": ["financial modeling", "financial analysis", "excel", "sql", "bloomberg",
                   "valuation", "dcf", "gaap", "forecasting", "budgeting", "equity research"],
        "raw_text": "Yusuf Bülbül | MSc Finance CFA | 6 years | VP Financial Analysis. "
                    "DCF/LBO valuation, Bloomberg, M&A analysis, financial modeling."
    },
    # ── SUPPLY CHAIN ──────────────────────────────────────────────────────────
    {
        "name": "Tuğba Sarı", "email": "tugba.sari@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["excel", "supply chain management", "data analysis"],
        "raw_text": "Tuğba Sarı | 1 year | Logistics coordinator. "
                    "Excel shipment tracking, basic supply chain admin. No SAP experience."
    },
    {
        "name": "Umut Yıldız", "email": "umut.yildiz@email.com", "education": "Bachelor",
        "experience_years": 4.0,
        "skills": ["supply chain management", "procurement", "sap", "vendor management",
                   "contract negotiation", "rfq", "inventory management", "excel"],
        "raw_text": "Umut Yıldız | 4 years | Procurement specialist. "
                    "SAP MM, supplier negotiation, RFQ processes, category management."
    },
    # ── ENGINEERING ───────────────────────────────────────────────────────────
    {
        "name": "Serhat Kurt", "email": "serhat.kurt@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["autocad", "solidworks", "mechanical design"],
        "raw_text": "Serhat Kurt | 1 year | Junior mechanical engineer. "
                    "AutoCAD 2D/3D, SolidWorks basics. No FEA or manufacturing experience."
    },
    {
        "name": "Özge Demir", "email": "ozge.demir@email.com", "education": "Bachelor",
        "experience_years": 4.0,
        "skills": ["solidworks", "catia", "finite element analysis", "ansys", "mechanical design",
                   "autocad", "fmea", "quality management", "lean manufacturing"],
        "raw_text": "Özge Demir | 4 years | Mechanical design engineer. "
                    "SolidWorks + CATIA modeling, ANSYS FEA simulation, FMEA, GD&T."
    },
    # ── MARKETING ─────────────────────────────────────────────────────────────
    {
        "name": "Şule Koç", "email": "sule.koc@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["social media marketing", "canva", "content marketing"],
        "raw_text": "Şule Koç | Marketing graduate | No experience. "
                    "Instagram content creation, Canva, basic copywriting."
    },
    {
        "name": "Atakan Yılmaz", "email": "atakan.yilmaz@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["digital marketing", "seo", "google ads", "google analytics", "ga4",
                   "a/b testing", "hubspot", "email marketing", "sem", "content marketing"],
        "raw_text": "Atakan Yılmaz | 3 years | Digital marketing specialist. "
                    "Google Ads campaigns, SEO content strategy, HubSpot automation."
    },
    # ── LEGAL ─────────────────────────────────────────────────────────────────
    {
        "name": "Başak Güneş", "email": "basak.gunes@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["legal research", "legal writing", "microsoft office"],
        "raw_text": "Başak Güneş | Law graduate | No experience. "
                    "Legal research, academic writing, courtroom observation internship."
    },
    {
        "name": "Alp Arslan", "email": "alp.arslan@email.com", "education": "Master",
        "experience_years": 5.0,
        "skills": ["corporate law", "contract drafting", "contract negotiation",
                   "merger & acquisition", "legal research", "legal writing",
                   "compliance", "due diligence", "gdpr", "data privacy"],
        "raw_text": "Alp Arslan | LLM Corporate Law | 5 years | Senior associate at law firm. "
                    "M&A transactions, GDPR compliance, contract negotiation."
    },
    # ── HEALTHCARE ────────────────────────────────────────────────────────────
    {
        "name": "Müge Şahin", "email": "muge.sahin@email.com", "education": "Master",
        "experience_years": 2.0,
        "skills": ["clinical research", "gcp", "data analysis", "r", "statistics"],
        "raw_text": "Müge Şahin | MSc Clinical Research | 2 years | Clinical data coordinator. "
                    "GCP certified, CRF completion, R for biostatistics. No REDCap experience."
    },
    # ── EXTRA TECH PROFILES (varied) ─────────────────────────────────────────
    {
        "name": "Berk Taş", "email": "berk.tas@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["python", "sql", "excel", "data analysis"],
        "raw_text": "Berk Taş | 2 years | Data analyst. Python, SQL, Excel reports. Limited ML."
    },
    {
        "name": "Ceren Aksoy", "email": "ceren.aksoy@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["javascript", "vue.js", "html", "css", "git", "rest api"],
        "raw_text": "Ceren Aksoy | 3 years | Vue.js frontend developer. "
                    "Single-page applications, REST API integration."
    },
    {
        "name": "Kürşat Yıldız", "email": "kursat.yildiz@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["python", "javascript", "api", "git", "ci/cd", "docker"],
        "raw_text": "Kürşat Yıldız | Self-taught | Bootcamp grad | CI/CD pipelines, Docker, Python scripts."
    },
    {
        "name": "Gamze Arslan", "email": "gamze.arslan@email.com", "education": "Bachelor",
        "experience_years": 1.5,
        "skills": ["java", "sql", "oop", "git", "api", "spring boot"],
        "raw_text": "Gamze Arslan | 1.5 years | Junior Java developer. Spring Boot REST APIs."
    },
    {
        "name": "Erhan Çelik", "email": "erhan.celik@email.com", "education": "Master",
        "experience_years": 7.0,
        "skills": ["python", "machine learning", "deep learning", "tensorflow", "sql",
                   "spark", "mlops", "docker", "kubernetes", "data analysis", "statistics",
                   "nlp", "computer vision"],
        "raw_text": "Erhan Çelik | MSc ML | 7 years | Principal ML engineer. "
                    "Large-scale ML systems, MLOps, Spark, Kubernetes, computer vision and NLP."
    },
    {
        "name": "Sude Polat", "email": "sude.polat@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["python", "fastapi", "postgresql", "docker", "git", "rest api"],
        "raw_text": "Sude Polat | 2 years | FastAPI backend developer. PostgreSQL, Docker, async Python."
    },
    {
        "name": "Anıl Kılıç", "email": "anil.kilic@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["javascript", "react", "html", "css", "git", "api"],
        "raw_text": "Anıl Kılıç | 0 years | Frontend bootcamp grad. React, HTML/CSS, REST APIs."
    },
    {
        "name": "Duygu Yurt", "email": "duygu.yurt@email.com", "education": "Bachelor",
        "experience_years": 4.0,
        "skills": ["product management", "agile", "scrum", "sql", "data analysis",
                   "stakeholder management", "roadmapping", "user research"],
        "raw_text": "Duygu Yurt | 4 years | Product manager at SaaS company. "
                    "Agile/Scrum, SQL analytics, roadmap planning, user research."
    },
    {
        "name": "Volkan Kara", "email": "volkan.kara@email.com", "education": "Bachelor",
        "experience_years": 3.0,
        "skills": ["javascript", "typescript", "react", "css", "html", "git", "storybook"],
        "raw_text": "Volkan Kara | 3 years | UI developer. React + TypeScript, design systems, Storybook."
    },
    {
        "name": "Filiz Erdem", "email": "filiz.erdem@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["python", "sql", "pandas", "data analysis", "excel"],
        "raw_text": "Filiz Erdem | 1 year | Junior data analyst. Python/pandas, SQL, Excel reports."
    },
    {
        "name": "Sinan Doğan", "email": "sinan.dogan@email.com", "education": "Bachelor",
        "experience_years": 5.0,
        "skills": ["node.js", "javascript", "typescript", "mongodb", "postgresql",
                   "docker", "aws", "microservices", "ci/cd", "kafka", "redis", "git"],
        "raw_text": "Sinan Doğan | 5 years | Node.js senior engineer. "
                    "Event-driven microservices, Kafka, AWS, MongoDB, PostgreSQL."
    },
    {
        "name": "Rüya Koşar", "email": "ruya.kosar@email.com", "education": "Bachelor",
        "experience_years": 0.5,
        "skills": ["c#", "sql", "oop", "git"],
        "raw_text": "Rüya Koşar | 6 months | .NET intern. C#, SQL Server basics, OOP concepts."
    },
    {
        "name": "Taner Çelik", "email": "taner.celik@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["java", "python", "c#", "sql", "git", "oop", "api"],
        "raw_text": "Taner Çelik | CS graduate | Multiple languages. "
                    "Java, Python, C# university projects. Strong OOP, SQL, REST API basics."
    },
    {
        "name": "Aybüke Demir", "email": "aybuke.demir@email.com", "education": "Bachelor",
        "experience_years": 2.0,
        "skills": ["react", "javascript", "css", "html", "git", "node.js", "sql", "api"],
        "raw_text": "Aybüke Demir | 2 years | Full stack developer. React + Node.js + SQL."
    },
    {
        "name": "Koray Yıldırım", "email": "koray.yildirim@email.com", "education": "Bachelor",
        "experience_years": 4.0,
        "skills": ["java", "spring boot", "microservices", "kafka", "docker",
                   "kubernetes", "sql", "oop", "api", "git", "aws"],
        "raw_text": "Koray Yıldırım | 4 years | Senior Java engineer. "
                    "Spring Boot, Kafka, Kubernetes, AWS. Domain-driven design."
    },
    {
        "name": "Nesrin Yılmaz", "email": "nesrin.yilmaz@email.com", "education": "Bachelor",
        "experience_years": 1.0,
        "skills": ["python", "django", "sql", "git", "api", "rest api"],
        "raw_text": "Nesrin Yılmaz | 1 year | Django developer. REST APIs, SQL, Python basics."
    },
    {
        "name": "Musa Altın", "email": "musa.altin@email.com", "education": "Bachelor",
        "experience_years": 0.0,
        "skills": ["python", "data analysis", "sql", "statistics", "git"],
        "raw_text": "Musa Altın | Data science student | Python, SQL, statistics coursework. Kaggle beginner."
    },
    {
        "name": "Canan Koç", "email": "canan.koc@email.com", "education": "Master",
        "experience_years": 3.0,
        "skills": ["data analysis", "sql", "python", "r", "statistics",
                   "tableau", "power bi", "machine learning"],
        "raw_text": "Canan Koç | MSc Statistics | 3 years | Data analyst. "
                    "SQL, Python, R, Tableau. Applied statistical modeling and ML basics."
    },
]


def seed():
    db = SessionLocal()
    try:
        # ── Jobs ──────────────────────────────────────────────────────────────
        jobs_added = 0
        for j in JUNIOR_JOBS:
            existing = db.query(JobPosting).filter(JobPosting.title == j["title"]).first()
            if existing:
                print(f"  Job skip (exists): {j['title']}")
                continue
            job = JobPosting(**j)
            db.add(job)
            jobs_added += 1
            print(f"  Job added: {j['title']}")

        db.commit()
        print(f"\n{jobs_added} junior/intern jobs added.\n")

        # ── Candidates ────────────────────────────────────────────────────────
        cands_added = 0
        for c in DIVERSE_CANDIDATES:
            existing = db.query(Candidate).filter(Candidate.email == c["email"]).first()
            if existing:
                print(f"  Candidate skip: {c['name']}")
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

            cands_added += 1
            print(f"  Candidate added: {c['name']} ({len(c['skills'])} skills, {c['experience_years']} yrs)")

        db.commit()
        print(f"\n{cands_added} diverse candidates added.")
        print(f"\nTotal new records: {jobs_added} jobs + {cands_added} candidates")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
