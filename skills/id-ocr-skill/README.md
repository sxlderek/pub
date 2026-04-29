# id-ocr-skill

Extract a person’s identity fields from an uploaded ID document image.

## What it does

Use this skill when the user asks to OCR an ID document or types `id-ocr-skill`.

## Output

Return:

1. Full Name (Native)
2. Full Name (EN)
3. DOB
4. Document type
5. Document number
6. Issuing country
7. Expiry

## Notes

- Ask for an ID image if none was provided.
- Prefer mixed-case English names.
- Normalize dates to `YYYY-MM-DD`.
- Mark unclear fields as `[unclear]`.
- Keep sensitive details minimal unless explicitly requested.

## Related files

- `SKILL.md`
- `LICENSE`
