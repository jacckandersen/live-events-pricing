-- ============================================================================
-- Block 4 (cleaning) lives here too — the clean view everything reads from.
-- Run AFTER raw_events is loaded. Creates stg_events.
-- ============================================================================
DROP VIEW IF EXISTS stg_events CASCADE;
CREATE VIEW stg_events AS
SELECT
    event_id,
    NULLIF(TRIM(event_name), '')                        AS event_name,
    NULLIF(TRIM(artist_name), '')                       AS artist_name,
    NULLIF(TRIM(segment), '')                           AS segment,
    NULLIF(TRIM(genre), '')                             AS genre,
    NULLIF(TRIM(subgenre), '')                          AS subgenre,
    NULLIF(TRIM(city), '')                              AS city,
    NULLIF(TRIM(state), '')                             AS state,
    NULLIF(TRIM(venue), '')                             AS venue,
    NULLIF(TRIM(venue_id), '')                          AS venue_id,
    -- dates: 'YYYY-MM-DD' text -> date (some may be blank)
    CASE WHEN event_date ~ '^\d{4}-\d{2}-\d{2}$'
         THEN event_date::date END                      AS event_date,
    CASE WHEN onsale_start ~ '^\d{4}-\d{2}-\d{2}$'
         THEN onsale_start::date END                    AS onsale_start,
    -- prices: blank -> NULL, else numeric
    NULLIF(price_min, '')::numeric                      AS price_min,
    NULLIF(price_max, '')::numeric                      AS price_max,
    NULLIF(TRIM(currency), '')                          AS currency,
    NULLIF(TRIM(promoter), '')                          AS promoter,
    -- has this event got usable price data?
    (NULLIF(price_min,'') IS NOT NULL)                  AS has_price,
    -- month bucket for seasonality
    CASE WHEN event_date ~ '^\d{4}-\d{2}-\d{2}$'
         THEN TO_CHAR(event_date::date, 'YYYY-MM') END  AS event_month
FROM raw_events
WHERE event_id IS NOT NULL AND event_id <> '';

-- Sanity checks after creating:
--   SELECT count(*) FROM stg_events;                       -- ~16,013
--   SELECT count(*) FILTER (WHERE has_price) FROM stg_events;  -- ~2,785
--   SELECT segment, count(*) FROM stg_events GROUP BY 1 ORDER BY 2 DESC;
