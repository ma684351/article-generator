import pytest
import os
import json
import subprocess
import tempfile

SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generate_wxr.py'))

def test_generate_wxr_success():
    data = {
        "title": "テストタイトル",
        "slug": "test-title",
        "category_name": "テスト",
        "category_slug": "test-cat",
        "content": "<p>テスト本文</p>"
    }

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f_in:
        json.dump(data, f_in)
        temp_input = f_in.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as f_out:
        temp_output = f_out.name

    try:
        result = subprocess.run(['python', SCRIPT_PATH, temp_input, temp_output], capture_output=True, text=True)
        assert result.returncode == 0

        with open(temp_output, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        assert "<title>テストタイトル</title>" in xml_content
        assert "<wp:post_name>test-title</wp:post_name>" in xml_content
        assert "<![CDATA[<p>テスト本文</p>]]>" in xml_content
        assert "nicename=\"test-cat\"" in xml_content
    finally:
        os.unlink(temp_input)
        os.unlink(temp_output)

def test_generate_wxr_missing_key():
    # title が欠けているデータ
    data = {
        "slug": "test-title",
        "category_name": "テスト",
        "category_slug": "test-cat",
        "content": "<p>テスト本文</p>"
    }

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f_in:
        json.dump(data, f_in)
        temp_input = f_in.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as f_out:
        temp_output = f_out.name

    try:
        result = subprocess.run(['python', SCRIPT_PATH, temp_input, temp_output], capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error:" in result.stdout
    finally:
        os.unlink(temp_input)
        os.unlink(temp_output)
