Live Events: Market Segmentation & Price-Positioning Analysis

Same product, double the price: Jazz tickets sell for a median $38 in New York but $19 in Los Angeles. One signal in a market-opportunity map that tells a live-events promoter where to expand, defend, and pull back next quarter.

A commercial analytics project built on live data pulled from the Ticketmaster Discovery API, enriched with metro population data, and analyzed in PostgreSQL. It segments US live-events markets by supply saturation and price position, then fuses both into a single prioritization matrix.

Skills demonstrated: multi-API integration (Ticketmaster + Deezer) · multi-source data enrichment · data cleaning on messy real-world data · market segmentation · price-positioning analysis · window functions & percentile statistics · hypothesis testing · honest limitation-setting.

1. Business context

Cadence Live (fictional) is a mid-size live-events promoter that books and sells tickets for concerts and comedy across US markets. Its commercial team wins or loses on two levers: pricing events correctly for each market, and allocating the right volume of events per city: too many cannibalize each other, too few leave money on the table.

As an analyst on the Commercial Strategy team reporting to the VP of Commercial, the trigger for this project is next quarter's booking calendar. Before the booking team commits venues and dates, Commercial needs a market-by-genre read: which city-genre segments are underpriced relative to comparable markets, and which are oversaturated with supply, a concrete allocation decision, not "insights."

2. The data
Attribute	Detail
Source	Two live APIs: Ticketmaster Discovery (events) + Deezer (artist fan-count); enriched with metro-area population
Grain	One row per event (concert or comedy show)
Volume	16,016 unique events across 20 major US metros
Coverage	88% have a named artist; 15% carry a usable listed price (see §7)
Key fields	event, artist, genre, city/state, venue, event date, on-sale date, price min/max

Two live APIs feed the project: the Ticketmaster Discovery API for events and the Deezer API for artist fan-count (the demand proxy in §4 Finding 6). Spotify was the original demand source but was dropped after its API stopped returning popularity/followers for this app, so Deezer was substituted, a real data-sourcing call. A third input, metro-area population (20 metros, CSV), is joined on city for per-capita intensity.

3. Methodology (and why each choice over the alternatives)
Per-capita normalization over raw counts. Raw event counts just rank cities by size (New York wins everything). Dividing by metro population surfaces true intensity and is immune to the mix-distortion that share analysis suffers from (§ Finding 1).
Median (percentile_cont) over mean for prices. Ticket prices are right-skewed by VIP packages; the median reports the typical ticket, not an average dragged up by outliers. The p25 to p75 spread captures pricing consistency, not just level.
Window functions over self-joins for benchmarks. Each city-genre is compared to its genre's cross-city average via AVG(...) OVER (PARTITION BY genre), computing the benchmark in place without collapsing rows.
Thin-segment gating throughout. Every comparison is gated on a minimum event count (10 to 30 depending on the cut) so small samples don't masquerade as findings.
Hypothesis testing, not assertion. The "destination markets" explanation was stated, then tested against venue concentration and refuted (§ Finding 2).
4. Key findings

▶ Explore the interactive dashboard on Tableau Public

Finding 1: Population normalization overturns the naive read. Share analysis flagged Las Vegas as under-represented in Rock (−10.3 pts vs the national norm). Per-capita analysis ranks Vegas #1 in Rock events per 100k residents (10.56). The share signal was a mix artifact: Vegas Comedy is so dominant (28.6/100k) that it compressed every other genre's share. Decisions should use per-capita intensity, not share.

Finding 2: "Destination market" dominance is real breadth, not mega-venues (hypothesis tested & refuted). Vegas and Nashville top per-capita intensity across genres. Hypothesis: a few tourist mega-venues inflate the counts. Test: top-3 venue share per city. Result refutes it: Las Vegas has 63 distinct venues with only 29.5% of events in its top 3 (one of the least concentrated markets). The most-concentrated markets are actually San Antonio (61.9%) and Miami (58.4%), which were not the per-capita leaders. The dominance is genuine market depth.

Finding 3: The headline, same genre, double the price across markets. Jazz sells for a median $38.10 in New York (+$5.42 vs the genre benchmark, 251 priced events) but $18.80 in Los Angeles (−$13.89, 85 events). LA applies the same low floor to R&B (−$9.65), suggesting it systematically underprices these genres. This is a concrete, sample-backed pricing action: test increases on LA Jazz/R&B, or confirm LA is structurally price-sensitive.

Finding 4: Pricing landscape, level and consistency. Median price runs from Jazz ($35, priciest) to Dance/Electronic ($25). The spread adds nuance: Comedy has the highest floor (p25 $29) but a wide top (p75 $48), rarely cheap, occasionally premium; Folk is tightly clustered ($25 to $35), predictable; Hip-Hop/Rap is the widest ($19 to $36), unstandardized pricing.

Finding 5: Seasonality, a universal fall surge with a genre offset (supporting). In the reliable booking window, volume peaks in fall for every genre, but Rock/Pop/Country/Alternative peak in October while Comedy and Jazz lead a month earlier in September. Booking implication: September for intimate formats, October for mainstream music. (Honestly scoped: this is the current booking calendar's shape, not multi-year seasonality, see §7.)

Finding 6: Pricing is largely demand-blind (new: artist-demand layer). Enriching each artist with a Deezer fan-count demand proxy (635/645 priced artists matched, 98%) and correlating fan-count against event price within each market shows that in 10 of 12 markets, price barely tracks demand, correlations cluster near zero. Denver (−0.25) and Portland (−0.12) even run slightly inverse: bigger-draw artists are priced the same or lower than smaller ones. Only Los Angeles (+0.39) and anomalous San Diego price meaningfully to demand. Commercial read: where price and demand are decoupled, popular acts are systematically underpriced relative to their pull, headroom to raise prices on high-demand bookings. Honestly scoped: listed prices, not sales, so this flags a test-worthy gap, not a proven inefficiency. (A simpler price-per-fan ratio was tried first and rejected as unstable, see docs/FINDINGS.md.)

Synthesis: The Market Opportunity Matrix. Supply intensity (per-capita) and price position (vs peers) fuse into a 4-quadrant action label per city-genre:

Quadrant	Meaning	Top examples
EXPAND	Premium price + under-served	New York R&B (+$9.65, 0.20/100k); New York Jazz (+$5.42, 256 events)
DEFEND	Premium but saturated	Nashville Country (+$4.50, 11.67/100k); Chicago Rock
AVOID	Below-peer price + saturated	Nashville Rock (−$1.79); Denver Comedy

This is the deliverable: a ranked, defensible where-to-expand-vs-defend-vs-avoid list for the booking calendar.

5. Recommendations
Expand booking in premium under-served segments: prioritize New York Jazz (the most reliable signal, 256 events, commands +$5.42) and New York R&B for added inventory next quarter. (Owner: Booking team.)
Test price increases on LA Jazz and R&B, currently ~$14 and ~$10 below comparable markets on solid samples. Run a controlled price lift on the next tranche and measure sell-through. (Owner: Pricing/Commercial.)
Defend, don't flood, Nashville Country and Chicago Rock: premium but already saturated; protect margin rather than add supply. (Owner: Commercial Strategy.)
Time the calendar by format: slot comedy/jazz for September, mainstream music for October, matching where each genre's supply already concentrates.
Test demand-based price lifts on high-draw acts in decoupled markets: in Denver, Portland, and Chicago, price barely tracks artist demand, so the most popular bookings are the likeliest to be underpriced. Run a controlled lift on top-fan-count acts and measure sell-through. (Owner: Pricing/Commercial.)
6. Repo guide
live-events-pricing/
├── extract/       Python live Ticketmaster Discovery API extractor
├── enrichment/    metro population data + Deezer artist fan-count pull (demand proxy)
├── sql/           staging + analysis queries (00 load, 01 clean, 02-05 analysis)
├── docs/          business problem, findings log
├── live_events_walkthrough.pptx   12-slide commercial walkthrough deck
├── LICENSE
└── README.md

Reproduce: set a Ticketmaster API key, run extract/extract_events.py, load the CSV into Postgres (sql/00_create_raw.sql), build the clean view (sql/01_staging.sql), run analyses 02 to 04. For the demand layer, follow enrichment/HOW_TO_ENRICH.md (Deezer, no auth) and run sql/05_demand_vs_price.sql. Requires Python 3 + requests, and PostgreSQL. Data pulls (events_raw.csv, artist_popularity.csv) are regenerated from the APIs and are not committed.

7. Limitations & assumptions
Price coverage is 15% and worst exactly where volume is highest (Rock/Pop ~12% priced vs Jazz 82%). Pricing findings are gated to genres/markets with enough priced events; Rock/Pop pricing is caveated. 398 zero-price records were excluded as free/placeholder entries.
No sales or attendance data. The API gives listed prices, not realized demand. Below-peer pricing can mean untapped pricing power or genuinely weak local demand, the data can't distinguish them.
Per-capita uses resident population, which overstates intensity for tourism markets (Vegas, Nashville). A per-visitor denominator would refine it.
Seasonality is a single snapshot, not multi-year history; the 2027 taper is partly a booking-horizon artifact. Junk dates (2038, 2039) were excluded.
Artist-demand layer (delivered): artists are enriched with a Deezer fan-count demand proxy to test whether markets price in line with the demand they book (§4 Finding 6). Spotify was the original plan, but its API stopped returning popularity/followers on artist objects for this app, so Deezer's auth-free fan-count was substituted. Fan-count is a proxy for demand, not sales, so the value-gap read is directional.
