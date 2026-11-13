# Parstoken v0.1.0 — Initial Stable Release

## 🚀 Persian Text Preprocessing & Token Optimization for LLMs

We are excited to announce the first official stable release of **Parstoken (v0.1.0)**! 

Parstoken is an engineered, zero-dependency Python toolkit designed to solve critical tokenization and normalization bottlenecks for the **110M+ Persian speakers** interacting with modern Large Language Models (OpenAI, Anthropic Claude, Google Gemini, Meta Llama).

---

## 🌟 What's New in v0.1.0

### 1. Unicode & Script Normalization (`PersianNormalizer`)
- **Arabic to Persian Character Conversion**: Standardizes Arabic letter variants (`ك` → `ک`, `ي` → `ی`, `ة` → `ه`, `ۀ` → `هٔ`) to eliminate split subword tokens.
- **Diacritics Removal**: Strips Arabic short vowels and harakat (`َ ُ ِ ّ ْ ً ٌ ٍ`) that inflate token counts without providing prompt value.
- **Smart Half-Space (ZWNJ) Handling**: Intelligently standardizes Zero-Width Non-Joiner (`\u200c`) around prefixes and suffixes (`می‌`, `ها`, `تر`) while removing orphaned ZWNJs.
- **Bidirectional Digit Conversion**: Convert between Persian (`۱۲۳`), Arabic (`١٢٣`), and ASCII (`123`) numerals.

### 2. Token-Saving Compression (`TokenOptimizer`)
- **Character Elongation Compression**: Compresses repeated characters (e.g. `سلااااام` → `سلام`) to prevent token waste in user chat prompts.
- **Punctuation Compression**: Collapses redundant punctuation sequences (`؟؟؟` → `؟`, `!!!!` → `!`).
- **Whitespace & Boundary Optimization**: Removes extraneous spacing before punctuation marks and cleans multi-line padding.
- **Savings Telemetry**: Provides real-time metrics showing tokens saved, character delta, and reduction percentage.

### 3. Noise Sanitizer (`TextCleaner`)
- Configurable stripping of HTML/XML tags, web URLs, email addresses, phone numbers (Iranian mobile and landlines), emojis, hashtags, and mentions.

### 4. LLM Token Estimation & Tokenization (`PersianTokenizer`)
- Persian-aware word and sentence tokenization that respects ZWNJ boundaries.
- Heuristic token estimation calibrated for GPT-4o, GPT-4, Claude 3.5, and Gemini context windows.

### 5. High-Throughput CLI
- Full command-line interface with subcommands: `normalize`, `clean`, `optimize`, `count`, and `pipeline`.
- Native UNIX pipe and stdin/stdout support for shell data processing.

---

## ⚡ Performance Benchmarks

Measured on benchmark dataset across 100 iterations:
- **Text Normalizer**: ~24,600,000 chars/second
- **Noise Cleaner**: ~28,600,000 chars/second
- **Token Optimizer**: ~3,100,000 chars/second
- **Full Pipeline**: ~2,800,000 chars/second
- **Token Reduction**: Up to **52.0% token reduction** on informal conversational texts.

---

## 🧪 Quality & Test Coverage

- **100% Test Pass Rate**: 76 unit tests covering Unicode edge cases, diacritics, regex compilation, and CLI execution.
- **Multi-OS CI**: Automated continuous integration workflows running on Ubuntu, macOS, and Windows across Python 3.8 through 3.13.

---

## 📦 Distribution Packages & Checksums

| Package Asset | Format | SHA-256 Checksum |
|---|---|---|
| `parstoken-0.1.0-py3-none-any.whl` | Wheel | `38f2cd241200cdd4cbecccfc0e24208e4eda27a141ef050905da44bc3170d904` |
| `parstoken-0.1.0.tar.gz` | Source Archive | `2251ca6f3c5384b51ecb7d6e1054037a6c0e2f8f25602e65f8bd42dc2f19f05d` |

---

## 📥 Installation

```bash
pip install parstoken
```

Or install from source:
```bash
git clone https://github.com/ilifield/parstoken.git
cd parstoken
pip install .
```

---

**Maintainer**: [@ilifield](https://github.com/ilifield)  
**Full Changelog**: https://github.com/ilifield/parstoken/blob/main/CHANGELOG.md
