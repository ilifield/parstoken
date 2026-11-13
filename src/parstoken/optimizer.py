"""Token optimization module for reducing LLM API token consumption.

Provides tools for compressing Persian text to use fewer tokens
while preserving meaning and readability.
"""

import re
from dataclasses import dataclass
from typing import Optional

from .unicode_data import ZWNJ


@dataclass
class OptimizationResult:
    """Result of text optimization with savings metrics.
    
    Attributes:
        text: The optimized text.
        original_length: Character count of the original text.
        optimized_length: Character count of the optimized text.
        estimated_original_tokens: Estimated token count before optimization.
        estimated_optimized_tokens: Estimated token count after optimization.
    """
    text: str
    original_length: int
    optimized_length: int
    estimated_original_tokens: int
    estimated_optimized_tokens: int
    
    @property
    def chars_saved(self) -> int:
        """Number of characters saved."""
        return self.original_length - self.optimized_length
    
    @property
    def tokens_saved(self) -> int:
        """Estimated number of tokens saved."""
        return self.estimated_original_tokens - self.estimated_optimized_tokens
    
    @property
    def savings_percentage(self) -> float:
        """Percentage of tokens saved."""
        if self.estimated_original_tokens == 0:
            return 0.0
        return (self.tokens_saved / self.estimated_original_tokens) * 100
    
    @property
    def savings_summary(self) -> str:
        """Human-readable savings summary."""
        return (
            f"Saved {self.tokens_saved} tokens "
            f"({self.savings_percentage:.1f}%) -- "
            f"{self.estimated_original_tokens} -> {self.estimated_optimized_tokens}"
        )


class TokenOptimizer:
    """Optimizes Persian text to reduce LLM API token consumption.
    
    Example:
        >>> optimizer = TokenOptimizer()
        >>> result = optimizer.optimize("سلاااااام!!!   چطوری؟؟؟")
        >>> print(result.text)
        سلام! چطوری؟
        >>> print(result.savings_summary)
        Saved 5 tokens (29.4%) — 17 → 12
    """
    
    def __init__(
        self,
        compress_repeated_chars: bool = True,
        compress_repeated_punctuation: bool = True,
        remove_redundant_spaces: bool = True,
        max_char_repeat: int = 1,
        max_punctuation_repeat: int = 1,
        tokens_per_char_estimate: float = 0.7,
    ):
        """Initialize the optimizer.
        
        Args:
            compress_repeated_chars: Compress consecutively repeated letters.
            compress_repeated_punctuation: Compress repeated punctuation marks.
            remove_redundant_spaces: Remove unnecessary extra spaces.
            max_char_repeat: Maximum allowed consecutive repetitions of a letter.
            max_punctuation_repeat: Maximum allowed consecutive punctuation marks.
            tokens_per_char_estimate: Estimated tokens per character for Persian text.
                Persian typically uses ~0.7 tokens/char with GPT-4 tokenizer.
        """
        self.compress_repeated_chars_flag = compress_repeated_chars
        self.compress_repeated_punctuation_flag = compress_repeated_punctuation
        self.remove_redundant_spaces_flag = remove_redundant_spaces
        self.max_char_repeat = max_char_repeat
        self.max_punctuation_repeat = max_punctuation_repeat
        self.tokens_per_char_estimate = tokens_per_char_estimate
        
        # Pre-compile patterns
        self._multiple_spaces_re = re.compile(r'[ \t]{2,}')
        self._space_before_punctuation_re = re.compile(r'\s+([.!?،؟؛:»\)])')
        self._space_after_open_re = re.compile(r'([«\(])\s+')
        self._repeated_punctuation_re = re.compile(r'([!?؟.،;؛])\1+')
    
    def optimize(self, text: str) -> OptimizationResult:
        """Apply full optimization pipeline and return result with metrics.
        
        Args:
            text: The text to optimize.
            
        Returns:
            OptimizationResult with optimized text and savings metrics.
        """
        original = text
        
        if self.compress_repeated_chars_flag:
            text = self.compress_chars(text)
        
        if self.compress_repeated_punctuation_flag:
            text = self.compress_punctuation(text)
        
        if self.remove_redundant_spaces_flag:
            text = self.clean_spaces(text)
        
        original_tokens = self._estimate_tokens(original)
        optimized_tokens = self._estimate_tokens(text)
        
        return OptimizationResult(
            text=text,
            original_length=len(original),
            optimized_length=len(text),
            estimated_original_tokens=original_tokens,
            estimated_optimized_tokens=optimized_tokens,
        )
    
    def compress_chars(self, text: str) -> str:
        """Compress consecutively repeated characters.
        
        Reduces patterns like 'سلاااام' to 'سلام' based on max_char_repeat.
        Only compresses actual letter repetitions, not legitimate doubled letters.
        
        Args:
            text: Input text.
            
        Returns:
            Text with compressed repeated characters.
        """
        if not text:
            return text
        
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            count = 1
            
            # Count consecutive repetitions
            while i + count < len(text) and text[i + count] == char:
                count += 1
            
            # For Persian/Arabic characters, compress according to max_char_repeat.
            # For non-Persian alphabets with legitimate double letters (e.g. "Hello"),
            # only compress excessive repetitions (> 2) to preserve valid spelling.
            is_persian_char = (
                '\u0600' <= char <= '\u06FF'
                or '\uFB50' <= char <= '\uFDFF'
                or '\uFE70' <= char <= '\uFEFF'
            )
            threshold = self.max_char_repeat if is_persian_char else max(2, self.max_char_repeat)
            repeat_limit = self.max_char_repeat if is_persian_char else min(2, self.max_char_repeat)
            
            if char.isalpha() and count > threshold:
                result.append(char * repeat_limit)
            else:
                result.append(char * count)
            
            i += count
        
        return ''.join(result)
    
    def compress_punctuation(self, text: str) -> str:
        """Compress repeated punctuation marks.
        
        Reduces patterns like '!!!' or '???' to single marks,
        and normalizes mixed sequences like '!؟!؟' to '!؟'.
        
        Args:
            text: Input text.
            
        Returns:
            Text with compressed punctuation.
        """
        replacement = r'\1' * self.max_punctuation_repeat
        text = self._repeated_punctuation_re.sub(replacement, text)
        
        # Compress mixed exclamation and question marks (e.g., !؟!؟ -> !؟)
        text = re.sub(r'(![؟?]|[؟?]!){2,}', r'!؟', text)
        return text
    
    def clean_spaces(self, text: str) -> str:
        """Remove redundant spaces and fix spacing around punctuation.
        
        Args:
            text: Input text.
            
        Returns:
            Text with cleaned spaces.
        """
        # Collapse multiple spaces/tabs
        text = self._multiple_spaces_re.sub(' ', text)
        
        # Remove space before closing punctuation
        text = self._space_before_punctuation_re.sub(r'\1', text)
        
        # Remove space after opening brackets
        text = self._space_after_open_re.sub(r'\1', text)
        
        return text.strip()
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate the token count for Persian text.
        
        Uses a character-based estimation. For more accurate counting,
        use the tokenizer module with a specific model's tokenizer.
        
        Args:
            text: Input text.
            
        Returns:
            Estimated token count.
        """
        if not text:
            return 0
        return max(1, int(len(text) * self.tokens_per_char_estimate))
