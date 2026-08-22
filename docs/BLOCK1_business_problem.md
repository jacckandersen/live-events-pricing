# Block 1 — The Real Business Problem

## The company
**Cadence Live** — a mid-size live-events promoter and ticketing operation that
books and sells tickets for concerts and comedy across US markets. Revenue is
per-ticket margin plus fees, so the commercial team lives or dies on two things:
pricing events correctly for their market, and putting the right *volume* of
events into the right cities. Too many events chasing the same market cannibalize
each other; too few in a hungry market leaves money on the table.

## My role
Analyst on the **Commercial Strategy** team, reporting to the **VP of Commercial**.
I sit between the booking team (who decide what goes where) and finance.

## The stakeholder and what they actually care about
**VP of Commercial** owns pricing and inventory allocation. Their recurring
questions, the ones that trigger this project:
- *"Are we priced in line with the market in each city, or are we leaving margin
  on the table / pricing ourselves out?"*
- *"Which markets are saturated with events in a genre, and which are underserved?
  Where should we add or pull back inventory next quarter?"*

## The trigger (a decision, not "insights")
Cadence is planning next quarter's booking calendar. Before the booking team
commits venues and dates, Commercial needs a **market-by-genre read**: which
city-genre combinations are *underpriced relative to comparable markets* and which
are *oversaturated with supply*. That read decides where to push more events and
where to hold back — a concrete allocation decision worth real money.

## What "demand" means here (honesty up front)
The Ticketmaster Discovery API gives **listed price ranges** and **event/venue
metadata** — NOT ticket sales or attendance. So we cannot measure realized demand
directly. We proxy it with what the data supports:
- **Supply density** — count of events per city per genre (saturation).
- **Price positioning** — an event's price range vs the market median for its
  genre and market tier (over/under-priced).
- **Venue scale** — venue capacity as a rough ceiling on market size.
- **On-sale timing** — lead time to event, where available, as a soft signal.

Realized demand (sell-through, actual attendance) is explicitly out of scope and
listed in "what this can't answer" — it would need internal sales data or a
resale-price feed.

## The one-sentence goal
> Give Commercial a ranked, defensible list of city-genre segments that are
> underpriced or oversaturated, so next quarter's booking and pricing decisions
> are made on market position rather than gut feel.
