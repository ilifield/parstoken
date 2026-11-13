"""Tests for the PersianTokenizer module."""

import pytest

from parstoken.tokenizer import PersianTokenizer


class TestPersianTokenizer:
    """Tests for PersianTokenizer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tokenizer = PersianTokenizer()
    
    def test_word_tokenize_simple(self):
        """Simple text should be tokenized into words."""
        result = self.tokenizer.word_tokenize("سلام دنیا")
        assert result == ["سلام", "دنیا"]
    
    def test_word_tokenize_empty(self):
        """Empty string should return empty list."""
        assert self.tokenizer.word_tokenize("") == []
    
    def test_word_tokenize_preserves_zwnj(self):
        """ZWNJ-connected words should be kept as single tokens."""
        result = self.tokenizer.word_tokenize("کتاب\u200cها")
        assert len(result) == 1
        assert result[0] == "کتاب\u200cها"
    
    def test_word_tokenize_without_zwnj(self):
        """ZWNJ can be stripped from tokens."""
        tokenizer = PersianTokenizer(preserve_zwnj=False)
        result = tokenizer.word_tokenize("کتاب\u200cها")
        assert result[0] == "کتابها"
    
    def test_word_tokenize_multiple_words(self):
        """Multiple words should be correctly tokenized."""
        result = self.tokenizer.word_tokenize("من کتاب\u200cهای خوب را می\u200cخوانم")
        assert len(result) == 5
    
    def test_sentence_tokenize_simple(self):
        """Simple sentences should be split correctly."""
        result = self.tokenizer.sentence_tokenize("سلام. خوبی؟")
        assert len(result) == 2
    
    def test_sentence_tokenize_empty(self):
        """Empty string should return empty list."""
        assert self.tokenizer.sentence_tokenize("") == []
    
    def test_sentence_tokenize_single(self):
        """Single sentence should return list with one item."""
        result = self.tokenizer.sentence_tokenize("سلام دنیا")
        assert len(result) == 1
    
    def test_sentence_tokenize_persian_question(self):
        """Persian question mark should be a sentence boundary."""
        result = self.tokenizer.sentence_tokenize("حالت خوبه؟ آره خوبم.")
        assert len(result) == 2
    
    def test_count_words(self):
        """Word count should be correct."""
        assert self.tokenizer.count_words("سلام دنیا خوب") == 3
    
    def test_count_words_empty(self):
        """Empty text should have zero words."""
        assert self.tokenizer.count_words("") == 0
    
    def test_count_sentences(self):
        """Sentence count should be correct."""
        assert self.tokenizer.count_sentences("سلام. خوبی؟ آره!") == 3
    
    def test_estimate_llm_tokens(self):
        """Token estimation should return a positive integer."""
        result = self.tokenizer.estimate_llm_tokens("سلام دنیا", model='gpt-4')
        assert result > 0
        assert isinstance(result, int)
    
    def test_estimate_tokens_empty(self):
        """Empty text should return 0 tokens."""
        assert self.tokenizer.estimate_llm_tokens("") == 0
    
    def test_estimate_tokens_different_models(self):
        """Different models should give different estimates."""
        text = "این یک متن فارسی طولانی برای تست است"
        gpt4 = self.tokenizer.estimate_llm_tokens(text, model='gpt-4')
        gpt4o = self.tokenizer.estimate_llm_tokens(text, model='gpt-4o')
        # gpt-4o has lower ratio, so should estimate fewer tokens
        assert gpt4o <= gpt4
    
    def test_estimate_tokens_unknown_model(self):
        """Unknown model should use general ratio."""
        result = self.tokenizer.estimate_llm_tokens("سلام", model='unknown-model')
        assert result > 0
