"""Tests for the PersianNormalizer module."""

import pytest

from parstoken.normalizer import PersianNormalizer


class TestPersianNormalizer:
    """Tests for PersianNormalizer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.normalizer = PersianNormalizer()
    
    def test_normalize_empty_string(self):
        """Empty string should return empty string."""
        assert self.normalizer.normalize("") == ""
    
    def test_normalize_none_like(self):
        """Empty string edge case."""
        assert self.normalizer.normalize("") == ""
    
    def test_fix_arabic_kaf(self):
        """Arabic Kaf (ك) should be converted to Persian Kaf (ک)."""
        assert self.normalizer.fix_arabic_characters("كتاب") == "کتاب"
    
    def test_fix_arabic_yeh(self):
        """Arabic Yeh (ي) should be converted to Persian Yeh (ی)."""
        assert self.normalizer.fix_arabic_characters("عربي") == "عربی"
    
    def test_fix_arabic_teh_marbuta(self):
        """Arabic Teh Marbuta (ة) should be converted to Heh (ه)."""
        assert self.normalizer.fix_arabic_characters("دانشگاة") == "دانشگاه"
    
    def test_fix_multiple_arabic_chars(self, sample_arabic_text, sample_persian_text):
        """Multiple Arabic characters should be fixed in one pass."""
        result = self.normalizer.normalize(sample_arabic_text)
        assert result == sample_persian_text
    
    def test_strip_diacritics(self):
        """Diacritical marks should be removed."""
        result = self.normalizer.strip_diacritics("سَلَام")
        assert result == "سلام"
    
    def test_strip_all_diacritics(self, sample_diacritics_text):
        """All types of diacritics should be removed."""
        result = self.normalizer.strip_diacritics(sample_diacritics_text)
        # No diacritics should remain
        diacritics = set("ًٌٍَُِّْٰٕٓٔ")
        assert not any(char in diacritics for char in result)
    
    def test_normalize_digits_to_persian(self):
        """English digits should be converted to Persian."""
        result = self.normalizer.normalize_digits("test 123", target='fa')
        assert result == "test ۱۲۳"
    
    def test_normalize_digits_to_english(self):
        """Persian digits should be converted to English."""
        result = self.normalizer.normalize_digits("تست ۱۲۳", target='en')
        assert result == "تست 123"
    
    def test_normalize_arabic_digits_to_persian(self):
        """Arabic digits should be converted to Persian."""
        result = self.normalizer.normalize_digits("٠١٢٣٤٥٦٧٨٩", target='fa')
        assert result == "۰۱۲۳۴۵۶۷۸۹"
    
    def test_invalid_digit_target(self):
        """Invalid digit target should raise ValueError."""
        with pytest.raises(ValueError):
            self.normalizer.normalize_digits("123", target='invalid')
    
    def test_fix_punctuation(self):
        """Arabic punctuation should be normalized."""
        result = self.normalizer.fix_punctuation("سلام؟ ۵۰٪")
        assert "?" in result
        assert "%" in result
    
    def test_fix_whitespace(self):
        """Multiple spaces should be collapsed."""
        result = self.normalizer.fix_whitespace("سلام    دنیا")
        assert result == "سلام دنیا"
    
    def test_fix_whitespace_newlines(self):
        """Excessive newlines should be limited to 2."""
        result = self.normalizer.fix_whitespace("سلام\n\n\n\n\nدنیا")
        assert result == "سلام\n\nدنیا"
    
    def test_fix_halfspace(self):
        """ZWNJ with surrounding spaces should be fixed."""
        text = "کتاب \u200c ها"
        result = self.normalizer.fix_halfspace(text)
        assert " \u200c " not in result
    
    def test_normalize_preserves_content(self):
        """Normalization should not remove meaningful content."""
        text = "سلام دنیا. این یک تست است!"
        result = self.normalizer.normalize(text)
        assert "سلام" in result
        assert "دنیا" in result
        assert "تست" in result
    
    def test_custom_config(self):
        """Custom configuration should be respected."""
        normalizer = PersianNormalizer(
            remove_diacritics=False,
            fix_arabic_chars=False,
        )
        text = "كتاب سَلام"
        result = normalizer.normalize(text)
        # Arabic char should remain since fix_arabic_chars=False
        assert "ك" in result
        # Diacritics should remain since remove_diacritics=False
        assert "َ" in result
    
    def test_unicode_normalization(self):
        """Unicode NFC normalization should be applied."""
        # Test that the method runs without error
        result = self.normalizer.apply_unicode_normalization("تست")
        assert result == "تست"
    
    def test_special_spaces_normalized(self):
        """Special Unicode space characters should be normalized."""
        text = "سلام\u00A0دنیا"  # Non-breaking space
        result = self.normalizer.fix_whitespace(text)
        assert "\u00A0" not in result
        assert "سلام دنیا" == result
