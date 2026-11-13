<div align="center">

# 🔤 Parstoken

**High-Performance Persian Text Preprocessing & Token Optimization for Large Language Models**

[![PyPI version](https://img.shields.io/pypi/v/parstoken.svg)](https://pypi.org/project/parstoken/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CI Tests](https://github.com/ilifield/parstoken/actions/workflows/ci.yml/badge.svg)](https://github.com/ilifield/parstoken/actions/workflows/ci.yml)
[![Ecosystem: LLM Tooling](https://img.shields.io/badge/Ecosystem-NLP%20%2F%20LLM-blueviolet.svg)](https://github.com/ilifield/parstoken)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-success.svg)](https://github.com/ilifield/parstoken)

A production-grade, zero-dependency Python toolkit designed to **normalize, clean, and optimize Persian (Farsi) text** for modern LLM APIs (OpenAI, Anthropic Claude, Google Gemini, Llama 3) — **reducing token counts by up to 30–50%** while preserving semantic meaning.

[Key Features](#-key-features) · [Ecosystem Importance](#-ecosystem-importance) · [Installation](#-installation) · [Quick Start](#-quick-start) · [LLM Integrations](#-llm-pipeline-integrations) · [Benchmarks](#-benchmarks) · [Governance & Maintenance](#-governance--active-maintenance)

</div>

---

## 🌍 Ecosystem Importance

Right-to-Left (RTL) languages like Persian (Farsi), spoken by over **110 million people worldwide**, face systemic inefficiencies in modern AI infrastructure:

1. **Token Inefficiency & Disproportionate API Costs**: Generic BPE/WordPiece tokenizers (cl100k_base, Tiktoken, Llama) are heavily English-skewed. Persian text often requires **3× to 5× more tokens per word** than English, placing higher financial and latency burdens on Persian-speaking developers.
2. **Character & Unicode Fragmentation**: Widespread Arabic/Persian letter confusion (`ي` vs `ی`, `ك` vs `ک`), inconsistent Zero-Width Non-Joiner (ZWNJ / نیم‌فاصله) usage, and unnecessary diacritics fragment vocabulary embeddings and degrade LLM comprehension.
3. **The Open-Source Tooling Void**: Legacy libraries (Hazm, Parsivar) were built for classical statistical NLP and are not designed for LLM context windows, prompt compression, or modern async pipelines.

**Parstoken bridges this critical gap** by delivering a modern, high-throughput, zero-dependency preprocessor engineered specifically for LLM workflows and retrieval-augmented generation (RAG).

---

## ✨ Key Features

| Capability | Technical Mechanism | Impact on LLMs |
|---|---|---|
| 🔄 **Unicode & Script Normalization** | Converts Arabic variants (`ك`, `ي`, `ة`, `ۀ`) to standard Persian glyphs; applies canonical NFC normalization. | Prevents split subword tokens and ensures consistent embeddings. |
| 📏 **Smart ZWNJ Management** | Standardizes Zero-Width Non-Joiner (`\u200c`) around affixes (`می‌`, `ها`, `تر`) while removing orphaned ZWNJs. | Preserves compound word semantics without wasting tokens. |
| ⚡ **Repetition & Redundancy Compression** | Compresses elongated characters (e.g., `سلاااام` → `سلام`) and redundant punctuation (`؟؟؟` → `؟`). | **Cuts token usage by 15–50%** on informal and user-generated text. |
| ✂️ **Diacritics & Noise Stripping** | Removes Arabic short vowels (tashkeel/harakat) and unnecessary control characters. | Eliminates unnecessary tokens that carry zero prompt utility. |
| 🧹 **Production-Ready Sanitizer** | Configurable stripping of HTML/XML, URLs, emails, phone numbers, and social media artifacts. | Clean prompts for fine-tuning, RAG ingestion, and safety filters. |
| 🔢 **Bidirectional Digit Conversion** | Normalizes between Eastern Arabic (`١٢٣`), Persian (`۱۲۳`), and ASCII (`123`) digits. | Consistent numeric representation for function calling and extraction. |
| 📊 **Token Estimation & Metrics** | Real-time token savings calculations calibrated for GPT-4, Claude, and Gemini models. | Instant observability of cost and latency improvements. |
| ⚡ **Extreme Throughput** | Pure Python implementation with zero third-party dependencies processing **>24M chars/sec**. | Negligible overhead in high-throughput production pipelines. |

---

## 📦 Installation

```bash
pip install parstoken
```

For development and running tests locally:

```bash
git clone https://github.com/ilifield/parstoken.git
cd parstoken
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

### 1. One-Line Preprocessing Pipeline

```python
from parstoken import pipeline

# Raw text with Arabic letters, elongation, diacritics, and redundant spacing
raw_text = "سلاااام دوست من!   اين يك    تَستِ عاااالی است...   چطورییی؟؟؟"

result = pipeline(raw_text)

print(result.text)
# Output: سلام دوست من! این یک تست عالی است. چطوری؟

print(result.savings_summary)
# Output: Saved 12 tokens (38.7%) -- 31 -> 19
```

### 2. Unicode & Script Normalization

```python
from parstoken import PersianNormalizer

normalizer = PersianNormalizer(
    fix_arabic_chars=True,      # ك -> ک, ي -> ی, ة -> ه
    remove_diacritics=True,     # Remove tashkeel (َ ُ ِ ّ ْ)
    normalize_halfspace=True,   # Standardize ZWNJ (نیم‌فاصله)
    digit_target="fa"           # Convert English digits to Persian (123 -> ۱۲۳)
)

text = normalizer.normalize("كتاب هاي آموزشي شماره 123 با تخفيف ويژه")
print(text)
# Output: کتاب‌های آموزشی شماره ۱۲۳ با تخفیف ویژه
```

### 3. Token-Saving Compression

```python
from parstoken import TokenOptimizer

optimizer = TokenOptimizer(
    compress_repeated_chars=True,
    compress_repeated_punctuation=True,
    remove_redundant_spaces=True
)

result = optimizer.optimize("واقعاااااا دستت درد نکنهههه!!!!!   خیلییی خوب بوددددد")
print(result.text)
# Output: واقعا دستت درد نکنه! خیلی خوب بود

print(f"Characters saved: {result.chars_saved}")
print(f"Token reduction:  {result.savings_percentage:.1f}%")
```

---

## 🔗 LLM Pipeline Integrations

### OpenAI & LangChain Integration

```python
from langchain_core.documents import Document
from parstoken import PersianNormalizer, TokenOptimizer
import openai

normalizer = PersianNormalizer()
optimizer = TokenOptimizer()

def preprocess_persian_prompt(user_query: str) -> str:
    """Normalize and compress Persian text before sending to OpenAI."""
    normalized = normalizer.normalize(user_query)
    optimized = optimizer.optimize(normalized).text
    return optimized

# Example prompt
query = "لطفاااا درباره تاريخچه هوش مصنوعي توضيح بدهههه!"
optimized_query = preprocess_persian_prompt(query)

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant responding in Persian."},
        {"role": "user", "content": optimized_query}
    ]
)
```

### RAG & Hugging Face Dataset Ingestion

```python
from parstoken import pipeline

def clean_dataset_record(record: dict) -> dict:
    """Prepare Persian corpus for embedding or fine-tuning."""
    processed = pipeline(
        record["text"],
        normalize=True,
        clean=True,
        optimize=True
    )
    return {"text": processed.text, "tokens_saved": processed.tokens_saved}
```

---

## 💻 CLI Usage

Parstoken includes a comprehensive CLI suitable for batch processing, CI/CD data pipelines, and shell scripting:

```bash
# Normalize a file
parstoken normalize dataset.txt -o cleaned.txt

# Run full pipeline with token statistics
parstoken pipeline input.txt --normalize --clean --optimize --stats

# Filter social media noise
parstoken clean comments.txt --remove-emojis --remove-hashtags --remove-mentions

# Count and estimate tokens across models
parstoken count document.txt --model gpt-4o

# Pipe via standard input / Unix pipelines
cat corpus.txt | parstoken optimize --stats > optimized.txt
```

---

## 📈 Benchmarks

Tested on standard hardware across varying text structures:

| Module | Processing Throughput | Efficiency |
|---|---|---|
| **Text Normalizer** | **24.6M+ chars/sec** | Sub-millisecond on 100K-word files |
| **Noise Cleaner** | **28.6M+ chars/sec** | Regex-compiled single pass |
| **Token Optimizer** | **3.1M+ chars/sec** | 15–50% token reduction on chat data |
| **Full Pipeline** | **2.8M+ chars/sec** | Comprehensive end-to-end cleaning |

---

## 🛡️ Governance & Active Maintenance

Parstoken is an actively maintained open-source project adhering to strict community and engineering standards:

- **100% Test Coverage Strategy**: Comprehensive suite of **76 unit tests** validating Unicode mappings, boundary rules, diacritics stripping, and CLI operations across Python 3.8–3.13.
- **Cross-Platform Continuous Integration**: Automated GitHub Actions matrix testing on Ubuntu, macOS, and Windows.
- **Semantic Versioning & Release Cycles**: Stable releases following [SemVer](https://semver.org) with thorough [CHANGELOG](CHANGELOG.md) documentation.
- **Strict Issue Triage & PR Review SLA**:
  - Issue response within **48 hours**.
  - Standardized templates for bug reports and feature requests.
  - Required CI validation and code review before PR merge.

### Core Maintainer
- **Iliya Sharifi** ([@ilifield](https://github.com/ilifield)) — Primary Maintainer

---

## 🤝 Contributing

Contributions from the open-source community are warmly welcomed! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) guide before submitting a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/awesome-addition`)
3. Commit your Changes (`git commit -m 'feat: add enhanced affix normalization'`)
4. Verify Tests Pass (`pytest`)
5. Push to the Branch (`git push origin feature/awesome-addition`)
6. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<div align="center">
Built to empower the Persian-speaking NLP and AI developer ecosystem.
</div>
