#!/usr/bin/env python3
"""
Export PRDB database to static JSON files for the React web interface.

Outputs to web/public/data/:
  exemptions.json    - All exemptions with parsed JSON fields
  rules.json         - All response rules
  templates.json     - All request templates
  agencies.json      - All agencies with parsed JSON fields
  documents.json     - Document metadata only (no full text)
  jurisdictions.json - Pre-computed jurisdiction summaries
  stats.json         - Global counts
  search-index.json  - Serialized MiniSearch index (built via Node)
"""

import json
import os
import sqlite3
import subprocess
import sys
import tempfile

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'prdb.db')
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web', 'public', 'data')
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web')

os.makedirs(OUT_DIR, exist_ok=True)

STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
    'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
    'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    'federal': 'Federal',
}

# Known law names by jurisdiction code
LAW_NAMES = {
    'federal': 'Freedom of Information Act (FOIA)',
    'AL': 'Alabama Open Records Act',
    'AK': 'Alaska Public Records Act',
    'AZ': 'Arizona Public Records Law',
    'AR': 'Arkansas Freedom of Information Act',
    'CA': 'California Public Records Act (CPRA)',
    'CO': 'Colorado Open Records Act (CORA)',
    'CT': 'Connecticut Freedom of Information Act',
    'DE': 'Delaware Freedom of Information Act',
    'DC': 'D.C. Freedom of Information Act',
    'FL': 'Florida Public Records Law',
    'GA': 'Georgia Open Records Act',
    'HI': 'Hawaii Uniform Information Practices Act',
    'ID': 'Idaho Public Records Act',
    'IL': 'Illinois Freedom of Information Act',
    'IN': 'Indiana Access to Public Records Act',
    'IA': 'Iowa Open Records Act',
    'KS': 'Kansas Open Records Act',
    'KY': 'Kentucky Open Records Act',
    'LA': 'Louisiana Public Records Law',
    'ME': 'Maine Freedom of Access Act',
    'MD': 'Maryland Public Information Act',
    'MA': 'Massachusetts Public Records Law',
    'MI': 'Michigan Freedom of Information Act',
    'MN': 'Minnesota Government Data Practices Act',
    'MS': 'Mississippi Public Records Act',
    'MO': 'Missouri Sunshine Law',
    'MT': 'Montana Right to Know Act',
    'NE': 'Nebraska Public Records Statutes',
    'NV': 'Nevada Public Records Act',
    'NH': 'New Hampshire Right-to-Know Law',
    'NJ': 'New Jersey Open Public Records Act (OPRA)',
    'NM': 'New Mexico Inspection of Public Records Act',
    'NY': 'Freedom of Information Law (FOIL)',
    'NC': 'North Carolina Public Records Law',
    'ND': 'North Dakota Open Records Law',
    'OH': 'Ohio Public Records Act',
    'OK': 'Oklahoma Open Records Act',
    'OR': 'Oregon Public Records Law',
    'PA': 'Pennsylvania Right-to-Know Law',
    'RI': 'Rhode Island Access to Public Records Act',
    'SC': 'South Carolina Freedom of Information Act',
    'SD': 'South Dakota Open Records Law',
    'TN': 'Tennessee Public Records Act',
    'TX': 'Texas Public Information Act',
    'UT': 'Utah Government Records Access and Management Act (GRAMA)',
    'VT': 'Vermont Public Records Act',
    'VA': 'Virginia Freedom of Information Act',
    'WA': 'Washington Public Records Act',
    'WV': 'West Virginia Freedom of Information Act',
    'WI': 'Wisconsin Open Records Law',
    'WY': 'Wyoming Public Records Act',
}


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def strip_nulls(record):
    """Remove None/null values from a dict to reduce file size."""
    return {k: v for k, v in record.items() if v is not None}


def parse_json_fields(records, fields):
    """Parse JSON string fields into Python objects in-place."""
    for rec in records:
        for field in fields:
            if field in rec and isinstance(rec[field], str):
                try:
                    rec[field] = json.loads(rec[field])
                except (json.JSONDecodeError, TypeError):
                    pass
    return records


def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    size = os.path.getsize(path)
    return size


def fmt_size(n):
    if n < 1024:
        return f'{n} B'
    elif n < 1024 * 1024:
        return f'{n/1024:.1f} KB'
    else:
        return f'{n/1024/1024:.1f} MB'


def export():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory

    sizes = {}

    # -------------------------------------------------------------------------
    # 1. exemptions.json
    # -------------------------------------------------------------------------
    exemptions = conn.execute('''
        SELECT id, jurisdiction, statute_citation, exemption_number, short_name,
               category, description, scope, key_terms, common_agency_uses,
               successful_challenge_rate, related_case_law, related_ag_opinions,
               counter_arguments, notes, last_verified
        FROM exemptions
        ORDER BY jurisdiction, exemption_number
    ''').fetchall()

    parse_json_fields(exemptions, ['key_terms', 'counter_arguments', 'related_case_law',
                                   'related_ag_opinions', 'common_agency_uses'])
    exemptions = [strip_nulls(e) for e in exemptions]

    path = os.path.join(OUT_DIR, 'exemptions.json')
    sizes['exemptions.json'] = write_json(path, exemptions)
    print(f'  exemptions.json    {len(exemptions):>5} records  {fmt_size(sizes["exemptions.json"])}')

    # -------------------------------------------------------------------------
    # 2. rules.json
    # -------------------------------------------------------------------------
    rules = conn.execute('''
        SELECT id, jurisdiction, rule_type, param_key, param_value,
               day_type, statute_citation, notes, last_verified
        FROM response_rules
        ORDER BY jurisdiction, rule_type, param_key
    ''').fetchall()

    rules = [strip_nulls(r) for r in rules]

    path = os.path.join(OUT_DIR, 'rules.json')
    sizes['rules.json'] = write_json(path, rules)
    print(f'  rules.json         {len(rules):>5} records  {fmt_size(sizes["rules.json"])}')

    # -------------------------------------------------------------------------
    # 3. templates.json
    # -------------------------------------------------------------------------
    templates = conn.execute('''
        SELECT id, jurisdiction, record_type, template_name, template_text,
               fee_waiver_language, expedited_language, appeal_template, notes, source
        FROM request_templates
        ORDER BY jurisdiction, template_name
    ''').fetchall()

    templates = [strip_nulls(t) for t in templates]

    path = os.path.join(OUT_DIR, 'templates.json')
    sizes['templates.json'] = write_json(path, templates)
    print(f'  templates.json     {len(templates):>5} records  {fmt_size(sizes["templates.json"])}')

    # -------------------------------------------------------------------------
    # 4. agencies.json
    # -------------------------------------------------------------------------
    agencies = conn.execute('''
        SELECT id, name, jurisdiction, level, parent_agency_id, abbreviation,
               foia_officer_title, foia_officer_name, email, mailing_address,
               phone, fax, portal_url, submission_method, required_form_url,
               fee_schedule, fee_waiver_available, fee_waiver_criteria,
               avg_response_days, common_denial_exemptions, notes,
               source_url, last_verified, is_active
        FROM agencies
        ORDER BY jurisdiction, name
    ''').fetchall()

    parse_json_fields(agencies, ['fee_schedule', 'common_denial_exemptions'])
    agencies = [strip_nulls(a) for a in agencies]

    path = os.path.join(OUT_DIR, 'agencies.json')
    sizes['agencies.json'] = write_json(path, agencies)
    print(f'  agencies.json      {len(agencies):>5} records  {fmt_size(sizes["agencies.json"])}')

    # -------------------------------------------------------------------------
    # 5. documents.json — metadata only, no full text
    # -------------------------------------------------------------------------
    documents = conn.execute('''
        SELECT id, citation, title, date, court, document_type, jurisdiction,
               source, source_url, summary
        FROM documents
        ORDER BY jurisdiction, date DESC
    ''').fetchall()

    documents = [strip_nulls(d) for d in documents]

    path = os.path.join(OUT_DIR, 'documents.json')
    sizes['documents.json'] = write_json(path, documents)
    print(f'  documents.json     {len(documents):>5} records  {fmt_size(sizes["documents.json"])}')

    # -------------------------------------------------------------------------
    # 6. jurisdictions.json — pre-computed summaries
    # -------------------------------------------------------------------------
    # Gather all jurisdictions that appear in any of the core tables
    all_jurisdictions = set()
    for table in ('exemptions', 'response_rules', 'request_templates', 'agencies'):
        rows = conn.execute(f'SELECT DISTINCT jurisdiction FROM {table}').fetchall()
        for r in rows:
            all_jurisdictions.add(r['jurisdiction'])

    # Build a lookup from response_rules for initial_response
    # param_key = 'days_to_respond' or 'response_deadline_days'
    initial_response_keys = {'days_to_respond', 'response_deadline_days'}

    jurisdictions = []
    for code in sorted(all_jurisdictions):
        name = STATE_NAMES.get(code, code)
        law_name = LAW_NAMES.get(code, 'Public Records Law')

        # Pull all rules for this jurisdiction for efficient lookups
        jur_rules = conn.execute(
            'SELECT rule_type, param_key, param_value, day_type, statute_citation, notes '
            'FROM response_rules WHERE jurisdiction=?', (code,)
        ).fetchall()

        # Find initial response info
        response_days = None
        response_type = None
        response_description = None
        statute_citation = None

        for rule in jur_rules:
            if rule['rule_type'] == 'initial_response':
                if rule['param_key'] in initial_response_keys:
                    val = rule['param_value']
                    try:
                        response_days = int(val)
                    except (ValueError, TypeError):
                        response_days = val  # keep as string if not numeric (e.g., "none_statutory")
                    response_type = rule['day_type'] or 'calendar'
                    if rule['statute_citation']:
                        statute_citation = rule['statute_citation']
                    if rule['notes']:
                        response_description = rule['notes']

        # Fee info
        fee_info = None
        for rule in jur_rules:
            if rule['rule_type'] in ('fee_cap', 'fee_schedule') and rule['notes']:
                fee_info = rule['notes']
                break
        if not fee_info:
            for rule in jur_rules:
                if rule['rule_type'] == 'fee_cap':
                    fee_info = f"{rule['param_key']}: {rule['param_value']}"
                    break

        # Appeal info
        appeal_info = None
        for rule in jur_rules:
            if rule['rule_type'] == 'appeal_deadline':
                if rule['notes']:
                    appeal_info = rule['notes']
                elif rule['param_key'] in ('days_to_appeal', 'appeal_deadline_days'):
                    days = rule['param_value']
                    dtype = rule['day_type'] or 'calendar'
                    appeal_info = f"Must appeal within {days} {dtype} days"
                break

        has_fee_waiver = any(r['rule_type'] == 'fee_waiver' for r in jur_rules)
        has_admin_appeal = any(r['rule_type'] == 'appeal_deadline' for r in jur_rules)

        exemption_count = conn.execute(
            'SELECT COUNT(*) as c FROM exemptions WHERE jurisdiction=?', (code,)
        ).fetchone()['c']

        rule_count = conn.execute(
            'SELECT COUNT(*) as c FROM response_rules WHERE jurisdiction=?', (code,)
        ).fetchone()['c']

        template_count = conn.execute(
            'SELECT COUNT(*) as c FROM request_templates WHERE jurisdiction=?', (code,)
        ).fetchone()['c']

        document_count = conn.execute(
            'SELECT COUNT(*) as c FROM documents WHERE jurisdiction=?', (code,)
        ).fetchone()['c']

        summary = {
            'code': code,
            'name': name,
            'law_name': law_name,
            'has_fee_waiver': has_fee_waiver,
            'has_admin_appeal': has_admin_appeal,
            'exemption_count': exemption_count,
            'rule_count': rule_count,
            'template_count': template_count,
            'document_count': document_count,
        }

        if statute_citation:
            summary['statute_citation'] = statute_citation
        if response_days is not None:
            summary['response_days'] = response_days
        if response_type:
            summary['response_type'] = response_type
        if response_description:
            summary['response_description'] = response_description
        if fee_info:
            summary['fee_info'] = fee_info
        if appeal_info:
            summary['appeal_info'] = appeal_info

        jurisdictions.append(summary)

    path = os.path.join(OUT_DIR, 'jurisdictions.json')
    sizes['jurisdictions.json'] = write_json(path, jurisdictions)
    print(f'  jurisdictions.json {len(jurisdictions):>5} records  {fmt_size(sizes["jurisdictions.json"])}')

    # -------------------------------------------------------------------------
    # 7. stats.json
    # -------------------------------------------------------------------------
    doc_count = conn.execute('SELECT COUNT(*) as c FROM documents').fetchone()['c']
    stats = {
        'documents': doc_count,
        'exemptions': len(exemptions),
        'rules': len(rules),
        'templates': len(templates),
        'agencies': len(agencies),
        'jurisdictions': len(jurisdictions),
    }

    path = os.path.join(OUT_DIR, 'stats.json')
    sizes['stats.json'] = write_json(path, stats)
    print(f'  stats.json               {fmt_size(sizes["stats.json"])}  {stats}')

    # -------------------------------------------------------------------------
    # 8. search-index.json — MiniSearch index built via Node
    # -------------------------------------------------------------------------
    # Build list of searchable items from Python, pass to Node for indexing
    search_items = []

    for ex in exemptions:
        text_parts = [
            ex.get('short_name', ''),
            ex.get('description', ''),
            ex.get('scope', ''),
            ex.get('statute_citation', ''),
            ex.get('notes', ''),
        ]
        search_items.append({
            'id': f"exemption:{ex['id']}",
            'type': 'exemption',
            'title': ex.get('short_name') or ex.get('exemption_number') or ex.get('statute_citation', ''),
            'text': ' '.join(p for p in text_parts if p),
            'jurisdiction': ex.get('jurisdiction', ''),
        })

    for ag in agencies:
        text_parts = [
            ag.get('name', ''),
            ag.get('abbreviation', ''),
            ag.get('notes', ''),
        ]
        search_items.append({
            'id': f"agency:{ag['id']}",
            'type': 'agency',
            'title': ag.get('name', ''),
            'text': ' '.join(p for p in text_parts if p),
            'jurisdiction': ag.get('jurisdiction', ''),
        })

    for tpl in templates:
        text_parts = [
            tpl.get('template_name', ''),
            tpl.get('record_type', ''),
            tpl.get('notes', ''),
        ]
        search_items.append({
            'id': f"template:{tpl['id']}",
            'type': 'template',
            'title': tpl.get('template_name', ''),
            'text': ' '.join(p for p in text_parts if p),
            'jurisdiction': tpl.get('jurisdiction', ''),
        })

    for doc in documents:
        text_parts = [
            doc.get('title', ''),
            doc.get('citation', ''),
            doc.get('summary', ''),
            doc.get('court', ''),
        ]
        search_items.append({
            'id': f"document:{doc['id']}",
            'type': 'document',
            'title': doc.get('title') or doc.get('citation', ''),
            'text': ' '.join(p for p in text_parts if p),
            'jurisdiction': doc.get('jurisdiction', ''),
        })

    conn.close()

    # Write items to a temp file, then let Node build the MiniSearch index
    items_path = os.path.join(OUT_DIR, '_search_items_tmp.json')
    with open(items_path, 'w') as f:
        json.dump(search_items, f)

    index_out_path = os.path.join(OUT_DIR, 'search-index.json')
    builder_path = os.path.join(SCRIPTS_DIR, 'build_search_index.js')

    result = subprocess.run(
        ['node', builder_path, items_path, index_out_path],
        capture_output=True, text=True, cwd=WEB_DIR
    )
    if result.returncode != 0:
        print(f'  ERROR building search index: {result.stderr}', file=sys.stderr)
        sys.exit(1)

    os.unlink(items_path)

    sizes['search-index.json'] = os.path.getsize(index_out_path)
    print(f'  search-index.json  {len(search_items):>5} items    {fmt_size(sizes["search-index.json"])}')

    # Summary
    print()
    print('Export complete.')
    total = sum(sizes.values())
    print(f'Total output: {fmt_size(total)}')


if __name__ == '__main__':
    export()
