#!/usr/bin/env bash
# PreToolUse(Bash): 公開・デプロイ系は事前確認を要求
source "$(dirname "$0")/_lib.sh"
cmd="$(jget tool_input.command)"
if printf '%s' "$cmd" | grep -Eq 'vercel +(deploy|--prod)|wrangler +(deploy|pages +deploy)|npm +publish'; then
  deny "外部公開コマンドです。ユーザーの明示承認を得てから再実行してください: $cmd"
fi
