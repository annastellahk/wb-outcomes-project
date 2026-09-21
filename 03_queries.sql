-- 03_queries.sql
-- Sample analytical queries against wb_outcomes.db (run with:
--   sqlite3 wb_outcomes.db < 03_queries.sql
-- or paste individually into any SQLite client / DB Browser for SQLite)

-- 1) Most recent unemployment rate available for each country, highest first
SELECT country_name, year, value AS unemployment_pct
FROM indicators
WHERE indicator_code = 'SL.UEM.TOTL.ZS'
  AND year = (
      SELECT MAX(year) FROM indicators i2
      WHERE i2.country_code = indicators.country_code
        AND i2.indicator_code = 'SL.UEM.TOTL.ZS'
  )
ORDER BY unemployment_pct DESC
LIMIT 15;

-- 2) Average poverty headcount ratio by region, most recent year available per country
SELECT region, ROUND(AVG(value), 2) AS avg_poverty_rate, COUNT(*) AS n_countries
FROM indicators
WHERE indicator_code = 'SI.POV.DDAY'
  AND year = (
      SELECT MAX(year) FROM indicators i2
      WHERE i2.country_code = indicators.country_code
        AND i2.indicator_code = 'SI.POV.DDAY'
  )
GROUP BY region
ORDER BY avg_poverty_rate DESC;

-- 3) Countries where GDP grew but unemployment also rose, comparing 2015 vs 2022
--    (a genuine "signal" query: jobless growth is a real development concern)
WITH gdp_2015 AS (
    SELECT country_code, value AS gdp_2015
    FROM indicators WHERE indicator_code = 'NY.GDP.MKTP.KD.ZG' AND year = 2015
),
gdp_2022 AS (
    SELECT country_code, value AS gdp_2022
    FROM indicators WHERE indicator_code = 'NY.GDP.MKTP.KD.ZG' AND year = 2022
),
unemp_2015 AS (
    SELECT country_code, value AS unemp_2015
    FROM indicators WHERE indicator_code = 'SL.UEM.TOTL.ZS' AND year = 2015
),
unemp_2022 AS (
    SELECT country_code, value AS unemp_2022
    FROM indicators WHERE indicator_code = 'SL.UEM.TOTL.ZS' AND year = 2022
)
SELECT c.country_name, c.region,
       g22.gdp_2022, u22.unemp_2022 - u15.unemp_2015 AS unemployment_change
FROM gdp_2022 g22
JOIN unemp_2022 u22 USING (country_code)
JOIN unemp_2015 u15 USING (country_code)
JOIN countries c USING (country_code)
WHERE g22.gdp_2022 > 0 AND (u22.unemp_2022 - u15.unemp_2015) > 0
ORDER BY unemployment_change DESC
LIMIT 15;

-- 4) Year-over-year trend of the median poverty headcount ratio, by income group
SELECT income_level, year, ROUND(AVG(value), 2) AS avg_poverty_rate
FROM indicators
WHERE indicator_code = 'SI.POV.DDAY'
GROUP BY income_level, year
ORDER BY income_level, year;
