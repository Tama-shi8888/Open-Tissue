# Open-Tissue — KEITO の AI エコシステム

Claude Code を中核とする個人AI環境の設定一式です。構成は `docs/architecture.md`、運用ルールは `CLAUDE.md` を参照。

- `.claude/settings.json` 権限と hooks 登録
- `.claude/hooks/` 安全・品質・ログ用フック 11 本
- `.claude/skills/` 19 スキル(作る系 9 / 外部サービス 5 / 外部API 5)
- `knowledge/` ナレッジ(Obsidian Vault)
- `design-system/` デザイントークン

## 使い方
1. `cp .env.example .env` してキーを設定
2. Claude Code をこのディレクトリで起動
