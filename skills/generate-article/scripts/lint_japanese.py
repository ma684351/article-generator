import sys
import re
import json
from sudachipy import dictionary
from sudachipy import tokenizer

# --- AI特有の禁止語リスト ---
FORBIDDEN_WORDS = [
    r"と言えるでしょう",
    r"と言えるのではないでしょうか",
    r"について深掘り",
    r"興味深いことに",
    r"注目すべき点は",
    r"なのだ",
    r"である", # デスマスの混在チェックも兼ねる
    r"重要な役割を果た(す|し)",
    r"焦点を当て",
    r"不可欠(です|な)",
    r"結論として",
    r"まとめとして",
]

# --- 助動詞・語尾判定用の簡易リスト ---
SENTENCE_ENDINGS = [
    "です", "ます", "でした", "ました", "でしょう", "ましょう"
]

def analyze_text(text: str):
    issues = []

    # Sudachiの初期化
    try:
        tokenizer_obj = dictionary.Dictionary(dict="core").create()
    except Exception as e:
        print(f"辞書の初期化に失敗しました。要件を確認してください: {e}")
        return []

    lines = text.split('\n')

    previous_ending = None
    consecutive_ending_count = 0
    total_characters = 0

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # HTMLタグの除去 (簡単なもの)
        clean_line = re.sub(r'<[^>]+>', '', line)

        # マークダウン記法の除去 (見出し、太字、斜体、引用、リストなど)
        clean_line = re.sub(r'^(#+\s+|\*\s+|-\s+|\d+\.\s+|>\s+)', '', clean_line) # 行頭の記号
        clean_line = re.sub(r'(\*\*|__)(.*?)\1', r'\2', clean_line) # 太字
        clean_line = re.sub(r'(\*|_)(.*?)\1', r'\2', clean_line)    # 斜体
        clean_line = re.sub(r'~~(.*?)~~', r'\1', clean_line)        # 取り消し線
        clean_line = re.sub(r'`(.*?)`', r'\1', clean_line)          # インラインコード
        clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line) # リンク

        clean_line = clean_line.strip()
        if not clean_line:
            continue

        total_characters += len(clean_line.replace(" ", "").replace("　", ""))

        # 1. 一文の長さチェック (100文字超え)
        sentences = re.split(r'(?<=。)', clean_line)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(sentence) > 100:
                issues.append(f"[Line {i+1}] 長すぎる文（{len(sentence)}文字）: 読点の追加や文の分割を検討してください。 -> {sentence[:30]}...")

            # 2. 禁止語チェック
            for pattern in FORBIDDEN_WORDS:
                if re.search(pattern, sentence):
                    issues.append(f"[Line {i+1}] AI特有の表現を検出: 「{pattern}」 -> {sentence}")

            # 3. 文末表現の連続チェック (形態素解析を活用)
            mode = tokenizer.Tokenizer.SplitMode.C
            morphemes = tokenizer_obj.tokenize(sentence, mode)

            # 文末を取得
            ending = None
            if len(morphemes) > 0:
                # 最後の形態素から2つくらいを見て語尾を判断する簡易ロジック
                last_morph = morphemes[len(morphemes)-1].surface()
                if last_morph == "。" and len(morphemes) > 1:
                     start = max(0, len(morphemes) - 3)
                     end = len(morphemes) - 1
                     last_morph = "".join([morphemes[j].surface() for j in range(start, end)]) # です, ます など
                else:
                     start = max(0, len(morphemes) - 2)
                     last_morph = "".join([morphemes[j].surface() for j in range(start, len(morphemes))])

                # 簡単なマッピング
                for e in SENTENCE_ENDINGS:
                    if e in last_morph:
                        ending = e
                        break

            if ending:
                if ending == previous_ending:
                    consecutive_ending_count += 1
                else:
                    consecutive_ending_count = 1

                if consecutive_ending_count >= 3:
                     issues.append(f"[Line {i+1}] 同じ文末表現（{ending}）が3回以上連続しています。リズムを変えることを検討してください。 -> {sentence}")
                     consecutive_ending_count = 0 # リセット
                previous_ending = ending
            else:
                 previous_ending = None
                 consecutive_ending_count = 0

    # 4. 全体文字数チェック (短すぎる記事の防止)
    if total_characters < 800:
        issues.append(f"[全体] 記事の文字数が少なすぎます（現在 {total_characters} 文字）。見出しを追加し、具体例を交えてより詳しく解説し、最低でも800文字以上になるように加筆してください。")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python lint_japanese.py <input.json>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'content' not in data:
            print("Error: JSONファイルに 'content' キーが見つかりません。")
            sys.exit(1)

        article_text = data['content']

        print(f"ファイルを解析中: {file_path}")
        issues = analyze_text(article_text)

        if issues:
            print("\n🚨 以下の日本語の不自然な箇所が検出されました。AIエージェントはこれらを判断して修正してください。:\n")
            for issue in issues:
                print(f"  - {issue}")
            print("\n🚨 修正後、再度このスクリプトを実行して確認してください。")
            sys.exit(1)
        else:
            print("\n✅ 問題は見つかりませんでした。自然な日本語です。")
            sys.exit(0)

    except Exception as e:
         print(f"エラーが発生しました: {e}")
         sys.exit(1)

if __name__ == "__main__":
    main()
