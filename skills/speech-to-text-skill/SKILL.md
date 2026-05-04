---
name: speech-to-text-skill
description: Speech-to-text workflow for audio or video messages. When the user says STT, ask them to send an audio message, extract audio from video if needed, transcribe with SiliconFlow FunAudioLLM/SenseVoiceSmall, and reply in the appropriate Chinese/English output language.
version: 1.0.0
author: Hermes Agent
tags: [speech-to-text, asr, transcription, siliconflow, video, audio, cantonese, mandarin, english]
---

# Speech to Text Skill

Use this skill when the user wants transcription from a voice note, audio message, or video message containing speech.

## Trigger

- If the user says `stt`, ask them to send an audio message.
- If the user already sent an audio or video message and asks for transcription, proceed directly.

## Workflow

1. Ask the user to send an audio message when they only typed `stt`.
2. Accept either:
   - an audio message
   - a video message with speech
3. If the input is a video message, extract the audio track first using `ffmpeg`.
4. Use the `siliconflow-media` skill and its ASR workflow.
5. Run SiliconFlow ASR with `FunAudioLLM/SenseVoiceSmall`.
6. Detect the spoken language:
   - Cantonese (Hong Kong)
   - Mandarin
   - English
7. Output the transcription/translation in the correct language:
   - Cantonese → Traditional Chinese
   - Mandarin → Simplified Chinese
   - English → English

## Important rules

- Prefer the `FunAudioLLM/SenseVoiceSmall` model for transcription when available.
- If the user explicitly requests a different ASR model, follow that request instead of the default.
- If the user sends a video, always extract audio before transcription.
- If language is mixed, choose the dominant spoken language and mention that briefly if needed.
- Keep the final response concise and provide only the transcribed text unless the user asks for extra detail.

## Practical notes

- Use `ffmpeg` to extract audio from video files, for example:
- See `references/output-contract.md` for the current output contract and example normalization behavior.

- If the user wants a retry with a different ASR engine, keep the response format stable: show both literal transcript and normalized meaning, rather than replacing one with the other.

```bash
ffmpeg -i input.mp4 -vn -acodec copy output.m4a
```

- If direct stream copy fails, convert to a compatible audio format such as WAV or MP3.
- If transcription quality is unclear, return the best-effort transcription and note uncertainty briefly.
- If the user corrects a transcription, treat that as a signal to inspect model choice and listening assumptions before replying again.
- See `references/model-selection-and-pitfalls.md` for model-choice notes and failure modes.
- If the user corrects a transcription, treat that as a signal to inspect model choice and listening assumptions before replying again.
- See `references/model-selection-and-pitfalls.md` for model-choice notes and failure modes.

## Output language mapping

- Cantonese audio → reply in `繁體中文`
- Mandarin audio → reply in `简体中文`
- English audio → reply in `English`

## Response format

When possible, output both:

1. **Literal transcript** — the closest verbatim transcription of what was spoken.
2. **Normalized meaning** — the most likely intended phrasing, cleaned up for clarity and naturalness.

If the audio is in:
- Cantonese: keep the literal transcript and normalized meaning in `繁體中文`
- Mandarin: keep both in `简体中文`
- English: keep both in `English`

Use a compact structure such as:

- `Literal:` ...
- `Normalized:` ...

If you are uncertain, keep the literal transcript faithful and make the normalized phrase conservative.

## Dependencies

- `siliconflow-media` skill
- `SILICONFLOW_API_KEY` environment variable
- `ffmpeg` for video-to-audio extraction
