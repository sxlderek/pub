# whatis-skill

A tiny OpenClaw skill that turns **"whatis"** requests into **kid-friendly (15-year-old)** explanations.

## What it does

When a user types `whatis`:
- If no term is provided, it asks the user to input **one or more terms**.
- If the user pastes a **long paragraph**, it extracts likely terminology and asks which ones to explain if ambiguous.
- For each confirmed term, it explains it in **exactly 3 bullet points**.
- If the term is a **software package / open-source project / Wikipedia topic**, it includes a **direct link**.

## Examples

### 1) Prompting for terms

User:

```text
whatis
```

Assistant:

```text
Type one or more terminology you want me to explain...
```

### 2) Explaining multiple terms

User:

```text
whatis OAuth, JWT, SSO
```

Assistant (per term):

```text
Term: OAuth
- ...
- ...
- ...
Link: https://en.wikipedia.org/wiki/OAuth
```

### 3) Pasting text

User:

```text
whatis
<paste a paragraph>
```

Assistant:
- extracts 3–10 candidate terms
- asks which ones you want (when unclear)
- then explains the selected ones

## Files

- `SKILL.md` — the skill definition and behavior rules
- `LICENSE` — MIT

## License

MIT (see `LICENSE`).
