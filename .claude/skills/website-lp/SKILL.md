---
name: website-lp
description: Webサイトやランディングページを作るときに使う
---

# website-lp (スキルで作る/Webサイト・LP)

## 目的
Webサイトやランディングページを作るときに使う

## 手順
1. 目的・CTAを定義
2. 静的HTML/CSSで実装
3. 表示確認後、公開は確認を取りVercel/Cloudflareへ

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。

## 実行コマンド
公開: `scripts/deploy.sh` に vercel か cloudflare と公開ディレクトリを渡す(承認後・対話確認あり。設定は deploy/)
