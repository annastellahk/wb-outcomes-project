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

All four scripts were logic-tested against a synthetic fixture before you
received this — `01_fetch_data.py` itself needs a real internet connection
to hit `api.worldbank.org`, which you'll have on your own machine.

## Suggested day-by-day plan (closing date 9/30)

- **Day 1 (today/tomorrow):** Set up the venv, run `01_fetch_data.py` and
  `02_clean_and_load.py`. Open `wb_outcomes.db` in DB Browser for SQLite
  and just look around — get a feel for the real numbers.
- **Day 2:** Run the four queries in `03_queries.sql` one at a time. For
  each, write one sentence in your own words: what does this actually say?
  Which result surprised you? Save these — they're your interview material.
- **Day 3:** Run `04_analyze.py`, look at the chart, and rewrite the
  printed insight paragraph with a real, specific claim from your data
  (not the placeholder). Optionally swap the query/chart for whichever of
  the four findings you found most interesting.
- **Day 4:** Write the actual README top section in your own words (a
  couple of sentences on why you built this and what it shows), push the
  whole folder to a public GitHub repo.
- **Day 5:** Add the GitHub link to your resume's Technical Skills or
  Projects section and to your LinkedIn. Re-read the CV I drafted for you
  and swap the "SQL (applied project in progress)" wording for something
  concrete now that it's done, e.g. "SQL (applied project — see
  github.com/yourname/wb-outcomes-project)".

## If you want to go further

- Swap in an indicator closer to the posting's named themes (climate:
  `EN.ATM.CO2E.PC`; women: `SG.GEN.PARL.ZS`; jobs: keep unemployment or add
  labor force participation `SL.TLF.CACT.ZS`).
- Try a very small NLP angle to mirror the "AI for Outcomes" part of the
  role: pull World Bank project abstracts/descriptions (available via the
  Projects API, `https://search.worldbank.org/api/v3/projects`) and do
  basic keyword/topic extraction. Only attempt this if Days 1–4 go
  smoothly — a small, complete project beats a large, half-finished one.

## Honesty note

Everything in this repo is real code you ran on real public data. When you
talk about it in an interview, describe exactly what you did and what you
found — don't inflate a few days' project into more than it is. "I built a
small pipeline to understand X" is a stronger, more credible answer than
overclaiming production experience you don't have yet.
