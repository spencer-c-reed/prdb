#!/usr/bin/env python3
"""Build government contracts request templates for states missing them."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

# State statutes for reference
STATUTES = {
    'AK': 'AS 40.25.110', 'AR': 'Ark. Code § 25-19-105', 'AZ': 'A.R.S. § 39-121',
    'CA': 'Cal. Gov. Code § 7920.000 et seq.', 'CT': 'Conn. Gen. Stat. § 1-200 et seq.',
    'DC': 'D.C. Code § 2-531 et seq.', 'FL': 'Fla. Stat. § 119.07',
    'GA': 'O.C.G.A. § 50-18-70', 'HI': 'HRS § 92F-11', 'ID': 'Idaho Code § 74-101',
    'IL': '5 ILCS 140/1', 'MA': 'M.G.L. c. 66, § 10', 'ME': '1 M.R.S.A. § 408',
    'MI': 'MCL 15.231', 'MN': 'Minn. Stat. § 13.01', 'MO': 'Mo. Rev. Stat. § 610.010',
    'MT': 'Mont. Code § 2-6-1002', 'NC': 'N.C.G.S. § 132-1', 'ND': 'N.D.C.C. § 44-04-18',
    'NE': 'Neb. Rev. Stat. § 84-712', 'NH': 'RSA 91-A:4', 'NM': 'NMSA § 14-2-1',
    'PA': '65 P.S. § 67.101', 'RI': 'R.I.G.L. § 38-2-1', 'SC': 'S.C. Code § 30-4-10',
    'UT': 'Utah Code § 63G-2-201', 'VT': '1 V.S.A. § 315', 'WA': 'RCW 42.56.010',
    'WY': 'Wyo. Stat. § 16-4-202',
}

TEMPLATES = []
for jur, statute in STATUTES.items():
    TEMPLATES.append({
        'jurisdiction': jur,
        'record_type': 'government_contracts',
        'template_name': f'{jur} — Government Contracts and Procurement Records Request',
        'template_text': f"""{{{{requester_name}}}}
{{{{requester_address}}}}
{{{{requester_email}}}}

{{{{date}}}}

{{{{records_officer_name}}}}
{{{{agency_name}}}}
{{{{agency_address}}}}

Re: Public Records Request — Government Contracts and Procurement

Dear {{{{records_officer_name}}}}:

Pursuant to {statute}, I am requesting copies of the following records:

1. All contracts, agreements, and memoranda of understanding between {{{{agency_name}}}} and {{{{contractor_name_or_description}}}} for the period {{{{start_date}}}} through {{{{end_date}}}}.

2. All bids, proposals, and responses received in connection with {{{{solicitation_number_or_description}}}}.

3. The complete procurement file for {{{{contract_description}}}}, including but not limited to:
   - The request for proposals (RFP) or invitation to bid (ITB)
   - All submitted proposals or bids
   - Evaluation criteria and scoring sheets
   - Award recommendation memoranda
   - The executed contract including all amendments and change orders

4. All invoices, payment records, and expenditure reports related to {{{{contract_description}}}} for the period {{{{start_date}}}} through {{{{end_date}}}}.

5. Any performance evaluations, audit reports, or compliance reviews related to {{{{contractor_name_or_description}}}}.

I request records in electronic format where available. If any records are withheld, please cite the specific statutory exemption and provide all reasonably segregable non-exempt portions.

{{{{fee_waiver_language}}}}

Thank you for your prompt attention to this request.

Sincerely,
{{{{requester_name}}}}""",
        'notes': f'Government contracts and procurement records are generally public records under {statute}. Trade secrets or proprietary information in bids may be partially exempt in some states, but the contract itself, pricing, and performance records are almost always public.',
    })

def build():
    conn = db_connect(DB_PATH)
    for t in TEMPLATES:
        existing = conn.execute(
            "SELECT id FROM request_templates WHERE jurisdiction=? AND record_type='government_contracts'",
            (t['jurisdiction'],)
        ).fetchone()
        if existing:
            print(f"  {t['jurisdiction']}: contracts template already exists, skipping")
            continue
        conn.execute('''
            INSERT INTO request_templates (jurisdiction, record_type, template_name, template_text, notes)
            VALUES (:jurisdiction, :record_type, :template_name, :template_text, :notes)
        ''', t)
        print(f"  {t['jurisdiction']}: inserted")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    build()
