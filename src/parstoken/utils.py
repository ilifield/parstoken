"""Shared utility functions for the Parstoken library."""

import re
from typing import Optional


def is_persian(text: str) -> bool:
    """Check if the text contains Persian/Arabic script characters.
    
    Args:
        text: Text to check.
        
    Returns:
        True if the text contains at least one Persian/Arabic character.
    """
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', text))


def persian_char_ratio(text: str) -> float:
    """Calculate the ratio of Persian/Arabic characters in the text.
    
    Args:
        text: Text to analyze.
        
    Returns:
        Ratio between 0.0 and 1.0.
    """
    if not text:
        return 0.0
    
    persian_count = len(re.findall(
        r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', text
    ))
    total = len(text.replace(' ', ''))
    
    if total == 0:
        return 0.0
    
    return persian_count / total


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """Truncate text to a maximum length, adding a suffix if truncated.
    
    Args:
        text: Text to truncate.
        max_length: Maximum allowed length (including suffix).
        suffix: String to append when truncating.
        
    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def remove_control_characters(text: str) -> str:
    """Remove Unicode control characters from text.
    
    Preserves newlines, tabs, and ZWNJ.
    
    Args:
        text: Input text.
        
    Returns:
        Text without control characters.
    """
    # Keep: \n (0x0A), \r (0x0D), \t (0x09), ZWNJ (0x200C)
    return ''.join(
        char for char in text
        if not (
            ord(char) < 0x20
            and char not in ('\n', '\r', '\t')
        )
        or char == '\u200c'  # Keep ZWNJ
    )


def count_characters(text: str, ignore_spaces: bool = False) -> int:
    """Count characters in text.
    
    Args:
        text: Input text.
        ignore_spaces: Whether to exclude spaces from the count.
        
    Returns:
        Character count.
    """
    if ignore_spaces:
        return len(text.replace(' ', ''))
    return len(text)
