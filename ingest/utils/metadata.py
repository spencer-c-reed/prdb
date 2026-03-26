#!/usr/bin/env python3
"""Metadata normalization utilities for public records documents."""

import re
from typing import Any, Dict

_STATE_CODE_RE = re.compile(r'^[A-Z]{2}$')

# Legacy aliases observed in ingests
_DOC_TYPE_ALIASES = {
    'Attorney General Opinion': 'AG Opinion - Public Records',
    'AG Opinion': 'AG Opinion - Public Records',
    'FOIA Statute': 'Federal FOIA Statute',
    'Public Records Statute': 'State Public Records Statute',
    'FOIA Regulation': 'Federal FOIA Regulation',
}

# Canonical authority defaults
_DEFAULT_AUTHORITY_WEIGHTS = {
    # Federal FOIA
    'Federal FOIA Statute': 100,
    'Federal FOIA Regulation': 85,
    'OGIS Advisory Opinion': 70,
    'DOJ OIP Guidance': 65,
    # State public records
    'State Public Records Statute': 95,
    'State Public Records Regulation': 80,
    'AG Opinion - Public Records': 75,
    'AG Guidance - Public Records': 65,
    # Court opinions
    'Federal Court Opinion': 80,
    'Supreme Court Opinion': 100,
    'Circuit Court Opinion': 80,
    'District Court Opinion': 50,
    'State Court Opinion': 70,
    'State Supreme Court Opinion': 75,
    'State Appellate Court Opinion': 60,
    # Agency materials
    'Agency FOIA Handbook': 40,
    'Agency FOIA Report': 35,
    'FOIA Annual Report': 30,
    # Reference
    'Fee Schedule': 50,
    'Request Template': 30,
    'Practitioner Guide': 25,
    'Legislative History': 30,
    'Academic Analysis': 20,
    # Open meetings
    'Open Meetings Statute': 90,
    'Open Meetings Regulation': 75,
    'Open Meetings Opinion': 65,
}

_DEFAULT_PRECEDENT_STRENGTHS = {
    'Federal FOIA Statute': 'settled',
    'State Public Records Statute': 'settled',
    'Federal FOIA Regulation': 'settled',
    'State Public Records Regulation': 'settled',
    'Open Meetings Statute': 'settled',
    'Open Meetings Regulation': 'settled',
    'Supreme Court Opinion': 'settled',
    'Federal Court Opinion': 'established',
    'Circuit Court Opinion': 'established',
    'District Court Opinion': 'established',
    'State Court Opinion': 'established',
    'State Supreme Court Opinion': 'established',
    'State Appellate Court Opinion': 'established',
    'AG Opinion - Public Records': 'established',
    'OGIS Advisory Opinion': 'established',
    'Open Meetings Opinion': 'established',
    'DOJ OIP Guidance': 'guidance',
    'AG Guidance - Public Records': 'guidance',
    'Agency FOIA Handbook': 'guidance',
    'Agency FOIA Report': 'guidance',
    'FOIA Annual Report': 'guidance',
    'Fee Schedule': 'guidance',
    'Request Template': 'guidance',
    'Practitioner Guide': 'guidance',
    'Legislative History': 'guidance',
    'Academic Analysis': 'guidance',
}


def _normalize_jurisdiction(value: Any) -> str:
    if value is None:
        return 'federal'

    text = str(value).strip()
    if not text:
        return 'federal'

    low = text.lower()
    if low == 'federal':
        return 'federal'
    if low == 'multi-state':
        return 'multi-state'
    if text.upper() == 'US':
        return 'US'
    if _STATE_CODE_RE.match(text.upper()):
        return text.upper()
    return text


def _infer_level(jurisdiction: str, doc_type: str, provided_level: Any) -> str:
    if provided_level is not None:
        level = str(provided_level).strip().lower()
        if level in {'federal', 'state', 'county', 'city'}:
            return level

    if doc_type.startswith('Municipal '):
        return 'city'

    if jurisdiction in {'federal', 'US', 'multi-state'}:
        return 'federal'

    if _STATE_CODE_RE.match(jurisdiction):
        return 'state'

    return 'federal'


def _canonical_type(doc_type: Any, jurisdiction: str, jurisdiction_level: str) -> str:
    doc_type_text = str(doc_type or '').strip()
    canonical = _DOC_TYPE_ALIASES.get(doc_type_text, doc_type_text)
    return canonical


def _normalize_authority(weight: Any, doc_type: str) -> int:
    if weight is not None:
        try:
            return int(weight)
        except (TypeError, ValueError):
            pass
    return _DEFAULT_AUTHORITY_WEIGHTS.get(doc_type, 50)


def _normalize_precedent_strength(value: Any, doc_type: str) -> str:
    if value is not None:
        text = str(value).strip().lower()
        if text in {'settled', 'established', 'guidance'}:
            return text
    return _DEFAULT_PRECEDENT_STRENGTHS.get(doc_type, '')


def apply_metadata_defaults(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of doc with canonical type/level/authority defaults."""
    normalized = dict(doc)

    jurisdiction = _normalize_jurisdiction(normalized.get('jurisdiction'))
    normalized['jurisdiction'] = jurisdiction

    level = _infer_level(
        jurisdiction,
        str(normalized.get('document_type') or ''),
        normalized.get('jurisdiction_level'),
    )
    doc_type = _canonical_type(normalized.get('document_type'), jurisdiction, level)

    # Final guardrails after canonicalization
    if doc_type.startswith('Municipal ') and level not in {'city', 'county'}:
        level = 'city'
    if doc_type.startswith('State ') and _STATE_CODE_RE.match(jurisdiction) and level == 'federal':
        level = 'state'

    normalized['document_type'] = doc_type
    normalized['jurisdiction_level'] = level
    normalized['authority_weight'] = _normalize_authority(normalized.get('authority_weight'), doc_type)
    normalized['precedent_strength'] = _normalize_precedent_strength(
        normalized.get('precedent_strength'),
        doc_type,
    )

    # Strip null bytes from text fields (null bytes truncate SQLite FTS5 indexing)
    for field in ('text', 'summary', 'title', 'citation'):
        if field in normalized and isinstance(normalized[field], str):
            normalized[field] = normalized[field].replace('\x00', ' ')

    return normalized
