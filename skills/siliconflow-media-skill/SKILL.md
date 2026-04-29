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

## Practical Notes

- Keep the prompt short and specific when generating images or videos.
- For video generation, wait for the polling loop to finish; it may take 2–10 minutes.
- For image-to-video, provide a real input image path with `--image`.
- If `SILICONFLOW_API_KEY` is missing, the scripts exit immediately with an error.

## Linked Scripts

- `scripts/image_gen.py`
- `scripts/video_gen.py`
- `scripts/tts.py`
- `scripts/asr.py`
