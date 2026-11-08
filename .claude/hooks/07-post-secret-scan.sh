#!/usr/bin/env bash
# PostToolUse(Write|Edit): APIキーらしき文字列を検知
source "$(dirname "$0")/_lib.sh"
p="$(jget tool_input.file_path)"
[ -f "$p" ] && grep -EIl 'sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|xox[bp]-[A-Za-z0-9-]+' "$p" >/dev/null \
  && deny "秘密情報らしき文字列が $p に含まれています。環境変数(.env)へ移してください。"
exit 0
