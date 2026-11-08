#!/usr/bin/env python3
"""翻訳 (DeepL API)。例: translate.py "Hello" --to JA"""
import argparse, json, urllib.parse
from _common import need, request
ap = argparse.ArgumentParser(); ap.add_argument("text"); ap.add_argument("--to", default="JA")
a = ap.parse_args(); key = need("TRANSLATE_API_KEY")
host = "api-free.deepl.com" if key.endswith(":fx") else "api.deepl.com"
body, _ = request(f"https://{host}/v2/translate", {"Authorization": "DeepL-Auth-Key " + key,
    "Content-Type": "application/x-www-form-urlencoded"},
    urllib.parse.urlencode({"text": a.text, "target_lang": a.to}).encode(), "POST")
print(json.loads(body)["translations"][0]["text"])
