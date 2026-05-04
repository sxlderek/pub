# TTS Session Notes

## Verified Cantonese TTS flow

Use the SiliconFlow TTS script with CosyVoice:

```bash
HOME=/tmp UV_CACHE_DIR=/tmp/uv-cache \
  uv run /opt/data/skills/custom/siliconflow-media/scripts/tts.py \
  --text '讀出嚟畀我聽' \
  --filename '/tmp/cosyvoice_cantonese.mp3' \
  --model cosyvoice
```

### Why the environment overrides matter

In this session, running `uv run` from `/opt/data` failed because uv tried to initialize its cache under:

- `/opt/data/home/.cache/uv/...`

That path was not writable and produced:

- `failed to open file '/opt/data/home/.cache/uv/sdists-v9/.git': Permission denied (os error 13)`

Setting both `HOME=/tmp` and `UV_CACHE_DIR=/tmp/uv-cache` resolved the issue.

### Result

The command successfully generated:

- `MEDIA: /tmp/cosyvoice_cantonese.mp3`

## Practical note

- For Cantonese voice output, `FunAudioLLM/CosyVoice2-0.5B` is a reasonable default candidate for this user, but it must be auditioned first because it may still sound Mandarin-like depending on the prompt/voice.
