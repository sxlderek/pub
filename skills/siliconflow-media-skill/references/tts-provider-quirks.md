# TTS Provider Quirks

## Session findings

### SiliconFlow / `FunAudioLLM/CosyVoice2-0.5B`
- Script path: `scripts/tts.py`
- Environment override needed in this environment:
  - `HOME=/tmp`
  - `UV_CACHE_DIR=/tmp/uv-cache`
- Successful run:
  - `uv run /opt/data/skills/custom/siliconflow-media/scripts/tts.py --text '你好，我是 Hermes。现在我用普通话跟你打招呼。' --filename '/tmp/cosyvoice_mandarin_greeting.mp3' --model cosyvoice`
- Important caveat:
  - The output was Mandarin; it did **not** reliably produce Cantonese in live tests.

### OmniRoute / `qwen/qwen3-tts`
- OmniRoute discovery endpoint worked:
  - `GET https://omniroute.uk.sxl.net/v1/models`
- `qwen/qwen3-tts` exists as an audio speech model.
- Live TTS requests returned:
  - `500 Speech request failed: fetch failed`
- Treat as currently unstable in this environment.

### OmniRoute / `openai/gpt-4o-mini-tts`
- Live TTS request returned:
  - `429 You exceeded your current quota`
- Treat as quota-limited unless the account is upgraded.

### OmniRoute / `elevenlabs/eleven_multilingual_v2`
- Model exists in OmniRoute catalog.
- Live TTS request without a custom `voice_id` returned:
  - `402 Free users cannot use library voices via the API`
- Passing a library name like `Rachel` as `voice_id` returned `404`.
- Treat as requiring a valid ElevenLabs `voice_id` and appropriate plan.
