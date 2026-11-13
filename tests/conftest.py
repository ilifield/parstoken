"""Shared test fixtures for Parstoken test suite."""

import pytest


@pytest.fixture
def sample_arabic_text():
    """Sample text with Arabic characters that should be converted to Persian."""
    return "اين يك متن فارسي است كه با كاراكترهاي عربي نوشته شده"


@pytest.fixture
def sample_persian_text():
    """Properly normalized Persian text."""
    return "این یک متن فارسی است که با کاراکترهای عربی نوشته شده"


@pytest.fixture
def sample_diacritics_text():
    """Text with Arabic diacritical marks."""
    return "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"


@pytest.fixture
def sample_html_text():
    """Text with HTML markup."""
    return "<p>سلام <b>دنیا</b></p><br/><a href='#'>لینک</a>"


@pytest.fixture
def sample_messy_text():
    """Text with various issues for full pipeline testing."""
    return (
        "سلاااام!!!   اين يك    تست است...\n\n\n\n"
        "https://example.com @user #تست\n"
        "<b>متن</b> test@email.com 😊"
    )


@pytest.fixture
def sample_zwnj_text():
    """Text with ZWNJ (half-space) characters."""
    return "کتاب\u200cها و کتاب\u200cهای خوب"
