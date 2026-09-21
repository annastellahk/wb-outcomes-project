"""
01_fetch_data.py

Pulls indicator data and country metadata from the World Bank Open Data API
(no key required) and saves them as raw CSVs for the next step to clean.

Indicators chosen to echo the WBG Department for Outcomes themes named in
the job posting (jobs, poverty, growth):
  - SL.UEM.TOTL.ZS   Unemployment, total (% of total labor force)
  - SI.POV.DDAY      Poverty headcount ratio at $2.15/day (2017 PPP)
  - NY.GDP.MKTP.KD.ZG GDP growth (annual %)

Run:
    python 01_fetch_data.py
"""

import time
import requests
import pandas as pd

API_ROOT = "https://api.worldbank.org/v2"
INDICATORS = {
    "SL.UEM.TOTL.ZS": "unemployment_pct",
    "SI.POV.DDAY": "poverty_headcount_215",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",
}
DATE_RANGE = "2010:2023"
PER_PAGE = 20000  # large enough to get everything in one page for these calls


def fetch_indicator(indicator_code: str) -> pd.DataFrame:
    """Fetch one indicator for all countries/years and return a tidy DataFrame."""
    url = f"{API_ROOT}/country/all/indicator/{indicator_code}"
    params = {"format": "json", "per_page": PER_PAGE, "date": DATE_RANGE}

    rows = []
    page = 1
    while True:
        params["page"] = page
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        meta, data = resp.json()
        if not data:
            break
        for rec in data:
            if rec["value"] is None:
                continue
            rows.append(
                {
                    "country_code": rec["countryiso3code"],
                    "country_name": rec["country"]["value"],
                    "indicator_code": rec["indicator"]["id"],
                    "year": int(rec["date"]),
                    "value": float(rec["value"]),
                }
            )
        if page >= meta["pages"]:
            break
        page += 1
        time.sleep(0.2)  # be polite to the API

    return pd.DataFrame(rows)


def fetch_country_metadata() -> pd.DataFrame:
    """Fetch country/region/income-group metadata, used to drop aggregates
    (e.g. 'World', 'OECD members') and to enable region-level analysis."""
    url = f"{API_ROOT}/country"
    params = {"format": "json", "per_page": 400}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    _, data = resp.json()

    rows = []
    for rec in data:
        rows.append(
            {
                "country_code": rec["id"],
                "country_name": rec["name"],
                "region": rec["region"]["value"],
                "region_code": rec["region"]["id"],
                "income_level": rec["incomeLevel"]["value"],
                "income_level_code": rec["incomeLevel"]["id"],
            }
        )
    return pd.DataFrame(rows)


def main():
    print("Fetching country metadata...")
    meta = fetch_country_metadata()
    meta.to_csv("data/countries_meta.csv", index=False)
    print(f"  saved {len(meta)} countries/aggregates -> data/countries_meta.csv")

    all_frames = []
    for code, short_name in INDICATORS.items():
        print(f"Fetching indicator {code} ({short_name})...")
        df = fetch_indicator(code)
        df["indicator_short"] = short_name
        all_frames.append(df)
        print(f"  got {len(df)} observations")

    combined = pd.concat(all_frames, ignore_index=True)
    combined.to_csv("data/indicators_raw.csv", index=False)
    print(f"Saved {len(combined)} total observations -> data/indicators_raw.csv")


if __name__ == "__main__":
    main()
