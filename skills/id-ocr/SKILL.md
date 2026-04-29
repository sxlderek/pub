---
name: id-ocr
slug: id-ocr
version: 1.1.0
description: Extract a person’s identity fields from an uploaded ID document image, including transliterated English name and normalized dates.
---

## When to Use

Use this skill when the user types **"id-ocr"** (or asks to OCR an ID document) and wants structured identity details extracted from an ID image.

## Core Rules

1) **Require an ID image first**
   - If the user has not provided an ID document image in the current conversation, ask them to upload a clear photo/scan of the ID (front, and back if relevant).
   - Assume the document can be in **any language**. Ask the user which language/country it is if unsure.

2) **Output exactly these fields** (in this order)
   1. Full Name (Native)
   2. Full Name (EN) — First name + Last name in English (best-effort phonetic transliteration; mixed case)
   3. DOB (YYYY-MM-DD)
   4. Document type (one of: National ID, Driving License, Passport, HK/Macau Pass(港澳通行证), or `[unclear]`)
   5. Document number (ID/passport/permit number; or `[unclear]`)
   6. Issuing country of the document
   7. Expiry (YYYY-MM-DD | N/A | [unclear])

3) **Be explicit about uncertainty**
   - If any field is missing/illegible, output it as: `[unclear]`.
   - If the document has **no expiry date**, output: `N/A`.

4) **English name casing (must be mixed case)**
   - Always output `Name (EN)` in **mixed case** (e.g., `Chunyue Liang`), not ALL CAPS.
   - If the ID prints the English name in ALL CAPS, convert it to mixed case.

5) **Transliteration rules (phonetic translate)**
   - If the ID does not provide an English/Latin name, produce a best-effort phonetic transliteration.
   - Prefer a language-appropriate romanization when obvious (examples: Chinese → pinyin; Japanese → Hepburn; Korean → RR; Thai → RTGS; Arabic → common passport-style Latinization).
   - If the script/language is unclear, ask a follow-up question (or provide a best-effort transliteration and mark `[unclear]`).

6) **Date normalization**
   - Convert any detected date format (e.g., DD/MM/YYYY, MM-DD-YY, local formats) into **YYYY-MM-DD**.
   - If only partial date is present (month/year only), output `[unclear]`.

7) **Privacy + minimal retention**
   - Do not store or repeat unnecessary sensitive details (ID number, address, MRZ, etc.) unless the user explicitly asks.

## Response Format

Return the results as 7 lines, exactly like:

Full Name (Native): ...
Full Name (EN): First Last
DOB: YYYY-MM-DD
Document type: National ID | Driving License | Passport | HK/Macau Pass(港澳通行证) | [unclear]
Document number: ... | [unclear]
Issuing country: ...
Expiry: YYYY-MM-DD | N/A | [unclear]

## Optional: Extract ID Photo + Generate Artistic Avatar

If the user asks for an **artistic avatar** (e.g., “make a social avatar”), do this after the 7-line output:

1) **Preprocess if needed (rotate + flatten)**
   - If the ID is tilted, run a best-effort card-boundary detection + perspective transform to flatten it before cropping.

2) **Extract the ID photo rectangle** from the document and send it back to the user.
   - Add padding and **verify the crop contains the full face (hairline → neck)** before sending.
   - Verification method (preferred): use **MediaPipe FaceMesh** to confirm mouth + chin + forehead landmarks are present with margin (not cut off). If it fails, retry with progressively larger padding and/or re-crop.
   - If you cannot reliably verify (repeated failures), ask the user for a clearer photo of the ID (less glare, higher resolution, straighter angle).
2) Ask the user for:
   - desired style (e.g., anime, watercolor, oil painting, Pixar-like, cyberpunk)
   - background (solid color / gradient / transparent)
   - aspect ratio (1:1 recommended for socials)
3) **Get explicit confirmation** before generating the avatar if the workflow requires sending the cropped photo to an external model/provider.
4) Generate 1–3 avatar variants and send them.

See `avatar.md` for prompt presets.

## Optional: Local OCR Workflow for ID Cards

If the user wants to inspect an ID card locally instead of receiving a transcription here, use a robust offline OCR pipeline:

1) **Flatten / deskew the card first**
   - Try 4-corner card detection with OpenCV perspective transform.
   - If card detection fails, fall back to a straight rotation search (0°, 90°, 180°, 270°).

2) **Preprocess for OCR**
   - Convert to grayscale.
   - Improve local contrast with CLAHE or histogram equalization.
   - Reduce noise with bilateral filtering.
   - Threshold with Otsu or adaptive thresholding.
   - Deskew the thresholded image before OCR.

3) **OCR multiple regions, not just the full card**
   - Full card
   - Text-heavy half (often the right side)
   - Bottom band (often where dates / numbers live)

4) **Use a Cyrillic-capable OCR engine**
   - Tesseract with `rus+eng` is a good first pass.
   - If Tesseract is weak on the photo, try EasyOCR as a fallback.

5) **Save debug intermediates**
   - Original
   - Flattened / rotated card
   - Preprocessed OCR inputs
   - Region crops

### Practical baseline script outline

A solid reusable baseline is a Python script that does the following:

- tries to flatten the card via contour detection
- picks the best of 0/90/180/270 orientation guesses
- preprocesses the whole card, right half, and bottom band separately
- runs OCR with `rus+eng`
- saves all OCR text and intermediate images for inspection

### Tesseract install

```bash
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng python3-opencv python3-pip
pip install numpy pytesseract pillow
```

### Recommended OCR settings

- Full card: `--oem 3 --psm 6`
- Dense text blocks: `--oem 3 --psm 4`
- Sparse / irregular text: `--oem 3 --psm 11`

### Why this is better than a single crop

Many ID cards mix:
- portrait area
- bilingual labels
- dates / document numbers at the bottom

A single OCR pass over the whole card often misses key text. Region-based OCR is usually more reliable.

### When to stop and ask for a better image

If the image is:
- blurry
- tilted heavily
- low resolution
- cropped too tightly
- covered by glare

then OCR quality will be poor no matter what model you use. Ask for a clearer front-facing photo instead of guessing.

## Optional: ID Photo Extraction (OpenCV)

If you need to extract the **ID photo rectangle** (not just a headshot crop), you can use the bundled helper scripts under `scripts/`.

### Requirements (WSL/Ubuntu)

```bash
sudo apt update
sudo apt install -y python3-opencv python3-numpy
```

### Model weights

Download OpenCV DNN face detector weights into:

`models/opencv-face/`

```bash
curl -L -o models/opencv-face/deploy.prototxt \
  https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt

curl -L -o models/opencv-face/res10_300x300_ssd_iter_140000_fp16.caffemodel \
  https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
```

### Scripts

- `scripts/crop_headshot_opencv_dnn.py` — detect face and produce a padded headshot crop (hair-to-chin style).
- `scripts/crop_id_photo_opencv.py` — attempt to crop the **ID photo rectangle**; falls back to a conservative face-based rectangle if border detection fails.
- `scripts/flatten_id_card.py` — rotate/flatten (deskew) the ID card via card-boundary detection.
- `scripts/mediapipe_facecheck.py` — verify crop contains full face (forehead/mouth/chin) using MediaPipe FaceMesh.
- `scripts/extract_id_photo_fullface.py` — flatten (best-effort) + photo-rect crop + **FaceMesh verification** with aggressive padding retries (recommended).
- `scripts/extract_id_photo_rect_verified.py` — edge-based photo-rectangle crop + basic verification + padding retries (baseline).

### Lightweight fallback when Python imaging libraries are unavailable

If the environment does not have Pillow/OpenCV available, a practical fallback is to use `ffmpeg` for the image transforms and then verify the result with vision:

1. Rotate the card first with `transpose=1` (clockwise) or `transpose=2` (counterclockwise) until the document is upright.
2. Crop the portrait from the rotated card using a conservative box that keeps the full hairline → shoulders area.
3. Inspect the crop visually; if the head is cut off or too much document text is included, enlarge or shift the crop and retry.
4. When possible, use vision/FaceMesh-style verification to confirm the crop includes the full face and enough shoulder padding.

This fallback is useful for quick one-off extraction when the more advanced scripts cannot run in the current environment.
