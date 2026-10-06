"""
Sync the ingested live ESCO dataset directly into Supabase tables using the Service Role Key.
"""

import sys
import json
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent.parent
backend_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from backend.database import get_supabase

def sync_data():
    json_path = backend_dir / "data" / "esco_ingested_roles.json"
    if not json_path.exists():
        print(f"❌ Error: {json_path} not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        roles_data = json.load(f)

    supabase = get_supabase()
    if not supabase:
        print("❌ Error: Could not connect to Supabase. Check backend/.env.")
        return

    print(f" Connecting to Supabase to sync {len(roles_data)} real ESCO occupations...")

    total_roles = 0
    total_skills = 0
    total_mappings = 0

    for occ in roles_data:
        title = occ["title"]
        try:
            # 1. Upsert Role
            role_payload = {
                "title": title,
                "category": "Technology & ICT (ESCO)",
                "description": occ["description"],
                "experience_range": "0-3 years",
                "avg_salary": "₹7 - 16 LPA",
                "nco_code": occ.get("code", "2512.01"),
                "esco_uri": occ.get("esco_uri")
            }
            res = supabase.table("roles").upsert(role_payload, on_conflict="title").execute()
            if not res.data:
                # If select needed
                s_res = supabase.table("roles").select("id").eq("title", title).execute()
                role_id = s_res.data[0]["id"] if s_res.data else None
            else:
                role_id = res.data[0]["id"]

            if not role_id:
                continue

            total_roles += 1

            # 2. Insert Essential Skills
            for s_name in occ.get("essential_skills", []):
                s_name = s_name.strip()
                if not s_name:
                    continue
                # Upsert skill
                sk_res = supabase.table("skills").upsert({"name": s_name, "category": "ESCO Technical Competency"}, on_conflict="name").execute()
                if sk_res.data:
                    skill_id = sk_res.data[0]["id"]
                else:
                    sel = supabase.table("skills").select("id").eq("name", s_name).execute()
                    skill_id = sel.data[0]["id"] if sel.data else None

                if skill_id:
                    total_skills += 1
                    # Upsert relation
                    rel_payload = {"role_id": role_id, "skill_id": skill_id, "relation_type": "essential"}
                    supabase.table("role_skills").upsert(rel_payload, on_conflict="role_id,skill_id").execute()
                    total_mappings += 1

            # 3. Insert Optional Skills
            for s_name in occ.get("optional_skills", []):
                s_name = s_name.strip()
                if not s_name:
                    continue
                sk_res = supabase.table("skills").upsert({"name": s_name, "category": "ESCO Optional Competency"}, on_conflict="name").execute()
                if sk_res.data:
                    skill_id = sk_res.data[0]["id"]
                else:
                    sel = supabase.table("skills").select("id").eq("name", s_name).execute()
                    skill_id = sel.data[0]["id"] if sel.data else None

                if skill_id:
                    rel_payload = {"role_id": role_id, "skill_id": skill_id, "relation_type": "optional"}
                    supabase.table("role_skills").upsert(rel_payload, on_conflict="role_id,skill_id").execute()
                    total_mappings += 1

            print(f"  ✓ Synced: {title}")
        except Exception as e:
            print(f"  ⚠️ Error syncing {title}: {e}")

    print("\n Sync completed successfully!")
    print(f"  • Roles Synced: {total_roles}")
    print(f"  • Total Role-Skill Relations Synced: {total_mappings}")

if __name__ == "__main__":
    sync_data()
