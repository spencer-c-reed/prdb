#!/usr/bin/env python3
"""Scaffolding smoke tests for PRDB.

Run: python3 -m pytest tests/test_scaffolding.py -v
"""

import json
import os
import sqlite3
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'prdb.db')


class TestDatabase:
    def test_schema_version(self):
        conn = sqlite3.connect(DB_PATH)
        version = conn.execute('SELECT version FROM schema_version ORDER BY version DESC LIMIT 1').fetchone()[0]
        conn.close()
        assert version == 1

    def test_core_tables_exist(self):
        conn = sqlite3.connect(DB_PATH)
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()]
        conn.close()

        expected = [
            'documents', 'exemptions', 'agencies', 'response_rules',
            'request_templates', 'campaigns', 'requests', 'request_events',
            'response_documents', 'document_citations', 'authority_aliases',
            'supersession_edges', 'extracted_citations', 'authority_status',
            'ingestion_log', 'schema_version',
        ]
        for t in expected:
            assert t in tables, f'Missing table: {t}'

    def test_fts_table_exists(self):
        conn = sqlite3.connect(DB_PATH)
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%fts%'"
        ).fetchall()]
        conn.close()
        assert 'documents_fts' in tables


class TestNormalize:
    def test_normalize_text(self):
        from ingest.utils.normalize import normalize_text
        assert normalize_text('  hello   world  ') == 'hello world'
        assert normalize_text('') == ''
        assert normalize_text(None) == ''

    def test_compute_hash(self):
        from ingest.utils.normalize import compute_hash
        assert compute_hash('test') == compute_hash('  TEST  ')
        assert compute_hash('a') != compute_hash('b')

    def test_normalize_citation(self):
        from ingest.utils.normalize import normalize_citation
        result = normalize_citation('5 USC sec 552')
        assert '§' in result
        assert 'U.S.C.' in result


class TestMetadata:
    def test_federal_defaults(self):
        from ingest.utils.metadata import apply_metadata_defaults
        doc = {
            'document_type': 'Federal FOIA Statute',
            'jurisdiction': 'federal',
            'text': 'test',
            'source': 'test',
        }
        result = apply_metadata_defaults(doc)
        assert result['authority_weight'] == 100
        assert result['precedent_strength'] == 'settled'
        assert result['jurisdiction_level'] == 'federal'

    def test_state_inference(self):
        from ingest.utils.metadata import apply_metadata_defaults
        doc = {
            'document_type': 'State Public Records Statute',
            'jurisdiction': 'NY',
            'text': 'test',
            'source': 'test',
        }
        result = apply_metadata_defaults(doc)
        assert result['jurisdiction_level'] == 'state'
        assert result['authority_weight'] == 95

    def test_null_byte_stripping(self):
        from ingest.utils.metadata import apply_metadata_defaults
        doc = {
            'document_type': 'Federal FOIA Statute',
            'jurisdiction': 'federal',
            'text': 'hello\x00world',
            'source': 'test',
        }
        result = apply_metadata_defaults(doc)
        assert '\x00' not in result['text']


class TestDedup:
    def test_insert_and_dedup(self):
        from ingest.utils.dedup import insert_document, get_document_count
        doc = {
            'id': 'pytest-001',
            'citation': 'Pytest Citation 1',
            'title': 'Test Document',
            'document_type': 'Federal FOIA Statute',
            'jurisdiction': 'federal',
            'source': 'pytest',
            'text': 'Unique test content for pytest dedup test.',
        }
        # Insert
        assert insert_document(DB_PATH, doc) == True
        # Dedup
        assert insert_document(DB_PATH, doc) == False
        # Cleanup
        conn = sqlite3.connect(DB_PATH)
        conn.execute('DELETE FROM documents WHERE id = ?', ('pytest-001',))
        conn.commit()
        conn.close()


class TestQueryEngine:
    def _setup_test_docs(self):
        from ingest.utils.dedup import insert_document
        docs = [
            {
                'id': 'pytest-search-001',
                'citation': '5 U.S.C. § 552',
                'title': 'Freedom of Information Act',
                'document_type': 'Federal FOIA Statute',
                'jurisdiction': 'federal',
                'source': 'pytest',
                'text': 'Each agency shall make available public records.',
                'date': '1966-07-04',
            },
            {
                'id': 'pytest-search-002',
                'citation': 'NY FOIL § 87',
                'title': 'New York Freedom of Information Law',
                'document_type': 'State Public Records Statute',
                'jurisdiction': 'NY',
                'source': 'pytest',
                'text': 'Each agency shall make available for public inspection all records.',
                'date': '1977-01-01',
            },
        ]
        for doc in docs:
            insert_document(DB_PATH, doc)
        return docs

    def _teardown_test_docs(self, docs):
        conn = sqlite3.connect(DB_PATH)
        for doc in docs:
            conn.execute('DELETE FROM documents WHERE id = ?', (doc['id'],))
        conn.commit()
        conn.execute('INSERT INTO documents_fts(documents_fts) VALUES("rebuild")')
        conn.commit()
        conn.close()

    def test_basic_search(self):
        docs = self._setup_test_docs()
        try:
            from fetch_json import search
            results = search('freedom of information', limit=10)
            assert len(results) >= 1
            assert any(r['id'] == 'pytest-search-001' for r in results)
        finally:
            self._teardown_test_docs(docs)

    def test_jurisdiction_filter(self):
        docs = self._setup_test_docs()
        try:
            from fetch_json import search
            results = search('Jurisdiction:"NY"', limit=10)
            assert all(r['jurisdiction'] == 'NY' for r in results)
        finally:
            self._teardown_test_docs(docs)

    def test_type_filter(self):
        docs = self._setup_test_docs()
        try:
            from fetch_json import search
            results = search('Type:"Federal FOIA Statute"', limit=10)
            assert all(r['document_type'] == 'Federal FOIA Statute' for r in results)
        finally:
            self._teardown_test_docs(docs)

    def test_stats(self):
        from fetch_json import get_stats
        stats = get_stats()
        assert 'total_documents' in stats
        assert 'exemptions' in stats
        assert 'agencies' in stats


class TestFlask:
    def _get_client(self):
        from app import app
        app.config['TESTING'] = True
        return app.test_client()

    def test_health(self):
        client = self._get_client()
        resp = client.get('/health')
        assert resp.status_code == 200
        assert resp.json['status'] == 'ok'

    def test_index(self):
        client = self._get_client()
        resp = client.get('/')
        assert resp.status_code == 200

    def test_search(self):
        client = self._get_client()
        resp = client.get('/search')
        assert resp.status_code == 200

    def test_jurisdictions(self):
        client = self._get_client()
        resp = client.get('/jurisdictions')
        assert resp.status_code == 200

    def test_exemptions(self):
        client = self._get_client()
        resp = client.get('/exemptions')
        assert resp.status_code == 200

    def test_agencies(self):
        client = self._get_client()
        resp = client.get('/agencies')
        assert resp.status_code == 200

    def test_templates(self):
        client = self._get_client()
        resp = client.get('/templates')
        assert resp.status_code == 200

    def test_404(self):
        client = self._get_client()
        resp = client.get('/document/nonexistent')
        assert resp.status_code == 404

    def test_api_stats(self):
        client = self._get_client()
        resp = client.get('/api/stats')
        assert resp.status_code == 200
        assert 'total_documents' in resp.json
