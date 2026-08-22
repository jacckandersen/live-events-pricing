# Findings (with numbers) — fill/adjust from query outputs

## Finding 1 — Population normalization overturns the share-based read
Share analysis flagged Las Vegas as *under*-represented in Rock (-10.3 pts vs the
national genre norm). But per-capita analysis ranks Las Vegas **#1 in Rock events
per 100k residents (10.56)**. The share signal was a mix artifact: Vegas Comedy is
so dominant (28.62 events/100k, also #1) that it compressed every other genre's
*share*, making Rock look thin when it is actually the most intense Rock market.
Takeaway: share reveals specialization; per-capita reveals true intensity — and
they can disagree. Decisions should use per-capita.

## Finding 2 — Destination markets dominate per-capita intensity
Las Vegas and Nashville (mid-size metros, ~2.1–2.3M) occupy the top per-capita
ranks across multiple genres — Vegas #1 in Comedy/Theatre/Rock/Pop/Dance,
Nashville #1 in Country/Alternative. They punch far above population because they
are tourism/destination markets whose events serve visitors, not just residents.
Limitation: resident-population denominator overstates intensity for tourism
markets — a per-visitor denominator would refine this (data we don't have).

## Finding 3 — Genre specialization is real and matches domain intuition
The metric recovers known market identities as a validity check: Nashville→Country
(#1, 11.57/100k), Vegas→Comedy, New York→Theatre (share 39.8%). That the data
independently reproduces real-world specialization is evidence the saturation
metric measures something true, not noise.

## Finding 4 (pending) — Price positioning on the 17% priced subset
Only 2,785 of 16,013 events (17%) carry a price. Where cells are dense enough,
compare an event's price range to the market/genre median to flag over/under-priced
segments. Gated on minimum priced-event count per cell (thin-segment discipline).

## Explicit limitations
- 17% price coverage → pricing is a secondary, gated analysis, not the backbone.
- Resident population overstates intensity for tourism markets (Vegas, Nashville).
- No sales/attendance → we measure supply intensity, not realized demand.
- Metro populations are approximate; final version should cite Census figures.
- ~116 events in junk classification buckets were excluded.

## Finding 4 — Price coverage is worst exactly where volume is highest
Zero-priced records: 398 (14% of priced events) were excluded as free/placeholder
(price_min = 0). On the clean subset (price_min > 0, 2,380 events): price coverage
varies wildly by genre. The highest-volume genres have the WORST coverage — Rock
(3,084 events, ~12% priced), Pop (~12%) — while niche genres are well-covered
(Jazz 82%). So pricing claims about Rock/Pop rest on a thin, possibly unrepresentative
slice and must be caveated; Jazz/Blues/Alternative pricing is solid.

## Finding 5 — Pricing landscape: premium vs value genres, floor vs spread
On gated genres (30+ priced events), median price_min ranges from Jazz ($35.46,
priciest) down to Dance/Electronic ($24.95). Beyond the median, the p25–p75 spread
is itself informative: Comedy has the highest FLOOR (p25 $29.13) but a wide top
(p75 $48.10) — comedy rarely goes cheap; Folk is tightly clustered ($24.61–$35.46)
— predictable pricing; Hip-Hop/Rap has the widest relative spread ($18.80–$36.16)
— unstandardized pricing.

## Finding 6 — Premium markets by genre (actionable pricing signal)
Comparing each city's genre-median to the genre's cross-city average (gated 15+
priced events): NEW YORK JAZZ commands $38.10 vs the $32.69 genre benchmark
(+$5.42) on a robust 251 priced events — the most reliable premium-market signal.
Boston Jazz (+$9.77) and NYC R&B (+$9.65) show larger gaps but on thin samples
(19, 16 events) — suggestive, not conclusive. This is the "where do we have
pricing power" read the commercial team needs.

## Finding 6b — The headline: same genre, double the price across markets
Jazz sells for roughly 2x in New York vs Los Angeles, on reliable samples:
  - New York Jazz:  median $38.10  (+$5.42 vs benchmark),  251 priced events
  - Los Angeles Jazz: median $18.80 (-$13.89 vs benchmark),  85 priced events
LA also underprices R&B ($18.80, -$9.65, 62 events) — the same floor as its Jazz,
suggesting LA systematically underprices these genres vs the national norm.
Decision this unblocks: test price increases on LA Jazz/R&B, or confirm LA is a
structurally price-sensitive market for them. Either way it's a concrete,
sample-backed pricing action — not "analyze trends."
Caveat: below-peer pricing can mean either untapped pricing power OR genuinely
weaker local demand; the API's listed prices can't distinguish the two without
sales data.

## Finding 2 (VALIDATED) — Per-capita dominance is real breadth, not mega-venues
Hypothesis: Vegas/Nashville's high per-capita intensity was a "few tourist
mega-venues" artifact. Test: top-3 venue share per city.
Result REFUTES the hypothesis:
  - Las Vegas: 63 distinct venues, only 29.5% of events in its top 3 (one of the
    LEAST concentrated markets) — 1,995 events spread broadly.
  - Nashville: 27 venues, 35.2% top-3 — mid-pack concentration.
Most-concentrated markets are actually San Antonio (61.9%) and Miami (58.4%),
which were NOT the per-capita leaders. So Vegas/Nashville dominance reflects
genuine market depth across many venues, not a handful of tourist venues.
Bonus findings: Miami is a thin, concentrated market (14 venues, 101 events,
58.4% top-3); New York is the most diversified (65 venues, 36.7% top-3).
Method note: hypothesis stated, tested, refuted — conclusion changed by evidence.

## SYNTHESIS — Market Opportunity Matrix (the capstone deliverable)
Combined supply intensity (events per 100k, from population enrichment) with
price position (vs genre's cross-city median) into a 4-quadrant action map per
city-genre. This is the marketing prioritization deliverable — every segment
gets an EXPAND / DEFEND / TEST / AVOID label.

TOP EXPAND targets (premium pricing + under-served):
  - New York R&B    : +$9.65 vs peers, 0.20 events/100k  (pays premium, thin supply)
  - Boston Jazz     : +$9.77, 0.51/100k
  - New York Folk   : +$6.73, 0.24/100k
  - Phoenix Alt.    : +$7.09, 1.14/100k
  - New York Jazz   : +$5.42, 1.30/100k  (256 events — most reliable)

DEFEND (premium but already saturated — protect margin, don't flood):
  - Nashville Country: +$4.50 but 11.67/100k (very crowded)
  - Chicago Rock     : +$4.46, 2.63/100k
  - Phoenix Rock     : +$5.69, 2.86/100k

AVOID (saturated + below-peer pricing):
  - Nashville Rock   : -$1.79, 9.05/100k
  - Denver Comedy    :  0.00, 2.42/100k
  - Denver Dance/Elec: -$1.67, 3.02/100k

Decision unblocked: a ranked, defensible where-to-expand-vs-defend-vs-avoid list
for next quarter's booking calendar — market position, not gut feel.
Method: two independent analyses (Ticketmaster supply + Census-style population +
listed pricing) fused via window functions into one prioritization score.

## Finding 7 — Seasonality: a universal fall surge, with a genre offset (supporting)
Within the reliable booking window (Aug 2026–Jan 2027; further-out and junk dates
excluded — see data-quality note), event volume peaks in fall across all genres:
  - Rock, Pop, Country, Alternative → peak in OCTOBER
  - Comedy, Jazz → peak one month earlier, in SEPTEMBER
Rock's October peak is huge (1,032 events), reflecting fall arena-tour season.
Read: the fall surge is broadly universal, but intimate-format genres (comedy,
jazz) lead mainstream music by ~a month. Booking implication: Sept for comedy/jazz,
Oct for mainstream music.

DATA-QUALITY / METHOD NOTE (important, discovered by exploration):
This is a single snapshot of *currently-listed* events, not multi-year history.
Volume tapers in 2027 partly because far-out events aren't listed yet (a booking-
horizon artifact, NOT falling demand). A handful of junk dates (2038-01, 2039-01,
scattered 2025/2028) were excluded as data errors. So this is "distribution of the
current booking calendar," honestly caveated — not confirmed seasonal demand.
Confirming true seasonality would need multi-year historical event data.

## Finding 8 — Pricing is largely demand-blind (the value-gap headline)
Demand proxy: Deezer fan-count per artist (nb_fan), matched to 635/645 priced
artists (98%). [Substituted for Spotify popularity — Spotify's API stopped
returning popularity/followers on artist objects for our app, confirmed against
GET /v1/artists/{id}, which came back without those fields. Deezer's fan-count is
a comparable, auth-free demand proxy.]
Method: within each market, Pearson correlation between artist fan-count and event
mid-price ((price_min+price_max)/2), gated at 20+ priced events (12 markets qualify).
Result: across 10 of 12 markets, price barely tracks demand — correlations cluster
near zero:
  - Denver -0.245, Portland -0.121  (price runs slightly INVERSE to demand)
  - Philadelphia -0.065, Chicago -0.052, Nashville -0.040, Detroit +0.024,
    Miami +0.025, Phoenix +0.029, New York +0.089  (essentially no relationship)
  - Seattle +0.190, Los Angeles +0.394  (weak-to-moderate coupling)
  - San Diego +0.706  (strong — but avg price $167 vs ~$30-75 elsewhere; likely a
    premium/VIP-skewed sample of 60 events, treat as anomalous, not exemplary)
Read: in most major markets, what an artist charges is close to unrelated to how
popular they are. For a promoter that prices to demand, that is headroom — popular
acts appear systematically underpriced relative to their pull.
Why correlation, not a price-per-fan ratio: the ratio (median price / fans) was
tried first and was unstable — the city ranking flipped completely between
average-fans and median-fans denominators (Denver moved from mid-pack to #1
"overpriced"), because median fans swing ~50x across cities and dominate the ratio.
Event-level correlation uses every event and does not hinge on that arbitrary choice.
Method note: metric proposed, stress-tested, rejected for a more robust one — the
conclusion followed the evidence, not the first idea.
Caveat: listed prices, not realized sales. A near-zero correlation means price does
not track THIS demand proxy — not that pricing is provably wrong (markets may price
on venue size or production cost). This is a test-worthy hypothesis, not a proven
inefficiency. Per-market samples run 20-247 events: directional, not conclusive.
