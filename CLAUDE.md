# CLAUDE.md — KEITO の AI エコシステム

Claude Code を中核に、スキル・外部サービス・外部API・ナレッジを束ねる作業環境。

## 基本方針
- 日本語で簡潔に回答する。判断が必要なら推奨案を1つ示す。
- 外部への公開・送信・課金・削除は **必ず事前にユーザー確認**(hooks でも一部ブロック)。
- APIキー・秘密情報はチャットに貼らせない。`.env`(未コミット)から読む。`.env.example` 参照。
- 成果物のスタイルは `design-system/` に従う。

## 構成
| 層 | 場所 |
|---|---|
| ハーネス(判断・安全) | `CLAUDE.md` / `.claude/settings.json` / `.claude/hooks/` |
| スキル | `.claude/skills/*`(作る系 / 外部サービス系 / 外部API系) |
| ナレッジ・記憶 | `knowledge/`(Obsidian Vault として開ける) |
| デザインシステム | `design-system/` |
| 出力 | `docs/`, `assets/`(公開は Vercel / Cloudflare、承認後) |

## 記憶メモのルール
- 重要な決定・好み・再利用したい知見は `knowledge/notes/YYYY-MM-DD-題名.md` に保存。
- 未整理のメモは `knowledge/inbox/` に置き、後で整理する。
