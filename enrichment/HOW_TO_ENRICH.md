# Artist-demand enrichment — steps

The demand layer attaches a per-artist popularity proxy to each priced event, so
we can test whether markets price in line with the demand they book (see
`docs/FINDINGS.md` Finding 8 and README §4). The proxy is **Deezer fan-count**,
pulled from Deezer's public API (no authentication required).

## 1. Export the priced-artist list
In pgAdmin / psql, export the artists that appear on priced events:
```sql
COPY (
    SELECT DISTINCT e.artist_name
    FROM stg_events e
    WHERE e.artist_name IS NOT NULL AND e.artist_name <> ''
      AND e.price_min IS NOT NULL
) TO 'C:\temp\artists_priced.txt';
```
Move `artists_priced.txt` into this `enrichment/` folder (one artist name per line;
strip any header/quotes).

## 2. Run the Deezer enrichment
```
cd enrichment
python deezer_enrich.py --debug "Taylor Swift"   # confirm one artist first
python deezer_enrich.py                            # full run
```
No credentials needed. Writes `artist_popularity.csv` with columns
`artist_name, matched, deezer_name, deezer_id, fans, albums`. Expect a high match
rate (~98% on this dataset); unmatched rows are typically non-artist events
(festivals, "DJ X b2b Y", odd spellings).

## 3. Load into Postgres
Copy the CSV to `C:\temp` first (server-side COPY can't read Downloads), then:
```sql
DROP TABLE IF EXISTS artist_popularity;
CREATE TABLE artist_popularity (
    artist_name  text,
    matched      boolean,
    deezer_name  text,
    deezer_id    bigint,
    fans         bigint,
    albums       integer
);
COPY artist_popularity FROM 'C:\temp\artist_popularity.csv'
  WITH (FORMAT csv, HEADER true);

SELECT count(*) AS rows,
       count(*) FILTER (WHERE matched) AS matched
FROM artist_popularity;
```

## 4. Run the finding
Run `sql/05_demand_vs_price.sql` — it correlates artist fan-count against event
price within each market. Near-zero / negative correlation means pricing is
decoupled from demand (the headline read).

---

### Why Deezer, not Spotify
Spotify was the original demand source. Its Web API stopped returning
`popularity`, `followers`, and `genres` on artist objects for this app —
confirmed by calling `GET /v1/artists/{id}` directly and getting a response
without those fields, so the gap was on Spotify's side, not in parsing. Deezer's
public `nb_fan` is an auth-free, comparable popularity proxy, so it was
substituted. Fan-count is a *proxy* for demand, not realized sales, so the
value-gap read is directional (see README §7).
