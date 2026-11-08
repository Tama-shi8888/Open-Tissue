---
name: api-video
description: 動画生成APIを使うときに使う
---

# api-video (外部APIを呼ぶ)

## 目的
動画生成APIを使うときに使う

## 手順
1. 構成とプロンプトを確認
2. 生成ジョブ投入
3. 完了を待って保存

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。

## 実行コマンド
`python3 scripts/video_gen.py "<プロンプト>"` (VIDEO_API_URL を設定)
