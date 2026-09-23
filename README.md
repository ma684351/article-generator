# Natural Japanese Writer

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Ready-blue.svg)](https://agentskills.io/)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-orange.svg)](https://claude.ai/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

AIが書いた特有の「手癖」や「不自然な表現」を排除し、論旨がすっきり通る自然な日本語の執筆・推敲を支援する Agent Skill です。
議事録・調査レポート・社内ガイド・企画書・ブログ記事など、あらゆる日本語テキストの生成に対応しています。オプションとして、WordPress に直接インポート可能な **WXR（WordPress eXtended RSS 1.2 形式）XML ファイル** の生成も可能です。

**Claude Code**、**Cursor**、**Antigravity**、**Windsurf** などの主要な AI コーディングエージェントに対応しています。

単にテキストを出力するだけでなく、形態素解析（SudachiPy）による**日本語品質チェック（Lint）と自己修正ループ**を実行し、AI特有の不自然な表現を自動排除した高品質な日本語を生成します。

---

## ✨ 主な特徴

- **AI臭さを抜くLinter**: `sudachipy` を用いて「AI特有の定型句（『〜と言えるでしょう』など）」、「同じ文末の連続（『〜ます』の3連続）」、「過剰なルビ・英語併記（『漢字（ひらがな）』など）」、「1文の長さ（100文字超）」を自動検出。エージェント自身が警告を読み、自然な文章になるまで自己修正します。
- **多角的な文章チェック**: 形態素解析によるLinterに加え、見出しや段落先頭文の構成チェック (`outline.py`) 、専門用語と初出説明の確認 (`terms.py`) 、さらに高度な推敲向けに話題の平板さを検出するオプトイン機能 (`semantic.py`) を備え、総合的に文章の質を高めます。
- **あらゆる用途の日本語に対応**: レポート、議事録、ブログなど、用途を問わず読みやすい日本語を生成します。出力形式もマークダウンやプレーンテキストなど柔軟に対応。
- **WordPress への WXR エクスポート（オプション）**: オプションで、カテゴリ、スラッグ、投稿日時などを含む正式な WXR (XML) ファイルを出力できます。
- **独立した仮想環境（venv）**: スキル専用の仮想環境（`.venv`）を自律構築し、依存パッケージのバージョンを厳密に固定しているため、ホスト環境を汚しません。
- **マルチエージェント対応**: `npx skills add`（Agent Skills 規格）および Claude Code のプラグイン機能（`/plugin`）の両方に完全対応。

---

## 📁 ディレクトリ構成

```text
natural-japanese-skill/
├── skills/
│   └── natural-japanese/          # 【スキル本体】
│       ├── SKILL.md               # エージェント向け指示書・ワークフロー定義
│       ├── requirements.txt       # 実行用依存パッケージ（バージョン固定）
│       ├── requirements-dev.txt   # テスト用依存パッケージ（pytest）
│       └── scripts/
│           ├── lint.py            # 形態素解析日本語 Linter スクリプト
│           ├── outline.py         # 構成（見出し・段落先頭文）チェックスクリプト
│           ├── terms.py           # 専門用語と初出説明のチェックスクリプト
│           ├── semantic.py        # 話題の平板さの深層検出スクリプト (オプトイン)
│           ├── generate_wxr.py    # JSON → WXR XML 変換スクリプト（オプション用）
│           ├── textcore.py        # 各スクリプトの共有基盤モジュール
│           ├── calibrate.py       # 検出器の校正・分析用スクリプト (開発用)
│           └── tests/             # ユニットテスト群
│
├── .claude-plugin/                # Claude Code プラグイン定義
│   ├── marketplace.json           # マーケットプレイスカタログ
│   └── plugin.json                # プラグインマニフェスト
│
├── .github/workflows/             # GitHub Actions CI（自動テスト）
│   └── python-test.yml
├── README.md                      # 本ドキュメント
└── package.json
```

---

## 🧩 インストール方法

お使いのエージェント環境に合わせて、以下のいずれかの方法でインストールできます。

### 方法 1: `npx skills add` でインストール（推奨）

Agent Skills オープン規格に対応したツール（Cursor, Claude Code, Antigravity 等）で、ワンコマンドで追加できます：

```bash
# プロジェクト内にインストールする場合
npx skills add ma684351/natural-japanese

# Claude Code 向けにインストールする場合
npx skills add ma684351/natural-japanese --agent claude-code

# 全プロジェクトで使えるようグローバルにインストールする場合
npx skills add ma684351/natural-japanese -g --agent claude-code
```

---

### 方法 2: Claude Code のプラグインとしてインストール

公式マーケットプレイスへの登録なしで、本 GitHub リポジトリから直接 Claude Code にプラグインとしてインストール可能です：

```bash
# 1. リポジトリをマーケットプレイスとして登録（初回のみ）
/plugin marketplace add ma684351/natural-japanese

# 2. プラグインをインストール
/plugin install natural-japanese@natural-japanese-skill

# 3. 反映
/reload-plugins
```

---

### 方法 3: シンボリックリンクによる手動登録

ローカルマシン上の全プロジェクトから即座に利用できるようにする場合：

```bash
# Claude Code の場合
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/natural-japanese" ~/.claude/skills/natural-japanese

# Cursor / Antigravity の場合
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/natural-japanese" ~/.agents/skills/natural-japanese
```

---

## 🚀 使い方

スキルをインストールした後は、AI エージェントに対して日本語の作成・推敲を依頼するだけです。エージェントが自動的にスキルを認識して起動します。

### 指示（プロンプト）の例

- 「**2026年のWeb開発トレンドについて、調査レポートを書いて**」
- 「**このメモを元に、自然で読みやすい議事録を作成して**」
- 「**AIが書いた以下の文章を、もっと自然な日本語に直して**」
- 「**おすすめのメカニカルキーボードについての記事をWordPressインポート用XMLで出力して**」

### 生成される成果物

エージェントの作業完了後、ユーザーの指示に応じた結果がチャット上に表示されます。
WordPress（WXR）出力が指定された場合は、以下のファイルが生成されます：

- `draft.json`: 下書きデータ
- `output.xml`: WordPress に直接インポート可能な WXR 形式 XML ファイル

---

## ⚙️ 内部処理ワークフロー

スキルが呼び出されると、エージェントは以下のパイプラインを自律的に実行します：

```mermaid
flowchart TD
    A[ユーザーのプロンプト] --> B[下書き Markdown (draft.md) の作成]
    B --> C[仮想環境 .venv の準備 & 依存関係導入]
    C --> D[lint.py 等を実行\n形態素・構成・用語のチェック]
    D --> E{警告があるか？}
    E -- 警告あり --> F[AI自身による draft.md の自己修正]
    F --> D
    E -- 警告なし（パス） --> G{WXR出力が指定されたか？}
    G -- はい --> J[draft.json を作成]
    J --> H[generate_wxr.py を実行して output.xml 作成]
    G -- いいえ --> I[推敲された自然な日本語をテキストとして出力]
```

---

## 🧪 開発・テスト

本スキルのスクリプト（Linter および XML 生成）にはユニットテストが用意されています。

```bash
# 依存関係のインストール
pip install -r skills/natural-japanese/requirements.txt
pip install -r skills/natural-japanese/requirements-dev.txt

# テストの実行
cd skills/natural-japanese/scripts
pytest tests/
```

GitHub Actions により、プルリクエストおよび main ブランチへの push 時に自動でテストが実行されます。

---

## 📄 ライセンス

[MIT License](LICENSE)
