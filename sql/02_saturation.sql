-- ============================================================================
-- Block 5 analysis — Market saturation & whitespace.
-- Core finding: which city-genre segments are over- vs under-represented
-- relative to the national genre norm. Junk genres filtered; thin cells gated.
-- ============================================================================

WITH city_genre AS (
    SELECT
        city, genre,
        COUNT(*) AS event_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY city), 1) AS pct_of_city
    FROM stg_events
    WHERE segment IN ('Music', 'Arts & Theatre')
      AND genre NOT IN ('Undefined', 'Other', 'Miscellaneous')   -- drop junk buckets
      AND city IS NOT NULL AND genre IS NOT NULL
    GROUP BY city, genre
),
genre_avg AS (
    SELECT genre, ROUND(AVG(pct_of_city), 1) AS avg_pct_across_cities
    FROM city_genre
    GROUP BY genre
)
SELECT
    c.city, c.genre, c.event_count, c.pct_of_city,
    g.avg_pct_across_cities,
    ROUND(c.pct_of_city - g.avg_pct_across_cities, 1) AS gap_vs_benchmark
FROM city_genre c
JOIN genre_avg g ON c.genre = g.genre
WHERE c.event_count >= 10
ORDER BY gap_vs_benchmark DESC;   -- flip to ASC for whitespace
