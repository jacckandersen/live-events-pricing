-- ============================================================================
-- Block 5 enrichment — load metro population, join to events for per-capita.
-- ============================================================================

-- 1. reference table
DROP TABLE IF EXISTS metro_population;
CREATE TABLE metro_population (
    city              text PRIMARY KEY,
    metro_population  bigint
);

-- 2. load it. Move metro_population.csv to C:\temp first (same as events),
--    then run this COPY (edit path if needed):
-- COPY metro_population FROM 'C:\temp\metro_population.csv'
--   WITH (FORMAT csv, HEADER true);

-- 3. sanity check
-- SELECT count(*) FROM metro_population;   -- 20
