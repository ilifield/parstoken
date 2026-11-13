"""Persian text normalization module.

Handles Unicode normalization, Arabic-to-Persian character conversion,
half-space (ZWNJ) management, diacritics removal, and number/punctuation
normalization.
"""

import re
import unicodedata
from typing import Optional

from .unicode_data import (
    ARABIC_DIACRITICS,
    ARABIC_PUNCTUATION_MAP,
    ARABIC_TO_PERSIAN_DIGITS,
    ARABIC_TO_PERSIAN_MAP,
    ENGLISH_TO_PERSIAN_DIGITS,
    PERSIAN_TO_ENGLISH_DIGITS,
    SPACE_CHARS,
    ZWNJ,
    ZWJ,
)


class PersianNormalizer:
    """Normalizes Persian text for consistent processing and LLM usage.
    
    This class provides methods for normalizing various aspects of Persian
    text including Unicode characters, half-spaces (ZWNJ), diacritics,
    numbers, and punctuation.
    
    Example:
        >>> normalizer = PersianNormalizer()
        >>> normalizer.normalize("متن فارسي با كاراكترهاي عربي")
        'متن فارسی با کاراکترهای عربی'
    """
    
    def __init__(
        self,
        unicode_normalize: bool = True,
        fix_arabic_chars: bool = True,
        remove_diacritics: bool = True,
        normalize_halfspace: bool = True,
        normalize_whitespace: bool = True,
        normalize_punctuation: bool = False,
        digit_target: Optional[str] = None,
    ):
        """Initialize the normalizer with configuration options.
        
        Args:
            unicode_normalize: Apply Unicode NFC normalization.
            fix_arabic_chars: Replace Arabic characters with Persian equivalents.
            remove_diacritics: Remove Arabic diacritical marks (tashkeel).
            normalize_halfspace: Normalize ZWNJ (half-space) usage.
            normalize_whitespace: Normalize various space characters.
            normalize_punctuation: Normalize Arabic punctuation to standard forms.
            digit_target: Target digit format - 'fa' for Persian, 'en' for English,
                         None to leave unchanged.
        """
        self.unicode_normalize = unicode_normalize
        self.fix_arabic_chars = fix_arabic_chars
        self.remove_diacritics_flag = remove_diacritics
        self.normalize_halfspace_flag = normalize_halfspace
        self.normalize_whitespace_flag = normalize_whitespace
        self.normalize_punctuation_flag = normalize_punctuation
        self.digit_target = digit_target
        
        # Pre-compile regex patterns
        self._multiple_spaces_re = re.compile(r' {2,}')
        self._multiple_newlines_re = re.compile(r'\n{3,}')
        self._zwnj_spaces_re = re.compile(r'\s*' + ZWNJ + r'\s*')
        self._leading_trailing_zwnj_re = re.compile(
            r'(^' + ZWNJ + r'+|' + ZWNJ + r'+$)'
        )
    
    def normalize(self, text: str) -> str:
        """Apply full normalization pipeline to the text.
        
        Applies all enabled normalization steps in the correct order.
        
        Args:
            text: The Persian text to normalize.
            
        Returns:
            Normalized text.
        """
        if not text:
            return text
        
        if self.unicode_normalize:
            text = self.apply_unicode_normalization(text)
        
        if self.fix_arabic_chars:
            text = self.fix_arabic_characters(text)
        
        if self.remove_diacritics_flag:
            text = self.strip_diacritics(text)
        
        if self.digit_target:
            text = self.normalize_digits(text, target=self.digit_target)
        
        if self.normalize_punctuation_flag:
            text = self.fix_punctuation(text)
        
        if self.normalize_halfspace_flag:
            text = self.fix_halfspace(text)
        
        if self.normalize_whitespace_flag:
            text = self.fix_whitespace(text)
        
        return text
    
    @staticmethod
    def apply_unicode_normalization(text: str) -> str:
        """Apply Unicode NFC normalization.
        
        NFC (Canonical Decomposition, followed by Canonical Composition)
        ensures consistent representation of Unicode characters.
        
        Args:
            text: Input text.
            
        Returns:
            NFC-normalized text.
        """
        return unicodedata.normalize('NFC', text)
    
    @staticmethod
    def fix_arabic_characters(text: str) -> str:
        """Replace Arabic characters with their Persian equivalents.
        
        Converts Arabic-specific characters (like ك and ي) to their
        Persian counterparts (ک and ی).
        
        Args:
            text: Input text.
            
        Returns:
            Text with Persian characters.
        """
        for arabic, persian in ARABIC_TO_PERSIAN_MAP.items():
            text = text.replace(arabic, persian)
        return text
    
    @staticmethod
    def strip_diacritics(text: str) -> str:
        """Remove Arabic diacritical marks (tashkeel/harakat).
        
        Removes marks like Fatha, Damma, Kasra, Shadda, etc.
        
        Args:
            text: Input text.
            
        Returns:
            Text without diacritics.
        """
        for mark in ARABIC_DIACRITICS:
            text = text.replace(mark, '')
        return text
    
    @staticmethod
    def normalize_digits(text: str, target: str = 'fa') -> str:
        """Normalize digits to a consistent format.
        
        Args:
            text: Input text.
            target: 'fa' for Persian digits, 'en' for English digits.
            
        Returns:
            Text with normalized digits.
            
        Raises:
            ValueError: If target is not 'fa' or 'en'.
        """
        if target not in ('fa', 'en'):
            raise ValueError(f"Invalid digit target: {target!r}. Use 'fa' or 'en'.")
        
        if target == 'fa':
            # Convert English and Arabic digits to Persian
            for eng, per in ENGLISH_TO_PERSIAN_DIGITS.items():
                text = text.replace(eng, per)
            for arb, per in ARABIC_TO_PERSIAN_DIGITS.items():
                text = text.replace(arb, per)
        else:
            # Convert Persian and Arabic digits to English
            for per, eng in PERSIAN_TO_ENGLISH_DIGITS.items():
                text = text.replace(per, eng)
            for arb, per in ARABIC_TO_PERSIAN_DIGITS.items():
                eng = PERSIAN_TO_ENGLISH_DIGITS.get(per, per)
                text = text.replace(arb, eng)
        
        return text
    
    @staticmethod
    def fix_punctuation(text: str) -> str:
        """Normalize Arabic punctuation to standard equivalents.
        
        Args:
            text: Input text.
            
        Returns:
            Text with normalized punctuation.
        """
        for arabic, standard in ARABIC_PUNCTUATION_MAP.items():
            text = text.replace(arabic, standard)
        return text
    
    def fix_halfspace(self, text: str) -> str:
        """Normalize ZWNJ (Zero-Width Non-Joiner / half-space) usage.
        
        - Removes spaces around ZWNJ
        - Removes ZWJ characters
        - Removes leading/trailing ZWNJ from words
        - Collapses multiple consecutive ZWNJs
        
        Args:
            text: Input text.
            
        Returns:
            Text with normalized half-spaces.
        """
        # Remove ZWJ (Zero-Width Joiner)
        text = text.replace(ZWJ, '')
        
        # Remove spaces around ZWNJ
        text = self._zwnj_spaces_re.sub(ZWNJ, text)
        
        # Collapse multiple ZWNJs
        while ZWNJ + ZWNJ in text:
            text = text.replace(ZWNJ + ZWNJ, ZWNJ)
        
        return text
    
    def fix_whitespace(self, text: str) -> str:
        """Normalize various space characters and whitespace patterns.
        
        Replaces special Unicode spaces with standard space, collapses
        multiple spaces, and limits consecutive newlines.
        
        Args:
            text: Input text.
            
        Returns:
            Text with normalized whitespace.
        """
        # Replace special space characters with standard space
        for space_char in SPACE_CHARS:
            text = text.replace(space_char, ' ')
        
        # Collapse multiple spaces (but not newlines)
        text = self._multiple_spaces_re.sub(' ', text)
        
        # Limit consecutive newlines to 2
        text = self._multiple_newlines_re.sub('\n\n', text)
        
        # Strip leading/trailing whitespace from each line
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        text = '\n'.join(lines)
        
        return text.strip()
