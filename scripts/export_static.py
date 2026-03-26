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

    # -------------------------------------------------------------------------
    # 8. Derived analytical data
    # -------------------------------------------------------------------------
    print('\n  Computing derived analytics...')

    # Helper: normalize response days from heterogeneous param_keys
    RESPONSE_DAY_KEYS = {
        'days_to_respond', 'response_deadline_days', 'initial_response_deadline_days',
        'response_standard_days', 'formal_request_response_days', 'production_deadline_days',
        'days_to_produce', 'response_timeline',
    }
    COPY_FEE_KEYS = {
        'copy_rate_per_page', 'copy_fee_per_page', 'default_copy_rate_per_page',
        'standard_copy_rate_per_page', 'duplication_per_page_standard', 'duplication_per_page',
        'copy_fee_cap_per_page', 'standard_copy_rate', 'copy_rate_paper', 'copying_per_page_paper',
        'copying_fee_standard', 'copy_fee_standard', 'standard_paper_copy_rate',
        'copy_fee_max_per_page', 'copying_per_page_letter_size', 'fee_standard',
    }

    # Build per-jurisdiction rule lookups
    jur_rules_map = {}
    for r in rules:
        code = r.get('jurisdiction', '')
        jur_rules_map.setdefault(code, []).append(r)

    # --- 8a. Deadline rankings ---
    deadline_rankings = []
    for code in sorted(jur_rules_map.keys()):
        jrules = jur_rules_map[code]
        days = None
        day_type = None
        extension_days = None
        for r in jrules:
            if r.get('rule_type') == 'initial_response' and r.get('param_key') in RESPONSE_DAY_KEYS:
                try:
                    days = int(r['param_value'])
                    day_type = r.get('day_type', 'business')
                except (ValueError, TypeError):
                    pass
            if r.get('rule_type') == 'initial_response' and r.get('param_key') in (
                'extension_days', 'extension_deadline_days', 'max_extension_days',
                'extension_available_days', 'response_extension_days',
            ):
                try:
                    extension_days = int(r['param_value'])
                except (ValueError, TypeError):
                    pass

        # Normalize to calendar-equivalent for ranking
        cal_equiv = None
        if days is not None:
            cal_equiv = round(days * 1.4) if day_type == 'business' else days

        deadline_rankings.append({
            'code': code,
            'name': STATE_NAMES.get(code, code),
            'days': days,
            'day_type': day_type or 'business',
            'calendar_equivalent': cal_equiv,
            'extension_days': extension_days,
        })

    deadline_rankings.sort(key=lambda x: (x['calendar_equivalent'] or 999, x['code']))
    path = os.path.join(OUT_DIR, 'deadline_rankings.json')
    sizes['deadline_rankings.json'] = write_json(path, deadline_rankings)
    print(f'  deadline_rankings  {len(deadline_rankings):>5} records  {fmt_size(sizes["deadline_rankings.json"])}')

    # --- 8b. Fee comparison ---
    fee_comparison = []
    for code in sorted(jur_rules_map.keys()):
        jrules = jur_rules_map[code]
        per_page = None
        per_page_numeric = None
        search_fees = None
        staff_time = None
        fee_notes = None
        fee_citation = None

        for r in jrules:
            if r.get('rule_type') == 'fee_cap':
                pk = r.get('param_key', '')
                pv = r.get('param_value', '')
                if pk in COPY_FEE_KEYS:
                    per_page = pv
                    try:
                        per_page_numeric = float(pv)
                    except (ValueError, TypeError):
                        pass
                    if r.get('statute_citation'):
                        fee_citation = r['statute_citation']
                elif 'search' in pk or 'retrieval' in pk:
                    search_fees = pv
                elif 'staff' in pk or 'labor' in pk:
                    staff_time = pv
                if r.get('notes') and not fee_notes:
                    fee_notes = r['notes']

        # Check for fee waiver
        has_waiver = any(r.get('rule_type') == 'fee_waiver' for r in jrules)

        fee_comparison.append({
            'code': code,
            'name': STATE_NAMES.get(code, code),
            'per_page': per_page,
            'per_page_numeric': per_page_numeric,
            'search_fees': search_fees,
            'staff_time': staff_time,
            'has_fee_waiver': has_waiver,
            'notes': fee_notes,
            'citation': fee_citation,
        })

    fee_comparison.sort(key=lambda x: (x['per_page_numeric'] if x['per_page_numeric'] is not None else 999, x['code']))
    path = os.path.join(OUT_DIR, 'fee_comparison.json')
    sizes['fee_comparison.json'] = write_json(path, [strip_nulls(f) for f in fee_comparison])
    print(f'  fee_comparison     {len(fee_comparison):>5} records  {fmt_size(sizes["fee_comparison.json"])}')

    # --- 8c. Penalty comparison ---
    penalty_comparison = []
    for code in sorted(jur_rules_map.keys()):
        jrules = jur_rules_map[code]
        atty_fees = None
        atty_fees_type = None  # mandatory, discretionary, none
        civil_penalty = None
        criminal_penalty = None
        per_diem = None
        statutory_damages = None

        for r in jrules:
            if r.get('rule_type') != 'penalty':
                continue
            pk = r.get('param_key', '')
            pv = r.get('param_value', '')

            if 'attorneys_fees' in pk:
                atty_fees = pv
                if 'mandatory' in pv:
                    atty_fees_type = 'mandatory'
                elif 'discretionary' in pv or 'available' in pv:
                    atty_fees_type = 'discretionary'
                elif 'not' in pv:
                    atty_fees_type = 'none'
                else:
                    atty_fees_type = 'available'
            elif 'criminal' in pk:
                criminal_penalty = pv
            elif 'per_diem' in pk or 'per_day' in pk or 'statutory_damages' in pk:
                per_diem = pv
            elif 'civil' in pk:
                civil_penalty = pv

        # Also check judicial_review_deadline for attorney fee info
        if not atty_fees:
            for r in jrules:
                if r.get('rule_type') == 'judicial_review_deadline' and 'attorney' in r.get('param_key', ''):
                    atty_fees = r.get('param_value', '')
                    if 'mandatory' in atty_fees:
                        atty_fees_type = 'mandatory'
                    else:
                        atty_fees_type = 'discretionary'

        penalty_comparison.append({
            'code': code,
            'name': STATE_NAMES.get(code, code),
            'attorneys_fees': atty_fees,
            'attorneys_fees_type': atty_fees_type,
            'civil_penalty': civil_penalty,
            'criminal_penalty': criminal_penalty,
            'per_diem': per_diem,
        })

    path = os.path.join(OUT_DIR, 'penalty_comparison.json')
    sizes['penalty_comparison.json'] = write_json(path, [strip_nulls(p) for p in penalty_comparison])
    print(f'  penalty_comparison {len(penalty_comparison):>5} records  {fmt_size(sizes["penalty_comparison.json"])}')

    # --- 8d. Exemption cross-walk ---
    # Group exemptions by category across jurisdictions
    category_map = {}
    for ex in exemptions:
        cat = ex.get('category')
        if not cat:
            continue
        category_map.setdefault(cat, []).append({
            'jurisdiction': ex.get('jurisdiction'),
            'id': ex.get('id'),
            'exemption_number': ex.get('exemption_number'),
            'short_name': ex.get('short_name'),
            'description': (ex.get('description', '') or '')[:200],
            'statute_citation': ex.get('statute_citation'),
        })

    crosswalk = []
    for cat in sorted(category_map.keys()):
        items = category_map[cat]
        jur_set = set(i['jurisdiction'] for i in items)
        crosswalk.append({
            'category': cat,
            'count': len(items),
            'jurisdictions': len(jur_set),
            'exemptions': items,
        })

    path = os.path.join(OUT_DIR, 'exemption_crosswalk.json')
    sizes['exemption_crosswalk.json'] = write_json(path, crosswalk)
    print(f'  exemption_crosswalk {len(crosswalk):>4} categories {fmt_size(sizes["exemption_crosswalk.json"])}')

    # --- 8e. Appeal pathways ---
    appeal_pathways = []
    for code in sorted(jur_rules_map.keys()):
        jrules = jur_rules_map[code]
        admin_appeal = None
        admin_body = None
        admin_deadline = None
        judicial_court = None
        judicial_deadline = None
        judicial_fees = None
        steps = []

        for r in jrules:
            if r.get('rule_type') == 'appeal_deadline':
                pk = r.get('param_key', '')
                pv = r.get('param_value', '')
                if 'administrative_appeal' in pk:
                    admin_appeal = pv
                elif 'days_to_appeal' in pk or 'deadline_days' in pk:
                    admin_deadline = pv
                elif pk in ('appeal_response_days', 'agency_head_response_days', 'appeal_to_agency_head_days'):
                    admin_deadline = pv
                elif any(x in pk for x in ('foic', 'grc', 'pac', 'oor', 'ipib', 'oip', 'coog', 'compliance_board', 'ethics_commission', 'records_committee', 'public_access_counselor', 'attorney_general', 'supervisor', 'office_of_open_government', 'district_attorney')):
                    admin_body = pk.replace('_', ' ').replace('deadline days', '').replace('complaint', '').strip()
                    if pv and pv not in ('yes', 'true', 'available'):
                        admin_deadline = pv

            if r.get('rule_type') == 'judicial_review_deadline':
                pk = r.get('param_key', '')
                pv = r.get('param_value', '')
                if any(x in pk for x in ('court', 'enforcement', 'mandamus', 'suit', 'review', 'action')):
                    judicial_court = pk.replace('_', ' ')
                    if pv and pv not in ('yes', 'true', 'available'):
                        judicial_deadline = pv
                elif 'attorney' in pk:
                    judicial_fees = pv
                elif 'statute_of_limitations' in pk:
                    judicial_deadline = pv

        # Build step list
        if admin_appeal and 'no' not in str(admin_appeal).lower():
            step = {'step': 1, 'type': 'administrative', 'action': 'File administrative appeal'}
            if admin_body:
                step['body'] = admin_body
            if admin_deadline:
                step['deadline'] = admin_deadline
            steps.append(step)
        elif admin_body:
            step = {'step': 1, 'type': 'administrative', 'action': f'File complaint with {admin_body}'}
            if admin_deadline:
                step['deadline'] = admin_deadline
            steps.append(step)

        if judicial_court:
            step = {
                'step': len(steps) + 1,
                'type': 'judicial',
                'action': f'File suit in {judicial_court}',
            }
            if judicial_deadline:
                step['deadline'] = judicial_deadline
            if judicial_fees:
                step['attorneys_fees'] = judicial_fees
            steps.append(step)

        appeal_pathways.append({
            'code': code,
            'name': STATE_NAMES.get(code, code),
            'has_admin_appeal': bool(steps and steps[0].get('type') == 'administrative'),
            'steps': steps,
        })

    path = os.path.join(OUT_DIR, 'appeal_pathways.json')
    sizes['appeal_pathways.json'] = write_json(path, appeal_pathways)
    print(f'  appeal_pathways    {len(appeal_pathways):>5} records  {fmt_size(sizes["appeal_pathways.json"])}')

    # --- 8f. Scorecards ---
    # Compute transparency grade per jurisdiction based on multiple factors
    def score_deadline(days, day_type):
        """Score response deadline: shorter = better. Max 20 points."""
        if days is None:
            return 0
        cal = round(days * 1.4) if day_type == 'business' else days
        if cal <= 4: return 20
        if cal <= 7: return 17
        if cal <= 10: return 14
        if cal <= 14: return 11
        if cal <= 21: return 8
        if cal <= 30: return 5
        return 2

    def score_fees(per_page_numeric):
        """Score fee per page: lower = better. Max 15 points."""
        if per_page_numeric is None:
            return 5  # No statutory cap, but not necessarily bad
        if per_page_numeric <= 0.05: return 15
        if per_page_numeric <= 0.10: return 13
        if per_page_numeric <= 0.15: return 11
        if per_page_numeric <= 0.25: return 8
        if per_page_numeric <= 0.50: return 4
        return 2

    def score_penalties(atty_type, has_civil, has_criminal, has_per_diem):
        """Score enforcement: stronger = better. Max 15 points."""
        pts = 0
        if atty_type == 'mandatory': pts += 8
        elif atty_type in ('discretionary', 'available'): pts += 4
        if has_per_diem: pts += 4
        elif has_civil: pts += 3
        if has_criminal: pts += 3
        return min(pts, 15)

    # Build exemption count per jurisdiction for scoring
    exemption_counts = {}
    for ex in exemptions:
        j = ex.get('jurisdiction', '')
        exemption_counts[j] = exemption_counts.get(j, 0) + 1

    scorecards = []
    for code in sorted(jur_rules_map.keys()):
        jrules = jur_rules_map[code]

        # Deadline score
        dl_entry = next((d for d in deadline_rankings if d['code'] == code), None)
        dl_days = dl_entry['days'] if dl_entry else None
        dl_type = dl_entry['day_type'] if dl_entry else 'business'
        dl_score = score_deadline(dl_days, dl_type)

        # Fee score
        fee_entry = next((f for f in fee_comparison if f['code'] == code), None)
        fee_num = fee_entry['per_page_numeric'] if fee_entry else None
        fee_score = score_fees(fee_num)

        # Fee waiver: 10 points
        has_waiver = any(r.get('rule_type') == 'fee_waiver' for r in jrules)
        waiver_score = 10 if has_waiver else 0

        # Admin appeal: 10 points
        ap_entry = next((a for a in appeal_pathways if a['code'] == code), None)
        has_admin = ap_entry['has_admin_appeal'] if ap_entry else False
        appeal_score = 10 if has_admin else 0

        # Penalty score
        pen_entry = next((p for p in penalty_comparison if p['code'] == code), None)
        pen_score = score_penalties(
            pen_entry.get('attorneys_fees_type') if pen_entry else None,
            bool(pen_entry.get('civil_penalty')) if pen_entry else False,
            bool(pen_entry.get('criminal_penalty')) if pen_entry else False,
            bool(pen_entry.get('per_diem')) if pen_entry else False,
        )

        # Segregability required: 10 points
        has_segregability = any(
            r.get('rule_type') == 'initial_response' and r.get('param_key') in ('segregability_required', 'segregability')
            for r in jrules
        )
        seg_score = 10 if has_segregability else 0

        # Presumption of openness: 5 points
        has_presumption = any(
            r.get('rule_type') == 'initial_response' and r.get('param_key') in (
                'presumption_of_openness', 'disclosure_presumption', 'government_presumptive_openness',
                'balancing_test_presumption', 'constitutional_right_to_know', 'constitutional_guarantee',
            )
            for r in jrules
        )
        presump_score = 5 if has_presumption else 0

        # No ID required: 5 points
        has_no_id = any(
            r.get('rule_type') == 'initial_response' and r.get('param_key') in (
                'identity_not_required', 'purpose_not_required', 'identity_and_purpose_not_required',
                'requester_identity_not_required',
            )
            for r in jrules
        )
        no_id_score = 5 if has_no_id else 0

        # Exemption count: 0-10 points (fewer = better)
        ex_count = exemption_counts.get(code, 0)
        if ex_count <= 7: ex_score = 10
        elif ex_count <= 10: ex_score = 8
        elif ex_count <= 15: ex_score = 6
        elif ex_count <= 20: ex_score = 4
        elif ex_count <= 30: ex_score = 2
        else: ex_score = 0

        total = dl_score + fee_score + waiver_score + appeal_score + pen_score + seg_score + presump_score + no_id_score + ex_score

        if total >= 85: grade = 'A+'
        elif total >= 75: grade = 'A'
        elif total >= 65: grade = 'B+'
        elif total >= 55: grade = 'B'
        elif total >= 45: grade = 'C+'
        elif total >= 35: grade = 'C'
        elif total >= 25: grade = 'D'
        else: grade = 'F'

        # Model provisions flags
        model_provisions = []
        if dl_days and dl_days <= 3: model_provisions.append('fast_response')
        if fee_num is not None and fee_num <= 0.10: model_provisions.append('low_fees')
        if pen_entry and pen_entry.get('attorneys_fees_type') == 'mandatory': model_provisions.append('mandatory_attorney_fees')
        if pen_entry and pen_entry.get('per_diem'): model_provisions.append('per_diem_penalties')
        if has_no_id: model_provisions.append('no_id_required')
        if has_presumption: model_provisions.append('presumption_of_openness')
        if has_segregability: model_provisions.append('segregability_required')

        scorecards.append({
            'code': code,
            'name': STATE_NAMES.get(code, code),
            'grade': grade,
            'score': total,
            'max_score': 100,
            'breakdown': {
                'deadline': {'score': dl_score, 'max': 20, 'detail': f"{dl_days or 'no statutory'} {dl_type} days"},
                'fees': {'score': fee_score, 'max': 15, 'detail': f"${fee_num}/page" if fee_num else 'no cap'},
                'fee_waiver': {'score': waiver_score, 'max': 10},
                'admin_appeal': {'score': appeal_score, 'max': 10},
                'penalties': {'score': pen_score, 'max': 15},
                'segregability': {'score': seg_score, 'max': 10},
                'presumption': {'score': presump_score, 'max': 5},
                'anonymity': {'score': no_id_score, 'max': 5},
                'exemption_count': {'score': ex_score, 'max': 10, 'detail': f"{ex_count} exemptions"},
            },
            'model_provisions': model_provisions,
        })

    scorecards.sort(key=lambda x: (-x['score'], x['code']))
    path = os.path.join(OUT_DIR, 'scorecards.json')
    sizes['scorecards.json'] = write_json(path, scorecards)
    print(f'  scorecards         {len(scorecards):>5} records  {fmt_size(sizes["scorecards.json"])}')

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
