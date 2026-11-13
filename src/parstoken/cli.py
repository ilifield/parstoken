"""Command-line interface for Parstoken.

Provides CLI commands for normalizing, cleaning, optimizing,
and counting tokens in Persian text files.
"""

import argparse
import sys
from typing import Optional

from .normalizer import PersianNormalizer
from .cleaner import TextCleaner
from .optimizer import TokenOptimizer
from .tokenizer import PersianTokenizer


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='parstoken',
        description='Persian text preprocessing and LLM token optimization toolkit.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  parstoken normalize input.txt -o output.txt
  parstoken clean input.txt --remove-emojis --remove-hashtags
  parstoken optimize input.txt
  parstoken count input.txt --model gpt-4
  parstoken pipeline input.txt --normalize --clean --optimize
  cat input.txt | parstoken normalize
        """,
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0',
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # --- Normalize command ---
    normalize_parser = subparsers.add_parser(
        'normalize',
        help='Normalize Persian text (fix characters, ZWNJ, diacritics)',
    )
    normalize_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    normalize_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    normalize_parser.add_argument(
        '--keep-diacritics', action='store_true',
        help='Do not remove diacritical marks',
    )
    normalize_parser.add_argument(
        '--digits', choices=['fa', 'en'],
        help='Convert digits to Persian (fa) or English (en)',
    )
    normalize_parser.add_argument(
        '--fix-punctuation', action='store_true',
        help='Normalize Arabic punctuation marks',
    )
    
    # --- Clean command ---
    clean_parser = subparsers.add_parser(
        'clean',
        help='Clean text by removing HTML, URLs, emails, etc.',
    )
    clean_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    clean_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    clean_parser.add_argument(
        '--remove-emojis', action='store_true',
        help='Remove emoji characters',
    )
    clean_parser.add_argument(
        '--remove-hashtags', action='store_true',
        help='Remove hashtags',
    )
    clean_parser.add_argument(
        '--remove-mentions', action='store_true',
        help='Remove @mentions',
    )
    clean_parser.add_argument(
        '--remove-phones', action='store_true',
        help='Remove phone numbers',
    )
    
    # --- Optimize command ---
    optimize_parser = subparsers.add_parser(
        'optimize',
        help='Optimize text to reduce LLM token consumption',
    )
    optimize_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    optimize_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    optimize_parser.add_argument(
        '--max-repeat', type=int, default=1,
        help='Max consecutive character repetitions (default: 1)',
    )
    optimize_parser.add_argument(
        '--stats', action='store_true',
        help='Print optimization statistics to stderr',
    )
    
    # --- Count command ---
    count_parser = subparsers.add_parser(
        'count',
        help='Count and estimate LLM tokens',
    )
    count_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    count_parser.add_argument(
        '--model', default='gpt-4',
        choices=['gpt-4', 'gpt-4o', 'gpt-3.5', 'claude', 'general'],
        help='Model for token estimation (default: gpt-4)',
    )
    
    # --- Pipeline command ---
    pipeline_parser = subparsers.add_parser(
        'pipeline',
        help='Run multiple processing steps in sequence',
    )
    pipeline_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    pipeline_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    pipeline_parser.add_argument(
        '--normalize', action='store_true',
        help='Apply text normalization',
    )
    pipeline_parser.add_argument(
        '--clean', action='store_true',
        help='Apply text cleaning',
    )
    pipeline_parser.add_argument(
        '--optimize', action='store_true',
        help='Apply token optimization',
    )
    pipeline_parser.add_argument(
        '--stats', action='store_true',
        help='Print processing statistics to stderr',
    )
    
    return parser


def read_input(filepath: Optional[str] = None) -> str:
    """Read input from file or stdin.
    
    Args:
        filepath: Path to input file, or None for stdin.
        
    Returns:
        Text content.
    """
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        if sys.stdin.isatty():
            print("Reading from stdin (press Ctrl+D to finish):", file=sys.stderr)
        return sys.stdin.read()


def write_output(text: str, filepath: Optional[str] = None) -> None:
    """Write output to file or stdout.
    
    Args:
        text: Text to write.
        filepath: Path to output file, or None for stdout.
    """
    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Output written to {filepath}", file=sys.stderr)
    else:
        sys.stdout.write(text)
        if not text.endswith('\n'):
            sys.stdout.write('\n')


def cmd_normalize(args: argparse.Namespace) -> None:
    """Execute the normalize command."""
    text = read_input(args.input)
    
    normalizer = PersianNormalizer(
        remove_diacritics=not args.keep_diacritics,
        digit_target=args.digits,
        normalize_punctuation=args.fix_punctuation,
    )
    
    result = normalizer.normalize(text)
    write_output(result, args.output)


def cmd_clean(args: argparse.Namespace) -> None:
    """Execute the clean command."""
    text = read_input(args.input)
    
    cleaner = TextCleaner(
        remove_emojis=args.remove_emojis,
        remove_hashtags=args.remove_hashtags,
        remove_mentions=args.remove_mentions,
        remove_phone_numbers=args.remove_phones,
    )
    
    result = cleaner.clean(text)
    write_output(result, args.output)


def cmd_optimize(args: argparse.Namespace) -> None:
    """Execute the optimize command."""
    text = read_input(args.input)
    
    optimizer = TokenOptimizer(max_char_repeat=args.max_repeat)
    result = optimizer.optimize(text)
    
    if args.stats:
        print(f"\n{result.savings_summary}", file=sys.stderr)
    
    write_output(result.text, args.output)


def cmd_count(args: argparse.Namespace) -> None:
    """Execute the count command."""
    text = read_input(args.input)
    
    tokenizer = PersianTokenizer()
    
    words = tokenizer.count_words(text)
    sentences = tokenizer.count_sentences(text)
    chars = len(text)
    tokens = tokenizer.estimate_llm_tokens(text, model=args.model)
    
    print(f"Characters:         {chars:,}")
    print(f"Words:              {words:,}")
    print(f"Sentences:          {sentences:,}")
    print(f"Estimated tokens:   {tokens:,} ({args.model})")


def cmd_pipeline(args: argparse.Namespace) -> None:
    """Execute the pipeline command."""
    text = read_input(args.input)
    original_len = len(text)
    
    if args.normalize:
        normalizer = PersianNormalizer()
        text = normalizer.normalize(text)
    
    if args.clean:
        cleaner = TextCleaner()
        text = cleaner.clean(text)
    
    if args.optimize:
        optimizer = TokenOptimizer()
        opt_result = optimizer.optimize(text)
        text = opt_result.text
        
        if args.stats:
            print(f"\n{opt_result.savings_summary}", file=sys.stderr)
    
    if args.stats:
        print(f"Original length:  {original_len:,} chars", file=sys.stderr)
        print(f"Final length:     {len(text):,} chars", file=sys.stderr)
    
    write_output(text, args.output)


def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    commands = {
        'normalize': cmd_normalize,
        'clean': cmd_clean,
        'optimize': cmd_optimize,
        'count': cmd_count,
        'pipeline': cmd_pipeline,
    }
    
    try:
        commands[args.command](args)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()
