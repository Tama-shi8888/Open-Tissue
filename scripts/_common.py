"""共通: 環境変数/.env 読み込みとHTTPヘルパー(標準ライブラリのみ)。"""
import json, os, sys, urllib.request, urllib.error, uuid
from pathlib import Path

def load_env():
    p = Path(__file__).resolve().parent.parent / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def need(name):
    load_env()
    v = os.environ.get(name)
    if not v:
        sys.exit(f"環境変数 {name} が未設定です (.env.example 参照)")
    return v

def request(url, headers=None, data=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read(), r.headers
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}")

def post_json(url, payload, headers=None):
    h = {"Content-Type": "application/json", **(headers or {})}
    body, hd = request(url, h, json.dumps(payload).encode(), "POST")
    return body, hd

def multipart(fields, files):
    b = uuid.uuid4().hex
    out = b""
    for k, v in fields.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (name, content) in files.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode() + content + b"\r\n"
    out += f"--{b}--\r\n".encode()
    return out, f"multipart/form-data; boundary={b}"
