"""
02_clean_and_load.py

Cleans the raw World Bank pulls from step 1, joins in country metadata,
drops non-country aggregates (regions/income groups reported by the API
alongside real countries), and loads everything into a small SQLite
database for step 3's SQL queries.

Run:
    python 02_clean_and_load.py
"""

import sqlite3
import pandas as pd

DB_PATH = "wb_outcomes.db"


def main():
    indicators = pd.read_csv("data/indicators_raw.csv")
    meta = pd.read_csv("data/countries_meta.csv")

    # The API returns regional/income aggregates (e.g. "World", "Euro area")
    # mixed in with actual countries. Real countries have a real income
    # group; aggregates are tagged "Aggregates".
    real_countries = meta[meta["income_level"] != "Aggregates"].copy()

    merged = indicators.merge(
        real_countries[["country_code", "region", "region_code", "income_level", "income_level_code"]],
        on="country_code",
        how="inner",  # drops aggregate rows that had no match
    )

    merged = merged.dropna(subset=["value"])
    merged = merged.sort_values(["indicator_code", "country_code", "year"])

    print(f"Clean rows: {len(merged)} (from {len(indicators)} raw)")

    conn = sqlite3.connect(DB_PATH)
    merged.to_sql("indicators", conn, if_exists="replace", index=False)
    real_countries.to_sql("countries", conn, if_exists="replace", index=False)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_ind_country_year ON indicators(country_code, year)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ind_code ON indicators(indicator_code)")
    conn.commit()
    conn.close()

    print(f"Loaded 'indicators' and 'countries' tables into {DB_PATH}")


if __name__ == "__main__":
    main()
