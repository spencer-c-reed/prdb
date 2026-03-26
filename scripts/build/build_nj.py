#!/usr/bin/env python3
"""Build New Jersey Open Public Records Act data: exemptions, rules, and templates.

Covers New Jersey's Open Public Records Act (OPRA), N.J.S.A. 47:1A-1 et seq.
OPRA is one of the strongest state public records laws in the country — it
creates a specific right to inspect government records, imposes a 7-business-day
response deadline, provides for free access through the Government Records
Council (GRC), and mandates attorney fees for prevailing requesters. Courts
construe exemptions narrowly and the burden of proof is on the agency.

Run: python3 scripts/build/build_nj.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

# =============================================================================
# EXEMPTIONS
# OPRA's exemptions are enumerated at N.J.S.A. 47:1A-1.1 and 47:1A-9.
# Unlike many states, OPRA's enumerated exemptions are exclusive — an agency
# cannot withhold records based on an unlisted rationale. Courts apply a
# strict construction against withholding. The common-law right of access
# (New Jersey Open Public Meetings Act and common law) supplements OPRA for
# records not technically "government records" under OPRA's definition.
# =============================================================================

NJ_EXEMPTIONS = [
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(a)',
        'exemption_number': 'OPRA § 47:1A-1.1(a)',
        'short_name': 'Interagency or Intra-Agency Advisory, Consultative, or Deliberative Material',
        'category': 'deliberative',
        'description': 'Advisory, consultative, or deliberative (ACD) communications — including drafts, recommendations, and intra-agency memoranda — that reflect the deliberative process of government decision-making are exempt from OPRA to the extent they contain opinions and recommendations that have not been adopted as final agency positions.',
        'scope': 'Predecisional communications between government officials that express opinions, recommendations, or policy analysis. The exemption tracks the federal deliberative process privilege but is codified in OPRA as the "advisory, consultative, or deliberative" (ACD) exception. It does not protect purely factual material, even if embedded in a deliberative document. Final decisions, working law, and policies actually applied by the agency are not covered. Courts have held the ACD exception is narrow and should not be used to shield routine decision-making from accountability. The New Jersey Supreme Court in Burnett v. County of Bergen (2010) held that OPRA exemptions must be narrowly construed.',
        'key_terms': json.dumps([
            'advisory material', 'consultative material', 'deliberative material',
            'intra-agency memorandum', 'predecisional', 'draft', 'recommendation',
            'policy deliberation', 'ACD exception', 'working paper',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual information within deliberative documents must be segregated and released — the ACD exception covers only opinion and recommendation portions',
            'Once a recommendation is adopted as agency policy or final decision, the ACD exception no longer applies',
            'Documents circulated to parties outside the agency lose their predecisional character and may not qualify',
            'Challenge overbroad claims where the agency withholds entire documents when only specific recommendation sections qualify',
            'New Jersey courts apply OPRA exemptions strictly against the agency — any ambiguity goes in favor of disclosure',
            '"Working law" — standards agencies actually apply — must be disclosed even if contained in internal documents',
        ]),
        'notes': 'The ACD exception under OPRA is one of the most frequently litigated exemptions before the Government Records Council. The GRC and New Jersey courts have consistently held it does not cover purely factual material. See Burnett v. County of Bergen, 198 N.J. 408 (2009). The common-law right of access may independently require disclosure of some deliberative records that OPRA technically exempts.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(b)',
        'exemption_number': 'OPRA § 47:1A-1.1(b)',
        'short_name': 'Criminal Investigatory Records',
        'category': 'law_enforcement',
        'description': 'Records compiled by a government agency for the purpose of criminal investigation are exempt from OPRA, including information about victims, criminal intelligence, and information that would reveal investigative techniques or compromise ongoing investigations.',
        'scope': 'Records assembled by a law enforcement agency for the purpose of detecting and investigating crime. The exemption covers confidential informant identities, active investigation files, criminal intelligence, and information that would reveal investigative techniques or methods. It does NOT cover all law enforcement records — incident reports, arrest records, booking information, and records of completed investigations are generally accessible. The exemption requires that: (1) the record was compiled for criminal investigation purposes; (2) disclosure would be against the public interest by revealing informants, compromising ongoing investigations, or enabling evasion of the law. New Jersey courts apply a specific harm test.',
        'key_terms': json.dumps([
            'criminal investigatory record', 'criminal investigation', 'confidential informant',
            'investigative technique', 'ongoing investigation', 'criminal intelligence',
            'law enforcement sensitive', 'investigation file',
        ]),
        'counter_arguments': json.dumps([
            'Incident reports and general police reports documenting the occurrence of a crime are public regardless of investigation status',
            'Arrest records, booking information, and charging documents are not criminal investigatory records and are public',
            'Records of completed investigations where prosecution has concluded do not retain exemption protection',
            'The agency must demonstrate that each specific record was compiled for criminal investigation purposes — a generic label is insufficient',
            'Factual information in investigative files that does not reveal informants, techniques, or harm ongoing proceedings must be segregated and released',
            'New Jersey courts apply a specific harm test — the agency must show actual harm from disclosure, not speculative harm',
        ]),
        'notes': 'N.J.S.A. 47:1A-1.1(b) is broadly written but narrowly construed by New Jersey courts. The GRC has consistently required agencies to identify specific harm from disclosure. Completed investigation files are generally public. The New Jersey Supreme Court\'s OPRA jurisprudence emphasizes that exemptions are the exception, not the rule.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(c)',
        'exemption_number': 'OPRA § 47:1A-1.1(c)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records that would reveal communications protected by the attorney-client privilege — including legal advice from government attorneys to government officials — are exempt from disclosure under OPRA.',
        'scope': 'Confidential communications between a government agency and its attorneys made for the purpose of obtaining or providing legal advice. The privilege applies to communications with both in-house government counsel and outside counsel retained by the agency. It requires that the communication: (1) be made in confidence; (2) be for the purpose of legal advice (not business or policy advice); and (3) not be waived through disclosure to parties outside the privilege. Billing records, retainer agreements, and general financial terms are not privileged. Work product prepared in anticipation of litigation also falls under this exemption. New Jersey applies the common-law attorney-client privilege to government entities.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'privileged communication',
            'in-house counsel', 'attorney work product', 'in anticipation of litigation',
            'legal opinion', 'confidential legal communication',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not general policy or business guidance — mixing legal and business advice does not automatically privilege the entire communication',
            'Attorney billing records describing services rendered are generally public under New Jersey law',
            'Waiver occurs when the agency uses the legal advice in public decision-making or discloses it to non-essential parties',
            'The privilege must be asserted specifically for each document — a blanket "attorney-client privilege" claim is insufficient',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis and opinions',
            'The common-law right of access may apply to some legal communications that OPRA exempts',
        ]),
        'notes': 'New Jersey recognizes the attorney-client privilege for government entities under OPRA. The GRC requires agencies to provide a privilege log identifying each document withheld and the specific basis for the claim. The privilege is not absolute — New Jersey courts have held that the public\'s right to know about government attorney advice on public matters can override the privilege in limited circumstances.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(d)',
        'exemption_number': 'OPRA § 47:1A-1.1(d)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Proprietary commercial or financial information that constitutes a trade secret, or information that, if disclosed, would give an advantage to competitors and cause competitive harm, is exempt from OPRA.',
        'scope': 'Commercially valuable information submitted by private entities to government agencies where: (1) the information derives independent economic value from secrecy; (2) the submitter took reasonable measures to maintain secrecy; and (3) disclosure would cause competitive harm. New Jersey applies the Uniform Trade Secrets Act definition. Government-generated records cannot constitute trade secrets — only privately submitted information qualifies. Amounts paid with public funds, contract prices, and government expenditures are generally public regardless of trade secret designations by vendors.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm', 'commercial information',
            'financial information', 'UTSA', 'confidential business information',
            'economic value', 'competitive advantage',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices paid with public funds are public regardless of vendor trade secret claims',
            'The submitter must demonstrate that the specific information meets the UTSA definition — a "confidential" label is not sufficient',
            'Information required by law to be submitted to the government has reduced secrecy expectations',
            'The agency must independently evaluate trade secret designations — it may not simply defer to vendor claims',
            'Publicly available information cannot qualify as a trade secret',
            'Challenge whether the submitter actually maintained secrecy — careless disclosure elsewhere defeats the claim',
        ]),
        'notes': 'OPRA\'s trade secret exemption is broadly invoked by government contractors seeking to shield procurement records. New Jersey courts and the GRC have consistently held that public contract amounts, bid prices, and performance metrics are public. The trade secret designation must be supported by specific evidence, not just vendor preference.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(e)',
        'exemption_number': 'OPRA § 47:1A-1.1(e)',
        'short_name': 'Personal Information — Privacy Protection',
        'category': 'privacy',
        'description': 'Personal information in government records whose disclosure would constitute an unwarranted invasion of personal privacy — including Social Security numbers, driver\'s license numbers, medical information, and similar sensitive personal data — is exempt from OPRA.',
        'scope': 'Specific categories of personal identifying information including Social Security numbers, driver\'s license numbers, dates of birth, financial account numbers, medical information, and similar data whose disclosure would constitute an unwarranted invasion of personal privacy. The exemption is field-specific — agencies must release records with protected fields redacted rather than withholding entire documents. Names, job titles, salaries, and work-related information of public employees are generally public and do not qualify. Courts balance the individual privacy interest against the public interest in disclosure. N.J.S.A. 47:1A-5(a) expressly allows fee-bearing copies of personnel records limited to name, title, position, salary, and dates of service.',
        'key_terms': json.dumps([
            'personal privacy', 'Social Security number', 'SSN', 'driver\'s license number',
            'date of birth', 'medical information', 'financial account', 'personal information',
            'unwarranted invasion of privacy', 'personally identifiable information',
        ]),
        'counter_arguments': json.dumps([
            'Names, titles, salaries, and job-related information of public employees are expressly public under N.J.S.A. 47:1A-5(a)',
            'The exemption protects specific fields, not entire records — agencies must redact and release the non-exempt remainder',
            'Information already published in public records (court filings, official directories) cannot be withheld',
            'The privacy interest must outweigh the public interest in accountability — the balancing test frequently favors disclosure for public employees\' official conduct',
            'Challenge overbroad redactions where the agency removed non-exempt context along with the protected data',
        ]),
        'notes': 'OPRA\'s privacy exemption requires case-by-case balancing for most information, but certain categories (SSNs, medical records) are categorically protected. The GRC has produced extensive guidance on specific categories. The common-law right of access applies a similar but distinct balancing test.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(f)',
        'exemption_number': 'OPRA § 47:1A-1.1(f)',
        'short_name': 'Security Information and Vulnerability Assessments',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, emergency response procedures, and related records whose disclosure would compromise the security of critical infrastructure or government facilities are exempt from OPRA.',
        'scope': 'Specific plans, procedures, and assessments related to the physical security of government facilities, critical infrastructure, and public safety systems. The exemption requires that disclosure would actually compromise security — generic assertions that "security information" is involved are insufficient. It does not protect budget information, staffing levels, general emergency management policies, or after-action reports addressing general policy improvements rather than specific vulnerabilities. Courts require a specific showing of how disclosure of each record would create a security risk.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'emergency response procedure', 'physical security', 'facility security',
            'security protocol', 'counterterrorism', 'security vulnerability',
        ]),
        'counter_arguments': json.dumps([
            'General emergency management policies and plans do not automatically qualify — the agency must show specific vulnerability data',
            'Budget and staffing information for security agencies is generally public',
            'After-action reports addressing policy improvements rather than specific vulnerabilities are public',
            'The exemption applies to specific security plans, not to all records held by security agencies',
            'Challenge whether the specific record contains vulnerability information as opposed to general administrative material',
        ]),
        'notes': 'Post-9/11 security exemptions are frequently invoked in New Jersey, particularly for transit, utility, and law enforcement security records. The GRC requires a specific showing of security risk from disclosure, not a generalized security classification.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(g)',
        'exemption_number': 'OPRA § 47:1A-1.1(g)',
        'short_name': 'Victim Records — Confidentiality',
        'category': 'privacy',
        'description': 'Records identifying victims of sex crimes, domestic violence, child abuse, or other specified offenses are exempt from OPRA to protect victim safety and privacy.',
        'scope': 'Records that would identify victims of sexual offenses, domestic violence, child abuse, child exploitation, or stalking. The exemption is victim-identity-specific — it does not protect the entire record of a criminal investigation, only the portions that would identify or endanger the victim. Non-identifying factual information about the crime, the perpetrator\'s public actions, and the outcome of prosecution are generally public. New Jersey law provides strong protections for domestic violence victims through multiple statutes.',
        'key_terms': json.dumps([
            'victim identity', 'sex crime victim', 'domestic violence victim',
            'child abuse victim', 'victim confidentiality', 'victim privacy',
            'sexual offense victim', 'protected victim information',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects victim identity, not the entire investigation record — non-identifying case details are public',
            'Outcome of prosecution, perpetrator identity, and court records are public regardless of this exemption',
            'Aggregate statistics about crime types, outcomes, and trends are not covered',
            'Challenge claims that this exemption protects all records of a domestic violence or sexual offense investigation',
        ]),
        'notes': 'New Jersey has a strong statutory framework for victim privacy across multiple laws. OPRA\'s victim record exemption works in conjunction with the Address Confidentiality Program, the Violence Against Women Act\'s provisions, and specific New Jersey statutes protecting victims of domestic violence. The exemption is narrowly targeted at identity-revealing information.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-3(a)',
        'exemption_number': 'OPRA § 47:1A-3(a)',
        'short_name': 'Pending Criminal Investigations — Specific Limitations',
        'category': 'law_enforcement',
        'description': 'Information that, if disclosed, would be inimical to the public interest — including information that would prejudice ongoing criminal investigations, reveal the identity of undercover officers, or compromise witness safety — is exempt during the pendency of the investigation.',
        'scope': 'Applies to specific categories of pending criminal investigation information: identity of undercover officers; identity of confidential informants; information that would jeopardize the safety of witnesses or victims; information that would enable a person to avoid detection or apprehension; and information that would obstruct or impede a pending investigation or prosecution. The exemption is time-limited — it expires when the investigation is no longer pending. Courts require specific identification of which harm applies to each withheld record. Generic "pending investigation" labels are insufficient under New Jersey law.',
        'key_terms': json.dumps([
            'pending investigation', 'undercover officer', 'confidential informant',
            'witness safety', 'inimical to public interest', 'obstruction', 'criminal intelligence',
            'investigation pending', 'law enforcement sensitive',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the investigation is no longer pending — challenge stale claims of ongoing investigations',
            'Factual information not implicating any of the enumerated harms must be released',
            'Arrest records, charging documents, and court filings are public even during pending investigation',
            'The agency must identify specifically which harm applies to each record, not assert a blanket investigative privilege',
            'New Jersey courts require specific evidence of harm, not generalized law enforcement sensitivity',
        ]),
        'notes': 'N.J.S.A. 47:1A-3(a) provides a separate pending-investigation exemption that supplements the criminal investigatory records exemption. The GRC and New Jersey courts have been skeptical of broad "pending investigation" claims and require specific harm documentation.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1 (statutory confidentiality)',
        'exemption_number': 'OPRA — Statutory Confidentiality',
        'short_name': 'Records Declared Confidential by Other Statute',
        'category': 'statutory',
        'description': 'Records that are declared confidential by another state or federal statute, or by a court order, are exempt from OPRA to the extent required by the applicable law or order.',
        'scope': 'Records specifically designated as confidential by another New Jersey statute or federal law. Common examples include: Division of Child Protection and Permanency (DCPP) records under N.J.S.A. 9:6-8.10a; motor vehicle records under the Driver\'s Privacy Protection Act (DPPA); tax return information under N.J.S.A. 54:50-8; and certain mental health records under N.J.S.A. 30:4-24.3. The exemption tracks the specific scope of the other statute — if the other statute has exceptions, those exceptions apply. Agencies may not use a broad statutory confidentiality claim without identifying the specific applicable statute.',
        'key_terms': json.dumps([
            'statutory confidentiality', 'confidential by statute', 'DCPP records',
            'motor vehicle records', 'DPPA', 'tax records', 'mental health records',
            'court order confidentiality', 'another statute', 'federally protected',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific other statute and explain how it applies to each withheld record',
            'Broad statutory confidentiality claims without statute identification are insufficient',
            'The scope of the other statute\'s protection is the maximum allowed — some statutes have exceptions that permit disclosure',
            'Federal preemption arguments do not automatically exempt records from OPRA — the specific federal law must be analyzed',
            'Aggregate statistics and anonymized data from confidential records are generally public',
        ]),
        'notes': 'The "other statute" exemption is a catch-all for records protected by New Jersey\'s extensive statutory scheme. It is among the most frequently invoked exemptions before the GRC. Agencies must provide specific citations, not general references to unspecified "confidentiality" protections.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(i)',
        'exemption_number': 'OPRA § 47:1A-1.1(i)',
        'short_name': 'Inter-Agency and Intra-Agency Test Questions',
        'category': 'deliberative',
        'description': 'Questions, scoring instructions, answer keys, and related materials used in civil service examinations, licensing tests, and competitive employment evaluations are exempt prior to administration of the test.',
        'scope': 'Unpublished test questions, answer keys, scoring guides, and evaluation criteria for government-administered examinations, including civil service exams, professional licensing tests, and competitive hiring evaluations. The exemption expires once the test is administered and results are final — post-test questions and answer keys may be public. The exemption is prospective, not retrospective: it protects test security before administration, not general evaluation policy or aggregate performance data.',
        'key_terms': json.dumps([
            'examination questions', 'test questions', 'answer key', 'scoring instructions',
            'civil service exam', 'licensing test', 'competitive evaluation',
            'test security', 'pre-administration',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires after test administration — post-test records may be public',
            'General examination policies, scoring criteria on their face, and aggregate results are public',
            'Challenge whether prior-year examinations (no longer in use) remain protected after they are retired',
            'Budget and administrative records for examination programs are public',
        ]),
        'notes': 'This exemption is narrow and time-limited by nature. New Jersey civil service examinations have been the subject of extensive OPRA litigation. The GRC has generally held that once examinations are administered and results published, the confidentiality interest diminishes significantly.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-5(g)',
        'exemption_number': 'OPRA § 47:1A-5(g)',
        'short_name': 'Personnel Records — Limited Disclosure',
        'category': 'privacy',
        'description': 'Personnel files of public employees are not generally available for public inspection; however, OPRA expressly permits access to the employee\'s name, title, position, salary, payroll record, length of service, date of separation, and amount and type of pension.',
        'scope': 'Government employee personnel records are largely protected from disclosure as a whole. However, OPRA creates a specific list of personnel information that is always public: name, title, position, salary, payroll records, length of service, date of separation, and amount and type of pension received. Information beyond this enumerated list — including performance evaluations, disciplinary records (in many cases), medical information, and non-public personal information — may be withheld. New Jersey courts have extended some public access to disciplinary records, particularly for officers whose discipline arose from misconduct affecting the public.',
        'key_terms': json.dumps([
            'personnel record', 'employee file', 'salary', 'payroll record',
            'public employee', 'disciplinary record', 'performance evaluation',
            'government employee privacy', 'N.J.S.A. 47:1A-5(g)',
        ]),
        'counter_arguments': json.dumps([
            'Name, title, position, salary, payroll records, length of service, and pension information are expressly public under OPRA',
            'Disciplinary records for public employees involved in on-duty misconduct affecting the public may be accessible through the common-law right of access',
            'Final disciplinary action — suspensions, terminations, demotions — may be public even if supporting records are not',
            'Challenge whether the specific record is truly a "personnel record" vs. a public record about the employee\'s official actions',
            'The common-law right of access supplements OPRA and may require disclosure of some personnel information OPRA exempts',
        ]),
        'notes': 'Personnel record protection under OPRA works alongside the New Jersey Civil Service Act (N.J.S.A. 11A:1-1 et seq.) and the Local Government Ethics Law. The 2022 Police Records Access Law (N.J.S.A. 47:1A-1 et seq. amendment) significantly expanded access to police disciplinary records. Officers\' disciplinary records from 2020 forward are subject to new public access requirements.',
    },
    {
        'jurisdiction': 'NJ',
        'statute_citation': 'N.J.S.A. 47:1A-1.1(a); Common Law',
        'exemption_number': 'OPRA — Common Law Override',
        'short_name': 'Common-Law Right of Access (Supplement to OPRA)',
        'category': 'deliberative',
        'description': 'New Jersey courts have recognized an independent common-law right of access to government records that supplements OPRA. When OPRA exempts records, the common-law right of access may still require disclosure if the public interest in transparency outweighs the government\'s interest in confidentiality.',
        'scope': 'Not strictly an exemption — rather, the common-law right of access is a separate legal basis for obtaining records that OPRA does not cover or that OPRA technically exempts. New Jersey courts balance the requester\'s interest, the public benefit of disclosure, the sensitivity of the information, and the government\'s interest in nondisclosure. The common-law right is more flexible than OPRA but requires the requester to demonstrate a particularized need. Particularly significant for records outside OPRA\'s definition of "government record" and for deliberative/personnel records where OPRA\'s exemptions apply.',
        'key_terms': json.dumps([
            'common-law right of access', 'particularized need', 'public interest',
            'balancing test', 'government records outside OPRA', 'common law',
            'Loigman v. Kimmelman', 'supplemental access right',
        ]),
        'counter_arguments': json.dumps([
            'The common-law right of access provides an independent basis for access when OPRA exemptions technically apply',
            'Requesters with a particularized need — journalists, researchers, parties with direct interest — have stronger common-law claims',
            'Courts apply a balancing test that frequently favors disclosure for records about the exercise of government power',
            'Always plead both OPRA and the common-law right of access when filing complaints to preserve all remedies',
            'The GRC has jurisdiction over OPRA claims; common-law claims go to Superior Court — strategic choice matters',
        ]),
        'notes': 'The New Jersey common-law right of access was recognized in Loigman v. Kimmelman, 102 N.J. 98 (1986) and has been repeatedly affirmed by the New Jersey Supreme Court. It is a crucial supplement to OPRA because OPRA\'s definition of "government record" excludes certain categories. Requesters whose OPRA requests are denied should always consider a simultaneous common-law access petition in Superior Court.',
    },
]

# =============================================================================
# RULES
# New Jersey OPRA, N.J.S.A. 47:1A-1 et seq.
# OPRA\'s key procedural features: 7-business-day response deadline,
# Government Records Council (GRC) free administrative appeal, mandatory
# attorney fees and penalties for prevailing requesters, $0.05/page standard
# copy rate, and a strong presumption of disclosure. New Jersey is widely
# regarded as having one of the most requester-friendly procedural frameworks.
# =============================================================================

NJ_RULES = [
    {
        'jurisdiction': 'NJ',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '7',
        'day_type': 'business',
        'statute_citation': 'N.J.S.A. 47:1A-5(i)',
        'notes': 'OPRA requires custodians of government records to respond to requests within 7 business days. The 7-day clock begins when the request is received by the custodian. Failure to respond within 7 business days is a deemed denial under N.J.S.A. 47:1A-5(i). A "deemed denial" triggers the requester\'s right to file a GRC complaint or action in Superior Court immediately — no further agency action is required before seeking enforcement. The deemed-denial rule is unique and powerful: silence itself is a violation.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'initial_response',
        'param_key': 'deemed_denial_rule',
        'param_value': 'failure_to_respond_7_business_days',
        'day_type': 'business',
        'statute_citation': 'N.J.S.A. 47:1A-5(i)',
        'notes': 'OPRA\'s deemed-denial rule is one of its most powerful enforcement provisions. If a custodian fails to respond within 7 business days, the request is "deemed denied" by operation of law. This is not a discretionary determination — it is an automatic legal consequence of non-response. A deemed denial immediately entitles the requester to file a GRC complaint or file in Superior Court. The requester need not wait for an explicit denial, send a follow-up, or wait longer. This rule has been affirmed repeatedly by the New Jersey Supreme Court and Appellate Division.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'initial_response',
        'param_key': 'extension_allowed',
        'param_value': 'yes_with_written_notice',
        'day_type': 'business',
        'statute_citation': 'N.J.S.A. 47:1A-5(i)',
        'notes': 'A custodian who cannot comply within 7 business days may seek an extension, but must provide written notice to the requester within the 7-day period explaining the reason for the extension and specifying when the records will be provided. The extension must be for a specific reason — such as the need to review large volumes of records, await redaction review, or coordinate with other agencies. A generic "we need more time" extension notice is insufficient. Extensions must be reasonable — the GRC has found extensions of 30+ days unreasonable for small requests.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate_per_page',
        'param_value': '0.05',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-5(b)',
        'notes': 'The standard copy rate under OPRA is $0.05 per letter-size page (one side) and $0.07 per page for legal-size or double-sided copies. This is the maximum fee for routine copies of government records. Electronic records in their native format must be provided free of charge or at minimal cost. Agencies may NOT charge for staff time spent locating, reviewing, redacting, or preparing records — those costs are part of the government\'s public obligation. The $0.05 rate applies regardless of document complexity. Agencies that attempt to charge higher rates based on "actual cost" or "administrative cost" are not complying with OPRA.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'fee_cap',
        'param_key': 'special_service_charge',
        'param_value': '0.05-0.07',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-5(c)',
        'notes': 'When the volume of records or complexity of the request requires the agency to devote an extraordinary amount of resources to compliance, OPRA permits a "special service charge." This charge must be based on the actual direct cost of the extraordinary service — typically copying, digital media, or delivery costs only. It does NOT include staff time for review or redaction. The special service charge is rarely justified and the GRC scrutinizes it carefully. The agency must provide advance written notice of any special service charge and the requester may agree or withdraw/modify the request before the charge is incurred.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_news_media',
        'param_value': 'authorized_news_media_automatic_waiver',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-5(a)',
        'notes': 'Members of the "news media" as defined by N.J.S.A. 47:1A-5(a) are entitled to a fee waiver when requesting records for news gathering purposes. The news media waiver is not discretionary — if the requester qualifies as news media under the statute\'s definition (a newspaper, radio, television, or online publication that regularly disseminates news to the public), the fee is automatically waived. This is one of the strongest news media access provisions in any state OPRA statute. Requesters claiming news media status must document it if challenged, but agencies may not demand proof as a precondition to processing the request.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'appeal_deadline',
        'param_key': 'grc_complaint_deadline_days',
        'param_value': '45',
        'day_type': 'calendar',
        'statute_citation': 'N.J.S.A. 47:1A-6; N.J.A.C. 5:39-1.6',
        'notes': 'A requester who is denied access — or whose request is deemed denied by non-response — may file a complaint with the Government Records Council (GRC) within 45 calendar days of the denial. The GRC is a quasi-judicial body that provides free adjudication of OPRA disputes. GRC proceedings are free for requesters, substantially more accessible than court, and often faster. The GRC can order records released, assess civil penalties, and award attorney fees. Alternatively, requesters may file directly in New Jersey Superior Court without going through the GRC. The two remedies can be pursued simultaneously in some circumstances.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'appeal_deadline',
        'param_key': 'superior_court_action_available',
        'param_value': 'yes_alternative_to_grc',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-6',
        'notes': 'In addition to GRC complaints, requesters may file an action for access in New Jersey Superior Court (Law Division). Court actions are a separate remedy from GRC complaints. Court proceedings allow discovery, can address broader issues including constitutional claims, and may be faster for time-sensitive matters. The requester who substantially prevails in Superior Court is entitled to attorney fees and costs. Some requesters file simultaneously in GRC and court; others choose one forum. Superior Court has held that it may review GRC decisions and that the GRC\'s factual findings are entitled to deference.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_knowing_violation',
        'param_value': '$1,000 first offense; $2,500-$5,000 second and subsequent',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-11',
        'notes': 'For knowing and willful violations of OPRA, the GRC or court may impose civil penalties: $1,000 for a first offense, $2,500 to $5,000 for second and subsequent offenses. "Knowing and willful" requires more than negligence — the custodian must have known the records were public and deliberately withheld them. The GRC and courts have found knowing-and-willful violations where agencies denied requests based on exemptions they knew were inapplicable. Penalties are personally assessable against the custodian, not just the agency. This personal liability provision is a significant deterrent.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_mandatory',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-6',
        'notes': 'A requester who prevails in a court action or GRC proceeding is entitled to reasonable attorney fees and litigation costs. The fee-shifting provision is mandatory for prevailing requesters — courts and the GRC do not have discretion to deny fees to a requester who substantially prevails. This is one of the strongest fee-shifting provisions in any state records law. The mandatory fee provision makes OPRA enforcement economically viable for advocacy organizations and attorneys who take OPRA cases on contingency. New Jersey courts have awarded substantial attorney fees in OPRA cases, including cases involving relatively modest amounts of records.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-5(a)',
        'notes': 'OPRA does not require requesters to identify themselves or state the purpose of their request. Requesters may submit anonymous or pseudonymous requests. Contact information is only required for delivery purposes if the requester wants electronic or mailed copies. The GRC and courts have held that requiring identification as a condition of processing a request is an unlawful barrier to access. Some agencies have online portals that request contact information — providing such information must be voluntary.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_custodian',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-6',
        'notes': 'The burden of proving that any denial was authorized under OPRA rests entirely on the custodian, not the requester. N.J.S.A. 47:1A-6 explicitly places the burden of proof on the agency. This is consistent with OPRA\'s foundational premise — access is the rule and exemption is the exception. In GRC proceedings and court actions, the agency must affirmatively justify each withholding with specific evidence. Generic assertions of exemption categories are insufficient.',
    },
    {
        'jurisdiction': 'NJ',
        'rule_type': 'initial_response',
        'param_key': 'custodian_must_denote_exemption',
        'param_value': 'specific_exemption_required',
        'day_type': None,
        'statute_citation': 'N.J.S.A. 47:1A-5(g)',
        'notes': 'When denying a request, the custodian must specify the legal basis for the denial — citing the specific statutory exemption. A generic denial without a statutory citation is not a valid denial under OPRA. N.J.S.A. 47:1A-5(g) requires the custodian to indicate the specific provision of law that permits the denial for each record or category of records withheld. Failure to cite specific authority is itself a violation that the GRC may use to support a finding in the requester\'s favor.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

NJ_TEMPLATES = [
    {
        'jurisdiction': 'NJ',
        'record_type': 'general',
        'template_name': 'General New Jersey OPRA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Public Records Act Request — N.J.S.A. 47:1A-1 et seq.

Dear Custodian of Records:

Pursuant to the New Jersey Open Public Records Act (OPRA), N.J.S.A. 47:1A-1 et seq., I hereby request access to and copies of the following government records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, as this minimizes cost for both parties.

I am willing to pay copying fees as permitted by N.J.S.A. 47:1A-5(b) — $0.05 per letter-size page or $0.07 per legal-size or double-sided page. I am not willing to pay for staff time spent locating, reviewing, or redacting records, which OPRA does not permit. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under N.J.S.A. 47:1A-6, the burden of demonstrating that any denial is authorized under OPRA rests on the custodian. If any records are denied, in whole or in part, I request that you: (1) identify each record withheld or each portion redacted; (2) state the specific statutory provision that authorizes withholding, with citation to N.J.S.A.; (3) describe the record with sufficient detail for me to evaluate the claimed exemption; and (4) confirm that all reasonably segregable non-exempt portions have been released.

Under N.J.S.A. 47:1A-5(i), failure to respond within 7 business days constitutes a "deemed denial" under OPRA and entitles me to file a complaint with the Government Records Council or an action in Superior Court.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I am a member of the news media as defined by N.J.S.A. 47:1A-5(a), and I am requesting these records for news-gathering purposes related to {{news_gathering_purpose}}. Under N.J.S.A. 47:1A-5(a), members of the news media are entitled to a fee waiver when requesting records for news-gathering purposes. Please process this request without charge.

[Alternative if not news media:]
I respectfully request that any copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of significant public interest. If records are provided electronically, the copying cost is zero. I am {{requester_category_description}} and disclosure of these records will benefit the public by {{public_benefit_explanation}}.''',
        'expedited_language': '''I request that this request be processed as expeditiously as possible. Prompt production is important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me immediately if there are questions that would allow faster processing.''',
        'notes': 'General OPRA template. Key NJ features: (1) 7-business-day response deadline with automatic deemed-denial for non-response (N.J.S.A. 47:1A-5(i)); (2) $0.05/page standard copy rate — no staff time charges allowed; (3) burden of proof is on the custodian; (4) GRC complaint is free and available within 45 days of denial; (5) mandatory attorney fees for prevailing requesters; (6) news media get automatic fee waiver; (7) use "OPRA" and "N.J.S.A. 47:1A" — not "FOIA"; (8) always request that the agency cite the specific statutory provision for any denial.',
    },
    {
        'jurisdiction': 'NJ',
        'record_type': 'law_enforcement',
        'template_name': 'New Jersey OPRA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Public Records Act Request — Law Enforcement Records, N.J.S.A. 47:1A-1 et seq.

Dear Custodian of Records:

Pursuant to the New Jersey Open Public Records Act (OPRA), N.J.S.A. 47:1A-1 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and arrest reports
- Use-of-force reports and documentation
- Internal Affairs investigation records (final dispositions)
- Officer disciplinary records subject to the 2020 Police Records Access Law
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Booking records and detention logs

Regarding claimed exemptions: N.J.S.A. 47:1A-1.1(b) exempts "criminal investigatory records" but does not exempt all law enforcement records. Incident reports, arrest records, and booking documents are government records accessible under OPRA. Any withholding under the criminal investigatory records exemption requires identification of the specific harm that disclosure would cause — a generic "investigation" label is insufficient.

Pursuant to the Police Records Access Law (effective December 1, 2020), disciplinary records for law enforcement officers for conduct occurring on or after December 1, 2020 are subject to mandatory public disclosure in New Jersey. Please identify any disciplinary records responsive to this request that fall within this category.

Under N.J.S.A. 47:1A-6, the burden of justifying any denial rests on the custodian. Please state the specific statutory provision authorizing withholding for each record denied.

I am willing to pay fees at the OPRA standard rate of $0.05 per letter-size page, up to ${{fee_limit}}.

Under N.J.S.A. 47:1A-5(i), failure to respond within 7 business days is a deemed denial.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I am a member of the news media requesting these records for news-gathering purposes related to {{news_gathering_purpose}}. Under N.J.S.A. 47:1A-5(a), news media are entitled to fee waivers for news-gathering requests. Please process this request without charge.''',
        'expedited_language': '''I request expedited processing of this OPRA request. These records are time-sensitive because: {{expedited_justification}}. I need them by {{needed_by_date}}.''',
        'notes': 'NJ law enforcement OPRA template. Key features: (1) Police Records Access Law (effective December 1, 2020) requires disclosure of law enforcement disciplinary records for conduct after that date; (2) criminal investigatory records exemption requires specific harm showing — generic labels are insufficient; (3) incident reports, arrest records, and booking documents are public government records not covered by the criminal investigatory exemption; (4) body camera footage is public subject to applicable exemptions; (5) 7-business-day deadline with deemed-denial rule; (6) GRC is free and fast — file within 45 days of denial.',
    },
    {
        'jurisdiction': 'NJ',
        'record_type': 'contracts_procurement',
        'template_name': 'New Jersey OPRA Request — Government Contracts and Procurement',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Public Records Act Request — Government Contracts and Procurement Records, N.J.S.A. 47:1A-1 et seq.

Dear Custodian of Records:

Pursuant to the New Jersey Open Public Records Act (OPRA), N.J.S.A. 47:1A-1 et seq., I request access to the following government records relating to contracts and procurement:

{{description_of_records}}

Specifically, I request:
- All contracts, amendments, and exhibits between {{agency_name}} and {{contractor_or_vendor_name}} for the period {{date_range_start}} through {{date_range_end}}
- Requests for Proposal (RFPs), Requests for Qualifications (RFQs), and bid specifications
- Bid submissions and proposal documents from all bidders
- Evaluation records, scoring sheets, and selection committee notes
- Invoices, payment records, and change orders
- Correspondence relating to the above contracts

Regarding trade secret claims: Contract prices, amounts paid with public funds, and performance terms are public government records and do not qualify as trade secrets under New Jersey law. See Asbury Park Press v. County of Monmouth, 374 N.J. Super. 312 (App. Div. 2005). Any vendor trade secret claims must be supported by specific evidence and may be challenged. Redaction of specific proprietary technical information may be appropriate but wholesale withholding of contract documents is not.

Under N.J.S.A. 47:1A-6, the burden of justifying any withholding rests on the custodian.

I am willing to pay OPRA standard copying fees of $0.05 per letter-size page, up to ${{fee_limit}}. If records can be provided electronically, please do so at no charge.

Please respond within 7 business days as required by N.J.S.A. 47:1A-5(i).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived. These records concern public expenditures by {{agency_name}}, a matter of significant public interest and government accountability. Disclosure will benefit the public by enabling scrutiny of how public funds are spent. If provided electronically, there is no reproduction cost.''',
        'expedited_language': '''I request expedited processing because these procurement records relate to {{time_sensitive_reason}} and delay would harm the public interest in the following way: {{harm_from_delay}}. I need these records by {{needed_by_date}}.''',
        'notes': 'NJ procurement OPRA template. Key features: (1) contract prices and amounts paid with public funds are definitively public in NJ — cite Asbury Park Press v. County of Monmouth; (2) trade secret claims on bid documents are frequently overbroad — challenge specific redactions rather than wholesale withholding; (3) scoring sheets and evaluation records may be ACD-protected if pre-decisional but are public once the contract is awarded; (4) 7-business-day deadline; (5) GRC is the preferred forum for procurement record disputes — free and experienced with these issues.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in NJ_EXEMPTIONS:
        try:
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
        except Exception as e:
            errors += 1
            print(f'Error inserting exemption {exemption["short_name"]}: {e}', file=sys.stderr)

    print(f'NJ exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in NJ_RULES:
        try:
            existing = conn.execute(
                'SELECT id FROM response_rules WHERE jurisdiction = ? AND rule_type = ? AND param_key = ?',
                (rule['jurisdiction'], rule['rule_type'], rule['param_key'])
            ).fetchone()

            if existing:
                conn.execute(
                    '''
                    UPDATE response_rules SET
                        param_value = ?, day_type = ?, statute_citation = ?,
                        notes = ?, last_verified = datetime('now'), updated_at = datetime('now')
                    WHERE id = ?
                    ''',
                    (rule['param_value'], rule.get('day_type'), rule['statute_citation'],
                     rule.get('notes'), existing[0])
                )
                skipped += 1
            else:
                conn.execute(
                    '''
                    INSERT INTO response_rules (
                        jurisdiction, rule_type, param_key, param_value,
                        day_type, statute_citation, notes, last_verified
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                    ''',
                    (rule['jurisdiction'], rule['rule_type'], rule['param_key'],
                     rule['param_value'], rule.get('day_type'), rule['statute_citation'],
                     rule.get('notes'))
                )
                added += 1
        except Exception as e:
            errors += 1
            print(f'Error inserting rule {rule["param_key"]}: {e}', file=sys.stderr)

    print(f'NJ rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in NJ_TEMPLATES:
        try:
            existing = conn.execute(
                'SELECT id FROM request_templates WHERE jurisdiction = ? AND template_name = ?',
                (template['jurisdiction'], template['template_name'])
            ).fetchone()

            if existing:
                conn.execute(
                    '''
                    UPDATE request_templates SET
                        record_type = ?, template_text = ?,
                        fee_waiver_language = ?, expedited_language = ?,
                        notes = ?, updated_at = datetime('now')
                    WHERE id = ?
                    ''',
                    (template['record_type'], template['template_text'],
                     template.get('fee_waiver_language'), template.get('expedited_language'),
                     template.get('notes'), existing[0])
                )
                skipped += 1
            else:
                conn.execute(
                    '''
                    INSERT INTO request_templates (
                        jurisdiction, record_type, template_name,
                        template_text, fee_waiver_language, expedited_language,
                        notes, source
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'prdb-built')
                    ''',
                    (template['jurisdiction'], template['record_type'],
                     template['template_name'], template['template_text'],
                     template.get('fee_waiver_language'), template.get('expedited_language'),
                     template.get('notes'))
                )
                added += 1
        except Exception as e:
            errors += 1
            print(f'Error inserting template {template["template_name"]}: {e}', file=sys.stderr)

    print(f'NJ templates: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    total_added = 0
    total_skipped = 0
    total_errors = 0

    try:
        ea, es, ee = build_exemptions(conn)
        ra, rs, re_ = build_rules(conn)
        ta, ts, te = build_templates(conn)

        total_added = ea + ra + ta
        total_skipped = es + rs + ts
        total_errors = ee + re_ + te

        conn.commit()
    except Exception as e:
        total_errors += 1
        print(f'Fatal error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'NJ total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_nj', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
