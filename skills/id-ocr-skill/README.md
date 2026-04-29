# id-ocr-skill

ID OCR skill converted from OpenClaw into Hermes-agent format.

## Origin
- Original skill source: `/home/derek/.openclaw/workspace/skills/id-ocr`
- Original author: Tom FONG

## Conversion
- Converted and tested in Hermes-agent format.
- Published as a Hermes skill package for the `pub/skills` repo.

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
