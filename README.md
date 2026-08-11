# Antigravity SDK WordPress WXR Article Generator

Antigravity SDK (`google-antigravity`) を用いた WordPress 用記事（WXR XML形式）自動生成ツールです。
Nix を用いた開発環境（Flakes 推奨）と自動仮想環境構築が組み込まれています。

## ディレクトリ構成

```
wxr-article-generator/
├── flake.nix                  # Nix Flakes環境定義
├── shell.nix                  # 従来型Nix（direnv用）サポート
├── config/
│   └── system_prompt.md       # WordPress記事執筆用のシステムプロンプト
├── output/                    # 生成された記事（WXR XML）の出力先
├── src/
│   ├── __init__.py
│   ├── cli.py                 # CLIエントリーポイント
│   └── generator.py           # 記事生成ロジック
├── pyproject.toml             # Python依存関係定義（uv / pip互換）
└── README.md
```

## 使用方法

### 1. APIキーの設定

本ツールを利用するには、Gemini APIキーが必要です。

プロジェクトのルートディレクトリに `.env` ファイルを作成し、APIキーを設定してください（`.env.example` をコピーして利用できます）。

```bash
cp .env.example .env
```

`.env` ファイルを開き、以下のように取得したAPIキーを入力します。

```env
GEMINI_API_KEY="あなたのAPIキー"
```

これにより、ツール起動時に自動的にAPIキーが読み込まれます。

### 2. 開発環境の起動

#### Nix Flakes を使用する場合（推奨）
```bash
nix develop --extra-experimental-features "nix-command flakes"
```

※ もしエラーが出る場合は、Nix の実験的機能を有効にするため上記のコマンドを実行するか、`~/.config/nix/nix.conf` に `experimental-features = nix-command flakes` を追記してください。

#### 従来の nix-shell を使用する場合
```bash
nix-shell
```

※ 初回起動時にシェルに入ると、自動的に `.venv` が作成され、`pyproject.toml` に定義された Python 依存関係（`google-antigravity`）がインストールされます。

---

### 3. 記事の生成

環境に入った後は、`pyproject.toml` で定義された `note-gen` コマンドが直接使用可能です。

#### タイトルを指定して生成する場合
`-t` または `--title` オプションでタイトルを指定できます。

```bash
note-gen -t "2026年注目のWeb開発トレンドまとめ"
```

#### 方向性・テーマのみ指定する場合
`-d` または `--direction` オプションを使うことで、記事のテーマ、ターゲット、トーンなどを指定できます（タイトルはAIが自動決定します）。

```bash
note-gen -d "初心者向けのPythonプログラミング学習ロードマップ"
```

#### タイトルと方向性の両方を指定する場合
```bash
note-gen -t "PythonとTypeScriptの選び方" -d "初心者向けに分かりやすく解説し、それぞれの特徴に焦点を当ててください。"
```

#### 完全自動で生成する場合（引数なし）
すべての引数を省略すると、AIが読者の興味を惹くテーマ・タイトル・構成を完全に自動で考案して生成します。

```bash
note-gen
```

生成された記事は、`output/` ディレクトリ配下に `{タイトル}.xml` という名前で保存されます。

---

### 4. 環境に入らず直接1行で実行したい場合

`nix develop` のコマンド指定実行を使うことで、Nix環境の起動からコマンド実行までを1行で完了できます。

```bash
nix develop --extra-experimental-features "nix-command flakes" --command note-gen -t "2026年注目のWeb開発トレンドまとめ"
```
