# Block 2 — How to pull the data

## 1. Get your Consumer Key
On the Ticketmaster developer portal, click your app (`ajack2600-App`) and
copy the **Consumer Key**. That is your API key. Keep it private — never commit it.

## 2. Install the one dependency
```
pip install requests
```

## 3. Set your key as an environment variable (don't hardcode it)
Windows PowerShell:
```
$env:TM_API_KEY="paste_your_consumer_key_here"
```
Windows cmd:
```
set TM_API_KEY=paste_your_consumer_key_here
```
Mac/Linux:
```
export TM_API_KEY="paste_your_consumer_key_here"
```
(The variable only lasts for that terminal session — set it again if you reopen.)

## 4. Run it
```
cd extract
python extract_events.py
```
You'll see it page through markets. When done it writes `events_raw.csv`
one level up (in the project root) and prints how many events it got and what
fraction have a price.

## What it pulls
Concert (Music) + Comedy events across 20 major US metros, deduped by event id.
For each event: name, segment/genre, city/state, venue + venue id, event date,
on-sale date, and price min/max (when the API provides it).

## Expect missing prices
Many events return no `priceRanges`. That is normal for the Discovery API and
is part of the project's data-quality story — we handle it in cleaning (Block 4)
and note it in limitations, rather than pretending every event has a price.

## Next
Once `events_raw.csv` exists, we load it into Postgres (Block 3) and start the
SQL analysis. Tell me the row count and the % with price it prints, and I'll
tailor the cleaning + analysis to what actually came back.
