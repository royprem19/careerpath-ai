"""
Seed Supabase database programmatically using supabase-py.
Reads credentials from backend/.env or environment variables.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Prefer SERVICE_KEY for migrations/seeding, fallback to ANON_KEY
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or "your_supabase" in SUPABASE_URL:
    print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY / SUPABASE_SERVICE_KEY must be set in backend/.env")
    print(f"Current SUPABASE_URL: {SUPABASE_URL}")
    sys.exit(1)

try:
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f" Connected to Supabase at: {SUPABASE_URL}")
except Exception as e:
    print(f"❌ Failed to connect to Supabase: {e}")
    sys.exit(1)

def run_verification():
    print("\n🔍 Verifying Supabase Tables...")
    tables = ["roles", "skills", "role_skills", "courses", "skill_synonyms"]
    for tbl in tables:
        try:
            res = supabase.table(tbl).select("count", count="exact").execute()
            print(f"  ✓ Table '{tbl}': {res.count} records")
        except Exception as err:
            print(f"  ❌ Table '{tbl}' could not be queried: {err}")
            print(f"     👉 Please run supabase_schema.sql in your Supabase SQL Editor!")

if __name__ == "__main__":
    run_verification()
