"""
Core semantic prompt and context compression engine.
"""

import re
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class CompressionStats:
    original_chars: int
    compressed_chars: int
    char_reduction_pct: float
    est_original_tokens: int
    est_compressed_tokens: int
    tokens_saved: int
    elapsed_ms: float

class TokenCompressor:
    """
    Ultra-fast semantic prompt compression engine.
    Slashes context token burn by removing conversational filler,
    redundant whitespace, boilerplate, and low-information syntactic structures.
    """

    # Low-information conversational boilerplate patterns
    FILLER_PATTERNS = [
        re.compile(r"(?i)\b(?:as an ai(?: language model)?|i am an ai)\b[,.!]?", re.IGNORECASE),
        re.compile(r"(?i)\b(?:certainly|sure|absolutely)\b[!.,]?", re.IGNORECASE),
        re.compile(r"(?i)\b(?:i can help with that|here is the information you requested|here is what you asked for):?", re.IGNORECASE),
        re.compile(r"(?i)\b(?:i hope this helps|let me know if you need anything else|feel free to ask)\b[!.,]?", re.IGNORECASE),
    ]

    REPLACEMENT_MAP = [
        (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
        (re.compile(r"\bdue to the fact that\b", re.IGNORECASE), "because"),
        (re.compile(r"\bfor the purpose of\b", re.IGNORECASE), "to"),
        (re.compile(r"\bat this point in time\b", re.IGNORECASE), "now"),
        (re.compile(r"\bplease note that\b", re.IGNORECASE), "note:"),
        (re.compile(r"\bit is important to remember that\b", re.IGNORECASE), "note:"),
        (re.compile(r"\bkeep in mind that\b", re.IGNORECASE), "note:"),
    ]

    def __init__(self, aggressive: bool = False):
        self.aggressive = aggressive

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, math.ceil(len(text) / 4.0))

    def compress_text(self, text: str) -> Tuple[str, CompressionStats]:
        import time
        t_start = time.perf_counter()

        orig_len = len(text)
        orig_tokens = self.estimate_tokens(text)

        # 1. Normalize line endings
        cleaned = text.replace("\r\n", "\n").replace("\t", " ")

        # 2. Strip conversational filler
        for pat in self.FILLER_PATTERNS:
            cleaned = pat.sub("", cleaned)

        # 3. Simplify verbose phrases
        for pat, replacement in self.REPLACEMENT_MAP:
            cleaned = pat.sub(replacement, cleaned)

        # 4. Clean orphaned punctuation colons/commas at line starts
        cleaned = re.sub(r"^\s*[:;,]\s*", "", cleaned, flags=re.MULTILINE)

        # 5. Collapse repeated horizontal whitespace
        cleaned = re.sub(r"[ ]{2,}", " ", cleaned)

        # 6. Collapse repeated newlines
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

        # 7. Aggressive mode
        if self.aggressive:
            cleaned = re.sub(r"^[ \t]*[-*_]{3,}[ \t]*$", "", cleaned, flags=re.MULTILINE)
            cleaned = re.sub(r"\n{2,}", "\n", cleaned)

        cleaned = cleaned.strip()
        comp_len = len(cleaned)
        comp_tokens = self.estimate_tokens(cleaned)
        saved = max(0, orig_tokens - comp_tokens)
        pct = ((orig_len - comp_len) / orig_len * 100.0) if orig_len > 0 else 0.0

        t_elapsed = (time.perf_counter() - t_start) * 1000.0

        stats = CompressionStats(
            original_chars=orig_len,
            compressed_chars=comp_len,
            char_reduction_pct=pct,
            est_original_tokens=orig_tokens,
            est_compressed_tokens=comp_tokens,
            tokens_saved=saved,
            elapsed_ms=t_elapsed
        )
        return cleaned, stats
