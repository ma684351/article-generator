import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from outline import (
    _heading_level_and_text,
    _is_nominal_ending,
    _match_structural_pattern,
    _match_template_word,
    build_heading_stats,
    build_outline,
)


def test_heading_level_and_text():
    level, text = _heading_level_and_text("# Heading")
    assert level == 1
    assert text == "Heading"

    level2, text2 = _heading_level_and_text("###  Subheading  ")
    assert level2 == 3
    assert text2 == "Subheading"

def test_is_nominal_ending():
    assert _is_nominal_ending("テストの見出し") is True
    assert _is_nominal_ending("テストを実行する") is False
    assert _is_nominal_ending("システムの設計") is True

def test_match_template_word():
    assert _match_template_word("はじめに") == "はじめに"
    assert _match_template_word("1. はじめに") == "はじめに"
    assert _match_template_word("まとめ") == "まとめ"
    assert _match_template_word("おわりに") == "おわりに"
    assert _match_template_word("普通の見出し") is None

def test_match_structural_pattern():
    assert _match_structural_pattern("1. 導入") == "numbered"
    assert _match_structural_pattern("【補足】") == "bracketed"
    assert _match_structural_pattern("APIとは？") == "towa"
    assert _match_structural_pattern("通常の見出し") is None

def test_build_outline():
    text = """
# 見出し1
段落1の1文目。段落1の2文目。

段落2の1文目！段落2の2文目。

* 箇条書き1
* 箇条書き2

## 見出し2
段落3。
"""
    outline = build_outline(text)

    assert outline[0]["kind"] == "heading"
    assert outline[0]["level"] == 1
    assert outline[0]["text"] == "見出し1"

    assert outline[1]["kind"] == "lead"
    assert outline[1]["text"] == "段落1の1文目。"

    assert outline[2]["kind"] == "lead"
    assert outline[2]["text"] == "段落2の1文目！"

    assert outline[3]["kind"] == "bullets"
    assert "箇条書き 2 項目" in outline[3]["text"]

    assert outline[4]["kind"] == "heading"
    assert outline[4]["level"] == 2
    assert outline[4]["text"] == "見出し2"

    assert outline[5]["kind"] == "lead"
    assert outline[5]["text"] == "段落3。"

def test_build_heading_stats():
    outline = [
        {"kind": "heading", "level": 1, "text": "はじめに", "line": 1},
        {"kind": "lead", "text": "...", "line": 2},
        {"kind": "heading", "level": 2, "text": "システムの設計", "line": 3},
        {"kind": "heading", "level": 2, "text": "システムの構築", "line": 4},
        {"kind": "heading", "level": 2, "text": "まとめ", "line": 5},
    ]

    stats = build_heading_stats(outline)

    assert stats["total_headings"] == 4
    assert stats["level_distribution"]["1"] == 1
    assert stats["level_distribution"]["2"] == 3

    h2_stats = stats["by_level"]["2"]
    assert h2_stats["count"] == 3

    assert any(h["matched"] == "まとめ" for h in h2_stats["template_hits"])
