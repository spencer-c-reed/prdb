#!/usr/bin/env python3
"""Text normalization utilities for public records documents."""

import re
import hashlib
import unicodedata


def normalize_text(text: str) -> str:
    """Clean and normalize document text."""
    if not text:
        return ""
    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)
    # Collapse multiple whitespace (preserve paragraph breaks)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    return text.strip()


def compute_hash(text: str) -> str:
    """Compute MD5 hash of normalized text for dedup."""
    normalized = re.sub(r'\s+', ' ', text.lower().strip())
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


def normalize_citation(citation: str) -> str:
    """Normalize a legal citation to standard form."""
    if not citation:
        return ""
    SECTION = '\u00a7'  # section sign
    # Normalize U.S. Code citations
    citation = re.sub(r'(\d+)\s+U\.?S\.?C\.?\s*(?:\u00a7|sec\.?|section)\s*(\d+)',
                       r'\1 U.S.C. ' + SECTION + r' \2', citation, flags=re.IGNORECASE)
    # Normalize CFR citations
    citation = re.sub(r'(\d+)\s+C\.?F\.?R\.?\s*(?:\u00a7|sec\.?)?\s*(\d+\.\d+)',
                       r'\1 C.F.R. ' + SECTION + r' \2', citation, flags=re.IGNORECASE)
    # Normalize state code citations (common patterns)
    # "Gov. Code sec. 6253" -> "Gov. Code § 6253"
    citation = re.sub(r'((?:Gov|Pub|Gen|Admin|Exec|Civ|Pen|Elec|Bus|Corp|Educ|Health|Lab|Welf)\.\s*(?:Off\.\s*)?(?:Code|Law|Stat)\.?)\s*(?:sec\.?|section)\s*',
                       r'\1 ' + SECTION + r' ', citation, flags=re.IGNORECASE)
    return citation.strip()


def extract_date(text: str):
    """Extract a date from text, return ISO format or None."""
    import datetime
    patterns = [
        (r'(\d{4})-(\d{2})-(\d{2})', r'\1-\2-\3'),  # ISO
        (r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', None),     # "January 15, 2024"
        (r'(\d{1,2})/(\d{1,2})/(\d{4})', None),        # "1/15/2024"
    ]
    for pattern, replacement in patterns:
        match = re.search(pattern, text)
        if match:
            if replacement:
                return match.expand(replacement)
            try:
                date_str = match.group(0)
                for fmt in ('%B %d, %Y', '%B %d %Y', '%m/%d/%Y'):
                    try:
                        dt = datetime.datetime.strptime(date_str, fmt)
                        return dt.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            except Exception:
                pass
    return None
