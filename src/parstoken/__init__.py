"""Parstoken — Persian Text Preprocessing & Token Optimization for LLMs.

A zero-dependency Python library that normalizes, cleans, and optimizes
Persian (Farsi) text for Large Language Models, reducing API token
consumption by up to 30%.

Basic usage:
    >>> from parstoken import PersianNormalizer, TextCleaner, TokenOptimizer
    >>> normalizer = PersianNormalizer()
    >>> normalizer.normalize("متن فارسي با كاراكترهاي عربي")
    'متن فارسی با کاراکترهای عربی'

Full pipeline:
    >>> from parstoken import pipeline
    >>> result = pipeline("سلاااام!   اين يك    تست است...")
    >>> print(result.text)
    سلام! این یک تست است.
"""

__version__ = "0.3.0"

from .normalizer import PersianNormalizer
from .cleaner import TextCleaner
from .optimizer import OptimizationResult, TokenOptimizer
from .tokenizer import PersianTokenizer
from .utils import (
    count_characters,
    is_persian,
    persian_char_ratio,
    remove_control_characters,
    truncate_text,
)


def pipeline(
    text: str,
    normalize: bool = True,
    clean: bool = True,
    optimize: bool = True,
    **kwargs,
) -> OptimizationResult:
    """Run the full text processing pipeline.
    
    Convenience function that applies normalization, cleaning, and
    optimization in sequence.
    
    Args:
        text: Input Persian text.
        normalize: Apply text normalization.
        clean: Apply text cleaning.
        optimize: Apply token optimization.
        **kwargs: Additional keyword arguments passed to individual processors.
        
    Returns:
        OptimizationResult with processed text and metrics.
        
    Example:
        >>> result = pipeline("سلاااام!!!   اين يك   تست است...")
        >>> print(result.text)
        سلام! این یک تست است.
        >>> print(result.savings_summary)
        Saved 8 tokens (32.0%) — 25 → 17
    """
    original_length = len(text)
    
    if normalize:
        normalizer = PersianNormalizer(**{
            k: v for k, v in kwargs.items()
            if k in PersianNormalizer.__init__.__code__.co_varnames
        })
        text = normalizer.normalize(text)
    
    if clean:
        cleaner = TextCleaner(**{
            k: v for k, v in kwargs.items()
            if k in TextCleaner.__init__.__code__.co_varnames
        })
        text = cleaner.clean(text)
    
    if optimize:
        optimizer = TokenOptimizer(**{
            k: v for k, v in kwargs.items()
            if k in TokenOptimizer.__init__.__code__.co_varnames
        })
        return optimizer.optimize(text)
    
    # If optimization is disabled, return a result with basic metrics
    return OptimizationResult(
        text=text,
        original_length=original_length,
        optimized_length=len(text),
        estimated_original_tokens=max(1, int(original_length * 0.7)),
        estimated_optimized_tokens=max(1, int(len(text) * 0.7)),
    )


def count_tokens(text: str, model: str = 'gpt-4') -> int:
    """Quick function to estimate LLM tokens for Persian text.
    
    Args:
        text: Input text.
        model: Model name for estimation.
        
    Returns:
        Estimated token count.
    """
    return PersianTokenizer.estimate_llm_tokens(text, model=model)


__all__ = [
    'PersianNormalizer',
    'TextCleaner',
    'TokenOptimizer',
    'OptimizationResult',
    'PersianTokenizer',
    'pipeline',
    'count_tokens',
    'is_persian',
    'persian_char_ratio',
    'count_characters',
    'truncate_text',
    'remove_control_characters',
    '__version__',
]
