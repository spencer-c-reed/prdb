#!/usr/bin/env python3
"""Build state public records statute documents for KY, LA, ME, MD, MA, MI, MN, MS."""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

# =============================================================================
# KENTUCKY
# =============================================================================

KY_TEXT = '''Kentucky Open Records Act (ORA)
KRS Sections 61.870 through 61.884

LEGISLATIVE PURPOSE AND POLICY

The Kentucky Open Records Act declares that free and open examination of public records is in the public interest and that the people of the Commonwealth have a fundamental right to inspect and copy public records. The Act must be liberally construed to promote maximum public access while balancing the privacy interests of individuals in personnel and similar records. All exceptions to disclosure are strictly construed against the public agency claiming them. The burden of proof in any dispute over access lies with the agency, not the requester. This statutory presumption of openness, reinforced by decades of Attorney General opinions and court decisions, places Kentucky among the states with the strongest pro-disclosure frameworks.

DEFINITIONS (KRS 61.870)

"Public agency" is broadly defined to include every state or local governmental body, office, department, agency, branch, authority, board, bureau, commission, district, institution, instrumentality, and political subdivision. The term covers all three branches of state government, city and county governments, school districts, special districts, public universities, and any entity created by or pursuant to state or local authority. Bodies that receive at least twenty-five percent of their funds from state or local authority also qualify as public agencies. The breadth of this definition ensures that entities exercising governmental functions cannot avoid transparency obligations through creative organizational structures.

"Public record" means all documentation regardless of physical form or characteristics, which is prepared, owned, used, in the possession of, or retained by a public agency. The term includes paper documents, electronic files, emails, databases, audio and video recordings, photographs, maps, and any other medium of recorded information. The critical test is whether the record was prepared, owned, used, possessed, or retained by the agency in the course of its official functions, regardless of where the record is physically located. Records maintained on personal devices or in private email accounts are public records if they were created or used in connection with official business. The Act does not distinguish between final and draft documents for purposes of the definition — the question of whether a draft is subject to disclosure is addressed through the exemption provisions.

"Official custodian" means the chief administrative officer of the public agency or any employee designated by the agency to have custody of and responsibility for maintaining public records. Every agency must identify its official custodian. The custodian is personally responsible for ensuring compliance with the Act and may be individually liable for willful violations.

RIGHTS OF INSPECTION AND COPYING (KRS 61.872)

All public records are open to inspection by any person, except as otherwise provided by law. No person may be required to state the reason for requesting the records or the intended use. Agencies may not impose conditions on access based on the identity or purpose of the requester. This prohibition on purpose-based restrictions is absolute — the Act does not permit differential treatment of requesters under any circumstances, whether the requester is a journalist, a competitor, a litigant, or a casual member of the public.

Any person may inspect public records during the regular office hours of the public agency. Requests may be made in person, by mail, by fax, or by other written communication, including email. When records are requested by mail, the agency must mail copies upon receipt of all fees and the cost of mailing. The requester need not appear in person to obtain records.

If a record is in active use or in storage, the agency must inform the requester and designate a time and place for inspection not to exceed three business days from the date of the request. The agency must make records available for inspection and copying within a reasonable time, not to exceed five (5) business days after receiving the request. If the agency is unable to comply within five business days, it must give a detailed explanation of the cause for delay and the earliest date on which the records will be available. A failure to comply within the five-business-day period, or a failure to provide adequate justification for delay, is treated as a denial of the request.

Agencies must provide copies in the format requested, including electronic format, if the records are maintained in that format. The agency may not require the requester to accept paper copies when electronic records are available. When records exist in multiple formats, the requester may choose the format of the copies.

RESPONSE AND DENIAL REQUIREMENTS (KRS 61.880)

An agency that denies a request in whole or in part must do so in writing and must include: (1) a statement of the specific exception authorizing the withholding and a brief explanation of how the exception applies to the records withheld; (2) notification that the requester may appeal the denial to the Attorney General; and (3) notification that the requester may challenge the denial in circuit court after exhausting the administrative remedy or alternatively may go directly to circuit court. A denial that fails to cite a specific statutory exemption or fails to explain how the exemption applies to the particular records at issue is itself a violation of the Act. Generic or boilerplate denials are insufficient.

When a record contains both exempt and non-exempt information, the agency must redact only the exempt portions and provide the remainder. The agency may not deny access to an entire record based on the presence of some exempt information. The obligation to segregate and produce non-exempt material is affirmative — the agency must make the effort, not the requester.

FEES AND COSTS (KRS 61.874)

Agencies may charge a reasonable fee for copies of public records that does not exceed the actual cost of reproduction. For standard copies, a fee of no more than ten cents per page is permissible, making Kentucky one of the lowest-cost states for paper copies. No charge may be imposed for inspection of records at the agency's offices.

Agencies may also charge the actual cost of mailing, mechanical reproduction such as microfilm or microfiche, or other nonstandard reproduction costs. For records maintained in electronic format, the agency may charge the actual cost of the medium (CD, USB drive, or similar) but may not charge for the staff time needed to retrieve or compile records unless the request requires creation of a new record by extracting data and programming the agency's computer systems.

If a request requires the agency to produce a record that does not currently exist by extracting data from electronic databases or creating a compilation, the agency may charge a reasonable fee for the programming and staff time needed. This exception applies only to truly new records — if the information already exists in a retrievable format, the agency cannot treat a retrieval as a "creation" to justify additional charges. Kentucky AG opinions have scrutinized agency attempts to characterize ordinary retrievals as record creation.

EXEMPTIONS (KRS 61.878)

The Act enumerates specific exemptions, all strictly construed against the agency. The agency bears the burden of proving that the exemption applies to the specific records at issue. The principal exemptions include:

Personal privacy (61.878(1)(a)): Public records containing information of a personal nature where the public disclosure would constitute a clearly unwarranted invasion of personal privacy. This is the most frequently litigated exemption. Kentucky applies a comparative balancing test: the agency must weigh the privacy interest of the individual against the public's interest in disclosure. Information that sheds light on an agency's performance of its public duty generally must be disclosed even if it incidentally touches on private individuals. The privacy interest must be substantial and clearly outweigh the public interest — a marginal or theoretical privacy concern does not justify withholding. Kentucky AG opinions have developed extensive guidance on this balancing, consistently favoring disclosure of information about public employees acting in their official capacities.

Confidential commercial information (61.878(1)(b)): Records confidentially disclosed to an agency that, if made public, would cause competitive injury to the entity that disclosed them. The agency must demonstrate that the information was actually furnished in confidence (not merely marked confidential) and that disclosure would cause actual, demonstrable competitive harm. Boilerplate confidentiality stamps and blanket designations do not create an exemption — the agency must conduct a record-by-record analysis.

Law enforcement records (61.878(1)(c)): Records certified by the head of the agency as having been compiled and maintained for a prospective law enforcement action, including records of ongoing criminal investigations, pending prosecutions, or administrative enforcement proceedings. Once the enforcement action is complete or abandoned, the exemption expires except for records that would reveal the identity of informants or endanger the safety of law enforcement personnel. The certification requirement is mandatory — a generic assertion that records relate to law enforcement is insufficient.

Records made confidential by other statutes (61.878(1)(d)): Records made confidential by enactment of the General Assembly, including educational records (FERPA), medical records, adoption records, and records protected by specific state confidentiality provisions. This is a referral exemption — the agency must cite the specific confidentiality statute rather than relying on this subsection alone.

Real estate appraisals (61.878(1)(e)): Real estate appraisals, engineering or feasibility estimates, and evaluations relative to proposed acquisition of property by the agency, until the transaction is completed or abandoned. This exemption protects the agency's negotiating position during active real estate transactions.

Examination materials (61.878(1)(f)): Test questions, scoring keys, and examination instruments for professional licensing and academic examinations, if disclosure would compromise the validity of the test.

Deliberative process (61.878(1)(g)–(h)): Preliminary recommendations, preliminary memoranda, and preliminary drafts in which opinions are expressed or policies formulated or recommended are exempt, as is correspondence with private individuals other than correspondence intended to give notice of final agency action. This exemption protects only predecisional and deliberative materials — once a recommendation is adopted as final policy, the exemption no longer applies. Purely factual material is not protected even when contained within a deliberative document. The exemption must be applied narrowly and cannot be used to shield decisions that have been made from public scrutiny.

Law enforcement photographs (61.878(1)(i)): Photographs or film made or produced by law enforcement depicting a person's death, serious physical injury, or graphic violence, if release would constitute a clearly unwarranted invasion of personal privacy.

Informant identity and safety (61.878(1)(j)): Records to the extent they would reveal the identity of a confidential informant or endanger the life or physical safety of law enforcement personnel, witnesses, or informants.

Federal law prohibitions (61.878(1)(k)): Records the disclosure of which is prohibited by federal law or regulation, including records protected by HIPAA, FERPA, federal tax confidentiality provisions, and other federal mandates.

State law prohibitions (61.878(1)(l)): Records the disclosure of which is prohibited, restricted, or otherwise made confidential by specific state law. The agency must identify the particular statute.

Additional exemptions exist for 911 databases, social security numbers, individual financial information, certain tax records, and specific records of the legislative and judicial branches.

ATTORNEY GENERAL APPEAL (KRS 61.880(2)-(4))

Kentucky's most distinctive feature is its Attorney General review process, which is unique among the states. Any person denied access may appeal to the Attorney General within sixty (60) days of the denial. The AG must issue a written decision within twenty (20) business days of receiving the appeal. The appeal process is free, requires no attorney, and involves no filing fees.

The AG's decision is binding on the agency unless the agency appeals to circuit court within thirty (30) days. If the agency does not appeal, it must comply with the AG's decision. This makes the AG process a quasi-judicial remedy that is substantially faster and cheaper than litigation. In practice, most disputes are resolved through the AG process without the need for court action.

The AG's Office of Open Records has issued thousands of decisions interpreting the ORA over several decades, creating a rich and detailed body of administrative precedent. AG opinions are frequently cited by circuit courts and the Kentucky Court of Appeals as persuasive authority. The opinions address virtually every aspect of the Act, from the scope of individual exemptions to procedural requirements, fee calculations, and electronic records access. This body of precedent provides unusually detailed guidance for both agencies and requesters.

The burden of proof in all AG proceedings is on the agency to justify its denial. The AG may request the disputed records for in camera review to evaluate the agency's exemption claims. The AG may also request affidavits or other supporting documentation from the agency explaining the basis for withholding.

ENFORCEMENT AND PENALTIES (KRS 61.882)

Any person denied access, or aggrieved by a violation of the Act, may file an action in circuit court. The court reviews the matter de novo, meaning it makes its own independent determination rather than deferring to the agency's judgment. The court may also consider relevant AG opinions as persuasive authority.

If the court finds that the agency violated the Act, it shall award the requester reasonable attorney's fees and costs. This fee-shifting provision is mandatory, not discretionary, providing a meaningful incentive for compliance. The court may also award damages of up to twenty-five dollars per day for each day the violation continues, subject to a statutory cap. If the court finds that the agency acted in bad faith or willfully, it may impose additional penalties.

Court records custodians who willfully conceal, remove, alter, mutilate, or destroy public records may be subject to criminal penalties under separate provisions of Kentucky law. The destruction of records that are the subject of a pending request or AG appeal is treated as a serious violation.

ELECTRONIC RECORDS AND FORMAT

Agencies must provide records in the format in which they are maintained if the requester asks for that format, including electronic records. If a record is maintained electronically, the agency cannot require the requester to accept a paper printout instead. The agency must provide a copy in the electronic format unless doing so would be genuinely impracticable, and the agency must explain any claimed impracticability.

Agencies may not adopt policies or practices that obstruct public access by converting electronic records to paper format, degrading the quality of electronic records, or otherwise making records less accessible than they were when created. Email, text messages, and other electronic communications created or received in connection with official business are public records subject to the Act.

RECORD RETENTION AND MANAGEMENT

Public agencies must adopt rules and regulations to ensure compliance with the ORA, including designating an official custodian, establishing reasonable procedures for inspection and copying, and maintaining records in accessible formats. Agencies must post their procedures and the identity of the custodian. Agencies are prohibited from adopting rules that effectively impede public access.

Records retention schedules are established by the State Archives and Records Commission. Public records may not be destroyed except in accordance with approved retention schedules. The destruction of records in violation of retention schedules, or the destruction of records that are the subject of a pending request or legal proceeding, may result in sanctions including criminal penalties.

SPECIAL PROVISIONS AND RELATIONSHIP TO OTHER LAWS

Certain records have specific statutory protections that override the general right of access, including adoption records, juvenile records, grand jury proceedings, tax returns, and certain medical and mental health records. When a specific confidentiality statute conflicts with the ORA, the specific statute controls.

Kentucky's ORA also works in parallel with the Open Meetings Act (KRS 61.800 through 61.850), which requires that meetings of public agencies be conducted in public with advance notice. While the two acts are separate statutory provisions, they share the same policy of governmental transparency and are frequently invoked together. Minutes and records of public meetings are subject to the ORA's disclosure requirements.'''

# =============================================================================
# LOUISIANA
# =============================================================================

LA_TEXT = '''Louisiana Public Records Law
La. R.S. Sections 44:1 through 44:41

CONSTITUTIONAL AND STATUTORY FOUNDATION

Louisiana is one of a small number of states with a constitutional right of access to public records. Article XII, Section 3 of the Louisiana Constitution of 1974 guarantees that no person shall be denied the right to observe the deliberations of public bodies and examine public documents, except in cases established by law. This constitutional provision gives the public records law elevated status and means that exemptions must meet a higher standard of justification than in states relying on statute alone. The constitutional guarantee cannot be narrowed by statute — the legislature may create specific exemptions, but those exemptions are subject to strict scrutiny by the courts. Louisiana courts have consistently emphasized that the constitutional right of access is self-executing, meaning it applies even in the absence of implementing legislation.

The statutory framework codified in Title 44 of the Revised Statutes implements the constitutional mandate. The law is broadly written and intended to make all government records available to the public unless a specific exemption applies. Courts construe the law liberally in favor of access and strictly against the custodian asserting an exemption. The custodian bears the burden of proving that an exemption applies, and that burden is heightened by the constitutional underpinning of the right of access.

DEFINITIONS (La. R.S. 44:1)

"Public body" means any branch, department, office, agency, board, commission, district, governing authority, political subdivision, or any committee, subcommittee, advisory board, or task force thereof, or any other instrumentality of state, parish, or municipal government, including a public or quasi-public nonprofit corporation designated as an entity to receive public funds. Private entities performing governmental functions under contract or delegation may also qualify as public bodies for purposes of the records they generate in connection with those functions. The definition is broad enough to reach entities that might otherwise claim private status if they are performing functions traditionally carried out by government.

"Public record" is defined comprehensively to include all documents, papers, letters, maps, books, photographs, films, sound recordings, magnetic or other tapes, electronic data processing records, artifacts, or other documentary material, regardless of physical form or characteristics, having been used, being in use, or prepared, possessed, or retained for use in the conduct, transaction, or performance of any business, transaction, work, duty, or function that was conducted, transacted, or performed by or under the authority of the constitution or laws of the state, or by any public body. This definition is intentionally technology-neutral and encompasses electronic communications, database records, metadata, and any other form of recorded information created or received in connection with governmental functions.

"Custodian" means the public official or head of any public body having custody or control of a public record, or a designee. The custodian has an affirmative duty to maintain records in a manner that facilitates public access and to respond to requests promptly.

RIGHT OF ACCESS (La. R.S. 44:31-32)

Any person of the age of majority may inspect, copy, or reproduce any public record. The right of access extends to examination and copying during regular office hours. No person may be required to state the purpose or reason for examining public records. The law does not restrict access based on residency or citizenship — any adult person has standing to request records.

The custodian must present records for examination or copying immediately if they are immediately available. If records are not immediately available because they must be retrieved from storage or another location, the custodian must certify this in writing and set a date and hour within three (3) business days for compliance. For electronic records specifically, the three-day period is a firm deadline. The immediacy requirement is significant — when records are on hand and accessible, the custodian may not interpose delays for review, consultation, or administrative processing. The record must be produced forthwith.

If a request involves voluminous records, the custodian must make records available as they are compiled and need not wait until the entire response is complete. This rolling-production requirement prevents agencies from using the volume of a request as a pretext for delay.

Requests may be made in person, by mail, by fax, by email, or by other written communication. The law does not require any particular form for requests, though agencies may make request forms available as a convenience.

RESPONSE AND DENIAL (La. R.S. 44:32-35)

When a request is denied, the custodian must state in writing the reasons for the denial, specifying the applicable exemption and explaining how it applies to the records at issue. If only part of a record is exempt, the non-exempt portions must be segregated and made available. Blanket denials that do not specify the exemption and its application are legally deficient and subject to judicial sanction.

If the custodian fails to respond within the three-day period for electronic records, or within a reasonable time for other records, the request is deemed denied for purposes of judicial enforcement. The deemed-denial provision ensures that agencies cannot defeat the right of access through inaction or delay.

FEES (La. R.S. 44:32)

The custodian may charge a reasonable fee for copying public records that does not exceed the cost of reproduction. For standard copies, a per-page fee set by the custodian must reflect the actual cost of materials and equipment. Agencies may not charge search fees, retrieval fees, or staff time fees unless specifically authorized by statute or unless the request requires the creation of a new record that does not already exist.

If records are maintained electronically, the requester may request them in the electronic format and the custodian must comply unless providing the records in that format would compromise the security of the database itself (not merely the security of individual records, but the integrity of the database system). The custodian may charge the actual cost of the electronic medium but generally may not charge for retrieval or compilation of existing electronic data.

No fee may be charged for merely inspecting records at the agency's offices. The right of inspection is free.

EXEMPTIONS

Louisiana's exemptions are distributed throughout the Revised Statutes rather than consolidated in a single section of the public records law. This scattered approach means that custodians and requesters must consult numerous statutes to determine whether a particular record is exempt. Despite this fragmentation, the constitutional presumption of openness means that exemptions are narrowly construed and the custodian bears the burden of identifying the specific statutory provision that authorizes withholding. The principal categories include:

Law enforcement records (La. R.S. 44:3): This section provides extensive exemptions for law enforcement records. Records pertaining to pending criminal litigation or active criminal investigations may be withheld during the pendency of the matter. Intelligence and security records of law enforcement agencies, including records relating to the identity of undercover officers, records that would reveal investigative techniques and procedures, and internal affairs investigation records prior to final disposition, are exempt. Records of the Department of Justice relating to ongoing investigations are similarly protected. Once a criminal matter is concluded, many of these exemptions expire, and the records become accessible subject to individual privacy protections.

Pending claims and litigation: Records pertaining to pending claims or litigation in which the public body is a party may be withheld during the pendency of the matter, on the ground that disclosure might prejudice the body's litigation position. This exemption expires when the matter is resolved.

Deliberative process: Interagency and intra-agency memoranda that are predecisional and deliberative in nature, including communications reflecting advisory opinions, recommendations, and deliberations comprising part of the process by which governmental decisions and policies are formulated, may be withheld. Factual material within deliberative documents is generally not protected by this exemption. Once a decision is final, the documents leading to it become more accessible, though the purely deliberative components may remain exempt.

Personnel records: Certain personnel records of public employees are protected, but the scope of the exemption is relatively narrow. Basic employment information including the employee's name, title, salary, dates of employment, and job description is always public. Performance evaluations, disciplinary records, and similar documents may be partially exempt under certain circumstances, but the employee's identity and position information remain accessible. Louisiana courts have emphasized that the public has a strong interest in knowing how public employees perform their duties.

Attorney-client privilege: Communications between a public body and its attorneys that are protected by the attorney-client privilege or the work product doctrine are exempt. However, the privilege does not extend to invoices, billing statements, and fee arrangements — these are generally public records even if the detailed description of legal services may be partially redacted to protect privileged communications.

Trade secrets and commercial information: Proprietary trade secrets and commercial or financial information provided to a public body under a promise of confidentiality are exempt if disclosure would cause competitive injury to the entity that provided the information. The entity claiming the exemption must demonstrate actual competitive harm, not merely theoretical disadvantage.

Medical and health records: Patient medical records and health information maintained by public hospitals or health agencies are confidential under both state and federal law, including HIPAA.

Tax records: Individual and corporate tax returns and related records filed with the Department of Revenue are confidential and may not be disclosed except as specifically authorized by tax statutes.

Juvenile records: Records of juvenile proceedings and delinquency adjudications are confidential under the Louisiana Children's Code.

Critical infrastructure: Records disclosing the specific location, description, or analysis of vulnerabilities of critical infrastructure facilities or systems are exempt from disclosure on public safety grounds.

Social security numbers and personal financial information: Social security numbers and certain categories of personal financial information (bank account numbers, credit card numbers, and similar) are exempt when they appear in otherwise public records.

Education records: Student educational records are protected under FERPA and corresponding state provisions.

ENFORCEMENT (La. R.S. 44:35)

Any person denied the right to inspect a public record may institute proceedings in the district court for the parish where the record is maintained. The suit is tried by preference and in a summary manner, meaning it receives expedited treatment on the court's docket. The burden of proof is on the custodian to justify the denial by establishing that a specific exemption applies to each withheld record or portion thereof.

If the court finds that the custodian unreasonably or arbitrarily failed to comply with the law, the court shall award the plaintiff reasonable attorney's fees and other costs of litigation. This fee-shifting is mandatory when the court finds unreasonable or arbitrary noncompliance. If the custodian acted in an arbitrary or capricious manner, the court may also award civil penalties of up to one hundred dollars per day for each day of noncompliance, subject to a cap of five thousand dollars. These penalties are paid to the requester, providing a meaningful deterrent against willful noncompliance.

The court may examine the disputed records in camera to determine whether exemptions apply. This procedure allows the court to review the actual records without disclosing them to the requester during the litigation.

Any custodian who arbitrarily or capriciously obstructs the right of access is subject to removal from office, and the public body's governing authority may be directed by the court to institute removal proceedings. This removal remedy, while rarely invoked, provides an ultimate sanction for the most egregious violations.

ELECTRONIC RECORDS

Public records maintained in electronic format are no less public than paper records and are subject to exactly the same access requirements. When requested, electronic records must be provided in the format in which they are maintained, provided that doing so does not compromise the security of the database system. Agencies may not convert electronic records to paper format to frustrate access or increase costs to the requester.

The custodian may charge the actual cost of the electronic medium (CD, USB drive, or similar) but may not charge for programming, retrieval, or compilation unless the request requires creation of a genuinely new record that does not already exist in the agency's systems. Routine database queries and standard reports do not constitute creation of new records.

RETENTION AND MANAGEMENT

The Secretary of State, through the State Archives and Records Service, establishes records retention schedules for all public bodies. Public bodies must follow approved retention schedules and may not destroy records outside those schedules. Destruction of public records in violation of applicable retention schedules is prohibited and may result in criminal penalties. The custodian is responsible for maintaining records in a manner that facilitates public access, including maintaining appropriate indexing and retrieval systems.

RELATIONSHIP TO OTHER LAWS

Louisiana's Public Records Law is supplemented by numerous specific confidentiality provisions throughout the Revised Statutes. When a specific statute provides that particular records are confidential, that statute controls over the general right of access. However, because the right of access is constitutional in Louisiana, any exemption must be established by law and must be narrowly tailored to serve a compelling governmental interest. Courts will not infer exemptions from ambiguous statutory language — the exemption must be clear and explicit.'''

# =============================================================================
# MAINE
# =============================================================================

ME_TEXT = '''Maine Freedom of Access Act (FOAA)
1 M.R.S.A. Sections 400 through 414

PURPOSE AND POLICY (Section 400)

Maine's Freedom of Access Act establishes that public proceedings exist to aid in the conduct of the people's business and that records of governmental actions are instruments of accountability. The Act creates a strong presumption that all government records and proceedings are open to public inspection unless a specific statutory exemption applies. The Legislature has directed that the FOAA be liberally construed to promote transparency and that any doubt about whether a record is subject to disclosure be resolved in favor of openness. This presumption of openness is the interpretive default — agencies must justify any withholding, and ambiguity favors the requester.

The FOAA applies to both public records access and open meetings. The public records provisions and the open meetings provisions are contained in the same statutory chapter and share the same policy objectives, though they operate through distinct procedural mechanisms.

DEFINITIONS (Section 402)

"Public records" means any written, printed, or electronic form of information created or received by or on behalf of any agency or public official in the transaction of public or governmental business. This includes, without limitation, documents, correspondence, reports, emails, text messages, instant messages, social media communications created in an official capacity, databases, spreadsheets, recordings, photographs, maps, and any other information regardless of format. The definition is intentionally broad and technology-neutral to ensure that changes in communication methods and information storage do not create gaps in public access. Records stored on personal devices or in personal email or cloud accounts are public records if they were created or received in the transaction of public business.

"Agency" means any bureau, department, commission, committee, board, council, district, authority, institution, officer, or other entity of any branch of state government, and any political subdivision including counties, cities, towns, plantations, school administrative units, and any quasi-governmental body performing public functions. The definition encompasses a wide range of entities at both state and local levels, including entities that might be characterized as quasi-public if they perform governmental functions or receive substantial public funding.

"Public official" means any elected or appointed official, officer, or employee of any agency. The term includes full-time, part-time, and volunteer officials and employees.

"Public proceeding" means the transaction of any function affecting any rights, duties, or privileges of any person or the expenditure of public funds by any agency, including deliberations, discussions, votes, and other actions taken in the course of official business.

RIGHT OF ACCESS AND PROCEDURES (Section 408-A)

Every person has the right to inspect and copy any public record during regular business hours at the offices of the agency that maintains the record. The right extends to obtaining copies in the format in which the records are maintained, including electronic formats such as spreadsheets, databases, and digital files. No requester is obligated to state a purpose or reason for the request. The agency may not deny access based on the identity of the requester or the intended use of the records, and may not impose conditions on access that are not authorized by statute.

Upon receipt of a written request, the agency must acknowledge the request within five (5) business days and provide either: (1) the records sought; (2) access to the records for inspection and copying; (3) a denial in writing that cites the specific exemption or statutory authority and explains how the exemption applies to each record or category of records withheld; or (4) a written notice that the request will take longer to fulfill, with a good-faith estimate of when the records will be available and the reasons for the delay.

If the agency fails to respond within five business days, the request is deemed denied for purposes of appeal and judicial enforcement. The five-day clock begins when the written request is received by the office of the agency responsible for the records, regardless of how it is delivered. Agencies may not toll or extend the five-day period by routing requests through multiple offices or by claiming that the request was received by the wrong department.

Agencies must make reasonable efforts to assist requesters in identifying the records they seek and must help clarify vague or overly broad requests rather than deny them on that basis. Agencies may not require that requests be made on specific forms, though they may make standardized forms available as a convenience. Oral requests should be accommodated where practicable, but agencies are not required to respond to oral requests within the five-day statutory timeline.

FEES (Section 408-A, Subsections 8 and 9)

Agencies may charge a reasonable fee to cover the actual cost of copying public records. Fees must be established by the agency in advance and made known to requesters upon request. For standard paper copies, agencies typically charge between ten and twenty-five cents per page, though the fee must reflect actual costs. No fee may be charged for inspection of records — the right to look at records is free.

For electronic records, agencies may charge the actual cost of the storage medium (CD, USB drive, or similar) and may charge a fee for the actual direct cost of providing the copy, including the time needed to locate and retrieve the record from electronic systems. However, the agency may not charge for time spent reviewing records to determine whether exemptions apply — that review is the agency's obligation and its cost may not be passed to the requester.

If a request requires the agency to search for, retrieve, and compile records from multiple locations or systems, the agency may charge for staff time at the hourly rate of the lowest-paid employee capable of performing the task. Before commencing work on any request with estimated costs, the agency must inform the requester of the estimated cost and obtain agreement to proceed. The requester may modify or narrow the request to reduce costs.

Agencies must waive or reduce fees when the requester demonstrates that the records are sought for a purpose that primarily benefits the general public, such as news gathering, academic research, or civic oversight. Indigent requesters may also qualify for fee waivers.

EXEMPTIONS (Section 402, Subsection 3)

The FOAA establishes categories of records that are confidential by law. Unlike many states that list all exemptions in the public records statute itself, Maine's exemptions are distributed throughout the Maine Revised Statutes. Section 402(3) establishes the framework and identifies some categories, while specific confidentiality provisions appear in the relevant substantive statutes across more than three hundred separate statutory provisions. The principal categories of exempt records include:

Records designated confidential by statute: Over three hundred specific statutory provisions in the Maine Revised Statutes designate particular categories of records as confidential. Common examples include individual tax returns and tax information, certain health and medical records, mental health records, substance abuse treatment records, adoption records, sealed criminal records, certain records of the Governor's office, and communications with the Governor's legal counsel.

Invasion of personal privacy: Records the disclosure of which would constitute a clearly unwarranted invasion of personal privacy are exempt. Maine courts apply a balancing test similar to that used under the federal FOIA, weighing the requester's interest in disclosure and the public benefit of transparency against the individual's privacy interest. Information about the performance of public duties by public employees is generally not considered private, even if the employee would prefer that it not be disclosed.

Law enforcement records: Records that are part of an active criminal investigation may be withheld during the investigation to the extent disclosure would interfere with the investigation, reveal confidential informant identities, disclose investigative techniques, or endanger the safety of individuals. Once the investigation is complete and any resulting prosecution is concluded, the records become subject to disclosure with limited exceptions for informant identities and safety-related information.

Intelligence and investigative records: Records compiled for intelligence or counterintelligence purposes may be withheld if disclosure would compromise ongoing operations or reveal sources and methods.

Attorney-client communications: Records protected by the attorney-client privilege or the work product doctrine are exempt from disclosure. This includes litigation strategy, legal advice to agencies, attorney mental impressions and evaluations, and communications made in confidence between the agency and its counsel for the purpose of obtaining legal advice.

Trade secrets: Commercial or financial information that constitutes trade secrets, submitted to an agency in confidence, is exempt from disclosure if release would cause competitive harm to the entity that provided the information. The entity must demonstrate that the information actually qualifies as a trade secret and that competitive harm would result from disclosure.

Personnel records: Certain records in employee personnel files are confidential, but basic employment information including name, position, salary, and dates of service is always public. Applications for public employment are public records thirty days after the position is filled. This delayed-disclosure provision balances applicant privacy during the hiring process against the public's right to know who applied for public positions.

Juvenile records: Records of juvenile court proceedings and juvenile services are confidential under Maine's juvenile code.

Deliberative communications: While Maine does not have a broad deliberative process exemption comparable to federal Exemption 5, certain narrow statutory provisions protect specific categories of predecisional material. Internal advisory memoranda and preliminary analyses are not subject to a general exemption, and Maine courts have been reluctant to recognize implied deliberative process protections beyond what the legislature has specifically enacted.

PUBLIC ACCESS OMBUDSMAN (Section 411)

Maine has established the position of Public Access Ombudsman within the Attorney General's office. The Ombudsman serves as a resource for both the public and government agencies on FOAA compliance. The Ombudsman's functions include:

(1) Mediating disputes between requesters and agencies informally, without the expense and delay of litigation. The mediation is voluntary for both parties but provides an accessible alternative to court action;
(2) Providing training and educational materials to agencies on their obligations under the FOAA, including best practices for records management, responding to requests, and applying exemptions;
(3) Issuing advisory opinions on FOAA compliance questions when requested by agencies or members of the public;
(4) Reporting annually to the Legislature on the status of FOAA compliance statewide, including trends in requests, common compliance issues, and recommendations for legislative action.

The Ombudsman has no binding adjudicatory authority — opinions are advisory and mediations depend on the voluntary participation of both parties. However, the position provides an important low-cost, accessible mechanism for resolving disputes and improving agency compliance without the need for judicial intervention.

ENFORCEMENT AND REMEDIES (Section 409)

Any person denied access to public records may appeal to the Superior Court. The court reviews the matter de novo, making its own independent determination of whether the records are subject to disclosure. The court may examine the disputed records in camera. The burden of proof is on the agency to justify withholding by demonstrating that a specific statutory exemption applies.

If the court orders disclosure, it may award the prevailing requester reasonable attorney's fees and litigation costs if the court finds that the agency acted without a reasonable basis for its denial. The fee award is discretionary, not mandatory, and depends on the court's assessment of the reasonableness of the agency's position.

A public official who willfully violates the FOAA is subject to a civil penalty of between five hundred and two thousand dollars for the first offense and between two thousand and five thousand dollars for subsequent offenses. These penalties are payable to the State and are imposed in addition to any attorney's fees or costs awarded to the requester. The penalty provision provides a personal deterrent against willful noncompliance by individual officials.

ELECTRONIC RECORDS

Agencies must provide records in the electronic format in which they are maintained if the requester asks for electronic copies, including spreadsheets, database extracts, and digital files. Agencies may not convert electronic records to paper to frustrate access or to increase costs. If a record exists only in an electronic database and the requested information can be extracted through standard query tools available to the agency, the agency must make reasonable efforts to provide the data in the requested format.

Agencies must maintain their electronic record-keeping systems in a manner that facilitates public access and must not adopt systems designed to make records less accessible than they would be in paper form. Email, text messages, and other electronic communications created or received in the transaction of public business are public records regardless of the platform or device on which they are stored.

RECORD RETENTION

Maine's Archives and Records Management Law (5 M.R.S.A. Sections 95-A through 100) establishes retention schedules for public records. Records may only be destroyed in accordance with approved retention schedules. Destruction of records in violation of retention schedules or in response to a pending request is unlawful and may give rise to sanctions. The FOAA and the retention law work together to ensure that records are both preserved for appropriate periods and accessible to the public during those periods.

RELATIONSHIP TO OPEN MEETINGS

The FOAA also governs public meetings (Sections 403 through 406), requiring that meetings of public bodies be open to the public with advance notice. Executive sessions are permitted only for specified purposes, including discussion of personnel matters, labor negotiations, consultations with legal counsel, discussion of records made confidential by law, and certain other enumerated topics. All votes must be taken in open session. Minutes of all meetings, including executive sessions, must be maintained as public records, though the content of executive session discussions may be kept confidential to the extent the underlying topic is itself exempt from disclosure.'''

# =============================================================================
# MARYLAND
# =============================================================================

MD_TEXT = '''Maryland Public Information Act (MPIA)
Md. Code, General Provisions Sections 4-101 through 4-601

PURPOSE AND POLICY (Section 4-103)

Maryland's Public Information Act declares that all persons are entitled to have access to information about the affairs of government and the official acts of public officials and employees. The Act shall be construed in favor of allowing inspection of public records with the least cost and delay to the applicant. Custodians must act in good faith and in a manner that furthers the stated purposes of the Act. Maryland courts have emphasized that the MPIA reflects the General Assembly's judgment that an informed citizenry is essential to democratic self-governance, and that the Act's presumption of openness must be given practical effect through prompt and complete responses to requests.

DEFINITIONS (Sections 4-101, 4-102)

"Public record" means the original or copy of any documentary material that is made by a unit or instrumentality of the State government or a political subdivision, or received by such a unit or instrumentality in connection with the transaction of public business, regardless of form. This includes paper documents, electronic files, emails, text messages, databases, audio and video recordings, photographs, maps, and any other format. The definition is technology-neutral and expansive, covering records in any medium that is used, created, or received in the course of governmental business. Records stored on personal devices or accounts are public records if they relate to official business.

"Custodian" means an official who has custody or control of a public record, or a designee. The head of the governmental unit is the default custodian. Each unit must designate specific personnel to handle MPIA requests, and the custodian's contact information must be publicly available.

"Unit" means an entity of the executive, legislative, or judicial branch of State government, including any department, agency, board, commission, office, council, or instrumentality. The definition also includes political subdivisions: counties, municipalities, school boards, special districts, and their component agencies and departments. The legislative and judicial branches have more limited coverage under certain provisions.

"Applicant" means a person or governmental unit that asks to inspect a public record. No restriction based on residency, citizenship, or identity applies. Any person has standing to make a request regardless of their relationship to the records or the agency.

"Person in interest" means a person or governmental unit that is the subject of a public record or a designee of that person. This concept is important because some records that might otherwise be exempt from general public disclosure must be made available to the person whose information is contained in them.

RIGHT OF ACCESS (Section 4-201)

All persons have the right to inspect any public record at reasonable times during the business hours of the agency. The right includes the ability to obtain copies. No applicant may be required to state a purpose or reason for requesting records. The custodian may not deny or condition access based on who is asking or why.

A custodian who receives a request must respond within a reasonable time, not to exceed thirty (30) days from receipt. However, within ten (10) business days of receiving the request, the custodian must either: (1) grant the request and provide the records; (2) deny the request in writing and explain the legal grounds for denial, including the specific statutory exemption; or (3) acknowledge receipt of the request, provide a good-faith time estimate for completion, and explain the reason for the delay.

The ten-day initial response requirement ensures that requesters receive prompt acknowledgment and are not left without information about the status of their request. The thirty-day outer limit provides a firm deadline for production, though courts have recognized that extraordinarily complex requests may require additional time with proper justification.

If a request is denied, the denial must be in writing and must explain the legal authority for the denial, including the specific statutory exemption or other legal basis. Partial denials require the custodian to segregate exempt material from non-exempt material and release everything that is not exempt. The custodian may not deny access to an entire record based on the presence of some exempt information.

FEES (Section 4-206)

A custodian may charge a reasonable fee that does not exceed the actual cost of searching for, preparing, and reproducing the requested records. Fees must reflect actual costs, not standardized or inflated rates. For standard copies, fees typically range from twenty-five cents to one dollar per page depending on the agency. For electronic records, the agency may charge the cost of the electronic medium (CD, USB, or similar) and reasonable search and retrieval costs.

If the estimated cost exceeds three hundred fifty dollars, the custodian must obtain the applicant's agreement before proceeding with the work. The custodian must provide an itemized cost estimate to the applicant, broken down by category (search time, review time, copying costs). This cost-transparency requirement prevents surprise charges and allows the applicant to modify or narrow the request to manage costs.

Fee waivers are available in two circumstances: (1) the applicant demonstrates indigency; or (2) the applicant demonstrates that disclosure is in the public interest because it primarily benefits the general public rather than the individual requester. The public interest standard focuses on whether the information will contribute significantly to public understanding of government operations or activities.

MANDATORY DENIALS (Sections 4-301 through 4-339)

Maryland distinguishes between records a custodian must deny and records a custodian may deny. Mandatory denials involve categories of records where the law compels withholding regardless of the custodian's judgment. Principal mandatory denials include:

Adoption records and related court files. Library circulation records and registration records that identify individual users. Certain retirement and pension records containing personal financial information. Letters of reference submitted in confidence for employment, appointment, or admission to educational institutions. Hospital records and patient medical records protected by health privacy laws. Motor vehicle records containing personal information subject to the federal Driver's Privacy Protection Act. Individual and corporate tax return information filed with the Comptroller. Student education records protected by FERPA and state educational privacy laws. Social security numbers in most contexts. Records of child abuse and neglect investigations prior to final disposition. Records sealed by court order or made confidential by other specific statutes.

DISCRETIONARY DENIALS (Sections 4-341 through 4-362)

Discretionary denials involve categories of records where the custodian has authority, but not an obligation, to withhold. The custodian must exercise judgment and may choose to disclose even exempt records if the public interest in disclosure outweighs the interest in nondisclosure. Principal discretionary denials include:

Interagency or intra-agency memoranda and letters that would not be available by law to a party in litigation with the agency — this is the deliberative process exemption. It protects only predecisional and deliberative materials: documents that reflect the give-and-take of the consultative process leading to a final agency decision. Factual material within deliberative documents is not protected. Final policies, adopted positions, and working law (the standards the agency actually applies to the public) are not deliberative and must be disclosed.

Investigatory records compiled for law enforcement or regulatory purposes, to the extent that disclosure would interfere with a pending investigation, deprive a person of a fair trial, reveal a confidential source, disclose investigative techniques or procedures, or endanger the safety of an individual. Each of these harms must be specifically demonstrated — blanket assertions of investigative privilege are insufficient.

Trade secrets and confidential commercial or financial information obtained from a person or business entity. The custodian must balance the competitive harm that would result from disclosure against the public interest in transparency.

Records containing information about the security of information technology systems, buildings, structures, or critical infrastructure.

Real estate appraisals, engineering or feasibility estimates relating to proposed public acquisitions, until the transaction is complete or abandoned.

Certain records of the Governor's office reflecting deliberations, advice, and recommendations.

PERSON IN INTEREST ACCESS

Even when records are exempt from general public disclosure, Maryland law frequently grants the person who is the subject of the record the right to inspect their own records. This applies to personnel records, investigative records, medical records, and other categories where the exemption is designed to protect the individual rather than shield the government from accountability. The person in interest right ensures that individuals can access information about themselves that the government maintains.

PUBLIC ACCESS OMBUDSMAN (Sections 4-1B-01 through 4-1B-06)

Maryland has established an independent Public Access Ombudsman within the Office of the Attorney General. The Ombudsman receives and works to resolve complaints from applicants about access to public records, mediates disputes between applicants and custodians, provides advisory opinions on MPIA compliance, issues an annual report to the Governor and General Assembly on the state of public records access, and conducts training and outreach for agencies and the public. The Ombudsman process is voluntary and the opinions are non-binding, but the position provides a low-cost alternative to litigation and serves as an important accountability mechanism.

STATE PUBLIC INFORMATION ACT COMPLIANCE BOARD (Sections 4-1A-01 through 4-1A-10)

Maryland also has a Public Information Act Compliance Board, a three-member body appointed by the Governor that hears complaints about fee disputes, response delays, and other procedural MPIA issues. The Board issues written opinions and may recommend corrective action. While it cannot directly order disclosure of records, its opinions are publicly available and are frequently cited by courts as persuasive authority. The Board provides an additional layer of administrative review that is faster and cheaper than litigation.

ENFORCEMENT AND REMEDIES (Section 4-362)

An applicant who is denied access may file a complaint with the circuit court. The court reviews de novo and may examine records in camera. The burden of proof is on the custodian to justify withholding by demonstrating that a specific exemption applies and that the exemption has been properly invoked.

If the court determines that the custodian acted arbitrarily or capriciously in denying a request, the court shall award reasonable attorney's fees to the applicant. This fee award is mandatory, not discretionary, when arbitrary or capricious denial is found. If the custodian acted in bad faith, the court may also award costs and compensatory damages.

A custodian who willfully and knowingly violates the MPIA by failing to disclose records that are required to be disclosed is subject to a civil penalty not exceeding one thousand dollars for each violation. The penalty is payable to the State.

ELECTRONIC RECORDS (Section 4-205)

Agencies must provide records in the format in which they are maintained, including electronic formats, if the applicant requests electronic copies. Agencies may not refuse to produce electronic records solely because producing them would require exporting data from a database or running a standard query. Email, text messages, and other electronic communications created or received in connection with official business are public records.

If a request requires the creation of a genuinely new record by manipulating, reorganizing, or cross-referencing existing electronic data in a way the agency does not routinely do, the custodian may decline to create the new record but must provide access to the existing data in its current format.

RETENTION AND DESTRUCTION

Public records may only be destroyed in accordance with records retention schedules approved by the State Archivist. Premature destruction of records is unlawful. Destruction of records that are the subject of a pending request, litigation hold, or investigation may result in criminal penalties and sanctions for willful spoliation. Each governmental unit must maintain a records management program that includes identification of all record series, assignment of retention periods, and procedures for orderly disposition at the end of the retention period.

PROACTIVE DISCLOSURE AND TRANSPARENCY

Maryland law encourages governmental units to proactively publish commonly requested records online, including organizational charts, budgets, audits, meeting minutes, and directories. The Maryland General Assembly has enacted specific requirements for certain categories of information to be posted on agency websites, reducing the need for individual requests and advancing the MPIA's transparency objectives. Agencies that maintain websites are expected to use them as tools for public disclosure and to minimize the burden on both requesters and custodians.

RELATIONSHIP TO OPEN MEETINGS

The MPIA works in conjunction with Maryland's Open Meetings Act (General Provisions, Title 3). Minutes and records of public meetings are public records subject to disclosure under the MPIA. Closed session records are treated differently — while the minutes of closed sessions are maintained, their content may be restricted to the extent the underlying subject matter is itself exempt from disclosure. All final actions and votes must be taken in open session and documented in the public minutes. The two acts share the common objective of governmental transparency and are frequently invoked together in disputes about access to government information.'''

# =============================================================================
# MASSACHUSETTS
# =============================================================================

MA_TEXT = '''Massachusetts Public Records Law
M.G.L. c. 66, Sections 10 through 10B and c. 66A

PURPOSE AND POLICY

Massachusetts public records law establishes a broad presumption that all government records are public unless a specific exemption applies. The law was substantially strengthened by comprehensive reforms enacted in 2016 (Chapter 121 of the Acts of 2016), which reduced response times, capped fees, created an enhanced enforcement mechanism through the Supervisor of Records, established fee waivers for public-interest requests, and provided attorney fee recovery with the possibility of punitive damages for bad faith denials. These reforms were among the most significant updates to any state public records law in recent years and addressed long-standing criticism that Massachusetts had one of the weakest public records regimes in the country.

Prior to the 2016 reforms, Massachusetts was routinely criticized for excessively high fees, unreasonably long response times, and the absence of meaningful enforcement mechanisms. The reformed law represents a fundamental shift toward greater transparency and accountability, and remains the operative framework for public records access in the Commonwealth.

DEFINITIONS

"Public records" is defined in M.G.L. c. 4, Section 7(26) as all books, papers, maps, photographs, recorded tapes, financial statements, statistical tabulations, or other documentary materials or data, regardless of physical form or characteristics, made or received by any officer or employee of any agency, executive office, department, board, commission, bureau, division, or authority of the Commonwealth or any political subdivision, or of any authority established by the General Court to serve a public purpose. The term also encompasses documentary materials made or received by the judiciary or the General Court. The definition is broadly drafted and includes electronic communications, databases, spreadsheets, audio and video recordings, and all other forms of recorded information.

"Records access officer" (RAO) is the official designated by each agency to coordinate public records requests, ensure compliance with the law, and serve as the primary point of contact for requesters. The 2016 reforms required every agency to designate an RAO and post the RAO's name and contact information in a publicly accessible location, including the agency's website.

"Supervisor of Records" is the state official within the Secretary of the Commonwealth's office who oversees public records compliance statewide, adjudicates disputes between requesters and agencies, issues binding orders, and publishes guidance on the public records law.

RIGHT OF ACCESS AND PROCEDURES (c. 66, Section 10)

Every person has a right to access public records. No requester may be required to identify themselves or state a purpose for the request. An agency may ask for contact information solely to facilitate the response (such as an email address for electronic delivery), but may not condition access on the provision of identifying information.

Upon receipt of a request, the records access officer must respond within ten (10) business days. The response must either: (1) provide the records; (2) make the records available for inspection and copying; (3) deny the request in writing, citing the specific exemption under c. 4, Section 7(26) and explaining how the exemption applies to each category of records withheld; or (4) if more time is needed, provide a good-faith written estimate of the time needed, the specific reason for delay, and an itemized fee estimate if fees will be charged.

If the agency fails to respond within ten business days, the request is deemed constructively denied and the requester may appeal immediately to the Supervisor of Records without waiting further. The constructive denial provision prevents agencies from defeating the right of access through silence or delay.

Agencies may request up to an additional fifteen (15) business days to respond if the request is particularly complex, involves a large volume of records, or requires consultation with other agencies or legal counsel. The total response period may not exceed twenty-five (25) business days without the express approval of the Supervisor of Records. Extensions beyond twenty-five days require a showing of exceptional circumstances and Supervisor authorization.

FEES (c. 66, Section 10(d))

The 2016 reforms established detailed and specific fee limitations that significantly reduced the cost of obtaining public records. Agencies may charge:

Paper copies: up to five cents per page for black and white, single-sided copies. This is among the lowest statutory copy fees in the nation and represents a dramatic reduction from the fees agencies charged before the 2016 reforms.

Electronic records: the actual cost of the storage medium (CD, USB drive, or similar), but generally no charge for records delivered by email. Since most records are now electronic, this effectively makes electronic delivery free in most cases.

Staff time: if a request requires more than four (4) hours of employee time to search for, compile, segregate exempt from non-exempt material, and reproduce the records, the agency may charge for time beyond the first four hours at an hourly rate not to exceed twenty-five dollars per hour. The first four hours of staff time are free. This provision ensures that routine requests do not generate any labor charges and limits the hourly rate for more complex requests.

Fee waivers: agencies must waive fees if the requester demonstrates that the records are sought for a purpose that primarily benefits the public rather than the individual requester, or if the requester is indigent. The public interest standard focuses on whether disclosure will contribute significantly to public understanding of government operations. Fee waiver requests must be considered in good faith by the RAO.

Fee estimates: agencies must provide a written, itemized fee estimate to the requester before commencing work if the estimated cost exceeds five dollars. The requester may modify, narrow, or withdraw the request after receiving the estimate. This cost-transparency requirement prevents surprise charges and empowers requesters to make informed decisions.

EXEMPTIONS (c. 4, Section 7(26))

Massachusetts identifies its public records exemptions within the statutory definition of "public records" in c. 4, Section 7(26). A record that falls within one of the enumerated exemptions is excluded from the definition of "public records" and is not subject to mandatory disclosure. All exemptions are strictly construed against the agency. The principal exemptions are:

(a) Records specifically or by necessary implication exempted from disclosure by statute. Hundreds of specific confidentiality provisions exist throughout the Massachusetts General Laws. Common examples include individual tax returns and tax information, certain medical records, substance abuse treatment records, adoption records, grand jury materials, sealed court records, and certain educational records. The agency must cite the specific statute.

(b) Records related solely to internal personnel rules and practices of the agency, provided they are not significant in interpreting substantive agency action. This exemption is narrow — internal policies that affect the rights of the public, define agency practice, or serve as "working law" applied to the public must be disclosed even if they are characterized as internal.

(c) Personnel and medical files or information, and any other materials relating to a specifically named individual, the disclosure of which may constitute an unwarranted invasion of personal privacy. This exemption requires a case-by-case balancing test: the privacy interest of the individual must be weighed against the public's interest in disclosure. Information about the performance of public duties by public employees is generally not considered private. Salary information, job titles, employment dates, and similar data about public employees are public records.

(d) Inter-agency or intra-agency memoranda or letters relating to policy positions being developed by the agency, but not including factual reports, studies, or other factual material unless otherwise exempted. This is the deliberative process exemption. It protects only predecisional and deliberative communications — documents that reflect the formulation of policy before a decision is reached. Factual information, final policies, adopted positions, instructions to staff, and the rules and standards the agency actually applies (working law) are not protected. The exemption is designed to encourage candid internal discussion, not to hide the basis for governmental decisions.

(e) Notebooks and other materials prepared by an employee which are personal to the employee and not maintained as part of the official files of the governmental unit. Personal notes and aide-memoires that are truly personal and are not circulated, relied upon, or incorporated into agency files are not public records.

(f) Investigatory materials necessarily compiled out of the public view by law enforcement or prosecutorial agencies, but only to the extent that disclosure would: interfere with enforcement proceedings, deprive a person of a fair trial, identify a confidential source, disclose investigative techniques not generally known, or endanger the safety of law enforcement personnel. Each sub-element requires a specific factual showing tied to the particular records. Once an investigation is complete, many of these protections expire.

(g) Trade secrets or commercial or financial information voluntarily provided to an agency for use in developing governmental policy, if the provider has requested confidentiality. The provider must demonstrate that the information actually qualifies as a trade secret and that disclosure would cause demonstrable competitive harm.

(n) Records of responses to requests for proposals or bids to enter into a contract, until a contract is executed or all bids are rejected. This prevents competitors from accessing one another's proposals during the evaluation period but makes all submissions public once the process concludes.

(o) Records relating to internal layout, structural elements, security measures, emergency preparedness, threat assessments, or domestic preparedness strategies for buildings and facilities.

FAIR INFORMATION PRACTICES ACT (c. 66A)

Chapter 66A provides additional protections for "personal data" — information concerning an identifiable individual maintained in a data system by an agency. Agencies maintaining personal data systems must: collect and maintain only data relevant and necessary to the agency's authorized purpose; collect data directly from the individual where practicable; take reasonable steps to ensure the data is accurate, complete, and current; allow individuals to inspect and request correction of their own records; and establish appropriate administrative, technical, and physical safeguards to protect the data against unauthorized access, modification, destruction, or disclosure.

Chapter 66A does not create a blanket exemption for all personal data — it is not a substitute for the exemptions in c. 4, Section 7(26). Rather, it establishes principles for responsible data stewardship and gives individuals specific rights regarding their own information. The interplay between c. 66A and the public records exemptions requires careful case-by-case analysis.

SUPERVISOR OF RECORDS AND ADMINISTRATIVE APPEAL (c. 66, Section 10A)

The Supervisor of Records within the Secretary of the Commonwealth's office is the primary enforcement mechanism for the public records law. Any requester whose request is denied or constructively denied may appeal to the Supervisor within ninety (90) days of the denial.

The Supervisor reviews the appeal, may request the disputed records for in camera review, and issues a written determination typically within ten business days. The Supervisor may order the agency to produce all or part of the records, confirm the denial in full, or direct a compromise. The Supervisor's determination is binding on the agency unless the agency appeals to Superior Court within ten business days. If the agency fails to appeal and fails to comply, the Supervisor may refer the matter to the Attorney General for enforcement.

The Supervisor also has authority to investigate agency compliance on their own initiative, to issue regulations governing fees, response procedures, and other administrative aspects of the public records law, and to publish guidance and best practices for agencies.

JUDICIAL ENFORCEMENT (c. 66, Section 10A(d))

If the Supervisor orders disclosure and the agency does not comply, or if the requester chooses to bypass the Supervisor and file directly in court, the requester may commence an action in Superior Court. The court reviews the matter de novo and may examine the records in camera. The burden of proof is on the agency to demonstrate that the records fall within a specific exemption.

If the court orders disclosure and finds that the agency did not have a reasonable basis for its denial, the court shall award reasonable attorney's fees and costs to the requester. This fee-shifting is mandatory when the court finds the denial unreasonable. If the court finds the agency acted in bad faith, it may award punitive damages of up to five thousand dollars in addition to attorney's fees, costs, and any actual damages. The punitive damages provision, added by the 2016 reforms, provides a meaningful deterrent against willful noncompliance.

ELECTRONIC RECORDS

Agencies must provide records in electronic format when requested, if the records are maintained electronically. Agencies may not convert electronic records to paper to frustrate access or increase costs. If records can be delivered by email at no cost to the agency, the agency should do so without charge. The law recognizes that the cost of electronic delivery is essentially zero and should be reflected in fee calculations.

PROACTIVE DISCLOSURE

The 2016 reforms encouraged agencies to proactively post commonly requested records online, including organizational charts, budgets, expenditure reports, meeting minutes, and other frequently sought materials. Proactive disclosure reduces the burden on both requesters and agencies and advances the law's transparency objectives.'''

# =============================================================================
# MICHIGAN
# =============================================================================

MI_TEXT = '''Michigan Freedom of Information Act (FOIA)
MCL Sections 15.231 through 15.246

PURPOSE AND POLICY (Section 15.231)

Michigan's Freedom of Information Act declares it the public policy of the State that all persons are entitled to full and complete information regarding the affairs of government and the official acts of those who represent them as public officials and employees. FOIA provides the people with the right to know about the performance of government and the expenditure of public funds. The Act is to be construed liberally to accomplish its purpose of full disclosure and transparency. Michigan courts have consistently reinforced this liberal-construction mandate, holding that exemptions must be narrowly applied and that any doubt about whether a record is exempt should be resolved in favor of disclosure.

DEFINITIONS (Section 15.232)

"Public body" means any state officer, employee, agency, department, division, bureau, board, commission, council, authority, or other body in the executive branch of state government, including the state legislature, any county, city, township, village, intercounty, intercity, or regional governing body, council, school district, special district, or municipal corporation, and any board, department, commission, council, or agency thereof. The definition extends to any other body created by state or local authority or primarily funded by or through state or local authority. Courts are excluded from the definition. The breadth of the definition ensures that entities performing governmental functions at any level of government are covered, including special-purpose entities and quasi-governmental bodies that receive substantial public funding.

"Public record" means a writing prepared, owned, used, in the possession of, or retained by a public body in the performance of an official function, from the time it is created. A "writing" is defined broadly to include handwriting, typewriting, printing, photostating, photographing, photocopying, and every other means of recording, including letters, words, pictures, sounds, or symbols, or any combination thereof, and includes paper, electronic data, email, text messages, social media communications created in an official capacity, and any other digital format. The definition captures records from the moment of their creation, meaning that there is no minimum retention period before the right of access attaches.

"FOIA coordinator" is the individual designated by each public body to accept, process, and respond to FOIA requests. Every public body must designate a FOIA coordinator and post the coordinator's contact information.

"Unusual circumstances" are specifically defined and include: the need to search for, collect, or examine records at multiple field offices or storage locations; the need to search for, collect, and examine a voluminous amount of separate and distinct records; the need to separate exempt from non-exempt information in requested records; and the need to consult with another public body that has a substantial interest in the request.

RIGHTS OF ACCESS AND PROCEDURES (Sections 15.233, 15.235)

Any person has the right to inspect, copy, or receive copies of public records, with the narrow exception that an incarcerated individual may not submit a FOIA request on behalf of another incarcerated individual. The right extends to all records unless a specific exemption applies. No person is required to state the purpose of the request, and the public body may not condition access on the identity or purpose of the requester, except in the narrow context of determining eligibility for an indigency fee reduction.

Written requests must be directed to the FOIA coordinator. Upon receipt, the public body must respond within five (5) business days by: (1) granting the request and providing the records or making them available for inspection; (2) denying the request in writing, stating the specific reasons for denial and citing the applicable exemption; (3) granting in part and denying in part, with specific reasons for each denial; or (4) issuing a written notice of extension.

The public body may extend the response time by up to ten (10) additional business days (for a total of fifteen business days) if unusual circumstances exist. The extension notice must state the specific reasons for the extension, identify which unusual circumstances apply, and state the date by which the public body will respond. Only one extension is permitted per request. Further extensions are not authorized by statute.

If the public body fails to respond within the applicable time period, the request is deemed denied. The failure also may result in a reduction of otherwise allowable fees as a statutory penalty for late response.

FEES (Section 15.234)

Michigan FOIA contains unusually detailed and specific fee provisions that limit what public bodies may charge. Fees must be itemized in a detailed written statement provided to the requester before work begins. Allowable fee components include:

Labor costs for search and retrieval: the hourly wage of the lowest-paid employee capable of searching for, locating, and retrieving the requested records, with a fringe benefit multiplier not to exceed fifty percent of the hourly wage. For requests from Michigan residents made for non-commercial purposes, the first hour of search time is free.

Labor costs for examination and separation: if records must be examined to separate exempt from non-exempt material, the hourly wage (plus fringe) of the lowest-paid employee capable of performing the review. This is a separate labor category from search and retrieval.

Copying costs: the actual incremental cost of making copies, including paper, toner, and the per-page operating cost of the copying equipment. These costs must reflect direct actual costs, not standardized estimates or averages that include overhead or amortization of equipment. The per-page cost must be documented.

Mailing costs: the actual cost of mailing if the requester asks for records to be mailed.

Electronic media costs: the actual cost of the electronic medium (CD, USB drive, or similar) and any actual direct cost of duplication and transmission.

No fee may be charged for the FOIA coordinator's labor in reviewing the request, determining its scope, or supervising the response. These are administrative costs borne by the public body.

Deposit: a public body may require a deposit of up to fifty percent of the estimated total fee before commencing work on a request estimated to cost more than fifty dollars. The deposit must be accompanied by a detailed itemized cost estimate.

Indigency reduction: a requester who qualifies as indigent (household income below 200% of the federal poverty level) and who has not received a fee discount from the same public body within the preceding twelve months is entitled to a reduction of the first twenty dollars in fees.

Public interest waiver: a public body may waive or reduce fees if the requester demonstrates that disclosure primarily benefits the general public. This waiver is discretionary, not mandatory.

EXEMPTIONS (Section 15.243)

Section 15.243 lists specific exemptions. All exemptions in Michigan FOIA are discretionary, meaning the public body may choose to disclose even exempt records. When a record contains both exempt and non-exempt information, the exempt material must be redacted and the non-exempt portions produced. The principal exemptions include:

Personal privacy (15.243(1)(a)): Information of a personal nature if public disclosure would constitute a clearly unwarranted invasion of an individual's privacy. The balancing test weighs the individual's privacy interest against the public's interest in knowing how government functions. Information about public employees' performance of official duties is generally not considered private.

Law enforcement (15.243(1)(b)): Investigating records compiled for law enforcement purposes, but only to the extent that disclosure would: interfere with law enforcement proceedings, deprive a person of a fair trial, constitute an unwarranted invasion of personal privacy, disclose the identity of a confidential source, disclose investigative techniques or procedures not generally known outside of government, or endanger the life or physical safety of law enforcement personnel. Each sub-element requires a particularized showing — blanket assertions are insufficient.

Statutory exemptions (15.243(1)(c)): Records specifically exempted from disclosure by other state or federal statutes.

Trade secrets (15.243(1)(d)): Trade secrets or commercial or financial information voluntarily provided to the public body for use in developing governmental policy, if the provider has requested confidentiality and the information actually qualifies as a trade secret.

Deliberative process (15.243(1)(e) and (1)(k)): Advisory communications within or between public bodies of an advisory nature to the extent that they cover other than purely factual materials and are preliminary to a final agency determination of policy or action. This exemption does not protect factual information, final policy determinations, or the working law that the agency applies to the public. The exemption is designed to protect the candor of internal deliberations, not to shield the basis for governmental decisions from public scrutiny.

Testing materials (15.243(1)(g)): Testing data, examination questions, and scoring keys for licensing or academic examinations, to protect test integrity.

Medical and counseling records (15.243(1)(h)): Medical, counseling, or psychological records, but individuals retain the right to access their own records.

Attorney-client privilege (15.243(1)(i)): Records protected by the attorney-client privilege, including confidential communications between the public body and its legal counsel made for the purpose of obtaining or providing legal advice.

Bid and proposal materials (15.243(1)(j)): Bids, proposals, and related evaluation materials until the submission deadline has passed or the contract is awarded, whichever occurs first.

Security records (15.243(1)(s)): Records or information of measures designed to protect the security or safety of persons or property, whether public or private, including security plans, protocols, and vulnerability assessments.

Cybersecurity records (15.243(1)(y)): Records relating to cybersecurity plans, assessments, or vulnerabilities of public body information technology systems.

ENFORCEMENT AND REMEDIES (Section 15.240)

A person who is denied access in whole or in part may commence a civil action in circuit court. The action receives expedited treatment. The court reviews de novo and may examine records in camera. The burden of proof is on the public body to sustain its denial by demonstrating that the exemption applies.

If the court orders disclosure, it shall award reasonable attorney's fees, costs, and disbursements to the prevailing requester. This fee-shifting is mandatory upon a court order of disclosure. If the court finds that the public body acted arbitrarily and capriciously in denying the request, it may award additional punitive damages of one thousand dollars. If the court determines that the public body willfully and intentionally failed to comply with FOIA, the court shall award punitive damages of two thousand five hundred dollars. These punitive damages are in addition to actual or compensatory damages and attorney's fees.

Individual liability: a public body employee or official who willfully and intentionally violates FOIA is subject to a personal civil fine of up to seven thousand five hundred dollars. A public body found to have arbitrarily and capriciously violated FOIA by withholding non-exempt records is subject to a fine of not less than two thousand five hundred dollars nor more than seven thousand five hundred dollars.

ELECTRONIC RECORDS

Public bodies must provide records in the format in which they are maintained if the requester asks for electronic copies. Agencies may not convert electronic records to paper to frustrate access. If records are maintained in a database and can be extracted through standard tools, the public body must do so. However, a public body is not required to create a new record that does not already exist in its systems.

FOIA PROCEDURES AND GUIDELINES

Each public body must establish, adopt, and publish detailed FOIA procedures and guidelines, including a summary of the public body's procedures for processing requests, a description of available exemptions, a complete fee schedule, and information about how to submit requests and appeals. These guidelines must be publicly available on the public body's website and at its offices. The published guidelines serve as a binding statement of the public body's FOIA practices and are enforceable by requesters in court.

APPEAL PROCESS

Before filing suit in circuit court, a requester who receives a denial or partial denial may submit a written appeal to the head of the public body. The head of the public body must respond to the appeal within ten (10) business days by: (1) reversing the denial and making the record available; (2) upholding the denial in writing with a full explanation of the reasons; or (3) issuing a notice of extension for up to ten additional business days. If the head of the public body upholds the denial or fails to respond within the appeal period, the requester may then file a civil action in circuit court.

This two-step administrative process (request to FOIA coordinator, appeal to head of public body) provides an internal review mechanism that may resolve disputes without litigation. However, the requester is not required to exhaust this administrative process before filing suit — the statute provides that a person may commence an action after receiving a final determination or after the time for response has expired.

RECORD RETENTION

Michigan law requires public bodies to establish and follow records retention schedules approved by the State Records Management Services. Records may not be destroyed except in accordance with approved schedules. Destruction of records that are the subject of a pending FOIA request, appeal, or litigation hold is unlawful and may result in sanctions, including adverse inferences in litigation and contempt findings. The records retention framework works in tandem with FOIA to ensure that records are both preserved for appropriate periods and accessible to the public during those periods.

RELATIONSHIP TO OPEN MEETINGS

Michigan's FOIA operates alongside the Open Meetings Act (MCL 15.261 through 15.275), which requires that meetings of public bodies be open to the public. Minutes and records of public meetings are public records subject to FOIA. Closed session minutes are maintained but may be exempt from disclosure to the extent the underlying subject matter qualifies for a FOIA exemption. The two acts share the fundamental purpose of governmental transparency and are frequently invoked together in public access disputes.'''

# =============================================================================
# MINNESOTA
# =============================================================================

MN_TEXT = '''Minnesota Government Data Practices Act (MGDPA)
Minn. Stat. Chapter 13

PURPOSE AND POLICY (Section 13.01)

Minnesota's Government Data Practices Act takes a fundamentally different approach from most state public records laws. Rather than providing a general right of access with enumerated exemptions, the MGDPA classifies all government data into specific categories with defined access rules. All government data is presumed public unless the legislature has specifically classified it otherwise. This classification system is more structured and comprehensive than the exemption-based approach used by most states and the federal FOIA, and provides greater predictability for both agencies and requesters.

The Act declares that it is the policy of the State that all government data are public and are accessible by the public for both inspection and copying unless there is federal law, a state statute, or a temporary classification that provides that certain data are not public. The Act is the exclusive mechanism for classifying government data in Minnesota — agencies may not create their own data classifications, restrict access beyond what the statute authorizes, or treat data as non-public without statutory authority. This exclusivity principle is enforced by courts and distinguishes Minnesota's framework from states where agencies retain substantial discretion over access decisions.

DEFINITIONS (Section 13.02)

"Government data" means all data collected, created, received, maintained, or disseminated by any government entity regardless of its physical form, storage media, or conditions of use. This includes paper records, electronic files, databases, emails, text messages, audio and video recordings, photographs, metadata, and any other form of recorded information. The definition is broad and technology-neutral, ensuring that evolving forms of communication and data storage do not create gaps in the framework.

"Government entity" or "entity" means a state agency, statewide system, or political subdivision. This includes all state departments, offices, boards, commissions, the state legislature, and the courts (to a limited extent), as well as counties, cities, towns, school districts, and any other political subdivision or instrumentality of government. The Act also applies to private entities that perform governmental functions under contract, to the extent of those functions — the contractor's records relating to the government function are classified and accessible under the same rules that would apply if the government performed the function directly.

"Responsible authority" means the government entity official designated to be in charge of the entity's data collection and management. Every government entity must designate a responsible authority and publicly identify that person.

"Data practices compliance official" means the individual designated by the entity to receive and respond to requests for government data. This person serves as the entity's primary point of contact for data requests.

DATA CLASSIFICATION SYSTEM (Sections 13.02, 13.03)

The MGDPA classifies all government data into categories based on two dimensions: whether the data is about individuals versus not about individuals, and the level of access permitted. This two-axis system produces five distinct classification levels:

For data on individuals (data about natural persons that can be associated with a particular individual):

Public data on individuals: accessible to anyone without restriction. The entity must make this data available for inspection and copying upon request. Examples include names and salaries of public employees, certain licensing data, campaign finance data, and other data specifically classified as public by statute.

Private data on individuals: accessible only to the data subject (the individual the data is about), to authorized agents of the data subject, and to government personnel whose work assignments reasonably require access. Private data is not available to the general public. Examples include social security numbers, certain medical information, educational records, non-public portions of personnel files, and welfare data. The data subject has the right to be informed of what private data the entity maintains about them and to obtain copies.

Confidential data on individuals: the most restricted classification for data about individuals. Confidential data is not accessible to the data subject or to the public. Only authorized government personnel with a work assignment requiring access may view this data. Examples include active criminal investigative data about individuals, certain child protection assessment data during investigation, and data whose release to the subject would compromise an ongoing investigation.

For data not on individuals (data about organizations, things, or government operations that is not identifiable to a specific natural person):

Public data not on individuals: accessible to anyone without restriction.

Nonpublic data not on individuals: not accessible to the public, but accessible to the entity that maintains it and to other government entities that need the data to perform their duties. Examples include trade secrets and proprietary commercial information submitted to government agencies, certain security data, attorney-client privileged communications of the entity, and data whose release would compromise security.

Protected nonpublic data not on individuals: the most restricted classification for non-individual data. Accessible only to the entity that maintains it and to entities that are specifically authorized by statute. Not available to the public or to other government entities except as specifically authorized.

The critical principle underlying this entire system is the default classification: all government data is public unless the legislature has enacted a specific provision classifying it otherwise. The default applies at both levels — data on individuals is public unless classified private or confidential, and data not on individuals is public unless classified nonpublic or protected nonpublic.

RIGHT OF ACCESS (Section 13.03)

All public government data must be made available for inspection and copying during normal working hours at the offices of the entity that maintains it. The entity must respond to requests for public data immediately if the data is readily available, or within a reasonable time if retrieval or compilation is needed. Unlike many states, the MGDPA does not specify a fixed deadline measured in business days. Instead, it requires that data be provided "immediately" when available and otherwise within a "reasonable time." Courts have interpreted this to mean that entities must respond promptly and without unnecessary delay, and unreasonable delays may be challenged.

No requester is required to identify themselves or state a purpose for requesting public data. The entity may not deny access based on the identity or purpose of the requester. The entity may not require that requests be submitted in a particular form or through a particular channel, though it may make request forms available as a convenience.

For private data on individuals, the data subject has the right to be informed of what private data the entity maintains about them, to inspect and obtain copies of their own private data, and to contest the accuracy or completeness of that data. The entity must establish a process for handling correction requests and must either make the requested correction or provide a written explanation for declining.

TENNESSEN WARNING (Section 13.04(2))

Whenever a government entity asks an individual to supply private or confidential data about themselves, the entity must provide a "Tennessen Warning" — an informational notice that tells the individual: the purpose and intended use of the data; whether the individual may refuse to supply the data; any known consequences of refusing; and the identity of other persons or entities authorized by law to receive the data. This notice requirement is a distinctive feature of Minnesota's data practices framework and provides individuals with informed consent before they provide personal information to the government.

FEES (Section 13.03(3))

An entity may charge fees for providing copies of public data. Permissible fees include: the actual cost of searching for, retrieving, and copying the data, including employee time at the hourly rate of the lowest-paid employee capable of performing the task. Most entities do not charge for the first one hundred pages of paper copies in standard requests.

For electronic copies, the entity may charge the cost of the storage medium. For data transmitted electronically by email, there is generally no charge.

The entity may not charge for the time or effort required to separate public from non-public data. That separation is the entity's obligation and its cost falls on the entity, not the requester.

If a request involves data of significant commercial value that was developed with a substantial expenditure of public funds, the entity may charge a reasonable fee that includes both the cost of providing the data and a reasonable portion of the development cost. This provision allows entities to recoup some of the investment in creating valuable datasets while still making the data available.

SPECIFIC DATA CLASSIFICATIONS

The MGDPA and related statutes contain hundreds of specific data classifications. Major categories include:

Personnel data (Section 13.43): Detailed classification rules for employment data. Public personnel data includes: name, employee identification number (but not social security number), actual gross salary and salary range, terms and conditions of employment, contract fees, job title and description, education and training background, previous work experience, dates of first and last employment, status and outcome of any disciplinary proceeding (at the conclusion of the proceeding), work location and telephone number, and badge number of law enforcement officers. Private personnel data includes: performance evaluations and related documentation, employee assistance program participation, certain medical data, and specific investigative information prior to final disposition.

Law enforcement data (Section 13.82): An elaborate classification scheme distinguishes between different types of law enforcement data. Arrest data (name, time, place, and nature of charges) is public. Active criminal investigative data may be classified as confidential during an investigation and becomes public upon completion of the investigation, subject to specific exceptions for informant identities, security-sensitive techniques, and safety concerns. Certain response, incident, and activity data is public, including records of calls for service.

Welfare data (Section 13.46): Data on individuals collected, maintained, used, or disseminated by welfare agencies is classified as private, with numerous specific sub-classifications addressing different types of welfare data and the circumstances under which it may be shared with other agencies.

Health data (Section 13.3805): Patient health records maintained by government health care entities are classified as private data on individuals, consistent with both state law and HIPAA.

Educational data (Section 13.32): Student records are classified as private, consistent with FERPA requirements.

Financial and commercial data (Section 13.37): Trade secret information and certain commercial financial data submitted to government agencies are classified as nonpublic or protected nonpublic data not on individuals.

Security data (Section 13.37): Data relating to security systems, emergency response plans, critical infrastructure vulnerabilities, and building security assessments is classified as nonpublic.

Attorney-client data (Section 13.393): Data protected by the attorney-client privilege is classified as protected nonpublic or as private, depending on whether it relates to an individual.

TEMPORARY CLASSIFICATION (Section 13.06)

If an entity encounters data that is not classified by any existing statute and believes that releasing the data would be inappropriate, it may request a temporary classification from the Commissioner of Administration. The entity must submit a written justification explaining why the data should be non-public. The temporary classification lasts until the legislature takes action on the classification — either adopting it permanently through legislation or allowing it to expire. This mechanism provides flexibility for addressing novel data types while maintaining legislative control over the classification system.

COMMISSIONER OF ADMINISTRATION (Sections 13.05, 13.06, 13.072)

The Commissioner of Administration, through the Data Practices Office within the Department of Administration, serves as the primary administrative authority for the MGDPA. The Commissioner's responsibilities include: issuing advisory opinions on the application of the MGDPA to specific data and situations; reviewing and approving or denying temporary classification requests; developing model policies, procedures, and training materials for government entities; maintaining a comprehensive compilation of all statutory data classifications (a critical resource given the number of classification provisions scattered through the statutes); providing mediation services for data practices disputes between entities and requesters; and reporting to the legislature on the state of data practices compliance.

Advisory opinions from the Commissioner are not legally binding but are highly persuasive. Courts frequently cite Commissioner opinions when interpreting the MGDPA. Government entities that follow Commissioner opinions in good faith receive a degree of protection from liability.

ENFORCEMENT AND REMEDIES (Sections 13.08, 13.09)

Any person aggrieved by a violation of the MGDPA may bring a civil action in district court. The action may seek a court order compelling compliance, damages, and attorney's fees.

If the court finds a violation, the government entity is liable for actual damages sustained by the aggrieved person, or a minimum statutory damage award of one thousand dollars if actual damages are less than that amount, plus costs of the action and reasonable attorney's fees. The minimum damage provision ensures that even violations causing minimal quantifiable harm result in a meaningful penalty.

If the violation was willful, the entity is liable for exemplary (punitive) damages of up to fifteen thousand dollars per violation, in addition to actual damages, costs, and attorney's fees. This exemplary damage provision provides a strong deterrent against deliberate noncompliance.

Government officials and employees who willfully violate the MGDPA may be subject to personal liability for damages. Willful violations by government employees are also classified as a misdemeanor offense. Conversely, employees who act in good faith in attempting to comply with the Act, and particularly those who rely on a written opinion from the Commissioner of Administration, are immune from personal liability.

DATA INVENTORY AND COMPLIANCE

Every government entity must prepare and maintain a publicly available document — often called a data inventory, data practices policy, or Tennessen notice list — that identifies all data collections maintained by the entity, states the classification of each collection, identifies the responsible authority, and describes the purposes for which each collection is maintained. This proactive transparency requirement is unusual among state public records laws and provides requesters with a detailed roadmap for identifying what data exists and how it is classified before they submit requests. The inventory must be updated when new data collections are created or existing classifications change.

Entities must also maintain written policies and procedures for processing data requests, handling data subject access and correction requests, ensuring data accuracy and security, and responding to data breaches. The Commissioner of Administration provides model policies and reviews entity compliance.'''

# =============================================================================
# MISSISSIPPI
# =============================================================================

MS_TEXT = '''Mississippi Public Records Act
Miss. Code Sections 25-61-1 through 25-61-17

PURPOSE AND POLICY (Section 25-61-1)

The Mississippi Public Records Act declares that it is the policy of the Legislature that public records are a resource belonging to the people of Mississippi and that the purpose of the Act is to provide for and ensure the efficient recovery and use of public records while safeguarding the privacy of individuals. The Act creates a presumption that public records are available for inspection by any person unless specifically exempted by statute. Mississippi courts construe the Act in favor of public access and strictly against the governmental body asserting an exemption. The burden of demonstrating that an exemption applies lies with the governmental body, not the requester.

Mississippi's public records law is less detailed in its procedural provisions than some states, reflecting a framework that relies on broad principles of openness supplemented by court interpretation. The Act establishes the fundamental right of access, defines the scope of that right, identifies categories of exempt records, and provides judicial remedies for denials. Agency-level implementation varies, but the statutory foundation applies uniformly to all public bodies.

DEFINITIONS (Section 25-61-3)

"Public body" means the State of Mississippi and any department, bureau, division, council, commission, committee, subcommittee, board, agency, or any other entity of the State, or any county, municipality, school district, or other political subdivision of the State, or any department, bureau, division, council, commission, committee, subcommittee, board, agency, or other entity of such political subdivision, or any public body corporate created under the laws of the State. The definition encompasses all three branches of state government (executive, legislative, and judicial), all local government bodies (counties, municipalities, school districts, and special districts), and any entity created by state law to serve a governmental function. The breadth of the definition ensures that entities performing governmental functions at any level cannot evade transparency obligations through organizational form.

"Public record" includes all documents, papers, letters, maps, books, tapes, photographs, films, sound recordings, or other material regardless of physical form or characteristic, having been used, being in use, or prepared, possessed, or retained for use in the conduct, transaction, or performance of any business, transaction, work, duty, or function of any public body, or required to be maintained by any public body. The definition is intentionally technology-neutral and includes electronic records, emails, text messages, database records, and any other form of recorded information created or received in connection with governmental business. Records stored on personal devices or in personal accounts are public records if they relate to the transaction of public business.

RIGHT OF ACCESS (Section 25-61-5)

Except as otherwise provided by law, all public records are available to any person for inspection, copying, and mechanical reproduction during the regular business hours of the office in which they are maintained. The Act does not limit access to Mississippi residents — any person, regardless of residence, citizenship, or identity, may request records. No person may be required to state the purpose or reason for requesting public records. The right of access is unconditional — the requester need not demonstrate a need, a reason, or an interest in the records beyond the desire to inspect them.

The public body must acknowledge receipt of a written request within one (1) working day and indicate whether the records will be produced or whether the request is being denied. The body then has up to seven (7) working days from receipt of the request to produce the records. If the request involves unusual circumstances — including the need to search multiple offices or storage locations, the volume of records requested, or the need to review records for exempt material — the response time may be extended to fourteen (14) working days with written notice to the requester explaining the specific basis for the extension.

The one-day acknowledgment and seven-day production framework provides a relatively structured timeline for access. If the public body fails to respond within the applicable time period, the request is deemed denied for purposes of judicial enforcement, allowing the requester to proceed directly to court without further delay.

Requests may be made in person, by mail, by fax, by email, or by any other written communication. The law does not require any particular form for requests, though agencies may provide request forms as a convenience. Agencies must accept requests in whatever written format the requester chooses.

FEES (Section 25-61-7)

A public body may charge a reasonable fee for copying public records. The fee must reasonably correspond to the actual cost of searching for, reviewing, and duplicating the records. Agencies may not impose fees designed to discourage requests or to generate revenue — fees must be limited to actual, documented costs.

For standard paper copies, the fee is typically set at a per-page rate reflecting actual copying costs, including paper, toner, and the cost of operating copying equipment. Agencies may also charge for mailing costs if the requester asks for records to be mailed rather than picked up in person.

For electronic records, the public body may charge the cost of the electronic storage medium (CD, USB drive, or similar) and the actual cost of duplication. The body may also charge for the time of personnel needed to search for, retrieve, and compile the requested records, at the actual hourly rate of the employee performing the work. However, the fee for staff time must reflect actual work performed, not estimated or standardized rates.

No fee may be charged for merely inspecting records at the agency's offices. The right of inspection is free. Only copying, duplication, and related services may generate charges.

If the estimated cost exceeds fifty dollars, the public body may require prepayment or a deposit before processing the request. The body must provide a good-faith written cost estimate to the requester before commencing work on any request that will generate significant fees.

EXEMPTIONS (Sections 25-61-9, 25-61-11, 25-61-12)

Mississippi's exemptions are relatively narrow compared to many states, reflecting the legislature's emphasis on openness. The Act and related statutes provide the following principal categories of exempt records:

Law enforcement records: Records that are part of an active criminal investigation or criminal intelligence investigation may be withheld during the pendency of the investigation to the extent that disclosure would interfere with the investigation, compromise investigative techniques, reveal the identity of confidential informants, or endanger the safety of law enforcement personnel or witnesses. Once the investigation results in a prosecution, the records become available subject to the rules of criminal procedure and the court's discretion. If no prosecution results, certain records may remain exempt if their disclosure would compromise future investigative capacity or endanger individuals. The exemption is not blanket — it must be applied record-by-record with specific justification for each withholding.

Attorney-client privileged communications: Communications between a public body and its attorneys that are protected by the attorney-client privilege or the work product doctrine are exempt from disclosure. The privilege covers confidential communications made for the purpose of obtaining or providing legal advice and attorney mental impressions, legal theories, and litigation strategies. However, the privilege does not extend to billing records, fee arrangements, retainer agreements, or the general subject matter of the legal representation — these are typically public records even if specific details of the legal advice may be redacted.

Personnel records: Certain records in state employee personnel files are exempt, including letters of recommendation submitted in confidence and records relating to disciplinary proceedings prior to their final disposition. Once disciplinary proceedings are concluded, the final disposition and the basis for the action become public records. Basic employment information — including the employee's name, position title, salary, dates of employment, and general job description — is always public. The exemption for personnel records is narrower than in many states, reflecting Mississippi's policy that the public has a strong interest in knowing how public employees are compensated and how they perform their duties.

Individual privacy: Records containing information of a personal nature, the disclosure of which would constitute a clearly unwarranted invasion of personal privacy, may be withheld. This exemption requires a case-by-case balancing of the individual's privacy interest against the public's interest in disclosure. The public body bears the burden of demonstrating that the privacy interest clearly outweighs the access interest. Information about the performance of public duties by public employees is generally not considered to implicate personal privacy. The "clearly unwarranted" standard is deliberately high and is designed to prevent routine invocations of privacy to defeat access.

Trade secrets and proprietary information: Commercial or financial information, including trade secrets, furnished to a public body under an express or implied promise of confidentiality, may be withheld if disclosure would cause competitive injury to the person or entity that furnished the information. The entity claiming the exemption must demonstrate both that the information qualifies as a trade secret or confidential commercial information and that actual competitive harm would result from disclosure. Generic or speculative claims of harm are insufficient.

Tax records: Individual and corporate tax return information filed with the Department of Revenue is confidential and may not be disclosed except as specifically authorized by the tax code. This exemption covers the returns themselves and the detailed financial information they contain, but does not extend to aggregate or statistical tax data that cannot be traced to individual taxpayers.

Court-sealed records: Records sealed by court order or made confidential by specific court order are exempt from disclosure. The court order must be specific and must identify the records to be sealed and the basis for sealing.

Medical records: Individual patient medical records maintained by public hospitals, public health facilities, and public health agencies are confidential under state health privacy laws and federal law (HIPAA). The confidentiality extends to records that could identify an individual patient, including billing and treatment records.

Juvenile records: Records of juvenile court proceedings and juvenile detention are confidential under Mississippi's Youth Court Act. Disclosure of juvenile records is permitted only in the circumstances specifically authorized by the Youth Court Act.

Academic testing materials: Test questions, scoring keys, and examination instruments used in professional licensing examinations and academic assessments are exempt to protect the validity and integrity of the testing process.

Executive session records: Minutes and records of executive sessions of public bodies conducted under the Mississippi Open Meetings Act (Section 25-41-1 et seq.) are not subject to public disclosure. However, the fact that an executive session was held, the statutory basis for the session, and the general topic discussed must be reflected in the public minutes of the meeting. No binding action may be taken in executive session — all votes must occur in open session.

DENIAL AND APPEAL PROCEDURES

When a public body denies a request in whole or in part, the denial must be in writing and must state the specific legal authority for the withholding, including the particular statutory exemption relied upon and a brief explanation of how the exemption applies to the records at issue. If only a portion of a record is exempt, the body must segregate the exempt material and release the non-exempt portions. The obligation to segregate and produce non-exempt material is affirmative — the body must redact exempt information and produce the remainder, rather than withholding entire records because they contain some exempt information. Blanket denials that do not cite specific exemptions or that fail to explain the basis for withholding are legally insufficient.

ENFORCEMENT AND REMEDIES (Section 25-61-13)

Any person aggrieved by a denial of access may institute a suit in the chancery court of the county in which the public body is located. The suit is heard on an expedited basis. The chancery court reviews the denial de novo, making its own independent determination of whether the records are subject to disclosure. The court may examine the disputed records in camera to evaluate the agency's exemption claims without disclosing the records to the requester during the litigation.

If the court finds that the public body improperly withheld records, the court shall order the records disclosed and shall award the prevailing requester reasonable attorney's fees and costs. The mandatory fee-shifting for prevailing requesters provides a meaningful economic incentive for compliance and helps ensure that the cost of enforcement does not fall solely on the individuals seeking access to records that should have been produced. If the court finds that the denial was made in bad faith or was willfully obstructive, additional sanctions may be imposed, including enhanced damages.

A public official who willfully and knowingly violates the Act may be subject to removal from office and a civil fine. Individual employees who act in good faith reliance on the advice of legal counsel are protected from personal liability. The removal-from-office remedy, while drastic, provides an ultimate sanction for the most egregious and persistent violations.

ELECTRONIC RECORDS

Public records maintained in electronic format are subject to the same access requirements as paper records. There is no separate classification or set of rules for electronic records — they are public records and must be produced upon request in the same manner as paper documents. The public body must provide records in the electronic format in which they are maintained if the requester asks for electronic copies. The body may not convert electronic records to paper to frustrate access, increase costs, or make the records less useful to the requester.

If fulfilling an electronic records request requires the body to extract data from a database or run a query, the body must do so if it can be accomplished using the body's existing software tools and programming capabilities. The body is not required to create a new software program, develop a custom database, or acquire new technology to satisfy a request. However, if the requested data can be retrieved through standard queries or existing reporting tools, the body must make the effort to produce it.

Email, text messages, instant messages, and other electronic communications created or received in connection with public business are public records regardless of the device or platform used. Records stored on personal devices or in personal email or cloud accounts are not exempt from disclosure merely because of their storage location.

RECORD RETENTION

Mississippi's records retention requirements are established by the Department of Archives and History, which sets retention schedules for all categories of public records at both the state and local level. Public bodies must follow approved retention schedules and may not destroy records outside of those schedules. Premature destruction of records is unlawful and may result in administrative sanctions and criminal penalties. Destruction of records that are the subject of a pending public records request, a litigation hold, or a known investigation is particularly serious and may give rise to spoliation sanctions, contempt findings, and other legal consequences.

The Department of Archives and History provides guidance and training to public bodies on records management, retention schedule development, and proper destruction procedures. Agencies are expected to maintain records in an organized and accessible manner that facilitates both internal use and public access.

RELATIONSHIP TO OPEN MEETINGS

The Public Records Act works in conjunction with Mississippi's Open Meetings Act (Section 25-41-1 et seq.). Minutes of public meetings are public records and must be produced upon request. Records that document the deliberations, discussions, and decisions of public bodies at open meetings must be maintained and made available. Executive session records are treated differently as described above — the content of executive session discussions may be confidential, but the fact that the session occurred, its statutory basis, and its general subject matter must be documented in the public minutes. All votes and binding actions must be taken in open session and recorded in the minutes.'''

DOCUMENTS = [
    {
        'id': 'ky-statute-open-records',
        'citation': 'KRS §§ 61.870–61.884',
        'title': 'Kentucky Open Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'KY',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Kentucky Open Records Act (ORA) providing broad public access to government records with a unique binding Attorney General opinion appeal process, a 5-business-day response deadline, enumerated exemptions strictly construed in favor of disclosure, $0.10/page copy fees, and mandatory attorney fee recovery for prevailing requesters.',
        'text': KY_TEXT,
    },
    {
        'id': 'la-statute-public-records',
        'citation': 'La. R.S. §§ 44:1–44:41',
        'title': 'Louisiana Public Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'LA',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Louisiana Public Records Law with constitutional right of access (Article XII, Section 3), a 3-business-day response period for electronic records, a strong presumption of openness with strictly construed exemptions, attorney fee recovery, civil penalties up to $100/day, and custodian removal for arbitrary noncompliance.',
        'text': LA_TEXT,
    },
    {
        'id': 'me-statute-foaa',
        'citation': '1 M.R.S.A. §§ 400–414',
        'title': 'Maine Freedom of Access Act (FOAA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'ME',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Maine Freedom of Access Act (FOAA) establishing public access to government records and proceedings with a 5-business-day response period, a Public Access Ombudsman for mediation, over 300 statutory confidentiality provisions, civil penalties for willful violations ($500-$5,000), and discretionary attorney fee awards.',
        'text': ME_TEXT,
    },
    {
        'id': 'md-statute-mpia',
        'citation': 'Md. Code, Gen. Prov. §§ 4-101–4-601',
        'title': 'Maryland Public Information Act (MPIA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'MD',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Maryland Public Information Act (MPIA) granting broad access to government records with a 10-business-day initial response requirement, mandatory and discretionary denial categories, a Public Access Ombudsman and Compliance Board, and mandatory attorney fees for arbitrary or capricious denials.',
        'text': MD_TEXT,
    },
    {
        'id': 'ma-statute-public-records',
        'citation': 'M.G.L. c. 66, §§ 10–10B; c. 66A',
        'title': 'Massachusetts Public Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'MA',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Massachusetts Public Records Law (substantially reformed in 2016) with a 10-business-day response requirement, $0.05/page copies, a Supervisor of Records with binding order authority, detailed fee limitations including 4 free hours of staff time, and punitive damages up to $5,000 for bad faith denials.',
        'text': MA_TEXT,
    },
    {
        'id': 'mi-statute-foia',
        'citation': 'MCL §§ 15.231–15.246',
        'title': 'Michigan Freedom of Information Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'MI',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Michigan Freedom of Information Act (FOIA) providing public access to government records with a 5-business-day response period (extendable by 10 days), detailed itemized fee requirements, discretionary exemptions, mandatory attorney fees, punitive damages up to $2,500 for willful violations, and personal civil fines up to $7,500.',
        'text': MI_TEXT,
    },
    {
        'id': 'mn-statute-mgdpa',
        'citation': 'Minn. Stat. Ch. 13',
        'title': 'Minnesota Government Data Practices Act (MGDPA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'MN',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Minnesota Government Data Practices Act (MGDPA) using a unique five-level data classification system (public, private, confidential, nonpublic, protected nonpublic) where all data is presumed public unless legislatively classified otherwise. Administered by the Commissioner of Administration with advisory opinions, temporary classification authority, and exemplary damages up to $15,000 for willful violations.',
        'text': MN_TEXT,
    },
    {
        'id': 'ms-statute-public-records',
        'citation': 'Miss. Code §§ 25-61-1–25-61-17',
        'title': 'Mississippi Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'MS',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Mississippi Public Records Act establishing public access to government records with a 1-day acknowledgment and 7-working-day production deadline (extendable to 14 days), relatively narrow exemptions for law enforcement, personnel, privacy, and trade secrets, mandatory attorney fee recovery for prevailing requesters, and custodian removal for willful violations.',
        'text': MS_TEXT,
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
