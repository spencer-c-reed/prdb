#!/usr/bin/env python3
"""Build state public records statute documents for FL, GA, HI, ID, IL, IN, IA, KS."""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

DOCUMENTS = [
    # =========================================================================
    # FLORIDA — Fla. Stat. Ch. 119 (Public Records Law / Sunshine Law)
    # =========================================================================
    {
        'id': 'fl-statute-public-records',
        'citation': 'Fla. Stat. Ch. 119',
        'title': 'Florida Public Records Law (Government-in-the-Sunshine Law — Public Records Component)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'FL',
        'source': 'prdb-built',
        'text': '''FLORIDA PUBLIC RECORDS LAW
Fla. Stat. Ch. 119 (Public Records)

CHAPTER 119 — PUBLIC RECORDS

SECTION 119.01 — GENERAL STATE POLICY ON PUBLIC RECORDS

Florida's constitution and statutes establish one of the broadest public records access regimes in the United States. Article I, Section 24 of the Florida Constitution independently guarantees every person the right to inspect or copy any public record made or received in connection with the official business of any public body, officer, or employee of the state, or of persons acting on their behalf. This constitutional provision is self-executing, meaning it operates independently of any implementing statute, and can only be limited by the legislature through a two-thirds vote of each chamber, with a specific public necessity finding.

Chapter 119 of the Florida Statutes implements and supplements this constitutional guarantee. The legislature has declared it to be the policy of the state that all state, county, and municipal records are open for personal inspection and copying by any person, and that providing access to public records is a duty of each agency.

SECTION 119.011 — DEFINITIONS

"Public records" includes all documents, papers, letters, maps, books, tapes, photographs, films, sound recordings, data processing software, or other material, regardless of the physical form, characteristics, or means of transmission, made or received pursuant to law or ordinance or in connection with the transaction of official business by any agency. This definition is intentionally expansive and has been interpreted by Florida courts to encompass virtually any material created or received by a government entity in connection with official business, regardless of format.

"Agency" means any state, county, district, authority, or municipal officer, department, division, board, bureau, commission, or other separate unit of government created or established by law, including the Commission on Ethics, and any other public or private agency, person, partnership, corporation, or business entity acting on behalf of any public agency. This definition extends beyond traditional government offices to reach private entities performing governmental functions under contract or delegation.

"Custodian of public records" means the elected or appointed state, county, or municipal officer charged with the responsibility of maintaining the office having public records, or that officer's designee.

SECTION 119.07 — INSPECTION AND COPYING OF RECORDS; PHOTOGRAPHING PUBLIC RECORDS

(1) Every person who has custody of a public record shall permit the record to be inspected and copied by any person desiring to do so, at any reasonable time, under reasonable conditions, and under supervision by the custodian of the public records or the custodian's designee.

A requester is not required to state a reason for the request, identify themselves, or explain the purpose for which the records will be used. The right of access is not conditioned upon citizenship, residency, or any other status. These principles have been reinforced by the Florida Supreme Court in numerous decisions and reflect the law's fundamental premise that public records belong to the people.

The custodian must acknowledge a request to inspect or copy records promptly and respond to such request in good faith. While Chapter 119 does not specify a fixed statutory deadline in days for response (unlike some states' FOIA statutes), the Florida Supreme Court has held that agencies must respond within a "reasonable time," and unreasonable delay may constitute a violation of the statute. In practice, agencies are expected to begin producing records promptly, with an initial response acknowledging receipt typically expected within a few business days.

(2) An agency may not establish special conditions or fees that would effectively deny or materially impair access. Inspection of records in the agency's offices must be allowed without charge. An agency may charge a fee for copies, but the fee may not exceed the actual cost of duplication, including the labor cost and overhead directly attributable to the duplication effort. The actual cost of duplication does not include the agency's normal operating costs that would exist regardless of any records request.

For standard letter- and legal-size copies, the maximum allowable fee is $0.15 per one-sided copy and $0.20 per two-sided copy. For certified copies, the fee is $1.00 per page. For other types of duplication (electronic media, oversized copies, etc.), the fee must be based on the actual cost. If the nature or volume of records requested requires extensive use of information technology resources or extensive clerical or supervisory assistance, the agency may charge a reasonable service charge based on the actual cost incurred, but the agency must provide written notice of the estimated charge before incurring the expense.

SECTION 119.071 — GENERAL EXEMPTIONS FROM INSPECTION OR COPYING OF PUBLIC RECORDS

Florida has over 1,100 statutory exemptions to public records access — more than any other state. These exemptions are scattered throughout the Florida Statutes, not consolidated in Chapter 119. However, Section 119.071 contains many of the most commonly invoked general exemptions, organized by category.

(1) Exemptions related to agency administration:
(a) Examination questions and answer sheets of examinations administered by a governmental agency for the purpose of licensure, certification, or employment are exempt until the examination is completed.
(b) Sealed bids, proposals, or replies received by an agency pursuant to a competitive solicitation are exempt until the agency provides notice of an intended decision or until 30 days after opening the bids, whichever is earlier.
(c) Any data processing software obtained by an agency under a licensing agreement that prohibits its disclosure is exempt.
(d) Records related to the security of technology, including network schematics, passwords, IP addresses associated with agency technology infrastructure, and vulnerability assessments, are exempt.

(2) Exemptions related to law enforcement and investigations:
(a) Active criminal intelligence information and active criminal investigative information are exempt from disclosure. "Active" means a criminal intelligence or investigative activity is ongoing, with a reasonable good-faith belief that the activity may lead to a criminal prosecution. Once the investigation becomes inactive (i.e., no prosecution is anticipated or the prosecution is concluded), the information generally loses its exempt status.
(b) Information revealing the identity of a confidential informant or confidential source is exempt.
(c) Information revealing surveillance techniques, procedures, or apparatus is exempt.
(d) Information revealing undercover personnel identities is exempt.

(3) Exemptions related to personal privacy and safety:
(a) Social security numbers held by an agency are confidential and exempt.
(b) Bank account numbers, debit, charge, and credit card numbers held by an agency are exempt.
(c) Medical records, including substance abuse treatment records, are exempt unless specifically made public by another statute.
(d) The home addresses, telephone numbers, dates of birth, and photographs of active or former law enforcement personnel, judges, state attorneys, public defenders, firefighters, and certain other categories of public employees and their families are exempt from disclosure. This exemption was enacted in response to safety concerns and has been expanded repeatedly by the legislature to cover additional categories of employees.

(4) Exemptions related to trade secrets and proprietary business information:
Trade secrets as defined in Section 688.002, Florida Statutes, held by an agency are exempt from disclosure. The entity claiming the trade secret must identify the information as a trade secret and must demonstrate that the information meets the statutory definition.

SECTION 119.0701 — CONTRACTS; PUBLIC RECORDS; REQUEST FOR CONTRACTOR RECORDS; CIVIL ACTION

When a public agency contracts with a private entity for services, the contract must include provisions requiring the contractor to comply with public records requirements, including keeping and maintaining public records, providing access to public records on the same terms as the agency itself, and transferring records to the agency at the end of the contract.

SECTION 119.10 — VIOLATION OF CHAPTER; PENALTIES

Any public officer who violates any provision of Chapter 119 commits a noncriminal infraction, punishable by a fine not exceeding $500.

Any person who willfully and knowingly violates any provision of Chapter 119 commits a misdemeanor of the first degree, punishable by a fine of up to $1,000 and/or imprisonment for up to one year.

SECTION 119.12 — ATTORNEY'S FEES

If a civil action is filed to enforce the provisions of Chapter 119, and the court determines that the agency unlawfully refused to permit a public record to be inspected or copied, the court shall assess and award against the agency responsible the reasonable costs of enforcement, including reasonable attorney's fees.

This fee-shifting provision is a critical enforcement mechanism. It incentivizes requesters to enforce their rights by eliminating the financial risk of litigation when the requester prevails. The fee-shifting is mandatory ("shall"), not discretionary, once the court finds a violation.

SECTION 119.11 — ACCELERATED HEARING; IMMEDIATE COMPLIANCE

A court has the authority to order an accelerated hearing on a petition for access to public records. The statute provides that in an action to enforce Chapter 119, the court may issue an order requiring immediate compliance, and the order may be enforced through contempt proceedings.

ENFORCEMENT AND REMEDIES

Florida's public records enforcement framework provides multiple avenues for redress:

1. Civil action: Any person may bring a civil action in circuit court to compel compliance with Chapter 119. There is no requirement to exhaust administrative remedies before filing suit.

2. Attorney's fees: Mandatory fee-shifting in favor of prevailing requesters, as described above.

3. Criminal penalties: Willful and knowing violations are punishable as first-degree misdemeanors.

4. Writ of mandamus: A court may issue a writ of mandamus directing an agency to comply with the law.

5. In camera inspection: Courts may review disputed records in camera (in private) to determine whether an exemption applies, without requiring the records to be disclosed publicly during the litigation.

6. The Florida Attorney General, while not having direct enforcement authority under Chapter 119, regularly issues advisory opinions interpreting the Public Records Act and the Sunshine Law. These opinions, while not legally binding, are highly persuasive and are frequently cited by courts.

INTERACTION WITH THE SUNSHINE LAW

Chapter 119 (Public Records) is frequently discussed alongside Chapter 286 (Government in the Sunshine Law), which requires that meetings of public boards and commissions be open to the public. Together, these two chapters form what is colloquially known as Florida's "Sunshine Law." While Chapter 286 addresses open meetings, Chapter 119 addresses open records. The two statutes are complementary and are interpreted in pari materia — that is, they are read together to effectuate the overarching policy of open government.

Records created in connection with a meeting subject to Chapter 286 are themselves public records under Chapter 119. Written communications between members of a public board regarding matters that foreseeably will come before the board for action may also implicate both statutes — they are public records under Chapter 119, and their use to circumvent the open meetings requirement of Chapter 286 may constitute a separate violation.

CONSTITUTIONAL DIMENSION

Uniquely among American states, Florida's right of access to public records has constitutional status. Article I, Section 24 of the Florida Constitution provides: "Every person has the right to inspect or copy any public record made or received in connection with the official business of any public body, officer, or employee of the state, or persons acting on their behalf." This provision, adopted by voter referendum in 1992 (Amendment 4), means that: (1) the right of access exists independently of any statute; (2) exemptions must be enacted by the legislature with a two-thirds supermajority vote in each chamber, accompanied by a statement of public necessity and drafted to be no broader than necessary; and (3) all existing statutory exemptions were subject to sunset review unless reenacted. This constitutional framework makes Florida's public records protections among the strongest in the nation and creates a high bar for the enactment or expansion of exemptions.

SCOPE AND APPLICATION

Chapter 119 applies broadly to all levels of state and local government in Florida, including: the executive branch and all state agencies; counties, cities, towns, and other municipalities; special districts, authorities, and other governmental entities; the State Board of Administration; state universities and colleges; and private entities acting on behalf of a public agency. The judiciary and the legislature are covered by the constitutional provision (Art. I, § 24) but have separate implementing rules rather than being directly governed by Chapter 119 in all respects.

Records in any format are covered — paper, electronic, audio, video, email, text messages, social media communications made in connection with official business, and any other medium. Florida courts have consistently held that the format of the record does not affect its status as a public record; what matters is whether it was made or received in connection with official business.''',
        'summary': 'Florida\'s Public Records Law (Chapter 119, Florida Statutes), combined with Article I, Section 24 of the Florida Constitution, establishes one of the broadest public records access regimes in the United States, covering all records made or received in connection with official business regardless of format. The law provides strong enforcement mechanisms including mandatory attorney\'s fees, criminal penalties for willful violations, and over 1,100 statutory exemptions that must be enacted by a two-thirds legislative supermajority.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # GEORGIA — O.C.G.A. §§ 50-18-70 through 50-18-77 (Georgia Open Records Act)
    # =========================================================================
    {
        'id': 'ga-statute-public-records',
        'citation': 'O.C.G.A. §§ 50-18-70 through 50-18-77',
        'title': 'Georgia Open Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'GA',
        'source': 'prdb-built',
        'text': '''GEORGIA OPEN RECORDS ACT
O.C.G.A. §§ 50-18-70 through 50-18-77

SECTION 50-18-70 — POLICY OF OPEN GOVERNMENT; DEFINITIONS

(a) The General Assembly finds and declares that the strong public policy of this state favors open government; that open government is essential to a free, open, and democratic society; and that public access to public records should be encouraged to foster confidence in government and so that the public can evaluate the expenditure of public funds and the efficient and proper functioning of its institutions.

(b) As used in this article:

"Public record" means all documents, papers, letters, maps, books, tapes, photographs, computer-based or generated information, data, data fields, or similar material prepared and maintained or received by a public office or agency, or by a private person or entity in the performance of a service or function for or on behalf of a public office or agency, or received in the course of any agency's official business. "Public record" does not include those items made confidential or privileged by law.

"Agency" or "public agency" or "public office" means every state department, agency, board, bureau, commission, public corporation, and authority; every county, municipal corporation, school district, or other political subdivision of this state; every department, agency, board, bureau, commission, authority, and similar body of each such county, municipal corporation, or other political subdivision of the state; and any other entity or body which receives or expends public funds, including any nonprofit organization to which a public agency provides funds or over which a public agency exercises regulatory authority.

SECTION 50-18-71 — RIGHT OF ACCESS; RESPONSE TIMES; FEES

(a) All public records shall be open for personal inspection and copying, except those which by order of a court of this state or by law are specifically exempted from disclosure.

(b) A written request for records is not required but may be made. The law does not require a requester to identify themselves or explain the purpose of the request. Any person may request access to public records, regardless of citizenship, residency, or other status.

(c) Response Timeline:
Within three business days of receiving a request, an agency must determine whether the requested records are subject to access and, where appropriate, make the records available. If the records cannot be produced within three business days, the agency must, within that three-business-day period, provide a written description of the records and a timetable for their production, along with a statement of the applicable fees. The agency must produce the records "as soon as practicable" after the initial three-day response period.

There is no statutory maximum time limit beyond "as soon as practicable," but courts have enforced this requirement and have found agencies in violation for unreasonable delays. The three-business-day clock begins when the request is received by the agency, not when it is forwarded to a particular department or records custodian.

(d) Fees:
Agencies may charge a fee for the search, retrieval, and copying of records, but the fee must be based on the actual cost to the agency. For copies, agencies may charge a reasonable fee not to exceed $0.25 per page for letter- or legal-size copies. For electronic records, the agency may charge for the actual cost of the electronic medium (CD, flash drive, etc.) and for the direct administrative cost of complying with the request, including search and retrieval time, but may not charge for the initial review to determine whether records are subject to disclosure.

No agency may establish fees or conditions of access that effectively deny access or materially impair a person's right to inspect public records. Access for the purpose of inspection (viewing records without copying) cannot be conditioned on payment of a fee.

(e) Electronic Records:
When public records are maintained in electronic format, the agency must produce them in the format in which they are maintained, unless the requester agrees to a different format. Agencies may not require requesters to accept paper copies when records exist in electronic form, and agencies may not claim that a records management system's inability to produce records in a particular format justifies nondisclosure when the data exists in the system.

SECTION 50-18-72 — EXEMPTIONS

Georgia law provides a number of categories of records that are exempt from disclosure under the Open Records Act. The exemptions are construed narrowly, with doubts resolved in favor of disclosure. Key exemptions include:

(a) Records specifically required by federal statute or regulation to be kept confidential.

(b) Medical and veterinary records, and records compiled for social services related to the provision of public assistance.

(c) Records of law enforcement, prosecution, or regulatory agencies in any pending investigation or prosecution of criminal or unlawful activity, when disclosure would be harmful to the investigation. Once the investigation is no longer pending or active, the records become open. Records of completed investigations are generally subject to disclosure, though specific information (such as the identity of confidential informants) may remain protected.

(d) Records that would reveal confidential informants or confidential investigative techniques.

(e) Individual tax records, except in aggregate or statistical form.

(f) Sealed bids and proposals prior to the time set for public opening.

(g) Real estate appraisals made for the purpose of acquisition of property by an agency until the property has been acquired or the proposed acquisition is abandoned.

(h) Records of the Georgia Bureau of Investigation regarding criminal history information, except as provided by other law.

(i) Records concerning public employees' home addresses, home telephone numbers, day and month of birth, social security numbers, insurance or medical information, bank account information, and similar personal data are exempt from disclosure.

(j) Records that are attorney-client privileged communications or attorney work product.

(k) Trade secrets obtained from a person or business entity, provided the trade secret is identified as such at the time of submission to the agency and is maintained in confidence by the agency.

(l) Records containing information related to the security of any public building, structure, facility, utility, or infrastructure, including blueprints, building plans, vulnerability assessments, and security protocols.

SECTION 50-18-73 — ENFORCEMENT; PENALTIES

(a) Civil Action: Any person or entity whose request for access to records has been denied may bring a civil action in superior court to obtain access. The action must be filed in the county where the records are maintained or the county where the agency has its principal office.

(b) In Camera Review: The court may examine contested records in camera (privately) to determine whether an exemption applies.

(c) Burden of Proof: The agency bears the burden of proving that a record or portion of a record is exempt from disclosure. Doubts are resolved in favor of disclosure.

(d) Attorney's Fees and Litigation Costs: If the court finds that the agency has substantially and materially failed to comply with the Open Records Act and the agency cannot show that it acted in reasonable good faith, the court shall award reasonable attorney's fees and litigation costs to the prevailing requester.

(e) Civil Penalties: The court may impose a civil penalty not to exceed $1,000 for each violation of the Act. For a second offense within a 12-month period, the penalty may be up to $2,500. For repeat offenses, penalties may increase.

(f) Criminal Penalties: Any person who knowingly and willfully violates the Open Records Act by failing or refusing to provide access to records as required by the Act is guilty of a misdemeanor and, upon conviction, shall be fined not more than $1,000 or imprisoned for not more than 12 months, or both. A second conviction within a 36-month period is punishable as a misdemeanor of a high and aggravated nature, with a fine of up to $2,500.

(g) Personal Liability: Elected officials and heads of agencies may be held personally liable for violations of the Open Records Act. The statute specifically provides that a public officer or agency head who knowingly and willfully fails to comply with the Act may be subject to personal liability for attorney's fees and costs in addition to any other penalties.

SECTION 50-18-74 — RECORDS MANAGEMENT; RETENTION

Public officers and agency heads are required to maintain records in accordance with approved retention schedules established by the State Records Committee. The Open Records Act works in conjunction with the Georgia Records Act (O.C.G.A. § 50-18-90 et seq.) to ensure that records are properly created, maintained, and made available. The destruction of records in contravention of approved retention schedules, particularly when done to avoid disclosure, may itself be a violation of law and may give rise to adverse inferences in litigation.

SECTION 50-18-75 — ATTORNEY GENERAL MEDIATION

When a dispute arises between a requester and an agency regarding access to records, either party may request the Attorney General to mediate the dispute. This mediation is voluntary and nonbinding but provides an informal mechanism for resolving disputes without litigation. The Attorney General's office maintains an Open Government Unit that provides guidance on the Open Records Act, issues opinions, and assists with compliance questions.

SECTION 50-18-76 — RELATIONSHIP TO OTHER LAWS

The Open Records Act is to be liberally construed to carry out its purpose of providing open access to public records. Where a conflict exists between the Open Records Act and another statute that restricts access to records, the more specific statute controls, but exemptions are to be construed narrowly.

SECTION 50-18-77 — RECORDS OF PRIVATE ENTITIES

When a private entity performs a governmental function, including through contract, grant, or other arrangement with a public agency, the records of that private entity related to the governmental function are subject to the Open Records Act to the same extent as if the records were maintained by the public agency itself. This provision ensures that the outsourcing or privatization of government services does not result in the loss of public access to records that would otherwise be available.

ADDITIONAL PROVISIONS

Georgia's courts have consistently emphasized that the Open Records Act is remedial legislation that must be broadly construed in favor of access. The Georgia Supreme Court has stated that the Act "is not to be used to shield from public scrutiny the activities of those who act on behalf of the government" and that "exemptions are to be narrowly construed." Notable case law includes:

- Napper v. Georgia Television Co., 257 Ga. 156 (1987), establishing that the burden is on the agency to justify withholding records.
- Hardaway Co. v. Rives, 262 Ga. 631 (1992), addressing the scope of the trade secret exemption and requiring specific identification of trade secrets.
- Clayton County Hospital Authority v. Eason, 276 Ga. 166 (2003), extending the Act to cover private entities performing governmental functions.

The Georgia Attorney General's office publishes an Open Records and Open Meetings Handbook that provides practical guidance on compliance and is regularly updated. This handbook, while not binding legal authority, is widely consulted by agencies, requesters, and practitioners.''',
        'summary': 'The Georgia Open Records Act (O.C.G.A. §§ 50-18-70 through 50-18-77) requires all public records to be open for inspection and copying, with agencies required to respond within three business days and produce records "as soon as practicable." The Act provides strong enforcement through civil and criminal penalties, mandatory attorney\'s fees for bad-faith denials, and personal liability for officials who knowingly violate its provisions.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # HAWAII — HRS Ch. 92F (Uniform Information Practices Act - UIPA)
    # =========================================================================
    {
        'id': 'hi-statute-public-records',
        'citation': 'HRS Ch. 92F',
        'title': 'Hawaii Uniform Information Practices Act (UIPA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'HI',
        'source': 'prdb-built',
        'text': '''HAWAII UNIFORM INFORMATION PRACTICES ACT (UIPA)
HRS Chapter 92F

SECTION 92F-1 — FINDINGS AND PURPOSE

The Hawaii legislature found that government transparency is essential to the functioning of a democratic society and that the formation and conduct of public policy should be open to public scrutiny and participation. The legislature enacted the Uniform Information Practices Act (UIPA) in 1988 to create a unified framework for access to government records, replacing a fragmented patchwork of disclosure and confidentiality provisions scattered across multiple statutes. The UIPA is Hawaii's primary public records access law and is distinct from most mainland states' freedom of information statutes in its structure and administration.

SECTION 92F-2 — SCOPE; APPLICATION

The UIPA applies to all "agencies" of the State of Hawaii. "Agency" is broadly defined to include every state and county board, commission, department, or officer of the state or county government authorized to perform any function of the state or county government, and any entity which is an agency of the state or county government. This includes executive branch agencies, boards and commissions, county governments, and other entities performing governmental functions.

The UIPA does not directly apply to the judiciary or the legislature, though both have adopted rules governing public access to their own records that incorporate many UIPA principles.

SECTION 92F-3 — DEFINITIONS

"Government record" means information maintained by an agency in written, auditory, visual, electronic, or other physical form. This definition is format-neutral and covers paper documents, electronic files, emails, databases, audio recordings, video recordings, photographs, and any other medium.

"Personal record" means any item, collection, or grouping of information about an individual that is maintained by an agency, including but not limited to the individual's education, financial transactions, medical history, and criminal or employment history, and that contains the individual's name or other identifying particular.

SECTION 92F-11 — AFFIRMATIVE AGENCY DISCLOSURE RESPONSIBILITIES

All government records are open to public inspection and duplication during regular business hours, unless an exception under Part III of the UIPA applies. This establishes disclosure as the default, consistent with the legislative purpose of promoting government transparency.

Each agency must adopt rules specifying the procedures for requesting access to records, the costs for copies, and the time limits for responding to requests. The Office of Information Practices (OIP) has established model rules that agencies are expected to follow.

Agencies are also required to affirmatively make certain categories of records available without a specific request, including: rules and policies adopted by the agency; final opinions and orders made in the adjudication of contested cases; government purchasing information; personnel rosters including names, job titles, and salaries; and indices of government records.

SECTION 92F-12 — DISCLOSURE REQUIRED

Specific categories of records that must be disclosed, regardless of any general exemption, include:

(1) Rules and written policies adopted by an agency.
(2) Final opinions and orders in contested case proceedings.
(3) Government purchasing and procurement records, including winning bids, contracts, and purchase orders.
(4) Pardons and commutations.
(5) Land ownership, transfer, and lien records.
(6) Court records generally available to the public.
(7) Information collected and maintained for the purpose of making it available to the general public.
(8) Agency budgets and expenditures.
(9) The names, compensation, job titles, and business contact information of government employees.

SECTION 92F-13 — GOVERNMENT RECORDS: GENERAL EXCEPTIONS TO DISCLOSURE

An agency may withhold a government record or a portion of a record if disclosure would:

(1) Constitute a clearly unwarranted invasion of personal privacy. The UIPA uses a balancing test: the agency must weigh the privacy interest of the individual against the public interest in disclosure. The test requires a "significant privacy interest" that is "clearly unwarranted" — a high bar that strongly favors disclosure.

(2) Frustrate a legitimate government function. This exception covers several subcategories:
  (a) Records that are protected by attorney-client privilege or attorney work product doctrine.
  (b) Government records that, by their nature, must be confidential in order for the government to avoid the frustration of a legitimate government function. The OIP has identified specific categories that fall within this exception, including: records whose premature disclosure would give an unfair advantage to a private interest (such as real estate appraisals for potential government acquisitions); records relating to the investigation of possible violations of law where disclosure would interfere with law enforcement proceedings or reveal confidential techniques; and inter-agency or intra-agency advisory opinions, recommendations, and deliberations where disclosure would impair the quality of agency decision-making.
  (c) Records relating to the security of government buildings, facilities, and information systems.
  (d) Records whose disclosure would impair the state's ability to negotiate contracts or other obligations.

(3) Be protected from disclosure by state or federal statute, rule, or order of court.

The burden of justifying nondisclosure rests on the agency. Exemptions are to be construed narrowly, and the UIPA mandates that agencies must segregate and disclose non-exempt portions of records that contain some exempt information (segregability requirement).

SECTION 92F-14 — SIGNIFICANT PRIVACY INTEREST

This section specifies categories of information in which individuals have a significant privacy interest, including: information relating to medical, psychiatric, or psychological history, diagnosis, condition, treatment, or evaluation; information in an agency's personnel file relating to an individual's performance, disciplinary action, or retirement benefits; financial information about an individual including tax returns, credit reports, and bank account information; information in personal files maintained by the individual as an employee; and social security numbers and similar identifying numbers.

SECTION 92F-15 — RESPONSE TIMELINE

Upon receiving a request for access to a government record, an agency must respond within 10 business days. The response must either: (a) grant access to the record; (b) deny access in whole or in part, with a written explanation of the legal authority for the denial; or (c) acknowledge the request and provide a statement of the time within which the agency will respond. If the agency fails to respond within 10 business days, the request is deemed denied.

For working days, Saturdays, Sundays, and state holidays are excluded.

SECTION 92F-15.5 — FEES

Fees for copies of government records are limited to the actual cost of searching for, reviewing, and segregating the records, plus the actual costs of copying. The OIP has established fee guidelines that set maximum per-page copy fees and specify that search and review fees must reflect the actual salary costs of the personnel performing the work. Agencies may not charge fees calculated to discourage requests.

Inspection of records (viewing without copying) is generally free, though an agency may charge for the actual cost of retrieving records from storage if extensive retrieval is required.

Fees may be waived or reduced when the request is in the public interest, when disclosure is likely to contribute significantly to public understanding of the operations or activities of government, and when the request is not primarily in the commercial interest of the requester.

SECTION 92F-27 — OFFICE OF INFORMATION PRACTICES (OIP)

Hawaii is unique among states in having a dedicated administrative agency — the Office of Information Practices — that serves as the primary body for interpreting, enforcing, and advising on public records and open meetings issues. The OIP, headed by the Director of the Office of Information Practices, has the following responsibilities:

(1) Issuing formal and informal opinions on the applicability of the UIPA and the Sunshine Law (open meetings law).
(2) Providing training and guidance to agencies on compliance.
(3) Mediating and resolving disputes between requesters and agencies.
(4) Reviewing agency denial of access to records and issuing binding opinions on whether disclosure is required.
(5) Maintaining a publicly accessible database of formal opinions.
(6) Recommending legislation to improve transparency.

The OIP's opinions are binding on agencies unless overturned by a court. This administrative enforcement mechanism provides a faster, less expensive alternative to litigation for resolving access disputes.

SECTION 92F-42 — JUDICIAL ENFORCEMENT

Any person aggrieved by an agency's denial of access to records may bring an action in circuit court. The court reviews the matter de novo (anew, without deference to the agency's decision). The court may examine disputed records in camera and may order disclosure.

If the court finds that the agency acted unreasonably in denying access, the court may award reasonable attorney's fees and costs to the prevailing requester. This is discretionary, not mandatory — the court considers whether the agency acted in good faith and with a reasonable basis for its denial.

The court may also award damages if the agency's violation was willful, and may impose civil penalties.

PENALTIES AND ENFORCEMENT

Willful violation of the UIPA by an agency employee may subject the employee to disciplinary action, including suspension or termination. The UIPA does not impose criminal penalties for violations, unlike some other states' public records laws. However, the combination of the OIP's binding administrative opinions, judicial enforcement with attorney's fees, and the potential for disciplinary action provides meaningful enforcement leverage.

The OIP processes hundreds of requests for opinions and guidance annually and publishes its opinions in a searchable online database. The OIP also provides an annual report to the legislature on the status of government transparency in Hawaii, identifying trends, recurring issues, and recommendations for improvement.

RELATIONSHIP TO PRIVACY

The UIPA is notable for its integrated treatment of both access and privacy concerns. Unlike most other states, which have separate public records laws and privacy laws, Hawaii's UIPA addresses both within a single statutory framework. Part II of the UIPA establishes rights of access to government records, while Part III addresses privacy protections for personal records. This integrated approach requires agencies to balance access and privacy in a unified analysis, rather than applying separate and potentially conflicting statutory frameworks.

The privacy provisions of the UIPA give individuals the right to access and correct their own personal records, to be notified of the existence of personal record systems, and to object to the disclosure of personal records to third parties. These provisions are modeled on the federal Privacy Act of 1974 and reflect the "uniform information practices" concept that gives the Act its name.''',
        'summary': 'Hawaii\'s Uniform Information Practices Act (HRS Chapter 92F) creates a unified framework for both public records access and privacy protection, with all government records open by default and agencies required to respond within 10 business days. Hawaii is unique in having the Office of Information Practices (OIP), a dedicated administrative agency that issues binding opinions on records access disputes, providing a faster alternative to litigation.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # IDAHO — Idaho Code §§ 74-101 through 74-126 (Idaho Public Records Act)
    # =========================================================================
    {
        'id': 'id-statute-public-records',
        'citation': 'Idaho Code §§ 74-101 through 74-126',
        'title': 'Idaho Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'ID',
        'source': 'prdb-built',
        'text': '''IDAHO PUBLIC RECORDS ACT
Idaho Code §§ 74-101 through 74-126

SECTION 74-101 — LEGISLATIVE PURPOSE; DECLARATION OF PUBLIC POLICY

The Idaho legislature declares that the people of the State of Idaho have a fundamental right to have access to the records of government in order to hold their government officials accountable, and that providing persons the right to examine public records promotes government transparency and informed citizenry. All public records in Idaho are presumed to be open for inspection, and any exemption from disclosure must be narrowly construed.

SECTION 74-102 — DEFINITIONS

(1) "Public record" includes any writing containing information relating to the conduct or administration of the public's business prepared, owned, used, or retained by any state agency, independent public body corporate and politic, or local agency, regardless of physical form or characteristics. "Writing" includes handwriting, typewriting, printing, photographing, photocopying, transmitting by electronic mail or facsimile, and every other means of recording upon any tangible thing any form of communication or representation, including letters, words, pictures, sounds, or symbols, or combinations thereof, and all papers, maps, magnetic or paper tapes, photographic films and prints, magnetic or punched cards, discs, drums, diskettes, sound recordings, and other documents including existing data compilations from which information may be obtained or translated.

(2) "State agency" means every state board, commission, department, or officer authorized by law to make rules or to determine contested cases, except the legislative and judicial branches.

(3) "Local agency" means a county, city, school district, municipal corporation, district, public health district, political subdivision, or any agency thereof, or any committee of a local agency, or any combination thereof.

(4) "Custodian" means the person or persons having personal custody and control of the public records in question.

SECTION 74-103 — RIGHT OF INSPECTION; FEE SCHEDULE

(1) Every person has a right to examine and take a copy of any public record of this state and there is a presumption that all public records in Idaho are open at all reasonable times for inspection, and this section shall be liberally construed.

(2) The custodian of any public record shall not prevent the examination or copying of any public record by any person, except as otherwise provided by statute. A requester is not required to make a written request, though an agency may ask for a written request for purposes of clarity. A requester is not required to state the purpose of the request or identify themselves as a condition of access.

(3) Fees: Copies of public records may be provided at a fee that does not exceed the actual cost of copying, including labor costs for locating and copying documents. The fee for standard-size photocopies may not exceed $0.10 per page in most circumstances, though certain agencies may have specific fee schedules established by rule. Fees for electronic copies are limited to the actual cost of the electronic medium.

Labor costs for locating documents may be charged, but only if the request requires more than two person-hours of agency labor to fulfill. The first two hours of labor are provided without charge. After the first two hours, the agency may charge a fee based on the hourly wage of the lowest-paid employee capable of fulfilling the request.

(4) If the record is in active use or in storage, the custodian must inform the requester and provide a date and time, no more than three working days later, when the record will be available for inspection.

SECTION 74-104 — RESPONSE TIMELINE

Upon receipt of a request for examination or copying of a public record, the custodian shall either grant or deny the request within three working days. If the request is granted, the records must be made available for inspection or copying within three working days, or a longer period if the records are in storage or otherwise not immediately accessible, but the custodian must explain the reason for the delay and provide an estimated date for production.

If the request is denied in whole or in part, the custodian must provide a written denial specifying the statutory authority for each category of record withheld. The denial must identify the specific provision of Idaho Code that authorizes the withholding and must be signed by the custodian or the custodian's designee.

If the custodian fails to respond within three working days, the request is deemed denied.

SECTION 74-105 — EXEMPTIONS FROM DISCLOSURE

Idaho law provides numerous exemptions, which must be narrowly construed. The exemptions include:

(1) Records exempt by federal or state statute, court order, or rule.

(2) Law enforcement records:
  (a) Investigatory records of a law enforcement agency when disclosure would interfere with enforcement proceedings, deprive a person of a fair trial, constitute an unwarranted invasion of personal privacy, disclose the identity of a confidential source, disclose investigative techniques, or endanger the life or physical safety of any individual.
  (b) Information regarding the location of combative or fugitive persons, tactical plans, undercover operations, and similar matters where disclosure would compromise safety.

(3) Personnel records, personal information, and employment records of public employees, including evaluations, disciplinary records, letters of reprimand, and similar records, except that an employee's name, job title, compensation, employment dates, and job description are public.

(4) Records of investigations by the attorney general, when disclosure would jeopardize an ongoing investigation.

(5) Preliminary drafts, notes, and memoranda that are not retained by the agency in the ordinary course of business and that are not final policy documents.

(6) Records related to the negotiation of pending contracts or agreements, where disclosure would impair the agency's bargaining position.

(7) Trade secrets and proprietary information submitted to an agency, where the person submitting the information has requested confidentiality and the agency has agreed to treat the information as confidential.

(8) Computer programs and software developed by or for an agency, where the agency holds exclusive rights to the software.

(9) Records containing personal information about students, patients, or clients of public institutions, where disclosure would constitute an unwarranted invasion of personal privacy.

(10) Archaeological site location information, when disclosure would jeopardize the site.

(11) Records of the Idaho State Tax Commission relating to individual taxpayer returns and proprietary tax information.

(12) Records of the Department of Correction regarding security procedures, escape contingency plans, and similar operational records.

(13) Communications between a public agency and its attorney that are privileged under the attorney-client privilege.

(14) Records submitted to an agency in response to a competitive solicitation (sealed bids) prior to the time set for opening.

(15) Social security numbers, financial account numbers, and similar personal identifiers held by an agency.

SECTION 74-113 — DENIAL OF REQUEST; APPEAL; COURT ACTION

If a request for records is denied, the requester may appeal to the head of the agency. The agency head must respond within 10 working days. If the denial is upheld, the requester may file a petition for judicial review in district court.

The court reviews the denial de novo (without deference to the agency's decision) and may examine the disputed records in camera. The burden of sustaining the denial rests on the agency — the agency must demonstrate that the records fall within a specific exemption.

If the court finds that the records were improperly withheld, the court shall order disclosure and may award reasonable attorney's fees and costs to the prevailing requester. The award of attorney's fees is mandatory if the court finds the denial was without a reasonable basis in law or fact. If the denial was in bad faith or was frivolous, the court may also award costs and reasonable attorney's fees to the requester regardless of the outcome on the merits of the exemption claim.

SECTION 74-117 — VIOLATIONS AND PENALTIES

Any public official who intentionally violates the provisions of the Idaho Public Records Act may be subject to removal from office or other disciplinary action. The statute does not impose criminal penalties directly, but intentional destruction of records to avoid disclosure may constitute obstruction of justice or other criminal conduct under separate provisions of Idaho law.

An agency that is found to have improperly withheld records may also be ordered to pay the requester's costs and attorney's fees, as described above.

SECTION 74-118 — SEVERABILITY; LIBERAL CONSTRUCTION

The Idaho Public Records Act is to be liberally construed to effectuate its purpose of promoting public access to government records. If any provision of the Act is found to be unconstitutional or invalid, the remaining provisions shall remain in full force and effect.

SECTION 74-119 — ELECTRONIC RECORDS

Public records maintained in electronic format are subject to the same disclosure requirements as paper records. An agency may not deny access to a public record solely because it exists in electronic form, and an agency must provide electronic records in the format in which they are maintained if the requester so requests, unless doing so would jeopardize the security of the information or the integrity of the agency's information system.

Agencies are not required to create new records, compile data, or produce records in a format in which they are not maintained, though agencies are encouraged to accommodate reasonable requests for records in particular formats.

SECTION 74-120 through 74-126 — ADDITIONAL PROVISIONS

These sections address various administrative and procedural matters, including: requirements for agencies to designate a custodian of records and post contact information for records requests; requirements for agencies to adopt records retention schedules; provisions for the recovery of costs associated with responding to requests that are "solely intended to burden the agency" (a narrow provision that has been rarely invoked and is subject to judicial oversight); and provisions for coordination between state and local agencies when records are shared across jurisdictions.

SCOPE OF APPLICATION

The Idaho Public Records Act applies to all state agencies, local agencies, school districts, public health districts, and any other governmental entity or political subdivision. Private entities performing governmental functions under contract or agreement with a public agency are subject to the Act to the extent of their governmental function. The Act does not apply to the legislature or the judiciary, which have separate rules governing access to their records. However, financial records of the legislature and judiciary are generally treated as public records accessible under separate provisions of Idaho law.''',
        'summary': 'The Idaho Public Records Act (Idaho Code §§ 74-101 through 74-126) presumes all public records are open for inspection and requires agencies to respond within three working days, with the first two hours of labor for record retrieval provided at no charge. Denials must cite specific statutory authority and are subject to de novo judicial review, with mandatory attorney\'s fees when a denial lacked a reasonable basis in law or fact.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # ILLINOIS — 5 ILCS 140/1 through 140/11.5 (Illinois FOIA)
    # =========================================================================
    {
        'id': 'il-statute-public-records',
        'citation': '5 ILCS 140/1 through 140/11.5',
        'title': 'Illinois Freedom of Information Act (FOIA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'IL',
        'source': 'prdb-built',
        'text': '''ILLINOIS FREEDOM OF INFORMATION ACT (FOIA)
5 ILCS 140/1 through 140/11.5

SECTION 1 — LEGISLATIVE POLICY

The Illinois General Assembly declares that all persons are entitled to full and complete information regarding the affairs of government and the official acts and policies of those who represent them as public officials and public employees, consistent with the terms of the Freedom of Information Act. Pursuant to the fundamental philosophy of the American constitutional form of government, it is declared to be the public policy of the State of Illinois that access to government information is a fundamental right of citizenship.

The General Assembly further declares that it is the obligation of government to provide access to public records as expediently and efficiently as possible and in compliance with this Act. Restraints on access to information, to the extent permitted by this Act, are limited exceptions to the principle that the people of the State of Illinois have a right to full disclosure of information relating to the decisions, policies, procedures, rules, standards, and other aspects of government activity that affect the conduct of government and the lives of the people.

SECTION 2 — DEFINITIONS

"Public body" means all legislative, executive, administrative, or advisory bodies of the State, state universities and colleges, counties, townships, cities, villages, incorporated towns, school districts, and all other municipal corporations, boards, bureaus, committees, or commissions of this State, any subsidiary bodies of any of the foregoing, and a not-for-profit or for-profit corporation or organization that was established to perform a governmental function and that is funded by public funds or tax revenue.

"Public records" means all records, reports, forms, writings, letters, memoranda, books, papers, maps, photographs, microfilms, cards, tapes, recordings, electronic data processing records, electronic communications, recorded information and all other documentary materials pertaining to the transaction of public business, regardless of physical form or characteristics, having been prepared by or for, or having been or being used by, received by, in the possession of, or under the control of any public body.

"Head of the public body" means the president, chairman, or person with primary authority over the public body.

"Recurrent requester" means a person who, in the 12 months immediately preceding the request, has submitted to the same public body a combined total of 50 or more requests for records, 15 or more requests for records within a 30-day period, or 7 or more requests for records within a 7-day period. This definition, added by amendment, allows agencies additional time to respond to high-volume requesters.

"Commercial purpose" means the use of any part of a public record or records, or information derived from public records, in any form for sale, resale, or solicitation or advertisement for sales or services. This definition is relevant to the Act's provisions allowing agencies to inquire about purpose in limited circumstances.

SECTION 3 — RIGHT OF ACCESS; PROCEDURES

(a) Each public body shall make available to any person for inspection or copying all public records, except as otherwise provided in Section 7.

(b) A request for records must be submitted in writing (which includes email and other electronic formats). The request must be directed to the public body's FOIA officer.

(c) A requester is not required to specify the purpose of the request, except that a public body may ask whether the request is for a "commercial purpose." If the request is for a commercial purpose, the requester must so state, and the public body may require a certification to that effect. Failure to identify a request as being for a commercial purpose, when it is, is a violation of the Act.

(d) Each public body is required to designate one or more FOIA officers to receive and respond to requests. The FOIA officer must complete an annual training program conducted by the Public Access Counselor within the Attorney General's office.

SECTION 3.5 — ELECTRONIC RECORDS

When a public body maintains records in electronic format, the public body must provide the records in electronic format when requested, unless the public body can demonstrate that the format requested is not the format in which the records are maintained and conversion would be unreasonably burdensome. If a requester requests records in a format that the public body does not maintain, the public body must provide them in the format in which they are maintained, unless conversion is requested and is not unreasonably burdensome.

SECTION 4 — RESPONSE TIMELINE

A public body must respond to a request within five business days after receipt. The public body may extend the response period by an additional five business days (for a total of 10 business days) if:
  (1) The requested records are stored in whole or in part at other locations.
  (2) The request requires the collection of a substantial number of specified records.
  (3) The request is couched in categorical terms and requires an extensive search.
  (4) The requested records require examination, categorization, or redaction.
  (5) The request raises undecided legal issues.
  (6) The public body must consult with another public body that has a substantial interest in the subject matter.
  (7) The request requires the public body to compile data, write programming language, or construct a computer program.

For requests by "recurrent requesters," the response period is 21 business days.

If the public body fails to respond within the statutory time period, the request is deemed denied, and the requester may file an action in court or a complaint with the Public Access Counselor.

SECTION 6 — FEES

(a) No fee may be charged for the first 50 pages of black and white, letter- or legal-size copies. After the first 50 pages, fees may not exceed $0.15 per page.

(b) No fee may be charged for inspection of records (viewing without copying).

(c) For electronic records, fees are limited to the actual cost of the medium (disc, flash drive, etc.). If the records are provided by email, no fee may be charged.

(d) Fees for color copies, oversized copies, or other special formats must be based on the actual cost.

(e) A fee waiver or reduction is required when the request is in the public interest — that is, when the principal purpose of the request is to access and disseminate information regarding the health, safety, and welfare or the legal rights of the general public, and the request is not for the principal purpose of personal or commercial benefit.

(f) No public body may condition access to records on prepayment of fees that exceed $25.00 unless the requester has previously failed to pay fees.

SECTION 7 — EXEMPTIONS

Illinois FOIA provides numerous exemptions, organized by category. Key exemptions include:

(1) Information specifically prohibited from disclosure by federal or State law.

(1.5) Private information, defined as unique identifiers including social security numbers, driver's license numbers, employee identification numbers, biometric identifiers, personal financial information, passwords, medical records, home and personal telephone numbers, and email addresses.

(2) Records relating to pending or actually and reasonably contemplated litigation, including attorney-client communications and attorney work product.

(3) Preliminary policy recommendations and deliberative materials (the deliberative process exemption). This exemption protects only predecisional, deliberative communications — it does not protect factual information or final policy decisions.

(4) Trade secrets and commercial or financial information obtained from outside sources where disclosure would result in competitive harm.

(5) Information that would disclose unique or specialized investigative techniques used by law enforcement, other than the use of combative or defensive techniques, and when disclosure would create a risk of circumvention of the law.

(6) Records that would endanger the life or physical safety of any person.

(7) Test questions, scoring keys, and other examination data used to administer licensing examinations.

(8) Architects' and engineers' plans for buildings not yet constructed, security measures, vulnerability assessments, and emergency response protocols.

(9) Records of law enforcement agencies relating to active or pending investigations, but only to the extent that disclosure would interfere with pending or actually and reasonably contemplated enforcement proceedings, deprive a person of a right to a fair trial, disclose the identity of a confidential source, disclose techniques and procedures for law enforcement investigations if disclosure would create a risk of circumvention of the law, or endanger the life or physical safety of any person.

(10) Information submitted to an agency in confidence, where the agency has obligated itself in writing not to disclose the information.

(11) Minutes of closed meetings of public bodies, until the public body determines that the minutes no longer need to be kept confidential.

(12) Communications between an elected official and constituents, except when the communication relates to the transaction of public business.

The Act requires agencies to redact exempt information and disclose the non-exempt portions of records (segregability requirement).

SECTION 9 — DENIAL OF REQUEST; NOTICE

When a public body denies a request, it must provide a written denial that includes: the specific legal reasons for the denial, including a citation to the specific FOIA exemption; the names and titles of the persons responsible for the denial; and a statement advising the requester of the right to seek review by the Public Access Counselor or to file a lawsuit.

SECTION 9.5 — PUBLIC ACCESS COUNSELOR (PAC)

The Attorney General's office maintains a Public Access Counselor (PAC) who serves as an administrative enforcement mechanism for FOIA (and the Open Meetings Act). Functions of the PAC include:

(1) Receiving and reviewing complaints from requesters whose requests have been denied.
(2) Issuing binding opinions on whether records were properly withheld.
(3) Mediating disputes between requesters and public bodies.
(4) Conducting FOIA training for public body FOIA officers.
(5) Issuing advisory opinions on the applicability of FOIA exemptions.

A requester may file a "Request for Review" with the PAC within 60 days of a denial. The PAC reviews the denial and, after investigation, may issue a binding opinion ordering the public body to produce the records. The public body may seek judicial review of a binding opinion.

The PAC process provides a free, relatively expedient alternative to filing a lawsuit. The Attorney General's office processes thousands of requests for review each year.

SECTION 11 — ENFORCEMENT; CIVIL PENALTIES; ATTORNEY'S FEES

(a) A requester may file a lawsuit in circuit court if a request is denied. The court reviews the denial de novo and may examine records in camera.

(b) The burden of proof is on the public body to demonstrate that the records are exempt from disclosure.

(c) If the court finds that the public body's denial was not in good faith and lacked any reasonable basis in law, the court shall award the requester reasonable attorney's fees and costs.

(d) If the court finds that a public body intentionally and willfully violated the Act, the court may impose a civil penalty of not less than $2,500 and not more than $5,000 for each violation.

(e) If the court determines that a public body willfully and intentionally failed to comply with the Act, or that the public body's actions constituted a pattern or practice of violating the Act, the court shall order the public body to pay a civil penalty of $5,000 for each willful and intentional violation.

(f) If the court determines that a FOIA officer has acted in bad faith, the court may order that the FOIA officer complete a supplemental training program.

SECTION 11.5 — PROTECTION FROM RETALIATION

No public body shall take retaliatory action against any employee who discloses information that the employee reasonably believes evidences a violation of any law, rule, or regulation, or who assists a person in seeking access to public records. This anti-retaliation provision protects whistleblowers and employees who cooperate with records requests.

ADDITIONAL PROVISIONS — PROACTIVE DISCLOSURE

The Act requires public bodies to prominently display on their websites (if they maintain a website) certain categories of records, including: a description of the public body and its operations; the address, telephone number, and email address of its FOIA officer; a brief description of the procedures for requesting records; and a directory of employees including titles, salaries, and email addresses. This proactive disclosure requirement, added by the 2010 amendments, reduces the need for individual records requests for commonly sought information.

SCOPE AND APPLICATION

Illinois FOIA applies broadly to all public bodies, including state agencies, counties, cities, villages, townships, school districts, park districts, fire protection districts, library districts, public universities, community colleges, and any other unit of local government. Private entities performing governmental functions under contract may also be subject to the Act in certain circumstances, though this remains an area of developing case law.

The Act does not apply to the General Assembly (which has its own disclosure rules) or to the judiciary (governed by court rules). However, administrative bodies within the judicial branch, such as the Administrative Office of the Illinois Courts, are subject to FOIA.''',
        'summary': 'The Illinois Freedom of Information Act (5 ILCS 140) establishes that all public records are presumed open, requires agencies to respond within five business days (extendable to ten), and provides the first 50 pages of copies free of charge. Illinois has a robust administrative enforcement mechanism through the Attorney General\'s Public Access Counselor, who can issue binding opinions ordering disclosure, supplemented by judicial review with mandatory attorney\'s fees and civil penalties up to $5,000 per willful violation.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # INDIANA — Ind. Code §§ 5-14-3-1 through 5-14-3-10 (APRA)
    # =========================================================================
    {
        'id': 'in-statute-public-records',
        'citation': 'Ind. Code §§ 5-14-3-1 through 5-14-3-10',
        'title': 'Indiana Access to Public Records Act (APRA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'IN',
        'source': 'prdb-built',
        'text': '''INDIANA ACCESS TO PUBLIC RECORDS ACT (APRA)
Ind. Code §§ 5-14-3-1 through 5-14-3-10

SECTION 5-14-3-1 — POLICY AND PURPOSE

The Indiana General Assembly declares that a fundamental philosophy of the American constitutional form of representative government is that government is the servant of the people and not their master. Accordingly, it is the public policy of the state that all persons are entitled to full and complete information regarding the affairs of government and the official acts of those who represent them as public officials and employees. The Access to Public Records Act (APRA) is intended to provide the means by which the people may obtain information relating to governmental affairs.

The APRA works in conjunction with Indiana's Open Door Law (Ind. Code § 5-14-1.5), which governs open meetings. Together, these statutes form the framework for open government in Indiana.

SECTION 5-14-3-2 — DEFINITIONS

"Public agency" means any entity that is subject to the budget and financial reporting requirements of Indiana Code, including: the state and its agencies; any county, city, town, township, or school corporation; any board, commission, department, division, bureau, committee, office, instrumentality, or authority of any level of government; and any other entity, or any office thereof, by whatever name designated, exercising in a limited geographical area the executive, administrative, judicial, or legislative power of the state or a delegated local governmental power.

"Public record" means any writing, paper, report, study, map, photograph, book, card, tape recording, or other material that is created, received, retained, maintained, or filed by or with a public agency and which is generated on paper, paper substitutes, photographic media, chemically based media, magnetic or machine-readable media, electronically stored data, or any other material, regardless of form or characteristics.

"Person" means any individual, corporation, limited liability company, partnership, unincorporated association, or other entity.

SECTION 5-14-3-3 — RIGHT OF INSPECTION AND COPYING

(a) Any person may inspect and copy the public records of any public agency during the regular business hours of the agency, except as provided in section 4 (exemptions).

(b) A request for inspection or copying may be made orally or in writing. A public agency may not require that a request be in writing, though an agency may ask for a written request when the request involves a large volume of records or when a written request would assist the agency in identifying the records sought.

(c) A requester is not required to state the purpose of the request, and a public agency may not deny access based on the requester's purpose or intended use of the records. However, a public agency may ask whether the request is for a commercial purpose.

(d) Response Timeline: A public agency must respond to a request within a reasonable time. The statute does not prescribe a specific number of days, but the Indiana Public Access Counselor has interpreted "reasonable time" to mean that agencies should provide an initial response as promptly as possible, typically within one to three business days for straightforward requests. For requests involving a large volume of records, complex redactions, or records in storage, a longer response time may be reasonable, but the agency must communicate the timeline to the requester.

If a public agency denies a request, in whole or in part, the agency must provide a written denial, stating the statutory authority for the denial, within a reasonable time. The denial must cite the specific provision of the APRA or other statute that authorizes the withholding.

(e) Copying and Inspection:
A public agency must allow inspection of records at the agency's offices during regular business hours. The agency may not charge a fee for inspection (viewing without copying).

For copies, the agency may charge a fee based on the actual cost of copying. The fee may not exceed the greater of: (1) $0.10 per page for copies that are not color copies and are not larger than 11 by 17 inches; or (2) the actual cost of copying if the request involves specialized reproduction services (oversized copies, color copies, etc.).

For electronic records, the agency may charge for the actual cost of the electronic medium and, if the request requires the agency to create a program, write code, or compile data, the agency may charge for the actual cost of programming time at the hourly rate of the programmer.

SECTION 5-14-3-4 — EXEMPTIONS AND EXCEPTIONS

Indiana's APRA contains two categories of non-disclosable information: records that are "confidential" (which the agency must not disclose) and records that are "excepted from disclosure at the discretion of the agency" (which the agency may, but is not required to, withhold). This two-tier system is an important distinction.

(a) Confidential records (mandatory nondisclosure):

(1) Records declared confidential by state or federal statute.
(2) Records containing the identity of a donor of a gift made to a public agency if the donor requires nondisclosure as a condition of the gift.
(3) Patient medical records.
(4) Records of a grand jury.
(5) School records of individual students as required by the Family Educational Rights and Privacy Act (FERPA).
(6) Records containing Social Security numbers (confidential to the extent of the SSN itself).
(7) Personal information concerning research subjects in research conducted by state educational institutions.
(8) The identity of a child less than 18 years of age who is a victim of a sex offense.
(9) Records containing financial information of persons that are filed with or maintained by an agency, including tax returns.

(b) Records excepted from disclosure at the agency's discretion:

(1) Records of investigations by law enforcement agencies prior to the completion of the investigation.
(2) Work product of an attorney who is providing legal counsel to a public agency.
(3) Records that are intra-agency or interagency advisory, deliberative, or consultative in nature and are preliminary to a final agency action.
(4) Records containing trade secrets.
(5) Drafts, notes, or preliminary documents prepared by agency staff for their personal use, provided they are not retained as part of the agency's records.
(6) Records relating to negotiations between a public agency and a prospective employee regarding compensation.
(7) Test questions, scoring keys, and similar examination materials.
(8) Diaries, journals, or other personal notes serving as a memory aid.
(9) Records relating to negotiation of leases, purchases, or sales of real property.
(10) Records relating to the security of a jail, juvenile detention facility, or other correctional institution.
(11) Records containing the personal contact information of employees, including home addresses and phone numbers.
(12) Personnel file information regarding individual employees, except that names, compensation, job titles, education and training backgrounds, previous work experience, and dates of employment are always public.
(13) Records relating to pending litigation to which the agency is a party.
(14) Communications from a citizen to an elected official.

The Act requires agencies to redact exempt information and provide the non-exempt portions of records (segregability requirement). An agency may not deny an entire record based on the presence of some exempt information within it.

SECTION 5-14-3-5 — PUBLIC ACCESS COUNSELOR

Indiana has established a Public Access Counselor (PAC) within the Office of the Inspector General who serves as the primary administrative enforcement mechanism for the APRA and the Open Door Law. The PAC's responsibilities include:

(1) Receiving and responding to complaints from persons who believe their rights under the APRA have been violated.
(2) Issuing advisory opinions interpreting the APRA and the Open Door Law.
(3) Providing education and training to public agencies and the public.
(4) Mediating disputes between requesters and agencies.

A person denied access to records may file a complaint with the PAC. The PAC must respond with a formal opinion within 30 days. The PAC's opinions are advisory — not binding on the agency — but they carry significant persuasive weight and are frequently cited by Indiana courts.

SECTION 5-14-3-9 — JUDICIAL REVIEW; ENFORCEMENT

(a) A person who has been denied access to public records may bring an action in the circuit or superior court of the county where the denial occurred, or in Marion County (the state capital).

(b) The court shall determine the matter de novo and may inspect the disputed records in camera.

(c) The burden of proof is on the public agency to demonstrate that the records are exempt from disclosure.

(d) If the court finds that the agency improperly denied access, the court shall order the agency to disclose the records and may award reasonable attorney's fees, court costs, and other reasonable expenses of litigation to the prevailing requester.

(e) The court may also impose a civil penalty of $100 per day for each day the agency fails to comply with a court order requiring disclosure, up to a maximum of $5,000.

(f) If the court finds that the denial was willful or in bad faith, the court may order the agency to pay the requester's attorney's fees and costs regardless of the amount in controversy.

SECTION 5-14-3-10 — PENALTIES FOR VIOLATIONS

(a) A public employee who knowingly or intentionally violates the APRA commits a Class A infraction (civil penalty up to $10,000).

(b) A public official who knowingly or intentionally alters, defaces, or destroys a public record, or removes a public record from the office where it is maintained with the intent to prevent its disclosure, commits a Level 6 felony (imprisonment of 6 months to 2.5 years, and a fine of up to $10,000).

(c) An agency that fails to respond to a request within a reasonable time, or that engages in a pattern of violations, may be subject to injunctive relief, civil penalties, and fee-shifting.

ADDITIONAL PROVISIONS

Indiana law requires each public agency to designate a person responsible for records management and FOIA compliance. Agencies must post their policies and procedures for requesting records, including contact information for the records custodian.

The APRA also includes provisions addressing the retention and destruction of public records. Agencies must maintain records in accordance with retention schedules approved by the Indiana Commission on Public Records. Destruction of records outside of an approved retention schedule, particularly when done to avoid disclosure, is prohibited and may constitute a criminal offense.

SCOPE AND APPLICATION

The APRA applies to all public agencies at the state and local level, including state agencies, counties, cities, towns, townships, school corporations, library districts, and special districts. The Act extends to private entities only to the extent that they are performing a public function on behalf of a public agency, and courts have generally required a substantial connection between the private entity's activities and a governmental function before subjecting the entity to the APRA.

The General Assembly and the judiciary have their own rules governing access to their records, though records of the legislative services agency and administrative offices of the courts are generally subject to the APRA.''',
        'summary': 'Indiana\'s Access to Public Records Act (Ind. Code §§ 5-14-3) provides a two-tier exemption system distinguishing between "confidential" records that must be withheld and "discretionary" records that agencies may choose to release, with copies capped at $0.10 per page. Enforcement includes the Public Access Counselor for advisory opinions, de novo judicial review with fee-shifting, civil penalties up to $100/day for noncompliance, and Level 6 felony charges for destroying records to prevent disclosure.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # IOWA — Iowa Code Ch. 22 (Iowa Open Records Act)
    # =========================================================================
    {
        'id': 'ia-statute-public-records',
        'citation': 'Iowa Code Ch. 22',
        'title': 'Iowa Open Records Act (Examination of Public Records)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'IA',
        'source': 'prdb-built',
        'text': '''IOWA OPEN RECORDS ACT
Iowa Code Chapter 22 — Examination of Public Records

SECTION 22.1 — DEFINITIONS

"Public records" includes all records, documents, tape, or other information, stored or preserved in any medium, of or belonging to this state or any county, city, township, school corporation, political subdivision, nonprofit corporation other than combatant or combatant command whose members are combatant commanders or combatant command representatives, or tax-supported district in this state, or any branch, department, board, bureau, commission, council, or committee of any of the foregoing. "Public records" also includes all records relating to the investment of public funds, including but not limited to the nature and amount of investments, the identities of the parties to investment transactions, the terms of such transactions, and the source and amount of public funds involved.

"Government body" means this state, or any county, city, township, school corporation, political subdivision, tax-supported district, or nonprofit corporation other than combatant or combatant command, or any branch, department, board, bureau, commission, council, or committee of any of the foregoing, or any employee, officer, or agency of any of the foregoing.

"Lawful custodian" means the government body that has physical custody and control of the public record or its designee. The lawful custodian is responsible for ensuring compliance with Chapter 22.

SECTION 22.2 — RIGHT OF EXAMINATION

(1) Every person shall have the right to examine and copy a public record and to publish or otherwise disseminate a public record or the information contained in a public record. The right to examine and copy extends to all persons regardless of their reason for wanting the records. Iowa courts have consistently held that a requester's purpose is irrelevant to the right of access.

(2) The examination and copying of public records shall be done under the supervision of the lawful custodian of the records or the custodian's authorized designee. The custodian shall not unreasonably delay or refuse the examination of records.

(3) A government body shall not prevent the examination of records or the copying of records by requiring a requester to give a reason for the examination.

(4) All costs of examination and copying shall be paid by the person desiring to examine or copy. Fees are addressed separately in Section 22.3.

SECTION 22.3 — FEES

(1) A reasonable fee may be charged for the copying of public records. The fee shall not exceed the actual cost of providing the copy, including the cost of labor involved in retrieving and copying the record. The Iowa Public Information Board (IPIB) has issued guidance indicating that fees for standard-size photocopies should generally not exceed $0.25 per page.

(2) Supervisory costs may be charged if a requester's examination of records requires direct supervision beyond what the custodian would normally provide. However, the custodian may not impose supervisory fees calculated to discourage requests.

(3) If the request involves extensive search or retrieval, the custodian may charge for the actual costs of search and retrieval based on the hourly wage of the employee performing the search.

(4) Advance deposits may be required for requests where the estimated total cost exceeds $100.

(5) Inspection (viewing without copying) is generally free, subject to any reasonable supervisory fees described above.

SECTION 22.4 — RESPONSE TIMELINE

Iowa Code does not prescribe a specific statutory deadline (in terms of a fixed number of days) for responding to a records request. However, the statute provides that the lawful custodian must provide access "promptly" and must not "unreasonably delay or refuse" examination and copying. The Iowa Public Information Board and Iowa courts have interpreted this requirement to mean that agencies should respond within a few business days for straightforward requests, and within a reasonable time for more complex requests, with communication to the requester about the expected timeline.

If a request is denied, the custodian must provide a written statement setting forth the specific legal basis for the denial, including a citation to the specific statutory provision authorizing the withholding. The denial must also inform the requester of the right to seek review.

A good-faith, reasonable delay in producing records is not a violation, but an unexplained or protracted delay may constitute an unreasonable refusal subject to enforcement action.

SECTION 22.7 — CONFIDENTIAL RECORDS

Iowa Code § 22.7 lists specific categories of public records that are confidential and shall not be open to examination. These confidential records include:

(1) Personal information in confidential personnel records of government bodies relating to identified or identifiable individuals who are applicants for employment, current or former employees, or dependents or beneficiaries of such employees, except that the following are always public: the name, compensation, job title, education and training background, and dates of employment of every employee.

(2) Tax records made available to a government body that are specifically identified as confidential by a state or federal statute.

(3) Minutes and tape recordings of closed sessions of government bodies, until the body determines the minutes should be made available to the public.

(4) Records of identity of persons providing information to a government body when the information is provided in confidence and the identity of the provider is held in confidence by the body.

(5) Hospital records, medical records, and professional counselor records of the condition, diagnosis, care, or treatment of a patient or former patient, including outpatient.

(6) Trade secrets which are recognized and protected as such by law.

(7) Records of communications between a government body and its attorney that are privileged under the attorney-client privilege.

(8) The social security number of an individual in any record maintained by a government body.

(9) Criminal case records held by a court, to the extent that release is restricted by court order.

(10) Personal information in records of students, except as provided by FERPA.

(11) Records relating to the security of government buildings, including vulnerability assessments, emergency protocols, and security measures.

(12) Records of investigations conducted by a government body, to the extent that disclosure would jeopardize an ongoing investigation or would deprive a person of a right to a fair trial.

(13) Peace officers' investigative reports, except as otherwise provided by law.

(14) Information about the location of combative or fugitive persons.

(15) Records which represent and constitute the work product of an attorney, which are related to litigation or claim made by or against a government body.

Additional categories of confidential records are scattered throughout the Iowa Code in various subject-matter statutes. Section 22.7 is the primary but not the exclusive list of confidentiality provisions.

SECTION 22.8 — INJUNCTION TO RESTRAIN EXAMINATION; DEFENSE

(1) A government body which in good faith believes that a public record is confidential under a provision of law may seek an injunction to restrain examination of the record. The government body must petition the district court, and the court may examine the record in camera.

(2) The government body bears the burden of proving that the record is confidential or exempt from disclosure. If the court determines that the record is not exempt, it shall order disclosure.

SECTION 22.10 — ENFORCEMENT; PENALTIES

(1) A person who is denied access to public records may seek judicial enforcement through an action in district court for injunctive relief, mandamus, or declaratory judgment.

(2) If the court finds that a lawful custodian's refusal to permit examination was in violation of Chapter 22, the court shall assess the costs of the action, including reasonable attorney's fees, against the body that refused to permit the examination.

(3) A person who knowingly violates Chapter 22 or who knowingly fails to comply with a court order under the chapter is guilty of a serious misdemeanor.

(4) Damages: If the court finds that the custodian's refusal was willful and knowing, the court may award damages for the loss sustained by the person, including but not limited to the costs and attorney's fees of the action.

(5) Removal from Office: A person who has the custody of a public record and who knowingly and willfully refuses to give access as authorized by law may be subject to removal from office.

IOWA PUBLIC INFORMATION BOARD (IPIB)

Iowa established the Iowa Public Information Board (IPIB) in 2012 as an independent administrative agency responsible for overseeing compliance with the Open Records Act (Chapter 22) and the Open Meetings Act (Chapter 21). The IPIB's powers and duties include:

(1) Receiving and investigating complaints regarding violations of Chapter 22.
(2) Issuing advisory opinions interpreting the open records and open meetings laws.
(3) Issuing declaratory orders resolving specific disputes.
(4) Providing education and training to government bodies and the public.
(5) Recommending legislation to improve government transparency.
(6) Publishing an annual report on the state of open government in Iowa.

The IPIB's opinions are advisory but carry significant weight. The IPIB may also refer matters to the county attorney or the Attorney General for enforcement when it determines that a violation has occurred and the responsible party has failed to take corrective action.

The creation of the IPIB was a significant development in Iowa open government law, providing a centralized, expert body for the resolution of records access disputes without the cost and delay of litigation.

SECTION 22.11 — PERSONNEL INFORMATION; PUBLIC NATURE

Notwithstanding the confidentiality provisions of Section 22.7, certain personnel information is always public. The following information regarding a government employee must be made available upon request: name, compensation (salary and benefits), job title, education and training background, previous work experience, dates of first and last employment, the fact of resignation, discharge, or retirement, and the reasons for such resignation, discharge, or retirement, subject to certain privacy limitations for health-related reasons.

SECTION 22.13 — ELECTRONIC RECORDS

Public records maintained in electronic form are subject to the same access requirements as paper records. A government body may not deny access to a public record solely because it exists in electronic format, and must produce records in the format in which they are maintained if the requester so requests. Agencies are not required to create records that do not exist, compile data into new formats, or build databases in response to a request, but existing electronic records must be made available in their existing electronic format.

SCOPE AND APPLICATION

Chapter 22 applies to all government bodies in Iowa, including state agencies, counties, cities, townships, school corporations, and other political subdivisions. The Act extends to nonprofit corporations and other entities that receive public funds or perform governmental functions, though the scope of this extension has been subject to ongoing judicial interpretation.

The Iowa legislature and the judiciary are subject to Chapter 22, though each has adopted implementing rules and procedures specific to their operations. Records of the legislature and the courts are generally accessible under the same principles, though certain categories of judicial records (e.g., sealed court files, juvenile records) are governed by specific statutes and court rules.''',
        'summary': 'Iowa\'s Open Records Act (Iowa Code Chapter 22) establishes a broad right to examine and copy public records without requiring a statement of purpose, with fees limited to actual costs and no fixed statutory response deadline beyond the requirement to respond "promptly" without unreasonable delay. The Iowa Public Information Board (IPIB), established in 2012, provides administrative oversight including complaint investigation, advisory opinions, and referrals for enforcement, supplemented by judicial remedies including mandatory attorney\'s fees and criminal penalties for knowing violations.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # KANSAS — K.S.A. §§ 45-215 through 45-223 (Kansas Open Records Act - KORA)
    # =========================================================================
    {
        'id': 'ks-statute-public-records',
        'citation': 'K.S.A. §§ 45-215 through 45-223',
        'title': 'Kansas Open Records Act (KORA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'KS',
        'source': 'prdb-built',
        'text': '''KANSAS OPEN RECORDS ACT (KORA)
K.S.A. §§ 45-215 through 45-223

SECTION 45-215 — SHORT TITLE; LEGISLATIVE DECLARATION

This act shall be known and may be cited as the Kansas Open Records Act (KORA). The Kansas legislature recognizes that public records are the property of the people and that it is the intent of the legislature that public records be open for inspection by any person unless otherwise provided by the Act, and the Act shall be liberally construed and applied to promote such access.

SECTION 45-216 — DEFINITIONS

(a) "Public agency" means the state or any political or taxing subdivision of the state or any office, officer, or agency thereof, or any other entity receiving or expending and supported in whole or in part by public funds appropriated by the state or by a political or taxing subdivision of the state. This definition encompasses state agencies, counties, cities, school districts, townships, special districts, and any entity supported by public funds.

(b) "Public record" means any recorded information, regardless of form or characteristics, which is made, maintained, or kept by or is in the possession of any public agency, or which is described in the record retention and disposition schedules applicable to the public agency.

(c) "Custodian" means the official custodian or any person designated by the official custodian to carry out the duties of the custodian under the Act.

(d) "Official custodian" means any officer or employee of a public agency who is responsible for the maintenance of public records, regardless of whether such records are in the officer's or employee's actual personal custody and control. Each public agency shall designate one or more official custodians.

SECTION 45-217 — PUBLIC RECORDS; RIGHT OF ACCESS

Each public agency shall designate an official custodian or custodians who shall be responsible for compliance with the Kansas Open Records Act. Each official custodian shall:

(1) Post in a conspicuous place at the principal office of the public agency, and on the agency's website if one exists, the name, official title, business address, and business telephone number of the official custodian.

(2) Furnish, upon request, the information posted pursuant to paragraph (1) and other general information regarding the rights of requesters under the Act and the procedures for obtaining access to public records maintained by the agency.

(3) Adopt procedures for requesting access to, and obtaining copies of, public records that are consistent with the Act and that facilitate the expeditious provision of public records to requesters.

SECTION 45-218 — PUBLIC RECORDS; RIGHT OF INSPECTION; PROCEDURES

(a) All public records shall be open for inspection by any person, and the public agency shall not be required to justify its decision to release the record. The right of access belongs to any person without regard to the person's purpose for requesting the record or the person's identity.

(b) A request for access to a public record may be made orally or in writing. A public agency may request that a request be made in writing for purposes of clarity or to assist in identifying the records sought, but may not require a written request as a condition of access.

(c) Response Timeline: Each public agency shall respond to a request for access to public records not later than the end of the third business day following the date the request is received. The response must either provide access to the requested records or provide a written statement of the grounds for denial, including a citation to the specific provision of the Act or other statute that authorizes the withholding.

If the public agency determines that additional time is needed because the records are in storage or otherwise not immediately accessible, the agency must communicate this to the requester and provide an expected date of production. There is no statutory extension period beyond the initial three business days for the initial response, though agencies are given reasonable additional time for the actual production of voluminous records if they communicate the timeline.

(d) If a request is denied, the denial must be in writing, must state the specific legal grounds for the denial, and must be issued by the official custodian or the custodian's designee. A blanket denial that fails to cite specific statutory authority is improper and may constitute a violation of the Act.

SECTION 45-219 — FEES

(a) A public agency may prescribe reasonable fees for providing access to or furnishing copies of public records. The fees may include:

(1) Charges for copying: A reasonable charge not to exceed the actual cost of copying, including the cost of the paper, toner, and machine time. For standard-size copies, the fee should reflect actual costs and is typically $0.25 per page or less, though the statute does not prescribe a specific per-page maximum.

(2) Charges for staff time: A public agency may charge for the staff time required to retrieve, search for, and copy records. The charge must be based on the actual salary and benefit costs of the personnel performing the work, and may not include overhead or other indirect costs. Staff time for determining whether records are subject to disclosure (legal review time) generally may not be charged to the requester.

(3) Charges for electronic records: A public agency may charge for the actual cost of the electronic medium (disc, flash drive, etc.) and for any programming time required to extract or compile electronic data, at rates reflecting the actual cost of the programmer's time.

(b) Fees may not be used as a barrier to access. The Act requires that fees be reasonable and proportional to the actual cost of compliance. A public agency may require payment in advance for estimated costs exceeding $500.

(c) Inspection of records at the agency's offices (viewing without copying) may not be subject to a fee, though the agency may require that the inspection occur during regular business hours and under the supervision of agency personnel.

SECTION 45-220 — CERTAIN RECORDS NOT REQUIRED TO BE OPEN

The Kansas Open Records Act provides that certain categories of records are not required to be open for public inspection. These exceptions include:

(a) Records specifically closed or confidential by federal statute, state statute, or rule of the Kansas Supreme Court.

(b) Records released to a public agency by a private individual or entity upon a promise of confidentiality, unless the promise was made in violation of law.

(c) Records that are privileged under the rules of evidence, including attorney-client privileged communications and attorney work product.

(d) Medical, psychiatric, psychological, or alcoholism and drug dependency treatment records of individuals.

(e) Personnel records, performance ratings, and individually identifiable records pertaining to employees and applicants for employment, except that the following are always open: name, position, title, salary, length of service, and status as a full-time or part-time employee.

(f) Letters of reference and recommendation pertaining to the character or qualifications of an identifiable individual.

(g) Records relating to pending investigations of possible violations of civil or criminal law, until the investigation is complete or a decision is made not to proceed with enforcement. Once the investigation is complete, the records generally become open, except for information that would identify confidential informants or reveal investigative techniques.

(h) Trade secrets or commercial or financial information obtained from a person or entity that is of a privileged or confidential nature.

(i) Proposals, bids, or quotations submitted to a public agency in response to a request for proposals, bids, or quotations, until a contract is awarded or all proposals are rejected.

(j) Records pertaining to the security measures of a public agency, including vulnerability assessments, security plans, and emergency response protocols.

(k) Notes, drafts, and preliminary documents prepared by or for the personal use of a public official or employee, if not retained as an official record of the agency.

(l) Testing and examination materials used for the purpose of administering licensing, certification, or qualifying examinations, prior to the administration of the examination.

(m) Records of a public agency containing information of a personal nature where the public disclosure of the information would constitute a clearly unwarranted invasion of personal privacy.

(n) Software programs owned or licensed by a public agency.

(o) Records concerning the care and treatment of persons at any correctional institution or facility.

SECTION 45-221 — ADDITIONAL CLOSED RECORDS PROVISIONS

This section provides additional categories of closed records, including records relating to: security of information technology systems; location information for victims of domestic violence; personal financial information of individuals; and various other categories specified by cross-reference to other Kansas statutes.

The Act requires agencies to redact exempt information and provide the non-exempt portions of records. An agency may not refuse to produce an entire record based on the presence of some exempt information; the agency must redact the exempt portions and produce the remainder.

SECTION 45-222 — ENFORCEMENT; PENALTIES; ATTORNEY'S FEES

(a) Civil Action: Any person denied access to public records may bring an action in district court to compel disclosure. The action must be brought in the county where the records are located or the county where the public agency has its principal office.

(b) In Camera Review: The court may examine the disputed records in camera to determine whether an exemption applies.

(c) Burden of Proof: The public agency bears the burden of proving that the record is exempt from disclosure. Exemptions are to be narrowly construed, and doubts are resolved in favor of disclosure.

(d) Attorney's Fees and Costs: If the court finds that the public agency denied access to public records in violation of the Act, the court may award the prevailing requester reasonable attorney's fees and court costs. The award of fees is discretionary but is routinely made when the agency's denial lacked a reasonable basis.

(e) Civil Penalties: If the court finds that the denial was made in bad faith or was based on an unreasonable interpretation of the Act, the court may impose a civil penalty of $100 to $500 per violation.

(f) Criminal Penalties: The KORA does not impose criminal penalties directly for denial of access. However, the knowing destruction, alteration, or concealment of public records to prevent their disclosure may constitute a criminal offense under other provisions of Kansas law.

(g) Injunctive Relief: The court may issue an injunction ordering the public agency to produce the records and may impose ongoing requirements for compliance.

SECTION 45-223 — RELATIONSHIP TO OTHER LAWS; LIBERAL CONSTRUCTION

The Kansas Open Records Act shall be liberally construed and applied to promote public access to governmental records. Where a conflict exists between the KORA and another statute, the more specific statute controls, but exemptions are to be construed narrowly.

The KORA works in conjunction with the Kansas Open Meetings Act (K.S.A. § 75-4317 et seq.) to promote open government. Records created in connection with meetings subject to the Open Meetings Act are themselves public records subject to the KORA.

ROLE OF THE ATTORNEY GENERAL

The Kansas Attorney General's office plays an advisory role in the interpretation and enforcement of the KORA. The AG issues opinions on the applicability of the Act, provides training and guidance to public agencies, and may intervene in judicial proceedings involving the KORA. While the AG does not have a formal "Public Access Counselor" office comparable to some other states, the AG's Government Counsel division regularly advises on open records issues and publishes a Kansas Open Government Handbook.

ELECTRONIC RECORDS AND MODERN APPLICATIONS

Public records maintained in electronic format are subject to the same access requirements as paper records under the KORA. Agencies must produce electronic records in the format in which they are maintained if the requester so requests, and may not require a requester to accept paper copies when electronic records exist. Email communications, text messages, instant messages, and other electronic communications made in connection with official business are public records, and agencies are responsible for maintaining and producing them upon request.

The KORA applies to records regardless of where they are stored — on agency servers, in cloud storage, on personal devices of public employees, or in any other location — as long as the records relate to the conduct of public business.

SCOPE AND APPLICATION

The KORA applies to all public agencies in Kansas, including state agencies, counties, cities, townships, school districts, community colleges, and special districts. The Act extends to any entity supported in whole or in part by public funds, which has been interpreted to include certain quasi-governmental entities, nonprofit organizations receiving public funding, and private entities performing governmental functions under contract.

The Kansas legislature is subject to the KORA, though legislative records are subject to certain additional provisions. The judiciary has adopted its own rules governing access to court records, which generally parallel the KORA's principles.''',
        'summary': 'The Kansas Open Records Act (K.S.A. §§ 45-215 through 45-223) requires all public records to be open for inspection and mandates agency response within three business days, with fees limited to actual costs and free inspection at agency offices. Enforcement is through district court actions with discretionary attorney\'s fees and civil penalties of $100 to $500 per violation, supported by the Attorney General\'s advisory role and the Act\'s explicit mandate for liberal construction in favor of access.',
        'jurisdiction_level': 'state',
    },
]


def build():
    conn = db_connect(DB_PATH)
    added = 0
    for doc in DOCUMENTS:
        doc['md5_hash'] = hashlib.md5(doc['text'].encode()).hexdigest()
        existing = conn.execute('SELECT id FROM documents WHERE id=?', (doc['id'],)).fetchone()
        if existing:
            print(f"  {doc['id']}: exists, skipping")
            continue
        conn.execute('''
            INSERT INTO documents (id, citation, title, date, document_type, jurisdiction,
                                   source, text, summary, md5_hash, jurisdiction_level)
            VALUES (:id, :citation, :title, :date, :document_type, :jurisdiction,
                    :source, :text, :summary, :md5_hash, :jurisdiction_level)
        ''', doc)
        added += 1
        print(f"  {doc['id']}: inserted")
    conn.commit()
    print(f"\nInserted {added} documents")
    conn.close()

if __name__ == '__main__':
    build()
