# HK Bus ETA — route planning note

This note captures a common adjacent workflow: users sometimes ask for a *route* rather than an ETA.

## Trigger

- "去元朗幫我找巴士路線"
- "from here to X"
- "nearest route to Y"
- Any origin -> destination query where no exact stop name is provided

## Recommended workflow

1. Identify the destination hub/landmark if the user uses a broad area name.
   - Example mappings:
     - 元朗 → 元朗市中心 / 元朗站 / 朗屏站 / 元朗（西） depending on the trip intent
     - 科學園 / Pak Shek Kok → Science Park / Pak Shek Kok / Tai Po area as origin context
2. Search official route pages or timetable PDFs first.
3. Use the ETA script only *after* a route and stop are known.
4. If a likely direct route is found, present it as a candidate and mark it as needing timetable verification if not checked live.

## Practical clue from the session

For a trip from Pak Shek Kok / Science Park area to 元朗市中心, KMB 64X appeared as a plausible direct candidate in web search results, but the route should still be verified against the current timetable before being stated as final.

## Output style

- Keep the answer short.
- Mention whether the route is direct or likely needs a transfer.
- Offer to narrow by:
  - 最少行路
  - 最快到
  - 直達優先
  - live ETA
