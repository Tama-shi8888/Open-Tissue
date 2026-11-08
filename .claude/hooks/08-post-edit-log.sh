#!/usr/bin/env bash
# PostToolUse: 編集ログを記録
source "$(dirname "$0")/_lib.sh"
echo "$(date -Is) $(jget tool_name) $(jget tool_input.file_path)" >> "$LOG_DIR/edits.log"
