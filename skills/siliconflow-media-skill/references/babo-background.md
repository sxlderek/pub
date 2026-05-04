# Babo Background Style

## Definition

"Babo background" is a user-defined background style for product photography and mascot images.

## Visual Characteristics

- **Style:** Soft blue gradient background with bokeh effect
- **Elements:** Blurred circles, dreamy atmosphere, abstract, clean studio backdrop
- **Color profile (RGB):**
  - Red channel: ~70-80 (mean: 76.9)
  - Green channel: ~60 (mean: 60.9)
  - Blue channel: ~180-195 (mean: 181.8)
- **Overall tone:** Blue-dominant, professional product photography background

## Usage

When the user requests an image/logo/icon "on babo background", append this style description to the generation prompt:

```
on soft blue gradient background with bokeh effect, blurred circles, dreamy atmosphere, abstract, clean studio backdrop, professional product photography background
```

## Example Prompts

### Full prompt example
```
funny cartoon lobster mascot with big eyes and silly expression, wearing sunglasses, cheerful and playful character, on soft blue gradient background with bokeh effect, blurred circles, dreamy atmosphere, abstract, clean studio backdrop, professional product photography background
```

### Keywords for generation
- bokeh
- blur
- gradient
- soft focus
- defocused
- light blue to dark blue
- abstract
- minimal
- clean studio backdrop
- professional product photography

## Reference Image

Original reference: `/opt/data/image_cache/img_ce38e503102e.jpg` (760x427px)

## Recommended Models for Babo Background

### High-Quality Image Generation Models (OmniRoute)

When generating images on babo background, these models are available:

1. **Kolors (default)** - `Kwai-Kolors/Kolors` via SiliconFlow
   - User preference: Always use Kolors by default unless specified otherwise
   - Tested successfully with babo background style

2. **NanoBanana** - High-quality image generation
   - `nanobanana/nanobanana-pro` (best quality)
   - `nanobanana/nanobanana-flash` (faster)
   - Available via OmniRoute

3. **GPT Image** - High-quality image generation
   - `openai/gpt-image-2` (latest, may hit billing limits)
   - `openai/gpt-image-1.5`
   - `pollinations/gpt-image-2` (alternative)
   - `pollinations/gptimage-large`
   - Available via OmniRoute

4. **Flux** - Fast generation
   - `pol/flux` via OmniRoute
   - Returns base64 in `b64_json` field

### Model Selection Priority

1. Use **Kolors** by default (user preference)
2. Use **Flux** if user says "use flux"
3. Use **NanoBanana** or **GPT Image** if user explicitly requests high-quality generation
4. Check OmniRoute for model availability before attempting generation

## Session Notes

- Defined in session 2026-05-02
- User requested this be saved as a reusable style
- Successfully tested with Kolors, NanoBanana Pro, and Flux models
- User explicitly stated: "always use Kolors if I didn't specify which model to use"
