---
name: hkbus-skill
slug: hkbus-skill
version: 1.1.0
description: Hong Kong bus ETA lookup for KMB, CTB, and LWB with fast stop matching, bilingual output, and safe no-result fallbacks.
---

# Hong Kong Bus ETA

Use this skill for Hong Kong bus ETA / next bus questions.
It supports KMB, CTB, and LWB routes, bilingual output, fuzzy stop matching, and multi-route queries.

## When to use

Use when the user asks for:
- next bus / arrival time / ETA
- 香港巴士到站時間
- route + stop lookup
- single-route or multi-route ETA checks

## Core workflow

1. Prefer the skill’s script output.
2. Use exact or normalized stop matching first.
3. If no result, retry conservatively with a shorter stop keyword or common alias.
4. If still no result, return the fixed fallback message.

## Journey-planning note

This skill is optimized for *ETA / stop lookup*, not full origin-to-destination trip planning.
If the user asks for a route like "from here to 元朗" or "去某區", first identify the likely destination hub/landmark (for example: 元朗市中心, 元朗站, 朗屏站) and then look up current route/timetable sources.
For this workflow, see `references/route-planning.md`.

Preferred approach for planning questions:
- Ask for the exact target if the area name is broad.
- Search official route pages or timetable PDFs when ETA lookup alone is insufficient.
- If you find a likely direct bus, present it as a candidate and avoid claiming certainty unless verified from a current source.
- Offer to narrow by "最少行路 / 最快 / 直達優先 / live ETA".

Example: for Pak Shek Kok / Science Park to 元朗市中心, a likely direct candidate may exist, but it should still be verified against the current timetable before being treated as definitive.

## Commands

### Single route

```bash
python3 scripts/eta.py {ROUTE} {STOP_NAME} {LANG}
```

### Refresh local stop cache

```bash
python3 scripts/sync_bus_stops.py
```

## Parameters

- `ROUTE`: bus route number, for example `A29`, `98D`, `118`
- `STOP_NAME`: stop keyword, for example `機場`, `Airport`, `寶琳`
- `LANG`: `tc` for Chinese or `en` for English

## Language rules

- Use `en` when the user asks in English or non-Chinese text.
- Use `tc` when the user asks in Chinese.
- Return the script output directly when possible.

## Output rules

- Do not invent ETAs.
- Do not add unrelated explanation.
- Small formatting cleanup is allowed if it improves readability.
- For no-result cases, use these exact fallbacks:
  - `tc`: `尾班車已過或未有班次資料`
  - `en`: `Service hours have passed / No route information found`

For multi-route queries, add the route label before the fallback, for example:
- `296D：尾班車已過或未有班次資料`
- `296D: Service hours have passed / No route information found`

## Multi-route queries

When the user asks for more than one route, run the route checks in parallel if possible.

Example:

```bash
cd {skill_dir}/scripts && (python3 eta.py A29 機場 tc & python3 eta.py E22A 機場 tc & wait)
```

## Terminus handling

If a stop is both an origin in one direction and a terminus in the other direction:
- show the boarding direction by default
- show terminus ETAs only when the user explicitly asks for that direction

## Practical notes

- Keep retries conservative; do not brute-force many stop variants.
- The skill may use local cached stop data for faster lookup.
- Only read or write files inside the skill directory.
- Do not request or output secrets, tokens, or credentials.

## Linked scripts

- `scripts/eta.py`
- `scripts/bus_query.py`
- `scripts/sync_bus_stops.py`
