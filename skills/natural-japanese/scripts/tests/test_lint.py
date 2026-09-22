import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lint import (
    _finding_identity_key,
    compute_baseline_diff,
    detect_antithesis_repetition,
    detect_forbidden_phrases,
    detect_translationese,
    run_lint,
    validate_baseline_data,
)
from textcore import Finding


def test_detect_forbidden_phrases():
    lines = [
        (1, "これは非常に重要と言えるでしょう。"),
        (2, "個人差がありますが、結論としていかがでしたか。"),
        (3, "普通の文章です。")
    ]
    raw_lines_by_no = {1: "これは非常に重要と言えるでしょう。", 2: "個人差がありますが、結論としていかがでしたか。", 3: "普通の文章です。"}
    findings = detect_forbidden_phrases(lines, raw_lines_by_no)

    categories = [f.category for f in findings]
    assert "forbidden_phrase" in categories
    assert len(findings) > 0

def test_detect_translationese():
    lines = [
        (1, "処理をすることが可能になるでしょう。"),
        (2, "普通の文章です。")
    ]
    raw_lines_by_no = {1: "処理をすることが可能になるでしょう。", 2: "普通の文章です。"}
    findings = detect_translationese(lines, raw_lines_by_no)

    categories = [f.category for f in findings]
    assert "translationese" in categories
    assert len(findings) == 1

def test_detect_antithesis_repetition():
    lines = [
        (1, "Aではなく、Bである。"),
        (2, "CだけでなくDも必要。"),
        (3, "Eではなく、Fである。"),
        (4, "普通の文章。")
    ]
    raw_lines_by_no = {no: text for no, text in lines}

    # 閾値を2にしてテスト
    findings = detect_antithesis_repetition(lines, raw_lines_by_no, threshold=2)
    assert len(findings) == 3
    assert all(f.category == "antithesis_repetition" for f in findings)

def test_finding_identity_key():
    key = _finding_identity_key("forbidden_phrase", "  Hello \t World  ")
    assert key == ("forbidden_phrase", "HelloWorld")

    key2 = _finding_identity_key("low_burstiness", "burstiness=-0.62")
    assert key2 == ("low_burstiness", "")

def test_baseline_logic():
    old_findings = [
        {"category": "forbidden_phrase", "excerpt": "テスト1"},
        {"category": "translationese", "excerpt": "テスト2"},
    ]
    baseline_data = {"findings": old_findings}
    valid_data, warnings = validate_baseline_data(baseline_data)
    assert not warnings

    new_findings = [
        Finding(line=10, category="forbidden_phrase", excerpt="テスト1", severity="warn"),
        Finding(line=11, category="antithesis_repetition", excerpt="テスト3", severity="warn"),
    ]

    resolved, summary = compute_baseline_diff(new_findings, valid_data)

    assert summary["resolved"] == 1
    assert summary["new"] == 1
    assert summary["persisting"] == 1

    assert new_findings[0].status == "persisting"
    assert new_findings[1].status == "new"

    assert len(resolved) == 1
    assert resolved[0]["category"] == "translationese"

def test_run_lint_integration():
    raw_text = "# 見出し\n\nこれは非常に重要と言えるでしょう。また、処理をすることが可能です。\n"
    findings, stats = run_lint(raw_text)

    assert stats["total_findings"] == len(findings)
    assert any(f.category == "forbidden_phrase" for f in findings)
    assert any(f.category == "translationese" for f in findings)
