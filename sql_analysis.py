"""
sql_analysis.py
Runs analytical SQL queries against the jobs SQLite database
and prints findings used in the dashboard and resume bullets.
"""
import sqlite3
import pandas as pd

DB = "/home/claude/tech-job-market-analysis/data/processed/jobs.db"
conn = sqlite3.connect(DB)

def q(label, sql):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print('='*60)
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))
    return df

# 1. Top 20 most in-demand skills across ALL roles
q("Top 20 In-Demand Skills (All Roles)", """
    SELECT skill,
           COUNT(*) AS postings,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM skills), 1) AS pct_of_postings
    FROM skills
    GROUP BY skill
    ORDER BY postings DESC
    LIMIT 20
""")

# 2. Average salary by role
q("Average Salary by Role", """
    SELECT title,
           COUNT(*) AS postings,
           ROUND(AVG(salary)) AS avg_salary,
           ROUND(MIN(salary)) AS min_salary,
           ROUND(MAX(salary)) AS max_salary
    FROM jobs
    GROUP BY title
    ORDER BY avg_salary DESC
""")

# 3. Average salary by city
q("Average Salary by City", """
    SELECT city_short,
           COUNT(*) AS postings,
           ROUND(AVG(salary)) AS avg_salary
    FROM jobs
    WHERE city_short != 'Remote'
    GROUP BY city_short
    ORDER BY avg_salary DESC
""")

# 4. Salary by experience level
q("Salary by Experience Level", """
    SELECT experience,
           COUNT(*) AS postings,
           ROUND(AVG(salary)) AS avg_salary,
           ROUND(MIN(salary)) AS min_salary,
           ROUND(MAX(salary)) AS max_salary
    FROM jobs
    GROUP BY experience
    ORDER BY avg_salary DESC
""")

# 5. Work mode breakdown
q("Work Mode Distribution", """
    SELECT work_mode,
           COUNT(*) AS postings,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM jobs), 1) AS pct
    FROM jobs
    GROUP BY work_mode
    ORDER BY postings DESC
""")

# 6. Top skills specifically for Data Analyst roles
q("Top Skills for Data Analyst Roles", """
    SELECT skill,
           COUNT(*) AS postings
    FROM skills
    WHERE title = 'Data Analyst'
    GROUP BY skill
    ORDER BY postings DESC
    LIMIT 10
""")

# 7. Entry-level postings by role
q("Entry-Level Postings by Role (Avg Salary)", """
    SELECT title,
           COUNT(*) AS postings,
           ROUND(AVG(salary)) AS avg_salary
    FROM jobs
    WHERE experience = 'Entry'
    GROUP BY title
    ORDER BY postings DESC
""")

# 8. Salary premium: Remote vs Onsite
q("Remote vs Onsite Salary Comparison", """
    SELECT work_mode,
           COUNT(*) AS postings,
           ROUND(AVG(salary)) AS avg_salary
    FROM jobs
    WHERE work_mode IN ('Remote', 'Onsite')
    GROUP BY work_mode
""")

# 9. Top industries hiring for data roles
q("Postings by Industry", """
    SELECT industry,
           COUNT(*) AS postings,
           ROUND(AVG(salary)) AS avg_salary
    FROM jobs
    GROUP BY industry
    ORDER BY postings DESC
""")

# 10. YoY posting growth
q("Postings by Year", """
    SELECT year,
           COUNT(*) AS postings
    FROM jobs
    GROUP BY year
    ORDER BY year
""")

conn.close()
print("\n\nSQL analysis complete.")
