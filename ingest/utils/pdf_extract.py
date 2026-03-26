#!/usr/bin/env python3
"""PDF text extraction with OCR fallback for scanned/low-quality PDFs."""

import logging
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

import fitz  # pymupdf

logger = logging.getLogger(__name__)

MIN_CHARS_PER_PAGE = int(os.getenv('OCR_MIN_CHARS_PER_PAGE', '50'))
OCR_DPI = int(os.getenv('OCR_DPI', '400'))
OCR_TIMEOUT_SEC = int(os.getenv('OCR_TIMEOUT_SEC', '180'))
OCR_LANG = os.getenv('OCR_LANG', 'eng')
TESSERACT_CMD = os.getenv('TESSERACT_CMD', 'tesseract')
MAX_OCR_PAGES = int(os.getenv('OCR_MAX_PAGES', '350'))


def _alpha_ratio(text: str) -> float:
    if not text:
        return 0.0
    letters = sum(1 for ch in text if ch.isalpha())
    return letters / max(1, len(text))


def _needs_ocr(text: str, page_count: int) -> bool:
    if page_count <= 0:
        return False
    stripped = (text or '').strip()
    if not stripped:
        return True
    chars_per_page = len(stripped) / page_count
    if chars_per_page < MIN_CHARS_PER_PAGE:
        return True
    if len(stripped) < 2500 and _alpha_ratio(stripped) < 0.45:
        return True
    return False


def _ocr_pdf_with_fitz(pdf_bytes: bytes) -> str:
    """OCR via PyMuPDF rendering + Tesseract."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype='pdf')
        limit = min(len(doc), MAX_OCR_PAGES)
        text_parts = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for i in range(limit):
                page = doc[i]
                img_path = os.path.join(tmpdir, f'page_{i}.png')
                pix = page.get_pixmap(dpi=OCR_DPI, colorspace=fitz.csGRAY, alpha=False)
                pix.save(img_path)
                try:
                    result = subprocess.run(
                        [TESSERACT_CMD, img_path, 'stdout', '-l', OCR_LANG,
                         '--oem', '1', '--psm', '6'],
                        capture_output=True, timeout=OCR_TIMEOUT_SEC,
                    )
                    if result.returncode == 0:
                        text_parts.append(result.stdout.decode('utf-8', errors='ignore'))
                except (subprocess.TimeoutExpired, Exception) as exc:
                    logger.warning('OCR failed for page %s: %s', i, exc)
        doc.close()
        return '\n'.join(text_parts)
    except Exception as exc:
        logger.warning('fitz OCR fallback failed: %s', exc)
        return ''


def extract_text_from_pdf(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as fh:
        return extract_text_from_bytes(fh.read())


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    page_count = len(doc)
    native_text = '\n'.join(page.get_text() for page in doc)
    doc.close()

    if not _needs_ocr(native_text, page_count):
        return native_text

    logger.info('Low native extraction (%s chars / %s pages), trying OCR',
                len((native_text or '').strip()), page_count)
    ocr_text = _ocr_pdf_with_fitz(pdf_bytes)

    # Return whichever is better
    if len((ocr_text or '').strip()) > len((native_text or '').strip()) * 1.2:
        return ocr_text
    return native_text
