import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from semantic import compute_metrics, doc_sentences_with_lines


def test_semantic_compute_metrics():
    # 文数が3未満のケース
    embeddings_small = np.random.rand(2, 5)
    out_small = compute_metrics(embeddings_small)
    assert out_small["coherence_flatness_range"] is None

    # 正常ケース (3文以上)
    # 簡単のため、ダミーの類似度行列を直接計算できるような正規化ベクトルを用意
    e = np.array([
        [1.0, 0.0],
        [0.8, 0.6],
        [0.0, 1.0],
        [0.6, 0.8]
    ])

    out = compute_metrics(e)
    assert abs(out["coherence_flatness_range"] - 0.2) < 1e-6
    assert abs(out["topic_jump_min"] - 0.6) < 1e-6
    assert abs(out["semantic_repetition_max"] - 0.96) < 1e-6

def test_doc_sentences_with_lines():
    text = "# Title\n\n文1です。文2です。\n\n* 箇条書き\n\n文3。"
    sentences = doc_sentences_with_lines(text)

    texts = [s for _, s in sentences]
    assert "文1です" in texts
    assert "文2です" in texts
    assert "文3" in texts
