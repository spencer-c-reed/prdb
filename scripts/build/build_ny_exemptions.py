#!/usr/bin/env python3
"""Build New York FOIL exemptions catalog.

The exemptions under New York Public Officers Law § 87(2), plus related
privacy protections. FOIL's default is disclosure — exemptions are permissive,
not mandatory (except where another statute mandates withholding).

Run: python3 scripts/build/build_ny_exemptions.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

NY_EXEMPTIONS = [
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(a)',
        'exemption_number': '§ 87(2)(a)',
        'short_name': 'Statutory Exemptions',
        'category': 'statutory',
        'description': 'Protects records that are specifically exempted from disclosure by state or federal statute.',
        'scope': 'Records that are specifically exempted from disclosure by state statute, federal statute, or regulations promulgated pursuant to such statutes. Examples include certain tax records (Tax Law § 1146), grand jury materials (CPL § 190.25), and records sealed under court order.',
        'key_terms': json.dumps([
            'specifically exempted', 'state statute', 'federal statute', 'regulation',
            'sealed', 'grand jury', 'tax records', 'confidential by law',
        ]),
        'counter_arguments': json.dumps([
            'Agency must identify the specific statute that mandates confidentiality — a general confidentiality policy does not qualify',
            'The cited statute must affirmatively prohibit disclosure, not merely permit it',
            'Regulations can only qualify if they were promulgated pursuant to statutory authority that specifically authorizes withholding',
            'Challenge whether the specific record falls within the scope of the claimed exempting statute',
            'Some statutes that protect certain uses of records still allow disclosure under FOIL — read the statute carefully',
        ]),
        'notes': 'Unlike federal FOIA Exemption 3, NY § 87(2)(a) also covers exempting regulations, not just statutes. The Committee on Open Government (COOG) has issued many advisory opinions construing the scope of specific exempting statutes. See COOG Advisory Opinion 19766.',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(b)',
        'exemption_number': '§ 87(2)(b)',
        'short_name': 'Personal Privacy',
        'category': 'privacy',
        'description': 'Protects records that, if disclosed, would constitute an unwarranted invasion of personal privacy. This is a balancing test weighing the privacy interest against the public interest in disclosure.',
        'scope': 'Records that would constitute an unwarranted invasion of personal privacy. Public Officers Law § 89(2)(b) defines categories of unwarranted invasion including: employment, medical, or credit history without consent; lists of names and addresses where disclosure would be used for solicitation; information of a personal nature where disclosure would cause embarrassment. Agencies must balance the privacy interest against the legitimate public interest.',
        'key_terms': json.dumps([
            'personal privacy', 'unwarranted invasion', 'medical history', 'credit history',
            'employment history', 'personal information', 'embarrassment', 'solicitation',
            'home address', 'personal nature', 'privacy interest',
        ]),
        'counter_arguments': json.dumps([
            'NY courts apply a balancing test: the public interest in disclosure can override the privacy interest — articulate a specific public benefit',
            'Public officers and employees have reduced privacy expectations regarding their official duties and conduct',
            'The word "unwarranted" imports a balancing test — not all privacy invasions justify withholding',
            'Under § 89(2)(b)(iii), a list of names and addresses is only protected if the requester intends to use it for solicitation — agencies cannot assume bad intent',
            'Salary information for public employees is generally not protected — public payroll is a public record',
            'Disciplinary records of public employees may be disclosable under the balancing test',
            'Redaction of identifying information (name, address) while releasing substantive content is an alternative to full withholding',
            'COOG has held that the privacy exemption does not protect information voluntarily disclosed to the government in a public-facing capacity',
        ]),
        'notes': 'The most frequently invoked FOIL exemption. NY courts and COOG consistently hold that public employees have minimal privacy interests in records of their official conduct. Home addresses of private individuals generally receive stronger protection. See Matter of Gould v. New York City Police Dept., 89 N.Y.2d 267 (1996).',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(c)',
        'exemption_number': '§ 87(2)(c)',
        'short_name': 'Contract Awards',
        'category': 'commercial',
        'description': 'Protects records that, if disclosed, would impair present or imminent contract awards or collective bargaining negotiations.',
        'scope': 'Records that if disclosed would impair present or imminent: (1) contract awards, or (2) collective bargaining negotiations. The impairment must be real and demonstrable, not speculative. Once a contract is awarded or negotiations conclude, this exemption typically no longer applies.',
        'key_terms': json.dumps([
            'contract award', 'collective bargaining', 'impair', 'present', 'imminent',
            'bid', 'proposal', 'negotiation', 'procurement',
        ]),
        'counter_arguments': json.dumps([
            'This exemption is time-limited: once the contract is awarded or negotiations conclude, the exemption no longer applies',
            'Agency must show the impairment would be real and concrete, not speculative',
            'Records related to past contracts that have already been awarded are not covered',
            'If contract terms have already been made public (e.g., in a press release), the exemption may have been waived',
            'Only the specific portions that would impair negotiations need be withheld — the agency must segregate and release non-impairing portions',
        ]),
        'notes': 'Less frequently invoked than privacy or deliberative process. COOG has held that the exemption is only available when the contract award or negotiation is genuinely "present or imminent." Post-award records are generally disclosable.',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(d)',
        'exemption_number': '§ 87(2)(d)',
        'short_name': 'Trade Secrets / Commercial Information',
        'category': 'commercial',
        'description': 'Protects trade secrets or confidential commercial or financial information that, if disclosed, would cause substantial injury to the competitive position of the subject enterprise.',
        'scope': 'Trade secrets or confidential commercial or financial information submitted by a private entity to the government, where disclosure would cause substantial competitive injury to the submitting entity. The agency must consider whether the information was submitted with a reasonable expectation of confidentiality and whether disclosure would cause actual, demonstrable harm.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'financial information', 'confidential',
            'competitive position', 'substantial injury', 'proprietary', 'competitive harm',
            'submitted by private entity',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate that disclosure would cause substantial competitive injury — not just embarrassment or inconvenience',
            'Information that is publicly available elsewhere cannot be "confidential"',
            'Government-generated information is not "submitted by" a private entity and cannot qualify',
            'Financial records submitted in connection with government contracts may be disclosable to the extent they reflect public expenditures',
            'The agency, not the submitter, makes the final withholding determination — submitter objection alone is insufficient',
            'Challenge whether the records are truly "commercial or financial" rather than merely operational',
            'COOG has held that boilerplate "proprietary" markings do not establish trade secret status',
        ]),
        'notes': 'NY courts apply a "substantial injury to competitive position" standard. See Encore College Bookstores, Inc. v. Auxiliary Service Corp., 87 N.Y.2d 410 (1995). The exemption protects information submitted by private entities, not government-generated records.',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(e)',
        'exemption_number': '§ 87(2)(e)',
        'short_name': 'Law Enforcement / Inter-Agency Materials',
        'category': 'law_enforcement',
        'description': 'Protects records compiled for law enforcement purposes, and inter-agency or intra-agency materials that are not statistical or factual tabulations. Covers records that would: (i) interfere with law enforcement investigations or judicial proceedings; (ii) deprive a person of a right to a fair trial; (iii) identify a confidential source or disclose confidential information relating to a criminal investigation; (iv) reveal criminal investigative techniques or procedures; or (v) endanger the life or safety of any person.',
        'scope': 'Records compiled for law enforcement purposes which, if disclosed, would: (i) interfere with law enforcement investigations or judicial proceedings; (ii) deprive a person of a right to a fair trial or impartial adjudication; (iii) identify a confidential source or disclose confidential information relating to a criminal investigation; (iv) reveal criminal investigative techniques or procedures, except routine techniques and procedures; or (v) endanger the life or physical safety of any person.',
        'key_terms': json.dumps([
            'law enforcement', 'compiled for law enforcement', 'investigation', 'judicial proceedings',
            'fair trial', 'confidential source', 'investigative techniques', 'endanger life',
            'criminal investigation', 'interference',
        ]),
        'counter_arguments': json.dumps([
            'Records must be "compiled for law enforcement purposes" — records created for other purposes and later used in an investigation do not automatically qualify',
            'Once criminal proceedings conclude, the interference rationale under (i) typically evaporates',
            'Routine investigative techniques that are widely known do not qualify for protection under (iv)',
            'The agency must show each withheld record falls within one of the five specific harms',
            'Factual portions of investigative records may be segregable from protected deliberative or technique-revealing portions',
            'Records about closed investigations may not qualify — challenge whether the withholding rationale is still valid',
            'FOIL, unlike federal FOIA, has no Glomar-like provision — agencies cannot categorically refuse to confirm or deny record existence',
        ]),
        'notes': 'FOIL § 87(2)(e) covers law enforcement records with sub-categories (i)-(v) mirroring federal FOIA Exemption 7. NY courts have held that once proceedings conclude, the exemption typically no longer applies to interference-based withholding. See Matter of Capital Newspapers v. Burns, 67 N.Y.2d 562 (1986).',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(f)',
        'exemption_number': '§ 87(2)(f)',
        'short_name': 'Endanger Life or Safety',
        'category': 'safety',
        'description': 'Protects records that, if disclosed, would endanger the life or safety of any person.',
        'scope': 'Records that if disclosed would endanger the life or physical safety of any person. Applies broadly — not limited to law enforcement records. Frequently used to protect witness information, informant identities, and security-sensitive infrastructure data.',
        'key_terms': json.dumps([
            'endanger life', 'endanger safety', 'physical safety', 'witness', 'informant',
            'security', 'personal safety', 'threat',
        ]),
        'counter_arguments': json.dumps([
            'The endangerment must be real and concrete, not speculative or hypothetical',
            'General concerns about "safety" without specific, articulable risk are insufficient',
            'Challenge whether the specific information in the record (vs. the record generally) creates the safety risk',
            'Redaction of identifying information may eliminate the safety concern while permitting disclosure of substantive content',
            'COOG has held that agencies cannot invoke this exemption based solely on a requester\'s stated purpose',
        ]),
        'notes': 'Standalone safety exemption, distinct from the law enforcement exemption. COOG has held that the threat must be real and specific. Commonly used to protect the names and addresses of domestic violence victims and witnesses in criminal proceedings.',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(g)',
        'exemption_number': '§ 87(2)(g)',
        'short_name': 'Intra/Inter-Agency Materials',
        'category': 'deliberative',
        'description': 'Protects inter-agency or intra-agency materials that are not (i) statistical or factual tabulations or data; (ii) instructions to staff that affect the public; (iii) final agency policy or determinations; or (iv) external audits. Encompasses the deliberative process privilege and attorney-client privilege.',
        'scope': 'Inter-agency or intra-agency materials that are: not statistical or factual tabulations; not instructions to staff that affect the public; not final agency policy or determinations; and not external audits. Protects drafts, recommendations, pre-decisional deliberations, and privileged communications. Factual portions must be segregated and released.',
        'key_terms': json.dumps([
            'inter-agency', 'intra-agency', 'deliberative process', 'predecisional', 'draft',
            'recommendation', 'attorney-client', 'work product', 'internal memorandum',
            'advisory', 'preliminary', 'opinion', 'deliberation',
        ]),
        'counter_arguments': json.dumps([
            'FOIL expressly excludes from protection: (i) statistical or factual tabulations, (ii) instructions to staff affecting the public, (iii) final policy or determinations, and (iv) external audits — these must be released',
            'Factual material embedded in a deliberative document must be segregated and released',
            'A document adopted as final agency policy loses its predecisional character even if it was once a draft',
            '"Working law" — internal rules and policies that guide agency action — must be disclosed',
            'Agencies cannot shield records simply by labeling them "draft" if they reflect a final decision',
            'Attorney-client privilege in the government context is narrower than in private litigation — courts have required disclosure of legal advice that reflects final agency policy',
            'COOG has held that instructions to staff that affect the public (e.g., enforcement guidelines) must be disclosed under § 87(2)(g)(ii)',
        ]),
        'notes': 'The NY equivalent of federal FOIA Exemption 5. A key distinction: FOIL § 87(2)(g) has explicit carve-outs that must be disclosed regardless of their deliberative character. The "working law" doctrine requires agencies to disclose policies that guide their decisions, even if internal. See Matter of Gould v. NYPD, 89 N.Y.2d 267 (1996).',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(h)',
        'exemption_number': '§ 87(2)(h)',
        'short_name': 'Examination Questions',
        'category': 'examination',
        'description': 'Protects examination questions or answers that are requested prior to the final administration of such questions.',
        'scope': 'Examination questions or answers that are requested prior to the final administration of such questions. Once an examination has been finally administered (and is no longer in use), the rationale for withholding typically disappears. Applies to civil service, licensing, and similar examinations.',
        'key_terms': json.dumps([
            'examination', 'test questions', 'answers', 'prior to administration', 'civil service',
            'licensing exam', 'standardized test',
        ]),
        'counter_arguments': json.dumps([
            'Once the examination has been finally administered and is no longer in use, the exemption no longer applies',
            'Challenge whether the examination is "prior to final administration" — if the test has been given, the justification is gone',
            'Post-administration disclosure of past questions is often required — challenge any continuing withholding after the exam cycle ends',
            'Scoring rubrics and grading policies may not be "questions or answers" and could be disclosable',
        ]),
        'notes': 'Narrow exemption designed to protect the integrity of testing programs. COOG has held that the exemption ends once the examination is finally administered and retired from use.',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(i)',
        'exemption_number': '§ 87(2)(i)',
        'short_name': 'Computer Access Information',
        'category': 'security',
        'description': 'Protects computer access codes (passwords, security credentials, and similar access control information).',
        'scope': 'Computer access codes, passwords, security credentials, encryption keys, and similar information whose disclosure would allow unauthorized access to government computer systems. Intended to protect government cybersecurity, not to shield the existence or substance of electronic records.',
        'key_terms': json.dumps([
            'computer access', 'password', 'access code', 'security credential', 'encryption key',
            'cybersecurity', 'system access', 'login',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects access credentials, not the underlying records stored on computer systems',
            'An agency cannot withhold an entire electronic record on the ground that it exists in a computer system',
            'Challenge attempts to use this exemption as a pretext to avoid producing electronic records',
            'The exemption does not apply to metadata about records or system logs that do not reveal access credentials',
        ]),
        'notes': 'Narrow exemption protecting cybersecurity credentials. COOG has clarified that this exemption cannot be used to justify withholding electronic records simply because they are stored digitally. The exemption covers only the access credentials themselves.',
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': "N.Y. Pub. Off. Law § 87(2)(j) (\"Tina's Law\")",
        'exemption_number': '§ 87(2)(j)',
        'short_name': "Photographs/Videos of Deceased (Tina's Law)",
        'category': 'privacy',
        'description': "Protects photographs, videos, or audio recordings of the body or remains of a deceased person, enacted as Tina's Law. Protects the dignity of deceased persons and the privacy of families.",
        'scope': "Photographs, videos, and audio recordings of the body or remains of a deceased person, or recordings made during an autopsy. Enacted as Tina's Law after the publicized release of autopsy photos of Tina Crouse. Applies to law enforcement and medical examiner records. Does not protect investigative records generally — only the recordings themselves.",
        'key_terms': json.dumps([
            'photograph', 'video', 'audio recording', 'deceased', 'body', 'remains', 'autopsy',
            "Tina's Law", 'death images', 'crime scene photos',
        ]),
        'counter_arguments': json.dumps([
            "The exemption covers photographs and recordings of the body, not investigative reports or written records about the death",
            'Incident reports, autopsy reports (text), and other written records about a death are not covered by this exemption',
            'Challenge attempts to use this exemption to withhold non-photographic records related to a death investigation',
            "Courts have applied the exemption narrowly to its stated scope — recordings of the body, not all records related to the deceased",
        ]),
        'notes': "Enacted in 1999 as 'Tina's Law' (ch. 356, Laws of 1999) after posthumous publication of crime victim photos. One of the more recently added FOIL exemptions. Applies to all agencies holding such recordings, including police, fire departments, and medical examiners.",
    },
    {
        'jurisdiction': 'NY',
        'statute_citation': 'N.Y. Pub. Off. Law § 87(2)(b); § 89(2)',
        'exemption_number': '§ 87(2)(b) / § 89(2)',
        'short_name': 'Personal Privacy — Detailed Sub-categories',
        'category': 'privacy',
        'description': 'Detailed sub-categories of the personal privacy exemption under § 89(2)(b), enumerating specific types of records that constitute unwarranted invasions of personal privacy.',
        'scope': 'Under § 89(2)(b), unwarranted invasions of personal privacy include but are not limited to: (i) disclosure of employment, medical, financial, credit, or personal history of any person; (ii) disclosure of items involving the medical or personal records of a client or patient; (iii) sale or release of lists of names and addresses if the lists would be used for solicitation or fund-raising; (iv) disclosure of information of a personal nature relating to employees or elected officials if such disclosure would constitute harassment of the individual or result in an unwarranted invasion of personal privacy; (v) disclosure of the home address, personal telephone number, or other information that would tend to identify where any individual can be located when the disclosure is likely to endanger the safety of the individual.',
        'key_terms': json.dumps([
            'employment history', 'medical records', 'financial records', 'credit history',
            'personal history', 'client records', 'patient records', 'mailing list', 'solicitation',
            'home address', 'personal telephone', 'harassment', 'personal nature',
        ]),
        'counter_arguments': json.dumps([
            'Public employees have no privacy interest in their official duties, salaries, or professional conduct',
            'The § 89(2)(b) categories are illustrative, not exhaustive, but agencies cannot withhold records that fall outside the enumerated privacy interests',
            'The solicitation rationale under (iii) requires agency to show actual solicitation intent — speculative misuse is insufficient',
            'Court-ordered disclosure, disclosure pursuant to law, or disclosure at the subject\'s request removes the privacy protection',
            'Records about elected officials in their official capacity carry minimal privacy protection — public accountability outweighs privacy',
        ]),
        'notes': 'Section 89(2) expands on the privacy exemption in § 87(2)(b) by providing concrete examples. COOG advisory opinions have consistently held that public employees\' salaries, titles, and disciplinary records in their official capacity are disclosable.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for exemption in NY_EXEMPTIONS:
            existing = conn.execute(
                'SELECT id FROM exemptions WHERE jurisdiction = ? AND statute_citation = ?',
                (exemption['jurisdiction'], exemption['statute_citation'])
            ).fetchone()

            if existing:
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
    print(f'NY FOIL exemptions: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_ny_exemptions', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
