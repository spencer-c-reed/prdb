#!/usr/bin/env python3
"""Build the California Public Records Act (CPRA) exemptions catalog.

California Government Code §§ 7920-7931 (as renumbered effective January 1, 2023
by Stats. 2021, Ch. 614 (SB 92)). Prior citations from the old § 6250-6270 series
are noted where relevant for cross-referencing legacy case law.

Run: python3 scripts/build/build_ca_exemptions.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

CA_EXEMPTIONS = [
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7927.500',
        'exemption_number': '§ 7927.500',
        'short_name': 'Preliminary Drafts and Notes',
        'category': 'deliberative',
        'description': 'Protects preliminary drafts, notes, and interagency or intra-agency memoranda that are not retained by the public agency in the ordinary course of business, where the public interest in withholding clearly outweighs the public interest in disclosure.',
        'scope': 'Preliminary drafts, notes, and interagency or intra-agency memoranda that are not retained by the agency in the ordinary course of business, provided the agency can demonstrate the public interest in withholding outweighs disclosure. Formerly Gov. Code § 6254(a).',
        'key_terms': json.dumps(['preliminary draft', 'draft', 'notes', 'interagency memoranda', 'intra-agency', 'working papers', 'pre-decisional']),
        'counter_arguments': json.dumps([
            'Unlike federal deliberative process, California law places burden on agency to show public interest in withholding outweighs disclosure — affirmative showing required',
            'Records retained in the ordinary course of business are not protected, even if labeled "draft"',
            'Once a draft becomes the basis for agency action or is adopted, it loses protection',
            'Final reports, recommendations, and policies adopted by the agency must be disclosed even if earlier drafts are exempt',
            'Purely factual portions of drafts are not protected — only the deliberative, opinion-forming content',
            'Challenge whether the agency actually retains similar documents, negating the "not retained in ordinary course" qualifier',
            'Agency must affirmatively demonstrate the public interest in withholding — a conclusory claim is insufficient under City of San Jose v. Superior Court (1974)',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(a). This exemption is discretionary, not mandatory — the agency "may" withhold but is not required to. California courts have held that final documents that were once drafts must be disclosed if retained in the ordinary course of business. See Times Mirror Co. v. Superior Court (1991).',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7923.600',
        'exemption_number': '§ 7923.600',
        'short_name': 'Law Enforcement Investigatory Records',
        'category': 'law_enforcement',
        'description': 'Protects records of investigations conducted by law enforcement agencies and investigatory files compiled for law enforcement purposes. This is one of the most broadly applied exemptions in California.',
        'scope': 'Records of investigations conducted by, or investigatory files compiled by, any state or local agency for correctional, law enforcement, or licensing purposes. Includes files compiled during active investigations and intelligence information. Formerly Gov. Code § 6254(f).',
        'key_terms': json.dumps(['investigation', 'investigatory file', 'law enforcement', 'correctional', 'licensing', 'intelligence', 'crime', 'arrest', 'suspect']),
        'counter_arguments': json.dumps([
            'Arrest information — name, booking date, charges, bail — is explicitly public under § 7923.610 regardless of this exemption',
            'Completed investigations where no enforcement action is pending may not warrant withholding of all records',
            'Records compiled for administrative or regulatory purposes do not qualify as "law enforcement" records',
            'Challenge whether the agency is acting in a "law enforcement" capacity vs. a general regulatory capacity',
            'The California Supreme Court in Williams v. Superior Court (1993) held agencies cannot invoke this to withhold records about concluded, non-prosecuted matters where the public interest weighs heavily toward disclosure',
            'Segregability is required — factual information in investigatory files that can be separated without revealing protected information must be released',
            'SB 1421 (2019) and AB 748 (2019), codified at Penal Code § 832.7, override this exemption for records of serious use of force, sustained findings of dishonesty, and sexual assault by peace officers',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(f). California Penal Code § 832.7 (as amended by SB 1421 (2019)) creates important exceptions that require disclosure of peace officer records involving serious use of force, sustained misconduct findings, and sexual assaults, notwithstanding this exemption. This is an area of significant ongoing litigation.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7927.700',
        'exemption_number': '§ 7927.700',
        'short_name': 'Personnel, Medical, and Similar Files',
        'category': 'privacy',
        'description': 'Protects personnel, medical, or similar files the disclosure of which would constitute an unwarranted invasion of personal privacy. California uses a balancing test and requires a genuine, substantial privacy interest.',
        'scope': 'Personnel, medical, or similar files, the disclosure of which would constitute an unwarranted invasion of personal privacy. Formerly Gov. Code § 6254(c).',
        'key_terms': json.dumps(['personnel file', 'medical file', 'similar files', 'privacy', 'personal information', 'employee records', 'disciplinary records']),
        'counter_arguments': json.dumps([
            'Public employees have a reduced expectation of privacy regarding their official duties — salary, title, and public misconduct are generally disclosable',
            'The California Constitution (Art. I, § 1) privacy right cuts both ways: it protects individuals but does not automatically shield government records about officials exercising public duties',
            'Challenge whether the files are truly "similar" to personnel or medical files — must be of similar sensitivity and personal nature',
            'Conduct occurring in an official capacity during working hours is generally not protected under this exemption',
            'Sustained disciplinary findings against public officers are often disclosable, especially after SB 1421 for peace officers',
            'Information about spending of public funds, official decisions, and use of public authority does not constitute personnel information',
            'Request redaction of purely personal information (home address, SSN) while releasing professional conduct records',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(c). The California Supreme Court in International Federation of Professional & Technical Engineers v. Superior Court (2007) addressed the intersection of this exemption and the constitutional right of privacy. For peace officers, Penal Code § 832.7 controls many law enforcement personnel records.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7927.705',
        'exemption_number': '§ 7927.705',
        'short_name': 'Pending Litigation / Attorney-Client Privilege',
        'category': 'litigation',
        'description': 'Protects records pertaining to pending litigation to which the public agency is a party, or to claims made pursuant to the Government Claims Act, until the pending litigation or claim has been finally adjudicated or otherwise settled. Also protects attorney-client privileged communications.',
        'scope': 'Records pertaining to pending litigation to which the public agency is a party, or to claims pursuant to Division 3.6 (Gov. Claims Act), until final adjudication or settlement. Attorney-client privileged materials are also protected. Formerly Gov. Code § 6254(b).',
        'key_terms': json.dumps(['pending litigation', 'attorney-client privilege', 'government claims act', 'work product', 'legal advice', 'settlement', 'claim']),
        'counter_arguments': json.dumps([
            'Once litigation is finally adjudicated or settled, this exemption no longer applies and records must be released',
            'Attorney-client privilege can be waived — challenge whether the privilege was properly maintained',
            'The privilege applies to communications, not underlying facts — factual records that happen to be in attorney files are not automatically privileged',
            'Government attorney-client privilege can be overcome by evidence of crime or fraud exception',
            'Settlement agreements and their terms are often public records once finalized, notwithstanding this exemption',
            'Records showing how taxpayer money was spent in litigation (total amounts paid, general scope) are matters of public interest',
            'The work product doctrine protects attorney mental impressions and strategy but not pure facts compiled in investigation',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(b). The litigation exemption is temporal — it ends when litigation concludes. Many agencies improperly continue to withhold records after litigation ends. Settlement amounts paid by public agencies from public funds are generally public record.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7924.510',
        'exemption_number': '§ 7924.510',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Protects trade secrets submitted to a public agency. Also related to protections under Civil Code § 3426 et seq. (California Uniform Trade Secrets Act).',
        'scope': 'Trade secrets submitted by businesses, developers, and contractors to government agencies, where disclosure would cause substantial competitive harm. Formerly Gov. Code § 6254.7 (air quality data) and related provisions. Trade secret definition tracks Civil Code § 3426.1.',
        'key_terms': json.dumps(['trade secret', 'proprietary information', 'confidential business information', 'competitive harm', 'formula', 'process', 'method', 'financial data']),
        'counter_arguments': json.dumps([
            'Must meet California Uniform Trade Secrets Act definition: information with independent economic value, actually secret, subject to reasonable measures to maintain secrecy',
            'Information that has been publicly disclosed (in permits, contracts, public hearings) cannot retain trade secret status',
            'General financial information, pricing, and revenue data submitted for regulatory purposes often does not meet the trade secret standard',
            'Agency must conduct an independent evaluation of trade secret claims — submitter assertions are not binding',
            'The public interest in understanding government contracts, environmental impacts, and public safety often outweighs trade secret claims',
            'Under § 7924.500, even trade secret information must be disclosed in the interest of public health and safety when the public interest clearly outweighs the harm of disclosure',
            'Challenge whether the claimant actually took reasonable measures to protect the alleged trade secret',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254.7. Trade secret claims in California require meeting the CUTSA standard (Civil Code § 3426.1). Submitters often overclaim trade secret protection; agencies are required to conduct independent review. See also § 7924.500 (overriding public health and safety interest).',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7928.200',
        'exemption_number': '§ 7928.200',
        'short_name': 'Real Property Appraisals',
        'category': 'real_property',
        'description': 'Protects real property appraisals or engineering or feasibility estimates and evaluations made for or by the state or local agency relative to the acquisition of property, until the time the transaction is either closed or abandoned.',
        'scope': 'Appraisals, engineering estimates, and feasibility evaluations prepared for property acquisition by government agencies, while the acquisition is pending. Formerly Gov. Code § 6254(h).',
        'key_terms': json.dumps(['appraisal', 'real property', 'acquisition', 'fair market value', 'eminent domain', 'feasibility estimate', 'engineering estimate']),
        'counter_arguments': json.dumps([
            'Once the property transaction is closed, abandoned, or completed (including condemnation), all appraisal records must be released',
            'This exemption protects the agency\'s negotiating position — once negotiation is over, the rationale for withholding disappears',
            'Appraisals conducted after acquisition (for asset valuation, not negotiation) are not covered',
            'Challenge whether the acquisition has been effectively "abandoned" even if no formal decision has been made',
            'Comparable sales data and other factual market information in appraisals may be segregable',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(h). The exemption is explicitly temporal — it only applies while the acquisition transaction is pending. This is frequently tested in eminent domain and redevelopment contexts.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7928.300',
        'exemption_number': '§ 7928.300',
        'short_name': 'Library Circulation and Use Records',
        'category': 'privacy',
        'description': 'Protects records of library patron use of library materials, including circulation records, registration records, and records of use of services.',
        'scope': 'Library circulation records, registration records, and records of use of library services, protecting patron privacy in what they read and access. Formerly Gov. Code § 6254(j).',
        'key_terms': json.dumps(['library', 'patron', 'circulation', 'borrowing records', 'registration', 'library card', 'reading records']),
        'counter_arguments': json.dumps([
            'This exemption is essentially mandatory — privacy protection for library records is among the strongest in California law',
            'Law enforcement may access records via subpoena or court order, but not via CPRA',
            'Aggregate, anonymized statistics about library usage are public and must be distinguished from individual patron records',
            'Records about library operations, policies, budgets, and staffing are not patron records and are fully public',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(j). One of the strongest exemptions in the CPRA. Reflects California\'s strong commitment to intellectual privacy. Patron records may only be disclosed to law enforcement under court order or with patron consent.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7924.000',
        'exemption_number': '§ 7924.000',
        'short_name': 'Test Questions and Examination Data',
        'category': 'examination',
        'description': 'Protects test questions, scoring keys, and other examination data used to administer licensing or employment examinations, if disclosure would compromise the fairness of future examinations.',
        'scope': 'Questions, scoring keys, and examination data used to administer certification, qualification, or civil service examinations, until the exam questions are no longer used. Formerly Gov. Code § 6254(g).',
        'key_terms': json.dumps(['test questions', 'scoring keys', 'examination', 'civil service exam', 'licensing exam', 'test data', 'answer key']),
        'counter_arguments': json.dumps([
            'Once an exam version is retired and no longer used, the questions and answers must be disclosed',
            'Administrative policies, grading rubrics, and general test design criteria are not exam questions and should be disclosed',
            'Challenge whether specific questions are actually still in use on current exams',
            'Results and statistics about exam performance (pass rates, average scores) are not exam questions and are public',
            'Examinee scores are subject to the personnel/privacy exemption, not this one',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(g). This exemption applies while questions are in active use. Retired exam forms are public. California civil service examination records are also subject to California Code of Regulations, Title 2.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7929.600',
        'exemption_number': '§ 7929.600',
        'short_name': 'Homeland Security / Critical Infrastructure',
        'category': 'security',
        'description': 'Protects information about vulnerabilities in public infrastructure, buildings, and critical systems where disclosure would create a clear danger to public safety or critical infrastructure security.',
        'scope': 'Records of infrastructure, security systems, and emergency response plans that, if disclosed, would enable attacks or compromise public safety. Added post-9/11 and substantially expanded. Formerly Gov. Code § 6254(aa) and related provisions.',
        'key_terms': json.dumps(['critical infrastructure', 'vulnerability', 'security plan', 'emergency response', 'utility', 'water system', 'power grid', 'homeland security']),
        'counter_arguments': json.dumps([
            'Agency must demonstrate a specific nexus between disclosure and a concrete security risk — generalized threats are insufficient',
            'Information about security incidents that have already occurred, agency response failures, or contractor mismanagement is public',
            'Budget allocations, contractor awards, and general program descriptions for security programs are public',
            'The exemption does not cover the fact that plans exist, only the operationally sensitive details',
            'Records about past security failures and audits showing vulnerabilities already exploited are matters of public accountability',
            'Challenge overbroad application: agencies cannot designate entire security files as exempt when only specific operational details warrant protection',
        ]),
        'notes': 'This exemption was significantly expanded in the years after September 11, 2001. Courts have cautioned against overbroad application. General oversight and budget information about security programs remains public even if specific vulnerability assessments are protected.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7927.100',
        'exemption_number': '§ 7927.100',
        'short_name': 'Confidential Communications — Official Information Privilege',
        'category': 'official_information',
        'description': 'Protects records whose disclosure is exempted or prohibited pursuant to federal or state law, including provisions of the Evidence Code relating to privilege, such as the official information privilege under Evidence Code § 1040.',
        'scope': 'Records specifically exempted by other state or federal statutes, or protected by evidentiary privileges including official information privilege, informant privilege, and governmental secrets privilege. Formerly Gov. Code § 6254(k).',
        'key_terms': json.dumps(['official information privilege', 'statutory exemption', 'Evidence Code', 'federal preemption', 'informant privilege', 'government privilege']),
        'counter_arguments': json.dumps([
            'Must identify a specific applicable privilege or statute — a generalized claim of privilege is insufficient',
            'Evidence Code § 1040 official information privilege requires balancing — it is not absolute',
            'The privilege is discretionary, not mandatory; courts may compel disclosure when need outweighs confidentiality interest',
            'Federal statutes that merely authorize confidentiality (rather than mandate it) may not qualify as a "prohibition" on disclosure',
            'Challenge whether the specific statute or privilege claimed actually applies to the records at issue',
            'Where the agency has publicly disclosed related information, privilege may have been waived as to that topic',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(k). This is essentially California\'s catch-all for other statutory exemptions and evidentiary privileges. The Evidence Code privileges (§§ 1040-1042) include official information, identity of informers, and official secrets. Each has its own balancing test.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7928.405',
        'exemption_number': '§ 7928.405',
        'short_name': 'Welfare Fraud Investigation Records',
        'category': 'law_enforcement',
        'description': 'Protects records of welfare fraud investigations conducted by a county welfare department, including records relating to referrals, investigations, and files pertaining to public assistance recipients.',
        'scope': 'Records of investigations of suspected welfare fraud by county departments, protecting both investigatory integrity and privacy of public assistance recipients. Formerly Gov. Code § 6254(l) and related provisions.',
        'key_terms': json.dumps(['welfare fraud', 'public assistance', 'benefits investigation', 'county welfare', 'SNAP', 'Medi-Cal', 'CalWORKs']),
        'counter_arguments': json.dumps([
            'Aggregate statistics about fraud investigations and outcomes (without identifying individuals) are public',
            'Policy documents, training materials, and general program descriptions for anti-fraud programs are public',
            'Records about fraud by providers or contractors (not recipients) may not fall within this exemption',
            'Completed investigations where no action was taken against a recipient are less deserving of protection than active cases',
            'Agency budget and staffing for fraud investigation units are public',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6254(l). This exemption protects both investigatory integrity and the privacy interests of welfare recipients, who have strong privacy rights under both state and federal law.',
    },
    {
        'jurisdiction': 'CA',
        'statute_citation': 'Cal. Gov. Code § 7922.000',
        'exemption_number': '§ 7922.000',
        'short_name': 'Public Interest Catch-All (Balancing Test)',
        'category': 'balancing',
        'description': 'The general balancing test provision — the agency may withhold a record if it can show that the public interest served by not disclosing the record clearly outweighs the public interest served by disclosure. This is the California "catch-all" exemption, equivalent to a general deliberative/public interest privilege.',
        'scope': 'Any record where the agency demonstrates by clear and convincing evidence that the public interest in withholding clearly outweighs the public interest in disclosure. This is a discretionary, agency-invoked balancing test with the burden on the agency. Formerly Gov. Code § 6255.',
        'key_terms': json.dumps(['public interest', 'balancing test', 'clearly outweighs', 'catch-all exemption', 'deliberative process', 'agency discretion']),
        'counter_arguments': json.dumps([
            'This is the most challengeable exemption — agency bears the burden of affirmatively establishing that withholding serves a "clear and overriding" public interest',
            'The California Supreme Court held in CBS, Inc. v. Block (1986) that the exemption must be narrowly construed and the agency burden is significant',
            'The public interest in open government is the default; agencies cannot simply assert "public interest" without specific, articulable harm',
            'Courts apply de novo review — agency judgment is not entitled to deference on the balancing',
            'Where records relate to official misconduct, financial mismanagement, or public safety failures, the balance almost always tips toward disclosure',
            'This exemption cannot be used to withhold records that another specific exemption covers but does not fully protect — agencies cannot stack exemptions',
            'Challenge with specific public interest arguments: accountability, taxpayer oversight, public safety, preventing future misconduct',
            'Unlike other exemptions, this one is purely discretionary — agency must actively choose to invoke it and can always choose to disclose',
        ]),
        'notes': 'Formerly Cal. Gov. Code § 6255. This is the most litigated exemption after § 7923.600. California courts have consistently held that the burden is on the agency and the standard is "clearly outweighs" — not merely "outweighs." See Times Mirror Co. v. Superior Court (1991) and CBS, Inc. v. Block (1986). Commonly invoked for draft documents, internal communications, and records of ongoing negotiations.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for exemption in CA_EXEMPTIONS:
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
    print(f'CA CPRA exemptions: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_ca_exemptions', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
