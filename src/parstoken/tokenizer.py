"""Persian-aware text tokenization module.

Provides word and sentence tokenization that correctly handles
Persian-specific features like ZWNJ (half-space) and Persian
sentence boundaries.
"""

import re
from typing import List, Optional

from .unicode_data import PERSIAN_ZWNJ_SUFFIXES, SENTENCE_ENDINGS, ZWNJ


class PersianTokenizer:
    """Persian-aware word and sentence tokenizer.
    
    Unlike generic tokenizers, this handles ZWNJ (half-space) correctly
    and understands Persian sentence boundary patterns.
    
    Example:
        >>> tokenizer = PersianTokenizer()
        >>> tokenizer.word_tokenize("کتاب‌های خوب را بخوانید")
        ['کتاب‌های', 'خوب', 'را', 'بخوانید']
        >>> tokenizer.sentence_tokenize("سلام. حالت خوبه؟ آره!")
        ['سلام.', 'حالت خوبه؟', 'آره!']
    """
    
    def __init__(self, preserve_zwnj: bool = True):
        """Initialize the tokenizer.
        
        Args:
            preserve_zwnj: Whether to keep ZWNJ in tokenized output.
        """
        self.preserve_zwnj = preserve_zwnj
        
        # Word boundary pattern (splits on whitespace but preserves ZWNJ-connected words)
        self._word_re = re.compile(r'[^\s]+')
        
        # Sentence boundary pattern
        # Matches sentence-ending punctuation followed by space or end of string
        self._sentence_re = re.compile(
            r'(?<=[.!?؟!۔])\s+'
        )
    
    def word_tokenize(self, text: str) -> List[str]:
        """Tokenize text into words, respecting ZWNJ connections.
        
        Words connected with ZWNJ (half-space) are treated as single tokens.
        For example, "کتاب‌ها" (book+plural suffix) remains one token.
        
        Args:
            text: Input text.
            
        Returns:
            List of word tokens.
        """
        if not text:
            return []
        
        tokens = self._word_re.findall(text)
        
        if not self.preserve_zwnj:
            tokens = [t.replace(ZWNJ, '') for t in tokens]
        
        # Filter out empty tokens
        return [t for t in tokens if t.strip()]
    
    def sentence_tokenize(self, text: str) -> List[str]:
        """Split text into sentences at Persian sentence boundaries.
        
        Handles Persian-specific sentence endings including ؟ and ۔
        in addition to standard punctuation.
        
        Args:
            text: Input text.
            
        Returns:
            List of sentences.
        """
        if not text:
            return []
        
        # Split on sentence boundaries
        sentences = self._sentence_re.split(text.strip())
        
        # Filter out empty strings and strip whitespace
        return [s.strip() for s in sentences if s.strip()]
    
    def count_words(self, text: str) -> int:
        """Count the number of words in the text.
        
        Args:
            text: Input text.
            
        Returns:
            Word count.
        """
        return len(self.word_tokenize(text))
    
    def count_sentences(self, text: str) -> int:
        """Count the number of sentences in the text.
        
        Args:
            text: Input text.
            
        Returns:
            Sentence count.
        """
        return len(self.sentence_tokenize(text))
    
    @staticmethod
    def estimate_llm_tokens(text: str, model: str = 'gpt-4') -> int:
        """Estimate the number of LLM tokens for the given text.
        
        Provides a rough estimate based on character-to-token ratios
        observed for different models. For exact counting, use the
        model's official tokenizer.
        
        Args:
            text: Input text.
            model: Model name for token estimation.
                   Supported: 'gpt-4', 'gpt-3.5', 'claude', 'general'.
            
        Returns:
            Estimated token count.
            
        Note:
            These are estimates. For production use, integrate with
            tiktoken (OpenAI) or the model's official tokenizer.
        """
        if not text:
            return 0
        
        # Approximate tokens-per-character ratios for Persian text
        # Persian uses more tokens per character than English in most tokenizers
        ratios = {
            'gpt-4': 0.70,
            'gpt-4o': 0.55,
            'gpt-3.5': 0.75,
            'claude': 0.65,
            'general': 0.70,
        }
        
        ratio = ratios.get(model, ratios['general'])
        return max(1, int(len(text) * ratio))
