# Pollinations session notes: aspect ratio and safety

## Observed behavior
- `scripts/image.sh` accepts `--aspect-ratio`, but the script still logs the default `Size: 1024x1024` because it does not translate aspect ratio into width/height.
- A request using `--aspect-ratio 4:3` completed successfully, but the saved file metadata was tiny (`672` bytes) compared to a normal image, so output should be verified before assuming the aspect ratio was honored.

## Practical guidance
- If a specific aspect ratio matters, prefer explicit `--width` and `--height` when the target ratio is known, or inspect the generated file before returning it.
- Do not rely solely on the script's printed size line when `--aspect-ratio` is used.

## Safety note
- The assistant should still refuse explicit nudity/sexual content requests even when the underlying image model is described as uncensored.
- Safe substitutes that work well: bikini/swimwear, fashion, pin-up style, beach/pool scenes, stylized portraits.
