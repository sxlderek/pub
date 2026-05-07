# Email Attachments via Himalaya

Session-observed workflow for docren-ing email attachments:

1. List inbox envelopes with attachments:

```bash
himalaya envelope list --account hermes --output json
```

2. Download attachments for the selected message IDs into `/tmp/incoming/...`:

```bash
himalaya attachment download --account hermes --downloads-dir /tmp/incoming/hermes-email-attachments 2 3 4
```

3. Process the resulting PDFs locally with docren.

## Notes
- `himalaya envelope list --output json` is useful because it exposes `has_attachment` and sender info cleanly.
- Message bodies can be image-only PDFs even when the envelope text looks fine.
- In this environment, `pymupdf` + `rapidocr-onnxruntime` worked reliably after installing to `/opt/data/python-packages`.
- `himalaya attachment download` writes attachment files using the original attachment names if available.
- Keep downloaded mail attachments in `/tmp/incoming/` before moving renamed files into `/mnt/aihome/docren/sorted/`.
