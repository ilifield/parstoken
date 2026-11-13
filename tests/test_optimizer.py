"""Tests for the TokenOptimizer module."""

import pytest

from parstoken.optimizer import OptimizationResult, TokenOptimizer


class TestTokenOptimizer:
    """Tests for TokenOptimizer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.optimizer = TokenOptimizer()
    
    def test_compress_repeated_chars(self):
        """Repeated characters should be compressed."""
        result = self.optimizer.compress_chars("سلاااااام")
        assert result == "سلام"
    
    def test_compress_preserves_spaces(self):
        """Spaces should not be compressed as characters."""
        result = self.optimizer.compress_chars("سلام    دنیا")
        assert "    " in result  # Spaces preserved (handled by clean_spaces)
    
    def test_compress_single_chars(self):
        """Single characters should not be affected."""
        result = self.optimizer.compress_chars("سلام")
        assert result == "سلام"
    
    def test_compress_punctuation(self):
        """Repeated punctuation should be compressed."""
        result = self.optimizer.compress_punctuation("سلام!!!")
        assert result == "سلام!"
    
    def test_compress_question_marks(self):
        """Repeated question marks should be compressed."""
        result = self.optimizer.compress_punctuation("واقعا؟؟؟")
        assert result == "واقعا؟"
    
    def test_compress_mixed_punctuation(self):
        """Mixed question and exclamation marks should be normalized."""
        result = self.optimizer.compress_punctuation("واقعا!؟!؟")
        assert result == "واقعا!؟"
    
    def test_clean_spaces(self):
        """Multiple spaces should be collapsed."""
        result = self.optimizer.clean_spaces("سلام     دنیا")
        assert result == "سلام دنیا"
    
    def test_space_before_punctuation(self):
        """Spaces before punctuation should be removed."""
        result = self.optimizer.clean_spaces("سلام .")
        assert result == "سلام."
    
    def test_optimize_returns_result(self):
        """Optimize should return an OptimizationResult."""
        result = self.optimizer.optimize("سلاااام!!!")
        assert isinstance(result, OptimizationResult)
        assert result.text == "سلام!"
    
    def test_optimization_result_savings(self):
        """OptimizationResult should calculate savings correctly."""
        result = self.optimizer.optimize("سلاااااااام!!!   خوبییییی؟؟؟")
        assert result.tokens_saved > 0
        assert result.savings_percentage > 0
        assert result.chars_saved > 0
    
    def test_optimization_result_summary(self):
        """OptimizationResult should have a human-readable summary."""
        result = self.optimizer.optimize("سلاااام!!!")
        assert "Saved" in result.savings_summary
        assert "tokens" in result.savings_summary
    
    def test_no_optimization_needed(self):
        """Text that doesn't need optimization should be unchanged."""
        text = "سلام دنیا."
        result = self.optimizer.optimize(text)
        assert result.text == text
    
    def test_empty_text(self):
        """Empty text should return empty result."""
        result = self.optimizer.optimize("")
        assert result.text == ""
        assert result.tokens_saved == 0
    
    def test_custom_max_repeat(self):
        """Custom max_char_repeat should be respected."""
        optimizer = TokenOptimizer(max_char_repeat=2)
        result = optimizer.compress_chars("سلااااام")
        assert result == "سلاام"
    
    def test_mixed_content(self):
        """Mixed Persian and English content should be handled."""
        result = self.optimizer.optimize("سلاااام Hello!!!")
        assert result.text == "سلام Hello!"
    
    def test_savings_percentage_zero_division(self):
        """Empty text should not cause division by zero."""
        result = OptimizationResult(
            text="", original_length=0, optimized_length=0,
            estimated_original_tokens=0, estimated_optimized_tokens=0,
        )
        assert result.savings_percentage == 0.0
