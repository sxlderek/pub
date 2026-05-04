# Extraction techniques for docren

Use this reference when the uploaded document is a PDF and text extraction is uncertain.

## Preferred order
1. `pymupdf` / `page.get_text()` for text-based PDFs
2. Tesseract OCR for scanned/image-only PDFs
3. Ask the user for missing fields if OCR is unavailable or ambiguous

## Tesseract install facts from this session
- Installed inside the container with:
  ```bash
  docker exec -u root hermes-gateway apt-get install -y tesseract-ocr tesseract-ocr-eng
  ```
- `pytesseract` was installed into Hermes venv with:
  ```bash
  UV_CACHE_DIR=/tmp/uv-cache uv pip install pytesseract Pillow
  ```
- OCR test on `/tmp/brother_page1.png` succeeded using:
  ```python
  from PIL import Image
  import pytesseract
  text = pytesseract.image_to_string(Image.open('/tmp/brother_page1.png'), lang='eng')
  ```

## Practical OCR note
- Tesseract is a real fallback for scanned PDFs in this environment, so the skill should prefer it before asking the user to transcribe fields manually.
- `lang='eng'` worked for the tested Brother document.

## Filename parsing pitfall observed
- OCR can surface noisy or partial document numbers. Verify the number against nearby labels before finalizing the suggestion.
- If the document is a confirmation/order form that contains both a customer number and a reference number, prefer the actual document reference over the customer number when it is clearly labeled.
