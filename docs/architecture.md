# アーキテクチャ
```mermaid
flowchart LR
  U[KEITO] --> CC[Claude Code]
  CC --> H[ハーネス: CLAUDE.md / settings.json / hooks11本]
  CC --> S1[スキルで作る: 文書・デザイン・スライド・レポート・Web・ブログ・経理・動画・X]
  CC --> S2[外部サービスを操作: Google Workspace・チャット・Notion・決済・デザインツール]
  CC --> S3[外部APIを呼ぶ: 画像・音声・動画・検索・翻訳/OCR]
  K[(ナレッジ: Obsidian / Drive / デザインシステム / GitHub)] <--> CC
  S1 --> O[公開: Vercel / Cloudflare]
```
## hooks 一覧(11本)
01 session-start / 02 prompt-context / 03 bash-guard / 04 secret-file-guard / 05 publish-confirm / 06 post-edit-format / 07 post-secret-scan / 08 post-edit-log / 09 pre-compact / 10 stop-notify / 11 session-end

## 実装済みコンポーネント
| 図の要素 | 実装 |
|---|---|
| 外部API(画像/音声/動画/検索/翻訳・OCR) | `scripts/image_gen.py` `voice.py` `video_gen.py` `search.py` `translate.py` `ocr.py` |
| 通知 | `scripts/notify.sh`(Stop hook から Discord Webhook へ) |
| 公開(Vercel / Cloudflare) | `scripts/deploy.sh` + `deploy/`(承認後のみ。対話確認あり) |
| クロ (Discord Bot) | `bots/kuro-discord/`(Claude) |
| Grok Bot | `bots/grok-bot/`(xAI) |

## 検証状況
- 実API・Discord・Vercel/Cloudflare は認証情報が必要なため未接続(キー未設定時は明示エラーで終了)。
- hooks 03 / 05 は単体テスト済み。
