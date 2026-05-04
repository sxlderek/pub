---
name: siliconflow-media
slug: siliconflow-media
version: 1.0.0
description: SiliconFlow media workflows for image generation, video generation, TTS, and ASR.
---

## When to Use

Use this skill when the user wants to use **SiliconFlow** for:
- image generation or image editing
- text-to-video or image-to-video generation
- text-to-speech (TTS)
- speech-to-text / ASR

Do **not** use this skill as the wrapper for OmniRoute/OpenAI/ElevenLabs model routing. If the requested model lives in OmniRoute, call OmniRoute directly and use the provider-model-listing skill for discovery/debugging.

### Language caveat

In live tests, `FunAudioLLM/CosyVoice2-0.5B` was reachable through SiliconFlow and worked for Mandarin/English output, but it did **not** reliably produce Cantonese in this environment. If the user requests Cantonese audio, verify the language output before assuming CosyVoice is sufficient.

## Requirements

- Environment variable: `SILICONFLOW_API_KEY`
- Billing is through SiliconFlow credits/vouchers.
- Video jobs can take several minutes.

## Commands

### Image generation

```bash
uv run {baseDir}/scripts/image_gen.py --prompt "描述" --filename "output.png" [--model MODEL]
```

Models:
- `flux` → `black-forest-labs/FLUX.1-schnell` (default)
- `flux-dev` → `black-forest-labs/FLUX.1-dev`
- `flux-pro` → `black-forest-labs/FLUX.1-pro`
- `qwen` → `Qwen/Qwen-Image`
- `qwen-edit` → `Qwen/Qwen-Image-Edit`
- `qwen-edit-2509` → `Qwen/Qwen-Image-Edit-2509`
- `kolors` → `Kwai-Kolors/Kolors`

Practical note:
- Kolors worked successfully for a funny-kitten prompt in a live test, so it is a good choice when the user explicitly asks for Kolors.
- **User preference: Always use Kolors by default for image generation unless the user specifies a different model** (e.g., "use flux", "use qwen").
- **High-quality alternatives via OmniRoute**: NanoBanana (`nanobanana/nanobanana-pro`, `nanobanana/nanobanana-flash`) and GPT Image (`openai/gpt-image-2`, `pollinations/gpt-image-2`, `pollinations/gptimage-large`) are available for high-quality generation when explicitly requested. See `references/babo-background.md` for details.

### Image editing (background replacement, semantic edits)

For semantic image edits like background replacement, use Qwen-Image-Edit via the standard generations endpoint with an `image` parameter:

```bash
export UV_CACHE_DIR=/tmp/uv-cache
uv run {baseDir}/scripts/image_edit.py --input "input.jpg" --output "output.jpg" --prompt "change the background to white"
```

The script calls `/v1/images/generations` with:
- `model: "Qwen/Qwen-Image-Edit"`
- `prompt: "<edit instruction>"`
- `image: "data:image/jpeg;base64,<base64_data>"`

**When to use AI image editing vs ImageMagick:**
- **AI models (Qwen-Image-Edit)**: semantic edits like background replacement, object removal, style changes — produces clean, context-aware results
- **ImageMagick**: geometric transforms (resize, crop, rotate), format conversion, simple overlays — NOT for semantic edits (results are crude)

### Video generation

```bash
# Text to video
uv run {baseDir}/scripts/video_gen.py --prompt "描述" --filename "output.mp4"

# Image to video
uv run {baseDir}/scripts/video_gen.py --prompt "描述" --image "input.png" --filename "output.mp4"
```

Models:
- `Wan-AI/Wan2.2-T2V-A14B` for text-to-video
- `Wan-AI/Wan2.2-I2V-A14B` for image-to-video

### Text to speech

```bash
uv run {baseDir}/scripts/tts.py --text "要合成的文字" --filename "output.mp3" [--model MODEL]
```

Models:
- `fish-speech` → `fishaudio/fish-speech-1.5` (default)
- `cosyvoice` → `FunAudioLLM/CosyVoice2-0.5B`
- `indextts` → `IndexTeam/IndexTTS-2`
- `moss` → `fnlp/MOSS-TTSD-v0.5`

### ASR

```bash
uv run {baseDir}/scripts/asr.py --audio "input.mp3" [--model MODEL]
```

Models:
- `sensevoice` → `FunAudioLLM/SenseVoiceSmall` (default)
- `teleai` → `TeleAI/TeleSpeechASR`

## Output Rules

- `image_gen.py`, `video_gen.py`, and `tts.py` all print a final `MEDIA: <absolute_path>` line.
- `asr.py` prints the transcription as plain text.
- If a request fails, the script prints the error to stderr and exits non-zero.

## User-Specific Preference

- For this user, prefer `FunAudioLLM/CosyVoice2-0.5B` (`--model cosyvoice`) for Cantonese text-to-speech unless they explicitly ask for another voice/model.
- When the user says things like “讀出嚟畀我聽” or asks for voice output in Cantonese, default to the CosyVoice workflow.

## Image Editing Pitfalls

**Background replacement with Qwen-Image-Edit or Kolors**:
- These models often modify the foreground object when asked to "change only the background"
- Even explicit prompts like "change canvas to white, do not modify the lobster" can result in pure white output or altered foreground
- For precise background-only replacement, use a dedicated background removal tool (e.g., `rembg`) instead

## Practical Notes

- Keep the prompt short and specific when generating images or videos.
- For video generation, wait for the polling loop to finish; it may take 2–10 minutes.
- For image-to-video, provide a real input image path with `--image`.
- If `SILICONFLOW_API_KEY` is missing, the scripts exit immediately with an error.
- For voice questions, answer in the same language/register as the spoken input:
  - Cantonese voice question → reply in `繁體中文`
  - Mandarin voice question → reply in `简体中文`
  - English voice question → reply in plain English
- This skill is for *SiliconFlow* TTS/ASR/image/video workflows. If the user asks for OmniRoute/OpenAI/ElevenLabs speech, use the provider-specific flow instead of this script.
- Do not assume `FunAudioLLM/CosyVoice2-0.5B` will always output Cantonese just because the input text is Cantonese; verify with a short sample first.

## User Preference Note

- If the user asks for text-to-speech or voice output, prefer `siliconflow-media`'s `tts.py` workflow rather than the built-in Edge TTS.
- Do not route the user back to Edge TTS unless they explicitly ask for it.

## Linked Scripts

- `scripts/image_gen.py`
- `scripts/image_edit.py` — Qwen-Image-Edit for semantic edits (background replacement, object removal)
- `scripts/video_gen.py`
- `scripts/tts.py`
- `scripts/asr.py`

## Linked References

- `references/tts-session-notes.md` — session notes and verified caveats for Cantonese/English TTS
- `references/background-removal.md` — when to use rembg instead of generative image editing for background replacement
- `references/omniroute-flux-api.md` — OmniRoute Flux API response format: returns base64 in `b64_json`, not URL
- `references/babo-background.md` — user-defined "babo background" style: soft blue gradient bokeh for product photography, includes NanoBanana and GPT Image model recommendations
- `references/hermes-memory-increase.md` — how to permanently increase Hermes memory limits via config.yaml editing
