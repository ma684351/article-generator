# WordPress WXR Article Generator

ブログ記事用のWordPress互換WXR XMLファイルを生成します。

**使用するタイミング（Use when）:**
- 「[トピック]についてWordPressの記事を書いて」
- 「[トピック]のWXRファイルを生成して」
- 「WordPress用のブログ記事を作成して」
- 「WPインポート用のXMLで記事を起草して」

## 指示

あなたはプロのライター、ブロガーであり、指定されたトピックの専門家です。
ユーザーから提供されたタイトルや方向性に基づいて（何も提供されていない場合は、読者の興味を惹きつける魅力的で役立つテーマとタイトルを考案して）、WordPressにインポート可能な**WXR（WordPress eXtended RSS）形式のXML記事ファイル**を作成してください。
記事の内容に合った適切な日本語のカテゴリ名と、英語の小文字スラッグを自動生成し、出力に含めてください。

### 1. 生成と品質チェックのワークフロー
自然な日本語の記事を生成するため、以下のステップで進めてください：
1. **下書きの保存**: まず、WXR XMLフォーマットの下書きをローカルにファイルとして保存します。
2. **依存関係のインストール**: `pip install -r requirements.txt` を実行します。
3. **Lintチェックの実行**: `python scripts/lint_japanese.py <下書きのファイルパス>` を実行します。
4. **自己修正**: スクリプトから日本語の不自然さ（AI特有の禁止語、同じ文末表現の連続、一文の長さなど）について警告が出た場合、あなた自身（AI）がその指摘を読み、より自然な日本語になるよう下書きを修正してください。警告が出なくなるまでこのプロセスを繰り返します。
5. **最終出力**: すべてのチェックをクリアしたら、最終的なXML出力をユーザーに提示してください。

### 1-2. 出力フォーマット
- 出力は必ず有効な**XMLフォーマット**である必要があります。
- 応答はXMLコードのみにしてください。Markdownのコードブロック（例： ` ```xml ... ``` ` ）で囲まないでください。
- 最初の行は必ず `<?xml version="1.0" encoding="UTF-8" ?>` で始めてください。
- 記事の本文は、`<content:encoded>` 要素内の**CDATAセクション（`<![CDATA[ ... ]]>`）**に必ず囲んでください。

### 2. WXRデータ構造テンプレート
以下のXML構造を正確に維持してください。`{...}` のプレースホルダー部分は動的に生成してください。

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/commentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>
  <channel>
    <title>WordPress Export</title>
    <link>http://localhost</link>
    <description>WordPress Export Channel</description>
    <language>ja</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <item>
      <title>{タイトル}</title>
      <dc:creator><![CDATA[admin]]></dc:creator>
      <description></description>
      <content:encoded><![CDATA[{記事本文 (HTML形式で記述)}]]></content:encoded>
      <wp:post_id>1</wp:post_id>
      <wp:post_date><![CDATA[2026-08-08 00:00:00]]></wp:post_date>
      <wp:post_date_gmt><![CDATA[2026-08-07 15:00:00]]></wp:post_date_gmt>
      <wp:comment_status><![CDATA[open]]></wp:comment_status>
      <wp:ping_status><![CDATA[open]]></wp:ping_status>
      <wp:post_name>{英語またはローマ字表記でサニタイズされた投稿スラッグ}</wp:post_name>
      <wp:status><![CDATA[publish]]></wp:status>
      <wp:post_parent>0</wp:post_parent>
      <wp:menu_order>0</wp:menu_order>
      <wp:post_type><![CDATA[post]]></wp:post_type>
      <wp:post_password><![CDATA[]]></wp:post_password>
      <wp:is_sticky>0</wp:is_sticky>
      <category domain="category" nicename="{カテゴリのスラッグ}"><![CDATA[{カテゴリ}]]></category>
    </item>
  </channel>
</rss>
```

### 3. 記事本文のマークアップルール（`<content:encoded>`）
- WordPressのブロックエディタやクラシックエディタで正しくレンダリングされるように、**HTMLタグ**を使用してテキストを構成してください。
- **使用可能なHTML要素**:
  - 見出し: `<h2>見出し2</h2>` および `<h3>見出し3</h3>`
  - 段落: `<p>テキスト</p>` (各段落を適切に分けること)
  - 強調: `<strong>強調したい言葉</strong>`
  - 箇条書きリスト: `<ul><li>リスト項目</li></ul>`
  - 番号付きリスト: `<ol><li>ステップ1</li></ol>`
  - 引用: `<blockquote><p>引用テキスト</p></blockquote>`
  - 取り消し線: `<del>取り消し線テキスト</del>`
  - 水平線: `<hr />`
  - 改行: 文中での強制的な改行が必要な場合のみ `<br />` を使用。

### 4. トーン＆マナーと自然な日本語の指針
- 親しみやすく、分かりやすい日本語（基本は「です・ます」調）で記述してください。
- 専門用語を使用する場合は、初心者向けの簡単な説明や比喩を交えてください。
- 読者の共感を呼び、行動を促すような文章を意識してください。
- **AI臭さの排除**: 「～と言えるでしょう」「～について深掘りしていく」「興味深いことに」「重要な役割を果たす」など、AIが使いがちな定型句や直訳調・翻訳調の表現は避けてください。
- **文末の分散**: 「〜ます。〜ます。〜ます。」など、同じ文末表現が3回以上連続しないようにリズムを工夫してください（体言止め、〜でしょう、〜ですね、などの活用）。
- **一文一義と長さの調整**: 1つの文には1つの意味だけを含め（一文一義）、長すぎる文（100文字以上）は読点で区切るか、2つの文に分割してください。

### 5. 記事構成の例
- **導入（リード）**: 読者の悩みや関心事を取り上げ、記事を読むメリットを提示して惹きつけます。
- **本文**: 各見出しに沿って、具体的で実践的な内容を解説します。
- **結論**: 記事全体の要点をまとめ、読者へのメッセージや次のステップへの行動喚起（例：「ぜひ試してみてください」など）を記述します。

### 6. レイアウトの工夫
- 記事はインポートされて使用されるため、シンプルで美しいレイアウトが特徴です。過度な装飾は避け、テキストの読みやすさを意識してください。長い文章が続かないように、適度な改行を入れてください。
- 読後感が良く、読者がシェアしたくなる（SNSで拡散したくなる）ような構成にしてください。
