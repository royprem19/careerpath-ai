"""
Ingest real occupation and skill data directly from the official ESCO Web Service API.
European Commission ESCO Portal: https://ec.europa.eu/esco/api/
"""

import sys
import json
import time
import requests
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent.parent
backend_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from backend.database import get_supabase

# Target search queries for Indian Tech & Workforce priority domains
SEARCH_QUERIES = [
    "software developer",
    "data scientist",
    "web developer",
    "systems analyst",
    "database administrator",
    "computer network",
    "information security",
    "machine learning",
    "digital games developer",
    "cloud"
]

ESCO_SEARCH_URL = "https://ec.europa.eu/esco/api/search"
ESCO_RESOURCE_URL = "https://ec.europa.eu/esco/api/resource/occupation"

def fetch_esco_occupations():
    occupations_data = []
    seen_uris = set()

    print(" Connecting to European Commission ESCO Web Service API...")

    for query in SEARCH_QUERIES:
        print(f"\n🔍 Searching ESCO for: '{query}'...")
        try:
            params = {
                "type": "occupation",
                "text": query,
                "language": "en",
                "limit": 5
            }
            resp = requests.get(ESCO_SEARCH_URL, params=params, timeout=15)
            if resp.status_code != 200:
                print(f"  ❌ Query failed: HTTP {resp.status_code}")
                continue

            data = resp.json()
            hits = data.get("_embedded", {}).get("results", [])
            print(f"  Found {len(hits)} matching occupations")

            for hit in hits:
                occ_uri = hit.get("uri")
                occ_title = hit.get("title")

                if not occ_uri or occ_uri in seen_uris:
                    continue
                seen_uris.add(occ_uri)

                # Fetch deep occupation details with skills
                try:
                    detail_resp = requests.get(ESCO_RESOURCE_URL, params={"uri": occ_uri, "language": "en"}, timeout=15)
                    if detail_resp.status_code == 200:
                        detail = detail_resp.json()
                        links = detail.get("_links", {})
                        
                        essential_skills = [
                            s.get("title") for s in links.get("hasEssentialSkill", []) 
                            if s.get("title")
                        ]
                        optional_skills = [
                            s.get("title") for s in links.get("hasOptionalSkill", []) 
                            if s.get("title")
                        ]
                        
                        desc_obj = detail.get("description", {})
                        desc_text = desc_obj.get("en", {}).get("literal", "") if isinstance(desc_obj, dict) else str(desc_obj)
                        
                        record = {
                            "title": occ_title.title(),
                            "esco_uri": occ_uri,
                            "code": detail.get("code", "ISCO-25"),
                            "description": desc_text[:300] if desc_text else f"Professional role for {occ_title}.",
                            "essential_skills": essential_skills[:15],
                            "optional_skills": optional_skills[:15]
                        }
                        occupations_data.append(record)
                        print(f"  ✓ Ingested '{record['title']}': {len(essential_skills)} essential, {len(optional_skills)} optional skills")
                except Exception as err:
                    print(f"  ⚠️ Error fetching details for {occ_title}: {err}")
                
                time.sleep(0.3)  # Respect ESCO API rate limits

        except Exception as e:
            print(f"  ❌ Search request failed for '{query}': {e}")

    return occupations_data

def sync_to_supabase_or_file(occupations):
    out_file = backend_dir / "data" / "esco_ingested_roles.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(occupations, f, indent=2, ensure_ascii=False)
    print(f"\n Saved {len(occupations)} live ESCO occupations to {out_file}")

    # Sync to Supabase if configured
    supabase = get_supabase()
    if supabase:
        print("\n Syncing live ESCO data into Supabase database...")
        for occ in occupations:
            try:
                # 1. Insert role
                role_row = {
                    "title": occ["title"],
                    "category": "Technology & ICT (ESCO)",
                    "description": occ["description"],
                    "experience_range": "1-3 years",
                    "avg_salary": "₹8 - 16 LPA",
                    "nco_code": occ.get("code", "2512.01"),
                    "esco_uri": occ["esco_uri"]
                }
                res = supabase.table("roles").upsert(role_row, on_conflict="title").execute()
                role_id = res.data[0]["id"] if res.data else None

                if role_id:
                    # 2. Insert skills & mappings
                    for s_name in occ["essential_skills"]:
                        s_res = supabase.table("skills").upsert({"name": s_name, "category": "ESCO Essential"}, on_conflict="name").execute()
                        if s_res.data:
                            s_id = s_res.data[0]["id"]
                            supabase.table("role_skills").upsert({"role_id": role_id, "skill_id": s_id, "relation_type": "essential"}, on_conflict="role_id,skill_id").execute()

                    for s_name in occ["optional_skills"]:
                        s_res = supabase.table("skills").upsert({"name": s_name, "category": "ESCO Optional"}, on_conflict="name").execute()
                        if s_res.data:
                            s_id = s_res.data[0]["id"]
                            supabase.table("role_skills").upsert({"role_id": role_id, "skill_id": s_id, "relation_type": "optional"}, on_conflict="role_id,skill_id").execute()
                            
                    print(f"  ✓ Synced to Supabase: {occ['title']}")
            except Exception as sync_err:
                print(f"  ⚠️ Supabase sync warning for {occ['title']}: {sync_err}")
    else:
        print("\nℹ Supabase connection not set in backend/.env; saved to local cache for API serving.")

if __name__ == "__main__":
    data = fetch_esco_occupations()
    sync_to_supabase_or_file(data)
    print("\n ESCO live ingestion complete!")
