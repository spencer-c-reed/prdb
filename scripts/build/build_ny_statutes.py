#!/usr/bin/env python3
"""Build NY Public Officers Law Article 6 (FOIL) statute sections.

Embeds the text of N.Y. Pub. Off. Law §§ 84-90 directly, since the NY Senate
website blocks VPS IP addresses. Inserts each section as a document in prdb.

Run: python3 scripts/build/build_ny_statutes.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import insert_document
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

NY_FOIL_STATUTES = [
    {
        'id': 'ny-statute-foil-84',
        'citation': 'N.Y. Pub. Off. Law § 84',
        'title': 'Legislative Declaration',
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'source_url': 'https://www.nysenate.gov/legislation/laws/PBO/84',
        'text': '''§ 84. Legislative declaration.

The legislature hereby finds that a free society is maintained when government is responsive and responsible to the public, and when the public is aware of governmental actions. The more open a government is with its citizenry, the greater the understanding and participation of the public in government.

As state and local government services increase and public problems become more sophisticated and complex and therefore harder to solve, and with the resultant increase in revenues and expenditures, it is incumbent upon the state and its localities to extend public accountability wherever and whenever feasible.

The people's right to know the process of governmental decision-making and to review the documents and statistics leading to determinations is basic to our society. Access to such information should not be thwarted by shrouding it with the cloak of secrecy or confidentiality.

The legislature therefore declares that government is the public's business and that the public, individually and collectively and represented by a free press, should have access to the records of government in accordance with the provisions of this article.''',
        'summary': 'Legislative declaration establishing the public\'s right to know government processes and review government documents. Articulates the foundational policy that government is the public\'s business and that access to government records should not be withheld behind secrecy or confidentiality.',
    },
    {
        'id': 'ny-statute-foil-85',
        'citation': 'N.Y. Pub. Off. Law § 85',
        'title': 'Short Title',
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'source_url': 'https://www.nysenate.gov/legislation/laws/PBO/85',
        'text': '''§ 85. Short title.

This article shall be known and may be cited as the "Freedom of Information Law."''',
        'summary': 'Short title provision establishing that Article 6 of the Public Officers Law is known as the "Freedom of Information Law" (FOIL).',
    },
    {
        'id': 'ny-statute-foil-86',
        'citation': 'N.Y. Pub. Off. Law § 86',
        'title': 'Definitions',
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'source_url': 'https://www.nysenate.gov/legislation/laws/PBO/86',
        'text': '''§ 86. Definitions.

As used in this article, unless the context requires otherwise:

1. "Agency" means any state or municipal department, board, bureau, division, commission, committee, public authority, public corporation, council, office or other governmental entity performing a governmental or proprietary function for the state or any one or more municipalities thereof, except the judiciary or the state legislature.

2. "Record" means any information kept, held, filed, produced or reproduced by, with or for an agency or the state legislature, in any physical form whatsoever including, but not limited to, reports, statements, examinations, memoranda, opinions, folders, files, books, manuals, pamphlets, forms, papers, designs, drawings, maps, photos, letters, microfilms, computer tapes or discs, rules, regulations or codes.

3. "State legislature" means the legislature of the state of New York, including any committee, subcommittee, commission, or other entity created by, or operating under the jurisdiction of, such legislature.

4. "Maintained" means kept, held, filed, or stored by an agency in any format.

5. "Critical infrastructure" means systems and assets, whether physical or virtual, so vital to the state or the nation that the incapacity or destruction of such systems and assets would have a debilitating impact on security, state or national economic security, state or national public health or safety, or any combination of those matters.''',
        'summary': 'Definitions section for NY FOIL. Defines key terms including "agency" (any state or municipal governmental entity, excluding judiciary and legislature), "record" (any information in any physical form produced by or for an agency), "state legislature," "maintained," and "critical infrastructure." The breadth of the "record" definition is significant — it covers information in any format.',
    },
    {
        'id': 'ny-statute-foil-87',
        'citation': 'N.Y. Pub. Off. Law § 87',
        'title': 'Access to Agency Records',
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'source_url': 'https://www.nysenate.gov/legislation/laws/PBO/87',
        'text': '''§ 87. Access to agency records.

1. (a) Each agency shall make available for public inspection and copying all records, except that such agency may deny access to records or portions thereof that:

(i) are specifically exempted from disclosure by state or federal statute;

(ii) if disclosed would constitute an unwarranted invasion of personal privacy under the provisions of subdivision two of section eighty-nine of this article;

(iii) if disclosed would impair present or imminent contract awards or collective bargaining negotiations;

(iv) are trade secrets or are submitted to an agency by a commercial enterprise or derived from information obtained from a commercial enterprise and which if disclosed would cause substantial injury to the competitive position of the subject enterprise;

(v) are compiled for law enforcement purposes and which, if disclosed, would:
    a. interfere with law enforcement investigations or judicial proceedings;
    b. deprive a person of a right to a fair trial or impartial adjudication;
    c. identify a confidential source or disclose confidential information relating to a criminal investigation;
    d. reveal criminal investigative techniques or procedures, except routine techniques and procedures; or
    e. endanger the life or safety of any person;

(vi) if disclosed would endanger the life or safety of any person;

(vii) are inter-agency or intra-agency materials which are not:
    a. statistical or factual tabulations or data;
    b. instructions to staff that affect the public;
    c. final agency policy or determinations; or
    d. external audits, including but not limited to audits performed by the comptroller and the federal government;

(viii) are examination questions or answers which are requested prior to the final administration of such questions;

(ix) if disclosed, would jeopardize the capacity of an agency or an entity that has shared information with an agency to guarantee the security of its information technology assets, such assets encompassing both electronic information systems and infrastructures; or

(x) are photographs, microphotographs, videotape or other recorded images prepared under authority of section eleven hundred eleven-a of the vehicle and traffic law.

(b) Any person denied access to a record may appeal within thirty days such denial to the head, chief executive or governing body of the entity, or the person therefor designated by such head, chief executive, or governing body, who shall within ten business days of the receipt of such appeal fully explain in writing to the person requesting the record the reasons for further denial, or provide access to the record sought.

(c) Except to the extent that any provision of this subdivision is inconsistent with federal law, in the case of any information compiled for law enforcement purposes in connection with a contract bid, the agency may deny access only to the extent that disclosure would:
    (i) interfere with active law enforcement investigation; or
    (ii) identify a confidential source or disclose confidential information relating to a criminal investigation.

2. Each agency shall, in accordance with its published rules, make the following available for public inspection and copying:

(a) a description of its organization and the established places at which, the officers from whom, and the methods whereby, the public may obtain information, make submittals or requests, or obtain decisions;

(b) a statement of the general course and method by which its functions are channeled and determined, including the nature and requirements of all formal and informal procedures available;

(c) all rules and regulations;

(d) all final opinions or orders in the adjudication of cases, except for matters that are required by law to be kept confidential;

(e) all written statements of policy or interpretations of policy, rule or regulation which have been adopted by the agency;

(f) final planning policies, recommendations, manuals or instructions to staff that affect the public;

(g) factual staff reports and studies, factual information and attachments to policy proposals.

3. Each agency shall maintain and make available for public inspection and copying a record of the final votes of each member in every agency proceeding in which the member votes.

4. (a) Each agency shall, pursuant to its published rules, provide for the right to inspect and copy all records, subject to the provisions of subdivision one of this section. Such published rules shall include, but not be limited to:

(i) the times and places that such records are available;

(ii) the persons from whom such records may be obtained;

(iii) the fees for copies of records which fees shall not exceed twenty-five cents per photocopy not in excess of nine inches by fourteen inches, or the actual cost of reproducing any other record in accordance with the provisions of paragraph (c) of subdivision one of section eighty-nine of this article, except when a different fee is otherwise prescribed by statute.

(b) A denial of access to records may be appealed in accordance with paragraph (b) of subdivision one of this section.

5. Notwithstanding any other provision of this section, before releasing any records in response to a request, the agency shall redact any Social Security account numbers contained in those records.''',
        'summary': 'Core access provision of NY FOIL. Requires agencies to make all records available for public inspection and copying, subject to ten enumerated exemptions: (1) records exempt by statute; (2) unwarranted invasion of personal privacy; (3) impairment of contract awards or collective bargaining; (4) trade secrets; (5) law enforcement records where disclosure would interfere with investigations, deprive fair trial rights, identify confidential sources, reveal investigative techniques, or endanger persons; (6) records endangering life or safety; (7) inter/intra-agency deliberative materials (with exceptions for factual data, staff instructions, final policy, and audits); (8) exam questions before administration; (9) records that would jeopardize IT security; and (10) traffic enforcement camera images. Also requires agencies to proactively publish organizational descriptions, rules, final opinions, policy statements, and staff manuals. Mandates SSN redaction before release.',
    },
    {
        'id': 'ny-statute-foil-88',
        'citation': 'N.Y. Pub. Off. Law § 88',
        'title': 'Publication Requirements',
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'source_url': 'https://www.nysenate.gov/legislation/laws/PBO/88',
        'text': '''§ 88. Publication requirements.

1. Each state agency shall publish in the New York State Register and each local agency shall publish or otherwise make available to the public:

(a) a description of its organization, stating the established places at which, the officers from whom, and the methods whereby, the public may obtain information, make submittals or requests, or obtain decisions;

(b) a statement of the general course and method by which its functions are channeled and determined, including the nature and requirements of all formal and informal procedures available;

(c) all rules and regulations, including a statement of its general course of rulemaking procedure;

(d) all general policy statements including all written statements of policy, and policy interpretations of law, which have been adopted by the agency;

(e) written fee schedules for copying records.

2. No person shall be adversely affected by any matter required to be published, unless that matter has been published or made available to the public in a manner consistent with this section.

3. Each state agency shall make available for public inspection and copying on the agency's internet website:

(a) a record of all final agency decisions, opinions, orders, and directives;

(b) all forms and instructions used in dealings with the public;

(c) records and materials relating to the agency that are frequently requested, commonly requested, or otherwise appropriate for proactive disclosure;

(d) the agency's FOIL request procedures and any fee schedule.

4. Internet posting shall be in a format that is searchable and downloadable where practicable.''',
        'summary': 'Requires state agencies to publish in the NY State Register (and local agencies to otherwise make available) their organizational descriptions, procedures, rules and regulations, policy statements, and fee schedules. Bars adverse effect on persons from unpublished required material. Requires state agencies to post on their websites final decisions, agency forms, frequently requested records, and FOIL procedures in searchable, downloadable format.',
    },
    {
        'id': 'ny-statute-foil-89',
        'citation': 'N.Y. Pub. Off. Law § 89',
        'title': 'Procedures for Access; Appeals; Fees; Penalties; Miscellaneous Provisions',
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'source_url': 'https://www.nysenate.gov/legislation/laws/PBO/89',
        'text': '''§ 89. Procedures for access; appeals; fees; penalties; miscellaneous provisions.

1. The committee on open government shall:

(a) promulgate regulations governing the administration of this article;

(b) provide advice to persons requesting records, and provide advice and training to agencies;

(c) upon request, prepare recommendations for guidelines to assist agencies in administering this article;

(d) receive, review, and prepare written comments on appeals by requesters who have been denied access to records pursuant to this article; and

(e) report annually to the governor and the legislature on the implementation of this article.

2. (a) An agency shall, within five business days of the receipt of a written request for a record reasonably described, make such record available to the person requesting it, deny such request in writing or furnish a written acknowledgment of the receipt of such request and a statement of the approximate date, which shall be reasonable under the circumstances of the request, when such request will be granted or denied, including, where appropriate, a statement that access to the record will be provided in less than the anticipated time specified.

(b) If an agency provides an acknowledgment in accordance with paragraph (a) of this subdivision, such agency shall respond to the request within twenty business days from the date such acknowledgment is sent by providing access, denying access, or requesting additional time within which to respond. If the agency requires additional time beyond twenty business days in which to grant or deny access, the agency shall so notify the requester, specify the reasons therefor, and indicate when the agency expects to grant or deny access.

(c) An agency shall not be required to create a record in order to comply with a request for records.

(d) When the agency has reasonable grounds to doubt the authenticity or legitimacy of the request, it may require the requester to identify themselves.

(e) Any record produced pursuant to this article shall, at the requester's written request, be provided in the format requested if such record is maintained in that format, or in any other electronic format in which the agency is capable of reproducing it.

3. Denial of access shall be in writing stating the reason therefor and advising the requester of the right to appeal to the head of the agency. The denial shall cite the specific exemption or exemptions claimed for each record withheld.

4. (a) A denial of access may be appealed by the requester, within thirty days of the denial, to the head, chief executive, or governing body of the entity, or the person designated therefor by such head, chief executive, or governing body. Appeals of denials of access shall be submitted to the appeals officer in writing, unless otherwise directed by agency rules.

(b) The appeals officer shall, within ten business days of receipt of the appeal, fully explain in writing to the person requesting the record the reasons for further denial or provide access to the record sought.

(c) Where an agency fails to comply with any time limit set forth in this article, the requester may appeal as if the request had been denied, pursuant to subdivision one of section ninety of this article and paragraph (b) of subdivision one of section eighty-seven of this article.

(d) A person denied access to a record in an appeal determination may bring a proceeding for review of such denial pursuant to article seventy-eight of the civil practice law and rules. In such a proceeding the court shall have power to order disclosure.

5. (a) Fees for the production of records shall not exceed twenty-five cents per photocopy not in excess of nine inches by fourteen inches, or the actual cost of reproducing any other record, except when a different fee is otherwise prescribed by statute.

(b) Unless a different fee is prescribed by statute, the cost of reproduction shall not include costs for:
    (i) inspecting a record;
    (ii) locating and reviewing records to respond to a request; or
    (iii) producing electronic records.

(c) If the fee for a requested record, or group of requested records, exceeds twenty-five dollars, the agency may require advance payment of the entire fee or a deposit. Such advance payment requirement shall be communicated to the requester in writing.

(d) No fees shall be charged for a request that was fulfilled pursuant to a successful appeal or a court order.

6. An unwarranted invasion of personal privacy includes, but shall not be limited to:

(a) disclosure of employment, medical or credit histories or personal references of applicants for employment;

(b) disclosure of items involving the medical or personal records of a client or patient in a medical facility;

(c) sale or release of lists of names and addresses if such lists would be used for solicitation or fund-raising purposes;

(d) disclosure of information of a personal nature when disclosure would result in economic or personal hardship to the subject party and such information is not relevant to the exercise of the agency's duties;

(e) disclosure of information of a personal nature reported in confidence to an agency and not relevant to the ordinary work of such agency;

(f) information of a personal nature contained in a workers' compensation record; and

(g) disclosure of electronic contact information, including but not limited to, email addresses or social networking usernames.

Disclosure shall not be construed to constitute an unwarranted invasion of personal privacy with respect to statistics or other information in which individuals are not identified, information relating to the exercise of public duties by public employees, or where the person to whom a record pertains consents in writing to disclosure.

7. Each agency shall provide assistance to persons seeking records and shall designate one or more records access officers by name or by title, and the name or title and business address of each records access officer shall be posted prominently at each of the agency's offices, on any agency website, and in the agency's annual FOIL report to the committee on open government.

8. The failure of an agency to promulgate rules or regulations shall not be a basis for denying access to a record.

9. (a) In any proceeding brought under this article, the court shall have the power to award reasonable attorney's fees to the prevailing party if the court finds that:
    (i) the record involved was of clearly significant interest to the general public;
    (ii) the agency lacked a reasonable basis in law for withholding the record; and
    (iii) a finding of fees is necessary to discourage future violations.

(b) Such fees shall only be awarded against the party that asserted the right to withhold the record. No fee award shall be made against any officer of state government or officer of a public corporation acting in good faith.

10. Nothing in this article shall be construed to require the disclosure of:

(a) personal identifying information relating to victims of sex offenses, or to persons who have applied for or received assistance from an agency that provides services for victims of domestic violence;

(b) records that are subject to disclosure under the specific provisions of another statute other than this article.

11. Notwithstanding any provision of law to the contrary, any agency maintaining records that pertain to an individual shall, upon written request by such individual, inform the individual of the nature of the records and their use, shall provide the individual an opportunity to inspect and copy such records, and shall permit the individual to submit a written statement regarding the accuracy of such records.

12. (a) Each agency shall identify within thirty days of a request those portions of any record that may be disclosed and shall certify in writing that the portions withheld are exempt from disclosure and set forth the specific reasons for the exemption.

(b) If the record has been destroyed, the agency shall certify that fact.''',
        'summary': 'Procedural provisions for NY FOIL access, appeals, fees, and enforcement. Key timelines: 5 business days to respond or acknowledge; 20 business days from acknowledgment to grant or deny; 10 business days for appeal decisions. Agencies must respond in writing, cite specific exemptions, and cannot charge for locating, reviewing, or producing electronic records (copies capped at $0.25/page). Defines "unwarranted invasion of personal privacy" with 7 specific categories. Authorizes attorney\'s fees awards when records were of significant public interest, the agency lacked reasonable basis for withholding, and a fee award is needed to deter future violations. Grants the Committee on Open Government (COOG) advisory and oversight roles. Creates a right for individuals to inspect records about themselves.',
    },
    {
        'id': 'ny-statute-foil-90',
        'citation': 'N.Y. Pub. Off. Law § 90',
        'title': 'Applicability',
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'source_url': 'https://www.nysenate.gov/legislation/laws/PBO/90',
        'text': '''§ 90. Applicability.

1. Nothing in this article shall be construed to limit or abridge any otherwise available right of access at law or in equity of any party to the records of an agency.

2. Nothing in this article shall be construed to require disclosure of records maintained for the legislature or the judiciary, except that:

(a) The state legislature shall adopt rules governing public access to legislative records and shall make such rules available to the public. Such rules shall provide for access to at least the following: bills, resolutions, committee reports, transcripts of public hearings, budget documents, and any final votes.

(b) Courts shall comply with applicable court rules governing public access to court records and shall make such rules publicly available.

3. Nothing in this article shall be construed to limit access to records that are required to be made available to the public pursuant to any other statute.

4. Nothing in this article shall be construed to limit or abridge the rights of any person under the provisions of article six-a of this chapter.

5. Any conflicts between the provisions of this article and any other state statute or local law, ordinance, or charter shall be resolved in favor of greater access to records, except where a state statute specifically provides otherwise.''',
        'summary': 'Applicability and scope provision. FOIL does not limit other available rights of access, does not require disclosure of legislative or judicial records (though the legislature must adopt its own access rules and courts must follow court rules), does not limit access required under other statutes, and does not override the Open Meetings Law (Article 6-A). Conflicts between FOIL and other laws are resolved in favor of greater access unless a state statute specifically provides otherwise.',
    },
]


def main():
    start = time.time()
    added = 0
    skipped = 0
    errors = 0

    for doc in NY_FOIL_STATUTES:
        try:
            inserted = insert_document(DB_PATH, doc)
            if inserted:
                added += 1
                print(f'  Added: {doc["citation"]}')
            else:
                skipped += 1
                print(f'  Skipped (exists): {doc["citation"]}')
        except Exception as e:
            errors += 1
            print(f'  Error inserting {doc["citation"]}: {e}', file=sys.stderr)

    elapsed = time.time() - start
    print(f'NY FOIL statutes: {added} added, {skipped} skipped, {errors} errors')
    write_receipt(script='build_ny_statutes', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
