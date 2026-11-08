#!/usr/bin/env bash
# 公開: deploy.sh vercel|cloudflare <dir>   ※必ずユーザー承認後に実行すること
set -euo pipefail
[ -f "$(dirname "$0")/../.env" ] && set -a && . "$(dirname "$0")/../.env" && set +a
target="${1:?vercel|cloudflare}"; dir="${2:?公開ディレクトリ}"
read -r -p "本当に $target へ公開しますか? (yes/no) " ans; [ "$ans" = yes ] || exit 1
case "$target" in
  vercel) npx vercel deploy "$dir" --prod --token "${VERCEL_TOKEN:?}";;
  cloudflare) npx wrangler pages deploy "$dir" --project-name open-tissue-site;;
  *) echo "unknown target"; exit 1;;
esac
