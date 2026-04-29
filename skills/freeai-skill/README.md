# freeai-skill

Research free-tier limitations for AI providers.

## What it does

Use this skill when the user asks about:

- a provider’s free tier
- free API access
- free models
- request / token limits
- unusual signup or access requirements

## Output style

When you research a provider, return:

1. A compact list of free models with:
   - model name
   - context window
   - modality
   - rate / quota
2. A short bullet list of other free-tier limitations
3. A short note about unusual access requirements, if any

## Research rules

- Prefer official docs first
- Use reputable secondary sources when official docs are incomplete
- Do not invent model lists or limits
- If no public free-tier model list is published, say so explicitly

## Related docs

- `SKILL.md`
- `LICENSE`
