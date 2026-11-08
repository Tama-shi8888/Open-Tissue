#!/usr/bin/env bash
# 共通ヘルパー: stdin の JSON を読み、キーを取り出す
INPUT="$(cat)"
jget() { printf '%s' "$INPUT" | python3 -c 'import sys,json
d=json.load(sys.stdin)
for k in sys.argv[1].split("."):
    d=d.get(k,"") if isinstance(d,dict) else ""
print(d if isinstance(d,str) else json.dumps(d))' "$1" 2>/dev/null; }
deny() { echo "$1" >&2; exit 2; }   # exit 2 = ツール実行をブロックし理由をClaudeへ返す
LOG_DIR="${CLAUDE_PROJECT_DIR:-.}/logs"; mkdir -p "$LOG_DIR"
