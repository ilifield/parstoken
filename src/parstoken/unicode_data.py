"""Persian and Arabic Unicode character mappings and constants."""

# Arabic characters that should be replaced with Persian equivalents
ARABIC_TO_PERSIAN_MAP = {
    '\u0643': '\u06A9',  # ك → ک
    '\u064A': '\u06CC',  # ي → ی
    '\u0629': '\u0647',  # ة → ه
    '\u0649': '\u06CC',  # ى → ی
    '\u06C0': '\u0647\u0654',  # ۀ → هٔ
    '\u0624': '\u0648\u0654',  # ؤ → ؤ
}

# Arabic diacritical marks (tashkeel/harakat)
ARABIC_DIACRITICS = {
    '\u064B',  # Fathatan ً
    '\u064C',  # Dammatan ٌ
    '\u064D',  # Kasratan ٍ
    '\u064E',  # Fatha َ
    '\u064F',  # Damma ُ
    '\u0650',  # Kasra ِ
    '\u0651',  # Shadda ّ
    '\u0652',  # Sukun ْ
    '\u0653',  # Maddah ٓ
    '\u0654',  # Hamza Above ٔ
    '\u0655',  # Hamza Below ٕ
    '\u0670',  # Superscript Alef ٰ
}

# Persian digits to English digits mapping
PERSIAN_TO_ENGLISH_DIGITS = {
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
}

# English digits to Persian digits mapping
ENGLISH_TO_PERSIAN_DIGITS = {v: k for k, v in PERSIAN_TO_ENGLISH_DIGITS.items()}

# Arabic digits to Persian digits mapping
ARABIC_TO_PERSIAN_DIGITS = {
    '٠': '۰', '١': '۱', '٢': '۲', '٣': '۳', '٤': '۴',
    '٥': '۵', '٦': '۶', '٧': '۷', '٨': '۸', '٩': '۹',
}

# Arabic punctuation to standard punctuation
ARABIC_PUNCTUATION_MAP = {
    '٪': '%',       # Arabic percent
    '٫': '.',       # Arabic decimal separator
    '٬': ',',       # Arabic thousands separator
    '؟': '?',       # Arabic question mark
    '؛': ';',       # Arabic semicolon
    '٭': '*',       # Arabic five pointed star
}

# Zero-Width Non-Joiner (half-space)
ZWNJ = '\u200c'

# Zero-Width Joiner
ZWJ = '\u200d'

# Various space characters to normalize
SPACE_CHARS = {
    '\u00A0',  # Non-breaking space
    '\u2000',  # En quad
    '\u2001',  # Em quad
    '\u2002',  # En space
    '\u2003',  # Em space
    '\u2004',  # Three-per-em space
    '\u2005',  # Four-per-em space
    '\u2006',  # Six-per-em space
    '\u2007',  # Figure space
    '\u2008',  # Punctuation space
    '\u2009',  # Thin space
    '\u200A',  # Hair space
    '\u200B',  # Zero-width space
    '\u202F',  # Narrow no-break space
    '\u205F',  # Medium mathematical space
    '\u3000',  # Ideographic space
    '\uFEFF',  # Zero-width no-break space (BOM)
}

# Common Persian suffixes that should be connected with ZWNJ
PERSIAN_ZWNJ_SUFFIXES = [
    'ها', 'های', 'هایی', 'تر', 'ترین', 'گر', 'ای', 'ام', 'ات',
    'اش', 'مان', 'تان', 'شان',
]

# Common Persian prefixes that should be connected with ZWNJ  
PERSIAN_ZWNJ_PREFIXES = [
    'می', 'نمی', 'بر', 'در', 'بی',
]

# Persian sentence ending characters
SENTENCE_ENDINGS = {'.', '!', '?', '؟', '!', '۔'}

# Characters that Persian words can contain
PERSIAN_CHARS = set(
    'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ'
    'ؤإأءًٌٍَُِّْ'
)
