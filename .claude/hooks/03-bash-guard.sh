#!/usr/bin/env bash
# PreToolUse(Bash): 破壊的コマンドをブロック
source "$(dirname "$0")/_lib.sh"
cmd="$(jget tool_input.command)"
if printf '%s' "$cmd" | grep -Eq 'rm +-rf +(/|~|\$HOME)|mkfs|dd +if=|:\(\)\{|git +push +.*--force( |$)|git +reset +--hard +origin'; then
  deny "破壊的コマンドの可能性があるためブロックしました: $cmd"
fi
