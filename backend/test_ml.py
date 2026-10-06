import sys
from pathlib import Path

# Force UTF-8 output encoding for Windows command line compatibility
sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.services.ml_engine import salary_predictor, vector_matcher, analyze_skill_market_velocity

print("1. Testing ML Compensation Prediction...")
res = salary_predictor.predict_compensation(num_skills=7, years_exp=1.5, essential_ratio=0.85, is_ai_or_cloud=True)
print("   Predicted:", res)

print("\n2. Testing Emerging Skill Market Velocity...")
skills_sample = ["large language models (llms)", "fastapi", "docker", "tableau"]
velocities = analyze_skill_market_velocity(skills_sample)
for v in velocities:
    print(f"   - {v['skill']}: Velocity {v['velocity_score']}/100 ({v['trend']})")

print("\n3. Testing Semantic Vector Similarity...")
roles_sample = [
    {"id": "1", "title": "Data Scientist", "description": "Build ML models and statistics", "essential_skills": ["Python", "SQL", "Machine Learning"], "optional_skills": ["Pandas"]},
    {"id": "2", "title": "Frontend Engineer", "description": "Build web UIs with React and CSS", "essential_skills": ["JavaScript", "React"], "optional_skills": ["HTML5"]}
]
vector_matcher.fit_corpus(roles_sample)
sims = vector_matcher.compute_similarity("I know Python, SQL and built a machine learning random forest model")
print("   Semantic similarities:", sims)
print("\n[OK] All ML & NLP Components Functional!")
