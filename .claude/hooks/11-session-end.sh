#!/usr/bin/env bash
# SessionEnd: セッション終了ログ
source "$(dirname "$0")/_lib.sh"
echo "$(date -Is) end" >> "$LOG_DIR/session.log"
exit 0
