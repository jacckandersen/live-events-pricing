"""
Block 2 — Live API extraction from the Ticketmaster Discovery API.

Pulls concert + comedy events across a set of US markets and writes them to a
flat CSV (events_raw.csv) that Block 3 loads into Postgres.

The API key is read from the TM_API_KEY environment variable — never hardcoded.
    Windows (PowerShell):  $env:TM_API_KEY="your_consumer_key"
    Windows (cmd):         set TM_API_KEY=your_consumer_key
    Mac/Linux:             export TM_API_KEY="your_consumer_key"

Then:  python extract_events.py
"""

import os
import csv
import time
import requests
from datetime import datetime

API_KEY = os.environ.get("TM_API_KEY")
if not API_KEY:
    raise SystemExit(
        "No API key found. Set TM_API_KEY first, e.g.\n"
        '  Windows PowerShell:  $env:TM_API_KEY="your_consumer_key"\n'
        '  Mac/Linux:           export TM_API_KEY="your_consumer_key"'
    )

BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

# Target markets for the pricing project. DMA-style major US metros.
# (city name is used for the 'city' query param; keeps the pull focused and
#  under the API's paging limits per market.)
MARKETS = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin",
    "Atlanta", "Boston", "Denver", "Seattle", "Miami",
    "Nashville", "Portland", "Las Vegas", "Detroit", "Minneapolis",
]

# Discovery API classification segments we care about for this project.
SEGMENTS = ["Music", "Comedy"]   # 'Comedy' lives under segment name 'Arts & Theatre'
                                 # -> we filter by keyword too; see build_params.

PAGE_SIZE = 200          # API max per page
MAX_PAGES = 5            # API allows deep paging but caps total window ~1000; keep modest
SLEEP_SECONDS = 0.25     # be polite: default rate limit is 5 req/sec, 5000/day

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "events_raw.csv")

FIELDS = [
    "event_id", "event_name", "artist_name", "segment", "genre", "subgenre",
    "city", "state", "venue", "venue_id",
    "event_date", "onsale_start", "price_min", "price_max", "currency",
    "promoter", "pulled_at",
]


def build_params(city, segment, page):
    p = {
        "apikey": API_KEY,
        "city": city,
        "size": PAGE_SIZE,
        "page": page,
        "countryCode": "US",
        "sort": "date,asc",
    }
    # 'Music' is a real segmentName; comedy is classified under Arts & Theatre,
    # so we use classificationName which matches segment OR genre names.
    p["classificationName"] = "Music" if segment == "Music" else "Comedy"
    return p


def parse_event(ev):
    """Flatten one Discovery API event object into our row dict. Missing fields -> ''."""
    row = {k: "" for k in FIELDS}
    row["event_id"] = ev.get("id", "")
    row["event_name"] = ev.get("name", "")
    # structured artist/attraction name — cleaner than event_name for matching
    attractions = ((ev.get("_embedded") or {}).get("attractions") or [])
    row["artist_name"] = attractions[0].get("name", "") if attractions else ""
    row["pulled_at"] = datetime.utcnow().isoformat(timespec="seconds")

    # classification (segment / genre / subgenre)
    cls = (ev.get("classifications") or [{}])[0]
    row["segment"]  = (cls.get("segment")  or {}).get("name", "")
    row["genre"]    = (cls.get("genre")    or {}).get("name", "")
    row["subgenre"] = (cls.get("subGenre") or {}).get("name", "")

    # dates
    dates = ev.get("dates") or {}
    start = dates.get("start") or {}
    row["event_date"] = start.get("localDate", "")
    sales = (ev.get("sales") or {}).get("public") or {}
    row["onsale_start"] = (sales.get("startDateTime") or "")[:10]

    # price ranges (often missing — that's expected and part of the data story)
    pr = (ev.get("priceRanges") or [{}])[0]
    row["price_min"] = pr.get("min", "")
    row["price_max"] = pr.get("max", "")
    row["currency"]  = pr.get("currency", "")

    # promoter
    row["promoter"] = (ev.get("promoter") or {}).get("name", "")

    # venue (embedded)
    venues = ((ev.get("_embedded") or {}).get("venues") or [{}])
    v = venues[0] if venues else {}
    row["venue"]    = v.get("name", "")
    row["venue_id"] = v.get("id", "")
    row["city"]  = ((v.get("city")  or {}).get("name", ""))
    row["state"] = ((v.get("state") or {}).get("stateCode", ""))
    return row


def pull():
    seen_ids = set()
    rows = []
    for city in MARKETS:
        for segment in SEGMENTS:
            for page in range(MAX_PAGES):
                params = build_params(city, segment, page)
                try:
                    r = requests.get(BASE_URL, params=params, timeout=30)
                except requests.RequestException as e:
                    print(f"  ! request error {city}/{segment} p{page}: {e}")
                    break
                if r.status_code == 429:
                    print("  ! rate limited, sleeping 5s"); time.sleep(5); continue
                if r.status_code != 200:
                    print(f"  ! {r.status_code} {city}/{segment} p{page}: {r.text[:120]}")
                    break

                data = r.json()
                events = ((data.get("_embedded") or {}).get("events") or [])
                if not events:
                    break

                for ev in events:
                    eid = ev.get("id")
                    if eid and eid not in seen_ids:      # dedupe across city/segment overlap
                        seen_ids.add(eid)
                        rows.append(parse_event(ev))

                total_pages = ((data.get("page") or {}).get("totalPages") or 1)
                print(f"  {city:14s} {segment:7s} page {page+1}/{min(total_pages,MAX_PAGES)}  (+{len(events)})")
                if page + 1 >= total_pages:
                    break
                time.sleep(SLEEP_SECONDS)
    return rows


def main():
    print(f"Pulling {len(MARKETS)} markets x {len(SEGMENTS)} segments ...")
    rows = pull()
    out_path = os.path.abspath(OUTPUT)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    # quick data-quality summary
    n = len(rows)
    with_price = sum(1 for r in rows if r["price_min"] != "")
    print(f"\nDone. {n} unique events -> {out_path}")
    if n:
        print(f"  {with_price} have a price ({with_price*100//n}%). "
              f"The rest missing price is expected — that's part of the data story.")

if __name__ == "__main__":
    main()
