#!/usr/bin/env python3
"""Build state public records statute documents for TN, UT, VT, VA, WA, WV, WI, WY."""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

DOCUMENTS = [
    # =========================================================================
    # TENNESSEE
    # Tennessee Public Records Act, Tenn. Code §§ 10-7-501 through 10-7-512
    # =========================================================================
    {
        'id': 'tn-statute-public-records-act',
        'citation': 'Tenn. Code §§ 10-7-501 through 10-7-512',
        'title': 'Tennessee Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'TN',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Tennessee\'s Public Records Act establishes that all state, county, and municipal records are open for public inspection unless specifically exempted by statute. The Act broadly defines public records, mandates prompt responses, and provides for judicial enforcement with mandatory attorney\'s fees for prevailing requesters.',
        'text': '''Tennessee Public Records Act
Tenn. Code Ann. §§ 10-7-501 through 10-7-512

OVERVIEW AND PURPOSE

The Tennessee Public Records Act declares that all state, county, and municipal records are open for personal inspection by any citizen of Tennessee. The statute reflects a longstanding legislative judgment that public business should be conducted openly and that citizens have a right to examine and copy records documenting government operations. The Tennessee Supreme Court has described the Act as creating a "broad right of access" that must be construed liberally in favor of disclosure.

The Act applies to all branches and levels of state and local government, including executive agencies, legislative offices, courts, municipalities, counties, school districts, utility districts, and other governmental entities. Any entity performing a governmental function or receiving public funds may be subject to the Act's requirements.

DEFINITION OF PUBLIC RECORD

Under Section 10-7-503, "public record" is defined broadly to include all documents, papers, letters, maps, books, photographs, microfilms, electronic data processing files, and other material made or received pursuant to law or ordinance or in connection with the transaction of official business by any governmental agency. The definition is intentionally expansive and encompasses virtually any recorded information that a government entity creates, receives, or maintains in connection with its official functions.

The format of the record does not affect its status. Paper documents, electronic files, emails, text messages, audio recordings, video recordings, database records, and social media content maintained by a government entity all qualify as public records if they relate to official business. The Act focuses on the nature and purpose of the information rather than the physical medium in which it is stored.

Records need not be "final" to be public. Drafts, working papers, and internal memoranda are generally public records unless they fall within a specific statutory exemption. The Act does not contain a general deliberative process privilege or a work-product exemption for non-legal materials.

CITIZEN ACCESS RIGHTS

Any citizen of Tennessee may inspect and copy public records. The Act uses the term "citizen" rather than "person," which Tennessee courts have interpreted to include residents of the state. Federal courts and the Tennessee Attorney General's Office have addressed whether the Act extends to non-residents, with varying results depending on the context.

A requester is not required to state a reason for requesting records. The purpose for which a citizen seeks access to public records is generally irrelevant to whether access must be granted. An agency may not deny a request based on the requester's intended use of the records, except in narrow circumstances specified by statute (such as commercial use of certain categories of records).

Requests may be made orally or in writing. The Act does not require written requests, though agencies may ask requesters to put requests in writing for administrative clarity. An agency may not refuse to acknowledge or process an oral request.

RESPONSE REQUIREMENTS

Tennessee law requires that agencies make records available "promptly." The statute does not impose a specific numerical deadline measured in days, but Tennessee courts have interpreted "promptly" to require production within a reasonable time given the nature and volume of the request. Unreasonable delay constitutes a constructive denial that can be challenged in court.

The Office of Open Records Counsel, established within the Tennessee Comptroller's Office, provides guidance on response times and has recommended that agencies respond to straightforward requests within seven business days where possible. However, this guidance is advisory rather than mandatory.

When an agency determines that a record is exempt from disclosure, it must specify the legal basis for the withholding. A bare assertion that a record is "confidential" or "exempt" without citation to a specific statutory provision is insufficient under Tennessee law.

FEES AND COSTS

The Act authorizes agencies to charge for the costs of reproducing records but prohibits charges designed to discourage requests. Charges must reflect the actual cost of duplication, including the cost of the medium (paper, disc, etc.) and the labor cost of locating, retrieving, and copying the records.

Labor charges for locating and retrieving records are permissible, but agencies may not charge for time spent reviewing records for exempt material. The distinction between retrieval costs (chargeable) and review costs (not chargeable) has been a recurring issue in Tennessee records litigation.

Agencies must provide an estimate of costs before fulfilling a request if the costs exceed a threshold amount. The requester has the opportunity to narrow or modify the request to reduce costs.

Inspection of records in the agency's offices is generally available at no cost. The right to inspect is distinct from the right to obtain copies, and inspection fees are generally not permissible unless the agency can demonstrate extraordinary circumstances.

EXEMPTIONS AND CONFIDENTIAL RECORDS

Tennessee's exemptions to the Public Records Act are scattered throughout the Tennessee Code rather than consolidated in a single list. Section 10-7-504 contains many of the most frequently invoked exemptions, but additional confidentiality provisions appear in dozens of other chapters and titles.

Key categories of exempt records include:

Medical records and individually identifiable health information held by public health agencies and hospitals are confidential under Section 10-7-504(a)(1). This exemption protects patient-specific information but does not extend to aggregate health data, facility inspection reports, or administrative records of health agencies.

Law enforcement investigative records are exempt to the extent that disclosure would reveal confidential informants, compromise ongoing investigations, endanger individuals, or interfere with pending prosecutions under Section 10-7-504(a)(2). This exemption is harm-based rather than categorical. Once an investigation concludes and no prosecution is pending, the harm rationale may no longer apply.

Personnel records of public employees have limited confidentiality protections. Basic employment information including name, position, salary, and dates of employment is public. Performance evaluations, disciplinary records, and similar materials have been the subject of significant litigation, with Tennessee courts generally holding that records reflecting how a public employee performs official duties are public.

Records containing Social Security numbers, dates of birth, and similar personal identifiers may be redacted before disclosure under provisions added in later amendments to the Act.

Student records are protected under both federal law (FERPA) and state provisions.

Certain records related to security plans, vulnerability assessments, and emergency response protocols are exempt under post-2001 amendments.

Attorney-client privileged communications between a government entity and its legal counsel are exempt from disclosure under Section 10-7-504(a)(1). Work product prepared by government attorneys in connection with pending or anticipated litigation is also protected. The privilege belongs to the governmental entity, not to the individual attorney.

Trade secrets and proprietary business information submitted to government agencies under a promise of confidentiality may be exempt, though Tennessee courts apply this exemption narrowly and require the agency to demonstrate that the information meets the legal definition of a trade secret.

All exemptions are construed strictly against the government entity claiming them. The burden of justifying nondisclosure rests with the agency, and any ambiguity is resolved in favor of access.

JUDICIAL ENFORCEMENT

Tennessee does not have an administrative appeal mechanism for denied records requests. A requester whose request is denied or constructively denied through unreasonable delay must file suit in chancery court or circuit court in the county where the records are located or where the agency's principal office is situated.

Courts review records denial de novo, meaning the court makes an independent determination of whether the records are exempt rather than deferring to the agency's judgment. In camera inspection of disputed records is available and commonly used.

Under Section 10-7-505(g), a court that finds an agency wrongfully withheld records must award reasonable attorney's fees and litigation costs to the prevailing requester. This mandatory fee-shifting provision is one of the strongest enforcement mechanisms in state public records law and creates a significant incentive for agencies to comply with the Act. The court has discretion to award additional sanctions for willful violations.

The Act also provides for injunctive relief. A court may order production of records, enjoin ongoing violations, and impose penalties for contempt.

OFFICE OF OPEN RECORDS COUNSEL

Tennessee created the Office of Open Records Counsel (OORC) within the Comptroller of the Treasury's office to provide informal dispute resolution and guidance on public records issues. The OORC is authorized to receive complaints, mediate disputes, issue advisory opinions, and provide training to government officials and the public.

The OORC's opinions are advisory and not binding on agencies or courts. However, they provide useful guidance on recurring issues and represent the state's considered interpretation of the Act. An agency that follows OORC guidance in good faith may be better positioned to defend its actions in court.

The OORC may facilitate resolution of disputes without litigation, reducing costs for both requesters and agencies. Participation in OORC mediation is voluntary and does not waive either party's right to pursue judicial relief.

RECORDS MANAGEMENT AND RETENTION

The Act intersects with Tennessee's records management statutes, which require agencies to maintain records retention schedules approved by the Public Records Commission. An agency may not destroy records that are the subject of a pending public records request, and premature destruction of records may give rise to adverse inferences in litigation.

Electronic records are subject to the same retention requirements as paper records. Agencies must maintain electronic systems capable of producing records in a format that is usable and accessible.

SPECIAL PROVISIONS

The Act contains provisions addressing specific categories of records and requesters. These include provisions governing access to vital records (birth and death certificates), voter registration records, property tax records, and court records. Some of these provisions impose additional requirements or different fee structures.

The Act also addresses the use of public records for commercial purposes. Agencies may impose restrictions on the bulk commercial use of certain categories of records, though they may not refuse individual inspection or copying based on the requester's commercial purpose.

Records of public meetings and minutes of governmental bodies are public under both the Public Records Act and Tennessee's Open Meetings Act (the "Sunshine Law"), which operates as a complementary transparency statute.
''',
    },

    # =========================================================================
    # UTAH
    # Government Records Access and Management Act (GRAMA)
    # Utah Code §§ 63G-2-101 through 63G-2-901
    # =========================================================================
    {
        'id': 'ut-statute-grama',
        'citation': 'Utah Code §§ 63G-2-101 through 63G-2-901',
        'title': 'Government Records Access and Management Act (GRAMA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'UT',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Utah\'s GRAMA creates a tiered classification system for government records (public, private, controlled, protected) and establishes detailed procedures for requesting, classifying, and appealing records decisions through an administrative process culminating in review by the State Records Committee.',
        'text': '''Government Records Access and Management Act (GRAMA)
Utah Code Ann. §§ 63G-2-101 through 63G-2-901

OVERVIEW AND PURPOSE

The Government Records Access and Management Act, commonly known as GRAMA, is Utah's comprehensive public records law. Enacted in 1991, GRAMA replaced Utah's prior Information Practices Act and established a detailed framework for classifying, managing, and providing access to government records. The Act declares that the public's right of access to information concerning the conduct of the public's business is a fundamental right protected by the Utah Constitution.

GRAMA is distinctive among state public records laws for its record classification system, which assigns records to one of several access categories rather than using a simple public/exempt dichotomy. This classification approach provides more granular control over access but also introduces complexity not present in most other states' statutes.

GRAMA applies to all state agencies, political subdivisions (counties, cities, towns, school districts, special districts), the legislature, and the judiciary. It governs records created, received, or maintained by these entities in connection with the transaction of public business.

RECORD CLASSIFICATIONS

GRAMA establishes four primary record classifications:

Public records (Section 63G-2-301) are records that are available for inspection and copying by any person. The Act designates numerous categories of records as public, including the names, gender, gross compensation, job title, job description, business address, business email, business telephone number, and dates of employment of current and former employees. Meeting minutes, proposed and adopted budgets, audit reports, contracts, and policy documents are also public.

Private records (Section 63G-2-302) are records that the governmental entity must keep confidential and may disclose only to the subject of the record, the subject's authorized representative, or other persons or entities authorized by law. Private records include personnel files, medical records, student records, and certain records relating to eligibility for social services programs. The private classification protects individual privacy while allowing the subject to access their own records.

Controlled records (Section 63G-2-304) are records that are accessible only to the subject of the record and authorized government personnel. Medical, psychiatric, and psychological records of individuals in the custody of a governmental entity are classified as controlled. This classification serves a therapeutic purpose by preventing individuals from accessing records that mental health professionals determine could be harmful to the individual's well-being, while protecting the records from public access.

Protected records (Section 63G-2-305) are records that the governmental entity may not disclose unless authorized by specific statutory provisions. Protected classifications apply to trade secrets, records the disclosure of which would jeopardize the security of governmental property, records relating to pending or reasonably anticipated litigation, and certain law enforcement records. The protected classification is the most commonly litigated area of GRAMA.

REQUESTS AND RESPONSE PROCEDURES

A person requesting records under GRAMA must submit a written request that describes the records sought with reasonable specificity. The requester must provide sufficient detail to allow the governmental entity to identify and locate the records. GRAMA does not require the requester to identify records by their filing system designation or to use technical terminology, but the request must be specific enough that a reasonable search can be conducted.

The governmental entity must respond within ten business days of receiving a properly submitted request. The response must either grant the request, deny the request with a written explanation citing the specific GRAMA provision authorizing nondisclosure, or request an extension of time. Extensions may not exceed an additional ten business days without the requester's consent, except in extraordinary circumstances.

If a record contains both public and non-public information, the entity must segregate the non-public portions and provide the remainder. Redaction of exempt material is required rather than wholesale withholding of records that contain some exempt information.

FEES

Governmental entities may charge a reasonable fee to cover the actual cost of providing records. The fee may include the cost of staff time to search for, compile, and copy the requested records. However, the fee may not exceed the actual cost, and the first quarter hour of staff time is free of charge.

For electronic records, the entity may charge for the cost of the storage medium (disc, drive, etc.) and the programming time necessary to extract or compile the records from a database, provided that the programming is not available as a standard function of the entity's existing system.

Fee waivers are available when the requester demonstrates that release of the information primarily benefits the public rather than the individual requester.

ADMINISTRATIVE APPEALS

GRAMA provides a multi-tier administrative appeal process that distinguishes it from many other states' public records laws.

The first level of appeal is to the chief administrative officer of the governmental entity (or a designee). This appeal must be filed within 30 days of the denial. The chief administrative officer must issue a decision within ten business days, either affirming, reversing, or amending the initial determination.

If the requester is unsatisfied with the chief administrative officer's decision, the second level of appeal is to the State Records Committee (for state agency records) or a local appeals board (for records of political subdivisions). The State Records Committee is an independent body composed of members appointed by the Governor, the Legislature, and other officials. The Committee holds hearings, reviews records in camera, and issues written orders. Committee proceedings are quasi-judicial in nature.

Appeals to the State Records Committee must be filed within 30 days of the chief administrative officer's decision. The Committee must hold a hearing within a reasonable time and issue a written decision. The Committee has authority to order disclosure of records, uphold denials, and award attorney's fees in certain circumstances.

Judicial review of State Records Committee orders is available in district court. The court reviews the Committee's factual findings under a substantial evidence standard and its legal conclusions de novo. Either the requester or the governmental entity may seek judicial review.

PENALTIES AND ENFORCEMENT

GRAMA includes several enforcement provisions. A governmental entity that fails to respond to a records request within the statutory deadlines is deemed to have denied the request, entitling the requester to pursue an appeal.

The State Records Committee may impose a civil penalty of up to $500 for each violation against a governmental entity that intentionally or in bad faith violates GRAMA. The Committee may also award reasonable attorney's fees and costs to a prevailing requester.

A public employee who intentionally discloses a private, controlled, or protected record in violation of GRAMA is subject to criminal prosecution as a class B misdemeanor. This criminal penalty provision applies to affirmative wrongful disclosures rather than good-faith access decisions.

Courts reviewing GRAMA cases may award attorney's fees to a prevailing requester and may issue injunctive relief ordering production of records. The court may also impose sanctions for bad faith withholding.

RECORDS MANAGEMENT

GRAMA establishes records management requirements that complement the access provisions. Governmental entities must designate a records officer responsible for implementing records management policies. The State Archives coordinates statewide records management and provides guidance, training, and retention schedules.

Records retention schedules must be adopted by each governmental entity and approved by the State Records Committee. Records may not be destroyed except in accordance with approved retention schedules. An entity may not destroy records that are the subject of a pending records request, pending litigation, or a litigation hold.

Electronic records are subject to the same management requirements as paper records. Entities must maintain electronic recordkeeping systems that preserve the integrity, authenticity, and reliability of records throughout their retention period.

SPECIAL PROVISIONS

GRAMA contains provisions addressing specific categories of records, including records of the legislature, records of the judiciary, records relating to legislative audits, and records of higher education institutions. Some of these provisions modify the standard classification and access rules.

The Act also addresses records shared between governmental entities. When one entity shares records with another, the receiving entity generally must maintain the same classification that applied in the originating entity.

GRAMA interacts with Utah's Open and Public Meetings Act, which requires governmental bodies to keep minutes and recordings of public meetings. These records are classified as public under both statutes.
''',
    },

    # =========================================================================
    # VERMONT
    # Vermont Public Records Act, 1 V.S.A. §§ 315 through 320
    # =========================================================================
    {
        'id': 'vt-statute-public-records-act',
        'citation': '1 V.S.A. §§ 315 through 320',
        'title': 'Vermont Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'VT',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Vermont\'s Public Records Act establishes a strong presumption of access to records created or acquired by government agencies, with enumerated exemptions that must be strictly construed. The Act provides for administrative appeal to the agency head and judicial enforcement in superior court with attorney\'s fee shifting.',
        'text': '''Vermont Public Records Act
1 V.S.A. §§ 315 through 320

OVERVIEW AND PURPOSE

Vermont's Public Records Act declares that all public records are available for inspection and copying by any person, and that free and open examination of records is in the public interest. The statute reflects Vermont's commitment to transparent government and is construed liberally in favor of disclosure. The Vermont Supreme Court has repeatedly held that exemptions to the Act must be strictly construed and that the burden of justifying nondisclosure rests entirely with the public agency.

The Act applies to any agency, department, board, commission, committee, branch, instrumentality, or authority of the State of Vermont, as well as to any political subdivision including counties, cities, towns, villages, school districts, and similar entities. The Act also applies to any entity that is supported primarily by public funds or that exercises governmental authority.

DEFINITION OF PUBLIC RECORD

Section 317(b) defines "public record" as any written or recorded information, regardless of physical form or characteristics, that is produced or acquired in the course of public agency business. The definition encompasses paper documents, electronic files, emails, databases, audio and video recordings, photographs, and any other tangible medium containing information related to government operations.

The definition is intentionally broad and focuses on the nexus between the record and public business rather than the form of the record. An email sent from a government employee's personal account relating to government business qualifies as a public record. Similarly, records stored on personal devices, cloud services, or third-party systems are public records if they relate to the transaction of public business.

Records need not be final documents to qualify. Drafts, notes, and preliminary materials are generally public records unless they fall within a specific exemption. Vermont does not recognize a general deliberative process exemption comparable to the federal FOIA exemption.

ACCESS RIGHTS AND PROCEDURES

Any person may request access to public records regardless of citizenship, residency, or stated purpose. Vermont's Act is notably broad in this regard, imposing no restrictions based on the requester's identity or motivation. A requester need not explain why records are sought, and the agency may not condition access on the requester's stated purpose except in narrow circumstances specified by statute.

Requests may be submitted in writing or orally. While the Act does not mandate written requests, agencies may request that complex or voluminous requests be put in writing to ensure accuracy and to establish a record of the request for tracking purposes.

The Act requires agencies to respond to requests within three business days of receipt. If the agency needs additional time to locate, retrieve, or review records, it must notify the requester within the initial three-day period and provide an estimated date of completion. The estimated completion date must be reasonable given the nature and scope of the request.

When an agency determines that records are exempt from disclosure, it must provide a written denial specifying the statutory exemption relied upon and explaining how the exemption applies to the requested records. A generic citation to an exemption category without explanation is insufficient.

FEES

Agencies may charge reasonable fees for the cost of providing copies of records. The fee must reflect actual costs and may include the cost of the copy medium and the staff time necessary to locate, retrieve, compile, and copy the records. The first two pages of copies are provided free of charge, and inspection of records in the agency's offices is free.

Agencies may not impose search fees or review fees that are designed to discourage requests. The Secretary of State establishes recommended fee schedules, and agencies that exceed these recommendations must justify their charges.

When a request will result in substantial costs, the agency must provide an estimate to the requester before proceeding. The requester may narrow the request to reduce costs or may agree to the estimate and proceed.

EXEMPTIONS

Section 317(c) contains Vermont's list of exemptions to the Public Records Act. These exemptions are exclusive — an agency may not withhold records under any authority not specifically enumerated in the statute. Exemptions are strictly construed in favor of disclosure.

Key exemptions include:

Records that are specifically designated as confidential by other provisions of Vermont law. This cross-referencing exemption incorporates confidentiality provisions scattered throughout the Vermont Statutes. The agency must identify the specific provision conferring confidentiality.

Personnel files and personal documents relating to individual employees, with the exception of name, position, salary, and similar basic employment information, which are public.

Records dealing with the detection and investigation of crime, but only to the extent that production would impair a pending investigation, endanger the safety of any person, or reveal confidential investigative techniques. This exemption is harm-based and does not categorically protect all law enforcement records.

Trade secrets, proprietary business information, and financial information submitted to a government agency under a promise or expectation of confidentiality. The agency must determine that the information qualifies as a trade secret under Vermont law.

Records related to labor relations and collective bargaining strategy, to the extent that premature disclosure would compromise the governmental entity's bargaining position.

Communications between a public agency and its legal counsel that are privileged under the attorney-client relationship. The privilege belongs to the governmental entity and may be waived by the entity.

Internal advisory communications made as part of the deliberative process, but only to the extent that they consist of opinions, recommendations, and policy discussions rather than factual information. Factual information contained in otherwise deliberative communications must be segregated and disclosed.

Records whose disclosure would constitute an unwarranted invasion of personal privacy. This exemption requires a balancing test between the public interest in disclosure and the individual's privacy interest. Vermont courts apply this exemption narrowly and have held that information about public employees' conduct in their official capacity is subject to reduced privacy expectations.

Test questions, scoring keys, and other examination instruments used for licensing, employment, or academic purposes.

Tax returns and tax-related information furnished in confidence.

SEGREGATION AND REDACTION

When a record contains both public and exempt information, the agency must redact the exempt portions and provide the remainder. Wholesale withholding of a document that contains some exempt material is not permitted unless the public and exempt portions are so intertwined that segregation is not feasible. The agency bears the burden of demonstrating that segregation is impractical.

ADMINISTRATIVE APPEAL

A requester who is denied access to records may appeal to the head of the agency that issued the denial. The appeal must be filed within 30 days of the denial. The agency head must respond within five business days with a written decision affirming, modifying, or reversing the initial denial. The decision must include a specific explanation of the legal basis for any continued withholding.

JUDICIAL REVIEW

If the administrative appeal is unsuccessful, the requester may file suit in the Superior Court of the county where the records are located. The court reviews the matter de novo, meaning it makes an independent determination without deference to the agency's classification decision. In camera inspection of disputed records is available and commonly used.

The court may order production of records, impose injunctive relief, and award attorney's fees and costs to a prevailing requester. Attorney's fees are discretionary rather than mandatory, but Vermont courts have awarded them in cases where the agency's withholding was unreasonable or lacked a good-faith basis.

A court may also award punitive damages in cases of willful or bad-faith violation of the Act. This provision is rarely invoked but provides an additional deterrent against deliberate noncompliance.

RECORDS MANAGEMENT

Vermont law requires governmental entities to establish records retention schedules and to preserve records for the periods specified in those schedules. Records may not be destroyed while they are the subject of a pending records request or pending litigation. The Vermont State Archives provides guidance on records management and retention.

Electronic records are subject to the same preservation and access requirements as paper records. Agencies must maintain electronic systems capable of producing records in usable formats upon request.

PUBLIC RECORDS LEGISLATIVE COMMITTEE

Vermont has established a Public Records Legislative Committee to study and make recommendations concerning the state's public records laws. The Committee reviews proposed exemptions, evaluates the operation of the Act, and recommends legislative changes. This oversight mechanism ensures ongoing legislative attention to the balance between transparency and confidentiality.
''',
    },

    # =========================================================================
    # VIRGINIA
    # Virginia Freedom of Information Act (VFOIA)
    # Va. Code §§ 2.2-3700 through 2.2-3714
    # =========================================================================
    {
        'id': 'va-statute-vfoia',
        'citation': 'Va. Code §§ 2.2-3700 through 2.2-3714',
        'title': 'Virginia Freedom of Information Act (VFOIA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'VA',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Virginia\'s Freedom of Information Act establishes the right of Virginia citizens (and media) to inspect and copy public records, with over 100 enumerated exemptions. VFOIA provides for rapid response timelines, advisory opinions from the FOIA Council, and judicial enforcement with mandatory attorney\'s fees.',
        'text': '''Virginia Freedom of Information Act (VFOIA)
Va. Code Ann. §§ 2.2-3700 through 2.2-3714

OVERVIEW AND PURPOSE

The Virginia Freedom of Information Act, commonly referred to as VFOIA, declares that all public records are presumed open and that any exemption from disclosure must be narrowly construed. The Act states that the affairs of government are not combative in nature and that free access to public records is fundamental to promoting an informed citizenry.

VFOIA applies to "public bodies," which include any legislative body, authority, board, bureau, commission, district, or agency of the Commonwealth of Virginia or any political subdivision, as well as municipal corporations, counties, school boards, and other governmental entities. The Act also applies to any organization, corporation, or agency in the Commonwealth supported wholly or principally by public funds.

Virginia's Act is notable for its extensive enumeration of exemptions — over 100 specific exemptions are codified, making it one of the most detailed (and most criticized) exemption schemes in the nation. Despite this breadth, the statute mandates that exemptions are discretionary unless specifically stated otherwise; an agency "may" withhold exempt records but is not required to.

STANDING AND ELIGIBILITY

VFOIA limits standing to request records to citizens of the Commonwealth of Virginia, representatives of newspapers and magazines with circulation in Virginia, and representatives of broadcast media licensed to serve Virginia. This citizenship limitation has been a subject of criticism and legal challenge, though Virginia courts have upheld it. Non-Virginia residents and out-of-state media organizations generally lack standing to invoke VFOIA.

A requester is not required to state a purpose for seeking records. The Act prohibits agencies from requiring requesters to disclose their reason for requesting records as a condition of access.

REQUEST AND RESPONSE PROCEDURES

VFOIA requires that records requests be made in writing, though the statute does not prescribe a particular format. Requests should identify the records sought with reasonable specificity. A request need not reference the Freedom of Information Act by name to invoke its protections.

Public bodies must respond to requests within five working days of receipt. The response must either provide the requested records, cite a specific legal exemption and provide a written explanation for withholding, or invoke an extension of no more than seven additional working days when the request involves an extraordinary volume of records or requires legal consultation. Additional time beyond the seven-day extension may be negotiated with the requester.

Failure to respond within the statutory deadline constitutes a violation of VFOIA and is deemed a denial of the request. The requester may then pursue remedies as if the request had been explicitly denied.

FEES AND COSTS

Public bodies may charge reasonable costs for responding to records requests. Charges may include the actual cost of searching for records, reviewing records for exempt material, supplying copies, and transmitting records. However, no charge may be made for the first two hours of search and review time if the requester asks for the records to be provided at no charge.

Charges must reflect actual costs and may not include overhead, profit, or administrative expenses unrelated to the specific request. Before incurring costs, the public body must provide a cost estimate to the requester, who may narrow the request or agree to the estimate.

The Act prohibits charges that are designed to discourage requests. If a public body's fee schedule is challenged, the body bears the burden of demonstrating that its charges are reasonable.

EXEMPTIONS

VFOIA contains an extensive array of exemptions organized in Section 2.2-3705.1 through 2.2-3705.8 by subject category. Despite their number, exemptions are discretionary unless the statute specifies that records "shall" be withheld. Key categories include:

Personnel records. Section 2.2-3705.1 permits withholding of certain personnel-related records, including applications for employment, performance evaluations, and disciplinary actions. However, name, position, salary, and date of hire are public for all public employees.

Scholastic records. Student records protected under FERPA and state privacy provisions may be withheld.

Law enforcement records. Section 2.2-3706 addresses records relating to criminal investigations, intelligence records, and records that could endanger the safety of law enforcement personnel. Completed investigation files are generally subject to disclosure, subject to specific redactions for exempt material.

Legal records. Communications between a public body and its legal counsel involving specific legal matters requiring the provision of legal advice are exempt under the attorney-client privilege exemption.

Trade secrets and proprietary information. Business records submitted to a public body that contain trade secrets or proprietary information may be withheld if disclosure would cause competitive harm.

Records relating to the security of government facilities, including vulnerability assessments, security plans, and critical infrastructure information.

Records relating to real estate transactions, specifically appraisals and negotiations for acquisition of property, until the transaction is completed.

Information technology records, including security plans, disaster recovery plans, and network architecture documents, to the extent that disclosure would compromise the security of information systems.

Tax records. Individual tax returns and related information are exempt from disclosure.

Health records. Medical and mental health records of individuals are exempt, subject to the individual's right of access to their own records.

All exemptions must be invoked with specificity. A public body that denies a request must identify the specific Code section authorizing the withholding and must explain how the exemption applies to the particular records at issue.

SEGREGATION REQUIREMENT

When a record contains both public and exempt information, the public body must disclose the non-exempt portions after redacting the exempt material. The duty to segregate is mandatory, and wholesale withholding of records containing some exempt material is prohibited unless the public and exempt portions are inextricably intertwined.

VIRGINIA FREEDOM OF INFORMATION ADVISORY COUNCIL

Virginia established the Freedom of Information Advisory Council to provide guidance on VFOIA compliance. The Council issues advisory opinions on the application of the Act, provides training to public bodies and the public, and recommends legislative changes. Advisory opinions are not legally binding but are persuasive authority and provide practical guidance on recurring issues.

Any person may request an advisory opinion from the Council. The Council endeavors to respond within ten working days. Public bodies that follow a Council advisory opinion in good faith are shielded from certain penalties.

ENFORCEMENT AND REMEDIES

A requester who believes a public body has violated VFOIA may file a petition for mandamus or injunction in the general district court or circuit court of the jurisdiction where the records are located. The proceeding is expedited and given priority on the court's docket.

If the court finds that the public body violated VFOIA, it must award the requester reasonable attorney's fees and costs. This mandatory fee-shifting provision is a significant enforcement tool and incentivizes compliance.

The court may also impose a civil penalty of up to $500 for each violation. For subsequent violations within one year, the penalty may increase to up to $2,000. In cases involving bad faith or willful and knowing violations, the court may impose higher penalties.

The Act also provides for petition by a public body seeking a judicial determination that records may be withheld. This provision allows public bodies to obtain pre-disclosure judicial review when they are uncertain whether records are exempt.

RECORDS MANAGEMENT

Virginia's Public Records Act (a separate statute from VFOIA) governs records management and retention. Public bodies must maintain records retention schedules approved by the Library of Virginia and may not destroy records except in accordance with those schedules. Records that are the subject of pending FOIA requests, pending litigation, or audit holds may not be destroyed regardless of their retention schedule status.

Electronic records are subject to the same retention and access requirements as paper records. The Library of Virginia provides guidance on electronic records management.
''',
    },

    # =========================================================================
    # WASHINGTON
    # Washington Public Records Act (PRA)
    # RCW Ch. 42.56
    # =========================================================================
    {
        'id': 'wa-statute-pra',
        'citation': 'RCW Ch. 42.56',
        'title': 'Washington Public Records Act (PRA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'WA',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Washington\'s Public Records Act, originally enacted as a citizen initiative, establishes one of the nation\'s strongest rights of public access. The PRA creates a broad definition of public records, imposes strict response timelines, mandates per-day penalties for wrongful withholding, and requires attorney\'s fees for prevailing requesters.',
        'text': '''Washington Public Records Act (PRA)
RCW Chapter 42.56

OVERVIEW AND PURPOSE

Washington's Public Records Act was originally enacted in 1972 as Initiative 276, a citizen-sponsored ballot measure reflecting public demand for government transparency. Now codified in Chapter 42.56 of the Revised Code of Washington, the PRA establishes one of the strongest and most requester-friendly public records regimes in the United States. The Act declares that the people of Washington "insist on remaining informed so that they may maintain control over the instruments of government they have created."

The PRA is a "strongly worded mandate for broad disclosure of public records" (as described by the Washington Supreme Court) and must be liberally construed to promote access. Exemptions are narrowly construed, and any ambiguity is resolved in favor of disclosure. The people retain the right to amend the PRA through the initiative process, and the Legislature may not add exemptions except by a two-thirds supermajority vote, a constitutional protection unique to Washington.

The PRA applies to all state agencies, local agencies, and every office, department, division, bureau, board, commission, and committee of state and local government. It also applies to quasi-governmental entities and any entity created by statute to perform governmental functions.

DEFINITION OF PUBLIC RECORD

A "public record" under the PRA includes any writing containing information relating to the conduct of government or the performance of any governmental or proprietary function, prepared, owned, used, or retained by any state or local agency, regardless of physical form or characteristics. The definition encompasses paper documents, electronic files, emails, text messages, voicemails, videos, photographs, databases, spreadsheets, metadata, and any other format.

The definition is one of the broadest in the nation. Records need not be "final" to be public — drafts, notes, and working papers are public records. Records on personal devices or accounts are public if they relate to government business. The focus is on the content and its relationship to governmental functions rather than the location or medium of storage.

ACCESS RIGHTS

Any person, regardless of citizenship, residency, or stated purpose, may request public records. Washington places no restrictions on who may make requests or why. An agency may not require a requester to identify themselves (though requesters who want records mailed or emailed must provide contact information). An agency may not inquire into the requester's purpose except to the extent necessary to determine whether a specific exemption applies.

REQUEST AND RESPONSE PROCEDURES

Requests should be made in writing, though the Act does not categorically require written requests. Agencies typically provide request forms but may not require their use.

Upon receiving a request, an agency must respond within five business days. The response must either provide the records, provide a reasonable estimate of the time needed to fulfill the request, or deny the request and cite the specific exemption authorizing withholding. If an agency fails to respond within five business days, the request is deemed denied.

For large or complex requests, agencies must provide records on an installment basis as they are located and reviewed rather than withholding all records until the entire request is processed. This installment production requirement prevents agencies from using request complexity as a delay tactic.

Agencies must provide the "fullest assistance" to requesters and must create the "most timely possible" response. These statutory mandates have been interpreted by Washington courts to impose an affirmative obligation on agencies to help requesters obtain records efficiently.

FEES

Agencies may charge for the actual cost of providing copies of records, including the per-page cost of photocopies and the cost of electronic media. Default copy charges are established by statute, though agencies may adopt their own fee schedules that do not exceed actual costs.

In 2017, the Legislature enacted reforms clarifying fee authority. Agencies may charge for customized electronic access services only if those services are specifically authorized by their adopted fee schedules. Agencies must provide a summary of applicable charges before fulfilling a request.

Inspection of records in the agency's offices is free of charge. The right to inspect is independent of the right to obtain copies, and agencies may not charge inspection fees.

EXEMPTIONS

The PRA's exemptions are scattered across Chapter 42.56 and numerous other chapters of the Revised Code of Washington. Key categories include:

Personal information in files maintained for public employees to the extent that disclosure would violate their right to privacy. However, basic employment information (name, position, salary, dates of employment) is public. The privacy exemption requires a balancing test weighing the individual's privacy interest against the public interest in disclosure.

Law enforcement investigative records, including records of ongoing investigations where disclosure would impede the investigation, compromise confidential informants, or endanger any person. Completed investigation files are generally public, subject to specific redactions.

Attorney-client privileged communications and attorney work product relating to pending or anticipated litigation.

Real estate appraisals and negotiations until the transaction is completed.

Trade secrets, proprietary information, and financial data submitted to agencies under a promise of confidentiality.

Certain security-related records, including vulnerability assessments, security plans, and critical infrastructure information.

Tax return information and individual financial records.

Medical and health records of individuals.

Student records protected under FERPA.

The legislature may not create new exemptions except by a two-thirds supermajority vote of each chamber, reflecting the initiative's original intent to make exemptions difficult to enact. Each new exemption must include a statement of the public interest served by the exemption.

PENALTIES AND ENFORCEMENT

The PRA's enforcement provisions are among the most powerful in the nation. A requester who prevails in court against an agency that wrongfully withheld records is entitled to:

Mandatory attorney's fees and costs. The court must award reasonable attorney's fees and all costs to a prevailing requester. This mandatory fee-shifting provision is a central enforcement mechanism.

Per-day penalties. The court must impose a penalty of between $5 and $100 per day for each record wrongfully withheld, from the date of the request until the date the records are produced. This per-day penalty can result in substantial damages for prolonged withholding and creates a strong financial incentive for agencies to produce records promptly.

Injunctive relief. Courts may order production of records and enjoin ongoing violations.

The combination of mandatory attorney's fees and per-day penalties makes the Washington PRA one of the most heavily enforced public records statutes in the country. Agencies face significant financial exposure for noncompliance.

JUDICIAL REVIEW

A requester whose request is denied may file suit in superior court. Washington does not have an administrative appeal process for denied records requests; the sole remedy is judicial action.

The court reviews the matter de novo and may inspect disputed records in camera. The agency bears the burden of proving that an exemption applies. The court must issue a written decision specifying its findings and conclusions.

Washington courts have developed an extensive body of case law interpreting the PRA, and the Washington Supreme Court has been consistently protective of the public's access rights. The Court has rejected attempts to create implied exemptions, common-law exemptions, or judicial exemptions not grounded in the statute.

MODEL RULES

The Attorney General's Office issues model rules for PRA compliance. These rules provide guidance on processing requests, calculating fees, and applying exemptions. While not binding on local agencies, the model rules are widely adopted and serve as a benchmark for reasonable agency practices.

OPEN GOVERNMENT OMBUDSPERSON

Washington has established an Office of the Open Government Ombudsperson to provide informal assistance to both requesters and agencies. The Ombudsperson can mediate disputes, provide training, and issue recommendations. The Ombudsperson's recommendations are advisory but serve as a non-litigation dispute resolution mechanism.

RECORDS MANAGEMENT

Washington's records management statutes require agencies to maintain records retention schedules approved by the State Archivist. Records may not be destroyed except in accordance with approved schedules, and agencies may not destroy records that are the subject of pending requests or litigation holds.
''',
    },

    # =========================================================================
    # WEST VIRGINIA
    # West Virginia Freedom of Information Act
    # W. Va. Code §§ 29B-1-1 through 29B-1-7
    # =========================================================================
    {
        'id': 'wv-statute-foia',
        'citation': 'W. Va. Code §§ 29B-1-1 through 29B-1-7',
        'title': 'West Virginia Freedom of Information Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'WV',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'West Virginia\'s Freedom of Information Act establishes public access to records of all public bodies, with enumerated exemptions. The Act provides for a five-day response deadline, administrative appeal, and judicial review with discretionary attorney\'s fees.',
        'text': '''West Virginia Freedom of Information Act
W. Va. Code §§ 29B-1-1 through 29B-1-7

OVERVIEW AND PURPOSE

West Virginia's Freedom of Information Act declares that all public records are the property of the citizens of West Virginia and that the full and complete disclosure of public records is fundamental to the democratic process. The Act establishes a strong presumption that government records are open and accessible, and it mandates that exemptions be construed narrowly in favor of disclosure.

The Act applies to every "public body," defined to include every state officer, agency, department, including the Legislature and the Judiciary, county and municipal governing bodies, boards, bureaus, commissions, agencies, and authorities. Political subdivisions, school boards, and special districts are included. The term also encompasses any organization or agency supported in whole or in part by public funds or that expends public funds.

DEFINITION OF PUBLIC RECORD

"Public record" is defined as any writing containing information relating to the conduct of the public's business, prepared, owned, and retained by a public body. The term "writing" includes handwriting, typewriting, printing, photostating, photographing, transmitting by electronic mail or facsimile, and every other means of recording upon any tangible thing any form of communication or representation, including letters, words, pictures, sounds, or symbols, or any combination thereof.

The definition encompasses records in all formats, including electronic records, emails, text messages, databases, audio and video recordings, and social media content. The focus is on the record's connection to public business, not its physical form or location.

ACCESS RIGHTS

Any person has the right to inspect or copy public records of a public body in West Virginia. The Act uses the term "person" rather than "citizen," extending access rights to any individual regardless of residence. The requester need not provide a reason for seeking records, and the public body may not require disclosure of the requester's purpose as a condition of access.

REQUEST AND RESPONSE PROCEDURES

Requests may be made orally or in writing. The Act does not mandate written requests, though agencies may prefer written requests for complex or voluminous matters to ensure clarity and accountability.

A public body must respond to a records request within five business days. The response must either provide access to the records, deny the request with a written explanation citing the specific statutory exemption, or request additional time if the request requires an extraordinary amount of time to process. Any extension must be for a reasonable period and must be communicated to the requester in writing.

Failure to respond within the five-day period is treated as a denial of the request, and the requester may proceed with administrative or judicial remedies.

When records are denied, the written response must identify the specific exemption relied upon and explain its application to the requested records. Generic or conclusory denials are insufficient.

FEES

Public bodies may charge fees reflecting the actual cost of searching for and copying records. Fees must be reasonable and may not exceed the actual cost to the public body. The Act does not establish a specific fee schedule but requires that charges reflect actual costs.

Inspection of records at the public body's offices is generally free of charge. The right to inspect records is distinct from the right to obtain copies, and no fee may be charged for reviewing records in person absent extraordinary circumstances.

If a request will result in substantial costs, the public body should provide an estimate to the requester before proceeding. The requester may narrow the request to reduce costs.

EXEMPTIONS

Section 29B-1-4 enumerates the categories of records exempt from disclosure. West Virginia's exemption list is more concise than those of some other states, and all exemptions are construed strictly against nondisclosure. Key exemptions include:

Trade secrets and commercial or financial information obtained from a person that is privileged or confidential. The public body must determine that the information meets the legal definition of a trade secret or that disclosure would cause competitive harm to the entity that submitted the information.

Information of a personal nature such as that kept in a personal, medical, or similar file, if public disclosure would constitute an unreasonable invasion of privacy. This exemption requires a balancing test weighing the public interest in disclosure against the individual's privacy interest. Information about public employees' performance of their official duties is subject to reduced privacy expectations.

Test questions, scoring keys, and other examination data used to administer licensing examinations, employment examinations, or academic examinations.

Records of law enforcement agencies that deal with the detection and investigation of crime, to the extent that production would impede law enforcement, deprive a person of a fair trial, constitute an unwarranted invasion of privacy, disclose the identity of a confidential informant, disclose investigative techniques, or endanger the safety of law enforcement personnel. This exemption is harm-based and requires the agency to articulate specific harm rather than claiming a blanket exemption.

Internal memoranda or letters received or prepared by a public body in connection with a judicial, quasi-judicial, or legislative proceeding, to the extent that they would not be available by law to a private party in litigation. This exemption parallels the deliberative process and work-product concepts but is limited by the comparable civil litigation standard.

Information specifically exempted from disclosure by other provisions of West Virginia law. This catch-all provision incorporates confidentiality provisions from other code sections.

Records relating to the security of state buildings, facilities, and critical infrastructure.

The exemptions are discretionary rather than mandatory — the statute says records "may" be exempt, meaning the public body has discretion to release records even when an exemption applies. However, certain records (such as those protected by attorney-client privilege or records involving other individuals' privacy rights) may involve obligations that constrain the body's discretion.

SEGREGATION

When a record contains both exempt and non-exempt material, the public body must redact the exempt portions and release the remainder. The duty to segregate is mandatory and reflects the principle that exemptions protect specific information rather than entire documents.

ADMINISTRATIVE AND JUDICIAL REMEDIES

West Virginia provides both administrative and judicial remedies for denied records requests.

A requester may appeal a denial to the head of the public body (or designee) within the public body. The appeal should be in writing and should specify the records sought and the grounds for challenging the denial.

If the administrative appeal is unsuccessful or if the requester elects to bypass the administrative appeal, the requester may file suit in circuit court. The court reviews the matter de novo and may inspect disputed records in camera. The public body bears the burden of justifying its refusal to disclose records.

The court may order production of records and may award attorney's fees and costs to a prevailing requester. Attorney's fee awards are discretionary rather than mandatory in West Virginia, which provides somewhat less incentive for enforcement compared to states with mandatory fee-shifting.

The court may also impose penalties for willful violations of the Act, including personal liability for public officials who deliberately withhold records in bad faith.

CRIMINAL PENALTIES

The Act provides that any custodian of public records who willfully violates its provisions is guilty of a misdemeanor and, upon conviction, may be fined or removed from office. This criminal penalty provision applies to deliberate violations and serves as an additional deterrent against intentional noncompliance.

RECORDS MANAGEMENT

West Virginia law requires public bodies to maintain records retention schedules and to manage records in accordance with those schedules. Records may not be destroyed while they are the subject of a pending records request, pending litigation, or an audit hold. The Archives and History Commission provides guidance on records management and retention schedules.
''',
    },

    # =========================================================================
    # WISCONSIN
    # Wisconsin Open Records Law
    # Wis. Stat. §§ 19.31 through 19.39
    # =========================================================================
    {
        'id': 'wi-statute-open-records-law',
        'citation': 'Wis. Stat. §§ 19.31 through 19.39',
        'title': 'Wisconsin Open Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'WI',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Wisconsin\'s Open Records Law creates a presumption of access to government records and uses a balancing test to evaluate withholding claims. The law provides for mandamus enforcement, punitive damages of up to $1,000, and attorney\'s fees for successful requesters.',
        'text': '''Wisconsin Open Records Law
Wis. Stat. §§ 19.31 through 19.39

OVERVIEW AND PURPOSE

Wisconsin's Open Records Law declares that the public's right to inspect government records is a fundamental principle of democratic governance. Section 19.31 states that it is the public policy of the state that all persons are entitled to the greatest possible information regarding the affairs of government. The statute establishes a strong presumption of access that can be overcome only when the public interest in nondisclosure clearly outweighs the public interest in transparency.

Wisconsin's approach is distinctive because it relies on a case-by-case balancing test rather than a fixed list of categorical exemptions. While specific exemptions exist in other statutes, the Open Records Law itself authorizes withholding only when the custodian can demonstrate that the harm from disclosure outweighs the public benefit. This balancing framework gives Wisconsin courts significant flexibility but also creates uncertainty for both agencies and requesters.

The Law applies to every "authority," defined in Section 19.32 to include any of the following having custody of a public record: a state or local office, elected official, agency, board, commission, committee, council, department, or public body corporate and politic created by constitution, statute, rule, or order. School districts, technical college districts, and other special purpose districts are included.

DEFINITION OF RECORD

A "record" is defined as any material on which written, drawn, printed, spoken, visual, or electromagnetic information or electronically generated or stored data is recorded or preserved, regardless of physical form or characteristics, which has been created or is being kept by an authority. The definition excludes certain categories: drafts, notes, preliminary computations, and similar materials prepared for the originator's personal use; materials to which access is limited by copyright, patent, or trademark; and published materials available for sale or inspection at a public library.

The exclusion for "drafts, notes, and preliminary computations prepared for the originator's personal use" is more narrow than it might appear. Wisconsin courts have held that once a document is shared with others within the agency or used in decision-making, it loses its "personal use" character and becomes a public record. The exclusion protects only purely personal working notes that have not been circulated or relied upon.

Electronic records, including emails, text messages, and database entries, are records under the law. Records on personal devices or accounts are public records if they relate to government business.

ACCESS RIGHTS

Any person has a right to inspect a record and to obtain a copy, with limited exceptions. Wisconsin uses the term "person" without residency or citizenship restrictions. A requester need not provide identification or state a purpose for seeking records.

However, the balancing test that governs withholding decisions may take the requester's purpose into account. The Wisconsin Supreme Court has held that the identity and purpose of the requester can be relevant to the balancing analysis, particularly when privacy interests are at stake. This does not mean agencies routinely inquire into purpose, but it means that a requester who voluntarily discloses a purpose that demonstrates the public interest in disclosure may strengthen their claim to records.

REQUEST AND RESPONSE PROCEDURES

Requests may be made orally or in writing. The Law does not prescribe a particular format or require written requests, though agencies may suggest that requesters submit written requests for administrative convenience.

The Law does not establish a specific numerical response deadline. Instead, it requires that requests be fulfilled "as soon as practicable and without delay." Wisconsin courts have interpreted this standard to require reasonably prompt responses and have found violations where agencies delayed unreasonably without justification.

When a request is denied in whole or part, the custodian must provide a written explanation stating the specific reasons for the denial. The explanation must be sufficient to allow the requester to understand the basis for the withholding and to evaluate whether to seek judicial review.

FEES

Authorities may charge fees not exceeding the actual, necessary, and direct cost of reproducing records. This includes the cost of the recording medium (paper, disc, etc.) and the cost of any necessary staff time to locate and reproduce the records. The cost of locating records is chargeable, but the cost of redacting exempt material is generally not chargeable.

If a request involves programming or data extraction from electronic systems, the authority may charge for the actual cost of the programming time. However, the authority must use the least costly method of providing the records that is available and practicable.

Inspection of records at the authority's offices is free of charge.

THE BALANCING TEST

The heart of Wisconsin's Open Records Law is the balancing test established in Section 19.35(1)(a) and elaborated by the Wisconsin Supreme Court. When an authority seeks to withhold records, it must demonstrate that the public interest in nondisclosure outweighs the strong public interest in disclosure.

The balancing test requires the custodian to identify a specific public interest that would be harmed by disclosure. Abstract or speculative harm is insufficient. The custodian must articulate a concrete and particularized reason why disclosure of the specific records at issue would harm a recognized public interest.

Recognized public interests that may support nondisclosure include: individual privacy, protection of ongoing law enforcement investigations, preservation of attorney-client privilege, protection of trade secrets and competitive information, and security of government facilities. The weight given to each interest depends on the specific facts and circumstances.

The public interest in disclosure is presumed to be significant. The Wisconsin Supreme Court has described the presumption of access as "paramount" and has stated that the balancing test should tip in favor of nondisclosure only in exceptional circumstances.

Courts apply the balancing test de novo when reviewing agency withholding decisions. The custodian bears the burden of proof and must demonstrate that the public interest in nondisclosure clearly outweighs the public interest in access.

SPECIFIC EXEMPTIONS IN OTHER STATUTES

While the Open Records Law itself relies primarily on the balancing test, numerous other Wisconsin statutes create specific confidentiality protections for particular categories of records. These include student records (under FERPA and state law), patient health records, tax returns, certain law enforcement intelligence records, and juvenile court records. When a specific statute provides confidentiality protection, the records are exempt from the Open Records Law without application of the balancing test.

ENFORCEMENT AND REMEDIES

A requester who is denied access to records may bring a mandamus action in circuit court. The court reviews the denial de novo and may inspect disputed records in camera.

If the court orders release of records, it must award reasonable attorney's fees, damages (not to exceed $1,000), and other actual costs to the requester if the authority acted in an arbitrary or capricious manner. The $1,000 cap on punitive damages limits the financial penalty but the mandatory attorney's fees provision provides meaningful enforcement incentive.

The court may also impose a forfeiture of up to $1,000 on an authority that arbitrarily or capriciously denies or delays a response to a records request. Individual officials may be subject to discipline or forfeiture for willful violations.

There is no administrative appeal process under Wisconsin's Open Records Law. The sole remedy for a denied request is judicial action. However, requesters may seek informal assistance from the Attorney General's Office, which issues opinions on open records issues. These opinions are advisory but are widely respected and frequently cited by courts.

RECORDS MANAGEMENT

Wisconsin law requires authorities to maintain records in accordance with retention schedules approved by the Public Records Board. Records may not be destroyed while they are the subject of a pending records request or litigation hold. The Public Records Board provides guidance on records management, including electronic records.

RELATIONSHIP TO OPEN MEETINGS LAW

Wisconsin's Open Records Law operates alongside the Open Meetings Law (Sections 19.81 through 19.98), which requires governmental bodies to conduct business in open sessions and to keep meeting minutes. Minutes and records of governmental meetings are public records subject to the Open Records Law.
''',
    },

    # =========================================================================
    # WYOMING
    # Wyoming Public Records Act
    # Wyo. Stat. §§ 16-4-201 through 16-4-205
    # =========================================================================
    {
        'id': 'wy-statute-public-records-act',
        'citation': 'Wyo. Stat. §§ 16-4-201 through 16-4-205',
        'title': 'Wyoming Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'WY',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Wyoming\'s Public Records Act establishes a concise but broad right of access to government records, with enumerated exemptions and judicial enforcement in district court. The Act provides for attorney\'s fees and costs for prevailing requesters.',
        'text': '''Wyoming Public Records Act
Wyo. Stat. Ann. §§ 16-4-201 through 16-4-205

OVERVIEW AND PURPOSE

Wyoming's Public Records Act is a relatively concise statute that establishes a broad right of public access to government records. The Act declares that all public records are open to inspection by any person at reasonable times, reflecting Wyoming's commitment to government transparency. Wyoming courts have consistently interpreted the Act liberally in favor of disclosure and have held that exemptions must be narrowly construed.

The Act applies to all state and local governmental entities, including state agencies, departments, boards, commissions, counties, cities, towns, school districts, and special districts. Any entity that exercises governmental authority or is supported by public funds is subject to the Act.

DEFINITION OF PUBLIC RECORD

Section 16-4-201(a)(v) defines "public records" as documents, papers, and records made or received in connection with the transaction of official business by any governmental entity. The Wyoming Supreme Court has interpreted this definition broadly to include electronic records, emails, text messages, databases, audio and video recordings, and any other recorded information relating to government business.

The definition focuses on the connection between the record and official business. Records created or received by government employees in their official capacity are public records regardless of the format or medium. Records on personal devices or accounts may be public records if they relate to the transaction of official business.

Wyoming does not have a statutory exclusion for drafts, notes, or preliminary materials comparable to some other states' laws. Working papers and preliminary documents are generally public records unless they fall within a specific exemption.

ACCESS RIGHTS

Any person may inspect and copy public records at reasonable times during business hours. Wyoming uses the term "person" without imposing residency or citizenship restrictions. The Act does not require a requester to state a purpose for seeking records, and agencies may not condition access on the requester's identity or motivation.

The right to inspect includes the right to examine records at the custodian's office without charge. The right to copy includes the right to obtain reproductions in available formats.

REQUEST AND RESPONSE PROCEDURES

Wyoming's Public Records Act does not prescribe detailed request procedures or specific response deadlines comparable to some other states' laws. The Act states that records shall be available for inspection at "reasonable times" and that the custodian shall provide access "promptly."

Wyoming courts have interpreted the "promptly" requirement to mean within a reasonable time given the nature and scope of the request. While there is no statutory deadline measured in days, unreasonable delay constitutes a constructive denial that may be challenged in court.

Requests may be made orally or in writing. The Act does not require written requests, though custodians may request that complex or voluminous requests be put in writing for clarity.

When a custodian denies a request, the denial should be in writing and should specify the legal basis for the withholding. The custodian must identify the specific statutory exemption or other legal authority justifying nondisclosure.

FEES

Custodians may charge reasonable fees for providing copies of records. The fees must reflect the actual cost of reproduction and may not be set at levels designed to discourage access. The Act does not establish a specific fee schedule, leaving the determination of reasonable fees to the custodian's discretion, subject to judicial review.

Inspection of records at the custodian's office is free of charge. The Act distinguishes between inspection (no fee) and copying (reasonable fee), and custodians may not charge for the opportunity to examine records in person.

If a request will result in substantial costs, the custodian should notify the requester and provide an estimate before proceeding. The requester may narrow the request to reduce costs.

EXEMPTIONS

Section 16-4-203 enumerates the categories of records exempt from the Act's disclosure requirements. Wyoming's exemption list is more concise than those of many other states. Key exemptions include:

Records relating to law enforcement investigations, but only to the extent that disclosure would jeopardize an ongoing investigation, compromise confidential informants, endanger the safety of any person, or interfere with pending or anticipated prosecution. This exemption is harm-based and does not categorically protect all law enforcement records. Completed investigation files are generally subject to disclosure once the harm rationale no longer applies.

Personnel files, to the extent that disclosure would constitute a clearly unwarranted invasion of personal privacy. Basic employment information including name, position, salary, and dates of employment is public. The privacy exemption requires a balancing test similar to that applied under the federal FOIA.

Trade secrets, privileged information, and confidential commercial or financial information obtained from a person or entity. The custodian must determine that the information qualifies for protection and that disclosure would cause competitive harm.

Medical, psychological, and sociological data on individual persons that, if disclosed, would constitute an unwarranted invasion of personal privacy. This exemption protects individually identifiable health and personal information.

Letters of reference and academic transcripts.

Real estate appraisals made for public agencies until the transaction is completed.

Records of the mental processes of the Governor and other elected officials concerning policy discussions and deliberations. This deliberative process exemption protects the decision-making process but does not extend to factual information or to records documenting the final decision.

Attorney-client privileged communications and attorney work product prepared in connection with pending or reasonably anticipated litigation.

Records specifically made confidential by other provisions of Wyoming law or by federal law.

Interagency or intra-agency memoranda or letters that would not be available by law to a private party in litigation. This exemption parallels the federal deliberative process and work-product exemptions.

SEGREGATION

When a record contains both exempt and non-exempt material, the custodian must redact the exempt portions and provide the remainder. The duty to segregate is implicit in the Act's structure and has been confirmed by Wyoming courts. Wholesale withholding of records that contain some exempt material is not permitted unless segregation is impractical.

JUDICIAL ENFORCEMENT

Wyoming does not have a formal administrative appeal process for denied records requests. The remedy for a denial is to file suit in the district court of the county where the records are located.

The court reviews the custodian's decision de novo and may examine disputed records in camera. The custodian bears the burden of proving that an exemption applies. The court must determine whether the custodian acted properly based on the specific facts and the specific records at issue.

If the court finds that the custodian improperly withheld records, it may order production and may award reasonable attorney's fees and costs to the prevailing requester. Attorney's fees are discretionary rather than mandatory, giving the court flexibility to consider the custodian's good faith and the circumstances of the withholding.

The court may also impose sanctions or penalties for willful or bad-faith violations. Individual custodians who deliberately violate the Act may face personal liability.

RECORDS MANAGEMENT

Wyoming law requires governmental entities to maintain records in accordance with retention schedules established by the State Archives. Records may not be destroyed while they are the subject of a pending records request, pending litigation, or an administrative investigation.

Electronic records are subject to the same retention and access requirements as paper records. Agencies must maintain electronic records systems capable of producing records in usable formats.

INTERACTION WITH OPEN MEETINGS LAW

Wyoming's Public Records Act operates in conjunction with the Wyoming Open Meetings Act (Sections 16-4-401 through 16-4-408), which requires governmental bodies to deliberate and take action in open meetings. Meeting minutes, agendas, and records of votes are public records subject to both statutes. The two laws together form Wyoming's primary transparency framework.

PRACTICAL CONSIDERATIONS

Wyoming's relatively concise statute leaves many practical questions to judicial interpretation. The Wyoming Supreme Court has addressed numerous issues including the scope of the law enforcement exemption, the application of the privacy balancing test, the treatment of electronic records, and the meaning of "reasonable" fees and response times. Practitioners should consult both the statute and the relevant case law to understand the full scope of the Act's requirements.

The Wyoming Attorney General issues opinions on public records issues that, while not binding, provide useful guidance on the application of the Act. The Attorney General's Office also provides informal assistance to both requesters and custodians.
''',
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
