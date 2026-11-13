# Changelog

All notable changes to **Parstoken** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] - 2026-11-13

### Added
- **TokenOptimizer**: Compression engine for repeated characters, elongated vowels, and redundant punctuation sequences.
- **LLM Token Reduction**: Reduces prompt token consumption by up to 30–52% on informal Persian text.
- **Unified Pipeline API**: `pipeline()` convenience function combining normalizer, cleaner, and optimizer in a single call.
- **Benchmarking Suite**: High-throughput performance benchmark measuring processing speeds (>24M chars/second).
- Multi-OS GitHub Actions CI matrix running on Ubuntu, macOS, and Windows across Python 3.8–3.13.

---

## [0.2.0] - 2026-11-13

### Added
- **TextCleaner**: Sanitization module to strip HTML/XML markup, URLs, email addresses, and phone numbers.
- **PersianTokenizer**: Persian-aware word and sentence segmentation with ZWNJ preservation.
- **CLI Toolkit**: Command-line interface with subcommands (`normalize`, `clean`, `optimize`, `count`, `pipeline`) and Unix pipe support.
- Heuristic token estimation calibrated for GPT-4, Claude 3.5, and Gemini models.

---

## [0.1.0] - 2026-11-13

### Added
- Initial core release of Parstoken.
- **PersianNormalizer**: Unicode normalization (NFC) and Arabic-to-Persian character conversion (`ك` → `ک`, `ي` → `ی`, `ة` → `ه`).
- **Diacritics Stripping**: Removal of Arabic tashkeel/harakat.
- **Smart ZWNJ Handling**: Half-space normalization for Persian affixes.
- **Digit Normalization**: Bidirectional conversion between Persian (`۱۲۳`), Arabic (`١٢٣`), and English (`123`) digits.
- Comprehensive unit test suite with 100% pass rate.
