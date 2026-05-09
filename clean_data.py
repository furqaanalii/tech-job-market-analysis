"""
clean_data.py
Cleans raw job postings: normalizes titles, handles nulls,
explodes skills into a separate table, saves processed outputs.
"""
import pandas as pd
import sqlite3
import os

RAW  = "/home/claude/tech-job-market-analysis/data/raw/job_postings.csv"
PROC = "/home/claude/tech-job-market-analysis/data/processed"
DB   = "/home/claude/tech-job-market-analysis/data/processed/jobs.db"

os.makedirs(PROC, exist_ok=True)

# --- Load ---
df = pd.read_csv(RAW)
print(f"Loaded {len(df):,} rows")

# --- Nulls ---
print(f"Nulls before: {df.isnull().sum().sum()}")
df = df.dropna()
print(f"Rows after null drop: {len(df):,}")

# --- Types ---
df["date_posted"] = pd.to_datetime(df["date_posted"])
df["salary"] = df["salary"].astype(int)
df["year"]  = df["date_posted"].dt.year
df["month"] = df["date_posted"].dt.month

# --- Normalize city labels ---
df["city_short"] = df["city"].str.replace(r",.*", "", regex=True)
df.loc[df["city"] == "Remote", "city_short"] = "Remote"

# --- Salary bands ---
def salary_band(s):
    if s < 70000:  return "< $70K"
    if s < 100000: return "$70K–$100K"
    if s < 130000: return "$100K–$130K"
    if s < 160000: return "$130K–$160K"
    return "$160K+"

df["salary_band"] = df["salary"].apply(salary_band)

# --- Explode skills into long format ---
skills_long = (
    df[["job_id", "title", "experience", "city_short", "industry"]]
    .assign(skill=df["skills"].str.split(", "))
    .explode("skill")
    .reset_index(drop=True)
)
skills_long["skill"] = skills_long["skill"].str.strip()

# --- Save cleaned CSV ---
df.to_csv(f"{PROC}/jobs_clean.csv", index=False)
skills_long.to_csv(f"{PROC}/skills_long.csv", index=False)
print(f"Saved jobs_clean.csv ({len(df):,} rows)")
print(f"Saved skills_long.csv ({len(skills_long):,} rows)")

# --- Load into SQLite ---
conn = sqlite3.connect(DB)
df.to_sql("jobs", conn, if_exists="replace", index=False)
skills_long.to_sql("skills", conn, if_exists="replace", index=False)
conn.close()
print(f"SQLite DB written: {DB}")

print("\nCleaning complete.")
print(df[["title", "city_short", "experience", "salary", "work_mode"]].describe(include="all").to_string())
