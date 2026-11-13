"""Benchmark script for measuring Parstoken performance and token savings.

Usage:
    python benchmarks/benchmark_tokens.py
"""

import time
import sys
import os

if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parstoken import PersianNormalizer, TextCleaner, TokenOptimizer, pipeline


# Sample Persian texts of varying complexity
SAMPLE_TEXTS = [
    # Simple text with Arabic characters
    "اين يك متن ساده فارسي است كه با كاراكترهاي عربي نوشته شده است.",
    
    # Text with diacritics
    "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ. سَلامٌ عَلَيْكُمْ.",
    
    # Text with repeated characters (social media style)
    "سلاااااام!!! خوبییییی؟؟؟ عالیییییه!!!",
    
    # Mixed text with URLs and mentions
    "سلام @user123 این لینک رو ببین https://example.com/path?q=test #پایتون #هوش_مصنوعی",
    
    # Long paragraph
    (
        "زبان فارسی یکی از زبان‌های هندواروپایی است که در کشورهای ایران، افغانستان و "
        "تاجیکستان رسمی است. این زبان دارای تاریخ غنی و ادبیات کهن است. شاعرانی مانند "
        "فردوسی، حافظ، سعدی و مولوی از بزرگ‌ترین شاعران جهان هستند. امروزه بیش از ۱۱۰ "
        "میلیون نفر به زبان فارسی صحبت می‌کنند. زبان فارسی با خط عربی نوشته می‌شود اما "
        "تفاوت‌هایی در حروف و آوانگاری دارد."
    ),
]


def benchmark_normalizer():
    """Benchmark the normalizer."""
    normalizer = PersianNormalizer()
    text = " ".join(SAMPLE_TEXTS) * 100  # Repeat for meaningful benchmark
    
    start = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        normalizer.normalize(text)
    elapsed = time.perf_counter() - start
    
    chars_per_sec = (len(text) * iterations) / elapsed
    print(f"Normalizer:  {chars_per_sec:,.0f} chars/sec ({elapsed:.3f}s for {iterations} iterations)")


def benchmark_cleaner():
    """Benchmark the cleaner."""
    cleaner = TextCleaner(
        remove_emojis=True,
        remove_hashtags=True,
        remove_mentions=True,
    )
    text = " ".join(SAMPLE_TEXTS) * 100
    
    start = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        cleaner.clean(text)
    elapsed = time.perf_counter() - start
    
    chars_per_sec = (len(text) * iterations) / elapsed
    print(f"Cleaner:     {chars_per_sec:,.0f} chars/sec ({elapsed:.3f}s for {iterations} iterations)")


def benchmark_optimizer():
    """Benchmark the optimizer."""
    optimizer = TokenOptimizer()
    text = " ".join(SAMPLE_TEXTS) * 100
    
    start = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        optimizer.optimize(text)
    elapsed = time.perf_counter() - start
    
    chars_per_sec = (len(text) * iterations) / elapsed
    print(f"Optimizer:   {chars_per_sec:,.0f} chars/sec ({elapsed:.3f}s for {iterations} iterations)")


def benchmark_pipeline():
    """Benchmark the full pipeline."""
    text = " ".join(SAMPLE_TEXTS) * 100
    
    start = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        pipeline(text)
    elapsed = time.perf_counter() - start
    
    chars_per_sec = (len(text) * iterations) / elapsed
    print(f"Pipeline:    {chars_per_sec:,.0f} chars/sec ({elapsed:.3f}s for {iterations} iterations)")


def show_token_savings():
    """Show token savings for each sample text."""
    print("\n--- Token Savings Report ---\n")
    
    for i, text in enumerate(SAMPLE_TEXTS, 1):
        result = pipeline(text)
        print(f"Sample {i}:")
        print(f"  Original:  {result.original_length} chars, ~{result.estimated_original_tokens} tokens")
        print(f"  Optimized: {result.optimized_length} chars, ~{result.estimated_optimized_tokens} tokens")
        print(f"  {result.savings_summary}")
        print()


if __name__ == '__main__':
    print("=" * 60)
    print("Parstoken Benchmark")
    print("=" * 60)
    print()
    
    print("--- Performance Benchmarks ---\n")
    benchmark_normalizer()
    benchmark_cleaner()
    benchmark_optimizer()
    benchmark_pipeline()
    
    show_token_savings()
