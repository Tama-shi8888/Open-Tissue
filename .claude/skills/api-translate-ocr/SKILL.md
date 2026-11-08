---
name: api-translate-ocr
description: 翻訳・OCRなど変換系APIを使うときに使う
---

# api-translate-ocr (外部APIを呼ぶ)

## 目的
翻訳・OCRなど変換系APIを使うときに使う

## 手順
1. 入力を確認
2. API実行
3. 原文と訳文/抽出結果を併記

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。

## 実行コマンド
`python3 scripts/translate.py "<文>" --to JA` / `python3 scripts/ocr.py <画像>`
