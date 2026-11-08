#!/usr/bin/env bash
# PreCompact: 圧縮前に作業メモを退避
source "$(dirname "$0")/_lib.sh"
echo "$(date -Is) compact" >> "$LOG_DIR/session.log"
echo "圧縮前: 重要な決定事項は knowledge/notes/ に保存してください。"
