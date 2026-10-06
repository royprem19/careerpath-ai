from backend.models.schemas import RoadmapEntry

# Real courses catalog with accredited Indian Government Initiatives & Industry standards
REAL_COURSE_CATALOG = {
    "python": {
        "course_name": "Programming, Data Structures & Algorithms using Python",
        "platform": "NPTEL (IIT Madras) / SWAYAM",
        "url": "https://nptel.ac.in/courses/106106145",
        "duration_weeks": 4,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "NPTEL / SWAYAM (IIT Madras)",
        "is_govt_initiative": True,
        "project": "Build an Automated Job Application & Web Scraping Pipeline in Python"
    },
    "javascript": {
        "course_name": "Web Technologies & Modern Client Scripting",
        "platform": "SWAYAM / NPTEL (IIT Kharagpur)",
        "url": "https://swayam.gov.in/explorer?category=Computer_Science_and_Engineering",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "SWAYAM (Govt of India)",
        "is_govt_initiative": True,
        "project": "Build an Interactive Task Management Dashboard with LocalStorage"
    },
    "typescript": {
        "course_name": "Understanding TypeScript - Enterprise Application Patterns",
        "platform": "FutureSkills Prime / Udemy",
        "url": "https://futureskillsprime.in/",
        "duration_weeks": 2,
        "is_free": False,
        "difficulty": "Intermediate",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Refactor a Vanilla React app into Strict TypeScript with Generics"
    },
    "react": {
        "course_name": "Modern Frontend Development & Single Page Architecture",
        "platform": "Skill India Digital & freeCodeCamp",
        "url": "https://www.skillindiadigital.gov.in/",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "Skill India Digital (NSDC)",
        "is_govt_initiative": True,
        "project": "Build an E-Commerce Catalog with Cart, Filter, and Context API"
    },
    "next.js": {
        "course_name": "Next.js 14 Complete Course & App Router",
        "platform": "Next.js Learn (Official)",
        "url": "https://nextjs.org/learn",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": None,
        "is_govt_initiative": False,
        "project": "Create a Server-Side Rendered Blog with App Router and Markdown CMS"
    },
    "fastapi": {
        "course_name": "FastAPI Official Interactive Tutorial & Async APIs",
        "platform": "FastAPI Documentation",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "duration_weeks": 1,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": None,
        "is_govt_initiative": False,
        "project": "Develop a Production REST API with JWT Auth, Pydantic & Postgres"
    },
    "sql": {
        "course_name": "Database Management System",
        "platform": "NPTEL (IIT Kharagpur) / SWAYAM",
        "url": "https://nptel.ac.in/courses/106105175",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "NPTEL / SWAYAM (IIT Kharagpur)",
        "is_govt_initiative": True,
        "project": "Design Normalized Schemas, Complex Window Functions & Query Indexing"
    },
    "postgresql": {
        "course_name": "Relational Database Design & PostgreSQL Essentials",
        "platform": "FutureSkills Prime (MeitY & NASSCOM)",
        "url": "https://futureskillsprime.in/",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Implement Full-Text Search, Stored Procedures and PgBouncer connection pool"
    },
    "docker": {
        "course_name": "Containerization & Cloud Native Architecture",
        "platform": "FutureSkills Prime (C-DAC / MeitY)",
        "url": "https://futureskillsprime.in/course/cloud-computing-virtualization",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Containerize a Full-Stack Web App with Multi-Stage Builds and Docker Compose"
    },
    "kubernetes": {
        "course_name": "Cloud Native Computing & Container Orchestration",
        "platform": "NPTEL (IIT Kharagpur)",
        "url": "https://nptel.ac.in/courses/106105167",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Advanced",
        "initiative": "NPTEL / SWAYAM (IIT Kharagpur)",
        "is_govt_initiative": True,
        "project": "Deploy Microservices with Ingress, Horizontal Pod Autoscaling and ConfigMaps"
    },
    "aws": {
        "course_name": "Cloud Computing & AWS Cloud Solutions",
        "platform": "NPTEL (IIT Kharagpur) & FutureSkills Prime",
        "url": "https://nptel.ac.in/courses/106105167",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Host a Scalable Web App with S3, CloudFront, EC2 and RDS in a custom VPC"
    },
    "machine learning": {
        "course_name": "Introduction to Machine Learning",
        "platform": "NPTEL (IIT Kharagpur) / SWAYAM",
        "url": "https://nptel.ac.in/courses/106105152",
        "duration_weeks": 4,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "NPTEL / SWAYAM (IIT Kharagpur)",
        "is_govt_initiative": True,
        "project": "Build an End-to-End Churn Prediction Model with Model Evaluation & ROC/AUC"
    },
    "deep learning": {
        "course_name": "Deep Learning & Neural Networks",
        "platform": "NPTEL (IIT Ropar) / SWAYAM",
        "url": "https://nptel.ac.in/courses/106106184",
        "duration_weeks": 4,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "NPTEL / SWAYAM (IIT Ropar)",
        "is_govt_initiative": True,
        "project": "Train a Convolutional Neural Network (CNN) for Medical Image Classification"
    },
    "pytorch": {
        "course_name": "Deep Learning with PyTorch for Artificial Intelligence",
        "platform": "FutureSkills Prime / DeepLearning.AI",
        "url": "https://futureskillsprime.in/",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Build and Fine-tune a Custom ResNet Vision Model on PyTorch"
    },
    "large language models (llms)": {
        "course_name": "Generative AI and Large Language Models Fundamentals",
        "platform": "FutureSkills Prime (MeitY AI Initiative)",
        "url": "https://futureskillsprime.in/course/artificial-intelligence",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Build a Document Q&A Bot using RAG, LangChain, Vector Embeddings & Llama-3"
    },
    "retrieval augmented generation (rag)": {
        "course_name": "Production RAG Pipelines & Vector Search Systems",
        "platform": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/short-courses/",
        "duration_weeks": 1,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": None,
        "is_govt_initiative": False,
        "project": "Implement Hybrid Keyword + Semantic Vector Search with Reranking in Python"
    },
    "pandas": {
        "course_name": "Data Analytics with Python",
        "platform": "NPTEL (IIT Roorkee) / SWAYAM",
        "url": "https://nptel.ac.in/courses/110107092",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "NPTEL / SWAYAM (IIT Roorkee)",
        "is_govt_initiative": True,
        "project": "Analyze 100K+ Real-World Naukri Job Postings and Export Visual Insights"
    },
    "tableau": {
        "course_name": "Business Intelligence & Data Visualization",
        "platform": "Skill India Digital (NSDC)",
        "url": "https://www.skillindiadigital.gov.in/",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "Skill India Digital (NSDC)",
        "is_govt_initiative": True,
        "project": "Build an Interactive Executive Dashboard Tracking Workforce Hiring Metrics"
    },
    "git & github": {
        "course_name": "Software Engineering & Collaborative Version Control",
        "platform": "SWAYAM / NPTEL (IIT Kharagpur)",
        "url": "https://swayam.gov.in/",
        "duration_weeks": 1,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "SWAYAM (Govt of India)",
        "is_govt_initiative": True,
        "project": "Setup Git Flow Branching, Pull Request Reviews and Semantic Versioning"
    },
    "ci/cd pipelines": {
        "course_name": "DevOps Practices & Continuous Integration Automation",
        "platform": "FutureSkills Prime (MeitY)",
        "url": "https://futureskillsprime.in/",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Configure Automated Unit Tests, Docker Image Builds and Cloud Auto-Deploy"
    },
    "ui/ux design": {
        "course_name": "User Centric Computing & Interaction Design",
        "platform": "NPTEL (IIT Guwahati) / SWAYAM",
        "url": "https://nptel.ac.in/courses/106103115",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "NPTEL / SWAYAM (IIT Guwahati)",
        "is_govt_initiative": True,
        "project": "Create High-Fidelity Interactive Prototypes & Usability Audit for a Bharat E-Commerce App"
    },
    "figma": {
        "course_name": "UI/UX Design Masterclass with Figma",
        "platform": "Skill India Digital (NSDC Hub)",
        "url": "https://www.skillindiadigital.gov.in/",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "Skill India Digital (NSDC)",
        "is_govt_initiative": True,
        "project": "Design a Scalable Design System with Tokens, Auto-layout, and Component Variants"
    },
    "product management": {
        "course_name": "Agile Product Management & Requirements Engineering",
        "platform": "FutureSkills Prime / NASSCOM",
        "url": "https://futureskillsprime.in/",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Intermediate",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Draft a Product Strategy Memo, PRD, and Metric North Star for a FinTech Product"
    },
    "business analysis": {
        "course_name": "Business Analytics for Management Decision Making",
        "platform": "NPTEL (IIT Kharagpur) / SWAYAM",
        "url": "https://nptel.ac.in/courses/110105089",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "NPTEL / SWAYAM (IIT Kharagpur)",
        "is_govt_initiative": True,
        "project": "Conduct Gap Analysis, Process BPMN Mapping, and Stakeholder Requirements Traceability"
    },
    "digital marketing": {
        "course_name": "Certificate Course in Digital Marketing & Social Media Strategy",
        "platform": "Skill India Digital (NSDC Hub)",
        "url": "https://www.skillindiadigital.gov.in/",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "Skill India Digital (NSDC)",
        "is_govt_initiative": True,
        "project": "Plan and Launch a Multi-Channel SEO/SEM Campaign with Google Analytics Tracking"
    },
    "agile & scrum": {
        "course_name": "Project Management & Agile Methodology",
        "platform": "NPTEL (IIT Roorkee) / SWAYAM",
        "url": "https://nptel.ac.in/courses/110107081",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "NPTEL / SWAYAM (IIT Roorkee)",
        "is_govt_initiative": True,
        "project": "Run Simulated 2-Week Sprint Planning, Backlog Refinement and Retrospective on Jira"
    },
    "cybersecurity": {
        "course_name": "Information Security & Cyber Law Foundations",
        "platform": "FutureSkills Prime (C-DAC / MeitY)",
        "url": "https://futureskillsprime.in/",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "initiative": "FutureSkills Prime (MeitY & NASSCOM)",
        "is_govt_initiative": True,
        "project": "Perform Network Packet Analysis, Vulnerability Scanning, and Incident Response Playbook"
    }
}

def generate_roadmap(missing_skills: list[str], course_db: list[dict] = None) -> list[RoadmapEntry]:
    roadmap = []
    week = 1
    
    # Create lookup map from DB if provided
    db_lookup = {}
    if course_db:
        for c in course_db:
            s_name = c.get("skill_name", "").strip().lower()
            if s_name:
                db_lookup[s_name] = c
                
    for skill in missing_skills:
        s_clean = skill.strip()
        s_key = s_clean.lower()
        
        # 1. Check Supabase DB lookup
        # 2. Check Real Curated Catalog
        # 3. Dynamic High-Quality Fallback with Skill India / NPTEL accredited pathways
        if s_key in db_lookup:
            c_info = db_lookup[s_key]
            duration = int(c_info.get("duration_weeks") or 2)
            initiative = c_info.get("initiative")
            is_govt = bool(c_info.get("is_govt_initiative", False) or initiative)
            roadmap.append(RoadmapEntry(
                week=week,
                skill=s_clean,
                course=c_info.get("course_name") or f"Mastering {s_clean}",
                platform=c_info.get("platform") or "NPTEL / Coursera",
                url=c_info.get("url") or f"https://www.google.com/search?q={s_clean}+online+course",
                project=f"Build a production-ready application implementing {s_clean}",
                duration=f"{duration} week(s)",
                is_free=bool(c_info.get("is_free", True)),
                difficulty=c_info.get("difficulty") or "Intermediate",
                initiative=initiative,
                is_govt_initiative=is_govt
            ))
            week += max(1, duration)
        elif s_key in REAL_COURSE_CATALOG:
            c_info = REAL_COURSE_CATALOG[s_key]
            duration = c_info["duration_weeks"]
            roadmap.append(RoadmapEntry(
                week=week,
                skill=s_clean,
                course=c_info["course_name"],
                platform=c_info["platform"],
                url=c_info["url"],
                project=c_info["project"],
                duration=f"{duration} week(s)",
                is_free=c_info["is_free"],
                difficulty=c_info["difficulty"],
                initiative=c_info.get("initiative"),
                is_govt_initiative=bool(c_info.get("is_govt_initiative", False))
            ))
            week += max(1, duration)
        else:
            duration = 2
            roadmap.append(RoadmapEntry(
                week=week,
                skill=s_clean,
                course=f"Accredited {s_clean} Foundation & Applied Mastery",
                platform="Skill India Digital / NPTEL (Govt of India)",
                url=f"https://www.skillindiadigital.gov.in/courses",
                project=f"Implement a hands-on capstone project demonstrating industry competency in {s_clean}",
                duration=f"{duration} week(s)",
                is_free=True,
                difficulty="Beginner",
                initiative="Skill India Digital (NSDC)",
                is_govt_initiative=True
            ))
            week += max(1, duration)
            
    return roadmap
