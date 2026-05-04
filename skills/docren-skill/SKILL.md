---
name: docren-skill
description: "Document renaming assistant that suggests structured filenames based on document content (PDF/Word). Format: YYYYMMDD company-slug document-number short-description"
version: 1.6.0
author: Derek Chan
tags:
  - document-management
  - ocr
  - file-naming
  - productivity
---

# Document Renaming Skill (docren)

## Trigger Conditions
- User types `docren`
- User expresses intent to rename a document
- User uploads a PDF or Word document and mentions renaming
- The request clearly implies document renaming

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

Do not send full OCR dumps to a model unless absolutely necessary.

## Workflow

### 1. Request Document Upload
When triggered, always ask the user to upload the document before analysis:

`Please upload the document (PDF or Word format) that you'd like to rename.`

If the user has not uploaded a file yet, do not attempt filename suggestions.

### 2. Token-Saving Extraction Strategy
Use the cheapest reliable path first:
1. Text extraction first for PDFs and Word files
2. OCR only if text extraction is empty or clearly incomplete
3. OCR only page 1 first unless the first page clearly lacks the needed fields
4. Use compact extraction: keep only date/company/number/type lines
5. Ask only one clarification question at a time when a single field is missing

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
If the PDF is scanned or image-only:
- First try `tesseract` OCR with English language (`eng`)
- If the document is bilingual Chinese/English, preserve both when possible
- If available, use `pytesseract` in the Hermes venv
- If OCR is unavailable or fails, ask the user for clarification rather than guessing

Typical OCR flow:
1. Render page 1 to image
2. Run Tesseract OCR
3. Extract only relevant lines/fields
4. OCR more pages only if necessary

### 5. Word Document Rules
For `.docx` files:
- Extract text directly from the document
- Prefer the first page/first section for company name and document type
- Use headings, titles, and metadata when present
- If a `.docx` is image-only, treat it like a scanned PDF and OCR the minimum needed pages

### 6. Parse and Structure Information

**Date (YYYYMMDD):**
- Look for issue date, statement date, invoice date, or document date
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
- `Systems Xpress Limited` → `SXL` for this user's documents

**Document Number:**
- Prefer the labeled invoice/statement/policy/reference/quotation number
- Include prefixes if they are part of the number
- If no number exists, use `NA` or ask for clarification

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

## Pitfalls
- Scanned PDFs usually require OCR; text extraction alone may fail
- Preserve bilingual content when it matters
- Use `/opt/hermes/.venv/bin/python3` for Python package access
- Multiple dates: prioritize the document date
- No document number: use `NA` or ask for clarification
- Preserve the original file extension
- If a receipt or confirmation references another document, clarify which number to use
- If the user says `docren`, do not start analysis until they upload the file

## Example Output
`20240415 HKBNES 22677128 order-confirmation.pdf`

## Notes
- Keep slugs recognizable and consistent across documents from the same company
- Prioritize clarity over brevity when in doubt
- Prefer compact summaries over raw OCR dumps
