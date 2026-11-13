"""Tests for the TextCleaner module."""

import pytest

from parstoken.cleaner import TextCleaner


class TestTextCleaner:
    """Tests for TextCleaner."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cleaner = TextCleaner()
    
    def test_clean_empty_string(self):
        """Empty string should return empty string."""
        assert self.cleaner.clean("") == ""
    
    def test_strip_html(self):
        """HTML tags should be removed."""
        result = self.cleaner.strip_html("<p>سلام <b>دنیا</b></p>")
        assert result == "سلام دنیا"
        assert "<" not in result
        assert ">" not in result
    
    def test_strip_html_with_attributes(self):
        """HTML tags with attributes should be removed."""
        result = self.cleaner.strip_html('<a href="https://example.com">لینک</a>')
        assert result == "لینک"
    
    def test_strip_urls(self):
        """URLs should be removed."""
        result = self.cleaner.strip_urls("برو به https://example.com/path?q=1 اینجا")
        assert "https://" not in result
        assert "example.com" not in result
    
    def test_strip_emails(self):
        """Email addresses should be removed."""
        result = self.cleaner.strip_emails("ایمیل: test@example.com است")
        assert "test@example.com" not in result
        assert "@" not in result
    
    def test_strip_emojis(self):
        """Emojis should be removed when enabled."""
        cleaner = TextCleaner(remove_emojis=True)
        result = cleaner.clean("سلام 😊🎉 دنیا")
        assert "😊" not in result
        assert "🎉" not in result
        assert "سلام" in result
    
    def test_emojis_preserved_by_default(self):
        """Emojis should be preserved by default."""
        result = self.cleaner.clean("سلام 😊")
        assert "😊" in result
    
    def test_strip_hashtags(self):
        """Hashtags should be removed when enabled."""
        cleaner = TextCleaner(remove_hashtags=True)
        result = cleaner.clean("سلام #پایتون #برنامه_نویسی")
        assert "#پایتون" not in result
        assert "#برنامه_نویسی" not in result
    
    def test_hashtags_preserved_by_default(self):
        """Hashtags should be preserved by default."""
        result = self.cleaner.clean("سلام #پایتون")
        assert "#پایتون" in result
    
    def test_strip_mentions(self):
        """@mentions should be removed when enabled."""
        cleaner = TextCleaner(remove_mentions=True)
        result = cleaner.clean("سلام @user123 خوبی؟")
        assert "@user123" not in result
    
    def test_strip_phone_numbers(self):
        """Phone numbers should be removed when enabled."""
        cleaner = TextCleaner(remove_phone_numbers=True)
        result = cleaner.clean("تماس: 09123456789 یا 02112345678")
        assert "09123456789" not in result
    
    def test_strip_phone_with_country_code(self):
        """Phone numbers with +98 should be removed."""
        cleaner = TextCleaner(remove_phone_numbers=True)
        result = cleaner.clean("شماره: +989123456789")
        assert "+989123456789" not in result
    
    def test_full_clean(self, sample_html_text):
        """Full clean should remove HTML tags."""
        result = self.cleaner.clean(sample_html_text)
        assert "<" not in result
        assert ">" not in result
        assert "سلام" in result
    
    def test_clean_with_all_options(self, sample_messy_text):
        """Clean with all options enabled should remove everything."""
        cleaner = TextCleaner(
            remove_html=True,
            remove_urls=True,
            remove_emails=True,
            remove_emojis=True,
            remove_hashtags=True,
            remove_mentions=True,
            remove_phone_numbers=True,
        )
        result = cleaner.clean(sample_messy_text)
        assert "https://" not in result
        assert "@" not in result
        assert "#" not in result
        assert "<b>" not in result
        assert "😊" not in result
    
    def test_extra_newlines_collapsed(self):
        """3+ consecutive newlines should be collapsed to 2."""
        result = self.cleaner.clean("سلام\n\n\n\n\nدنیا")
        assert "\n\n\n" not in result
    
    def test_clean_preserves_persian_text(self):
        """Clean should preserve Persian text content."""
        text = "این یک متن فارسی عادی است بدون هیچ مشکلی"
        result = self.cleaner.clean(text)
        assert result == text
