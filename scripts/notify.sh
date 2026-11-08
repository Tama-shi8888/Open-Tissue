#!/usr/bin/env bash
# Discord Webhook 通知: notify.sh "メッセージ"
set -euo pipefail
[ -f "$(dirname "$0")/../.env" ] && set -a && . "$(dirname "$0")/../.env" && set +a
: "${DISCORD_WEBHOOK_URL:?DISCORD_WEBHOOK_URL 未設定}"
python3 - "$1" <<'PY' | curl -sS -H 'Content-Type: application/json' -d @- "$DISCORD_WEBHOOK_URL"
import json,sys; print(json.dumps({"content": sys.argv[1]}))
PY
