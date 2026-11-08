---
name: google-workspace
description: Googleカレンダー・Gmail・Drive・Docs・Sheetsを操作するときに使う
---

# google-workspace (外部サービスを操作)

## 目的
Googleカレンダー・Gmail・Drive・Docs・Sheetsを操作するときに使う

## 手順
1. 対象サービスと操作(読取/下書き/作成)を確認
2. MCP/コネクタ経由で実行
3. 送信・共有は必ず事前確認

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。
