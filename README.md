# 🇮🇳 CareerPath AI — Intelligent Talent & Workforce Ecosystem

> **Build For Bharat 2.0 Hackathon Project**
> An AI-powered Career Intelligence Platform connecting individual talent capabilities to real industry demand through Quantified Skill Gap Analysis and Explainable Learning Roadmaps.

---

## 🌟 Key Capabilities

1. **Resume Ingestion & Parsing**: High-performance extraction of text, skills, education, and experience from PDF, DOCX, and TXT using PyMuPDF and python-docx.
2. **Standardized Skill Normalization**: 300+ skill taxonomy mapped with 75+ alias synonyms (e.g., `ML` → `Machine Learning`, `k8s` → `Kubernetes`, `React.js` → `React`).
3. **Quantified Skill Gap Analysis**:
   - $70\%$ weighting on essential skills + $30\%$ weighting on optional competencies
   - Exact gap breakdown (matched, missing essential, missing optional, and surplus skills)
4. **Explainable Role Recommendations**: Ranks alternative careers with transparent reasoning based on real market demand.
5. **Personalized Learning Roadmaps**: Week-by-week curriculum mapped to **real courses** from **NPTEL (IITs)**, **Coursera**, and **freeCodeCamp**, accompanied by hands-on capstone project tasks.
6. **Automated PDF Export**: One-click professional report download for placement cells, mentors, and students.
7. **Production Supabase Database**: Real tables for roles, skills, role-skills relationships, courses, and synonyms.

---

## 🗄️ Setting Up Your Supabase Database

1. Log into your [Supabase Dashboard](https://supabase.com/dashboard).
2. Create a new project (e.g., `careerpath-ai`, Mumbai region).
3. Open the **SQL Editor** in your Supabase project.
4. Copy and paste the entire contents of [`supabase_schema.sql`](./supabase_schema.sql) and click **Run**.
   - This sets up all 7 tables (`roles`, `skills`, `role_skills`, `courses`, `skill_synonyms`, `user_profiles`, `gap_analyses`).
   - Seeds 15 high-demand industry roles calibrated to Indian job postings (Naukri 2025).
   - Seeds 85+ master skills, 50+ real courses, and 75+ synonym normalization rules.
   - Enables Row Level Security (RLS) with public read access.
5. In Supabase **Project Settings → API**, copy your **Project URL** and **anon public key**.
6. Open `backend/.env` and update:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-actual-anon-key
   SUPABASE_SERVICE_KEY=your-actual-service-key
   ```
7. *(Optional)* Verify connection from terminal:
   ```powershell
   .\backend\.venv\Scripts\python.exe backend/seed_supabase.py
   ```

---

## 🚀 Running the Project

### Option A: One-Click Launchers (Windows)
- Double click `run_backend.bat` to start the FastAPI server at `http://localhost:8000`.
- Double click `run_frontend.bat` to start the React + Vite UI at `http://localhost:5173`.

### Option B: Terminal Commands
**Terminal 1 — Backend:**
```powershell
cd backend
.\.venv\Scripts\python.exe main.py
# Server runs on http://localhost:8000
# OpenAPI Docs: http://localhost:8000/docs
```

**Terminal 2 — Frontend:**
```powershell
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/resume/upload` | Upload PDF/DOCX resume & extract skill profile |
| `POST` | `/api/skills/normalize` | Normalize manual skill inputs via synonyms |
| `GET` | `/api/roles` | List all 15 industry roles with skill counts |
| `GET` | `/api/roles/{id}` | Detailed role requirements (essential vs optional) |
| `POST` | `/api/analysis/gap` | Calculate quantified skill gap & explainability |
| `POST` | `/api/recommendations` | Rank alternative career roles by fit score |
| `POST` | `/api/roadmap` | Generate week-by-week learning roadmap & projects |
| `POST` | `/api/report/pdf` | Generate downloadable PDF summary report |
| `GET` | `/health` | API health check |
