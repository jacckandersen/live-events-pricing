# Block 3 — Load events_raw.csv into Postgres (pgAdmin)

You already made the `live_events` database. Do everything against it.

## 1. Create the raw table
Click `live_events` → Tools → Query Tool → open `sql/00_create_raw.sql` → run (F5).

## 2. Load the CSV via the Import wizard (maps by column name)
The CSV is at:
  Downloads\live-events-pricing\live-events-pricing\events_raw.csv
(it's in the project root, one level up from the extract/ and sql/ folders)

1. Tree: live_events → Schemas → public → Tables → **raw_events**
2. Right-click **raw_events** → **Import/Export Data…**
3. Import. Filename: browse to events_raw.csv.
4. Format: **csv**. Header: **Yes**. Delimiter: **,**. Quote: **"**
5. Columns tab: leave all selected (they match the header).
6. OK. ~16,013 rows load in a few seconds.

Check: `SELECT count(*) FROM raw_events;`  → ~16,013

## 3. Build the clean view
Run `sql/01_staging.sql`, then:
```sql
SELECT count(*) FROM stg_events;
SELECT count(*) FILTER (WHERE has_price) FROM stg_events;   -- ~2,785 (17%)
SELECT segment, count(*) FROM stg_events GROUP BY 1 ORDER BY 2 DESC;
```

Tell me those counts and we start the analysis (Block 3/5 SQL).
