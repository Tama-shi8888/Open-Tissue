---
name: chat-server
description: Slack/Discord等のチャットを操作するときに使う
---

# chat-server (外部サービスを操作)

## 目的
Slack/Discord等のチャットを操作するときに使う

## 手順
1. 対象チャンネルと内容を確認
2. 下書きを提示
3. 承認後に送信

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。
