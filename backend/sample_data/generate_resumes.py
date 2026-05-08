"""Generate 100 synthetic resume records for the demo dataset."""
import json, random, os

PROFILES = {
    "Python Developer": {"count": 15, "skills": [["python","django","flask","fastapi","sql","postgresql","docker","git","linux","rest","celery","redis","aws"],["python","fastapi","sql","docker","git","rest","pytest","mongodb","redis"],["python","django","sql","git","linux","rest","aws","docker"]]},
    "Frontend Developer": {"count": 15, "skills": [["javascript","react","typescript","html","css","tailwind","git","next.js","webpack","figma"],["javascript","vue","html","css","sass","git","webpack","rest"],["javascript","react","html","css","bootstrap","git","jquery","rest"]]},
    "Full Stack Developer": {"count": 15, "skills": [["javascript","react","node.js","python","postgresql","docker","git","rest","typescript","mongodb"],["javascript","react","python","django","sql","git","docker","aws","html","css"],["javascript","typescript","react","node.js","sql","git","docker","rest"]]},
    "Data Analyst": {"count": 10, "skills": [["python","sql","pandas","excel","tableau","power bi","data analysis","matplotlib","git"],["python","sql","excel","data analysis","pandas","tableau","statistics","git"],["python","sql","pandas","excel","power bi","data analysis","git"]]},
    "Data Scientist": {"count": 10, "skills": [["python","machine learning","pandas","numpy","scikit-learn","sql","tensorflow","matplotlib","statistics","git"],["python","machine learning","pandas","numpy","sql","scikit-learn","data analysis","deep learning","git"],["python","machine learning","pandas","numpy","sql","scikit-learn","pytorch","nlp","git"]]},
    "ML Engineer": {"count": 10, "skills": [["python","machine learning","tensorflow","pytorch","docker","sql","pandas","numpy","scikit-learn","aws","git","mlflow"],["python","machine learning","pytorch","nlp","docker","git","pandas","numpy","deep learning"],["python","machine learning","tensorflow","docker","kubernetes","git","sql","pandas","numpy"]]},
    "DevOps Engineer": {"count": 10, "skills": [["docker","kubernetes","aws","terraform","ci/cd","linux","git","jenkins","python","ansible","monitoring"],["docker","kubernetes","aws","linux","git","terraform","ci/cd","python","bash"],["docker","aws","gcp","linux","git","ci/cd","terraform","python","jenkins"]]},
    "Java Developer": {"count": 10, "skills": [["java","spring boot","sql","microservices","docker","git","rest","maven","postgresql","design patterns"],["java","spring boot","sql","docker","git","rest","maven","junit","kafka"],["java","spring boot","sql","git","rest","docker","microservices","maven"]]},
    "UI/UX Designer": {"count": 5, "skills": [["figma","ui/ux","ux design","photoshop","html","css","prototyping","adobe xd"],["figma","ui/ux","ux design","html","css","sketch","prototyping"],["figma","ui/ux","photoshop","html","css","prototyping"]]},
}

FIRST_NAMES = ["James","Emma","Liam","Olivia","Noah","Ava","William","Sophia","Oliver","Isabella","Elijah","Mia","Lucas","Charlotte","Mason","Amelia","Logan","Harper","Alexander","Evelyn","Ethan","Abigail","Jacob","Emily","Michael","Elizabeth","Daniel","Sofia","Henry","Avery","Sebastian","Ella","Jack","Scarlett","Aiden","Grace","Owen","Lily","Samuel","Chloe","Ryan","Victoria","Nathan","Riley","Caleb","Aria","Dylan","Zoey","Luke","Nora","Andrew","Hannah","Isaac","Lillian","Joshua","Addison","Adrian","Eleanor","Christopher","Savannah","Theodore","Brooklyn","Elias","Leah","Thomas","Natalie","David","Zoe","John","Audrey","Robert","Bella","Matthew","Claire","Joseph","Anna","Charles","Skylar","Leo","Samantha","Benjamin","Paisley","Aaron","Caroline","Gabriel","Genesis","Julian","Madelyn","Jayden","Naomi","Anthony","Alice","Lincoln","Sadie","Cameron","Hailey","Jeremiah","Eva","Christian","Emilia"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Chen","Park","Kim","Patel","Shah","Singh","Kumar","Cohen","Murphy","Sullivan","Foster","Reed","Cox","Ward","Brooks"]
EDUCATION = ["Bachelor","Master","PhD"]
EDU_WEIGHTS_NORMAL = [0.6, 0.35, 0.05]
EDU_WEIGHTS_RESEARCH = [0.2, 0.5, 0.3]

def gen_email(first, last):
    domains = ["gmail.com","outlook.com","yahoo.com","hotmail.com","protonmail.com"]
    sep = random.choice([".","-","_",""])
    return f"{first.lower()}{sep}{last.lower()}@{random.choice(domains)}"

def gen_phone():
    return f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

def gen_resume(idx, role, skill_templates, edu_weights):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    skills = list(set(random.choice(skill_templates) + random.sample(random.choice(skill_templates), k=random.randint(1,3))))
    edu = random.choices(EDUCATION, weights=edu_weights, k=1)[0]
    exp = round(random.uniform(0.5, 12.0), 1)
    
    # Generate realistic raw text
    skills_text = ", ".join(skills)
    raw = f"""{first} {last}
{gen_email(first, last)} | {gen_phone()}

SUMMARY
Experienced {role} with {exp} years of professional experience. Proficient in {skills_text}. Passionate about building high-quality software solutions.

EDUCATION
{edu}'s Degree in Computer Science
University of Technology, 20{random.randint(10,22)}

EXPERIENCE
{role} | Tech Company Inc. | {random.randint(1,5)} years
- Developed and maintained software applications using {', '.join(skills[:4])}
- Collaborated with cross-functional teams in agile environment
- Implemented best practices for code quality and testing

{'Junior ' if exp < 2 else ''}{role} | StartupXYZ | {max(1, int(exp)-2)} years
- Built features using {', '.join(skills[2:5])}
- Participated in code reviews and technical discussions
- Contributed to CI/CD pipeline improvements

SKILLS
{skills_text}
"""
    return {
        "name": f"{first} {last}",
        "email": gen_email(first, last),
        "phone": gen_phone(),
        "education": edu,
        "experience_years": exp,
        "skills": skills,
        "raw_text": raw,
        "category": role
    }

def main():
    resumes = []
    idx = 0
    for role, cfg in PROFILES.items():
        is_research = role in ("Data Scientist", "ML Engineer")
        weights = EDU_WEIGHTS_RESEARCH if is_research else EDU_WEIGHTS_NORMAL
        for _ in range(cfg["count"]):
            resumes.append(gen_resume(idx, role, cfg["skills"], weights))
            idx += 1
    
    random.shuffle(resumes)
    out = os.path.join(os.path.dirname(__file__), "resumes.json")
    with open(out, "w") as f:
        json.dump(resumes, f, indent=2)
    print(f"✅ Generated {len(resumes)} resumes → {out}")

if __name__ == "__main__":
    main()
