#!/usr/bin/env python3
"""PRDB — Public Records Request Database & Assistant

Flask web application serving the research corpus and API.
Placeholder name "prdb" — will be replaced with final project name.
"""

import json
import os
import secrets
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request, jsonify, abort, Response

# Configuration
# All env vars use PRDB_ prefix — easy to find-and-replace to final name
DB_PATH = os.environ.get('PRDB_DB_PATH',
                          str(Path(__file__).resolve().parent / 'db' / 'prdb.db'))
SECRET_KEY = os.environ.get('PRDB_SECRET_KEY', secrets.token_hex(32))
API_KEYS = [k.strip() for k in os.environ.get('PRDB_API_KEYS', '').split(',') if k.strip()]
BASE_URL = os.environ.get('PRDB_BASE_URL', 'http://localhost:8402')
PORT = int(os.environ.get('PRDB_PORT', 8402))

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    """Read-only database connection."""
    try:
        conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True, timeout=30)
        conn.execute('PRAGMA schema_version').fetchone()
    except sqlite3.OperationalError:
        conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro&immutable=1', uri=True, timeout=30)
    conn.execute('PRAGMA query_only = ON')
    conn.row_factory = sqlite3.Row
    return conn


def get_stats():
    """Corpus statistics for landing page."""
    conn = get_db()
    try:
        total = conn.execute('SELECT COUNT(*) FROM documents WHERE parent_id IS NULL').fetchone()[0]
        by_type = conn.execute(
            'SELECT document_type, COUNT(*) as cnt FROM documents WHERE parent_id IS NULL '
            'GROUP BY document_type ORDER BY cnt DESC'
        ).fetchall()
        by_jurisdiction = conn.execute(
            'SELECT jurisdiction, COUNT(*) as cnt FROM documents WHERE parent_id IS NULL '
            'GROUP BY jurisdiction ORDER BY cnt DESC LIMIT 20'
        ).fetchall()
        exemptions = conn.execute('SELECT COUNT(*) FROM exemptions').fetchone()[0]
        agencies = conn.execute('SELECT COUNT(*) FROM agencies WHERE is_active = 1').fetchone()[0]
        templates = conn.execute('SELECT COUNT(*) FROM request_templates').fetchone()[0]
        return {
            'total': total,
            'by_type': [(row[0], row[1]) for row in by_type],
            'by_jurisdiction': [(row[0], row[1]) for row in by_jurisdiction],
            'exemptions': exemptions,
            'agencies': agencies,
            'templates': templates,
        }
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response


# ---------------------------------------------------------------------------
# Template filters
# ---------------------------------------------------------------------------

@app.template_filter('filesize')
def filesize_filter(size):
    if not size:
        return '0 B'
    for unit in ('B', 'KB', 'MB', 'GB'):
        if abs(size) < 1024:
            return f'{size:.1f} {unit}'
        size /= 1024
    return f'{size:.1f} TB'


# ---------------------------------------------------------------------------
# Routes — HTML pages
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    stats = get_stats()
    return render_template('index.html', stats=stats)


@app.route('/search')
def search_page():
    query = request.args.get('q', '').strip()
    doc_type = request.args.get('type', '').strip()
    jurisdiction = request.args.get('jurisdiction', '').strip()
    page = max(1, request.args.get('page', 1, type=int))
    per_page = 20

    if not query and not doc_type and not jurisdiction:
        return render_template('search.html', results=[], query='', facets={},
                             page=1, total=0, per_page=per_page)

    # Build search query with filters
    search_query = query
    if doc_type:
        search_query += f' Type:"{doc_type}"'
    if jurisdiction:
        search_query += f' Jurisdiction:"{jurisdiction}"'

    from fetch_json import search as do_search
    all_results = do_search(search_query, limit=500, brief=True)

    # Compute facets from full result set
    type_facets = {}
    jurisdiction_facets = {}
    for r in all_results:
        dt = r.get('document_type', 'Unknown')
        type_facets[dt] = type_facets.get(dt, 0) + 1
        jur = r.get('jurisdiction', 'Unknown')
        jurisdiction_facets[jur] = jurisdiction_facets.get(jur, 0) + 1

    facets = {
        'type': sorted(type_facets.items(), key=lambda x: -x[1]),
        'jurisdiction': sorted(jurisdiction_facets.items(), key=lambda x: -x[1]),
    }

    # Paginate
    total = len(all_results)
    start = (page - 1) * per_page
    results = all_results[start:start + per_page]

    return render_template('search.html', results=results, query=query,
                         facets=facets, page=page, total=total,
                         per_page=per_page, doc_type=doc_type,
                         jurisdiction=jurisdiction)


@app.route('/document/<doc_id>')
def document_page(doc_id):
    conn = get_db()
    try:
        doc = conn.execute('SELECT * FROM documents WHERE id = ?', (doc_id,)).fetchone()
        if not doc:
            abort(404)

        doc = dict(doc)

        # Get citing documents
        citing = conn.execute(
            '''
            SELECT d.id, d.citation, d.title, d.date, d.document_type
            FROM document_citations dc
            JOIN documents d ON d.id = dc.source_doc_id
            WHERE dc.target_doc_id = ?
            ORDER BY d.date DESC
            LIMIT 20
            ''',
            (doc_id,)
        ).fetchall()

        # Get cited documents
        cited = conn.execute(
            '''
            SELECT d.id, d.citation, d.title, d.date, d.document_type
            FROM document_citations dc
            JOIN documents d ON d.id = dc.target_doc_id
            WHERE dc.source_doc_id = ?
            ORDER BY d.date DESC
            LIMIT 20
            ''',
            (doc_id,)
        ).fetchall()

        return render_template('document.html', doc=doc,
                             citing=[dict(r) for r in citing],
                             cited=[dict(r) for r in cited])
    finally:
        conn.close()


@app.route('/jurisdictions')
def jurisdictions_page():
    conn = get_db()
    try:
        rows = conn.execute(
            '''
            SELECT jurisdiction, COUNT(*) as cnt
            FROM documents WHERE parent_id IS NULL AND jurisdiction != 'federal'
            GROUP BY jurisdiction ORDER BY jurisdiction
            '''
        ).fetchall()

        federal_count = conn.execute(
            "SELECT COUNT(*) FROM documents WHERE parent_id IS NULL AND jurisdiction = 'federal'"
        ).fetchone()[0]

        jurisdictions = [{'code': 'federal', 'count': federal_count}]
        jurisdictions.extend({'code': row[0], 'count': row[1]} for row in rows)

        return render_template('jurisdictions.html', jurisdictions=jurisdictions)
    finally:
        conn.close()


@app.route('/jurisdiction/<state>')
def jurisdiction_detail(state):
    conn = get_db()
    try:
        # Documents for this jurisdiction
        docs = conn.execute(
            '''
            SELECT document_type, COUNT(*) as cnt
            FROM documents WHERE jurisdiction = ? AND parent_id IS NULL
            GROUP BY document_type ORDER BY cnt DESC
            ''',
            (state,)
        ).fetchall()

        # Exemptions
        exemptions = conn.execute(
            'SELECT * FROM exemptions WHERE jurisdiction = ? ORDER BY exemption_number',
            (state,)
        ).fetchall()

        # Response rules
        rules = conn.execute(
            'SELECT * FROM response_rules WHERE jurisdiction = ? ORDER BY rule_type',
            (state,)
        ).fetchall()

        # Agencies
        agencies = conn.execute(
            'SELECT * FROM agencies WHERE jurisdiction = ? AND is_active = 1 ORDER BY name',
            (state,)
        ).fetchall()

        # Templates
        templates = conn.execute(
            'SELECT * FROM request_templates WHERE jurisdiction = ? ORDER BY record_type',
            (state,)
        ).fetchall()

        return render_template('jurisdiction.html',
                             state=state,
                             doc_counts=[(row[0], row[1]) for row in docs],
                             exemptions=[dict(row) for row in exemptions],
                             rules=[dict(row) for row in rules],
                             agencies=[dict(row) for row in agencies],
                             templates=[dict(row) for row in templates])
    finally:
        conn.close()


@app.route('/exemptions')
def exemptions_page():
    conn = get_db()
    try:
        jurisdiction = request.args.get('jurisdiction', '').strip()
        if jurisdiction:
            exemptions = conn.execute(
                'SELECT * FROM exemptions WHERE jurisdiction = ? ORDER BY exemption_number',
                (jurisdiction,)
            ).fetchall()
        else:
            exemptions = conn.execute(
                'SELECT * FROM exemptions ORDER BY jurisdiction, exemption_number'
            ).fetchall()

        jurisdictions = conn.execute(
            'SELECT DISTINCT jurisdiction FROM exemptions ORDER BY jurisdiction'
        ).fetchall()

        return render_template('exemptions.html',
                             exemptions=[dict(row) for row in exemptions],
                             jurisdictions=[row[0] for row in jurisdictions],
                             selected_jurisdiction=jurisdiction)
    finally:
        conn.close()


@app.route('/exemption/<int:exemption_id>')
def exemption_detail(exemption_id):
    conn = get_db()
    try:
        exemption = conn.execute(
            'SELECT * FROM exemptions WHERE id = ?', (exemption_id,)
        ).fetchone()
        if not exemption:
            abort(404)

        exemption = dict(exemption)

        # Get related case law
        related_cases = []
        if exemption.get('related_case_law'):
            try:
                case_ids = json.loads(exemption['related_case_law'])
                if case_ids:
                    placeholders = ', '.join(['?'] * len(case_ids))
                    related_cases = conn.execute(
                        f'SELECT id, citation, title, date, document_type FROM documents WHERE id IN ({placeholders})',
                        case_ids
                    ).fetchall()
                    related_cases = [dict(row) for row in related_cases]
            except (json.JSONDecodeError, TypeError):
                pass

        # Get related AG opinions
        related_opinions = []
        if exemption.get('related_ag_opinions'):
            try:
                opinion_ids = json.loads(exemption['related_ag_opinions'])
                if opinion_ids:
                    placeholders = ', '.join(['?'] * len(opinion_ids))
                    related_opinions = conn.execute(
                        f'SELECT id, citation, title, date, document_type FROM documents WHERE id IN ({placeholders})',
                        opinion_ids
                    ).fetchall()
                    related_opinions = [dict(row) for row in related_opinions]
            except (json.JSONDecodeError, TypeError):
                pass

        return render_template('exemption_detail.html',
                             exemption=exemption,
                             related_cases=related_cases,
                             related_opinions=related_opinions)
    finally:
        conn.close()


@app.route('/agencies')
def agencies_page():
    conn = get_db()
    try:
        jurisdiction = request.args.get('jurisdiction', '').strip()
        level = request.args.get('level', '').strip()

        query = 'SELECT * FROM agencies WHERE is_active = 1'
        params = []

        if jurisdiction:
            query += ' AND jurisdiction = ?'
            params.append(jurisdiction)
        if level:
            query += ' AND level = ?'
            params.append(level)

        query += ' ORDER BY jurisdiction, name'
        agencies = conn.execute(query, params).fetchall()

        jurisdictions = conn.execute(
            'SELECT DISTINCT jurisdiction FROM agencies WHERE is_active = 1 ORDER BY jurisdiction'
        ).fetchall()

        return render_template('agencies.html',
                             agencies=[dict(row) for row in agencies],
                             jurisdictions=[row[0] for row in jurisdictions],
                             selected_jurisdiction=jurisdiction,
                             selected_level=level)
    finally:
        conn.close()


@app.route('/agency/<int:agency_id>')
def agency_detail(agency_id):
    conn = get_db()
    try:
        agency = conn.execute('SELECT * FROM agencies WHERE id = ?', (agency_id,)).fetchone()
        if not agency:
            abort(404)

        agency = dict(agency)

        # Parse fee schedule JSON
        if agency.get('fee_schedule'):
            try:
                agency['fee_schedule_parsed'] = json.loads(agency['fee_schedule'])
            except (json.JSONDecodeError, TypeError):
                agency['fee_schedule_parsed'] = None

        # Get response rules for this jurisdiction
        rules = conn.execute(
            'SELECT * FROM response_rules WHERE jurisdiction = ?',
            (agency['jurisdiction'],)
        ).fetchall()

        return render_template('agency_detail.html',
                             agency=agency,
                             rules=[dict(row) for row in rules])
    finally:
        conn.close()


@app.route('/templates')
def templates_page():
    conn = get_db()
    try:
        jurisdiction = request.args.get('jurisdiction', '').strip()

        if jurisdiction:
            templates = conn.execute(
                'SELECT * FROM request_templates WHERE jurisdiction = ? ORDER BY record_type',
                (jurisdiction,)
            ).fetchall()
        else:
            templates = conn.execute(
                'SELECT * FROM request_templates ORDER BY jurisdiction, record_type'
            ).fetchall()

        jurisdictions = conn.execute(
            'SELECT DISTINCT jurisdiction FROM request_templates ORDER BY jurisdiction'
        ).fetchall()

        return render_template('templates.html',
                             templates=[dict(row) for row in templates],
                             jurisdictions=[row[0] for row in jurisdictions],
                             selected_jurisdiction=jurisdiction)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Routes — JSON API (key-gated)
# ---------------------------------------------------------------------------

def require_api_key():
    if not API_KEYS:
        return  # No keys configured, allow all
    key = request.headers.get('X-API-Key') or request.args.get('api_key')
    if key not in API_KEYS:
        abort(403)


@app.route('/api/search')
def api_search():
    require_api_key()
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Missing query parameter q'}), 400

    limit = min(request.args.get('limit', 20, type=int), 500)
    sort = request.args.get('sort', 'relevance')

    from fetch_json import search as do_search
    results = do_search(
        query,
        limit=limit,
        sort_by_authority=(sort == 'authority'),
        sort_by_recent=(sort == 'recent'),
        brief=True,
    )

    return jsonify({'query': query, 'count': len(results), 'results': results})


@app.route('/api/documents/<doc_id>')
def api_document(doc_id):
    require_api_key()
    conn = get_db()
    try:
        doc = conn.execute('SELECT * FROM documents WHERE id = ?', (doc_id,)).fetchone()
        if not doc:
            abort(404)
        return jsonify(dict(doc))
    finally:
        conn.close()


@app.route('/api/stats')
def api_stats():
    require_api_key()
    from fetch_json import get_stats
    return jsonify(get_stats())


@app.route('/api/exemptions')
def api_exemptions():
    require_api_key()
    conn = get_db()
    try:
        jurisdiction = request.args.get('jurisdiction', '').strip()
        if jurisdiction:
            rows = conn.execute(
                'SELECT * FROM exemptions WHERE jurisdiction = ? ORDER BY exemption_number',
                (jurisdiction,)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT * FROM exemptions ORDER BY jurisdiction, exemption_number'
            ).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        conn.close()


@app.route('/api/agencies')
def api_agencies():
    require_api_key()
    conn = get_db()
    try:
        jurisdiction = request.args.get('jurisdiction', '').strip()
        if jurisdiction:
            rows = conn.execute(
                'SELECT * FROM agencies WHERE jurisdiction = ? AND is_active = 1 ORDER BY name',
                (jurisdiction,)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT * FROM agencies WHERE is_active = 1 ORDER BY jurisdiction, name'
            ).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Routes — Utility
# ---------------------------------------------------------------------------

@app.route('/health')
def health():
    try:
        conn = get_db()
        count = conn.execute('SELECT COUNT(*) FROM documents').fetchone()[0]
        conn.close()
        return jsonify({'status': 'ok', 'documents': count})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nDisallow: /api/\n", mimetype='text/plain')


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('error.html', code=404, message='Page not found'), 404


@app.errorhandler(403)
def forbidden(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Invalid or missing API key'}), 403
    return render_template('error.html', code=403, message='Forbidden'), 403


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT, debug=True)
