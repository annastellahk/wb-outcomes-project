# World Bank Open Data: Poverty, Jobs & Growth — a mini outcomes pipeline

A small, honest, end-to-end project: pull public World Bank development
data, clean it, load it into a real database, query it with SQL, and turn
one finding into a chart and a plain-language takeaway. Built to have
something genuine to show for the WBG Young Professional application
(req38251, Department for Outcomes) — that role is explicitly about moving
from raw data to a decision, which is exactly what this does at small scale.

## What it does

1. **`01_fetch_data.py`** — pulls three indicators (unemployment, extreme
   poverty headcount ratio, GDP growth) for every country, 2010–2023, from
   the free World Bank Open Data API (no key needed), plus country/region
   metadata.
2. **`02_clean_and_load.py`** — cleans the raw pull with pandas (drops
   missing values and non-country aggregates like "World" or "OECD
   members"), joins in region/income group, and loads it into a SQLite
   database (`wb_outcomes.db`).
3. **`03_queries.sql`** — four analytical SQL queries against that database:
   latest unemployment by country, average poverty rate by region, a
   "jobless growth" anomaly query (GDP up but unemployment also up), and a
   poverty trend by income group.
4. **`04_analyze.py`** — runs one of those angles end-to-end in Python,
   produces a chart (`outputs/poverty_by_region.png`), and prints a
   one-paragraph, decision-maker-facing takeaway you fill in with the real
   numbers.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run it, in order

```bash
python 01_fetch_data.py         # writes data/countries_meta.csv, data/indicators_raw.csv
python 02_clean_and_load.py     # writes wb_outcomes.db
python 04_analyze.py            # writes outputs/poverty_by_region.png, prints an insight

# explore the SQL queries in any SQLite client (DB Browser for SQLite is
# a free GUI option), or from the command line if you have sqlite3 installed:
sqlite3 wb_outcomes.db < 03_queries.sql
```

## Key findings

- Sub-Saharan Africa has by far the highest average extreme-poverty headcount ratio of any region (37.4%), compared with 0.75% in North America.
- Several countries show a "jobless growth" pattern — GDP grew, but unemployment rose anyway. Eswatini's unemployment rose 13 percentage points despite 0.4% GDP growth; South Africa's rose over 8 points on 2.1% growth.
- These findings hold up two ways: an independent SQL query and a matplotlib chart both point to the same regional poverty pattern.

## If you want to go further

- Swap in an indicator closer to the posting's named themes (climate: `EN.ATM.CO2E.PC`; women: `SG.GEN.PARL.ZS`; jobs: keep unemployment or add labor force participation `SL.TLF.CACT.ZS`).
- A small NLP angle to mirror the "AI for Outcomes" part of the role: pull World Bank project abstracts/descriptions (available via the Projects API, `https://search.worldbank.org/api/v3/projects`) and do basic keyword/topic extraction.
