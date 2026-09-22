import sys
from pathlib import Path

# scripts/ ディレクトリを sys.path に追加してモジュールをインポートできるようにする
sys.path.insert(0, str(Path(__file__).parent.parent))

from textcore import (
    Finding,
    iter_lines_with_no,
    iter_paragraphs_with_lines,
    mask_html_comments,
    mask_markdown_structure,
    split_sentences_with_lines,
)


def test_mask_html_comments():
    text = "Hello <!-- world -->"
    masked = mask_html_comments(text)
    assert masked == "Hello               "

    multiline = "Line 1 <!-- comment\nstill comment -->\nLine 3"
    masked_multi = mask_html_comments(multiline)
    expected = "Line 1             \n                 \nLine 3"
    assert masked_multi == expected

def test_mask_markdown_structure():
    text = "# Heading 1\n\nParagraph text.\n\n* List item\n* Another item\n\n> Blockquote\n\n```python\nprint('hello')\n```\n\nEnd text."
    masked = mask_markdown_structure(text)

    lines = masked.split('\n')
    assert lines[0] == "" # Heading masked
    assert lines[2] == "Paragraph text."
    assert lines[4] == "" # List item masked
    assert lines[5] == "" # List item masked
    assert lines[7] == "" # Blockquote masked
    assert lines[9] == "" # Code block boundary masked
    assert lines[10] == "" # Code block content masked
    assert lines[11] == "" # Code block boundary masked
    assert lines[13] == "End text."

def test_mask_markdown_inline_code_and_links():
    text = "Here is `inline code` and a [link](https://example.com)."
    masked = mask_markdown_structure(text)
    assert masked == "Here is               and a [link](                   )."

def test_iter_lines_with_no():
    text = "Line 1\nLine 2\nLine 3"
    lines = iter_lines_with_no(text)
    assert lines == [(1, "Line 1"), (2, "Line 2"), (3, "Line 3")]

def test_iter_paragraphs_with_lines():
    text = "P1 Line 1\nP1 Line 2\n\nP2 Line 1\n\n\n"
    lines = iter_lines_with_no(text)
    paragraphs = iter_paragraphs_with_lines(lines)
    assert len(paragraphs) == 2
    assert paragraphs[0] == [(1, "P1 Line 1"), (2, "P1 Line 2")]
    assert paragraphs[1] == [(4, "P2 Line 1")]

def test_split_sentences_with_lines():
    text = "これは文1です。これは文2です！文3です？文4\n文5"
    lines = iter_lines_with_no(text)
    sentences = split_sentences_with_lines(lines)
    assert len(sentences) == 5
    assert sentences[0] == (1, "これは文1です", "これは文1です")
    assert sentences[1] == (1, "これは文2です", "これは文2です")
    assert sentences[2] == (1, "文3です", "文3です")
    assert sentences[3] == (1, "文4", "文4")
    assert sentences[4] == (2, "文5", "文5")

def test_finding_to_dict():
    f = Finding(line=10, category="test", excerpt="abc", severity="warn", detail="msg", related_lines=[2, 1, 2])
    d = f.to_dict()
    assert d["line"] == 10
    assert d["category"] == "test"
    assert d["related_lines"] == [1, 2] # sorted and unique
    assert "status" not in d
