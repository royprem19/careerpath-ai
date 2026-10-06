from backend.models.schemas import RoadmapEntry

# Real courses catalog (matches supabase_schema.sql)
REAL_COURSE_CATALOG = {
    "python": {
        "course_name": "Programming, Data Structures & Algorithms using Python",
        "platform": "NPTEL (IIT Madras)",
        "url": "https://nptel.ac.in/courses/106106145",
        "duration_weeks": 4,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Build an Automated Job Application & Web Scraping Pipeline in Python"
    },
    "javascript": {
        "course_name": "JavaScript Algorithms and Data Structures",
        "platform": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Build an Interactive Task Management Dashboard with LocalStorage"
    },
    "typescript": {
        "course_name": "Understanding TypeScript - 2024 Edition",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/understanding-typescript/",
        "duration_weeks": 2,
        "is_free": False,
        "difficulty": "Intermediate",
        "project": "Refactor a Vanilla React app into Strict TypeScript with Generics"
    },
    "react": {
        "course_name": "Frontend Development Libraries (React)",
        "platform": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Build an E-Commerce Catalog with Cart, Filter, and Context API"
    },
    "next.js": {
        "course_name": "Next.js 14 Complete Course",
        "platform": "Next.js Learn (Official)",
        "url": "https://nextjs.org/learn",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Create a Server-Side Rendered Blog with App Router and Markdown CMS"
    },
    "fastapi": {
        "course_name": "FastAPI Official Interactive Tutorial",
        "platform": "FastAPI Documentation",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "duration_weeks": 1,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Develop a Production REST API with JWT Auth, Pydantic & Postgres"
    },
    "sql": {
        "course_name": "Database Management System",
        "platform": "NPTEL (IIT Kharagpur)",
        "url": "https://nptel.ac.in/courses/106105175",
        "duration_weeks": 3,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Design Normalized Schemas, Complex Window Functions & Query Indexing"
    },
    "postgresql": {
        "course_name": "PostgreSQL for Everybody Specialization",
        "platform": "Coursera (Univ. of Michigan)",
        "url": "https://www.coursera.org/specializations/postgresql-for-everybody",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Implement Full-Text Search, Stored Procedures and PgBouncer connection pool"
    },
    "docker": {
        "course_name": "Docker & Container Fundamentals",
        "platform": "freeCodeCamp YouTube",
        "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo",
        "duration_weeks": 1,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Containerize a Full-Stack Web App with Multi-Stage Builds and Docker Compose"
    },
    "kubernetes": {
        "course_name": "Certified Kubernetes Administrator (CKA)",
        "platform": "KodeKloud",
        "url": "https://kodekloud.com/courses/certified-kubernetes-administrator-cka/",
        "duration_weeks": 3,
        "is_free": False,
        "difficulty": "Advanced",
        "project": "Deploy Microservices with Ingress, Horizontal Pod Autoscaling and ConfigMaps"
    },
    "aws": {
        "course_name": "AWS Certified Cloud Practitioner Training",
        "platform": "freeCodeCamp YouTube",
        "url": "https://www.youtube.com/watch?v=SOTamWNgDKc",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Host a Scalable Web App with S3, CloudFront, EC2 and RDS in a custom VPC"
    },
    "machine learning": {
        "course_name": "Machine Learning Specialization by Andrew Ng",
        "platform": "Coursera (DeepLearning.AI)",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "duration_weeks": 4,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Build an End-to-End Churn Prediction Model with Model Evaluation & ROC/AUC"
    },
    "deep learning": {
        "course_name": "Deep Learning Specialization",
        "platform": "Coursera (DeepLearning.AI)",
        "url": "https://www.coursera.org/specializations/deep-learning",
        "duration_weeks": 4,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Train a Convolutional Neural Network (CNN) for Medical Image Classification"
    },
    "pytorch": {
        "course_name": "PyTorch for Deep Learning Bootcamp",
        "platform": "freeCodeCamp",
        "url": "https://www.youtube.com/watch?v=V_xro1bcAuA",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Build and Fine-tune a Custom ResNet Vision Model on PyTorch"
    },
    "large language models (llms)": {
        "course_name": "Generative AI with Large Language Models",
        "platform": "Coursera (AWS & DeepLearning.AI)",
        "url": "https://www.coursera.org/learn/generative-ai-with-llms",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Build a Document Q&A Bot using RAG, LangChain, Vector Embeddings & Llama-3"
    },
    "retrieval augmented generation (rag)": {
        "course_name": "Production RAG Pipelines & Vector Databases",
        "platform": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/short-courses/",
        "duration_weeks": 1,
        "is_free": True,
        "difficulty": "Intermediate",
        "project": "Implement Hybrid Keyword + Semantic Vector Search with Reranking in Python"
    },
    "pandas": {
        "course_name": "Data Analysis with Python",
        "platform": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Analyze 100K+ Real-World Naukri Job Postings and Export Visual Insights"
    },
    "tableau": {
        "course_name": "Tableau for Data Science",
        "platform": "Coursera (UC Davis)",
        "url": "https://www.coursera.org/learn/data-visualization-tableau",
        "duration_weeks": 2,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Build an Interactive Executive Dashboard Tracking Workforce Hiring Metrics"
    },
    "git & github": {
        "course_name": "Version Control with Git",
        "platform": "Coursera (Atlassian)",
        "url": "https://www.coursera.org/learn/version-control-with-git",
        "duration_weeks": 1,
        "is_free": True,
        "difficulty": "Beginner",
        "project": "Setup Git Flow Branching, Pull Request Reviews and Semantic Versioning"
    },
    "ci/cd pipelines": {
        "course_name": "GitHub Actions - The Complete Guide",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/github-actions-the-complete-guide/",
        "duration_weeks": 1,
        "is_free": False,
        "difficulty": "Intermediate",
        "project": "Configure Automated Unit Tests, Docker Image Builds and Cloud Auto-Deploy"
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
        # 3. Dynamic High-Quality Fallback
        if s_key in db_lookup:
            c_info = db_lookup[s_key]
            duration = int(c_info.get("duration_weeks") or 2)
            roadmap.append(RoadmapEntry(
                week=week,
                skill=s_clean,
                course=c_info.get("course_name") or f"Mastering {s_clean}",
                platform=c_info.get("platform") or "NPTEL / Coursera",
                url=c_info.get("url") or f"https://www.google.com/search?q={s_clean}+online+course",
                project=f"Build a production-ready application implementing {s_clean}",
                duration=f"{duration} week(s)",
                is_free=bool(c_info.get("is_free", True)),
                difficulty=c_info.get("difficulty") or "Intermediate"
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
                difficulty=c_info["difficulty"]
            ))
            week += max(1, duration)
        else:
            duration = 1
            roadmap.append(RoadmapEntry(
                week=week,
                skill=s_clean,
                course=f"Comprehensive {s_clean} Fundamentals & Applied Projects",
                platform="freeCodeCamp / NPTEL",
                url=f"https://www.youtube.com/results?search_query={s_clean}+full+course",
                project=f"Implement a hands-on project demonstrating core competencies in {s_clean}",
                duration="1-2 week(s)",
                is_free=True,
                difficulty="Beginner"
            ))
            week += 2
            
    return roadmap
