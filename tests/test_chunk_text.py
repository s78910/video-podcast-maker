"""Tests for generate_tts.chunk_text — TTS text chunking by sentence boundaries."""
from generate_tts import chunk_text


def test_short_text_single_chunk():
    text = "你好世界。"
    chunks = chunk_text(text, max_chars=400)
    assert len(chunks) == 1
    assert chunks[0] == "你好世界。"


def test_long_text_splits_into_multiple_chunks():
    # Build text with 10 sentences, each ~60 chars → should split when max_chars=200
    sentence = "这是一个足够长的测试句子用来验证分块逻辑的正确性和边界处理。"
    text = sentence * 10
    chunks = chunk_text(text, max_chars=200)
    assert len(chunks) > 1
    # Every chunk should be within the max (allow small slack because chunk_text appends "。" sometimes)
    for c in chunks:
        assert len(c) <= 250


def test_chinese_semicolons_normalized_to_period():
    """Chinese semicolon (；) is treated as a sentence boundary like period.

    Use sentences long enough that max_chars forces a split ONLY if ； is a
    valid split point. If ； were treated as inline punctuation the whole
    text would land in a single chunk.
    """
    # Each sentence is 15 chars, total 30+ → with max_chars=20 must split on ；
    text = "这是一个足够长的第一句话；这是一个足够长的第二句话。"
    chunks = chunk_text(text, max_chars=20)
    assert len(chunks) > 1


def test_english_sentences_split_on_period():
    text = "This is one. This is two. This is three."
    chunks = chunk_text(text, max_chars=20)
    assert len(chunks) >= 2
    # Each chunk should end with terminal punctuation
    for c in chunks:
        assert c.endswith((".", "。", "!", "?"))


def test_sentence_without_terminal_gets_period_appended():
    """A bare sentence without a period is closed with a Chinese period."""
    text = "这是一个没有句号的句子"
    chunks = chunk_text(text, max_chars=400)
    assert len(chunks) == 1
    assert chunks[0].endswith("。")


def test_empty_text_produces_no_chunks():
    assert chunk_text("", max_chars=400) == []
    assert chunk_text("   ", max_chars=400) == []


def test_existing_terminal_punctuation_preserved():
    """Sentence that already ends with ! should not get extra 。 appended."""
    text = "Amazing!"
    chunks = chunk_text(text, max_chars=400)
    assert chunks == ["Amazing!"]
