#!/usr/bin/env bash
set -euo pipefail
VENV="/home/adminlin/.openclaw/workspace/.venv-idocr"
source "$VENV/bin/activate"
python3 "/home/adminlin/.openclaw/workspace/skills/id-ocr/scripts/mediapipe_facecheck.py" "$@"
