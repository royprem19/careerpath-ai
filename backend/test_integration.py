"""
CareerPath AI - Full Stack Integration Test
Verifies all FastAPI backend endpoints against real Supabase database and ML models.
"""

import sys
import json
from pathlib import Path
from fastapi.testclient import TestClient

sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
backend_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from backend.main import app

client = TestClient(app)

def run_tests():
    print("==================================================================")
    print("CAREERPATH AI - FULL STACK END-TO-END VERIFICATION")
    print("==================================================================")

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("1. [PASS] GET /health ->", res.json())

    # 2. ML Metrics
    res = client.get("/api/ml/metrics")
    assert res.status_code == 200, f"ML metrics failed: {res.text}"
    ml_data = res.json()
    sal_model = ml_data.get("salary_model", {})
    metrics = sal_model.get("metrics", {})
    print(f"2. [PASS] GET /api/ml/metrics -> Model: {ml_data.get('model')}")
    print(f"   • R^2 Score: {metrics.get('test_r2')} | Test MAE: {metrics.get('test_mae_lpa')} LPA")
    print(f"   • Tracked Skills Count: {ml_data.get('tracked_skills_count')}")
    print(f"   • Empirical Indian Roles: {ml_data.get('empirical_indian_roles_count')}")

    # 3. Roles list
    res = client.get("/api/roles")
    assert res.status_code == 200, f"Get roles failed: {res.text}"
    roles = res.json()
    assert len(roles) >= 30, f"Expected at least 30 roles, got {len(roles)}"
    print(f"3. [PASS] GET /api/roles -> Returned {len(roles)} live roles from Supabase/benchmarks")
    target_role = roles[0]
    print(f"   • Sample role: {target_role.get('title')} ({target_role.get('category')}) | {target_role.get('avg_salary')}")
    print(f"   • Essential skills count: {len(target_role.get('essential_skills', []))}")

    # 4. Gap Analysis
    sample_skills = ["Python", "FastAPI", "React", "Docker", "SQL"]
    gap_payload = {
        "user_skills": sample_skills,
        "target_role_id": target_role["id"]
    }
    res = client.post("/api/analysis/gap", json=gap_payload)
    assert res.status_code == 200, f"Gap analysis failed: {res.text}"
    gap_res = res.json()
    print("4. [PASS] POST /api/analysis/gap ->")
    print(f"   • Fit Score: {gap_res.get('fit_score')}%")
    print(f"   • Essential Coverage: {gap_res.get('essential_coverage')}%")
    print(f"   • Matched Skills: {gap_res.get('matched_skills')}")
    print(f"   • Missing Essential: {gap_res.get('missing_essential')}")
    print(f"   • ML Predicted CTC: {gap_res.get('predicted_salary')}")
    print(f"   • Missing Skill Velocities: {len(gap_res.get('skill_velocities', []))} tracked")

    # 5. Career Recommendations
    rec_payload = {
        "user_skills": sample_skills,
        "user_education": ["B.Tech"],
        "user_experience": {"years": 1}
    }
    res = client.post("/api/recommendations", json=rec_payload)
    assert res.status_code == 200, f"Recommendations failed: {res.text}"
    recs = res.json()
    print(f"5. [PASS] POST /api/recommendations -> Generated {len(recs)} top role recommendations")
    for r in recs[:3]:
        print(f"   • {r.get('role_title')}: Score {r.get('score')}% | {r.get('explanation')}")

    # 6. Upskilling Roadmap
    missing_sample = gap_res.get("missing_essential", []) or ["Kubernetes", "AWS"]
    rm_payload = {
        "missing_skills": missing_sample,
        "preferences": {}
    }
    res = client.post("/api/roadmap", json=rm_payload)
    assert res.status_code == 200, f"Roadmap failed: {res.text}"
    rm = res.json()
    entries = rm.get("entries", [])
    print(f"6. [PASS] POST /api/roadmap -> Generated {len(entries)} modules for missing skills")
    if entries:
        print(f"   • W{entries[0].get('week')}: {entries[0].get('skill')} -> {entries[0].get('course')} ({entries[0].get('platform')})")

    # 7. PDF Report Generation
    pdf_payload = {
        "user_profile": {
            "skills": sample_skills,
            "education": ["B.Tech"],
            "experience": "1 year"
        },
        "gap_analysis": gap_res,
        "recommendations": recs[:5],
        "roadmap": entries[:5]
    }
    res = client.post("/api/report/pdf", json=pdf_payload)
    assert res.status_code == 200, f"PDF report generation failed: {res.text}"
    assert res.headers.get("content-type") == "application/pdf"
    print(f"7. [PASS] POST /api/report/pdf -> Generated valid PDF ({len(res.content)} bytes)")

    # 8. Candidate Authentication (Dynamic registration & login, JWT verification)
    reg_payload = {
        "email": "candidate_test@campus.ac.in",
        "password": "Password@123",
        "user_name": "Rohan Patel",
        "role": "candidate",
        "institution_name": "IIT Madras",
        "department": "Computer Science & Engineering",
        "graduation_year": 2026,
        "skills": []
    }
    client.post("/api/auth/register", json=reg_payload)
    res = client.post("/api/auth/login", json={"email": "candidate_test@campus.ac.in", "password": "Password@123"})
    assert res.status_code == 200, f"Student login failed: {res.text}"
    auth_data = res.json()
    token = auth_data["access_token"]
    user = auth_data["user"]
    assert user["role"] == "candidate"
    assert user["skills"] == []
    print(f"8. [PASS] POST /api/auth/login -> Logged in as student: {user['user_name']} (Skills: {user['skills']})")
    
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200, f"Token verification failed: {me_res.text}"
    print(f"   • Token verified successfully for {me_res.json()['email']}")

    # 8b. Profile Update (User edits name, college, department, grad year)
    update_res = client.put(
        "/api/auth/profile",
        json={
            "user_name": "Rohan A. Patel",
            "institution_name": "BITS Pilani, Goa Campus",
            "department": "Data Science & Artificial Intelligence",
            "graduation_year": 2027
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_res.status_code == 200, f"Profile update failed: {update_res.text}"
    updated_user = update_res.json()
    assert updated_user["user_name"] == "Rohan A. Patel"
    assert updated_user["institution_name"] == "BITS Pilani, Goa Campus"
    print(f"   • Profile updated successfully: {updated_user['user_name']} | {updated_user['institution_name']}")

    # 9. Security Gate: Verify unauthenticated resume upload is strictly rejected with 401
    unauth_res = client.post("/api/resume/upload", files={"file": ("resume.txt", b"Python SQL", "text/plain")})
    assert unauth_res.status_code == 401, f"Expected 401, got {unauth_res.status_code}"
    print("9. [PASS] POST /api/resume/upload -> Correctly rejected with 401 Unauthorized when unauthenticated")

    # 10. Authenticated Resume Upload: Verify authenticated candidate can upload and extract skills
    sample_resume_bytes = b"Experienced Software Engineer with proficiency in Python, FastAPI, Docker, and PostgreSQL."
    auth_upload_res = client.post(
        "/api/resume/upload", 
        files={"file": ("test_resume.txt", sample_resume_bytes, "text/plain")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert auth_upload_res.status_code == 200, f"Authenticated upload failed: {auth_upload_res.text}"
    uploaded_profile = auth_upload_res.json()
    assert "Python" in uploaded_profile["skills"], "Expected Python in extracted skills"
    print(f"10. [PASS] POST /api/resume/upload -> Successfully extracted {len(uploaded_profile['skills'])} skills with verified auth token")

    print("\n==================================================================")
    print("ALL 10 CORE FASTAPI, ML, CANDIDATE AUTH & SECURITY SERVICES PASSED!")
    print("==================================================================")

if __name__ == "__main__":
    run_tests()
