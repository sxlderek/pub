#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
Edit images using SiliconFlow Qwen-Image-Edit model.

Usage:
    uv run image_edit.py --input "input.jpg" --output "output.jpg" --prompt "change background to white"
    
Examples:
    uv run image_edit.py --input logo.jpg --output logo_white.jpg --prompt "replace background with pure white"
    uv run image_edit.py --input photo.jpg --output photo_clean.jpg --prompt "remove the person in the background"
"""

import argparse
import os
import sys
import base64
from pathlib import Path

import requests


SILICONFLOW_URL = "https://api.siliconflow.cn/v1/images/generations"


def get_api_key() -> str:
    key = os.environ.get("SILICONFLOW_API_KEY")
    if not key:
        print("Error: SILICONFLOW_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    return key


def edit_image(input_path: Path, output_path: Path, prompt: str, api_key: str) -> bool:
    # Read and encode image
    with open(input_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    payload = {
        "model": "Qwen/Qwen-Image-Edit",
        "prompt": prompt,
        "image": f"data:image/jpeg;base64,{image_data}",
        "image_size": "1024x1024"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"🎨 Editing image with Qwen-Image-Edit...")
    print(f"📝 Prompt: {prompt}")
    
    try:
        response = requests.post(SILICONFLOW_URL, json=payload, headers=headers, timeout=120)
        
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}", file=sys.stderr)
            return False
        
        data = response.json()
        
        if "images" in data and len(data["images"]) > 0:
            result_url = data["images"][0]["url"]
            
            print(f"📥 Downloading result...")
            img_response = requests.get(result_url, timeout=60)
            img_response.raise_for_status()
            
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            
            print(f"✅ Image saved: {output_path.resolve()}")
            print(f"MEDIA: {output_path.resolve()}")
            return True
        else:
            print(f"❌ Unexpected response: {data}", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Edit images with SiliconFlow Qwen-Image-Edit")
    parser.add_argument("--input", "-i", required=True, help="Input image path")
    parser.add_argument("--output", "-o", required=True, help="Output image path")
    parser.add_argument("--prompt", "-p", required=True, help="Edit instruction")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    api_key = get_api_key()
    
    if not edit_image(input_path, output_path, args.prompt, api_key):
        sys.exit(1)


if __name__ == "__main__":
    main()
