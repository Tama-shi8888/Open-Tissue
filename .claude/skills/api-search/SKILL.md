---
name: api-search
description: Web検索・調査APIを使うときに使う
---

# api-search (外部APIを呼ぶ)

## 目的
Web検索・調査APIを使うときに使う

## 手順
1. 検索クエリを複数作成
2. 結果を出典付きで要約
3. report-writer に引き渡し

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。

## 実行コマンド
`python3 scripts/search.py "<クエリ>" -n 5`
