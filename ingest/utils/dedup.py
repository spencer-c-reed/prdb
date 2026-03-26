#!/usr/bin/env python3
"""Deduplication utilities for document ingestion."""

import sqlite3


def db_connect(db_path: str, timeout: int = 120) -> sqlite3.Connection:
    """Create a connection with WAL mode and extended busy timeout."""
    conn = sqlite3.connect(db_path, timeout=timeout)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=120000')
    return conn


_connect = db_connect


def document_exists(db_path: str, md5_hash: str = None, citation: str = None) -> bool:
    """Check if a document already exists in the database."""
    conn = _connect(db_path)
    try:
        if md5_hash:
            row = conn.execute(
                'SELECT 1 FROM documents WHERE md5_hash = ? LIMIT 1',
                (md5_hash,)
            ).fetchone()
            if row:
                return True
        if citation:
            row = conn.execute(
                'SELECT 1 FROM documents WHERE citation = ? LIMIT 1',
                (citation,)
            ).fetchone()
            if row:
                return True
        return False
    finally:
        conn.close()


def get_document_count(db_path: str, source: str = None, document_type: str = None) -> int:
    """Count documents, optionally filtered by source or type."""
    conn = _connect(db_path)
    try:
        query = 'SELECT COUNT(*) FROM documents'
        params = []
        conditions = []
        if source:
            conditions.append('source = ?')
            params.append(source)
        if document_type:
            conditions.append('document_type = ?')
            params.append(document_type)
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        return conn.execute(query, params).fetchone()[0]
    finally:
        conn.close()


def insert_document(db_path: str, doc: dict) -> bool:
    """Insert a document if it does not already exist. Returns True if inserted or updated."""
    from .metadata import apply_metadata_defaults
    from .normalize import compute_hash

    normalized_doc = apply_metadata_defaults(doc)
    md5 = normalized_doc.get('md5_hash') or compute_hash(normalized_doc['text'])

    if document_exists(db_path, md5_hash=md5):
        return False

    # Check for citation match with different content (source was amended)
    citation = normalized_doc.get('citation')
    if citation:
        conn = _connect(db_path)
        try:
            row = conn.execute(
                'SELECT md5_hash FROM documents WHERE citation = ? LIMIT 1',
                (citation,),
            ).fetchone()
        finally:
            conn.close()
        if row:
            if row[0] == md5:
                return False
            import logging
            logging.getLogger(__name__).info(
                f'Source amendment detected for {citation}: hash changed, updating via upsert'
            )
            result = upsert_document(db_path, doc)
            return result in ('added', 'updated')

    conn = _connect(db_path)
    try:
        doc_id = normalized_doc.get('id', md5)
        conn.execute(
            '''
            INSERT INTO documents (
                id, citation, title, date, court, document_type,
                jurisdiction, source, source_url, text, summary, md5_hash,
                jurisdiction_level, authority_weight, precedent_strength
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                doc_id,
                normalized_doc.get('citation'),
                normalized_doc.get('title'),
                normalized_doc.get('date'),
                normalized_doc.get('court'),
                normalized_doc['document_type'],
                normalized_doc['jurisdiction'],
                normalized_doc['source'],
                normalized_doc.get('source_url'),
                normalized_doc['text'],
                normalized_doc.get('summary'),
                md5,
                normalized_doc.get('jurisdiction_level', 'federal'),
                normalized_doc.get('authority_weight', 50),
                normalized_doc.get('precedent_strength'),
            )
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def upsert_document(db_path: str, doc: dict, match_fields: tuple[str, ...] = ('citation', 'source_url', 'id')) -> str:
    """Insert or update a document. Returns added, updated, or skipped."""
    from .metadata import apply_metadata_defaults
    from .normalize import compute_hash

    normalized_doc = apply_metadata_defaults(doc)
    md5 = normalized_doc.get('md5_hash') or compute_hash(normalized_doc['text'])
    normalized_doc['md5_hash'] = md5

    conn = _connect(db_path)
    try:
        existing = None
        for field in match_fields:
            value = normalized_doc.get(field)
            if not value:
                continue
            row = conn.execute(
                f'SELECT rowid, id, md5_hash FROM documents WHERE {field} = ? LIMIT 1',
                (value,),
            ).fetchone()
            if row:
                existing = row
                break

        if existing is None:
            doc_id = normalized_doc.get('id', md5)
            conn.execute(
                '''
                INSERT INTO documents (
                    id, citation, title, date, court, document_type,
                    jurisdiction, source, source_url, text, summary, md5_hash,
                    jurisdiction_level, authority_weight, precedent_strength
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    doc_id,
                    normalized_doc.get('citation'),
                    normalized_doc.get('title'),
                    normalized_doc.get('date'),
                    normalized_doc.get('court'),
                    normalized_doc['document_type'],
                    normalized_doc['jurisdiction'],
                    normalized_doc['source'],
                    normalized_doc.get('source_url'),
                    normalized_doc['text'],
                    normalized_doc.get('summary'),
                    md5,
                    normalized_doc.get('jurisdiction_level', 'federal'),
                    normalized_doc.get('authority_weight', 50),
                    normalized_doc.get('precedent_strength'),
                )
            )
            conn.commit()
            return 'added'

        if existing[2] == md5:
            return 'skipped'

        # Content changed — full update, clear AI summaries
        conn.execute(
            '''
            UPDATE documents
            SET citation = ?,
                title = ?,
                date = ?,
                court = ?,
                document_type = ?,
                jurisdiction = ?,
                source = ?,
                source_url = ?,
                text = ?,
                summary = ?,
                md5_hash = ?,
                summary_ai = NULL,
                topics = NULL,
                holdings = NULL,
                summarized_at = NULL,
                cited_authorities = NULL,
                summary_model = NULL,
                summary_brief = NULL,
                jurisdiction_level = ?,
                authority_weight = ?,
                precedent_strength = ?,
                updated_at = datetime('now')
            WHERE rowid = ?
            ''',
            (
                normalized_doc.get('citation'),
                normalized_doc.get('title'),
                normalized_doc.get('date'),
                normalized_doc.get('court'),
                normalized_doc['document_type'],
                normalized_doc['jurisdiction'],
                normalized_doc['source'],
                normalized_doc.get('source_url'),
                normalized_doc['text'],
                normalized_doc.get('summary'),
                md5,
                normalized_doc.get('jurisdiction_level', 'federal'),
                normalized_doc.get('authority_weight', 50),
                normalized_doc.get('precedent_strength'),
                existing[0],
            ),
        )
        conn.commit()
        return 'updated'
    finally:
        conn.close()


def log_ingestion(db_path: str, source: str, added: int, skipped: int, errors: int, notes: str = None):
    """Log an ingestion run."""
    conn = _connect(db_path)
    try:
        conn.execute(
            '''
            INSERT INTO ingestion_log (source, documents_added, documents_skipped, errors, notes)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (source, added, skipped, errors, notes)
        )
        conn.commit()
    finally:
        conn.close()
