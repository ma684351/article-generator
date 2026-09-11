import pytest
import os
import sys

# scripts ディレクトリをパスに追加してモジュールをインポート可能にする
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lint_japanese import analyze_text

def test_analyze_text_too_short():
    # 800文字未満のテスト
    text = "これは短いテスト記事です。最低文字数に達していません。"
    issues = analyze_text(text, min_length=800)

    assert len(issues) >= 1
    assert any("記事の文字数が少なすぎます" in issue for issue in issues)

def test_analyze_text_forbidden_words():
    # 長さはクリアさせるためのダミーテキスト
    padding = "あ" * 800
    text = f"これはテストです。{padding} この点について深掘りしていきましょう。重要な役割を果たす。"
    issues = analyze_text(text)

    # 2つの禁止語が引っかかるはず
    assert any("について深掘り" in issue for issue in issues)
    assert any("重要な役割を果た" in issue for issue in issues)

def test_analyze_text_consecutive_endings():
    padding = "あ" * 800
    text = f"これはテストです。{padding} 良いです。素晴らしいです。最高です。"
    issues = analyze_text(text)

    assert any("同じ文末表現" in issue for issue in issues)

def test_analyze_text_natural():
    # 800文字以上にするための多様な文末表現のダミーテキスト
    sentences = [
        "この文章は非常に自然な日本語で書かれています。",
        "多様な表現を用いることが重要ですね。",
        "同じ文末が続かないように工夫する必要があります。"
    ]
    padding = "".join(sentences * 12)  # (22+18+24)*12 = 64*12 = 768文字
    text = f"はじめに、テストを行います。{padding} 次に、別の表現を試してみましょう。これで終了となります。それから、さらに文字数を稼ぐための文章を追加しておこう。"
    issues = analyze_text(text)

    assert len(issues) == 0, f"エラーがないはずですが、以下の警告が出ました: {issues}"
