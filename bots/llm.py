"""LLM呼び出し(標準ライブラリのみ)。Claude(Anthropic Messages API)とGrok(xAI, OpenAI互換)に対応。"""
import json, os, urllib.request

def _post(url, headers, payload):
    req = urllib.request.Request(url, json.dumps(payload).encode(),
        {"Content-Type": "application/json", **headers}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())

def claude(messages, system="", model=None):
    d = _post("https://api.anthropic.com/v1/messages",
        {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
        {"model": model or os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5"), "max_tokens": 1024,
         "system": system, "messages": messages})
    return d["content"][0]["text"]

def grok(messages, system="", model=None):
    msgs = ([{"role": "system", "content": system}] if system else []) + messages
    d = _post("https://api.x.ai/v1/chat/completions",
        {"Authorization": "Bearer " + os.environ["XAI_API_KEY"]},
        {"model": model or os.environ.get("GROK_MODEL", "grok-4"), "messages": msgs})
    return d["choices"][0]["message"]["content"]
