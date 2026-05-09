import pandas as pd
import numpy as np
import random
import json
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# --- CONFIG ---
N = 8000

JOB_ROLES = {
    "Data Analyst":         {"base": 72000,  "sd": 14000, "weight": 22},
    "Data Scientist":       {"base": 118000, "sd": 22000, "weight": 16},
    "Data Engineer":        {"base": 125000, "sd": 20000, "weight": 14},
    "BI Analyst":           {"base": 82000,  "sd": 15000, "weight": 12},
    "ML Engineer":          {"base": 138000, "sd": 25000, "weight": 8},
    "IT Analyst":           {"base": 68000,  "sd": 12000, "weight": 10},
    "Systems Analyst":      {"base": 75000,  "sd": 13000, "weight": 8},
    "Database Administrator":{"base": 88000, "sd": 14000, "weight": 6},
    "Analytics Engineer":   {"base": 115000, "sd": 18000, "weight": 4},
}

CITIES = {
    "San Francisco, CA": 1.35,
    "New York, NY":      1.30,
    "Seattle, WA":       1.22,
    "Boston, MA":        1.18,
    "Austin, TX":        1.05,
    "Dallas, TX":        1.00,
    "Chicago, IL":       1.03,
    "Denver, CO":        1.08,
    "Atlanta, GA":       0.97,
    "Remote":            1.10,
}

EXPERIENCE_LEVELS = {
    "Entry":  {"mult": 0.75, "weight": 30},
    "Mid":    {"mult": 1.00, "weight": 45},
    "Senior": {"mult": 1.40, "weight": 25},
}

INDUSTRIES = ["Tech", "Finance", "Healthcare", "Retail", "Consulting",
              "Media", "Government", "Education", "Manufacturing"]

# Skills by role — realistic combos
ROLE_SKILLS = {
    "Data Analyst":          ["SQL", "Excel", "Tableau", "Python", "Power BI", "R", "Looker", "Google Analytics", "Statistics"],
    "Data Scientist":        ["Python", "SQL", "Machine Learning", "Scikit-learn", "TensorFlow", "R", "Statistics", "Spark", "Jupyter", "NumPy", "pandas"],
    "Data Engineer":         ["Python", "SQL", "Spark", "AWS", "Azure", "Kafka", "Airflow", "dbt", "Hadoop", "Scala", "Docker"],
    "BI Analyst":            ["Tableau", "Power BI", "SQL", "Excel", "Looker", "DAX", "Google Analytics", "Python"],
    "ML Engineer":           ["Python", "TensorFlow", "PyTorch", "SQL", "Scikit-learn", "AWS", "Docker", "Kubernetes", "MLflow", "Spark"],
    "IT Analyst":            ["SQL", "Excel", "ITIL", "ServiceNow", "Networking", "Windows Server", "Azure", "Python", "Jira"],
    "Systems Analyst":       ["SQL", "Excel", "UML", "Jira", "JIRA", "Python", "Visio", "Agile", "ServiceNow"],
    "Database Administrator":["SQL", "Oracle", "PostgreSQL", "MySQL", "Azure", "AWS", "Python", "Shell Scripting", "Performance Tuning"],
    "Analytics Engineer":    ["SQL", "dbt", "Python", "Looker", "Airflow", "Spark", "Snowflake", "Tableau", "Git"],
}

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "Salesforce", "Oracle",
    "IBM", "Deloitte", "Accenture", "PwC", "KPMG", "JPMorgan Chase", "Goldman Sachs",
    "Bank of America", "Citi", "Wells Fargo", "UnitedHealth", "CVS Health",
    "Walmart", "Target", "Nike", "Pfizer", "Johnson & Johnson", "Boeing",
    "Lockheed Martin", "AT&T", "Verizon", "T-Mobile", "Netflix", "Uber",
    "Lyft", "Airbnb", "Stripe", "Snowflake", "Databricks", "Palantir",
    "DataRobot", "Tableau Software", "MicroStrategy", "Teradata", "Cloudera",
    "Startup A", "Startup B", "Startup C", "Regional Bank", "City Hospital",
    "State Agency", "University Research", "Consulting Firm X", "Consulting Firm Y",
]

WORK_MODES = {"Onsite": 38, "Hybrid": 42, "Remote": 20}

rows = []
roles = list(JOB_ROLES.keys())
role_weights = [JOB_ROLES[r]["weight"] for r in roles]

exp_levels = list(EXPERIENCE_LEVELS.keys())
exp_weights = [EXPERIENCE_LEVELS[e]["weight"] for e in exp_levels]

cities = list(CITIES.keys())
city_weights = [5 if c != "Remote" else 15 for c in cities]

work_mode_list = list(WORK_MODES.keys())
work_mode_weights = list(WORK_MODES.values())

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 3, 31)
date_range = (end_date - start_date).days

for i in range(N):
    role = random.choices(roles, weights=role_weights)[0]
    exp  = random.choices(exp_levels, weights=exp_weights)[0]
    city = random.choices(cities, weights=city_weights)[0]
    mode = random.choices(work_mode_list, weights=work_mode_weights)[0]

    if city == "Remote":
        mode = "Remote"

    base   = JOB_ROLES[role]["base"]
    sd     = JOB_ROLES[role]["sd"]
    city_m = CITIES[city]
    exp_m  = EXPERIENCE_LEVELS[exp]["mult"]

    salary = int(np.random.normal(base * city_m * exp_m, sd))
    salary = max(40000, min(280000, salary))
    # Round to nearest 5k
    salary = round(salary / 5000) * 5000

    industry = random.choice(INDUSTRIES)
    company  = random.choice(COMPANIES)

    # Pick 3–6 skills from role pool
    pool = ROLE_SKILLS[role]
    n_skills = random.randint(3, min(6, len(pool)))
    skills = random.sample(pool, n_skills)

    posted = start_date + timedelta(days=random.randint(0, date_range))

    rows.append({
        "job_id":         i + 1,
        "title":          role,
        "company":        company,
        "city":           city,
        "industry":       industry,
        "experience":     exp,
        "work_mode":      mode,
        "salary":         salary,
        "skills":         ", ".join(skills),
        "date_posted":    posted.strftime("%Y-%m-%d"),
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/tech-job-market-analysis/data/raw/job_postings.csv", index=False)
print(f"Generated {len(df)} job postings")
print(df.head(3).to_string())
print(f"\nSalary range: ${df['salary'].min():,} – ${df['salary'].max():,}")
print(f"Roles: {df['title'].value_counts().to_dict()}")
