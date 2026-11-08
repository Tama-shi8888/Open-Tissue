#!/usr/bin/env bash
# PreToolUse(Write|Edit): .env/鍵ファイルの書き換えをブロック
source "$(dirname "$0")/_lib.sh"
p="$(jget tool_input.file_path)"
case "$p" in
  *.env|*.env.*|*.pem|*id_rsa*|*credentials*) [[ "$p" == *.env.example ]] || deny "秘密情報ファイルは編集禁止です: $p";;
esac
