#!/usr/bin/env bash
# Stop: 応答完了をログ化(通知連携の差し込み口)
source "$(dirname "$0")/_lib.sh"
echo "$(date -Is) stop" >> "$LOG_DIR/session.log"
[ -x "${CLAUDE_PROJECT_DIR:-.}/scripts/notify.sh" ] && [ -n "${DISCORD_WEBHOOK_URL:-}" ] && "${CLAUDE_PROJECT_DIR:-.}/scripts/notify.sh" "Claude Code: 応答が完了しました" >/dev/null 2>&1
exit 0
