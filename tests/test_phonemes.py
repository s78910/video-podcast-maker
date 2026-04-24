"""Tests for tts.phonemes — inline phoneme extraction and SAPI pinyin conversion."""
from tts.phonemes import extract_inline_phonemes, pinyin_to_sapi


# ---------- extract_inline_phonemes ----------


def test_extract_single_marker():
    """Inline marker is extracted; brackets disappear from clean text.

    KNOWN LIMITATION: the regex greedily captures ALL Chinese characters
    immediately preceding the `[` — so "每个执行器[zhí xíng qì]" yields key
    "每个执行器", not just "执行器". Downstream SSML will wrap the extra
    prefix in the phoneme tag, which TTS may mispronounce. The test below
    locks in current behavior so a future fix is a deliberate change.
    """
    text = "每个执行器[zhí xíng qì]都有自己的窗口"
    clean, phonemes = extract_inline_phonemes(text)
    assert clean == "每个执行器都有自己的窗口"
    assert phonemes == {"每个执行器": "zhí xíng qì"}  # current (greedy) behavior


def test_extract_single_marker_tight():
    """When the annotated word is preceded by punctuation, the key is clean."""
    text = "上下文，执行器[zhí xíng qì]处理请求"
    clean, phonemes = extract_inline_phonemes(text)
    assert phonemes == {"执行器": "zhí xíng qì"}


def test_extract_multiple_markers():
    """Multi-marker extraction — also subject to the greedy-prefix limitation.

    In "执行器[...]和重做[...]" the second marker captures "和重做" because the
    Chinese run is unbroken. See test_extract_single_marker for context.
    """
    text = "执行器[zhí xíng qì]和重做[chóng zuò]都很常用"
    clean, phonemes = extract_inline_phonemes(text)
    assert "[" not in clean
    assert phonemes == {"执行器": "zhí xíng qì", "和重做": "chóng zuò"}


def test_extract_no_markers():
    text = "纯中文文本没有注音"
    clean, phonemes = extract_inline_phonemes(text)
    assert clean == text
    assert phonemes == {}


def test_extract_ignores_non_chinese_brackets():
    """[something] after ASCII should NOT be extracted as a phoneme."""
    text = "see file [abc] for details"
    clean, phonemes = extract_inline_phonemes(text)
    assert phonemes == {}
    assert clean == text


# ---------- pinyin_to_sapi ----------


def test_sapi_basic():
    assert pinyin_to_sapi("zhí xíng qì") == "zhi 2 xing 2 qi 4"


def test_sapi_neutral_tone():
    """Syllable with no tone mark uses tone 5 (neutral)."""
    assert pinyin_to_sapi("de") == "de 5"


def test_sapi_all_tones():
    # ā=1, á=2, ǎ=3, à=4, a=5
    assert pinyin_to_sapi("mā má mǎ mà ma") == "ma 1 ma 2 ma 3 ma 4 ma 5"


def test_sapi_u_umlaut_maps_to_v():
    """ü and ǘ etc. map to 'v' in SAPI format."""
    result = pinyin_to_sapi("nǚ")
    assert result == "nv 3"


def test_sapi_mixed_syllables():
    assert pinyin_to_sapi("chóng zuò") == "chong 2 zuo 4"
