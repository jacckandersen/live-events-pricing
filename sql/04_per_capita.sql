-- ============================================================================
-- Block 5 — Per-capita event intensity by city & genre (the enriched finding).
-- Absolute intensity, immune to the mix-distortion of share analysis.
-- ============================================================================

-- Events per 100k residents, by city and genre.
WITH cg AS (
    SELECT city, genre, COUNT(*) AS event_count
    FROM stg_events
    WHERE segment IN ('Music', 'Arts & Theatre')
      AND genre NOT IN ('Undefined', 'Other', 'Miscellaneous')
      AND city IS NOT NULL AND genre IS NOT NULL
    GROUP BY city, genre
)
SELECT
    cg.city, cg.genre, cg.event_count,
    p.metro_population,
    ROUND(cg.event_count * 100000.0 / p.metro_population, 2) AS events_per_100k,
    RANK() OVER (PARTITION BY cg.genre
                 ORDER BY cg.event_count * 100000.0 / p.metro_population DESC) AS rank_in_genre
FROM cg
JOIN metro_population p ON p.city = cg.city
WHERE cg.event_count >= 10
ORDER BY events_per_100k DESC;

-- Reading: for each genre, which metros have the highest event intensity
-- per resident. rank_in_genre = 1 is the most-served metro for that genre.
-- The bottom of a genre's ranking (high population, low count) is genuine
-- whitespace — real gap, not a mix artifact.
