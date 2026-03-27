#!/usr/bin/env python3
"""Build state public records statute documents for MO, MT, NE, NV, NH, NJ, NM, NC."""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

DOCUMENTS = [
    # =========================================================================
    # MISSOURI — Sunshine Law
    # Mo. Rev. Stat. §§ 610.010 through 610.035
    # =========================================================================
    {
        'id': 'mo-public-records-statute',
        'citation': 'Mo. Rev. Stat. §§ 610.010–610.035',
        'title': 'Missouri Sunshine Law — Public Records Provisions',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'MO',
        'source': 'prdb-built',
        'text': '''Missouri Sunshine Law — Public Records Provisions
Mo. Rev. Stat. §§ 610.010 through 610.035

ARTICLE I. DEFINITIONS AND SCOPE (§ 610.010)

Section 610.010 establishes the definitional framework for Missouri's Sunshine Law as it applies to public records. A "public record" is defined broadly to include any record retained by or of a public governmental body, regardless of its physical form or characteristics. This encompasses paper documents, electronic data, emails, photographs, maps, and any other documentary material. A "public governmental body" includes every state agency, political subdivision, authority, board, commission, committee, and any other entity created by the Constitution or any law of the state, as well as any entity that receives public funds or is supported primarily by public funds. The definition also extends to quasi-governmental bodies when performing governmental functions. A "closed record" means any record that is specifically exempted from disclosure by statute. A "public meeting" is defined separately but intersects with public records obligations because minutes and records generated during meetings are generally open. The term "custodian" refers to the official who has responsibility for the maintenance of the public record.

ARTICLE II. POLICY OF OPEN RECORDS (§ 610.011)

Section 610.011 sets forth the state's policy that records of public governmental bodies are open to the public unless otherwise provided by law. The statute declares that it is the public policy of Missouri that meetings, records, votes, actions, and deliberations of public governmental bodies shall be open to the public unless otherwise provided by law. This section creates a strong presumption of openness and places the burden on the governmental body to justify any closure or withholding of records. Courts are directed to broadly construe the Sunshine Law in favor of open government and to narrowly construe any exceptions or exemptions. When there is any doubt as to the applicability of an exemption, the record should be disclosed. This provision has been interpreted by Missouri courts to mean that agencies must identify a specific statutory basis for withholding any record, and generalized claims of confidentiality are insufficient. The legislative intent is that government transparency is the default, and secrecy is the exception that must be justified.

ARTICLE III. ACCESS AND INSPECTION OF PUBLIC RECORDS (§ 610.023)

Section 610.023 establishes the right of access to public records. Each public governmental body must appoint a custodian who is responsible for maintaining the body's records and for responding to public records requests. Any person, regardless of citizenship, residency, or purpose, may request to inspect or copy public records. The statute does not require the requester to state a reason for seeking the records, and no governmental body may require a requester to explain why the records are sought.

Upon receiving a request, the custodian must respond as soon as possible, but no later than the end of the third business day following the date the request is received. If the custodian determines that access will be granted, the records must be made available within a reasonable time. If the custodian determines that the records are closed or that access will be denied in whole or in part, the custodian must provide a written statement explaining the grounds for denial, including the specific statutory provision relied upon to close or withhold the records. Failure to respond within three business days constitutes a denial.

If the records exist in electronic form, the custodian must provide them in electronic format if requested, provided this does not require the creation of a new program or the conversion of existing data to a new format. The governmental body may not require a requester to make a request in any particular form, though it may ask for clarification to identify the records sought.

ARTICLE IV. FEES AND COSTS (§ 610.026)

Section 610.026 governs fees for copying and research. Public governmental bodies may charge fees for providing access to or copies of public records, but these fees must not exceed the actual cost of document search, duplication, and copying. The statute specifies that fees may include the cost of staff time required to locate and duplicate the records, but the rate charged for staff time must not exceed the average hourly wage of the employee or employees who actually perform the search and duplication. Fees may also include the actual cost of the medium on which records are provided, such as paper, CDs, or other media.

Public governmental bodies may not charge fees that are intended to discourage requests or that are calculated to produce revenue beyond the actual cost of fulfilling the request. If a body determines that a fee will exceed a certain amount, it should notify the requester of the estimated cost before proceeding. The first page of any document is often provided free of charge or at a reduced rate, though this varies by agency. Indigent requesters may ask for a fee waiver, and some agencies have policies permitting waiver when disclosure serves the public interest.

ARTICLE V. EXEMPTIONS AND CLOSED RECORDS (§ 610.021)

Section 610.021 enumerates the categories of records that may be closed. This section provides an extensive list of records that public governmental bodies may close to public inspection. Among the most significant categories are:

Legal actions, causes of action, or litigation involving a public governmental body, including privileged communications between the body and its attorney. Personnel records relating to identifiable individuals, including applications, evaluations, disciplinary records, letters of reference, and records protected by other provisions of law. However, the name, position, and salary of any public employee are open records.

Records relating to the hiring, firing, disciplining, or promoting of employees where the records identify specific individuals, except that the final action taken and the reasons for that action are open records once a decision has been made. Individually identifiable personnel records, performance ratings, or records pertaining to employees or applicants for employment.

Software codes for electronic data processing and telecommunications, when disclosure would jeopardize the security of the system. Specifications for competitive bidding until the contract is awarded or all bids are rejected. Records that are protected from disclosure by federal law, regulation, or order of a court. Records relating to mental health, substance abuse treatment, and medical records of individuals.

Notwithstanding these exemptions, the statute emphasizes that exemptions are permissive rather than mandatory. A governmental body may choose to release records falling within an exemption unless a separate statute mandates closure. The burden rests on the body to demonstrate that a specific exemption applies to the specific records at issue, and blanket claims of exemption are disfavored.

ARTICLE VI. ENFORCEMENT AND REMEDIES (§§ 610.027–610.035)

Section 610.027 establishes the enforcement mechanisms for violations of the public records provisions. Any person denied access to public records may bring a civil action in the circuit court of the county where the records are maintained. The court may issue injunctive relief, order the production of records, and assess civil penalties. If the court finds that the governmental body knowingly or purposely violated the Sunshine Law, it must award the requester's reasonable attorney fees and litigation costs.

Civil penalties for knowing violations range from one thousand to five thousand dollars for a first violation, and up to twenty thousand dollars for subsequent violations. If the court finds the violation was purposeful, it may assess penalties up to five thousand dollars for a first offense and twenty thousand dollars for subsequent offenses. Individual members of a governmental body who purposely violate the statute may be held personally liable for penalties.

Section 610.028 provides that the attorney general has authority to investigate complaints of Sunshine Law violations and to bring enforcement actions. The AG may issue advisory opinions on the application of the Sunshine Law, and these opinions, while not binding on courts, carry persuasive weight.

Section 610.029 provides that the custodian or the governmental body may seek a declaratory judgment or other appropriate order regarding whether records are required to be open or closed. This allows governmental bodies to seek judicial guidance on close questions before committing to disclosure or closure.

Section 610.030 provides that public governmental bodies must maintain and preserve their records in compliance with applicable records retention schedules. The destruction of records in an effort to avoid disclosure constitutes a separate violation of the Sunshine Law.

The remedial structure is designed to make enforcement accessible to ordinary citizens. The availability of attorney fees for successful plaintiffs reduces the financial barrier to challenging wrongful denials. Courts have interpreted these remedies broadly, finding that partial success can still support an award of attorney fees in appropriate cases.

ARTICLE VII. RELATIONSHIP TO OTHER STATUTES

The Sunshine Law operates alongside other Missouri statutes that may create specific disclosure or closure requirements. Where another statute specifically closes particular records, that closure is incorporated by reference into the Sunshine Law framework. Conversely, where the Sunshine Law is silent on a particular category of records, the general presumption of openness applies. The interplay between the Sunshine Law and statutes governing specific agencies (such as child welfare, law enforcement, or taxation) has generated substantial case law, with courts generally resolving ambiguities in favor of disclosure.''',
        'summary': 'Missouri\'s Sunshine Law (Mo. Rev. Stat. §§ 610.010-610.035) establishes a broad presumption of openness for all records of public governmental bodies. Any person may request records regardless of purpose. Custodians must respond within three business days. Fees are limited to actual costs of search and duplication. Section 610.021 enumerates permissive exemptions including personnel records, litigation materials, and security-related information. Enforcement is through circuit court, with mandatory attorney fee awards for knowing violations and civil penalties up to $20,000 for repeat offenders.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # MONTANA — Constitution Art. II § 9 + Right to Know Act
    # Mont. Code §§ 2-6-1001 through 2-6-1030
    # =========================================================================
    {
        'id': 'mt-public-records-statute',
        'citation': 'Mont. Code §§ 2-6-1001–2-6-1030',
        'title': 'Montana Right to Know — Constitutional and Statutory Public Records Provisions',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'MT',
        'source': 'prdb-built',
        'text': '''Montana Right to Know — Constitutional and Statutory Public Records Provisions
Montana Constitution Art. II, § 9 and Mont. Code §§ 2-6-1001 through 2-6-1030

ARTICLE I. CONSTITUTIONAL FOUNDATION (Art. II, § 9)

Montana is one of a small number of states that provides a constitutional right of access to public information. Article II, Section 9 of the Montana Constitution states: "No person shall be deprived of the right to examine documents or to observe the deliberations of all public bodies or agencies of state government and its subdivisions, except in cases in which the demand of individual privacy clearly exceeds the merits of public disclosure." This constitutional provision is self-executing, meaning it provides enforceable rights even absent implementing legislation. The constitutional standard creates a balancing test between public disclosure and individual privacy, with the burden falling on the party seeking to prevent disclosure to demonstrate that privacy interests clearly exceed the public interest in transparency.

The Montana Supreme Court has interpreted this provision as creating one of the strongest open-government mandates in the nation. Because the right is constitutional rather than merely statutory, the legislature cannot diminish it through ordinary legislation, and any statutory exemptions must be consistent with the constitutional standard. Courts apply strict scrutiny to claimed exemptions, requiring the government to demonstrate that privacy interests are not merely relevant but that they "clearly exceed" the merits of disclosure.

ARTICLE II. STATUTORY FRAMEWORK — RIGHT TO KNOW ACT (§§ 2-6-1001–1003)

Section 2-6-1001 sets forth the purpose of the statute: to provide the public with full and complete information regarding the affairs of government and the official acts of those who represent them. The legislature declares that the people of Montana have a constitutional right to know what their government is doing and that this right should be given the broadest possible construction.

Section 2-6-1002 defines key terms. "Public information" means any information prepared, owned, used, or retained by any public agency relating to the transaction of official business, regardless of form. "Public agency" means any political subdivision of the state, including all counties, cities, towns, school districts, special districts, boards, commissions, and any other entity created by or pursuant to law that receives or expends public funds.

Section 2-6-1003 establishes that every person has a right to inspect and take a copy of any public information of this state, except as provided by law. This right extends to all persons and is not conditioned on residency, citizenship, or stated purpose. No public agency may require a requester to state why the information is sought.

ARTICLE III. PROCEDURES FOR REQUESTING RECORDS (§§ 2-6-1004–1006)

Section 2-6-1004 establishes that a request for public information may be made orally or in writing. While the statute does not mandate written requests, a written request may be advisable to create a record of the request and to start any applicable response timeline. Upon receipt of a request, the agency must respond promptly.

Montana does not impose a specific statutory deadline measured in business days for responding to public records requests, but the constitutional right to know requires that responses be provided without unreasonable delay. Courts have interpreted this to mean that agencies must act with reasonable promptness under the circumstances, taking into account the volume and complexity of the request. Unreasonable delays may themselves constitute a violation of the constitutional right.

Section 2-6-1005 provides that if an agency determines that the requested information is confidential or otherwise exempt from disclosure, it must inform the requester in writing, stating the specific legal basis for the denial. A general assertion that records are confidential is insufficient; the agency must cite the particular statute or constitutional provision that authorizes closure.

Section 2-6-1006 addresses the form in which records are to be provided. If records exist in electronic form, they should be provided in electronic format if requested. The agency is not required to create new records, compile information not already maintained, or convert records into a format not used by the agency.

ARTICLE IV. FEES (§ 2-6-1009)

Section 2-6-1009 governs the fees that agencies may charge. An agency may charge a fee for producing a copy of public information that does not exceed the actual cost of producing the copy. This includes the cost of the medium (paper, electronic media) and the proportionate cost of staff time needed to locate and copy the records. Agencies may not charge for the time required to determine whether requested records are exempt from disclosure, as that is a governmental function and not a service to the requester. Inspection of records in person is generally free, with charges applicable only when copies are made.

If a request requires extensive staff time, the agency may require a deposit before beginning the search. However, the fees charged must bear a reasonable relationship to the actual cost, and fees set at levels designed to discourage requests are inconsistent with the constitutional right.

ARTICLE V. EXEMPTIONS (§§ 2-6-1020–1023)

Exemptions from disclosure under Montana law must be analyzed through the lens of the constitutional balancing test. Even where a statute purports to make records confidential, a court may order disclosure if the privacy interests do not "clearly exceed" the public interest. Major categories of records that may be withheld include:

Criminal justice information that is part of an ongoing investigation, where disclosure would jeopardize the investigation or endanger individuals. Once an investigation is complete, the records are generally subject to disclosure. Tax records and financial information of individuals that is submitted to the government under a promise of confidentiality. Medical, psychological, and mental health records of identifiable individuals. Records protected by attorney-client privilege or work product doctrine. Personnel records of public employees, though the name, title, salary, dates of employment, and job description of public employees are always open. Proprietary or trade secret information submitted by businesses to government agencies under circumstances indicating the information was to be kept confidential. Records whose disclosure is prohibited by federal law or regulation.

The Montana Supreme Court has repeatedly emphasized that categorical exemptions are disfavored. Each record or portion of a record must be evaluated individually, and agencies are expected to redact exempt information and disclose the remainder rather than withholding entire documents based on the presence of some exempt material.

ARTICLE VI. ENFORCEMENT AND REMEDIES (§§ 2-6-1025–1030)

Section 2-6-1025 provides that any person who has been denied access to public information may bring an action in district court. The court may examine the records in camera to determine whether they are subject to disclosure. If the court finds that the agency improperly withheld records, it must order their disclosure.

Section 2-6-1026 provides for the award of costs and attorney fees to a prevailing plaintiff. If the court finds that the agency acted arbitrarily or capriciously in withholding records, it must award attorney fees. This provision is critical to ensuring that citizens can effectively vindicate their constitutional right without bearing the full cost of litigation.

Section 2-6-1027 provides that a public servant who purposely or knowingly violates the right to know is subject to removal from office or employment in addition to any other penalties. This individual accountability measure underscores the seriousness with which Montana treats the right of public access.

The constitutional foundation of Montana's right to know means that enforcement actions can be brought not only under the statutory framework but also directly under the Montana Constitution. This dual avenue of enforcement provides robust protections for public access and limits the legislature's ability to narrow public access through statutory amendments alone.

ARTICLE VII. INTERACTION WITH FEDERAL LAW AND OTHER STATE STATUTES

Montana's right to know extends only to records of state and local government. Federal records held by federal agencies in Montana are governed by the federal Freedom of Information Act. However, when state or local agencies maintain copies of federal records, or when federal and state records are intermingled, the state constitutional and statutory framework applies to the state-held copies. Other Montana statutes create specific confidentiality requirements for certain categories of records (such as child abuse reports, adoption records, and certain health records), and these must be analyzed under the constitutional balancing test to determine whether they represent valid restrictions on the right to know.''',
        'summary': 'Montana provides a constitutional right to public information under Art. II, § 9, creating one of the strongest open-government mandates in the nation. The Right to Know Act (Mont. Code §§ 2-6-1001-1030) implements this right. Any person may request records without stating a purpose. No strict statutory response deadline exists, but unreasonable delay violates the constitutional right. Exemptions are evaluated under a balancing test where privacy must "clearly exceed" the public interest. Courts may award attorney fees for arbitrary withholding, and officials who purposely violate the right face removal from office.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NEBRASKA — Public Records Statutes
    # Neb. Rev. Stat. §§ 84-712 through 84-712.09
    # =========================================================================
    {
        'id': 'ne-public-records-statute',
        'citation': 'Neb. Rev. Stat. §§ 84-712–84-712.09',
        'title': 'Nebraska Public Records Statutes',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NE',
        'source': 'prdb-built',
        'text': '''Nebraska Public Records Statutes
Neb. Rev. Stat. §§ 84-712 through 84-712.09

ARTICLE I. RIGHT OF ACCESS AND DEFINITIONS (§ 84-712)

Section 84-712 establishes the fundamental right of public access to government records in Nebraska. Every citizen of the state, and every other person with a legitimate interest, has the right to examine public records during the regular business hours of the office in which the records are kept. The statute applies to all records and documents of or belonging to the state, any county, city, village, political subdivision, or any tax-supported district in the state. "Public records" includes all records and documents, regardless of physical form, of or belonging to the state, its agencies, or political subdivisions.

The scope of this right is broad. It encompasses paper documents, electronic records, databases, emails, text messages, recordings, photographs, and any other documentary material maintained by a government entity. The right extends to records held by entities that are supported by public funds, even if they are not traditional government agencies. The statute does not require the requester to identify a specific purpose for seeking the records, though it does reference persons with "legitimate interest," a phrase that has been interpreted broadly to encompass virtually any reason for seeking government records.

ARTICLE II. REQUEST PROCEDURES AND RESPONSE TIMELINES (§ 84-712.01)

Section 84-712.01 governs the procedures for requesting access to public records. A request may be made in person, by mail, by telephone, or by electronic means. While no particular form is required, a written request is advisable for documentation purposes. The custodian of public records must respond to a request within four business days after actual receipt. This response must either provide the records, provide a written estimate of the expected time to fulfill the request, or deny the request in writing with the specific legal basis for the denial.

If the request is denied, the custodian must identify the specific statute or legal authority that authorizes the withholding. A general assertion that records are confidential or exempt is not sufficient. The custodian must also inform the requester of the right to appeal the denial.

If the custodian needs additional time to locate or compile the records, the custodian must provide the records as soon as is practicable. The four-business-day requirement is for the initial response, not necessarily for the production of all responsive records. However, unreasonable delays in producing records after the initial response may be challenged.

ARTICLE III. FEES AND COSTS (§ 84-712.03)

Section 84-712.03 addresses the fees that may be charged for providing copies of public records. The custodian may charge a fee that does not exceed the actual cost of producing the copy. Actual costs include the cost of the medium (paper, electronic storage media) and the actual cost of personnel time required to make the copies. The fee must be uniform for all requesters and may not be increased for particular requesters or particular types of requests.

Inspection of records in the office where they are maintained is generally free of charge, and custodians may not charge fees for the right to inspect records. Fees apply only when copies are requested. If a request is anticipated to generate significant costs, the custodian should inform the requester of the estimated cost before proceeding, and may require prepayment or a deposit.

The statute prohibits agencies from using fee structures as a mechanism to discourage public records requests. Courts have held that fees must bear a reasonable relationship to the actual cost of production and that inflated or punitive fee schedules violate the public records law.

ARTICLE IV. EXEMPTIONS (§§ 84-712.04–84-712.06)

Section 84-712.05 enumerates the categories of records that are exempt from mandatory disclosure. Nebraska's exemptions include:

Personal information in records regarding students, prospective students, and their parents or guardians maintained by educational institutions. Medical records, psychiatric records, and other records of individual health maintained by government agencies. Trade secrets and proprietary business information provided to government agencies under express or implied promises of confidentiality. Records related to pending litigation or settlement negotiations involving a public body. Criminal investigative records, the disclosure of which would interfere with an ongoing investigation, reveal the identity of a confidential informant, or endanger the life or physical safety of any individual.

Tax return information and income data submitted to the state or political subdivisions. Appraisals or appraisal information regarding the purchase of real property for public purposes, prior to the execution of the purchase. Records protected from disclosure by federal law, regulation, or court order. Security-related records whose disclosure would compromise the safety of persons or property, including security plans, vulnerability assessments, and emergency response protocols.

Section 84-712.06 provides that where only a portion of a record is exempt, the custodian must redact the exempt portions and disclose the remainder. Agencies may not withhold an entire document merely because some portion of it contains exempt information. The obligation to segregate and disclose non-exempt material is affirmative, and agencies must make reasonable efforts to provide as much information as possible.

ARTICLE V. ENFORCEMENT AND REMEDIES (§§ 84-712.07–84-712.09)

Section 84-712.07 provides that any person denied access to public records may file a petition in the district court of the county where the records are maintained. The petition must name the custodian as defendant and identify the records sought. The court may conduct an in camera inspection of the records to determine whether they are exempt from disclosure.

If the court determines that the records were improperly withheld, it must order their production and may award reasonable attorney fees and costs to the prevailing plaintiff. The availability of attorney fees is essential to ensuring that citizens can meaningfully enforce their right of access without being deterred by the potential cost of litigation. Courts have interpreted this provision to support fee awards whenever the litigation has been a catalyst for the release of improperly withheld records.

Section 84-712.08 provides that a custodian who willfully fails to comply with the public records statutes is subject to removal from office or employment. This individual liability provision serves as a deterrent against purposeful withholding or destruction of records.

Section 84-712.09 establishes additional protections against the destruction of records in violation of applicable retention schedules. The purposeful destruction of records to avoid disclosure constitutes a separate violation and may subject the responsible individuals to penalties.

ARTICLE VI. ELECTRONIC RECORDS AND MODERN APPLICATIONS

Nebraska's public records statutes apply equally to electronic records. As government agencies increasingly maintain records in electronic databases, email systems, and other digital formats, the obligations of custodians extend to these electronic repositories. Custodians must be prepared to search electronic systems for responsive records and to provide electronic copies when requested in that format. The statute does not require agencies to create new software or to compile data in formats not already maintained, but it does require agencies to provide electronic records in their existing format when that is the form of the request.

The application of the public records law to electronic communications, including email and text messages, has been an evolving area. The Nebraska Attorney General has issued guidance confirming that emails and text messages related to official business are public records subject to the same disclosure obligations as paper records, regardless of whether they are sent or received on government-owned or personally owned devices.''',
        'summary': 'Nebraska\'s Public Records Statutes (Neb. Rev. Stat. §§ 84-712 through 84-712.09) grant citizens and persons with legitimate interest the right to examine all government records regardless of form. Custodians must respond within four business days. Fees are limited to actual costs and cannot be used to discourage requests. Exemptions cover personal records, medical records, trade secrets, ongoing investigations, and security information. Agencies must segregate and disclose non-exempt portions. Courts may award attorney fees to prevailing plaintiffs, and custodians who willfully violate the statute face removal from office.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NEVADA — Public Records Act
    # NRS §§ 239.005 through 239.030
    # =========================================================================
    {
        'id': 'nv-public-records-statute',
        'citation': 'NRS §§ 239.005–239.030',
        'title': 'Nevada Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NV',
        'source': 'prdb-built',
        'text': '''Nevada Public Records Act
NRS §§ 239.005 through 239.030

ARTICLE I. LEGISLATIVE DECLARATION AND DEFINITIONS (§§ 239.005–239.008)

Section 239.001 establishes the legislature's declaration that all public books and public records of governmental entities must be open to inspection by any person, and that this policy of transparency should be broadly construed to maximize access to government records. The legislature further declares that any restrictions on access must be narrowly construed and that any doubt regarding the applicability of an exemption should be resolved in favor of disclosure.

Section 239.005 defines the key terms. "Governmental entity" means any elected or appointed officer or any agency, department, board, commission, authority, or other unit of state government, as well as any political subdivision of the state, including counties, cities, towns, school districts, and special districts. "Public book" or "public record" means a book or record kept or required to be kept by any governmental entity, and includes any document, paper, electronic record, letter, map, book, tape, photograph, film, recording, or other material regardless of physical form or characteristics.

Section 239.008 establishes that the provisions of Chapter 239 must be construed liberally to maximize public access to governmental records and that any exemption, exception, or balancing of interests that limits or restricts access must be construed narrowly.

ARTICLE II. RIGHT OF ACCESS AND INSPECTION (§ 239.010)

Section 239.010 provides the core right of access: all public books and public records of a governmental entity must be open at all times during office hours to inspection by any person, and free copies must be furnished to members of the legislature and state officers. Any person may request copies of public records, and the governmental entity must provide them within five business days of receipt of the request.

The five-business-day response window is among the most commonly litigated aspects of the statute. If the governmental entity cannot provide the records within five business days, it must notify the requester and provide a date and time by which the records will be available. The notification must include the reasons for the delay. However, the statute does not set an outer limit on the total time for production, which has led to disputes about what constitutes an unreasonable delay after the initial response.

A governmental entity may not ask a requester to explain the purpose of the request as a condition of providing access. Any person may request records, regardless of residency, citizenship, or stated purpose.

ARTICLE III. FEES AND COSTS (§ 239.052–239.055)

Section 239.052 governs the fees that governmental entities may charge. A governmental entity may charge a fee for providing a copy of a public record. The fee must not exceed the actual cost to the governmental entity to provide the copy, unless a specific statute authorizes a different fee. The actual cost includes the cost of the medium on which the copy is provided and any applicable labor costs for the time required to locate and copy the records.

Section 239.055 provides that a governmental entity may charge an advance deposit if the estimated cost of fulfilling a request exceeds fifty dollars. The entity must provide a written estimate of the cost before requiring the deposit. If the actual cost is less than the deposit, the entity must refund the difference.

Governmental entities may not charge for the cost of determining whether records are exempt from disclosure. That analysis is a governmental function, not a service to the requester. Fees for inspection of records in person are generally not permitted; fees apply only to the production of copies.

ARTICLE IV. CONFIDENTIAL RECORDS AND EXEMPTIONS (§§ 239.010–239.012)

Section 239.010 provides that a governmental entity may deny access to public records only if the records are declared confidential by law. "Declared confidential by law" means that a specific statute, regulation, or court order identifies the records as confidential. A governmental entity may not create its own confidentiality designations absent specific legal authority.

Categories of records that are commonly declared confidential under various Nevada statutes include:

Records of ongoing criminal investigations, where disclosure would compromise the investigation or endanger individuals. The identity, home address, and personal telephone number of law enforcement officers, judges, and certain other public officials when disclosure would constitute a threat to their safety. Medical records and health information of identifiable individuals. Tax return information and personal financial data submitted to government agencies. Records related to the adoption of children. Trade secrets and proprietary business information submitted to government agencies under conditions of confidentiality. Personnel records of public employees, except that the name, title, salary, job description, and dates of employment of public employees are public records. Attorney-client privileged communications and attorney work product. Records whose disclosure is prohibited by federal law, regulation, or court order.

Section 239.0107 establishes that when a governmental entity denies a request, it must provide the specific statutory or legal authority for the denial within five business days. The entity must also indicate that the requester may appeal the denial to the district court. General claims of confidentiality without citation to specific legal authority are insufficient to justify denial.

Section 239.011 provides that even where a record contains some confidential information, the governmental entity must provide access to the non-confidential portions. The entity must segregate the confidential information through redaction and provide the remainder. Agencies may not withhold entire documents based on the presence of some exempt material.

ARTICLE V. ENFORCEMENT AND REMEDIES (§§ 239.011–239.030)

Section 239.011 provides that any person who is denied access to inspect or copy a public record may apply to the district court for an order compelling disclosure. The court may examine the records in camera and must order disclosure if it determines that the records are not properly exempt from disclosure.

Section 239.012 provides that if the court determines that a governmental entity acted in bad faith in denying access, the court may award reasonable attorney fees and costs to the requester. The court may also impose a civil penalty of not less than one hundred dollars and not more than five hundred dollars against the governmental entity for each act of bad faith.

Section 239.013 provides that a governmental entity that fails to comply with a court order requiring disclosure may be held in contempt. Individual officers or employees who willfully fail to comply with the public records act may be subject to disciplinary action, including removal from office.

The enforcement framework is designed to provide meaningful remedies while acknowledging that many denials are made in good faith, even if they are ultimately found to be incorrect. The bad faith standard for attorney fees means that requesters must demonstrate more than a simple error in judgment; they must show that the denial was unreasonable or based on improper motives. This standard has been criticized as too permissive of governmental entities and difficult for requesters to meet.

ARTICLE VI. PRESERVATION AND RETENTION

Nevada law requires governmental entities to maintain their records in accordance with applicable retention schedules established by the State Library, Archives and Public Records Administrator. The destruction of public records in violation of retention schedules, particularly when done to avoid disclosure, may constitute a criminal offense under separate provisions of Nevada law. Governmental entities must also maintain records in a manner that facilitates public access, and the adoption of records management systems that make records difficult to locate or retrieve may be challenged as inconsistent with the public records act.

The application of the public records act to electronic records, including email, text messages, social media accounts maintained for official purposes, and databases, follows the same principles as for paper records. The format of the record does not affect its status as a public record, and governmental entities must be prepared to search electronic systems and provide electronic copies when requested.''',
        'summary': 'Nevada\'s Public Records Act (NRS §§ 239.005-239.030) declares that all public records must be open to inspection by any person during office hours. Governmental entities must respond within five business days. Fees may not exceed actual costs, and deposits may be required for requests exceeding $50. Records may only be withheld if declared confidential by specific statute, and agencies must segregate and disclose non-confidential portions. Courts may award attorney fees and civil penalties ($100-$500 per act) for bad faith denials. The statute is construed liberally to maximize access.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NEW HAMPSHIRE — Right-to-Know Law
    # RSA Ch. 91-A
    # =========================================================================
    {
        'id': 'nh-public-records-statute',
        'citation': 'RSA Ch. 91-A',
        'title': 'New Hampshire Right-to-Know Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NH',
        'source': 'prdb-built',
        'text': '''New Hampshire Right-to-Know Law
RSA Chapter 91-A

ARTICLE I. PURPOSE AND DEFINITIONS (§§ 91-A:1–91-A:1-a)

Section 91-A:1 states the purpose of the chapter: openness in the conduct of public business is essential to a democratic society. The Right-to-Know Law is intended to ensure both that the actions of public bodies are conducted openly and that the records of public bodies are available for public inspection. The statute reflects the fundamental principle that government accountability requires public access to the records that document governmental decisions, expenditures, and actions.

Section 91-A:1-a provides definitions. "Governmental records" means any information created, accepted, or obtained by, or on behalf of, any public body, or a quorum of a public body, or a public agency in furtherance of its official function. Regardless of physical form, whether paper, electronic, audio, visual, or any other medium, information constitutes a governmental record if it pertains to government business. "Public body" means any board, commission, agency, department, or other governmental entity, as well as the general court (legislature) and its committees. "Public agency" means any agency, authority, department, or office of the state or of any county, town, city, school district, school administrative unit, or other political subdivision.

The scope of "governmental records" has been interpreted expansively by New Hampshire courts. It includes emails sent by public officials on personal devices regarding government business, text messages, calendars, notes from meetings, and drafts of documents. The key inquiry is whether the record was created or maintained in connection with official business, not who owns the device on which it resides.

ARTICLE II. ACCESS TO RECORDS AND RESPONSE PROCEDURES (§ 91-A:4)

Section 91-A:4 provides the core right of access. Every citizen during the regular or business hours of all public bodies or agencies, and on the regular business premises of such public bodies or agencies, has the right to inspect all governmental records in the possession, custody, or control of such public bodies or agencies, including minutes of meetings, and to copy and make memoranda or abstracts of the records or minutes.

Upon request, a public body or agency must make available for inspection and copying any governmental record, unless the record falls within one of the enumerated exemptions. The public body or agency must respond to a request within five business days by either making the records available, denying the request with a written explanation of the reason for the denial and the specific exemption relied upon, or acknowledging receipt and providing a reasonable estimate of when the records will be available.

The statute does not require a requester to identify a purpose for seeking the records. New Hampshire courts have held that the right of access belongs to all citizens and cannot be conditioned on the requester's identity, purpose, or intended use of the records. Anonymous requests are permitted, though agencies may require sufficient information to identify the records sought.

ARTICLE III. FEES (§ 91-A:4, IV)

Section 91-A:4, IV governs fees. A public body or agency may charge a reasonable fee for providing copies of governmental records. The fee must cover only the actual cost of providing the copy, which may include the cost of the medium (paper, electronic media) and the labor cost of locating the records and making copies. The fee may not include charges for reviewing records to determine whether they are exempt from disclosure.

There is no charge for merely inspecting records in person. Fees apply only to the production of copies. If the estimated cost of fulfilling a request is substantial, the agency may require prepayment or a deposit before beginning the work. The fee schedule should be uniform and publicly available.

New Hampshire courts have scrutinized fee practices to ensure that they do not serve as practical barriers to access. Fees that are disproportionate to the actual cost of production or that appear designed to discourage requests may be challenged and overturned.

ARTICLE IV. EXEMPTIONS (§ 91-A:5)

Section 91-A:5 enumerates the exemptions from disclosure. Governmental records are exempt from public disclosure if they fall into one of the following categories:

Records of matters related to the preparation for and carrying out of all emergency functions, including training, if disclosure would jeopardize the safety of any person or the physical security of any facility. Confidential, commercial, or financial information obtained from a person and not otherwise publicly available. This exemption is frequently invoked to protect trade secrets and proprietary business information submitted to government agencies. However, the information must be truly confidential and not otherwise available to the public.

Records pertaining to internal personnel practices, including but not limited to evaluations, disciplinary actions, and internal affairs investigations. The names, titles, salaries, and dates of employment of public employees are not exempt. Records pertaining to matters of strategy or negotiation with respect to collective bargaining. Personal school records of students, including their identities, grades, and other academic information. Records protected by attorney-client privilege or the work product doctrine. Medical and other health records of identifiable individuals.

Preliminary drafts, notes, and memoranda that are part of the deliberative process. This exemption protects the internal deliberations of government officials by shielding documents that reflect the agency's thinking before a final decision is reached. However, once a decision is made, the factual portions of deliberative documents may become subject to disclosure. The deliberative process exemption does not apply to purely factual material that can be segregated from the deliberative portions.

Records pertaining to the security of information technology systems and infrastructure. Records whose disclosure is prohibited by other statutes, federal law, or court order.

The New Hampshire Supreme Court has held that exemptions must be construed narrowly and that the public body bears the burden of demonstrating that a record falls squarely within an exemption. Where only part of a record is exempt, the agency must redact the exempt portion and disclose the remainder.

ARTICLE V. ENFORCEMENT AND REMEDIES (§§ 91-A:7–91-A:8)

Section 91-A:7 provides that any person aggrieved by a violation of the Right-to-Know Law may petition the superior court for injunctive relief. The court may order the production of records, enjoin future violations, and declare the rights of the parties. If the court finds that the public body or agency violated the statute, it shall award reasonable attorney fees and costs to the petitioner unless the court finds that the body or agency had a reasonable basis for denying the request.

The attorney fee provision is significant because it does not require a finding of bad faith. If the requester prevails, attorney fees are presumptively awarded unless the court specifically finds that the denial had a reasonable basis. This is a more requester-friendly standard than the bad faith standard used in some other states and creates a meaningful deterrent against unjustified denials.

Section 91-A:8 provides that the remedies available under the Right-to-Know Law are in addition to, and not exclusive of, any other remedies available under law. This means that a person denied access may pursue claims under other statutes, the state constitution, or common law in addition to the statutory remedy.

The Right-to-Know Law also provides for expedited hearings in the superior court. Recognizing that delayed access to records can effectively deny access, the statute provides that petitions under the Right-to-Know Law should be given priority on the court's calendar and should be heard expeditiously.

ARTICLE VI. RECORD RETENTION AND DESTRUCTION

Public bodies and agencies are required to maintain governmental records in accordance with applicable retention schedules. The destruction of records in violation of retention schedules, or in anticipation of a records request, may constitute a violation of the Right-to-Know Law and may give rise to sanctions. Courts have imposed adverse inferences against governmental bodies that destroy records after a request has been made or is reasonably anticipated.

ARTICLE VII. APPLICATION TO ELECTRONIC RECORDS

The Right-to-Know Law applies to governmental records in all forms, including electronic records. This encompasses email, text messages, voicemail, social media posts and messages (when related to government business), databases, and any other electronically stored information. Public officials who conduct government business on personal devices or accounts are subject to the same disclosure obligations as if they had used government-provided devices. New Hampshire courts have held that the use of personal email accounts or text messaging applications to conduct government business does not shield those communications from disclosure under the Right-to-Know Law.''',
        'summary': 'New Hampshire\'s Right-to-Know Law (RSA Ch. 91-A) provides every citizen the right to inspect and copy governmental records during business hours. Agencies must respond within five business days. Fees are limited to actual costs; inspection is free. Exemptions include emergency preparedness records, confidential commercial information, internal personnel practices, deliberative process materials, and attorney-client privileged records. Attorney fees are presumptively awarded to prevailing requesters unless the denial had a reasonable basis. The law applies fully to electronic records including those on personal devices used for government business.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NEW JERSEY — Open Public Records Act (OPRA)
    # N.J.S.A. §§ 47:1A-1 through 47:1A-13
    # =========================================================================
    {
        'id': 'nj-public-records-statute',
        'citation': 'N.J.S.A. §§ 47:1A-1–47:1A-13',
        'title': 'New Jersey Open Public Records Act (OPRA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NJ',
        'source': 'prdb-built',
        'text': '''New Jersey Open Public Records Act (OPRA)
N.J.S.A. §§ 47:1A-1 through 47:1A-13

ARTICLE I. LEGISLATIVE FINDINGS AND DEFINITIONS (§§ 47:1A-1–47:1A-2)

Section 47:1A-1 establishes the legislative findings and declaration of policy. The legislature finds and declares that government records must be readily accessible for inspection, copying, or examination by the citizens of New Jersey. This right of access is derived from the inherent right of the people in a democracy to have access to the records of government and to know what their government is doing. Any limitations on the right of access must be construed in favor of the public's right to access, and the custodian of a government record has the burden of proving that a denial of access is authorized by law.

Section 47:1A-1.1 provides definitions. "Government record" or "record" means any paper, written or printed book, document, drawing, map, plan, photograph, microfilm, data processed or image processed document, information stored or maintained electronically or by sound-recording or in a similar device, or any copy thereof, that has been made, maintained, or kept on file in the course of official business by any officer, commission, agency, or authority of the state or of any political subdivision thereof, including subordinate boards thereof, or that has been received in the course of official business by any such officer, commission, agency, or authority.

"Custodian" is defined as the officer officially designated by formal action of that body's governing body to serve as the custodian of government records, or in the absence of such a designation, the officer who has actual custody of the records. "Public agency" includes the state, any of its political subdivisions, agencies, commissions, authorities, boards, offices, departments, and divisions, as well as certain quasi-governmental entities.

ARTICLE II. REQUEST PROCEDURES AND RESPONSE (§§ 47:1A-5–47:1A-5.4)

Section 47:1A-5 establishes the procedures for requesting government records. A custodian must adopt a form for requests, which must include fields for the requester's name, address, and a description of the records sought. The use of the official request form is mandatory, and a custodian may reject requests that are not made on the form. However, the form must be readily available and easily accessible, and the use of the form requirement cannot be used to create practical barriers to access.

A request must identify specific records or categories of records sought. OPRA does not require agencies to conduct research, analyze data, or create new records in response to requests. The statute draws a distinction between requests for identifiable records and requests for information; only the former are cognizable under OPRA. This distinction has generated significant litigation, with courts holding that overly broad requests that do not identify specific documents or categories of documents may be denied as invalid.

The custodian must respond to a request within seven business days after receiving it. The response must either grant access, deny access with a specific statement of the basis for denial and the statutory provision relied upon, or request an extension of time. Extensions must be for a specific duration and are permitted only when the circumstances reasonably require additional time. If the custodian fails to respond within seven business days, the failure is deemed a denial.

The custodian must also inform the requester of the right to challenge a denial by filing a complaint with the Government Records Council or by bringing an action in the Superior Court.

ARTICLE III. FEES (§ 47:1A-5)

Section 47:1A-5 addresses fees. A custodian must permit access to a government record and must provide a copy or copies of a government record upon payment of the lawful fee. For paper copies, the fee may not exceed the actual cost of duplication. The statute sets a maximum fee of seventy-five cents per page for letter-sized and legal-sized copies, and a maximum fee for other sizes based on the actual cost of reproduction.

For electronic records, the fee may not exceed the actual cost of the medium on which the records are provided (such as a CD, flash drive, or electronic transmission cost). The custodian may not charge for the labor associated with retrieving or reviewing records, except in limited circumstances where the request requires an extraordinary expenditure of time and effort. In those cases, the custodian must notify the requester of the estimated special service charge before proceeding.

Inspection of records is free. The custodian must allow a requester to examine records during regular business hours without charge. The fee structure under OPRA is designed to keep the cost of access low and to prevent fees from serving as barriers to transparency.

ARTICLE IV. EXEMPTIONS (§§ 47:1A-1.1, 47:1A-3, 47:1A-9, 47:1A-10)

OPRA contains both specific categorical exemptions and broader exclusions. Section 47:1A-1.1 excludes certain categories from the definition of "government record" entirely, meaning that these categories are not subject to OPRA at all. These exclusions include:

Inter-agency or intra-agency advisory, consultative, or deliberative material. This is the deliberative process exclusion, which protects the internal decision-making process of government agencies. It applies to material that reflects the opinions, recommendations, or deliberations of agency personnel, but not to purely factual material that can be segregated. This exclusion has been one of the most frequently litigated aspects of OPRA, with courts requiring agencies to demonstrate that the specific material withheld is genuinely deliberative rather than merely inconvenient to disclose.

Legislative records, including bills, amendments, resolutions, and records of votes. Records within the attorney-client privilege. This exclusion protects communications between government agencies and their attorneys that are made for the purpose of obtaining or providing legal advice. The privilege belongs to the government agency and may be waived.

Section 47:1A-3 provides that a public agency has the burden of proving that a denial of access is authorized by law. This burden-shifting provision is critical: the agency, not the requester, must demonstrate that a specific legal authority justifies the withholding. Courts have applied this standard rigorously, requiring agencies to identify the particular statutory provision, court rule, or other legal basis for each record or category of records withheld.

Section 47:1A-9 provides additional exemptions for criminal investigatory records. Records that are part of an ongoing criminal investigation are exempt while the investigation is active. Victim records, including the names and addresses of crime victims, are also protected. However, certain law enforcement records are specifically designated as open, including arrest records, certain police reports, and records of completed investigations.

Section 47:1A-10 provides exemptions for personnel records. Employee personnel records, including evaluations, disciplinary records, and medical records, are generally exempt. However, the name, title, position, salary, payroll record, length of service, date of separation, reason for separation, and amount of pension of any current or former public employee are government records subject to disclosure.

ARTICLE V. GOVERNMENT RECORDS COUNCIL (§§ 47:1A-6–47:1A-7)

Section 47:1A-6 establishes the Government Records Council (GRC) as an administrative body with jurisdiction over OPRA complaints. The GRC consists of members appointed by the Governor and confirmed by the Senate. A person who is denied access to a government record may file a complaint with the GRC within forty-five days of the denial. The GRC investigates the complaint, conducts mediation if appropriate, and issues decisions that are binding on the parties unless appealed to the Appellate Division of the Superior Court.

The GRC process provides an alternative to litigation for challenging denials. It is generally faster and less expensive than court proceedings, and the requester does not need to retain an attorney. However, the GRC's remedial powers are more limited than those of a court, and some requesters prefer to proceed directly to court, which is also permitted under OPRA.

Section 47:1A-7 provides that the GRC may impose civil penalties on a custodian who knowingly and willfully violates OPRA. The penalties are one thousand dollars for a first offense, two thousand five hundred dollars for a second offense, and five thousand dollars for a third or subsequent offense. In addition to monetary penalties, the GRC may recommend that a custodian's employer impose appropriate disciplinary action.

ARTICLE VI. JUDICIAL REMEDIES (§ 47:1A-6)

Section 47:1A-6 also provides that a person denied access may institute a proceeding in the Superior Court to challenge the denial. The court may order the production of records, award reasonable attorney fees to a prevailing requester, and impose any appropriate sanctions. If the court determines that the denial was unreasonable, it must award reasonable attorney fees. The court may also impose civil penalties for knowing and willful violations on the same scale as the GRC.

The dual-track enforcement system — allowing requesters to choose between the GRC and the Superior Court — is a distinctive feature of OPRA. It provides flexibility and ensures that access to justice is not limited by the requester's financial resources or willingness to litigate.

ARTICLE VII. COMMON LAW RIGHT OF ACCESS

OPRA preserves the common law right of access that existed before the statute was enacted. Section 47:1A-8 expressly states that OPRA does not diminish any rights of access that existed under the common law. The common law right of access requires a showing of "interest" by the requester, but once established, it may provide broader access than OPRA in certain circumstances. For example, the common law right has been held to reach records that are excluded from OPRA's definition of "government record" (such as deliberative materials), provided the requester can demonstrate a sufficient interest.

This dual framework — statutory and common law — means that a requester who is denied access under OPRA may still seek access under the common law, potentially reaching categories of records that OPRA does not cover.''',
        'summary': 'New Jersey\'s OPRA (N.J.S.A. §§ 47:1A-1 through 47:1A-13) requires all government records to be readily accessible for inspection and copying. Requests must use an official form and identify specific records. Custodians must respond within seven business days. Copies cost no more than $0.75/page; inspection is free. Key exemptions include deliberative materials, attorney-client privileged records, criminal investigatory records, and personnel records (though salary and title are always public). The Government Records Council provides administrative adjudication with civil penalties up to $5,000 for willful violations. OPRA preserves the broader common law right of access.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NEW MEXICO — Inspection of Public Records Act (IPRA)
    # NMSA §§ 14-2-1 through 14-2-12
    # =========================================================================
    {
        'id': 'nm-public-records-statute',
        'citation': 'NMSA §§ 14-2-1–14-2-12',
        'title': 'New Mexico Inspection of Public Records Act (IPRA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NM',
        'source': 'prdb-built',
        'text': '''New Mexico Inspection of Public Records Act (IPRA)
NMSA §§ 14-2-1 through 14-2-12

ARTICLE I. LEGISLATIVE FINDINGS AND DEFINITIONS (§§ 14-2-1–14-2-3)

Section 14-2-1 declares the policy of the state: recognizing that a representative government is dependent upon an informed electorate, the intent of the Inspection of Public Records Act is to ensure that every person is permitted to inspect public records of the state. All public records are the property of the people of New Mexico, and the act shall be broadly construed to carry out this purpose.

Section 14-2-3 provides definitions. "Public records" means all documents, papers, letters, books, maps, tapes, photographs, recordings, and other materials, regardless of physical form or characteristics, that are used, created, received, maintained, or held by or on behalf of any public body and relate to public business. The definition is broad and format-neutral, encompassing electronic records, databases, emails, text messages, and social media content related to government business.

"Public body" means the state and all its branches, agencies, departments, commissions, councils, committees, and instrumentalities, as well as every county, municipality, district, and political subdivision, and any entity supported in whole or in part by public funds or authorized by law to spend public funds. This broad definition captures not only traditional government agencies but also quasi-governmental entities and organizations that receive public funding.

"Custodian" means any person who is responsible for the maintenance, care, or keeping of public records, regardless of whether the records are in the custodian's actual possession. This functional definition means that the obligation to respond to records requests extends to any official who has responsibility for the records, even if they have delegated physical custody to a subordinate.

ARTICLE II. RIGHT OF INSPECTION (§ 14-2-1)

Every person has the right to inspect the public records of the state. This right is unconditional and does not depend on the requester's citizenship, residency, or purpose. No public body may require a requester to state why the records are sought, and no request may be denied based on the requester's identity or intended use of the records.

The right of inspection extends to all records that meet the definition of "public records" unless a specific statutory exemption applies. The burden of establishing the applicability of an exemption rests on the public body, and any doubt is to be resolved in favor of disclosure.

ARTICLE III. REQUEST PROCEDURES AND RESPONSE TIMELINES (§ 14-2-8)

Section 14-2-8 establishes the procedures for requesting public records. A request may be made in writing or, at the discretion of the custodian, orally. Written requests are preferred because they create a record of the request and establish the starting date for the response timeline. The custodian must respond to a written request no later than fifteen calendar days after receipt.

Within the fifteen-day period, the custodian must either provide access to the records, provide a written explanation of the need for additional time (which may not exceed an additional fifteen calendar days), or deny the request in writing, stating the specific legal authority for the denial and advising the requester of the right to pursue legal remedies.

If the custodian neither provides the records nor responds within the fifteen-day period, the request is deemed denied. This constructive denial provision protects requesters against agencies that ignore requests rather than formally denying them.

New Mexico's fifteen-day response period is longer than many other states, which has drawn criticism from transparency advocates. However, the statute's provision allowing only one fifteen-day extension (for a maximum of thirty days total) provides a firm outer limit on the response time.

ARTICLE IV. FEES (§ 14-2-9)

Section 14-2-9 governs the fees that may be charged for providing copies of public records. The custodian may charge a reasonable fee for copying public records that does not exceed one dollar per page for standard-size copies. This statutory maximum is notably specific compared to the "actual cost" standards used in many other states. For non-standard copies (such as oversized documents, maps, or electronic media), the fee must reflect the actual cost of reproduction.

Inspection of records is free. No fee may be charged for the right to examine public records during regular business hours. Fees apply only when copies are requested. The custodian may require prepayment when the anticipated cost exceeds twenty-five dollars.

If the requested records exist in electronic form and the requester asks for an electronic copy, the custodian must provide the records in the electronic format in which they are maintained. The fee for electronic copies must reflect only the actual cost of the medium and any applicable labor costs for retrieval, and may not exceed the cost of paper copies for the same volume of information.

ARTICLE V. EXEMPTIONS (§ 14-2-1)

Section 14-2-1 provides that public records are subject to inspection unless they are exempted by law. New Mexico does not have a single, comprehensive list of exemptions within IPRA itself. Instead, exemptions are scattered throughout New Mexico law in various statutes governing specific categories of records. Major categories of records that are exempt from disclosure under various New Mexico statutes include:

Law enforcement records pertaining to open criminal investigations, including records that would reveal the identity of confidential informants, compromise ongoing investigations, or endanger the life or safety of any person. Once an investigation is complete and charges have been filed or the case has been closed, most investigative records become subject to disclosure.

Medical and health records of identifiable individuals, including mental health records and substance abuse treatment records. Records protected by the attorney-client privilege or the work product doctrine. Personnel records of public employees that contain medical information, evaluations, disciplinary actions, or other sensitive personal information. However, the name, title, position, salary, and dates of employment of public employees are public records under IPRA.

Tax return information and personal financial records submitted to government agencies. Records whose disclosure is prohibited by federal law, regulation, or court order. Letters of reference for employment, licensing, or permits. Records pertaining to the security of government facilities, including security plans, vulnerability assessments, and emergency response protocols.

The New Mexico Attorney General has issued guidance clarifying that exemptions must be specifically identified by statute and that blanket claims of confidentiality are insufficient. Each record or category of records must be evaluated individually, and the public body must identify the specific statutory provision that authorizes the withholding.

ARTICLE VI. SEGREGATION AND REDACTION

Although IPRA does not contain a specific segregation provision, the New Mexico Supreme Court has held that the statutory mandate of broad construction in favor of access requires public bodies to segregate exempt information from non-exempt information and to disclose the non-exempt portions. Agencies may not withhold entire documents based on the presence of some exempt material. This obligation extends to electronic records, where redaction may involve removing specific fields, entries, or portions of documents rather than withholding entire files.

ARTICLE VII. ENFORCEMENT AND REMEDIES (§§ 14-2-11–14-2-12)

Section 14-2-11 provides that any person denied access to public records may bring an action in the district court to compel disclosure. The court may examine the records in camera and must order disclosure if it determines that the records are not properly exempt. The proceedings are to be conducted on an expedited basis, with the court giving priority to the matter on its calendar.

Section 14-2-12 provides for the award of damages and attorney fees. If the court determines that the public body or custodian acted unreasonably in denying access, the court must award the requester actual damages, including reasonable attorney fees and costs. The statute also provides that the court may assess damages of up to one hundred dollars per day for each day that access was denied beginning on the sixteenth day after the written request was received (i.e., after the initial fifteen-day response period has expired).

This per-day damages provision is distinctive among state public records laws and provides a strong incentive for agencies to respond to requests promptly. The accumulation of daily damages creates an increasingly powerful motivation for compliance as the delay lengthens. Combined with the mandatory attorney fee award for unreasonable denials, the remedial structure makes IPRA one of the more requester-friendly public records statutes in the country.

Individual custodians who knowingly or willfully violate IPRA may be subject to disciplinary action and, in egregious cases, removal from office. The destruction or alteration of public records in anticipation of a records request constitutes a separate violation subject to additional penalties.''',
        'summary': 'New Mexico\'s IPRA (NMSA §§ 14-2-1 through 14-2-12) declares all public records to be the property of the people of New Mexico. Every person may inspect records regardless of purpose. Custodians must respond within fifteen calendar days, with one fifteen-day extension permitted. Copies cost no more than $1/page; inspection is free. Exemptions are scattered throughout state law rather than listed in IPRA itself. Courts must award attorney fees for unreasonable denials and may assess up to $100/day in damages starting on the sixteenth day after a request. The statute is construed broadly in favor of access.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NORTH CAROLINA — Public Records Law
    # N.C.G.S. §§ 132-1 through 132-10
    # =========================================================================
    {
        'id': 'nc-public-records-statute',
        'citation': 'N.C.G.S. §§ 132-1–132-10',
        'title': 'North Carolina Public Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'NC',
        'source': 'prdb-built',
        'text': '''North Carolina Public Records Law
N.C.G.S. §§ 132-1 through 132-10

ARTICLE I. DEFINITIONS AND SCOPE (§ 132-1)

Section 132-1 defines "public record" broadly: "Public record" or "public records" includes all documents, papers, letters, maps, books, photographs, films, sound recordings, magnetic or other tapes, electronic data-processing records, artifacts, or other documentary material, regardless of physical form or characteristics, made or received pursuant to law or ordinance in connection with the transaction of public business by any agency of North Carolina government or its subdivisions.

"Agency of North Carolina government or its subdivisions" includes every public office, public officer, or official (state or local, elected or appointed), institution, board, commission, bureau, council, department, authority, or other unit of government of the state or of any county, unit, special district, or other political subdivision of government. This encompasses state agencies, county and municipal governments, school boards, community colleges, the University of North Carolina system, and any other entity that exercises governmental authority.

The definition of "public record" is among the broadest in the nation. North Carolina courts have held that any document made or received in connection with public business is a public record, regardless of who created it, where it is stored, or what form it takes. This includes documents in the personal possession of public officials if they were made or received in connection with official business.

ARTICLE II. RIGHT OF ACCESS (§ 132-6)

Section 132-6 establishes the right of access. The public records and public information compiled by the agencies of North Carolina government or its subdivisions are the property of the people. Every custodian of public records must permit any record in the custodian's custody to be inspected and examined at reasonable times and under reasonable supervision by any person, and must furnish copies thereof upon payment of fees as prescribed by law.

The right of access is not limited to residents or citizens of North Carolina. Any person, regardless of identity, residency, or purpose, may inspect and obtain copies of public records. No custodian may require a requester to disclose the purpose of the request, and no request may be denied based on the identity or motivation of the requester.

North Carolina does not have a specific statutory deadline for responding to public records requests. The statute requires that access be provided at "reasonable times," which courts have interpreted to mean without unreasonable delay. The absence of a fixed deadline has been both praised (for flexibility in handling complex requests) and criticized (for allowing agencies to delay without technical violation). The North Carolina courts have held that what constitutes a reasonable time depends on the circumstances, including the volume and complexity of the records sought, the resources available to the custodian, and whether the records require review for exempt material. However, agencies may not use the lack of a deadline as an excuse for indefinite delay.

ARTICLE III. FEES (§ 132-6.2)

Section 132-6.2 governs fees for copies of public records. The custodian may charge a reasonable fee for copies. The fee must be based on the actual cost to the agency of providing the copies, including the cost of the medium and the actual cost of personnel time required to locate and make copies. The fee may not include charges for the overhead or administrative costs of maintaining the records or for the time spent reviewing records to determine whether they are exempt.

There is no charge for inspecting records. The right of inspection is free, and the custodian may not condition access upon the purchase of copies. If the cost of fulfilling a request is expected to be substantial, the custodian may require a deposit or prepayment.

Special service charges may apply when a request requires a significant amount of staff time for research, compilation, or preparation of records not routinely maintained in a readily accessible format. These charges must reflect actual costs and must be communicated to the requester in advance.

ARTICLE IV. EXEMPTIONS (§§ 132-1.1–132-1.12)

North Carolina's exemptions to the public records law are found in various sections of the General Statutes, both within Chapter 132 and throughout the code. Major categories include:

Section 132-1.1 provides that records relating to criminal investigations, intelligence information, and criminal intelligence information maintained by law enforcement agencies are not public records to the extent that disclosure would create a clear and specific danger to persons or would frustrate the purpose of the investigation. However, the basic law enforcement information — the time, date, location, and nature of a reported crime — is always a public record.

Section 132-1.2 protects confidential communications to public agencies, including trade secrets, confidential business information, and tax return information. The information must have been submitted under express or implied assurances of confidentiality.

Section 132-1.3 protects records related to the security of government facilities, including security plans, vulnerability assessments, building plans that reveal security measures, and response protocols.

Section 132-1.4 addresses law enforcement agency recordings, including body-worn camera and dashboard camera recordings. These recordings are not automatically public records and are subject to a specific disclosure framework that balances transparency with privacy concerns. A person whose image is captured may request disclosure, and agencies must disclose recordings under certain circumstances, but general public access requires a court order.

Section 132-1.7 protects the Social Security numbers and other personally identifying information of individuals from general disclosure. Section 132-1.10 addresses records related to public employee personnel actions and provides specific protections for certain categories of personnel information while making others (such as name, age, date of employment, current position, title, salary, office phone number, and date and amount of most recent salary increase) public records.

Other exemptions exist throughout North Carolina law for specific categories of records, including medical records, juvenile records, adoption records, student records, records of the State Bureau of Investigation, and records protected by federal law. The North Carolina Attorney General has published guidance listing the numerous statutory exemptions, which run to hundreds of specific provisions across the General Statutes.

ARTICLE V. ENFORCEMENT AND REMEDIES (§ 132-9)

Section 132-9 provides enforcement mechanisms. Any person who is denied access to public records may apply to the appropriate division of the General Court of Justice (the state trial court system) for an order compelling disclosure. The court may conduct an in camera examination of the records and must order production if it determines that the records are not exempt.

If the court orders disclosure, it may award reasonable attorney fees to the prevailing party. Unlike some states where attorney fees are mandatory for successful plaintiffs, North Carolina's provision is discretionary, allowing the court to consider the totality of the circumstances in deciding whether to award fees. Courts have awarded fees when agencies acted unreasonably or in bad faith but have declined to do so when the denial, while ultimately incorrect, was made in good faith.

Section 132-6 also provides that the custodian or any person who willfully and knowingly violates the public records law is subject to criminal penalties. This criminal enforcement mechanism, though rarely invoked, serves as an additional deterrent against willful violations, particularly the intentional destruction of records to avoid disclosure.

ARTICLE VI. RECORDS RETENTION AND PRESERVATION (§ 132-3)

Section 132-3 addresses the preservation of public records. No public official may destroy, sell, loan, or otherwise dispose of any public record without the consent of the Department of Natural and Cultural Resources (which administers the state's records management program). Records must be maintained in accordance with applicable retention schedules, and the purposeful destruction of records to avoid disclosure is a criminal offense.

The retention requirement extends to electronic records. Agencies must establish procedures for preserving electronic records that are subject to retention requirements, including email and other electronic communications. The deletion of electronic records in violation of retention schedules is treated the same as the physical destruction of paper records.

ARTICLE VII. ELECTRONIC RECORDS AND DATABASES

North Carolina's public records law applies to electronic records with the same force as to paper records. Databases maintained by government agencies are public records to the extent that they contain information made or received in connection with public business. Requesters may ask for electronic records in the format in which they are maintained, and agencies must provide them in that format when feasible. Agencies may not require requesters to accept paper printouts when the records exist in electronic form and the requester has asked for an electronic copy.

The application of the public records law to geographic information systems (GIS) data, property records databases, and other large datasets has been an area of particular activity in North Carolina. The state has developed policies to facilitate access to these resources while addressing legitimate concerns about the cost of data extraction and the protection of copyrighted software used to maintain the databases.''',
        'summary': 'North Carolina\'s Public Records Law (N.C.G.S. §§ 132-1 through 132-10) defines public records as the property of the people and provides one of the broadest definitions of "public record" in the nation. Any person may inspect records regardless of purpose; no statutory response deadline exists, but access must be provided without unreasonable delay. Fees are limited to actual costs. Exemptions cover criminal investigations, confidential business information, facility security records, and body-camera footage (subject to a specific framework). Attorney fees are discretionary. Willful violations carry criminal penalties. Records destruction requires approval from the Department of Natural and Cultural Resources.',
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
