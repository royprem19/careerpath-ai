from fastapi import APIRouter, HTTPException
from backend.database import get_supabase
from backend.models.schemas import RoleResponse
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# High-fidelity real dataset fallback (mirrors supabase_schema.sql)
# This guarantees the app works instantly and enriches smoothly once Supabase is connected
REAL_FALLBACK_ROLES = [
    {
        "id": "1",
        "title": "Full Stack Developer",
        "category": "Software Engineering",
        "description": "Architects and builds complete web applications from database modeling to responsive frontend interfaces.",
        "avg_salary": "₹6.5 - 12 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["JavaScript", "React", "Node.js", "SQL", "HTML5", "CSS3", "REST APIs", "Git & GitHub"],
        "optional_skills": ["TypeScript", "Next.js", "TailwindCSS", "PostgreSQL", "MongoDB", "Docker"]
    },
    {
        "id": "2",
        "title": "Backend Engineer",
        "category": "Software Engineering",
        "description": "Designs scalable REST/GraphQL APIs, microservices, database schemas, and manages server-side logic and caching.",
        "avg_salary": "₹7 - 14 LPA",
        "experience_range": "0-3 years",
        "essential_skills": ["Python", "SQL", "REST APIs", "PostgreSQL", "FastAPI", "Git & GitHub"],
        "optional_skills": ["Redis", "Docker", "Go", "GraphQL", "CI/CD Pipelines", "System Architecture Design"]
    },
    {
        "id": "3",
        "title": "Frontend Engineer",
        "category": "Software Engineering",
        "description": "Develops high-performance, accessible, and responsive user interfaces using modern reactive UI frameworks.",
        "avg_salary": "₹5.5 - 11 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["JavaScript", "React", "HTML5", "CSS3", "TypeScript", "Git & GitHub"],
        "optional_skills": ["TailwindCSS", "Next.js", "Redux", "Jest", "REST APIs"]
    },
    {
        "id": "4",
        "title": "Data Scientist",
        "category": "Data Science & AI",
        "description": "Leverages statistical modeling, machine learning, and data analytics to extract actionable business insights from big data.",
        "avg_salary": "₹8 - 16 LPA",
        "experience_range": "0-3 years",
        "essential_skills": ["Python", "SQL", "Machine Learning", "Pandas", "NumPy", "Scikit-learn"],
        "optional_skills": ["Deep Learning", "Natural Language Processing", "Tableau", "Apache Spark"]
    },
    {
        "id": "5",
        "title": "Machine Learning Engineer",
        "category": "Data Science & AI",
        "description": "Designs, trains, deploys, and monitors production ML systems, deep learning pipelines, and inference APIs.",
        "avg_salary": "₹9 - 18 LPA",
        "experience_range": "1-3 years",
        "essential_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "Scikit-learn", "Docker"],
        "optional_skills": ["TensorFlow", "FastAPI", "Large Language Models (LLMs)", "CI/CD Pipelines", "AWS"]
    },
    {
        "id": "6",
        "title": "DevOps & Cloud Engineer",
        "category": "Infrastructure & Cloud",
        "description": "Automates software delivery with CI/CD pipelines, container orchestration, and cloud infrastructure as code.",
        "avg_salary": "₹7.5 - 15 LPA",
        "experience_range": "1-3 years",
        "essential_skills": ["Docker", "Kubernetes", "CI/CD Pipelines", "Linux", "AWS", "Git & GitHub"],
        "optional_skills": ["Terraform", "Python", "Monitoring & Observability", "Azure"]
    },
    {
        "id": "7",
        "title": "AI / GenAI Solutions Engineer",
        "category": "Data Science & AI",
        "description": "Builds production LLM applications, RAG pipelines, fine-tuned transformer models, and AI agent workflows.",
        "avg_salary": "₹10 - 20 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["Python", "Large Language Models (LLMs)", "Retrieval Augmented Generation (RAG)", "LangChain", "FastAPI", "Hugging Face"],
        "optional_skills": ["Supabase", "PyTorch", "Docker", "Deep Learning"]
    },
    {
        "id": "8",
        "title": "Data Analyst",
        "category": "Data Science & AI",
        "description": "Extracts, cleans, and analyzes complex business datasets; crafts interactive executive dashboards and reports.",
        "avg_salary": "₹5 - 9 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["SQL", "Python", "Pandas", "Tableau"],
        "optional_skills": ["Power BI", "NumPy", "Data Modeling"]
    },
    {
        "id": "9",
        "title": "Cybersecurity Analyst",
        "category": "Security",
        "description": "Protects systems, networks, and data assets against cyber threats, performs vulnerability assessments, and enforces compliance.",
        "avg_salary": "₹6 - 13 LPA",
        "experience_range": "0-3 years",
        "essential_skills": ["Network Security", "Vulnerability Assessment", "Linux"],
        "optional_skills": ["Python", "Penetration Testing", "AWS"]
    },
    {
        "id": "11",
        "title": "Mobile App Developer",
        "category": "Mobile Development",
        "description": "Builds native or cross-platform mobile apps for iOS and Android using modern frameworks with offline capabilities.",
        "avg_salary": "₹6 - 12 LPA",
        "experience_range": "0-3 years",
        "essential_skills": ["Flutter", "REST APIs", "Git & GitHub"],
        "optional_skills": ["React Native", "Android (Kotlin)", "Supabase"]
    },
    {
        "id": "12",
        "title": "Product Manager (Technical)",
        "category": "Product & Management",
        "description": "Bridges business, engineering, and UX to define product strategy, roadmap execution, and metric-driven feature releases.",
        "avg_salary": "₹11 - 22 LPA",
        "experience_range": "1-4 years",
        "essential_skills": ["Agile & Scrum", "Product Roadmapping", "SQL"],
        "optional_skills": ["REST APIs", "Tableau", "System Architecture Design"]
    },
    {
        "id": "15",
        "title": "Data Engineer",
        "category": "Data Science & AI",
        "description": "Constructs scalable ETL data pipelines, data warehouses, streaming systems, and data lake architectures for analytics.",
        "avg_salary": "₹8 - 16 LPA",
        "experience_range": "1-3 years",
        "essential_skills": ["Python", "SQL", "Apache Spark", "ETL Pipelines", "PostgreSQL"],
        "optional_skills": ["Apache Kafka", "Docker", "AWS"]
    },
    {
        "id": "10",
        "title": "Cloud Solutions Architect",
        "category": "Infrastructure & Cloud",
        "description": "Architects enterprise multi-cloud platforms, high-availability microservices, and cost-effective distributed systems.",
        "avg_salary": "₹14 - 26 LPA",
        "experience_range": "3-6 years",
        "essential_skills": ["AWS", "Azure", "Terraform", "Kubernetes", "System Design", "Docker"],
        "optional_skills": ["GCP", "Linux", "CI/CD Pipelines", "Microservices"]
    },
    {
        "id": "13",
        "title": "Site Reliability Engineer (SRE)",
        "category": "Infrastructure & Cloud",
        "description": "Applies software engineering principles to operations, manages uptime SLIs/SLOs, automated alerting, and cluster resilience.",
        "avg_salary": "₹9 - 17 LPA",
        "experience_range": "1-4 years",
        "essential_skills": ["Kubernetes", "Docker", "Linux", "Prometheus", "CI/CD Pipelines", "Python"],
        "optional_skills": ["Terraform", "AWS", "Go", "Ansible"]
    },
    {
        "id": "14",
        "title": "QA Automation Engineer",
        "category": "Software Engineering",
        "description": "Develops automated test frameworks, end-to-end regression suites, and API integration testing pipelines.",
        "avg_salary": "₹5 - 9.5 LPA",
        "experience_range": "0-3 years",
        "essential_skills": ["Selenium", "Python", "Postman", "API Testing", "Java", "Git & GitHub"],
        "optional_skills": ["Playwright", "Cypress", "Jenkins", "SQL"]
    },
    {
        "id": "16",
        "title": "UI/UX & Product Designer",
        "category": "Design & Creative",
        "description": "Crafts intuitive human-centered product designs, wireframes, component libraries, and interactive prototypes.",
        "avg_salary": "₹5.5 - 12 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["UI/UX Design", "Figma", "Wireframing", "Prototyping", "User Research"],
        "optional_skills": ["Design Systems", "Usability Testing", "Information Architecture", "HTML5", "CSS3"]
    },
    {
        "id": "17",
        "title": "Business Analyst",
        "category": "Business & Analytics",
        "description": "Translates complex business workflows into clear functional specifications, process diagrams, and data-backed business insights.",
        "avg_salary": "₹5 - 10 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["Business Analysis", "SQL", "Data Modeling", "Process Mapping", "Requirements Gathering"],
        "optional_skills": ["Tableau", "Power BI", "User Stories", "Agile & Scrum", "Python"]
    },
    {
        "id": "18",
        "title": "Product Manager",
        "category": "Product & Management",
        "description": "Owns product vision, roadmap prioritization, cross-functional engineering alignment, and user-centric problem solving.",
        "avg_salary": "₹10 - 20 LPA",
        "experience_range": "1-3 years",
        "essential_skills": ["Product Management", "Product Roadmapping", "User Stories", "Agile & Scrum", "Stakeholder Management"],
        "optional_skills": ["SQL", "Data Analytics", "A/B Testing", "Wireframing", "Customer Journey Mapping"]
    },
    {
        "id": "19",
        "title": "Digital Marketing & Growth Specialist",
        "category": "Marketing & Growth",
        "description": "Drives user acquisition, brand visibility, and organic/paid growth through SEO, content campaigns, and performance marketing analytics.",
        "avg_salary": "₹4.5 - 9 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["Digital Marketing", "SEO / SEM", "Content Strategy", "Google Analytics", "Social Media Marketing"],
        "optional_skills": ["Email Marketing", "Copywriting", "A/B Testing", "Performance Marketing", "Conversion Rate Optimization"]
    },
    {
        "id": "20",
        "title": "Technical Operations & Customer Success Specialist",
        "category": "Operations & Support",
        "description": "Ensures seamless customer adoption, operational SLA resolution, client onboarding, and technical incident troubleshooting.",
        "avg_salary": "₹4.5 - 8.5 LPA",
        "experience_range": "0-2 years",
        "essential_skills": ["Technical Support & Troubleshooting", "Customer Success & Retention", "CRM / Salesforce", "Process Optimization"],
        "optional_skills": ["SQL", "SLA Management", "Incident Management", "Root Cause Analysis", "Jira"]
    }
]

import json
from pathlib import Path

ESCO_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "esco_ingested_roles.json"
INDIAN_BENCHMARKS_FILE = Path(__file__).resolve().parent.parent / "data" / "indian_role_benchmarks.json"

_CACHED_INDIAN_BENCHMARKS = None

def get_indian_benchmarks() -> dict:
    global _CACHED_INDIAN_BENCHMARKS
    if _CACHED_INDIAN_BENCHMARKS is None:
        if INDIAN_BENCHMARKS_FILE.exists():
            try:
                with open(INDIAN_BENCHMARKS_FILE, "r", encoding="utf-8") as f:
                    _CACHED_INDIAN_BENCHMARKS = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load indian_role_benchmarks.json: {e}")
                _CACHED_INDIAN_BENCHMARKS = {}
        else:
            _CACHED_INDIAN_BENCHMARKS = {}
    return _CACHED_INDIAN_BENCHMARKS

def get_esco_roles() -> List[RoleResponse]:
    if not ESCO_DATA_FILE.exists():
        return []
    try:
        with open(ESCO_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            RoleResponse(
                id=f"esco_{i+1}",
                title=r["title"],
                category="ESCO ICT & Technology",
                description=r.get("description", "European Commission ESCO standard occupation"),
                essential_skills=r.get("essential_skills", []),
                optional_skills=r.get("optional_skills", []),
                avg_salary="₹8 - 18 LPA",
                experience_range="1-3 years"
            )
            for i, r in enumerate(data)
        ]
    except Exception as e:
        logger.warning(f"Could not load ESCO json: {e}")
        return []

@router.get("/api/roles", response_model=List[RoleResponse])
async def list_roles():
    esco_roles = get_esco_roles()
    supabase = get_supabase()
    if not supabase:
        combined = [RoleResponse(**r) for r in REAL_FALLBACK_ROLES]
        # Append ESCO roles not already in fallback
        existing_titles = {r.title.lower() for r in combined}
        for er in esco_roles:
            if er.title.lower() not in existing_titles:
                combined.append(er)
        return combined
        
    try:
        # Fetch all roles
        roles_resp = supabase.table("roles").select("*").execute()
        if not roles_resp.data:
            return [RoleResponse(**r) for r in REAL_FALLBACK_ROLES]
            
        roles = roles_resp.data
        
        # Batch fetch all role_skills with skills name
        # Supabase foreign key join: role_skills(role_id, relation_type, skills(name))
        try:
            rs_resp = supabase.table("role_skills").select("role_id, relation_type, skills(name)").execute()
            mapping = {}
            for row in rs_resp.data:
                rid = str(row["role_id"])
                if rid not in mapping:
                    mapping[rid] = {"essential": [], "optional": []}
                skill_obj = row.get("skills")
                if skill_obj and "name" in skill_obj:
                    s_name = skill_obj["name"]
                    if row["relation_type"] == "essential":
                        mapping[rid]["essential"].append(s_name)
                    else:
                        mapping[rid]["optional"].append(s_name)
        except Exception as join_err:
            logger.warning(f"Join query failed, falling back to separate queries: {join_err}")
            mapping = {}

        result = []
        for r in roles:
            rid = str(r["id"])
            role_mapping = mapping.get(rid, {"essential": [], "optional": []})
            
            # If mapping was empty, check if we have data in Indian benchmarks, ESCO, or fallback
            if not role_mapping["essential"]:
                # Check Indian benchmarks
                indian_benchmarks = get_indian_benchmarks()
                if r["title"] in indian_benchmarks:
                    ib = indian_benchmarks[r["title"]]
                    role_mapping["essential"] = ib.get("essential_skills", [])
                    role_mapping["optional"] = ib.get("optional_skills", [])

            if not role_mapping["essential"]:
                # Check ESCO matches
                esco_match = next((er for er in esco_roles if er.title.lower() == r["title"].lower()), None)
                if esco_match:
                    role_mapping["essential"] = esco_match.essential_skills
                    role_mapping["optional"] = esco_match.optional_skills

            if not role_mapping["essential"]:
                fallback_match = next((fb for fb in REAL_FALLBACK_ROLES if str(fb["id"]) == rid or fb["title"].lower() == r["title"].lower()), None)
                if fallback_match:
                    role_mapping["essential"] = fallback_match["essential_skills"]
                    role_mapping["optional"] = fallback_match["optional_skills"]
            
            result.append(RoleResponse(
                id=rid,
                title=r["title"],
                category=r.get("category", "Technology"),
                description=r.get("description"),
                essential_skills=role_mapping["essential"],
                optional_skills=role_mapping["optional"],
                avg_salary=r.get("avg_salary") or "₹8 - 18 LPA",
                experience_range=r.get("experience_range") or "1-3 years"
            ))
            
        existing_titles = {item.title.lower() for item in result}
        for er in esco_roles:
            if er.title.lower() not in existing_titles:
                result.append(er)
                
        return result
    except Exception as e:
        logger.error(f"Error fetching roles from Supabase: {e}")
        combined = [RoleResponse(**r) for r in REAL_FALLBACK_ROLES]
        existing_titles = {item.title.lower() for item in combined}
        for er in esco_roles:
            if er.title.lower() not in existing_titles:
                combined.append(er)
        return combined

@router.get("/api/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: str):
    roles = await list_roles()
    matched = next((r for r in roles if r.id == role_id or r.title.lower() == role_id.lower()), None)
    if not matched:
        raise HTTPException(status_code=404, detail="Role not found")
    return matched
