---
name: design-tools
description: Figma/Canvaなどのデザインツールを操作するときに使う
---

# design-tools (外部サービスを操作)

## 目的
Figma/Canvaなどのデザインツールを操作するときに使う

## 手順
1. ファイル特定
2. design-system と整合確認
3. 変更案を提示してから適用

## 注意
- 外部への公開・送信は実行前にユーザーへ確認する。
- APIキーは環境変数(.env.example 参照)から読み、出力に含めない。
- 完成物は docs/ または knowledge/notes/ に保存し、必要ならナレッジへ要点を追記する。
