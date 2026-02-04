import re
from typing import Dict, List

"""
Utilities for morphological normalization of column names.
This module extracts structural and semantic components
without performing domain-specific interpretation."""

def _clean_column_name(name: str) -> str:
    """
    Remove non-alphabetic characters and normalize to uppercase.
    """
    return re.sub(r"[^A-Z_]", "", name.upper())


def _tokenize(name: str) -> List[str]:
    """
    Split a cleaned column name into tokens.
    """
    return [t for t in name.split("_") if t]


def normalize_column_name(column_name: str) -> Dict:
    """
    Decompose a column name into structural and semantic components.

    Robust rules for SINAN-like datasets:
    - Structural prefixes are ONLY well-known administrative markers
      (DT, NU, ID, CS, TP, SG).
    - Structural suffixes are single-letter tokens at the end (N, I, H, V).
    - All remaining tokens are semantic, including short clinical abbreviations.
    """

    original = column_name
    cleaned = _clean_column_name(column_name)
    tokens = _tokenize(cleaned)

    structural_tokens: List[str] = []
    semantic_tokens: List[str] = []

    if not tokens:
        return {
            "original": original,
            "cleaned": cleaned,
            "raw_tokens": [],
            "semantic_tokens": [],
            "structural_tokens": [],
            "base_name": "",
        }

    # --- Handle suffixes (_N, _I, _H, _V)
    if len(tokens[-1]) == 1:
        structural_tokens.append(tokens.pop())

    # --- Handle prefixes (administrative only)
    ADMIN_PREFIXES = {"DT", "NU", "ID", "CS", "TP", "SG", "NM", "DS"}

    if len(tokens) > 1 and tokens[0] in ADMIN_PREFIXES:
        structural_tokens.append(tokens.pop(0))

    # --- Everything else is semantic
    semantic_tokens = tokens

    base_name = "_".join(semantic_tokens)

    return {
        "original": original,
        "cleaned": cleaned,
        "raw_tokens": semantic_tokens + structural_tokens,
        "semantic_tokens": semantic_tokens,
        "structural_tokens": structural_tokens,
        "base_name": base_name,
    }