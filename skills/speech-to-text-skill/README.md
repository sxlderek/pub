# speech-to-text-skill

Speech-to-text workflow for audio and video messages.

## Origin
- Original skill source: created in this conversation
- Original skill source path: `/opt/data/skills/custom/speech-to-text-skill`
- Original author: Derek Chan + Hermes Agent

## Conversion
- Converted and tested in Hermes-agent format.
- Published as a Hermes skill package for the `pub/skills` repo.

## Notes
- If the user says `stt`, ask them to send an audio message.
- Video messages should have audio extracted with `ffmpeg` before transcription.
- Uses SiliconFlow `FunAudioLLM/SenseVoiceSmall` by default.
- Returns both a literal transcript and a normalized meaning when possible.
- Cantonese → Traditional Chinese
- Mandarin → Simplified Chinese
- English → English
