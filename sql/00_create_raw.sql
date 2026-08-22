-- ============================================================================
-- Block 3 — Create the raw landing table for the pulled events.
-- Run against the `live_events` database in the pgAdmin Query Tool.
-- Columns match the header of events_raw.csv exactly (order matters for import).
-- Everything loads as text first; casting/cleaning happens in 01_staging.sql
-- (Block 4) so we can inspect the messy values before trusting them.
-- ============================================================================

DROP TABLE IF EXISTS raw_events;
CREATE TABLE raw_events (
    event_id      text,
    event_name    text,
    artist_name   text,
    segment       text,
    genre         text,
    subgenre      text,
    city          text,
    state         text,
    venue         text,
    venue_id      text,
    event_date    text,
    onsale_start  text,
    price_min     text,
    price_max     text,
    currency      text,
    promoter      text,
    pulled_at     text
);
