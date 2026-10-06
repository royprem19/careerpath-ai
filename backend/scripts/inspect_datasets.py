import sys
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

data_dir = Path(__file__).resolve().parent.parent / "data"

print("==================================================================")
print("INSPECTING REAL INDIAN JOB MARKET DATASETS IN backend/data/")
print("==================================================================")

fresher_csv = data_dir / "Indian_Fresher_Salary_Skills_2025.csv"
if fresher_csv.exists():
    print(f"\n1. {fresher_csv.name}:")
    df_fresh = pd.read_csv(fresher_csv)
    print(f"   Shape: {df_fresh.shape} (Rows: {len(df_fresh)}, Columns: {len(df_fresh.columns)})")
    print(f"   Columns: {list(df_fresh.columns)}")
    print("   Sample Row:")
    print(df_fresh.head(1).to_dict(orient="records"))

tech_jobs_csv = data_dir / "india_job_market_2024_2026.csv"
if tech_jobs_csv.exists():
    print(f"\n2. {tech_jobs_csv.name}:")
    df_tech = pd.read_csv(tech_jobs_csv)
    print(f"   Shape: {df_tech.shape} (Rows: {len(df_tech)}, Columns: {len(df_tech.columns)})")
    print(f"   Columns: {list(df_tech.columns)}")
    print("   Sample Row:")
    print(df_tech.head(1).to_dict(orient="records"))

xlsx_file = data_dir / "indian-job-market-dataset-2025.xlsx"
if xlsx_file.exists():
    print(f"\n3. {xlsx_file.name}:")
    # Read sheet names or head of first sheet
    xl = pd.ExcelFile(xlsx_file)
    print(f"   Sheet names: {xl.sheet_names}")
    df_xl = xl.parse(xl.sheet_names[0], nrows=5)
    print(f"   Columns: {list(df_xl.columns)}")
    print("   Sample Row:")
    print(df_xl.head(1).to_dict(orient="records"))

print("\n✓ Inspection complete!")
