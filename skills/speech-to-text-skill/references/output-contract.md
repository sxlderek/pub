# Output contract

## Default ASR model
- Prefer `TeleAI/TeleSpeechASR` via SiliconFlow when available.
- If the user explicitly requests a different ASR engine, follow that request.

## Response format
- Always prefer a **literal transcript** plus a **normalized meaning** when possible.
- Keep the literal transcript faithful to the spoken audio.
- Keep the normalized meaning conservative and natural.
- Do not replace the literal transcript with a paraphrase.

## Language mapping
- Cantonese (Hong Kong) → `繁體中文`
- Mandarin → `简体中文`
- English → `English`

## Video handling
- If the input is a video message, extract the audio track with `ffmpeg` before transcription.
- If direct audio extraction fails, convert to a common format such as WAV or MP3 and retry.

## Useful examples
- Literal: `在香港,敵人做公司查查。`
- Normalized: `在香港，應該做公司查冊。`
