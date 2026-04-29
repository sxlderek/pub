# whois-skill

Look up domain WHOIS information and optionally capture website screenshots.

## What it does

Use this skill when the user asks for:

- WHOIS lookups
- DNS records
- DMARC / SPF / DKIM checks
- TLS certificate details
- website screenshots

## Notes

- Validate and sanitize user input before any external calls.
- Keep the final response compact and send it once.
- Use timeouts for every external command.

## Related files

- `SKILL.md`
- `LICENSE`
