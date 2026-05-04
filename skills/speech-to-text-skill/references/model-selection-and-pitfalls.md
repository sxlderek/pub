# Model selection and pitfalls

## Default model
- Use `FunAudioLLM/SenseVoiceSmall` as the default STT model.
- This has been the preferred model when transcribing the user's Cantonese, Mandarin, and English voice notes.

## Transcript handling
- Do not infer a language from a rough transcript alone if the audio is unclear.
- If the transcript seems wrong, the likely next step is to reassess the model or the transcription pass, not to guess a different language.
- Keep the literal transcript faithful; keep normalization conservative.

## User correction signal
- If the user says a transcription is wrong, treat it as a real correction signal.
- Prefer updating the model choice or the transcription workflow rather than defending the previous result.

## Output reminders
- Cantonese audio → Traditional Chinese
- Mandarin audio → Simplified Chinese
- English audio → English
- If uncertain, say so briefly instead of overconfidently normalizing.
