---
name: pollinations-skill
version: 1.0.0
description: Pollinations.ai generation and analysis toolkit for text, images, video, audio, vision, and transcription.
metadata:
  hermes:
    tags: [pollinations, media, vision, transcription, generation]
---

# Pollinations Skill

Use this skill when the user wants Pollinations-based generation or analysis:
- text/chat completion
- image generation or image editing
- video generation
- image/video analysis
- audio transcription
- text-to-speech / audio generation

## Requirements
- `curl`
- `jq`
- `base64`
- optional: `POLLINATIONS_API_KEY`

Free tier works without a key, but operations are rate-limited. If a key is available, use it for the same endpoints.

## Commands

### Text / chat
```bash
scripts/chat.sh "your prompt"
scripts/chat.sh "your prompt" --model claude
scripts/chat.sh "your prompt" --json
```

### Image generation
```bash
scripts/image.sh "a sunset over mountains"
scripts/image.sh "logo" --model gptimage --quality hd --transparent
scripts/image.sh "photo" --enhance --nologo
```

### Image editing
```bash
scripts/image-edit.sh "make it blue" --source input.jpg
scripts/image-edit.sh "add sunglasses" --source https://example.com/photo.jpg --model kontext
```

### Video generation
```bash
scripts/image.sh "a cat playing piano" --model veo --duration 6
scripts/image.sh "ocean waves" --model seedance --duration 8 --aspect-ratio 16:9
```

### Vision / image analysis
```bash
scripts/analyze-image.sh photo.jpg
scripts/analyze-image.sh image.png --prompt "extract all text"
```

### Video analysis
```bash
scripts/analyze-video.sh clip.mp4
scripts/analyze-video.sh clip.mov --prompt "summarize the key moments"
```

### Audio transcription
```bash
scripts/transcribe.sh recording.mp3
scripts/transcribe.sh podcast.wav --model gemini-large
```

### Text-to-speech
```bash
scripts/tts.sh "Hello world"
scripts/tts.sh "Welcome" --voice coral --format wav
```

### Model listing
```bash
scripts/models.sh
scripts/models.sh text
scripts/models.sh image
scripts/models.sh vision
scripts/models.sh audio
```

## Output rules
- Generation scripts save media to a file and print the saved path.
- Analysis and transcription scripts print text to stdout.
- Preserve the script defaults and model names; `scripts/models.sh` is the source of truth for the current catalog.

## Notes
- `scripts/image.sh` supports both image and video generation depending on the model.
- `--image-url` enables image-to-image or image-to-video flows where supported.
- For large or slower jobs, the analysis and transcription scripts already use longer timeouts.

## Troubleshooting
- If a generation returns a small text file such as `error code: 1027`, the request reached Pollinations but the selected model failed. Try a different image model or adjust the prompt.
- Always re-check the live model list with `scripts/models.sh image` before assuming a model name is currently available.

## Linked scripts
- `scripts/chat.sh`
- `scripts/image.sh`
- `scripts/image-edit.sh`
- `scripts/analyze-image.sh`
- `scripts/analyze-video.sh`
- `scripts/transcribe.sh`
- `scripts/tts.sh`
- `scripts/models.sh`
