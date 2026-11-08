---
name: api-voice
description: 音声合成・文字起こしAPIを使うときに使う
---

# api-voice (外部APIを呼ぶ)

## 目的
音声合成・文字起こしAPIを使うときに使う

## 手順
1. 入力音声/テキストを確認
2. API実行
3. 結果をknowledgeへ保存

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。

## 実行コマンド
`python3 scripts/voice.py tts "<文>" -o assets/x.mp3` / `python3 scripts/voice.py stt <音声ファイル>`
