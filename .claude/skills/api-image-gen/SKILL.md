---
name: api-image-gen
description: 画像生成APIを呼ぶときに使う
---

# api-image-gen (外部APIを呼ぶ)

## 目的
画像生成APIを呼ぶときに使う

## 手順
1. プロンプトを作成
2. IMAGE_API_KEY を環境変数から読み呼び出し
3. 結果を assets/ に保存

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。
