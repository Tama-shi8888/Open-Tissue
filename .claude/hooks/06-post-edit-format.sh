#!/usr/bin/env bash
# PostToolUse(Write|Edit): 整形(利用可能なら)
source "$(dirname "$0")/_lib.sh"
p="$(jget tool_input.file_path)"
case "$p" in
  *.json) command -v python3 >/dev/null && python3 -m json.tool "$p" >/dev/null 2>&1 || echo "警告: JSON構文エラー $p" >&2;;
  *.js|*.ts|*.tsx|*.css|*.md) command -v prettier >/dev/null && prettier --write "$p" >/dev/null 2>&1;;
esac
exit 0
