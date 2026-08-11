---
name: generate-article
description: WordPress用WXR形式の記事を自動生成するツール（`note-gen`）を実行し、指定されたタイトルや方向性に基づいてブログ記事を作成・保存するスキル。
---

# Generate Article Skill (`generate-article`)

WordPressにインポート可能な WXR (XML) 形式の記事コンテンツを自動生成するスキルです。

## コマンド概要

記事生成には `note-gen` コマンドを使用します。Nix環境または仮想環境（`.venv`）上で動作します。

### オプション
- `-t, --title <タイトル>`: （任意）記事のタイトルを指定します。
- `-d, --direction <指示・テーマ>`: （任意）記事のテーマ、トーン、ターゲット読者、構成の指定などの方向性を記述します。

※ 引数をすべて省略した場合は、完全自動で最適なテーマ・タイトル・本文が生成されます。

## 実行方法

実行時の環境に応じて、以下のいずれかの方法でコマンドを実行してください。

### 1. Nix環境経由での実行（推奨）
```bash
nix develop --extra-experimental-features "nix-command flakes" --command note-gen -t "タイトル" -d "記事の方向性"
```

### 2. Python仮想環境での実行
仮想環境が有効な場合、またはプロジェクト直下の `.venv` を使用する場合:
```bash
.venv/bin/note-gen -t "タイトル" -d "記事の方向性"
# または
python3 -m src.cli -t "タイトル" -d "記事の方向性"
```

## 使用例

### 例1: タイトルと方向性を指定して生成
```bash
nix develop --extra-experimental-features "nix-command flakes" --command note-gen -t "2026年注目のWeb開発トレンドまとめ" -d "フロントエンド・バックエンドの最新動向を初心者にも分かりやすくまとめてください。"
```

### 例2: テーマ指示のみでタイトルはAIに自動決定させる
```bash
nix develop --extra-experimental-features "nix-command flakes" --command note-gen -d "初心者向けのPythonプログラミング学習ロードマップ"
```

### 例3: 完全自動生成
```bash
nix develop --extra-experimental-features "nix-command flakes" --command note-gen
```

## 出力結果の確認

生成された記事は、プロジェクトの `output/` ディレクトリ配下に `{タイトル}.xml`（またはタイムスタンプ名）として出力・保存されます。

生成完了後、`output/` ディレクトリ内の XML ファイルが作成されたことを確認してください。
