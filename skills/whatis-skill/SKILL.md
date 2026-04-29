---
name: whatis-skill
description: Explains terminology when the user says "whatis" (or "what is"). If the user pastes long text, extracts likely terms from it, asks for clarification if ambiguous, then explains each term in exactly 3 bullet points suitable for a 15-year-old and includes a direct link for software packages, open-source projects, or Wikipedia topics.
---

# whatis-skill

Use this skill when the user says **"whatis"** (or equivalent like **"what is"**) to ask for explanations of terminology.

## 1) First turn behavior (mandatory)

If the user only typed **"whatis"** (or gave no clear term):
- Ask them to provide **one or more terms** they want explained.
- Prompt format suggestion: “Send terms separated by commas, or paste text and I’ll pull the terms out.”

## 2) If the user provides terms (short input)

Treat the user input as a list of terminology when it is clearly:
- One term (e.g., `Kubernetes`)
- Or multiple terms separated by commas/new lines (e.g., `OAuth, JWT, SSO`)

If the input is ambiguous (could be a term vs. a question vs. a product name), ask a brief clarification question before explaining.

## 3) If the user pastes a long paragraph / multiple sentences

Goal: **identify the terminology embedded in the text**.

Process:
1. Extract 3–10 candidate terms from the text, prioritizing:
   - Capitalized proper nouns / product names (e.g., “Redis”, “Nginx”)
   - Acronyms (e.g., “CI/CD”, “RAG”, “GPU”)
   - Repeated or emphasized phrases
   - Technical noun phrases (2–4 words), especially ones that look like concepts (e.g., “vector database”, “public key”)
2. If you’re not confident which ones the user wants:
   - Present the extracted candidates as a short list and ask: **“Which of these should I explain?”**
   - Allow the user to select multiple.

## 4) Output requirements (strict)

For each terminology item the user confirms:
- Explain it in **exactly 3 bullet points**.
- Write for a **15-year-old**: plain language, minimal jargon, quick analogy if helpful.
- Keep each bullet to **1–2 sentences**.

### Link requirement
If the terminology is related to:
- a **software package** / **open-source project**, provide a direct link to its official homepage or GitHub repo (prefer official docs).
- a **Wikipedia topic**, provide a direct link to the Wikipedia page.

Place the link on its own line under the 3 bullets, prefixed by `Link:`.

## 5) Clarification rule

If you are not sure what term(s) the user wants explained, ask a clarification question instead of guessing.

## 6) Formatting template

Use this template per term:

Term: <term>
- <bullet 1>
- <bullet 2>
- <bullet 3>
Link: <url if applicable>
