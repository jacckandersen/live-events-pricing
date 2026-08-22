"""
Deezer enrichment — demand proxy for priced artists (no auth required).

WHY THIS EXISTS
---------------
Spotify's API stopped returning popularity/followers/genres on artist objects
for our app (confirmed: even GET /v1/artists/{id} came back without them).
Deezer's public API needs no auth and returns a per-artist `nb_fan` count,
which is a solid popularity/demand proxy. Downstream, `fans` replaces
`popularity`: price_per_fan = median price / avg fans.

USAGE
-----
Confirm ONE artist first (prints raw JSON + parsed values):
    python deezer_enrich.py --debug "Taylor Swift"

Full run over artists_priced.txt:
    python deezer_enrich.py
    # Delete artist_popularity.csv FIRST if an old/blank one is present.

No credentials needed.
Output: artist_popularity.csv
"""

import os, csv, sys, json, time, requests

HERE = os.path.dirname(os.path.abspath(__file__))
IN_FILE = os.path.join(HERE, "artists_priced.txt")
OUT_FILE = os.path.join(HERE, "artist_popularity.csv")
SEARCH_URL = "https://api.deezer.com/search/artist"
FIELDS = ["artist_name", "matched", "deezer_name", "deezer_id", "fans", "albums"]

PACE = 0.2          # seconds between artists; Deezer allows ~50 req / 5s
MAX_SLEEP = 30


def search_artist(name, debug=False):
    r = requests.get(SEARCH_URL, params={"q": name}, timeout=15)
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", "5"))
        if wait > MAX_SLEEP:
            return "BANNED"
        time.sleep(wait + 1)
        return search_artist(name, debug)
    if r.status_code != 200:
        return {"matched": False}
    body = r.json()
    if debug:
        print("\n--- raw SEARCH response (first hit) ---")
        hits = body.get("data") or []
        print(json.dumps(hits[0] if hits else body, indent=2)[:1500])
    # Deezer sometimes returns {"error": {...}} with HTTP 200
    if isinstance(body, dict) and body.get("error"):
        return {"matched": False}
    items = body.get("data") or []
    if not items:
        return {"matched": False}
    a = items[0]
    return {"matched": True,
            "deezer_name": a.get("name", ""),
            "deezer_id": a.get("id", ""),
            "fans": a.get("nb_fan", ""),
            "albums": a.get("nb_album", "")}


def debug_one(name):
    res = search_artist(name, debug=True)
    print("\n--- PARSED ---")
    print(json.dumps(res, indent=2))
    if isinstance(res, dict) and res.get("fans") not in ("", None):
        print(f"\nOK: fans came through ({res['fans']}). Safe to run the full 645.")
    else:
        print("\nWARNING: fans still blank. Inspect the raw JSON above.")


def main():
    if not os.path.exists(IN_FILE):
        raise SystemExit(f"Missing {IN_FILE}. Export the priced artists to it first.")
    artists = [l.strip().strip('"') for l in open(IN_FILE, encoding="utf-8") if l.strip()]
    artists = [a for a in artists if a.lower() != "artist_name"]

    done = set()
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(row["artist_name"])
    todo = [a for a in artists if a not in done]
    print(f"{len(artists)} priced artists, {len(done)} already done, {len(todo)} to go.")
    if not todo:
        print("Nothing to do — all priced artists already enriched."); return

    new_file = not os.path.exists(OUT_FILE) or os.path.getsize(OUT_FILE) == 0
    f = open(OUT_FILE, "a", newline="", encoding="utf-8")
    w = csv.DictWriter(f, fieldnames=FIELDS)
    if new_file:
        w.writeheader(); f.flush()

    matched = 0
    for i, name in enumerate(todo, 1):
        res = search_artist(name)
        if res == "BANNED":
            f.flush()
            print(f"\nDeezer rate-limit hit at {i-1}/{len(todo)}. Progress saved. Re-run to resume.")
            f.close(); return
        row = {k: "" for k in FIELDS}
        row["artist_name"] = name
        row["matched"] = False
        if isinstance(res, dict) and res.get("matched"):
            row.update(res); matched += 1
        w.writerow(row)
        if i % 25 == 0:
            f.flush()
            print(f"  {i}/{len(todo)}  (matched this run: {matched})")
        time.sleep(PACE)
    f.flush(); f.close()
    print(f"\nDone. All priced artists enriched -> {OUT_FILE}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--debug":
        debug_one(sys.argv[2])
    else:
        main()
