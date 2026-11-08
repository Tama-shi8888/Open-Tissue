#!/usr/bin/env bash
# SessionStart: ナレッジ索引と直近メモを読み込む
source "$(dirname "$0")/_lib.sh"
cd "${CLAUDE_PROJECT_DIR:-.}"
echo "## 本日: $(date +%F)"
echo "## ナレッジ(knowledge/notes) 直近5件:"
ls -t knowledge/notes 2>/dev/null | head -5
echo "## 未処理 inbox: $(ls knowledge/inbox 2>/dev/null | wc -l) 件"
