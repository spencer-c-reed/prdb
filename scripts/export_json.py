#!/usr/bin/env python3
"""Export PRDB database to static JSON files for the web interface."""

import json
import os
import sqlite3
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'prdb.db')
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web', 'public', 'data')

os.makedirs(OUT_DIR, exist_ok=True)


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def export():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory

    # Exemptions — parse JSON fields
    exemptions = conn.execute('''
        SELECT id, jurisdiction, exemption_number, title, description, scope,
               key_terms, counter_arguments, statute_citation, notes
        FROM exemptions ORDER BY jurisdiction, exemption_number
    ''').fetchall()
    for ex in exemptions:
        for field in ('key_terms', 'counter_arguments'):
            if ex[field]:
                try:
                    ex[field] = json.loads(ex[field])
                except (json.JSONDecodeError, TypeError):
                    pass
    with open(os.path.join(OUT_DIR, 'exemptions.json'), 'w') as f:
        json.dump(exemptions, f, separators=(',', ':'))
    print(f'Exported {len(exemptions)} exemptions')

    # Response rules
    rules = conn.execute('''
        SELECT id, jurisdiction, rule_type, rule_name, description,
               deadline_days, deadline_type, statute_citation, notes
        FROM response_rules ORDER BY jurisdiction, rule_type
    ''').fetchall()
    with open(os.path.join(OUT_DIR, 'rules.json'), 'w') as f:
        json.dump(rules, f, separators=(',', ':'))
    print(f'Exported {len(rules)} rules')

    # Templates — parse JSON fields
    templates = conn.execute('''
        SELECT id, jurisdiction, template_name, record_type, body,
               fee_waiver_language, expedited_language, notes
        FROM request_templates ORDER BY jurisdiction, template_name
    ''').fetchall()
    with open(os.path.join(OUT_DIR, 'templates.json'), 'w') as f:
        json.dump(templates, f, separators=(',', ':'))
    print(f'Exported {len(templates)} templates')

    # Agencies
    agencies = conn.execute('''
        SELECT id, name, abbreviation, jurisdiction, level,
               parent_agency, foia_officer, email, phone,
               address, portal_url, submission_methods,
               fee_schedule, fee_waiver_criteria, notes
        FROM agencies ORDER BY jurisdiction, name
    ''').fetchall()
    for ag in agencies:
        for field in ('submission_methods',):
            if ag[field]:
                try:
                    ag[field] = json.loads(ag[field])
                except (json.JSONDecodeError, TypeError):
                    pass
    with open(os.path.join(OUT_DIR, 'agencies.json'), 'w') as f:
        json.dump(agencies, f, separators=(',', ':'))
    print(f'Exported {len(agencies)} agencies')

    # Jurisdiction summary — aggregate stats for the overview page
    jurisdictions = []
    for row in conn.execute('SELECT DISTINCT jurisdiction FROM exemptions ORDER BY jurisdiction'):
        j = row['jurisdiction']
        stats = {
            'jurisdiction': j,
            'exemptions': conn.execute('SELECT COUNT(*) as c FROM exemptions WHERE jurisdiction=?', (j,)).fetchone()['c'],
            'rules': conn.execute('SELECT COUNT(*) as c FROM response_rules WHERE jurisdiction=?', (j,)).fetchone()['c'],
            'templates': conn.execute('SELECT COUNT(*) as c FROM request_templates WHERE jurisdiction=?', (j,)).fetchone()['c'],
        }

        # Get key rules for quick reference
        deadline_row = conn.execute(
            "SELECT deadline_days, deadline_type, description FROM response_rules WHERE jurisdiction=? AND rule_type='initial_response' LIMIT 1",
            (j,)
        ).fetchone()
        if deadline_row:
            stats['response_deadline'] = deadline_row['description']
            stats['response_days'] = deadline_row['deadline_days']
            stats['response_type'] = deadline_row['deadline_type']

        fee_row = conn.execute(
            "SELECT description FROM response_rules WHERE jurisdiction=? AND rule_type='fee_cap' LIMIT 1",
            (j,)
        ).fetchone()
        if fee_row:
            stats['fee_info'] = fee_row['description']

        appeal_row = conn.execute(
            "SELECT description FROM response_rules WHERE jurisdiction=? AND rule_type='appeal_deadline' LIMIT 1",
            (j,)
        ).fetchone()
        if appeal_row:
            stats['appeal_info'] = appeal_row['description']

        jurisdictions.append(stats)

    with open(os.path.join(OUT_DIR, 'jurisdictions.json'), 'w') as f:
        json.dump(jurisdictions, f, separators=(',', ':'))
    print(f'Exported {len(jurisdictions)} jurisdiction summaries')

    # Global stats
    stats = {
        'documents': conn.execute('SELECT COUNT(*) as c FROM documents').fetchone()['c'],
        'exemptions': len(exemptions),
        'rules': len(rules),
        'templates': len(templates),
        'agencies': len(agencies),
        'jurisdictions': len(jurisdictions),
    }
    with open(os.path.join(OUT_DIR, 'stats.json'), 'w') as f:
        json.dump(stats, f, separators=(',', ':'))
    print(f'Exported stats: {stats}')

    conn.close()
    print('Done.')


if __name__ == '__main__':
    export()
