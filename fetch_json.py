#!/usr/bin/env python3
"""Query engine for the PRDB public records database.

Usage:
    python3 fetch_json.py "search query" [--limit N] [--authority] [--recent] [--json]

Supports structured filters:
    Type:"AG Opinion - Public Records"
    Jurisdiction:"NY"
    Date:2020-2025
    Authority>=70

Placeholder name "prdb" — will be replaced with final project name.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = os.environ.get('PRDB_DB_PATH',
                          str(Path(__file__).resolve().parent / 'db' / 'prdb.db'))

# Domain signals for natural language query expansion
DOMAIN_SIGNALS = None


def _load_domain_signals():
    global DOMAIN_SIGNALS
    if DOMAIN_SIGNALS is not None:
        return DOMAIN_SIGNALS
    signals_path = Path(__file__).resolve().parent / 'config' / 'domain_signals.json'
    if signals_path.exists():
        with open(signals_path) as f:
            DOMAIN_SIGNALS = json.load(f).get('domains', {})
    else:
        DOMAIN_SIGNALS = {}
    return DOMAIN_SIGNALS


# Type aliases for umbrella searches
TYPE_ALIASES = {
    'court opinion': [
        'Supreme Court Opinion', 'Circuit Court Opinion', 'District Court Opinion',
        'Federal Court Opinion', 'State Court Opinion', 'State Supreme Court Opinion',
        'State Appellate Court Opinion',
    ],
    'ag opinion': [
        'AG Opinion - Public Records', 'AG Guidance - Public Records',
    ],
    'statute': [
        'Federal FOIA Statute', 'State Public Records Statute',
        'Open Meetings Statute', 'Privacy Act Statute',
    ],
    'regulation': [
        'Federal FOIA Regulation', 'State Public Records Regulation',
        'Open Meetings Regulation', 'Privacy Act Regulation',
    ],
    'foia': [
        'Federal FOIA Statute', 'Federal FOIA Regulation',
        'OGIS Advisory Opinion', 'DOJ OIP Guidance',
    ],
}


def _db_connect(db_path: str = None) -> sqlite3.Connection:
    """Read-only connection for queries."""
    path = db_path or DB_PATH
    try:
        conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=30)
        conn.execute('PRAGMA schema_version').fetchone()
    except sqlite3.OperationalError:
        conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True, timeout=30)
    conn.execute('PRAGMA query_only = ON')
    conn.row_factory = sqlite3.Row
    return conn


def _clean_fts_query(query: str) -> str:
    """Clean a query string for FTS5 compatibility."""
    # Strip problematic characters
    query = re.sub(r'[?!;]', '', query)
    # Quote decimal numbers to avoid FTS parse errors
    query = re.sub(r'(\d+)\.(\d+)', r'"\1.\2"', query)
    # Don't let stray quotes break FTS
    if query.count('"') % 2 != 0:
        query = query.replace('"', '')
    return query.strip()


def _parse_filters(raw_query: str) -> tuple[str, dict]:
    """Extract structured filters from query, return (remaining_query, filters)."""
    filters = {}

    # Type:"value"
    type_match = re.findall(r'Type:"([^"]+)"', raw_query, re.IGNORECASE)
    if type_match:
        filters['type'] = type_match
        raw_query = re.sub(r'Type:"[^"]+"', '', raw_query, flags=re.IGNORECASE)

    # Jurisdiction:"value"
    jur_match = re.findall(r'Jurisdiction:"([^"]+)"', raw_query, re.IGNORECASE)
    if jur_match:
        filters['jurisdiction'] = jur_match
        raw_query = re.sub(r'Jurisdiction:"[^"]+"', '', raw_query, flags=re.IGNORECASE)

    # Date:YYYY-YYYY
    date_match = re.search(r'Date:(\d{4})-(\d{4})', raw_query, re.IGNORECASE)
    if date_match:
        filters['date_start'] = date_match.group(1)
        filters['date_end'] = date_match.group(2)
        raw_query = re.sub(r'Date:\d{4}-\d{4}', '', raw_query, flags=re.IGNORECASE)

    # Authority>=N
    auth_match = re.search(r'Authority>=(\d+)', raw_query, re.IGNORECASE)
    if auth_match:
        filters['min_authority'] = int(auth_match.group(1))
        raw_query = re.sub(r'Authority>=\d+', '', raw_query, flags=re.IGNORECASE)

    # Source:"value"
    source_match = re.findall(r'Source:"([^"]+)"', raw_query, re.IGNORECASE)
    if source_match:
        filters['source'] = source_match
        raw_query = re.sub(r'Source:"[^"]+"', '', raw_query, flags=re.IGNORECASE)

    # Court:"value"
    court_match = re.findall(r'Court:"([^"]+)"', raw_query, re.IGNORECASE)
    if court_match:
        filters['court'] = court_match
        raw_query = re.sub(r'Court:"[^"]+"', '', raw_query, flags=re.IGNORECASE)

    return raw_query.strip(), filters


def _expand_type_filter(type_values: list[str]) -> list[str]:
    """Expand type aliases into concrete type names."""
    expanded = []
    for t in type_values:
        lower = t.lower().strip()
        if lower in TYPE_ALIASES:
            expanded.extend(TYPE_ALIASES[lower])
        else:
            expanded.append(t)
    return expanded


def _detect_domains(query: str) -> list[str]:
    """Detect which domains a query relates to based on signal words/phrases."""
    signals = _load_domain_signals()
    query_lower = query.lower()
    scores = {}

    for domain, config in signals.items():
        score = 0
        for word in config.get('word_signals', []):
            if word in query_lower:
                score += 1
        for phrase in config.get('phrase_signals', []):
            if phrase in query_lower:
                score += 2
        if score >= 2:
            scores[domain] = score

    # Return domains sorted by score descending
    return [d for d, _ in sorted(scores.items(), key=lambda x: -x[1])]


def _build_fts_query(text_query: str, filters: dict) -> tuple[str, list, list[str]]:
    """Build SQL query from parsed components.

    Returns (sql, params, post_filter_types).
    """
    cleaned = _clean_fts_query(text_query)

    # Build WHERE conditions
    conditions = []
    params = []
    join_fts = bool(cleaned)

    if join_fts:
        # BM25 weighted: citation(5), title(10), text(1), summary(3), summary_ai(3), topics(2)
        base = '''
            SELECT d.*, bm25(documents_fts, 5, 10, 1, 3, 3, 2) AS rank
            FROM documents_fts fts
            JOIN documents d ON d.rowid = fts.rowid
            WHERE documents_fts MATCH ?
        '''
        params.append(cleaned)
    else:
        base = '''
            SELECT d.*, 0 AS rank
            FROM documents d
            WHERE 1=1
        '''

    # Type filter
    type_values = filters.get('type', [])
    if type_values:
        expanded = _expand_type_filter(type_values)
        placeholders = ', '.join(['?'] * len(expanded))
        conditions.append(f'd.document_type IN ({placeholders})')
        params.extend(expanded)

    # Jurisdiction filter
    jur_values = filters.get('jurisdiction', [])
    if jur_values:
        placeholders = ', '.join(['?'] * len(jur_values))
        conditions.append(f'd.jurisdiction IN ({placeholders})')
        params.extend(jur_values)

    # Date range filter
    if 'date_start' in filters:
        conditions.append('d.date >= ?')
        params.append(f"{filters['date_start']}-01-01")
    if 'date_end' in filters:
        conditions.append('d.date <= ?')
        params.append(f"{filters['date_end']}-12-31")

    # Authority filter
    if 'min_authority' in filters:
        conditions.append('d.authority_weight >= ?')
        params.append(filters['min_authority'])

    # Source filter
    source_values = filters.get('source', [])
    if source_values:
        placeholders = ', '.join(['?'] * len(source_values))
        conditions.append(f'd.source IN ({placeholders})')
        params.extend(source_values)

    # Court filter
    court_values = filters.get('court', [])
    if court_values:
        court_conditions = []
        for cv in court_values:
            court_conditions.append('d.court LIKE ?')
            params.append(f'%{cv}%')
        conditions.append('(' + ' OR '.join(court_conditions) + ')')

    # Exclude chunks (parent documents only)
    conditions.append('d.parent_id IS NULL')

    if conditions:
        base += ' AND ' + ' AND '.join(conditions)

    return base, params, type_values


def _domain_expansion(text_query: str, filters: dict, limit: int, conn: sqlite3.Connection) -> list[dict]:
    """Run domain-detected expansion queries for vague/natural-language queries."""
    if filters.get('type'):
        return []  # User specified type, don't expand

    domains = _detect_domains(text_query)
    if not domains:
        return []

    signals = _load_domain_signals()
    results = []
    seen_ids = set()
    expansion_cap = min(int(limit * 0.75), 15)

    for domain in domains[:3]:  # Max 3 domains
        domain_config = signals.get(domain, {})
        type_filters = domain_config.get('type_filters', [])
        if not type_filters:
            continue

        for doc_type in type_filters[:3]:
            if len(results) >= expansion_cap:
                break
            sub_filters = dict(filters)
            sub_filters['type'] = [doc_type]
            sql, params, _ = _build_fts_query(text_query, sub_filters)
            sql += ' ORDER BY rank LIMIT ?'
            params.append(5)

            try:
                rows = conn.execute(sql, params).fetchall()
                for row in rows:
                    row_dict = dict(row)
                    if row_dict['id'] not in seen_ids:
                        seen_ids.add(row_dict['id'])
                        results.append(row_dict)
            except sqlite3.OperationalError:
                continue

    return results


def _alias_injection(text_query: str, conn: sqlite3.Connection) -> list[dict]:
    """Check authority_aliases for exact matches and inject at top of results."""
    results = []
    # Check for known patterns
    query_upper = text_query.strip().upper()

    try:
        rows = conn.execute(
            '''
            SELECT d.* FROM authority_aliases aa
            JOIN documents d ON d.id = aa.doc_id
            WHERE aa.alias = ? OR aa.normalized_alias = ?
            LIMIT 5
            ''',
            (query_upper, query_upper)
        ).fetchall()
        results.extend(dict(row) for row in rows)
    except sqlite3.OperationalError:
        pass

    return results


def search(raw_query: str, limit: int = 500, sort_by_authority: bool = False,
           sort_by_recent: bool = False, brief: bool = True) -> list[dict]:
    """Main search function. Returns list of document dicts."""
    text_query, filters = _parse_filters(raw_query)
    conn = _db_connect()

    try:
        # Primary query
        sql, params, _ = _build_fts_query(text_query, filters)

        if sort_by_authority:
            sql += ' ORDER BY d.authority_weight DESC, rank'
        elif sort_by_recent:
            sql += ' ORDER BY d.date DESC, rank'
        else:
            sql += ' ORDER BY rank'

        sql += ' LIMIT ?'
        params.append(limit)

        try:
            rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError as e:
            # FTS query syntax error — fall back to simple LIKE search
            rows = conn.execute(
                '''
                SELECT d.*, 0 AS rank FROM documents d
                WHERE (d.title LIKE ? OR d.text LIKE ?) AND d.parent_id IS NULL
                ORDER BY d.authority_weight DESC
                LIMIT ?
                ''',
                (f'%{text_query}%', f'%{text_query}%', limit)
            ).fetchall()

        results = [dict(row) for row in rows]
        seen_ids = {r['id'] for r in results}

        # Domain expansion for vague queries
        if text_query and not filters.get('type') and len(results) < limit:
            expanded = _domain_expansion(text_query, filters, limit, conn)
            for doc in expanded:
                if doc['id'] not in seen_ids:
                    seen_ids.add(doc['id'])
                    results.append(doc)

        # Alias injection
        if text_query:
            aliases = _alias_injection(text_query, conn)
            for doc in aliases:
                if doc['id'] not in seen_ids:
                    seen_ids.add(doc['id'])
                    results.insert(0, doc)

        # Type diversity constraint: max 5 of any single type in top 10
        if len(results) > 10:
            top_10 = results[:10]
            rest = results[10:]
            type_counts = {}
            filtered_top = []
            overflow = []

            for doc in top_10:
                dt = doc.get('document_type', '')
                type_counts[dt] = type_counts.get(dt, 0) + 1
                if type_counts[dt] <= 5:
                    filtered_top.append(doc)
                else:
                    overflow.append(doc)

            # Fill top 10 from rest if we removed any
            while len(filtered_top) < 10 and rest:
                candidate = rest.pop(0)
                dt = candidate.get('document_type', '')
                type_counts[dt] = type_counts.get(dt, 0) + 1
                if type_counts[dt] <= 5:
                    filtered_top.append(candidate)
                else:
                    overflow.append(candidate)

            results = filtered_top + overflow + rest

        # Trim to limit
        results = results[:limit]

        # Brief mode: strip full text
        if brief:
            for doc in results:
                snippet = doc.get('summary_brief') or doc.get('summary_ai') or doc.get('summary') or ''
                if not snippet and doc.get('text'):
                    snippet = doc['text'][:500] + '...' if len(doc.get('text', '')) > 500 else doc.get('text', '')
                doc['snippet'] = snippet
                doc.pop('text', None)
                doc.pop('summary_ai', None)

        return results

    finally:
        conn.close()


def get_stats() -> dict:
    """Get corpus statistics."""
    conn = _db_connect()
    try:
        total = conn.execute('SELECT COUNT(*) FROM documents WHERE parent_id IS NULL').fetchone()[0]
        by_type = conn.execute(
            'SELECT document_type, COUNT(*) FROM documents WHERE parent_id IS NULL GROUP BY document_type ORDER BY COUNT(*) DESC'
        ).fetchall()
        by_jurisdiction = conn.execute(
            'SELECT jurisdiction, COUNT(*) FROM documents WHERE parent_id IS NULL GROUP BY jurisdiction ORDER BY COUNT(*) DESC'
        ).fetchall()
        exemption_count = conn.execute('SELECT COUNT(*) FROM exemptions').fetchone()[0]
        agency_count = conn.execute('SELECT COUNT(*) FROM agencies WHERE is_active = 1').fetchone()[0]
        template_count = conn.execute('SELECT COUNT(*) FROM request_templates').fetchone()[0]

        return {
            'total_documents': total,
            'by_type': {row[0]: row[1] for row in by_type},
            'by_jurisdiction': {row[0]: row[1] for row in by_jurisdiction},
            'exemptions': exemption_count,
            'agencies': agency_count,
            'templates': template_count,
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Search the Sunshine public records database')
    parser.add_argument('query', nargs='?', default='', help='Search query (supports Type:"...", Jurisdiction:"...", Date:YYYY-YYYY)')
    parser.add_argument('--limit', type=int, default=20, help='Max results (default: 20)')
    parser.add_argument('--authority', action='store_true', help='Sort by authority weight')
    parser.add_argument('--recent', action='store_true', help='Sort by date (newest first)')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    parser.add_argument('--full', action='store_true', help='Include full text (not brief)')
    parser.add_argument('--stats', action='store_true', help='Show corpus statistics')

    args = parser.parse_args()

    if args.stats:
        stats = get_stats()
        print(json.dumps(stats, indent=2))
        return

    results = search(
        args.query,
        limit=args.limit,
        sort_by_authority=args.authority,
        sort_by_recent=args.recent,
        brief=not args.full,
    )

    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print(f'\n{len(results)} results for: {args.query}\n')
        for i, doc in enumerate(results, 1):
            citation = doc.get('citation') or doc.get('title', 'Untitled')
            date = doc.get('date', '')
            doc_type = doc.get('document_type', '')
            jurisdiction = doc.get('jurisdiction', '')
            authority = doc.get('authority_weight', 0)

            print(f'{i}. [{doc_type}] {citation}')
            if date:
                print(f'   Date: {date} | Jurisdiction: {jurisdiction} | Authority: {authority}')
            snippet = doc.get('snippet', '')
            if snippet:
                # Truncate for display
                if len(snippet) > 200:
                    snippet = snippet[:200] + '...'
                print(f'   {snippet}')
            print()


if __name__ == '__main__':
    main()
