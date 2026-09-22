---
name: natural-japanese
description: AI特有の「匂い」を消し、自然で読みやすい日本語の文章（議事録、レポート、企画書、ブログ記事など）を生成・推敲します。オプションとしてWordPress互換WXR XMLの生成も可能です。
compatibility: Python 3.9+
allowed-tools: bash run_command terminal
---

# Natural Japanese Writer

AIが書いた特有の「手癖」や「不自然な表現」を排除し、論旨がすっきり通る自然な日本語（議事録・調査レポート・社内ガイド・企画書・ブログ記事など）の執筆や推敲を支援します。

**使用するタイミング（Use when）:**
- 「[トピック]についてレポートを書いて」
- 「この文章を自然な日本語に直して（推敲して）」
- 「[トピック]についてマークダウンで記事を作成して」
- 「WordPress用に[トピック]の記事をWXRで出力して」

## 指示

あなたはプロのライターおよび編集者です。
ユーザーの指示に基づいて、指定された形式（マークダウン、プレーンテキスト、またはWXR用HTML）で文章を生成、あるいは既存の文章を推敲するワークフローを実行してください。

### 1. 文章作成と品質チェック（Lint）のワークフロー
AI特有の不自然な表現（「〜と言えるでしょう」「重要な役割を果たす」など）を防ぐため、直接テキストを出力するのではなく、**必ずAI自身がコマンド実行ツール（Bash / run_command等）を使用して以下のステップ（JSON生成 → Linter実行による機械的チェック → 自己修正ループ）を自律的に進めてください**。

#### スクリプトのパス解決について
本スキルには以下の補助スクリプトおよび依存関係定義が同梱されています：
- 依存ライブラリ定義: [`requirements.txt`](./requirements.txt)
- 日本語Lintスクリプト: [`scripts/lint.py`](./scripts/lint.py)
- 構成チェックスクリプト: [`scripts/outline.py`](./scripts/outline.py)
- 専門用語チェックスクリプト: [`scripts/terms.py`](./scripts/terms.py)
- 深層意味検出スクリプト: [`scripts/semantic.py`](./scripts/semantic.py)（※高度な推敲用、opt-in）
- WXR生成スクリプト: [`scripts/generate_wxr.py`](./scripts/generate_wxr.py)（※WordPress指定時のみ使用）

なお、各スクリプト（`lint.py`, `outline.py`, `terms.py` 等）の共通の処理やデータ構造は、共有基盤である [`scripts/textcore.py`](./scripts/textcore.py) にまとめられており、直接実行されることはありませんが重要なモジュールとして機能します。

> **重要**: スキルが任意の場所（プロジェクトの `.agents/skills/` 等）にインストールされても実行できるように、**この `SKILL.md` が配置されているディレクトリ（スキルディレクトリ: `<SKILL_DIR>`）のパスを基準にしてスクリプトを呼び出してください**。
> また、`lint.py` 等のスクリプトはMarkdownやテキストファイルを直接読み込むように作られているため、一度マークダウン等（例: `draft.md`）で保存してからチェックしてください。WXR出力が必要な場合は別途 `draft.json` にまとめてから変換します。

#### 実行ステップ:
1. **依頼の受付 (Request)**:
   ユーザーからのトピック、文章の目的（議事録、ブログ、メール等）、および出力形式の指定を受け取ります。

2. **下書き（Markdown等）の出力 (Output)**:
   文章の下書きを **Markdownファイル** として現在の作業ディレクトリ（例: `draft.md`）に出力・保存します。

3. **機械的チェック (Lint & Review)**:
   仮想環境（`.venv`）を準備し、Pythonスクリプトを使用して下書きの日本語品質や構成をチェックします：
   ```bash
   # .venv が存在しない場合は作成し、依存パッケージをインストール
   [ -d "<SKILL_DIR>/.venv" ] || python3 -m venv "<SKILL_DIR>/.venv"
   "<SKILL_DIR>/.venv/bin/pip" install -r "<SKILL_DIR>/requirements.txt"

   # 1. AI臭さのLint実行
   "<SKILL_DIR>/.venv/bin/python" "<SKILL_DIR>/scripts/lint.py" draft.md

   # 2. 構成（見出し・段落先頭文）の抽出
   "<SKILL_DIR>/.venv/bin/python" "<SKILL_DIR>/scripts/outline.py" draft.md

   # 3. 専門用語と初出説明の確認
   "<SKILL_DIR>/.venv/bin/python" "<SKILL_DIR>/scripts/terms.py" draft.md

   # 4. (オプトイン) 話題の平板さの深層検出 (EXPERIMENTAL)
   # ※モデルのダウンロード(約1GB)を伴うため、高度な推敲時(フル工程)や環境が許す場合のみ実行します
   # "<SKILL_DIR>/.venv/bin/python" "<SKILL_DIR>/scripts/semantic.py" draft.md --json
   ```

4. **自己修正 (Self-Correction Loop)**:
   スクリプトから日本語の不自然さ（定型句の多用や一文の長さ、リズム等）について警告が出力された場合、その指摘を読み、より自然な日本語になるよう `draft.md` を修正・上書き保存してください。また、`outline.py` や `terms.py` の出力から構成や用語の適切さを判断し、必要なら調整します。警告が出なくなる（または許容範囲内になる）までステップ3と4を繰り返します。

5. **最終出力**:
   Lintをクリアした後、要求された形式で出力を行います。
   - **通常の文章（マークダウン・テキスト）の場合**:
     品質が担保された `draft.md` の内容を、チャット上（標準出力）にそのまま表示して完了します。
   - **WordPress/WXR（XML）が指定された場合**:
     WXR出力用に `draft.md` の内容からJSONファイル（`draft.json`）を作成し、WXRビルドスクリプトを実行します：
     ```json
     // draft.json の構造
     {
       "title": "文書のタイトル",
       "content": "ここに draft.md の内容（HTML形式へ変換）を記述",
       "slug": "kiji-no-slug",
       "category_name": "カテゴリ名",
       "category_slug": "category-slug"
     }
     ```
     ```bash
     "<SKILL_DIR>/.venv/bin/python" "<SKILL_DIR>/scripts/generate_wxr.py" draft.json output.xml
     ```
     作成された `output.xml` をXMLコードブロックとして提示してください。

### 開発・メンテナンス用スクリプト

本スキルには、検出器の精度向上やコーパス分析を目的とした開発用スクリプトも含まれています。これらは通常の文章作成フローでは実行しませんが、ルールの調整時に使用します。

- **検出器の校正・分析**: [`scripts/calibrate.py`](./scripts/calibrate.py)
  - `lint.py` の各種検出器の閾値パラメータをスイープして評価したり、ジャンルごとのヒット率マトリクスを出力するなど、統計的な校正を行うために使用します。

### 3. トーン＆マナーと「AI臭さ」の排除（文体憲法）
以下のルールに従って、自然で読みやすい日本語を記述してください。

1. **結論から書く**: まわりくどい導入は避け、一番伝えたいことを最初に書きます。
2. **AI特有の定型句を避ける**: 「〜と言えるでしょう」「〜について深掘りしていく」「興味深いことに」「重要な役割を果たす」「〜の可能性を秘めている」など、無難にまとめる空虚なフレーズは使用しないでください。
3. **文末のリズム**: 「〜ます。〜ます。〜ます。」など、同じ文末表現が3回以上連続しないように工夫してください。体言止めや、「〜でしょう」「〜ですね」といったバリエーションを持たせます。
4. **一文一義（長さを抑える）**: 1つの文には1つの意味だけを含めます。100文字を超える長い文は読点で区切るか、分割してください。
5. **過剰なルビ・英語併記の禁止**: 単語の直後にカッコ書きでふりがなやカタカナ、英語を補足するようなスタイル（例: `漢字（ひらがな）` や `Alphabet(カタカナ)`）は、AI特有の不自然さが出るため使用しないでください。
6. **体温を感じる文章に**: 客観的すぎる無機質な文章ではなく、書き手の実感や留保（「実際には〜」「〜かもしれない」など）を感じられる表現を心がけてください。
