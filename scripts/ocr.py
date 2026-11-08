#!/usr/bin/env python3
"""OCR (OpenAI Vision)。例: ocr.py scan.png"""
import argparse, base64, json
from pathlib import Path
from _common import need, post_json
ap = argparse.ArgumentParser(); ap.add_argument("image"); a = ap.parse_args()
b64 = base64.b64encode(Path(a.image).read_bytes()).decode()
body, _ = post_json("https://api.openai.com/v1/chat/completions", {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": [
    {"type": "text", "text": "画像内の文字をそのまま書き起こしてください。説明は不要です。"},
    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}}]}]},
    {"Authorization": "Bearer " + need("IMAGE_API_KEY")})
print(json.loads(body)["choices"][0]["message"]["content"])
