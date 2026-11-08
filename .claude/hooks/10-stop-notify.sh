#!/usr/bin/env bash
# Stop: 応答完了をログ化(通知連携の差し込み口)
source "$(dirname "$0")/_lib.sh"
echo "$(date -Is) stop" >> "$LOG_DIR/session.log"
# 通知例: [ -n "$DISCORD_WEBHOOK_URL" ] && curl -s -d "content=Claude Code 完了" "$DISCORD_WEBHOOK_URL"
exit 0
