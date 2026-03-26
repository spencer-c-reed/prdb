#!/usr/bin/env python3
"""Build the federal FOIA exemptions catalog.

The 9 FOIA exemptions (5 U.S.C. § 552(b)(1)-(9)) plus 3 exclusions (c)(1)-(3).
These are well-established and change rarely. Data sourced from the statute text,
DOJ guidance, and settled case law.

Run: python3 scripts/build/build_federal_exemptions.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

FEDERAL_EXEMPTIONS = [
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(1)',
        'exemption_number': 'Exemption 1',
        'short_name': 'National Security',
        'category': 'national_security',
        'description': 'Protects information that is classified to protect national security. The material must be properly classified under the criteria established by an Executive Order.',
        'scope': 'Information specifically authorized under criteria established by an Executive Order to be kept secret in the interest of national defense or foreign policy and is in fact properly classified pursuant to such Executive Order.',
        'key_terms': json.dumps(['classified', 'national security', 'national defense', 'foreign policy', 'secret', 'top secret', 'confidential', 'executive order']),
        'counter_arguments': json.dumps([
            'Challenge whether the information was properly classified under the applicable Executive Order',
            'Argue that classification was applied to conceal violations of law, inefficiency, or administrative error (prohibited by E.O. 13526 § 1.7)',
            'Request Vaughn index to verify classification is proper and not over-broad',
            'Argue information has been officially acknowledged or is in the public domain',
            'Challenge on segregability grounds — non-classified portions must be released',
        ]),
        'notes': 'Agencies bear the burden of proving classification is proper. Courts review de novo but give some deference to agency classification decisions. See EPA v. Mink, 410 U.S. 73 (1973).',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(2)',
        'exemption_number': 'Exemption 2',
        'short_name': 'Internal Personnel Rules',
        'category': 'internal_rules',
        'description': 'Protects records related solely to the internal personnel rules and practices of an agency. After Milner v. Dep\'t of Navy (2011), this is limited to records relating to human resources matters.',
        'scope': 'Records related solely to the internal personnel rules and practices of an agency, such as rules on lunch breaks, parking, and internal personnel procedures.',
        'key_terms': json.dumps(['internal rules', 'personnel rules', 'internal practices', 'human resources', 'employee handbook', 'internal procedures']),
        'counter_arguments': json.dumps([
            'After Milner v. Dep\'t of Navy, 562 U.S. 562 (2011), this exemption is narrowly construed to apply only to internal HR-type rules',
            'Agencies can no longer invoke "High 2" to protect law enforcement techniques — those must be claimed under Exemption 7(E) instead',
            'Records that affect the public or regulate public behavior are not "solely internal"',
            'Challenge whether the records truly relate to personnel rules vs. substantive policy',
        ]),
        'notes': 'Significantly narrowed by Milner v. Dep\'t of Navy, 562 U.S. 562 (2011), which eliminated the "High 2" doctrine that agencies had used to protect law enforcement techniques.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(3)',
        'exemption_number': 'Exemption 3',
        'short_name': 'Statutory Exemptions',
        'category': 'statutory',
        'description': 'Protects information specifically exempted from disclosure by another federal statute, provided that statute either requires withholding in a non-discretionary manner or establishes particular criteria for withholding.',
        'scope': 'Information specifically exempted from disclosure by statute (other than FOIA), provided that the statute: (A) requires that the matters be withheld in such a manner as to leave no discretion on the issue; or (B) establishes particular criteria for withholding or refers to particular types of matters to be withheld; and (C) if enacted after October 28, 2009, specifically cites 5 U.S.C. § 552(b)(3).',
        'key_terms': json.dumps(['statutory exemption', 'other statute', 'nondiscretionary', 'specific criteria', 'particular types']),
        'counter_arguments': json.dumps([
            'Challenge whether the cited statute actually qualifies as an Exemption 3 statute (must meet the precise criteria)',
            'Post-2009 statutes must specifically cite § 552(b)(3) to qualify — check the statute text',
            'Even if the statute qualifies, argue the specific records don\'t fall within its scope',
            'Request segregation of non-exempt portions',
            'Some "Exemption 3 statutes" have been narrowly construed by courts — research the specific statute\'s case law',
        ]),
        'notes': 'Over 100 federal statutes have been recognized as Exemption 3 statutes. Common examples include: IRC § 6103 (tax returns), 50 U.S.C. § 3024(i)(1) (intelligence sources/methods), 13 U.S.C. § 9 (census data).',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(4)',
        'exemption_number': 'Exemption 4',
        'short_name': 'Trade Secrets / Commercial Information',
        'category': 'commercial',
        'description': 'Protects trade secrets and commercial or financial information obtained from a person that is privileged or confidential.',
        'scope': 'Trade secrets and commercial or financial information obtained from a person and privileged or confidential.',
        'key_terms': json.dumps(['trade secret', 'commercial information', 'financial information', 'confidential', 'proprietary', 'competitive harm', 'submitter']),
        'counter_arguments': json.dumps([
            'After Food Marketing Institute v. Argus Leader Media, 139 S. Ct. 2356 (2019), information is "confidential" if customarily kept private or if the government provided an express or implied assurance of confidentiality',
            'Challenge whether the information is truly "commercial or financial" — must have a commercial character',
            'Information that is publicly available elsewhere cannot be "confidential"',
            'Government-generated information is not "obtained from a person" and cannot qualify',
            'Request segregation — not all data in a commercial document is necessarily confidential',
            'Invoke Executive Order 12600 submitter notice procedures to challenge the submitter\'s claims',
        ]),
        'notes': 'Standard changed significantly by Food Marketing Institute v. Argus Leader Media, 139 S. Ct. 2356 (2019), which broadened the definition of "confidential." Previously the National Parks test (substantial competitive harm) applied.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(5)',
        'exemption_number': 'Exemption 5',
        'short_name': 'Deliberative Process / Privileged',
        'category': 'deliberative',
        'description': 'Protects inter-agency or intra-agency memorandums or letters that would not be available by law to a party in litigation with the agency. Encompasses the deliberative process privilege, attorney-client privilege, and attorney work-product privilege.',
        'scope': 'Inter-agency or intra-agency memorandums or letters that would not be available by law to a party other than an agency in litigation with the agency. Covers three distinct privileges: (1) deliberative process, (2) attorney-client, (3) attorney work product.',
        'key_terms': json.dumps(['deliberative process', 'predecisional', 'draft', 'recommendation', 'inter-agency', 'intra-agency', 'attorney-client', 'work product', 'privilege', 'advisory opinion']),
        'counter_arguments': json.dumps([
            'The document must be both predecisional AND deliberative — factual portions are not protected',
            'Final opinions, working law, and statements of policy must be released even if they were once deliberative',
            'Records adopted as agency policy lose their predecisional character',
            'The deliberative process privilege is a qualified privilege — government misconduct or need can override it',
            'Request segregation of factual material from deliberative portions',
            'Challenge the agency\'s characterization of documents as "predecisional" — are they truly before a decision?',
            'Under FOIA Improvement Act of 2016 (§ 552(a)(8)), agencies may not withhold under Exemption 5 if the records are 25+ years old',
        ]),
        'notes': 'Most commonly invoked exemption. The 2016 FOIA Improvement Act added a 25-year sunset: deliberative process privilege cannot be invoked for records created 25+ years before the FOIA request.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(6)',
        'exemption_number': 'Exemption 6',
        'short_name': 'Personal Privacy',
        'category': 'privacy',
        'description': 'Protects information about individuals in personnel, medical, and similar files when disclosure would constitute a clearly unwarranted invasion of personal privacy.',
        'scope': 'Personnel and medical files and similar files the disclosure of which would constitute a clearly unwarranted invasion of personal privacy.',
        'key_terms': json.dumps(['personal privacy', 'personnel file', 'medical file', 'similar files', 'unwarranted invasion', 'privacy interest', 'public interest']),
        'counter_arguments': json.dumps([
            'The standard is "clearly unwarranted" — the balance tips in favor of disclosure',
            'Argue the public interest in disclosure outweighs the privacy interest (balancing test)',
            'The public interest must be in shedding light on government operations — purely private curiosity doesn\'t count',
            'Public officials have reduced privacy expectations in their official capacity',
            'Request redaction of identifying information rather than full withholding — the substance can often be released with names removed',
            'Information already publicly available has minimal privacy interest',
            'Challenge whether the files are truly "personnel, medical, or similar" files',
        ]),
        'notes': 'Balancing test: courts weigh the individual\'s privacy interest against the public interest in disclosure. The public interest must relate to FOIA\'s purpose of shedding light on government operations.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(7)',
        'exemption_number': 'Exemption 7',
        'short_name': 'Law Enforcement',
        'category': 'law_enforcement',
        'description': 'Protects records or information compiled for law enforcement purposes, but only to the extent that disclosure would cause one of six specified harms.',
        'scope': 'Records or information compiled for law enforcement purposes, but only to the extent that the production of such law enforcement records or information: (A) could reasonably be expected to interfere with enforcement proceedings; (B) would deprive a person of a right to a fair trial or an impartial adjudication; (C) could reasonably be expected to constitute an unwarranted invasion of personal privacy; (D) could reasonably be expected to disclose the identity of a confidential source; (E) would disclose techniques and procedures for law enforcement investigations or prosecutions, or would disclose guidelines for law enforcement investigations or prosecutions if such disclosure could reasonably be expected to risk circumvention of the law; (F) could reasonably be expected to endanger the life or physical safety of any individual.',
        'key_terms': json.dumps(['law enforcement', 'enforcement proceedings', 'fair trial', 'confidential source', 'techniques and procedures', 'endanger life', 'safety', 'investigation', 'prosecution', 'compiled for']),
        'counter_arguments': json.dumps([
            'Threshold requirement: records must be "compiled for law enforcement purposes" — records created for other purposes and later placed in a law enforcement file may not qualify',
            'The agency must demonstrate one of the six specific harms (A through F) — general claims of harm are insufficient',
            '7(A) only applies during pending or reasonably anticipated enforcement proceedings — once proceedings conclude, this harm typically no longer applies',
            '7(C) uses "could reasonably be expected" standard (lower than Exemption 6\'s "clearly unwarranted")',
            '7(E) after Milner only protects techniques whose disclosure would risk circumvention — routine techniques widely known do not qualify',
            'Request segregation — factual information can often be separated from protected information',
            'Challenge whether the records were truly compiled for law enforcement (vs. regulatory/administrative) purposes',
        ]),
        'notes': 'Has six sub-exemptions (A through F), each protecting against a different type of harm. Agency must satisfy both the threshold (compiled for law enforcement) and one of the harms.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(8)',
        'exemption_number': 'Exemption 8',
        'short_name': 'Financial Institutions',
        'category': 'financial',
        'description': 'Protects matters contained in or related to examination, operating, or condition reports prepared by, on behalf of, or for the use of an agency responsible for regulating or supervising financial institutions.',
        'scope': 'Matters that are contained in or related to examination, operating, or condition reports prepared by, on behalf of, or for the use of an agency responsible for the regulation or supervision of financial institutions.',
        'key_terms': json.dumps(['financial institution', 'bank', 'examination report', 'operating report', 'condition report', 'regulation', 'supervision', 'OCC', 'FDIC', 'Federal Reserve']),
        'counter_arguments': json.dumps([
            'This exemption is rarely litigated and broadly construed — challenges are difficult',
            'Argue that the records are not "related to" examination or condition reports',
            'Challenge whether the agency is truly responsible for "regulating or supervising" financial institutions',
            'Records created independently of the examination process may not qualify',
            'Request non-exempt portions to be segregated and released',
        ]),
        'notes': 'Broadly construed by courts. Intended to protect the security of financial institutions and the integrity of the regulatory examination process. Rarely successfully challenged.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(b)(9)',
        'exemption_number': 'Exemption 9',
        'short_name': 'Geological / Geophysical Wells',
        'category': 'geological',
        'description': 'Protects geological and geophysical information and data, including maps, concerning wells.',
        'scope': 'Geological and geophysical information and data, including maps, concerning wells.',
        'key_terms': json.dumps(['geological', 'geophysical', 'wells', 'oil', 'gas', 'mineral', 'maps', 'drilling']),
        'counter_arguments': json.dumps([
            'This exemption is extremely narrow — applies only to well data',
            'Non-well geological/geophysical data (e.g., earthquake, environmental data) does not qualify',
            'Information about wells that does not reveal geological/geophysical characteristics may not qualify',
            'Challenge the characterization of data as "concerning wells"',
        ]),
        'notes': 'Narrowest FOIA exemption. Rarely invoked. Intended to protect the competitive position of private oil and gas companies that submit well data to the government.',
    },
    # Exclusions
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(c)(1)',
        'exemption_number': 'Exclusion (c)(1)',
        'short_name': 'Law Enforcement - Ongoing Investigation',
        'category': 'exclusion',
        'description': 'Permits agencies to treat certain law enforcement records as not subject to FOIA when acknowledging their existence would tip off a target of an ongoing investigation.',
        'scope': 'Records subject to Exemption 7(A) pertaining to a pending criminal law enforcement investigation, where there is reason to believe the subject of the investigation is not aware of it, and disclosure could reasonably be expected to interfere with enforcement proceedings.',
        'key_terms': json.dumps(['exclusion', 'ongoing investigation', 'criminal', 'tip off', 'not aware']),
        'counter_arguments': json.dumps([
            'Exclusions are extremely difficult to challenge because the agency need not even acknowledge the records exist',
            'If you suspect an exclusion, file a complaint with OGIS or the agency Inspector General',
            'FOIA requires annual reporting of exclusion use — check the agency\'s annual FOIA report',
        ]),
        'notes': 'Unlike exemptions, exclusions allow agencies to respond as if records do not exist. This is a Glomar-like response but authorized by statute.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(c)(2)',
        'exemption_number': 'Exclusion (c)(2)',
        'short_name': 'Confidential Informant Records',
        'category': 'exclusion',
        'description': 'Permits agencies to treat informant records maintained by criminal law enforcement agencies as not subject to FOIA, unless the informant\'s status has been officially confirmed.',
        'scope': 'Records maintained by a criminal law enforcement agency under an informant\'s name or personal identifier, unless the informant\'s status as an informant has been officially confirmed.',
        'key_terms': json.dumps(['informant', 'confidential informant', 'criminal law enforcement', 'officially confirmed']),
        'counter_arguments': json.dumps([
            'If the informant\'s status has been officially confirmed, this exclusion no longer applies',
            'Only applies to criminal law enforcement agencies — not regulatory or civil enforcement',
        ]),
        'notes': 'Protects the identity and records of confidential informants in criminal law enforcement.',
    },
    {
        'jurisdiction': 'federal',
        'statute_citation': '5 U.S.C. § 552(c)(3)',
        'exemption_number': 'Exclusion (c)(3)',
        'short_name': 'FBI Foreign Intelligence / Terrorism',
        'category': 'exclusion',
        'description': 'Permits the FBI to treat certain foreign intelligence or international terrorism records as not subject to FOIA.',
        'scope': 'Records maintained by the FBI pertaining to foreign intelligence or counterintelligence, or international terrorism, when the existence of the records is classified.',
        'key_terms': json.dumps(['FBI', 'foreign intelligence', 'counterintelligence', 'international terrorism', 'classified']),
        'counter_arguments': json.dumps([
            'Only applies to the FBI, not other agencies',
            'Only applies when the existence of the records is classified',
            'If the subject matter has been publicly acknowledged, the exclusion may not apply',
        ]),
        'notes': 'Limited to the FBI and classified records relating to foreign intelligence, counterintelligence, or international terrorism.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for exemption in FEDERAL_EXEMPTIONS:
            # Check if already exists
            existing = conn.execute(
                'SELECT id FROM exemptions WHERE jurisdiction = ? AND statute_citation = ?',
                (exemption['jurisdiction'], exemption['statute_citation'])
            ).fetchone()

            if existing:
                # Update
                conn.execute(
                    '''
                    UPDATE exemptions SET
                        exemption_number = ?,
                        short_name = ?,
                        category = ?,
                        description = ?,
                        scope = ?,
                        key_terms = ?,
                        counter_arguments = ?,
                        notes = ?,
                        last_verified = datetime('now'),
                        updated_at = datetime('now')
                    WHERE id = ?
                    ''',
                    (
                        exemption['exemption_number'],
                        exemption['short_name'],
                        exemption['category'],
                        exemption['description'],
                        exemption['scope'],
                        exemption['key_terms'],
                        exemption['counter_arguments'],
                        exemption['notes'],
                        existing[0],
                    )
                )
                skipped += 1
            else:
                conn.execute(
                    '''
                    INSERT INTO exemptions (
                        jurisdiction, statute_citation, exemption_number,
                        short_name, category, description, scope,
                        key_terms, counter_arguments, notes, last_verified
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                    ''',
                    (
                        exemption['jurisdiction'],
                        exemption['statute_citation'],
                        exemption['exemption_number'],
                        exemption['short_name'],
                        exemption['category'],
                        exemption['description'],
                        exemption['scope'],
                        exemption['key_terms'],
                        exemption['counter_arguments'],
                        exemption['notes'],
                    )
                )
                added += 1

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'Federal exemptions: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_federal_exemptions', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
