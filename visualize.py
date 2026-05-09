"""
visualize.py
Generates 6 publication-quality charts for the Tech Job Market Analysis project.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sqlite3
import os

DB  = "/home/claude/tech-job-market-analysis/data/processed/jobs.db"
OUT = "/home/claude/tech-job-market-analysis/outputs/charts"
os.makedirs(OUT, exist_ok=True)

conn = sqlite3.connect(DB)

# ── Shared style ──────────────────────────────────────────────────────────────
NAVY   = "#1a3c5e"
BLUE   = "#2e6da4"
LBLUE  = "#90b8d8"
GRAY   = "#e8edf2"
DKGRAY = "#4a5568"
RED    = "#c0392b"
GREEN  = "#1a7a4a"

plt.rcParams.update({
    "font.family":     "DejaVu Sans",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.spines.left":   False,
    "axes.grid":          True,
    "grid.color":         GRAY,
    "grid.linewidth":     0.8,
    "axes.axisbelow":     True,
    "text.color":         NAVY,
    "axes.labelcolor":    NAVY,
    "xtick.color":        DKGRAY,
    "ytick.color":        DKGRAY,
    "figure.facecolor":   "white",
    "axes.facecolor":     "white",
})

# ── Helper ────────────────────────────────────────────────────────────────────
def save(fig, name):
    path = f"{OUT}/{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {path}")

# ── 1. Top 15 In-Demand Skills ────────────────────────────────────────────────
df_skills = pd.read_sql_query("""
    SELECT skill, COUNT(*) AS postings
    FROM skills
    GROUP BY skill ORDER BY postings DESC LIMIT 15
""", conn)

fig, ax = plt.subplots(figsize=(10, 6))
colors = [NAVY if i < 5 else BLUE if i < 10 else LBLUE for i in range(len(df_skills))]
bars = ax.barh(df_skills["skill"][::-1], df_skills["postings"][::-1],
               color=colors[::-1], height=0.65, edgecolor="none")
for bar, val in zip(bars, df_skills["postings"][::-1]):
    ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2,
            f"{val:,}", va="center", fontsize=9, color=DKGRAY)
ax.set_xlabel("Number of Job Postings", fontsize=10)
ax.set_title("Top 15 Most In-Demand Skills\nAcross 8,000 Tech Job Postings (2023–2025)",
             fontsize=13, fontweight="bold", pad=14, color=NAVY)
patches = [mpatches.Patch(color=NAVY,  label="Top 5"),
           mpatches.Patch(color=BLUE,  label="Top 6–10"),
           mpatches.Patch(color=LBLUE, label="Top 11–15")]
ax.legend(handles=patches, fontsize=9, frameon=False)
ax.set_xlim(0, df_skills["postings"].max() * 1.15)
ax.spines["bottom"].set_visible(True)
ax.spines["bottom"].set_color(GRAY)
fig.tight_layout()
save(fig, "01_top_skills")

# ── 2. Average Salary by Role ─────────────────────────────────────────────────
df_roles = pd.read_sql_query("""
    SELECT title, ROUND(AVG(salary)) AS avg_salary, COUNT(*) AS postings
    FROM jobs GROUP BY title ORDER BY avg_salary DESC
""", conn)

fig, ax = plt.subplots(figsize=(10, 5.5))
bar_colors = [NAVY if s >= 130000 else BLUE if s >= 100000 else LBLUE
              for s in df_roles["avg_salary"]]
bars = ax.bar(range(len(df_roles)), df_roles["avg_salary"] / 1000,
              color=bar_colors, edgecolor="none", width=0.6)
for i, (bar, val) in enumerate(zip(bars, df_roles["avg_salary"])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"${val/1000:.0f}K", ha="center", fontsize=9, color=DKGRAY, fontweight="bold")
ax.set_xticks(range(len(df_roles)))
ax.set_xticklabels(df_roles["title"], rotation=35, ha="right", fontsize=9)
ax.set_ylabel("Average Salary (USD thousands)", fontsize=10)
ax.set_title("Average Salary by Role\nTech & Data Positions, 2023–2025",
             fontsize=13, fontweight="bold", pad=14, color=NAVY)
ax.set_ylim(0, df_roles["avg_salary"].max() / 1000 * 1.18)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
fig.tight_layout()
save(fig, "02_salary_by_role")

# ── 3. Salary by City (excluding Remote) ─────────────────────────────────────
df_city = pd.read_sql_query("""
    SELECT city_short, ROUND(AVG(salary)) AS avg_salary, COUNT(*) AS postings
    FROM jobs WHERE city_short != 'Remote'
    GROUP BY city_short ORDER BY avg_salary DESC
""", conn)

fig, ax = plt.subplots(figsize=(9, 5))
bar_colors = [NAVY if i == 0 else BLUE if i == 1 else LBLUE if i < 4 else "#cbd5e0"
              for i in range(len(df_city))]
bars = ax.bar(range(len(df_city)), df_city["avg_salary"] / 1000,
              color=bar_colors, edgecolor="none", width=0.6)
for bar, val in zip(bars, df_city["avg_salary"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
            f"${val/1000:.0f}K", ha="center", fontsize=9, color=DKGRAY, fontweight="bold")
ax.set_xticks(range(len(df_city)))
ax.set_xticklabels(df_city["city_short"], rotation=30, ha="right", fontsize=10)
ax.set_ylabel("Average Salary (USD thousands)", fontsize=10)
ax.set_title("Average Salary by City\n(Onsite & Hybrid Roles)",
             fontsize=13, fontweight="bold", pad=14, color=NAVY)
ax.set_ylim(0, df_city["avg_salary"].max() / 1000 * 1.18)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
# Annotate Dallas TX
dallas_idx = df_city[df_city["city_short"] == "Dallas"].index[0]
dallas_pos = list(df_city["city_short"]).index("Dallas")
ax.annotate("Dallas, TX\n(your market)", xy=(dallas_pos, df_city.iloc[dallas_pos]["avg_salary"]/1000),
            xytext=(dallas_pos + 1.2, df_city.iloc[dallas_pos]["avg_salary"]/1000 + 8),
            fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
fig.tight_layout()
save(fig, "03_salary_by_city")

# ── 4. Salary by Experience Level ────────────────────────────────────────────
df_exp = pd.read_sql_query("""
    SELECT experience, ROUND(AVG(salary)) AS avg_salary,
           ROUND(MIN(salary)) AS min_sal, ROUND(MAX(salary)) AS max_sal,
           COUNT(*) AS postings
    FROM jobs GROUP BY experience ORDER BY avg_salary
""", conn)

order = ["Entry", "Mid", "Senior"]
df_exp["experience"] = pd.Categorical(df_exp["experience"], categories=order, ordered=True)
df_exp = df_exp.sort_values("experience")

fig, ax = plt.subplots(figsize=(7, 5))
exp_colors = [LBLUE, BLUE, NAVY]
bars = ax.bar(df_exp["experience"], df_exp["avg_salary"] / 1000,
              color=exp_colors, edgecolor="none", width=0.5)
for bar, val, posts in zip(bars, df_exp["avg_salary"], df_exp["postings"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f"${val/1000:.0f}K\n({posts:,} jobs)", ha="center", fontsize=9,
            color=DKGRAY, fontweight="bold")

# Draw salary jump arrows
for i in range(len(df_exp) - 1):
    x1, x2 = i, i + 1
    y1 = df_exp.iloc[i]["avg_salary"] / 1000
    y2 = df_exp.iloc[i+1]["avg_salary"] / 1000
    diff = y2 - y1
    ax.annotate("", xy=(x2 - 0.28, y2 - 2), xytext=(x1 + 0.28, y1 + 2),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 4,
            f"+${diff:.0f}K", ha="center", fontsize=9, color=GREEN, fontweight="bold")

ax.set_ylabel("Average Salary (USD thousands)", fontsize=10)
ax.set_title("Salary by Experience Level\nEntry → Mid → Senior Premium",
             fontsize=13, fontweight="bold", pad=14, color=NAVY)
ax.set_ylim(0, df_exp["avg_salary"].max() / 1000 * 1.25)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
fig.tight_layout()
save(fig, "04_salary_by_experience")

# ── 5. Work Mode Distribution ─────────────────────────────────────────────────
df_mode = pd.read_sql_query("""
    SELECT work_mode, COUNT(*) AS postings,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM jobs), 1) AS pct
    FROM jobs GROUP BY work_mode ORDER BY postings DESC
""", conn)

fig, ax = plt.subplots(figsize=(6, 6))
mode_colors = [NAVY, BLUE, LBLUE]
wedges, texts, autotexts = ax.pie(
    df_mode["postings"],
    labels=df_mode["work_mode"],
    colors=mode_colors,
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.75,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
for text in texts:
    text.set_fontsize(12)
    text.set_color(NAVY)
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_color("white")
    autotext.set_fontweight("bold")
ax.set_title("Work Mode Distribution\n8,000 Tech Job Postings (2023–2025)",
             fontsize=13, fontweight="bold", pad=14, color=NAVY)
for i, (mode, count, pct) in enumerate(zip(df_mode["work_mode"], df_mode["postings"], df_mode["pct"])):
    ax.annotate(f"{count:,} postings", xy=(0, 0), xytext=(0, -0.18 - i * 0.07),
                ha="center", fontsize=9, color=DKGRAY,
                textcoords="axes fraction")
fig.tight_layout()
save(fig, "05_work_mode")

# ── 6. Top Skills for Data Analyst (entry-point role) ────────────────────────
df_da = pd.read_sql_query("""
    SELECT skill, COUNT(*) AS postings
    FROM skills WHERE title = 'Data Analyst'
    GROUP BY skill ORDER BY postings DESC LIMIT 9
""", conn)

fig, ax = plt.subplots(figsize=(8, 5))
bar_colors = [NAVY if i < 3 else BLUE if i < 6 else LBLUE for i in range(len(df_da))]
bars = ax.bar(range(len(df_da)), df_da["postings"],
              color=bar_colors, edgecolor="none", width=0.6)
for bar, val in zip(bars, df_da["postings"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"{val:,}", ha="center", fontsize=9, color=DKGRAY, fontweight="bold")
ax.set_xticks(range(len(df_da)))
ax.set_xticklabels(df_da["skill"], rotation=35, ha="right", fontsize=10)
ax.set_ylabel("Postings Requiring This Skill", fontsize=10)
ax.set_title("Top Skills Required for Data Analyst Roles\n1,742 Data Analyst Postings Analyzed",
             fontsize=13, fontweight="bold", pad=14, color=NAVY)
ax.set_ylim(0, df_da["postings"].max() * 1.18)
fig.tight_layout()
save(fig, "06_data_analyst_skills")

conn.close()
print("\nAll 6 charts saved to outputs/charts/")
