# Tech Job Market Analysis (2023–2025)

**Tools:** Python · SQL (SQLite) · pandas · matplotlib · Tableau  
**Dataset:** 8,000 tech and data job postings across 9 roles, 10 cities, and 9 industries

---

## What This Project Does

Analyzes a dataset of 8,000 tech job postings to answer the questions that matter most to early-career data professionals:

- Which skills do employers actually require most?
- How much does salary vary by role, city, and experience level?
- What does the remote vs. onsite breakdown look like?
- What skills specifically drive Data Analyst hiring?

---

## Key Findings

| Finding | Detail |
|---|---|
| Top 2 skills across all roles | Python (10.6%) and SQL (10.6%) — tied |
| Highest-paying role | ML Engineer ($160K avg) |
| Entry-level Data Analyst avg salary | $61K |
| Salary jump: Entry → Senior | +$70K on average |
| Work mode split | 40.8% Remote, 31.5% Hybrid, 27.8% Onsite |
| San Francisco premium over Dallas | ~$31K higher avg salary |
| Top skill for Data Analyst roles | Tableau (appears in 52% of postings) |

---

## Project Structure

```
tech-job-market-analysis/
├── data/
│   ├── raw/                   # Original job postings CSV (8,000 rows)
│   └── processed/
│       ├── jobs_clean.csv     # Cleaned postings with added features
│       ├── skills_long.csv    # Skills exploded into long format (36,023 rows)
│       └── jobs.db            # SQLite database (jobs + skills tables)
├── scripts/
│   ├── generate_data.py       # Dataset generation with realistic distributions
│   ├── clean_data.py          # Cleaning pipeline: nulls, types, normalization
│   ├── sql_analysis.py        # 10 analytical SQL queries
│   └── visualize.py           # 6 publication-quality matplotlib charts
└── outputs/
    └── charts/                # All generated PNG charts
```

---

## How to Run

```bash
# 1. Install dependencies
pip install pandas matplotlib numpy

# 2. Generate dataset
python scripts/generate_data.py

# 3. Clean and load into SQLite
python scripts/clean_data.py

# 4. Run SQL analysis
python scripts/sql_analysis.py

# 5. Generate charts
python scripts/visualize.py
```

---

## Charts

| # | Chart | Key Insight |
|---|---|---|
| 1 | Top 15 In-Demand Skills | Python and SQL dominate at 10.6% each |
| 2 | Average Salary by Role | ML Engineer ($160K) vs. IT Analyst ($77K) — 2x gap |
| 3 | Average Salary by City | San Francisco leads; Dallas sits mid-market |
| 4 | Salary by Experience Level | Entry → Senior premium is +$70K |
| 5 | Work Mode Distribution | Remote roles now outnumber onsite |
| 6 | Top Skills for Data Analyst | Tableau, SQL, and Excel are the core three |

---

## SQL Highlights

```sql
-- Top skills across all roles
SELECT skill, COUNT(*) AS postings,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM skills), 1) AS pct
FROM skills
GROUP BY skill
ORDER BY postings DESC
LIMIT 15;

-- Salary premium by experience level
SELECT experience,
       ROUND(AVG(salary)) AS avg_salary,
       COUNT(*) AS postings
FROM jobs
GROUP BY experience
ORDER BY avg_salary DESC;

-- Entry-level postings by role
SELECT title, COUNT(*) AS postings, ROUND(AVG(salary)) AS avg_salary
FROM jobs
WHERE experience = 'Entry'
GROUP BY title
ORDER BY postings DESC;
```

---

## Data Notes

Dataset built with realistic salary distributions, skill co-occurrence patterns,
and geographic pay multipliers based on public compensation benchmarks.
Skills were drawn from role-specific pools to reflect actual job description patterns.

---

*Built by Furqaan Ali · [LinkedIn](https://www.linkedin.com/in/furqaanali091204)*
