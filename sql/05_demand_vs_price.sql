-- 05_demand_vs_price.sql
-- Demand-vs-price analysis: does price track artist demand within each market?
-- Demand proxy = Deezer fan-count (artist_popularity.fans), matched on artist_name.
-- Prereq: load artist_popularity (see enrichment/deezer_enrich.py output).

-- Reload table (CSV columns: artist_name, matched, deezer_name, deezer_id, fans, albums)
-- DROP TABLE IF EXISTS artist_popularity;
-- CREATE TABLE artist_popularity (
--     artist_name text, matched boolean, deezer_name text,
--     deezer_id bigint, fans bigint, albums integer);
-- COPY artist_popularity FROM 'C:\temp\artist_popularity.csv' WITH (FORMAT csv, HEADER true);

-- HEADLINE: within-market correlation of artist demand vs event price.
-- Near zero / negative = pricing decoupled from demand (opportunity).
SELECT
    e.city,
    count(*)                                                   AS priced_events,
    round(corr(ap.fans, (e.price_min + e.price_max)/2.0)::numeric, 3) AS price_fan_corr,
    round(avg((e.price_min + e.price_max)/2.0)::numeric, 2)    AS avg_price,
    round(avg(ap.fans))                                        AS avg_fans
FROM stg_events e
JOIN artist_popularity ap
  ON ap.artist_name = e.artist_name
 AND ap.matched
 AND ap.fans > 0
WHERE e.price_min IS NOT NULL
  AND e.price_max IS NOT NULL
GROUP BY e.city
HAVING count(*) >= 20        -- thin-segment gating: stable correlations only
ORDER BY price_fan_corr ASC; -- most demand-blind markets first

-- REJECTED APPROACH (kept for the method story): price-per-fan ratio.
-- Unstable — city ranking flips between avg-fans and median-fans denominators,
-- because median fans swing ~50x across cities and dominate the ratio.
-- SELECT e.city,
--        round(percentile_cont(0.5) WITHIN GROUP (
--            ORDER BY (e.price_min+e.price_max)/2.0)::numeric
--            / NULLIF(avg(ap.fans),0) * 1000000, 2) AS price_per_million_fans
-- FROM stg_events e JOIN artist_popularity ap ON ap.artist_name = e.artist_name
--   AND ap.matched AND ap.fans > 0
-- WHERE e.price_min IS NOT NULL AND e.price_max IS NOT NULL
-- GROUP BY e.city HAVING count(*) >= 10 ORDER BY price_per_million_fans DESC;
