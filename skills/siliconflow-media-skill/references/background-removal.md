# Background Removal and Replacement

## Problem

When asked to change only the background of an image while preserving the foreground object exactly, generative image editing models (Qwen-Image-Edit, Kolors) often:
- Modify the foreground object's colors, shape, or details
- Generate a completely white/blank image
- Reinterpret the scene rather than performing surgical background replacement

## Solution: Use rembg

`rembg` is a Python library that uses the U2-Net neural network specifically trained for background removal. It preserves the foreground exactly.

### Installation (via uv)

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "rembg[cpu]>=2.0.0",
#     "pillow>=10.0.0",
# ]
# ///
```

### Usage Pattern

```python
from PIL import Image
from rembg import remove

# Open input
input_img = Image.open(input_path)

# Remove background (returns RGBA with transparency)
output_img = remove(input_img)

# Composite onto white background
white_bg = Image.new("RGB", output_img.size, (255, 255, 255))
white_bg.paste(output_img, (0, 0), output_img)

# Save
white_bg.save(output_path, "JPEG", quality=95)
```

### First Run

On first execution, rembg downloads the U2-Net model (~176MB) to `~/.u2net/u2net.onnx`. This takes 20-40 seconds depending on network speed.

### When to Use

- User asks to "change background to white" or "replace background"
- User emphasizes "keep the foreground exactly as it is"
- User complains that AI image editing changed the subject

### When NOT to Use

- User wants creative reinterpretation or style transfer
- User wants to modify both foreground and background
- Image has complex transparency or semi-transparent elements that need artistic handling

## Session Context (2026-05-02)

User provided a 200x200 lobster mascot logo and asked to change background to white. Multiple attempts with Qwen-Image-Edit and Kolors failed:
- Qwen with "change canvas background color to pure white #FFFFFF, do not modify the lobster character at all" → pure white image
- Kolors with "a lobster mascot character on pure white background, keep the lobster's original colors and details" → modified lobster

`rembg` succeeded on first try, preserving the lobster exactly while replacing background with white.
