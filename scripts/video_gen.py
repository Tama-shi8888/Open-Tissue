#!/usr/bin/env python3
"""動画生成: プロバイダ非依存の汎用ジョブ投入。VIDEO_API_URL(POST)とVIDEO_API_KEYを設定して使う。
リクエストは {"prompt": ...} をJSONでPOSTし、レスポンスをそのまま表示する。"""
import argparse, os
from _common import need, post_json, load_env
ap = argparse.ArgumentParser(); ap.add_argument("prompt"); a = ap.parse_args(); load_env()
url = os.environ.get("VIDEO_API_URL") or need("VIDEO_API_URL")
body, _ = post_json(url, {"prompt": a.prompt}, {"Authorization": "Bearer " + need("VIDEO_API_KEY")})
print(body.decode())
