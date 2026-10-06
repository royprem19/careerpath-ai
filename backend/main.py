import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Configure UTF-8 stdout for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

# Add both root and backend directory to sys.path for universal import compatibility
root_dir = Path(__file__).resolve().parent.parent
backend_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import resume, roles, analysis, recommendations, roadmap, report, auth
from backend.database import get_supabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Supabase client
    client = get_supabase()
    if client:
        print("✓ Supabase client connected successfully")
    else:
        print("ℹ Supabase credentials not set or pending; operating in resilient real-dataset mode")
    yield

app = FastAPI(
    title="CareerPath AI - Backend API",
    description="Intelligent Talent & Workforce Ecosystem API for Build For Bharat 2.0",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(roles.router)
app.include_router(analysis.router)
app.include_router(recommendations.router)
app.include_router(roadmap.router)
app.include_router(report.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "CareerPath AI", "version": "2.0.0"}

@app.get("/api/ml/metrics")
async def get_ml_metrics():
    import json
    model_file = backend_dir / "data" / "trained_salary_model.json"
    vel_file = backend_dir / "data" / "skill_market_velocity.json"
    roles_file = backend_dir / "data" / "indian_role_benchmarks.json"
    
    metrics = {
        "status": "ready",
        "model": "NumPyRidgeRegressor (Closed-Form Analytical)",
        "datasets": [
            "Indian_Fresher_Salary_Skills_2025.csv (500 rows)",
            "india_job_market_2024_2026.csv (5,000 rows)",
            "indian-job-market-dataset-2025.xlsx (97,000+ listings sampled)",
            "ESCO European Commission Official API (42 roles, 788 skills)"
        ]
    }
    if model_file.exists():
        with open(model_file, "r", encoding="utf-8") as f:
            metrics["salary_model"] = json.load(f)
    if vel_file.exists():
        with open(vel_file, "r", encoding="utf-8") as f:
            v_data = json.load(f)
            metrics["tracked_skills_count"] = len(v_data)
    if roles_file.exists():
        with open(roles_file, "r", encoding="utf-8") as f:
            r_data = json.load(f)
            metrics["empirical_indian_roles_count"] = len(r_data)
            
    return metrics

if __name__ == "__main__":
    import uvicorn
    # Watch only source folders excluding .venv to enable instant live updates
    watch_dirs = [
        str(backend_dir / "routers"),
        str(backend_dir / "services"),
        str(backend_dir / "models")
    ]
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=watch_dirs)
