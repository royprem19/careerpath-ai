import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent.parent
json_file = root_dir / "backend" / "data" / "esco_ingested_roles.json"
sql_file = root_dir / "supabase_esco_dataset.sql"

with open(json_file, "r", encoding="utf-8") as f:
    roles = json.load(f)

lines = [
    "-- ==============================================================================\n",
    "-- Live Ingested ESCO Occupations & Skills (European Commission ESCO Web API)\n",
    "-- ==============================================================================\n\n"
]

for r in roles:
    title = r["title"].replace("'", "''")
    desc = r["description"].replace("'", "''")
    code = r.get("code", "ISCO-25").replace("'", "''")
    uri = r.get("esco_uri", "").replace("'", "''")
    lines.append(
        f"INSERT INTO roles (title, category, description, nco_code, esco_uri) "
        f"VALUES ('{title}', 'ESCO Technology', '{desc}', '{code}', '{uri}') "
        f"ON CONFLICT (title) DO NOTHING;\n"
    )

lines.append("\n-- Skills from ESCO\n")
all_skills = set()
for r in roles:
    for s in r.get("essential_skills", []):
        all_skills.add((s.strip(), "ESCO Essential"))
    for s in r.get("optional_skills", []):
        all_skills.add((s.strip(), "ESCO Optional"))

for s_name, cat in all_skills:
    s_escaped = s_name.replace("'", "''")
    lines.append(
        f"INSERT INTO skills (name, category) VALUES ('{s_escaped}', '{cat}') ON CONFLICT (name) DO NOTHING;\n"
    )

with open(sql_file, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"✓ Generated {sql_file} with {len(roles)} live ESCO occupations and {len(all_skills)} real skills!")
