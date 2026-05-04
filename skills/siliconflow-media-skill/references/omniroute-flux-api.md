# OmniRoute Flux API Response Format

## Session: 2026-05-02

When calling OmniRoute's `/v1/images/generations` endpoint with `model: "pol/flux"` or `pollinations/flux`, the response format differs from standard OpenAI-compatible image APIs.

## Response Structure

```json
{
  "created": 1777736388,
  "data": [
    {
      "b64_json": "<base64-encoded-image-data>"
    }
  ]
}
```

**Key difference**: The image is returned as `b64_json` (base64-encoded string), NOT as a `url` field.

## Working Code Pattern

```python
import base64
import requests

response = requests.post(
    "https://omniroute.uk.sxl.net/v1/images/generations",
    headers={"Authorization": f"Bearer {OMNIROUTE_API_KEY}"},
    json={
        "model": "pol/flux",
        "prompt": "your prompt here",
        "image": f"data:image/jpeg;base64,{input_base64}",  # optional, for img2img
        "size": "1024x1024"
    }
)

data = response.json()
if "data" in data and len(data["data"]) > 0:
    item = data["data"][0]
    if "b64_json" in item:
        img_data = base64.b64decode(item["b64_json"])
        with open("output.jpg", "wb") as f:
            f.write(img_data)
```

## Pitfall

Do NOT assume `data[0]["url"]` exists. Flux via OmniRoute returns base64-encoded data inline, not a URL to download.

## Size Output

Flux outputs at 1024x1024 by default, regardless of the input image size or the `size` parameter value.
