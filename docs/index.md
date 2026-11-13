# Parstoken Documentation

Welcome to the Parstoken documentation. Parstoken is a zero-dependency Python
library for Persian text preprocessing and LLM token optimization.

## Overview

Parstoken provides four core modules:

1. **Normalizer** — Unicode normalization, Arabic→Persian conversion, ZWNJ handling
2. **Cleaner** — Remove HTML, URLs, emails, emojis, and other noise
3. **Optimizer** — Compress text to reduce LLM token consumption
4. **Tokenizer** — Persian-aware word and sentence tokenization

## Installation

```bash
pip install parstoken
```

## Quick Example

```python
from parstoken import pipeline

result = pipeline("سلاااام!!!   اين يك    تست است...")
print(result.text)            # سلام! این یک تست است.
print(result.savings_summary) # Saved 8 tokens (32.0%) — 25 → 17
```

For detailed API documentation, see the [README](https://github.com/ilifield/parstoken).
