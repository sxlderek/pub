---
name: docren-skill
description: "Document renaming assistant that suggests structured filenames based on document content (PDF/Word). Format: YYYYMMDD company-slug document-number short-description"
version: 1.8.1
author: Derek Chan
tags:
  - document-management
  - ocr
  - file-naming
  - productivity
---

# Document Renaming Skill (docren)

## Trigger Conditions
- User explicitly asks to run `docren` / process documents / rename files
- User types `docren` with a path → process all documents in that directory
- User uploads a PDF or Word document and mentions renaming → process only the uploaded document
- The request clearly and explicitly implies document renaming
- If the user asks to check Hermes email for PDFs, attachments, or mailbox documents and then run docren, treat that as an explicit docren request and use Hermes Mailbox Attachment Mode
- User asks to process multiple documents in a directory (batch mode)

### Automation Policy
- **No scheduled processing**: do not create or rely on recurring cron jobs for docren unless the user explicitly asks for automation.
- **Explicit only**: do not auto-process `/mnt/aihome/docren/` just because the user typed `docren` alone; ask for or infer a specific explicit request instead.
- **Issue Resolution**: if issues are encountered during processing (e.g., missing dependencies, permission errors), diagnose and fix them so the requested task can complete.
- **Scope**: process only files directly in the target directory unless the user explicitly asks to include subdirectories.

## Trigger Conditions
- User explicitly asks to run `docren` / process documents / rename files
- User types `docren` with a path → process all documents in that directory
- User uploads a PDF or Word document and mentions renaming → process only the uploaded document
- The request clearly and explicitly implies document renaming
- If the user asks to check Hermes email for PDFs, attachments, or mailbox documents and then run docren, treat that as an explicit docren request and use Hermes Mailbox Attachment Mode
- User asks to process multiple documents in a directory (batch mode)

### Automation Policy
- **No scheduled processing**: do not create or rely on recurring cron jobs for docren unless the user explicitly asks for automation.
- **Explicit only**: do not auto-process `/mnt/aihome/docren/` just because the user typed `docren` alone; ask for or infer a specific explicit request instead.
- **Issue Resolution**: if issues are encountered during processing (e.g., missing dependencies, permission errors), diagnose and fix them so the requested task can complete.
- **Scope**: process only files directly in the target directory unless the user explicitly asks to include subdirectories.

## Routing Policy
Use the cheapest reliable route first:
1. Extract text locally with `pymupdf` or Word text extraction
2. If the document is scanned or incomplete, OCR page 1 only
3. Extract only the minimum fields needed: date, company, document number, document type
4. Use a low-cost model only on the compact summary if a model is needed for final disambiguation
5. Escalate to a stronger model or ask the user only when ambiguity remains

Recommended model usage:
- `gemini 2.5 lite`: good default for compact document understanding
- `glm-4.6v`: good scanned-page backup when a vision model is needed
- `gpt-5-nano`: good lightweight final formatter when extraction already did most of the work

See `references/token-saving-routing.md` for the compact extraction/routing recipe.
See `references/ocr-fallbacks.md` for the local OCR stack and verification pattern that worked in Hermes.
See `references/searchable-pdf-sidecar.md` for the resolved preference on in-place searchable PDFs vs sidecars.
See `references/batch-processing.md` for batch-scope and file-move handling notes.
See `references/email-attachments-from-himalaya.md` for the email-download → docren workflow.

Do not send full OCR dumps to a model unless absolutely necessary.

## Workflow

### 1. Determine Mode

**Automatic Batch Mode:**
When the user types `docren` alone (no file upload, no explicit path):
- Automatically process all documents in `/mnt/aihome/docren/`
- Skip the `sorted/` and `failed/` subdirectories themselves
- Create `sorted/` and `failed/` subdirectories if they don't exist (with group 100)
- Process each document and move to `sorted/` (success) or `failed/` (error)
- Report a summary

**Hermes Mailbox Attachment Mode:**
When the user explicitly asks to check the Hermes mailbox for PDF attachments and run docren on them:
- Use the configured Hermes email account to list mail in INBOX
- Prefer messages with `has_attachment=true` or obvious PDF-related subjects/senders
- Download attached PDFs to a temporary working directory under `/tmp/incoming/`
- Extract and rename each attachment using the standard docren rules
- Save the renamed outputs to `/mnt/aihome/docren/sorted/`
- If a message or attachment cannot be processed, report the blocker and save the failed item to `/mnt/aihome/docren/failed/` when possible
- Do not ask for confirmation for this flow unless a destructive move is required outside the docren output directories

**Explicit Batch Mode:**
When the user specifies a directory path (e.g., "docren /path/to/dir"):
- Process all documents in that directory
- Create `sorted/` and `failed/` subdirectories if they don't exist (with group 100)
- Move successfully renamed documents to `sorted/`
- Move failed documents to `failed/`
- Report a summary

**Interactive Single-Document Mode:**
When the user uploads a document via Telegram/WhatsApp or other channels:
- Process the uploaded document
- Rename it according to the standard format
- Save the renamed document to `/mnt/aihome/docren/sorted/` (success) or `/mnt/aihome/docren/failed/` (error)
- Report the new filename and location

**Legacy Interactive Mode:**
When triggered without a file or directory:
- Ask: `Please upload the document (PDF or Word format) that you'd like to rename.`

For batch mode, use filename-based heuristics first (date patterns, company names, document numbers in the original filename) before falling back to full content extraction. This is faster and often sufficient for well-named source files.

### 2. Token-Saving Extraction Strategy
Use the cheapest reliable path first:
1. **Batch mode**: Try filename-based extraction first (patterns in original filename)
2. Text extraction first for PDFs and Word files
3. OCR only if text extraction is empty or clearly incomplete
4. OCR only page 1 first unless the first page clearly lacks the needed fields
5. Use compact extraction: keep only date/company/number/type lines
6. Ask only one clarification question at a time when a single field is missing

Do not paste full OCR dumps into chat unless needed. Reduce raw document output to a compact summary before responding.

### 3. Extract Document Content
- Use `pymupdf` for text-based PDFs
- Extract text directly from Word documents (`.docx` preferred)
- If the document appears scanned or image-only, OCR the first page first
- If page 1 is insufficient, OCR only the minimum additional pages needed
- Read the document to identify:
  - Document date (YYYYMMDD format)
  - Company/organization name
  - Document number
  - Document type

### 4. OCR Rules for Scanned PDFs
### 4. OCR Rules for Scanned PDFs
If the PDF is scanned or image-only:
- Render page 1 to an image before OCRing it
- Deskew scanned pages before OCR when the page is visibly tilted or skewed
- Remove blank pages before OCR and before saving the final processed document when they are clearly empty
- Treat a page as blank when it has no meaningful text and only negligible marks (for example: empty OCR result, page number only, or tiny specks/noise)
- Prefer a Chinese-capable OCR path for mixed Chinese/English pages: `RapidOCR` on the rendered image works well in this environment
- If using Tesseract, set `TESSDATA_PREFIX=/opt/data/tessdata` so `chi_sim` and `chi_tra` are available
- If the document is bilingual Chinese/English, preserve both when possible
- If available, use `pytesseract` in the Hermes venv
- For page-image understanding, prefer SiliconFlow vision/OCR helpers when available: use OCR for text extraction, then use a vision-capable chat model to verify the issuer/date/number/type before renaming.
- In live Hermes testing, SiliconFlow OCR can be noisy on scan-style Chinese business documents: `PaddlePaddle/PaddleOCR-VL-1.5` returned a lot of garbage on a scanned MPFA notice, while `Qwen/Qwen3-VL-32B-Instruct` produced a compact, usable field extraction for the same pages.
- In live Hermes testing, SiliconFlow vision models can be picky about parameters: some reject `enable_thinking`; omit it unless the model is known to support it.
- See `references/siliconflow-docren-vision-fallback.md` for the verified scan/OCR fallback recipe and field-verification workflow.
- The verified fallback pattern is: render page 1 to PNG, run SiliconFlow OCR first if you want text, then use a SiliconFlow vision model to confirm the final rename fields when OCR is noisy.

- If OmniRoute `auto/ocr` returns `Stream ended before producing useful content`, treat it as a model/path failure and fall back to a local OCR install or ask the user for clarification rather than guessing

Typical OCR flow:
1. Render page 1 to image
2. Deskew if needed
3. Remove blank pages if needed
4. Run RapidOCR or Tesseract OCR with the correct tessdata
5. Extract only relevant lines/fields
6. OCR more pages only if necessary

### 5. Word Document Rules
For `.docx` files:
- Extract text directly from the document
- Prefer the first page/first section for company name and document type
- Use headings, titles, and metadata when present
- If a `.docx` is image-only, treat it like a scanned PDF and OCR the minimum needed pages

### 6. Parse and Structure Information

**Date (YYYYMMDD):**
- Look for issue date, statement date, invoice date, or document date
- If no date can be found in the document content, use the date embedded in the filename
- Format as 8 digits

**Company Slug (1-3 words, max 15 chars):**
- Prefer the shortest recognizable official name
- Abbreviate common phrases:
  - Hong Kong → HK
  - Limited → Ltd
  - Corporation → Corp
  - Company → Co
  - International → Intl
  - Enterprise → Ent
  - Holdings → Hldgs
  - Services → Svc
- Prefer English when both English and Chinese names appear
- Use Chinese only if no English company name appears
- Keep Chinese company names in Chinese; do not transliterate unless asked
- Company-specific abbreviations are local overrides only
- `Systems Xpress Limited` → `SXL` for this user's documents when Systems Xpress is the subject/recipient
- For debit notes, use the issuer/creator company as the company slug instead of the recipient; `W.S. Wong Certified Public Accountant (Practising)` → `W.S.Wong`, and use `CPA` as the shorthand for `Certified Public Accountant`

**Document Number:**
- Prefer the labeled invoice/statement/policy/reference/quotation number
- Include prefixes if they are part of the number
- If no number exists or is uncertain, use `NA`

**Short Description (1-5 words, max 20 chars):**
- Common types:
  - invoice
  - bank-statement
  - insurance-policy
  - receipt
  - quotation
  - contract
  - tax-invoice
  - credit-note
  - delivery-note
  - order-confirmation
  - application-form
  - price-list
- Prefer `cert` over `certificate` in filenames when the document type is certificate-related
- Keep it specific but concise

### 7. Ask for Clarification
If anything important is unclear:
- Ask one specific question
- Use a numbered list if choices are needed
- Avoid asking for information already found

Example:
1. Use `NA` for the document number
2. Omit the document number
3. Enter the number manually

### 8. Output Suggested Filename
Format:

`YYYYMMDD company-slug document-number short-description.pdf`

## Tools Required
- `pymupdf` - primary text extraction for text PDFs
- `tesseract-ocr` - OCR engine for scanned PDFs
- `pytesseract` - Python wrapper for Tesseract
- `Pillow` - image handling for OCR
- `python-docx` or similar Word text extraction support
- Ghostscript / ImageMagick - useful for PDF-to-image conversion

## Support Files
- `references/filename-parsing-patterns.md` - Filename-based extraction patterns for when pymupdf/OCR is unavailable
- `references/extraction-techniques.md` - Text extraction methods
- `references/token-saving-routing.md` - Cost-effective routing

## Pitfalls
- Scanned PDFs usually require OCR; text extraction alone may fail
- Preserve bilingual content when it matters
- Use `/opt/hermes/.venv/bin/python3` for Python package access
- Multiple dates: prioritize the document date
- No document number: use `NA` or ask for clarification
- Preserve the original file extension
- If a receipt or confirmation references another document, clarify which number to use
- **NEW BEHAVIOR**: When the user types `docren` alone, automatically process `/mnt/aihome/docren/` — do NOT ask them to upload a file
- **NEW BEHAVIOR**: When a document is uploaded via messaging platforms, save the renamed result to `/mnt/aihome/docren/sorted/` or `/mnt/aihome/docren/failed/`
- In batch mode, create sorted/ and failed/ directories with group ownership matching the parent directory (typically gid 100 in NAS environments)
- **Batch mode**: Create `sorted/` and `failed/` directories with group 100 (gid 100) using `mkdir -p` with appropriate permissions
- **Batch mode**: When moving files, handle filenames with spaces or special characters using proper quoting
- **Batch mode**: Skip processing files that are already in `sorted/` or `failed/` subdirectories
- **Preflight write check**: before moving any files, verify the runtime can write to *both* target directories (`sorted/` and `failed/`) with an actual create/remove test (`touch` or a temporary file), not just `stat`; if either target returns `Permission denied`, stop and report the blocker instead of pretending the rename ran
- **Scanner-generated PDFs**: if metadata shows scanner provenance (e.g. `Brother Scanner System`) and the PDF is image-only, treat it as OCR-required rather than content-rich; when reporting a failure, separate *document-quality* issues from *filesystem/permission* issues so the user knows whether the file failed because of OCR ambiguity or because the move itself was blocked
- **Permission fallback**: if batch renaming fails because the runtime cannot write to NAS-mounted storage, provide the suggested filenames and ask the user to fix ownership/ACLs or rerun in a write-enabled shell

## Example Output
`20240415 HKBNES 22677128 order-confirmation.pdf`

## Notes
- Keep slugs recognizable and consistent across documents from the same company
- Prioritize clarity over brevity when in doubt
- Prefer compact summaries over raw OCR dumps
