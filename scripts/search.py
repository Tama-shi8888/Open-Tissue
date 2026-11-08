#!/usr/bin/env python3
"""Web検索 (Brave Search API)。例: search.py "Claude Code hooks" -n 5"""
import argparse, json, urllib.parse
from _common import need, request
ap = argparse.ArgumentParser(); ap.add_argument("query"); ap.add_argument("-n", type=int, default=5)
a = ap.parse_args()
body, _ = request("https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode({"q": a.query, "count": a.n}),
    {"X-Subscription-Token": need("SEARCH_API_KEY"), "Accept": "application/json"})
for r in json.loads(body).get("web", {}).get("results", []):
    print(f"- {r['title']}\n  {r['url']}\n  {r.get('description','')}")
