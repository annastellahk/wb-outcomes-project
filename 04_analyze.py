"""
04_analyze.py

Turns the SQLite data into one chart and one short written insight -
the "translate the finding for a decision-maker" step the job posting
explicitly asks for. Produces outputs/poverty_by_region.png.

Run:
    python 04_analyze.py
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = "wb_outcomes.db"
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)


def main():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT region, year, AVG(value) AS avg_poverty_rate
        FROM indicators
        WHERE indicator_code = 'SI.POV.DDAY'
        GROUP BY region, year
        ORDER BY region, year
    """
    df = pd.read_sql(query, conn)
    conn.close()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for region, group in df.groupby("region"):
        ax.plot(group["year"], group["avg_poverty_rate"], marker="o", linewidth=2, label=region)

    ax.set_title("Average poverty headcount ratio ($2.15/day) by region, 2010–2023")
    ax.set_xlabel("Year")
    ax.set_ylabel("Avg. poverty rate (%)")
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "poverty_by_region.png", dpi=150)
    print(f"Saved chart -> {OUT_DIR / 'poverty_by_region.png'}")

    # A short, decision-maker-facing takeaway - fill this in with what the
    # data actually shows once you've run the pipeline for real.
    latest_year = df["year"].max()
    latest = df[df["year"] == latest_year].sort_values("avg_poverty_rate", ascending=False)
    print("\n--- One-paragraph insight (edit after reviewing the real numbers) ---")
    print(
        f"As of {latest_year}, the region with the highest average extreme-poverty "
        f"headcount ratio in this sample is {latest.iloc[0]['region']} "
        f"({latest.iloc[0]['avg_poverty_rate']:.1f}%), compared with "
        f"{latest.iloc[-1]['region']} at {latest.iloc[-1]['avg_poverty_rate']:.1f}%. "
        "[Add one sentence here on the trend direction and what it implies for "
        "where outcome-focused interventions might matter most.]"
    )


if __name__ == "__main__":
    main()
