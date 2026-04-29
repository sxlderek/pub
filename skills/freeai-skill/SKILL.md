---
name: freeai-skill
description: Research free-tier limitations for AI providers. When a user says “freeapi” or asks about free-tier limitations, ask which provider to research, then summarize free models, rates, and other constraints.
version: 1.0.0
author: Hermes Agent
tags: [research, ai, free-tier, models, pricing, limits, providers]
---

# Free AI Provider Research Skill

Use this skill when the user asks about a provider’s free tier, free API, free models, or types `freeapi`.

## Trigger rule

If the user says **freeapi** or asks about **free-tier limitations** for an AI provider, first ask:

> Which AI provider should I research?

Do not guess the provider unless the user already named it clearly.

Examples of providers the user might enter:
- OpenRouter
- GitHub Models
- Anthropic
- Gemini
- Azure OpenAI
- Together
- Groq

## Goal

Help the user decide which free-tier AI provider is suitable for a project.

## Research workflow

1. Confirm the provider name if missing.
2. Research current public docs / pricing / model pages.
3. Prefer official sources first, but also check reputable internet sources when official docs are incomplete or hard to access.
4. If the provider looks brand- or region-specific, search using both the company name and product name, and inspect whether the public site is only a consumer/login shell with the API area hidden behind authentication.
5. Extract free models and free-tier limits.
6. Note any unusual registration or access requirements.
7. If no public free-tier model list or quota is published, say so explicitly instead of inferring one from the login-gated UI.

Helpful non-official sources can include curated directories or community resources such as:
- `https://github.com/cheahjs/free-llm-api-resources`
- `https://free-llm.com/`

Use these as supporting sources, not replacements for official docs when official docs are available.

## Provider-specific notes

### OpenRouter

- The public models API at `https://openrouter.ai/api/v1/models` exposes free models as entries whose IDs end with `:free` and whose prompt/completion pricing is `0`.
- The FAQ says new users get a very small free allowance to test the service.
- OpenRouter’s FAQ also says free models have low daily request caps and are usually not suitable for production.
- If the user has purchased credits, the free-model daily allowance changes to a separate lower cap; mention that distinction explicitly.
- OpenRouter provides a `openrouter/free` router that auto-selects a free model.
- When reporting rate limits, prefer the FAQ’s daily allowance language plus the model API’s context window and modality; exact per-model RPM/RPD may vary and should be verified from the live API if needed.

### Groq

- Groq’s public pricing page at `https://groq.com/pricing` lists the current model catalog and per-token pricing, including context windows and throughput.
- Groq’s public site advertises a `Free API key` flow and says to `Get started for free`, but the public pages do not clearly publish a numeric free quota or request allowance.
- The public docs pages on `console.groq.com` may be access-restricted in browser sessions; if that happens, use the public marketing and pricing pages as the fallback source.
- Some Groq models are enterprise-only (`Contact us`) rather than self-serve.
- Groq also has separately billed products such as compound tools, batch API, TTS, and ASR; do not treat those as part of the free API tier unless the docs explicitly say so.
- For Groq, report `unknown` or `not publicly stated` for free-tier quota limits when the public docs do not specify them.

### GitHub Models

- Inspect both `https://github.com/features/models` and the GitHub Docs Models pages, because the public marketing page may mention free usage while the docs page may have additional billing/usage notes.
- Treat `github.com/marketplace/models` as potentially sign-in gated; use the docs pages as the authoritative source when the marketplace catalog is not directly accessible.
- GitHub often documents free access by **model family / tier** rather than a single public model catalog. If exact model availability is not published, list the documented families or specific models mentioned in the docs and mark missing context windows as `not publicly stated`.
- When free-tier limits are published, capture the full bucket: RPM, RPD, tokens per request, and concurrent requests.
- Call out `public preview`, `subject to change`, and `opt in to paid usage` as part of the free-tier limitations.
- Mention any account/org requirements or feature gating if access differs between personal accounts and organizations.
- If docs say a family is `Not applicable` on Copilot Free, include that explicitly instead of trying to infer a free limit.

Observed GitHub Models free-tier patterns from the docs:
- Playground and free API usage are free resources, but rate limited.
- Low, high, embedding, and certain Azure OpenAI / DeepSeek / xAI families have different quotas.
- GitHub requires a personal access token with `models:read` for local API use.
- For production, GitHub recommends paid usage or BYOK via OpenAI/Azure keys.

## Output format

Keep the reply short and easy to understand.

### 1) Free models list
Provide a compact bullet list with one bullet per model, using this structure:
- `model-name` — `input context-window`, `modality`, `rate`

Formatting rules:
- Keep `model-name` short by removing unnecessary provider prefixes/suffixes when it remains unambiguous.
- Round context windows to K or M when appropriate, e.g. `262K` instead of `262000`.
- Use short forms when possible: `8K` instead of `8000`, `RPD` instead of `requests/day`.
- Use `text` instead of `text-generation`.
- If exact context windows are not public, say `unknown` or use the documented token/request cap if that is the only available limit.

### 2) Other free-tier limitations
Summarize in bullets, such as:
- RPM / RPD / token caps
- concurrent request limits
- public preview / subject to change
- model-family restrictions
- API vs playground differences
- region, account, or organization restrictions
- paid upgrade thresholds
- whether the provider publishes user inputs and outputs, if documented

### 3) Unusual registration / access requirements
If the provider requires anything unusual, call it out clearly, for example:
- Discord account
- Telegram account
- GitHub account
- KYC / identity verification
- invite-only access
- waitlist / approval
- phone verification
- credit card required even for free tier

## Style

- Be concise.
- Prefer factual bullets over long paragraphs.
- If the provider name is ambiguous, ask one clarifying question only.
- Do not invent model lists or limits; verify from current sources.

## Suggested research sources

- Official provider docs
- Pricing pages
- Model catalogs / marketplaces
- Help center / FAQ pages
- Community announcements only if official docs are incomplete

## Example interaction

User: `freeapi`
Assistant: `Which AI provider should I research?`

User: `OpenRouter`
Assistant: researches OpenRouter free models and limits, then returns the compact table and bullet summary.
