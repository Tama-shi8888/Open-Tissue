#!/usr/bin/env python3
"""画像生成 (OpenAI Images API)。例: image_gen.py "青い猫のイラスト" -o assets/cat.png"""
import argparse, base64, json
from _common import need, post_json
ap = argparse.ArgumentParser(); ap.add_argument("prompt"); ap.add_argument("-o", default="assets/out.png")
ap.add_argument("--model", default="gpt-image-1"); ap.add_argument("--size", default="1024x1024")
a = ap.parse_args()
body, _ = post_json("https://api.openai.com/v1/images/generations",
    {"model": a.model, "prompt": a.prompt, "size": a.size},
    {"Authorization": "Bearer " + need("IMAGE_API_KEY")})
open(a.o, "wb").write(base64.b64decode(json.loads(body)["data"][0]["b64_json"]))
print("saved", a.o)
