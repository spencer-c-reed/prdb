#!/usr/bin/env python3
"""Build state public records statute documents for ND, OH, OK, OR, PA, RI, SC, SD."""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

DOCUMENTS = [
    # =========================================================================
    # NORTH DAKOTA
    # =========================================================================
    {
        'id': 'nd-statute-open-records',
        'citation': 'N.D.C.C. §§ 44-04-17 through 44-04-21.3',
        'title': 'North Dakota Open Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'ND',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'North Dakota Open Records Law establishing broad public access to government records maintained by public entities, with enforcement through district court actions and attorney fee shifting for successful requesters.',
        'text': '''North Dakota Open Records Law
N.D.C.C. §§ 44-04-17 through 44-04-21.3

OVERVIEW AND LEGISLATIVE PURPOSE

North Dakota's Open Records Law is codified at Chapter 44-04 of the North Dakota Century Code. The statute establishes a broad presumption that all records maintained by public entities are open to public inspection and copying. The law reflects the state's policy that government transparency is essential to democratic accountability and that citizens must be able to review the records underlying governmental decisions. The North Dakota Attorney General plays a central advisory role in interpreting the law through non-binding opinions, and the legislature has periodically amended the statute to address emerging issues around electronic records, meeting transparency, and specific categories of exempt information.

DEFINITIONS AND SCOPE

Section 44-04-17.1 defines the key terms used throughout the chapter. A "public entity" includes every office, department, board, bureau, commission, association, or agency of the state or any political subdivision, as well as any organization supported in whole or in part by public funds or expending public funds. A "record" means recorded information of any kind, regardless of physical form or characteristics, that is maintained by a public entity. This includes paper documents, electronic files, emails, databases, photographs, audio and video recordings, and any other medium used to store information. The definition is intentionally technology-neutral so that it applies to new forms of record-keeping as they emerge.

The law's reach extends to records maintained by entities that receive public funding or that perform governmental functions, even if those entities are not traditional government agencies. Private organizations that receive substantial public funding or that carry out delegated governmental duties may be subject to the open records requirements with respect to the records related to those public functions.

RIGHT OF ACCESS

Section 44-04-18 establishes the core right of access. All records of a public entity are open and accessible for inspection during reasonable office hours. Any person has the right to inspect and obtain copies of public records regardless of the purpose of the request. The requester is not required to state a reason for wanting to see the records, and the public entity may not inquire into the requester's purpose as a condition of granting access. The right belongs to any person — there is no residency or citizenship requirement, and both individuals and organizations may exercise the right.

When a person requests to inspect records, the public entity must provide access promptly. If the records cannot be made available immediately, the entity must provide them within a reasonable time. The law does not specify rigid deadlines in the way some other states do, but the expectation is that compliance will be prompt and that delays must be justified by legitimate operational needs, not used as a tool to discourage requests.

Public entities must provide copies of records upon request. The entity may charge reasonable fees for copies, but fees may not exceed the actual cost of making the copies. Fees for search time and retrieval are generally not authorized unless specifically provided for by law. The entity may not impose excessive fees designed to deter requesters from obtaining records. If a record exists in electronic form, the entity should provide it in electronic form if the requester asks for it that way, and the entity may not charge more for an electronic copy than it would for a paper copy.

OPEN MEETINGS AND RECORDS INTERSECTION

North Dakota's open records provisions work in tandem with the state's open meetings law, also found in Chapter 44-04. Records generated by or for public entities in connection with meetings of governing bodies are generally public records subject to disclosure. Minutes, agendas, supporting materials distributed to members of governing bodies, and recordings of meetings are all accessible under the open records law. The interplay between the two transparency statutes means that records associated with executive sessions or closed meetings may be exempt from disclosure to the extent they fall within a recognized exemption, but the fact that a record was discussed in a closed session does not automatically make it exempt.

EXEMPTIONS FROM DISCLOSURE

Section 44-04-18.1 and related provisions identify specific categories of records that are exempt from mandatory disclosure. The exemptions are construed narrowly, and the burden falls on the public entity to demonstrate that a particular record falls within a recognized exemption. The following are among the principal categories of exempt records:

Attorney-client privileged records. Records protected by the attorney-client privilege are exempt from disclosure. This covers communications between a public entity and its legal counsel made for the purpose of obtaining legal advice. The privilege belongs to the entity, and the entity may choose to waive it and disclose the records. Work product prepared by attorneys in anticipation of litigation is also protected. However, the mere involvement of an attorney does not make a record privileged — the communication must have been made for the purpose of seeking or providing legal advice, and factual information does not become privileged simply because it was shared with an attorney.

Records protected by other statutes. Records that are made confidential or exempt by other provisions of the Century Code or by federal law are exempt. This includes, but is not limited to, medical and mental health records, certain tax records, juvenile records, adoption records, trade secrets submitted to a government entity, certain law enforcement investigative records, records relating to security measures and vulnerability assessments, social services records concerning individual cases, and records whose disclosure is prohibited by federal privacy statutes such as HIPAA, FERPA, or the federal Tax Code.

Personnel records. Certain personal information in the personnel files of public employees is exempt, including Social Security numbers, home addresses, home telephone numbers, and medical information. However, the names of public employees, their job titles, salaries, dates of employment, and records of disciplinary actions are public. The distinction is between sensitive personal data (exempt) and information about how public employees perform their public duties (public).

Active criminal investigation and intelligence records. Records compiled for law enforcement purposes that, if disclosed, would interfere with an active criminal investigation, reveal the identity of a confidential informant, or endanger the safety of law enforcement personnel or others may be withheld. Once an investigation is closed and the law enforcement purpose has been served, the records generally become available. Routine law enforcement records such as incident reports, arrest records, and booking information are public.

Records relating to negotiations. Records relating to labor negotiations, real estate negotiations, or other pending negotiations in which premature disclosure would give an unfair advantage to parties outside the government are temporarily exempt. Once the negotiations conclude, the records become public.

Security and infrastructure records. Records that, if disclosed, would reveal security measures, vulnerability assessments, emergency response plans, or critical infrastructure information that could be exploited to threaten public safety are exempt.

PROCEDURES FOR REQUESTING RECORDS

A request for records should be directed to the public entity that maintains the records. There is no required form for a request — it may be made orally or in writing. However, written requests are advisable because they create a clear record of what was requested and when. The request should describe the records sought with reasonable specificity so that the entity can identify and locate them, but the requester is not required to identify specific documents by name or file number. A request that describes the subject matter, time period, and type of records sought is generally sufficient.

The public entity should respond to the request as promptly as circumstances permit. If the entity determines that the requested records are exempt or that portions must be redacted, it must provide a written explanation identifying the specific statutory exemption relied upon. A blanket denial without identification of the applicable exemption is not sufficient. If a record contains both exempt and non-exempt information, the entity must segregate and release the non-exempt portions, redacting only the specifically exempt material.

ATTORNEY GENERAL OPINIONS

The North Dakota Attorney General issues advisory opinions on open records and open meetings questions. Any person may request an opinion, and the AG's office regularly publishes these opinions, which form a significant body of interpretive guidance. While AG opinions are not legally binding on courts, they are persuasive authority and are frequently cited by courts and relied upon by public entities. The AG's office has consistently interpreted the law in favor of transparency, construing exemptions narrowly and requiring public entities to demonstrate specific statutory authority for any withholding.

The AG opinion process provides a relatively quick and inexpensive way for requesters to get an authoritative interpretation of the law without filing a lawsuit. Public entities that follow AG opinions in good faith generally receive deference, although a court may reach a different conclusion in a contested case.

ENFORCEMENT AND REMEDIES

Section 44-04-21.2 provides for judicial enforcement. A person who is denied access to records may bring an action in the district court of the county where the records are maintained. The court reviews the denial de novo, meaning it makes its own independent determination rather than deferring to the agency's judgment. The court may inspect the records in camera (privately) to determine whether they are exempt. The burden of proof is on the public entity to demonstrate that the withheld records fall within a recognized exemption.

If the court finds that the records were improperly withheld, it will order their disclosure. The court may also award reasonable attorney's fees and costs to the requester if the requester substantially prevails, which provides a meaningful incentive for public entities to comply with the law and a mechanism for requesters to recover the cost of enforcing their rights. The availability of attorney fee shifting is important because it makes enforcement economically viable for individual citizens who might otherwise be unable to afford litigation against a government entity.

The court may also impose sanctions or other remedies if it finds that a public entity has willfully violated the open records law. Repeated or egregious violations may result in the court ordering institutional reforms to prevent future noncompliance.

ELECTRONIC RECORDS AND TECHNOLOGY

North Dakota's open records law applies to electronic records with the same force as it applies to paper records. Public entities may not deny access to a record solely because it is maintained electronically. If a record exists in electronic format, the entity must provide it in that format if the requester asks for it, provided that doing so does not require the entity to create a new record or write custom software. The entity may provide records in alternative electronic formats if the requested format is not feasible, but it must work with the requester to find a reasonable accommodation.

Public entities are expected to maintain their electronic record-keeping systems in a manner that facilitates public access. Records management practices should account for the preservation of electronic records, including email, text messages, and records stored in cloud-based systems, so that they remain accessible for inspection and copying.

RELATIONSHIP TO FEDERAL LAW

The North Dakota Open Records Law operates alongside federal transparency statutes, including the Freedom of Information Act (which applies only to federal agencies). When both state and federal records laws apply to the same records — for example, when a state agency holds records subject to federal privacy requirements — the more restrictive provision generally controls. Federal statutes such as HIPAA, FERPA, and the Internal Revenue Code may independently require that certain records be kept confidential, and compliance with those federal mandates is not a violation of the state open records law.

PRACTICAL CONSIDERATIONS

Requesters should be as specific as possible in describing the records they seek, as this facilitates prompt compliance and reduces the likelihood of disputes. Requesters should also be prepared to pay reasonable copying costs. If fees seem excessive, the requester may challenge them through the AG opinion process or in court. Public entities should train their staff on open records obligations, designate records custodians, and develop clear internal procedures for processing requests. Proactive disclosure — posting commonly requested records on agency websites — reduces the volume of individual requests and advances the law's transparency goals.'''
    },

    # =========================================================================
    # OHIO
    # =========================================================================
    {
        'id': 'oh-statute-public-records',
        'citation': 'R.C. §§ 149.43 through 149.437',
        'title': 'Ohio Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'OH',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Ohio Public Records Act providing broad public access to records maintained by public offices, with mandatory prompt disclosure, statutory damages for noncompliance, and attorney fee shifting for successful requesters in mandamus actions.',
        'text': '''Ohio Public Records Act
R.C. §§ 149.43 through 149.437

OVERVIEW AND LEGISLATIVE PURPOSE

Ohio's Public Records Act, codified at Revised Code Sections 149.43 through 149.437, establishes one of the more muscular public records access frameworks in the United States. The statute creates a broad right of access to records maintained by public offices and imposes significant penalties on public offices that fail to comply promptly. Ohio courts have consistently interpreted the Act as a remedial statute that should be construed liberally in favor of disclosure. The Ohio Supreme Court has repeatedly stated that the Act's purpose is to expose government activity to public scrutiny and that exemptions must be strictly construed against the public office seeking to withhold records.

DEFINITIONS

Section 149.43(A) provides the definitions that control the Act's scope. A "public record" means records kept by any public office, including state agencies, counties, municipalities, townships, school districts, and any other political subdivision or taxing authority. The term includes records maintained by persons performing governmental functions on behalf of public offices. Records include documents, devices, or items created, received, or maintained by a public office, regardless of physical form or characteristics — paper, electronic, photographic, or any other medium.

A "public office" includes every organized body, office, agency, institution, or entity established by the laws of the state for governmental purposes, as well as organized bodies that receive public funds and perform public functions. This broad definition ensures that entities performing governmental functions cannot evade transparency simply by adopting a non-governmental organizational structure.

RIGHT OF ACCESS AND RESPONSE REQUIREMENTS

Section 149.43(B) establishes the right of access and sets forth the obligations of public offices when responding to requests. All public records must be promptly prepared and made available for inspection at all reasonable times during regular business hours. Upon request, a public office must make copies of public records available at cost and within a reasonable period of time.

Ohio law does not require a requester to put a request in writing, identify themselves, or state the purpose of the request. The public office may not require a written request as a precondition to processing it, although a requester may choose to submit a request in writing. The office may not condition access on the requester's identity, organizational affiliation, or intended use of the records. This approach prevents public offices from using identity-based screening to deter requests from journalists, activists, or other disfavored requesters.

If a public office denies a request, it must provide the requester with an explanation, including the legal authority for the denial. The denial must identify the specific statutory exemption that applies. If only part of a record is exempt, the office must redact the exempt portions and release the remainder. An office may not deny an entire record when only a portion is exempt.

Ohio imposes a "prompt" response standard rather than a fixed number of days. What constitutes a prompt response depends on the volume and complexity of the request, but courts have found delays of weeks or months to be unreasonable in many circumstances. The Ohio Supreme Court has held that a public office has a duty to organize and maintain its records in a manner that makes them readily available for inspection and copying, and an office may not use its own disorganization as an excuse for delay.

EXEMPTIONS

Section 149.43(A)(1) lists the categories of records exempt from disclosure. Ohio's exemption framework is specific and detailed, and each exemption is narrowly construed. The principal exemptions include:

Medical records. Records that relate to the medical condition, diagnosis, care, or treatment of a patient, as maintained by a hospital, physician, or other medical professional, are exempt to protect patient privacy.

Trial preparation records. Records compiled by an attorney in anticipation of litigation or for trial are exempt. This covers work product and litigation strategy materials, but does not extend to underlying factual records that happen to have been gathered in connection with litigation.

Confidential law enforcement investigatory records. Records compiled for law enforcement purposes that, if released, would create a high probability of disclosure of specific investigative techniques not generally known to the public, or would endanger the life or physical safety of law enforcement personnel, a crime victim, a witness, or a confidential informant, are exempt. Routine law enforcement records — incident reports, arrest records, booking photographs, 911 call logs, police dispatches — are generally public and not covered by this exemption.

Records protected by attorney-client privilege. Communications between a public office and its attorneys that are subject to the attorney-client privilege are exempt.

Security and infrastructure records. Records the release of which would threaten public security, including security plans, vulnerability assessments, and emergency response protocols, are exempt.

Trade secrets and proprietary business information. Trade secrets submitted to a public office and records containing proprietary business information are exempt if disclosure would cause competitive harm.

Personal information. Certain personal information — Social Security numbers, tax identification numbers, and certain financial information — is exempt. Ohio has also created specific exemptions for personal information in various contexts, such as concealed carry permit records, certain victim information, and donor information for public charities.

Additional exemptions exist for records pertaining to adoption, juvenile proceedings, grand jury proceedings, certain infrastructure and utility records, and other specific categories. Each exemption must be evaluated on a record-by-record basis, and the public office bears the burden of establishing that a specific exemption applies.

FEES AND COSTS

Public offices may charge for copies at their actual cost. This includes the cost of paper, toner, and media for electronic copies. Offices may not charge for the labor involved in searching for, retrieving, or reviewing records. The prohibition on labor charges is an important feature of Ohio law that distinguishes it from many other states, as it prevents offices from using inflated labor charges to deter requests. If records are provided electronically, the charge is limited to the cost of the medium (disc, USB drive) or transmission.

ENFORCEMENT: MANDAMUS AND STATUTORY DAMAGES

Ohio provides a powerful enforcement mechanism through mandamus actions in the Court of Claims or in a court of common pleas. Section 149.43(C) establishes that a person who is aggrieved by a failure to comply with the Act may commence a mandamus action. The court's review is de novo, and the public office bears the burden of demonstrating that an exemption applies.

If the court orders disclosure, it shall award the requester reasonable attorney's fees. This mandatory fee shifting is significant — unlike many states where fee awards are discretionary, Ohio requires them when the requester prevails. The availability of mandatory attorney's fees makes enforcement economically viable and gives requesters strong leverage in disputes.

Section 149.43(C)(2) also provides for statutory damages. If the court finds that the public office failed to comply with its obligations, the court may award the requester statutory damages of $100 per business day of unexcused delay, up to a maximum of $1,000. The damages provision adds a financial penalty beyond attorney's fees and serves as a deterrent against foot-dragging by public offices.

In addition, courts may impose court costs on the public office and may issue orders requiring the office to adopt specific procedures to prevent future violations.

TRAINING AND COMPLIANCE

Section 149.43(E) requires public offices to designate a person or persons responsible for public records and to establish procedures for handling requests. Each public office must adopt a public records policy and make it available to the public. Public offices are required to post a notice in a conspicuous location at the office informing the public of their right to access public records.

Ohio law also requires that elected officials and their designees complete a public records training program within a specified period after taking office. This training requirement is designed to ensure that the officials responsible for records decisions understand their obligations under the Act.

PUBLIC RECORDS REQUESTS IN LITIGATION

Ohio's Public Records Act operates independently of litigation discovery. The right of access under the Act is not affected by the existence of pending litigation, and a party in litigation may use the Act to obtain records from a public office that is not a party to the litigation. However, courts have recognized that a party may not use the Act as an end-run around discovery rules when the records are relevant to pending litigation between the requester and the public office.

ELECTRONIC RECORDS

The Act applies to records in any format, including electronic records. Public offices must provide records in the format requested if the records exist in that format. If a record exists only in electronic form, the office may not refuse to provide it simply because producing it requires extracting data from a database or running a report. However, the office is not required to create new records or perform analysis that it would not otherwise perform.

Email and text messages sent or received by public officials and employees in connection with public business are public records, even if stored on personal devices. The use of personal email accounts or messaging apps to conduct public business does not shield those communications from disclosure.

RELATIONSHIP TO OTHER LAW

The Public Records Act is the primary vehicle for public access to government records in Ohio, but other statutes may also authorize or restrict access to specific types of records. When a specific statute conflicts with the Public Records Act, the specific statute generally controls. The Act also operates alongside Ohio's open meetings law (the Sunshine Law, R.C. 121.22), and records associated with public meetings are generally subject to the Public Records Act.

Federal privacy statutes, including HIPAA, FERPA, and the Internal Revenue Code, may independently restrict disclosure of certain records held by public offices, and compliance with those federal mandates does not violate the state Act.

RETENTION AND RECORDS MANAGEMENT

Ohio's records retention framework interacts directly with the Public Records Act. Public offices are required to adopt records retention schedules that specify how long different categories of records must be maintained. These schedules are developed by the individual office and approved by the appropriate records commission (State Records Commission for state agencies, County Records Commission for county offices, etc.). A record that is subject to a retention schedule may not be destroyed before the scheduled retention period expires, and the existence of a pending records request generally requires the office to preserve the requested records regardless of the retention schedule. Premature destruction of records that are subject to a records request may result in sanctions, adverse inferences in litigation, and other consequences.

Public offices must maintain their records in a manner that facilitates retrieval and production. An office may not use its own poor records management practices as a defense to a records request. Courts have held that a public office has an affirmative duty to organize its records so that they can be made available for inspection and copying without unreasonable delay. The Ohio Supreme Court has emphasized that the obligation to maintain accessible records is a fundamental component of the Act's transparency mandate.

INTERPLAY WITH PRIVACY AND DATA PROTECTION

Ohio's Public Records Act contains specific provisions addressing the tension between transparency and individual privacy. The Act does not include a general privacy exemption — instead, it relies on specific, enumerated exemptions to protect privacy interests. This approach means that records are presumed public unless they fall within a specific exemption, and general assertions of privacy without a statutory basis are insufficient to justify withholding.

However, courts have recognized that the Act must be read in harmony with other laws that protect personal information. For example, records that contain Social Security numbers, financial account numbers, or other identity-theft-sensitive data may be redacted even when the underlying record is public. Ohio law independently prohibits the inclusion of Social Security numbers in publicly filed court documents and government records accessible to the public.

The intersection of the Public Records Act with federal laws such as HIPAA, FERPA, and the Privacy Act of 1974 creates additional complexity. When a federal privacy statute independently restricts disclosure of specific categories of information held by a public office, that federal restriction is generally treated as superseding the Public Records Act with respect to that specific information, but does not exempt the remainder of the record from disclosure.

PRACTICAL GUIDANCE

Requesters should describe the records they seek with reasonable specificity. While a requester need not identify specific documents by name, a description of the subject matter, time period, and type of records sought facilitates prompt compliance. Requesters should note the date and time of their request, as the timeline of the office's response is relevant to any subsequent mandamus action. If a request is denied, the requester should demand a written explanation citing the specific statutory exemption. Public offices should respond promptly, err on the side of disclosure, segregate and redact exempt information rather than withholding entire records, and maintain records in a manner that facilitates access. Given the mandatory fee-shifting and statutory damages provisions, public offices that deny requests without a solid legal basis face meaningful financial consequences, which provides a strong incentive for compliance.'''
    },

    # =========================================================================
    # OKLAHOMA
    # =========================================================================
    {
        'id': 'ok-statute-open-records',
        'citation': '51 O.S. §§ 24A.1 through 24A.30',
        'title': 'Oklahoma Open Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'OK',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Oklahoma Open Records Act declaring that all records of public bodies and public officials are open to any person for inspection and copying, with narrowly construed exemptions and enforcement through district court actions with attorney fee awards.',
        'text': '''Oklahoma Open Records Act
51 O.S. §§ 24A.1 through 24A.30

OVERVIEW AND LEGISLATIVE DECLARATION

The Oklahoma Open Records Act, codified at Title 51, Sections 24A.1 through 24A.30 of the Oklahoma Statutes, declares as state policy that the people of Oklahoma are entitled to know the activities of their government. Section 24A.2 articulates the legislative finding that openness in government is essential to a democratic society and that public records belong to the people. The Act is to be construed broadly in favor of disclosure and narrowly with respect to any limitations on access. Oklahoma courts treat the Act as remedial legislation and resolve ambiguities in favor of the requester.

DEFINITIONS

Section 24A.3 defines the terms that control the Act's scope. A "record" means all documents, photographs, recordings, or other material regardless of physical form or characteristics, created by, received by, under the authority of, or coming into the custody of a public body or public official in connection with the transaction of public business. The definition is format-neutral and encompasses paper, electronic, photographic, and audio or video materials.

A "public body" includes the state and all its agencies, offices, departments, boards, commissions, committees, and subcommittees, as well as counties, cities, towns, townships, school districts, and all other political subdivisions and their agencies. It also includes entities supported in whole or in part by public funds or expending public funds, and entities created by state or local authority to perform governmental functions. A "public official" means any official or employee of a public body.

RIGHT OF ACCESS

Section 24A.5 establishes the fundamental right. All records of public bodies and public officials are open to any person for inspection, copying, or mechanical reproduction during regular business hours. The right belongs to "any person" — no residency requirement, no organizational affiliation, and no obligation to state a purpose. The public body may not require the requester to identify themselves or explain why they want the records.

Upon receiving a request, the public body must provide prompt, reasonable access to its records. The Act does not set a specific number of days for response, but the requirement of prompt access means that unreasonable delays constitute a violation. If records cannot be produced immediately due to their volume or the need to retrieve them from storage, the public body should communicate a reasonable timeline to the requester.

If the public body determines that a record or portion of a record is confidential, it must provide a written statement identifying the specific provision of law that authorizes confidentiality. A public body may not simply refuse to produce records without citing specific legal authority.

COPYING FEES

Section 24A.5 authorizes public bodies to charge a reasonable fee for copies. The fee must not exceed the actual direct cost of document copying. Search fees may be charged only if specifically authorized by statute. The Act prohibits public bodies from using fees as a barrier to access. If records are available electronically, they should be provided in electronic form upon request, and the fee should reflect the actual cost of the medium or transmission, not an inflated charge designed to discourage electronic access.

EXEMPTIONS AND CONFIDENTIAL RECORDS

Sections 24A.7 through 24A.16 and various other provisions throughout the Oklahoma Statutes identify categories of records that are confidential or exempt from the Act. The exemptions must be strictly construed, and the burden of establishing that an exemption applies rests on the public body. The principal exemption categories include:

Personnel records. Section 24A.7 addresses personnel records of public bodies. The following information about public employees is public: name, position, title, gross salary (including any incentive payments, allowances, or benefits), and dates of employment. Personal information in personnel files — such as Social Security numbers, home addresses, home telephone numbers, and evaluations or other information that, if released, could constitute a clearly unwarranted invasion of personal privacy — may be kept confidential. The balance struck is that the public has a right to know who works for the government, what they are paid, and what positions they hold, but personal data unrelated to the performance of public duties is protected.

Law enforcement records. Section 24A.8 addresses law enforcement records. Certain investigative records compiled for law enforcement purposes may be withheld if disclosure would interfere with an investigation, deprive a person of a fair trial, reveal the identity of a confidential source, disclose investigative techniques not generally known, or endanger the safety of law enforcement personnel. However, completed investigation reports, arrest records, booking records, and other routine law enforcement records are public. The "investigative records" exemption applies only during the active investigation phase and does not permanently shield records once the investigation concludes.

Personal privacy. Records whose disclosure would constitute a clearly unwarranted invasion of personal privacy are exempt. This balancing test requires the public body (and ultimately the court) to weigh the public interest in disclosure against the privacy interest of the individual. Information about the performance of public duties by public officials and employees generally does not implicate a significant privacy interest.

Attorney-client privileged communications. Communications between a public body and its attorney that are protected by the attorney-client privilege are confidential. Work product prepared in anticipation of litigation is also protected.

Trade secrets and proprietary information. Trade secrets and confidential commercial or financial information submitted to a public body are exempt if disclosure would cause competitive harm.

Other statutory confidentiality provisions. Records made confidential by specific provisions of state or federal law are exempt. These include, among others, certain tax records, juvenile records, adoption records, medical and mental health records protected by HIPAA, student records protected by FERPA, and records relating to security measures and critical infrastructure.

SEGREGATION AND REDACTION

When a record contains both public and confidential information, the public body must segregate the confidential portions and release the remainder. A public body may not withhold an entire record when only a portion is confidential. Redaction must be limited to the specific information covered by the exemption.

ENFORCEMENT AND REMEDIES

Section 24A.17 provides for enforcement through district court actions. Any person denied access to records may bring a civil action in the district court of the county where the records are maintained. The court reviews the matter de novo and may examine the records in camera. The burden of proof is on the public body to justify its refusal to disclose.

If the court finds that the public body violated the Act, it shall order disclosure of the records. The court shall also award the requester reasonable attorney's fees and costs if the requester substantially prevails. The availability of attorney fees is critical to making enforcement practical for individual citizens.

The court may also impose civil penalties. A public body or official that willfully violates the Act may be subject to penalties. Section 24A.17 authorizes the court to impose sanctions and to order the public body to adopt procedures to prevent future violations.

In addition to court enforcement, the Oklahoma District Attorneys Council and the Oklahoma Attorney General may investigate complaints of violations and take appropriate action.

RELATIONSHIP TO OPEN MEETINGS ACT

The Open Records Act works in conjunction with the Oklahoma Open Meeting Act (25 O.S. §§ 301-314). Records generated in connection with meetings of public bodies — including minutes, agendas, and supporting materials — are subject to the Open Records Act. The two statutes together form a comprehensive transparency framework, and they share interpretive principles: both are construed liberally in favor of openness.

ELECTRONIC RECORDS

The Act applies to records in all formats, including electronic records. Email, text messages, social media communications, databases, and other electronic records created or received by public bodies in connection with public business are public records subject to the Act. The use of personal devices or accounts to conduct public business does not exempt those communications from the Act's requirements. Public bodies must maintain their electronic records in a manner that facilitates access and must produce electronic records in electronic format upon request when they exist in that format.

DISTRICT ATTORNEYS COUNCIL AND ATTORNEY GENERAL ROLE

The Oklahoma District Attorneys Council and the Oklahoma Attorney General both play roles in enforcing and interpreting the Open Records Act. The Attorney General has the authority to investigate complaints about violations and to issue opinions interpreting the Act. AG opinions, while advisory rather than binding, carry significant persuasive weight and are frequently relied upon by courts and public bodies. The AG's office has consistently interpreted the Act in favor of transparency and has issued numerous opinions clarifying the scope of exemptions, the obligations of public bodies, and the rights of requesters.

The District Attorneys Council provides training and guidance to local government officials on open records compliance. District attorneys in individual counties may also investigate and prosecute criminal violations of the Act. Section 24A.17 provides that any person who willfully violates the Act is guilty of a misdemeanor, which gives the Act criminal enforcement teeth beyond the civil remedies available to individual requesters.

RECORDS RETENTION AND PRESERVATION

Oklahoma's records retention requirements interact with the Open Records Act to create a comprehensive framework for government transparency. Public bodies are required to maintain records in accordance with retention schedules approved by the State Records Administrator or the appropriate local records authority. Records subject to a retention schedule may not be destroyed before the retention period expires, and destruction of records in the face of a pending records request may constitute a violation of the Act and may result in sanctions in subsequent litigation.

The duty to preserve records extends to electronic records, including email and other electronic communications. Public bodies must adopt and implement records management practices that ensure electronic records are preserved, organized, and accessible for the duration of their required retention period. The increasing use of electronic communication by government officials has created new challenges for records retention, and the Act's requirements apply with equal force to electronic records.

SPECIAL CATEGORIES: CONTRACTS, FINANCIAL RECORDS, AND SALARIES

Oklahoma law places particular emphasis on the public availability of government financial records and contract information. Records documenting the expenditure of public funds — including purchase orders, invoices, contracts with vendors and consultants, grant disbursements, and payroll records — are among the most commonly requested categories and are firmly within the Act's disclosure mandate. Public bodies may not insert confidentiality clauses into government contracts that would override the Act's requirements, and the terms of government contracts with private parties are public records.

Salary and compensation information for public employees is expressly public under Section 24A.7. This includes not only base salary but also any additional compensation such as stipends, bonuses, car allowances, housing allowances, and benefits paid by the public body. The public's right to know what its employees are paid is a bedrock principle of the Act and may not be circumvented through creative compensation structures or by routing payments through intermediary entities. Courts and the Attorney General have consistently held that all forms of compensation derived from public funds are subject to disclosure regardless of how they are characterized by the public body.

Contracts between public bodies and private vendors, consultants, and service providers are public records subject to the Act. Public bodies may not insert confidentiality clauses into government contracts that would override the Act's disclosure requirements. While specific trade secrets embedded within contract attachments may be protected under the trade secrets exemption, the core terms of any government contract — including the identity of the contracting parties, the scope of services, the compensation paid, the duration, and the performance requirements — are always subject to public inspection and copying.

PRACTICAL CONSIDERATIONS

Requesters should describe the records they seek with reasonable specificity, noting the subject matter, time period, and type of records. Written requests are advisable to create a record of the request and its date. If access is denied, the requester should demand a written explanation citing the specific statutory exemption. Requesters should be aware that the Act provides for both civil and criminal enforcement, giving requesters multiple avenues for challenging improper denials. Public bodies should train staff on the Act's requirements, designate records custodians, respond promptly, and err on the side of disclosure. Proactive publication of commonly requested records on government websites reduces the burden of individual requests and advances the Act's transparency goals.'''
    },

    # =========================================================================
    # OREGON
    # =========================================================================
    {
        'id': 'or-statute-public-records',
        'citation': 'ORS §§ 192.311 through 192.478',
        'title': 'Oregon Public Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'OR',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Oregon Public Records Law establishing the right of public access to government records with a detailed exemption framework, fee provisions, an elected Attorney General petition process, and enforcement through circuit court orders with discretionary attorney fee awards.',
        'text': '''Oregon Public Records Law
ORS §§ 192.311 through 192.478

OVERVIEW AND PURPOSE

Oregon's Public Records Law, codified at Oregon Revised Statutes Sections 192.311 through 192.478, provides for public access to the records of state and local government. The statute reflects the principle that democratic governance requires an informed citizenry with access to information about government activities. Oregon courts apply a presumption of disclosure and construe exemptions narrowly against the governmental body seeking to withhold records. The law has been substantially amended and reorganized over the years to address emerging transparency issues, fee disputes, electronic records, and the role of the Attorney General in resolving records disputes.

DEFINITIONS

Section 192.311 defines the key terms. A "public record" includes any writing that contains information relating to the conduct of the public's business, including every account, voucher, and contract, and is prepared, owned, used, or retained by a public body regardless of physical form or characteristics. "Writing" is defined broadly to include handwriting, typewriting, printing, photographing, and every other means of recording, including letters, words, pictures, sounds, or symbols, or combinations thereof, and all papers, maps, files, facsimiles, or electronic recordings.

A "public body" includes every state officer, agency, department, division, bureau, board, and commission; every county, city, school district, and special district; and any other public or private body that receives public funding and is subject to audit by the Secretary of State. The definition also encompasses advisory bodies, committees, and subcommittees of public bodies.

RIGHT OF ACCESS AND REQUEST PROCEDURES

Section 192.314 establishes the fundamental right: every person has a right to inspect any public record of a public body. This right is not conditioned on the requester's identity, residency, or purpose. A public body may not require a requester to explain why they want the records.

Requests may be made orally or in writing, although written requests are advisable. The public body must respond within the timeframes established by the statute. Section 192.329 requires the public body to respond to a request within five business days of receiving it. The response must either provide the records, acknowledge the request and provide an estimated date for compliance, assert that the records are exempt, or state that the public body is the custodian but needs additional time or clarification. If additional time is needed, the body must provide a reasonable estimated completion date.

If the public body denies a request in whole or in part, it must provide a written statement identifying the specific exemption or exemptions that justify the denial. A public body that fails to respond within the five-business-day window is deemed to have denied the request for purposes of appeal.

FEES

Oregon's fee provisions, found in Sections 192.324 and 192.329, are among the more detailed in the country. A public body may charge fees reasonably calculated to reimburse for the actual cost of making the records available. This includes the cost of staff time spent searching for, reviewing, and segregating the records, as well as the cost of copying. The public body must provide an estimate of fees before incurring them if the estimated cost exceeds $25.

Fee waivers or reductions are available when the request is in the public interest. If furnishing copies of the records is in the public interest because making the records available primarily benefits the general public, the public body must reduce or waive fees. Disputes about fees may be appealed to the Attorney General or resolved in court.

Public bodies may not charge fees that are designed to discourage requests. The fee must reflect actual costs, and a public body that inflates fees or imposes unreasonable fees may be ordered to reduce them and may face other consequences.

EXEMPTIONS

Oregon's exemption framework is extensive, with exemptions found both within the Public Records Law itself and scattered throughout the Oregon Revised Statutes. Section 192.345 lists conditional exemptions — records that are exempt from disclosure unless the public interest requires disclosure. Section 192.355 lists unconditional exemptions — records that must be withheld regardless of the public interest. The distinction between conditional and unconditional exemptions is important because it determines whether a balancing test applies.

Conditional exemptions (Section 192.345) include:

Internal advisory communications. Records that consist of advice, opinions, and deliberative materials prepared by agency staff for the purpose of decision-making are conditionally exempt. This exemption protects the deliberative process by encouraging frank internal discussion. However, factual information within such records is generally not exempt, and the exemption does not apply after the decision has been made and the deliberative purpose has been served.

Investigatory information. Information compiled for the purpose of investigation that, if disclosed, would prejudice the ability to conduct an investigation, interfere with an enforcement proceeding, or reveal information that would enable circumvention of the law is conditionally exempt.

Personal privacy information. Information whose disclosure would constitute an unreasonable invasion of privacy is conditionally exempt. This requires a balancing of the privacy interest against the public interest in disclosure.

Trade secrets. Trade secrets submitted to a public body are conditionally exempt if disclosure would cause competitive harm.

Unconditional exemptions (Section 192.355) include:

Communications privileged under law. Attorney-client communications, physician-patient records, and other legally privileged communications are unconditionally exempt.

Records specifically made confidential by federal or state law. Records whose confidentiality is required by specific provisions of law, including HIPAA-protected health records, FERPA-protected student records, tax return information, and juvenile records, are unconditionally exempt.

Personnel discipline records. Records relating to proposed disciplinary action against a public employee are unconditionally exempt until the action is finalized. Once discipline is imposed, the records become public to the extent they are not otherwise exempt.

For all exemptions, the public body bears the burden of establishing that the exemption applies. If a record contains both exempt and non-exempt information, the body must segregate the exempt portions and release the rest.

ATTORNEY GENERAL PETITION PROCESS

Oregon provides a distinctive administrative remedy through the Attorney General. Section 192.407 through 192.431 establish a petition process by which a requester who has been denied records may petition the Attorney General to review the denial. The AG reviews the request, obtains the records from the public body, and issues an order either requiring disclosure or upholding the denial. The AG's orders are binding on public bodies unless overturned on appeal.

This petition process provides a relatively inexpensive and accessible alternative to litigation. There is no filing fee, and the process is designed to be completed within a reasonable timeframe. The AG's office has developed substantial expertise in public records law through this process, and its orders form a body of interpretive guidance.

A party dissatisfied with the AG's order may appeal to circuit court. The court reviews the AG's order de novo.

ENFORCEMENT AND JUDICIAL REMEDIES

Section 192.431 and related provisions govern judicial enforcement. A person may bring an action in circuit court to compel disclosure of records. The court reviews the denial de novo and may examine the records in camera. The burden of proof is on the public body to establish that an exemption applies.

If the court orders disclosure, it may in its discretion award reasonable attorney fees to the requester. The discretionary nature of fee awards in Oregon is less favorable to requesters than mandatory fee-shifting states, but courts regularly exercise this discretion in favor of requesters who prevail, particularly when the public body's position was unreasonable.

The court may also award costs and may impose other appropriate remedies, including injunctive relief to prevent ongoing violations.

ELECTRONIC RECORDS AND DATA

The Public Records Law applies to records in all formats, and public bodies must produce electronic records in the format requested if they exist in that format. If a record exists in a database, the public body must extract the requested data and provide it in a usable format if doing so can be accomplished using the body's existing technology without creating a new record. Email and electronic communications related to public business are public records regardless of the device or account used to create or store them.

RELATIONSHIP TO OPEN MEETINGS LAW

Oregon's Public Records Law operates alongside the Oregon Public Meetings Law (ORS 192.610-192.695). Records generated in connection with public meetings — minutes, agendas, supporting materials, and recordings — are subject to the Public Records Law. Records discussed in executive session may be exempt from disclosure to the extent they fall within a recognized exemption, but the fact that information was discussed in closed session does not independently create an exemption.

SPECIAL PROVISIONS FOR LAW ENFORCEMENT AND CRIMINAL JUSTICE RECORDS

Oregon's Public Records Law contains specific provisions addressing law enforcement and criminal justice records that go beyond the general investigatory records exemption. District attorney files, grand jury records, and records relating to pending criminal prosecutions are subject to specific confidentiality requirements. However, basic law enforcement records — arrest reports, booking information, incident reports, and records of dispatched calls — are generally public. The Oregon Department of Justice has issued guidance clarifying the boundaries between records that are available to the public and those that are legitimately exempt due to ongoing investigative or prosecutorial needs.

Oregon law also addresses the public availability of body camera footage, surveillance recordings, and other law enforcement audio and video recordings. These recordings are generally public records subject to the Act, but may be subject to redaction or delayed release to protect the identities of victims, witnesses, or undercover personnel, or to avoid interference with ongoing investigations. The specific rules for these recordings have been refined by legislative amendments in recent years in response to public demand for greater transparency in policing.

RECORDS MANAGEMENT AND RETENTION

Oregon's records retention framework, administered by the State Archivist, requires state and local agencies to adopt and follow retention schedules. Records subject to an approved retention schedule may not be destroyed before the scheduled retention period expires. The retention framework interacts with the Public Records Law by ensuring that records remain available for public access throughout their required retention period. Destruction of records in the face of a pending records request constitutes a violation and may result in sanctions or adverse inferences in litigation.

The State Archivist provides guidance to agencies on records management best practices, including the preservation of electronic records, email, and social media records. Agencies are expected to maintain records management systems that facilitate both internal operations and public access.

FEE DISPUTES AND PUBLIC INTEREST WAIVERS

Oregon's detailed fee provisions have generated substantial litigation and AG opinions. The requirement that fees be "reasonably calculated to reimburse" for actual costs means that public bodies must be able to justify their fee calculations. Courts and the AG have held that inflated fees, charges for time spent on activities other than search and retrieval, and fees calculated using the salary of the highest-ranking employee involved (rather than the employee who actually performed the work) are not permissible.

The public interest fee waiver is a significant feature of Oregon law. When a request is made by a representative of the news media, a nonprofit organization, or an individual whose request primarily benefits the general public, the public body must consider whether to waive or reduce fees. The determination of whether a request primarily benefits the public involves evaluating the nature of the information sought and its likely use. Requests for information about government spending, public safety, environmental conditions, and other matters of broad public concern are strong candidates for fee waivers. Disputes about fee waivers may be appealed to the AG or resolved in court, and the AG has issued numerous orders addressing fee waiver requests.

PRACTICAL GUIDANCE

Requesters should make written requests, describe the records sought with reasonable specificity, note the date and method of submission, and request a fee estimate before the body incurs costs. If denied, requesters should demand a written explanation and consider filing a petition with the Attorney General before resorting to litigation — the AG petition process is free and relatively fast. Public bodies should respond within the five-business-day window, cite specific exemptions when denying access, segregate and redact rather than withhold entirely, provide reasonable fee estimates, and consider fee waivers for public-interest requests. The distinction between conditional and unconditional exemptions is important for both requesters and public bodies: conditional exemptions are subject to a public-interest override, while unconditional exemptions are not.'''
    },

    # =========================================================================
    # PENNSYLVANIA
    # =========================================================================
    {
        'id': 'pa-statute-rtkl',
        'citation': '65 P.S. §§ 67.101 through 67.3104',
        'title': 'Pennsylvania Right-to-Know Law (RTKL)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'PA',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Pennsylvania Right-to-Know Law providing broad access to records of Commonwealth and local agencies through a structured request process, designated Open Records Officers, administrative appeals to the Office of Open Records (or legislative/judicial equivalents), and enforcement through Commonwealth Court review.',
        'text': '''Pennsylvania Right-to-Know Law (RTKL)
65 P.S. §§ 67.101 through 67.3104

OVERVIEW AND LEGISLATIVE PURPOSE

Pennsylvania's Right-to-Know Law (RTKL), enacted in its current form in 2008 as a comprehensive overhaul of the prior 1957 law, is codified at 65 P.S. Sections 67.101 through 67.3104. The RTKL establishes a presumption that records in the possession of a Commonwealth or local agency are public records and creates a structured process for requesting, receiving, appealing, and enforcing access to those records. The 2008 overhaul fundamentally shifted the burden of proof from the requester to the agency: under the current law, if the agency wants to deny a request, it bears the burden of proving by a preponderance of the evidence that the record is exempt. The law reflects the General Assembly's recognition that public access to government records is essential to democratic accountability.

DEFINITIONS

Section 67.102 defines the controlling terms. A "record" means information, regardless of physical form or characteristics, that documents a transaction or activity of an agency and is created, received, or retained pursuant to law or in connection with a transaction, business, or activity of the agency. The definition encompasses paper documents, electronic files, emails, photographs, maps, recordings, and any other form of documented information.

A "Commonwealth agency" means any office, department, authority, board, multistate agency, commission, or similar governmental entity of the Commonwealth, as well as any judicial agency and legislative agency. A "local agency" means any political subdivision, intermediate unit, charter school, cyber charter school, municipal authority, or similar local governmental entity. The RTKL thus covers the full spectrum of state and local government.

An "agency" is further defined to include entities performing a governmental function, which means that quasi-governmental organizations and authorities are subject to the law even if they are not traditional government offices.

OPEN RECORDS OFFICERS

Section 67.502 requires each agency to designate an Open Records Officer (ORO) who is responsible for receiving and processing requests. The ORO serves as the point of contact for requesters and is the official who makes the initial determination on whether to grant or deny a request. The ORO must be identified by name and contact information, which the agency must make publicly available. The ORO designation ensures accountability and provides requesters with a clear path for submitting requests.

REQUEST PROCEDURES

Section 67.702 establishes the requirements for submitting a request. A request must be in writing and must be submitted to the agency's designated ORO. The request must identify or describe the records sought with sufficient specificity to enable the agency to ascertain which records are being requested. The request must include the requester's name and address (which may be a mailing address, email address, or fax number). The request may, but need not, include a specific reference to the RTKL.

The requester is not required to state a reason for the request. The agency may not deny a request based on the requester's intended use of the records, except in limited circumstances involving certain criminal justice records.

RESPONSE TIMELINES

Section 67.901 imposes strict timelines on agency responses. The agency must respond to a request within five business days of receiving it. The response must either grant the request, deny the request, or invoke a 30-day extension for one of the reasons permitted by the statute (the record is in storage, requires redaction, the request requires legal review, the requester has not complied with fee requirements, or the request is for a record that the agency determines requires retrieval from a remote location).

If the agency fails to respond within five business days (or within the extended 30-day period if an extension was properly invoked), the request is deemed denied. This deemed-denial provision prevents agencies from ignoring requests and gives the requester a basis for appealing.

FEES

Section 67.1307 and related provisions address fees. The agency may charge fees for duplication of records, but may not charge for the cost of searching for, reviewing, or redacting records. Duplication fees are set by the Office of Open Records and currently cover the cost of photocopying, printing, and providing electronic copies. Fees must reflect actual cost and may not be used to discourage requests. Certified copies may be provided at the fee established by law for the issuing agency.

If the estimated fees exceed $100, the agency must notify the requester and obtain prepayment before producing the records. Requesters may modify their requests to reduce fees.

EXEMPTIONS

The RTKL contains 30 specific exemptions in Section 67.708, as well as additional exemptions found in other provisions and in other statutes. The exemptions are specific and detailed, and the agency bears the burden of proving by a preponderance of the evidence that a record falls within an exemption. The principal exemptions include:

Records protected by privilege. Records subject to the attorney-client privilege, work product doctrine, or any other privilege recognized by statute or court rule are exempt.

Records relating to investigations. Records relating to a criminal investigation, including investigative materials, notes, correspondence, and reports, are exempt while the investigation is ongoing and to the extent that disclosure would jeopardize the investigation or endanger an individual. Noncriminal investigative records may also be exempt under certain conditions.

Personal identification information. Social Security numbers, driver's license numbers, financial account numbers, and similar personal identification information are exempt. Records that reveal the identity of a confidential source or an undercover law enforcement officer are also exempt.

Personal security information. Records that, if disclosed, would be reasonably likely to jeopardize the safety of an individual, including home addresses and personal telephone numbers of law enforcement officers and certain other public employees, are exempt.

Trade secrets and proprietary information. Trade secrets, confidential proprietary information, and financial information submitted to an agency that, if disclosed, would cause competitive harm to the submitting party, are exempt.

Draft documents. Internal, predecisional deliberations, including draft documents, notes, and preliminary analyses, are exempt when they relate to a matter in which the agency has not yet taken final action. This exemption does not extend to final agency actions, which are public regardless of whether they were preceded by drafting and deliberation.

Additional exemptions cover records relating to academic transcripts, library records, certain medical records, victims of crime, adoption records, security plans, emergency response plans, and other specific categories.

ADMINISTRATIVE APPEALS

The RTKL creates a robust administrative appeal process. Sections 67.1101 through 67.1102 establish that a requester whose request has been denied (including a deemed denial) may file an appeal within 15 business days of the denial. The appeal is filed with the appropriate appeals officer:

For Commonwealth agencies (executive branch), the appeals officer is the Office of Open Records (OOR), an independent agency created by the RTKL. For legislative agencies, the appeal goes to the relevant legislative appeals officer. For judicial agencies, the appeal goes to the relevant judicial appeals officer.

The OOR conducts a review of the denial, which may include written submissions by both parties, in camera review of the records, and in some cases, hearings. The OOR must issue a final determination within 30 days of receiving the appeal (though extensions are available). The OOR's determinations are publicly available and form a significant body of interpretive guidance on the RTKL.

The OOR's determination is binding unless appealed to court. Both the requester and the agency may appeal the OOR's determination to the court of common pleas within 30 days. The court reviews the determination de novo.

JUDICIAL REVIEW

Section 67.1301 through 67.1304 govern judicial review. A party dissatisfied with the OOR's determination may petition the court of common pleas for review. For Commonwealth agencies, the petition may be filed in Commonwealth Court. The court conducts a de novo review and may examine the records in camera.

If the court orders disclosure, it may award reasonable attorney's fees and costs to the requester if the court finds that the agency's denial was not made in good faith. The good-faith standard means that fee awards are not automatic, but courts have interpreted "good faith" to require the agency to have had a reasonable basis for its denial. Frivolous or unreasonable denials will result in fee awards.

The court may also impose sanctions for willful violations and may order the agency to adopt procedures to prevent future violations. In cases of repeated or egregious violations, the court may award enhanced remedies.

CRIMINAL PENALTIES

Section 67.1702 provides for criminal penalties for certain violations. A public official or employee who willfully or with wanton disregard denies access to a public record or improperly charges fees may be subject to a fine of up to $1,500 per violation. This criminal penalty provision is unusual among state public records laws and reflects the General Assembly's intent to deter deliberate noncompliance.

ELECTRONIC RECORDS AND TECHNOLOGY

The RTKL applies to records in all formats. Electronic records, including email, text messages, social media posts, database records, and documents stored in cloud-based systems, are subject to the law if they document a transaction or activity of the agency. Public officials and employees who use personal devices or accounts to conduct agency business create public records that are subject to disclosure.

If records exist in electronic form, the agency should provide them in electronic form upon request. The agency may not charge more for electronic copies than for paper copies when the electronic format is more efficient.

OFFICE OF OPEN RECORDS — STRUCTURE AND SIGNIFICANCE

The Office of Open Records (OOR) is one of the most distinctive features of Pennsylvania's RTKL. Created as an independent quasi-judicial agency, the OOR has issued thousands of final determinations since the RTKL's enactment in 2008, building a substantial body of administrative precedent. OOR determinations address every aspect of the law, including the scope of exemptions, fee disputes, the adequacy of agency searches, procedural compliance, and the application of the law to specific types of records.

OOR appeals officers conduct their reviews based on written submissions, position statements, and, where necessary, in camera review of disputed records. The OOR may also hold hearings in complex cases. Either party may submit legal arguments, evidence, and affidavits in support of their position. The process is designed to be accessible to unrepresented requesters, and many appeals are filed by individuals without legal representation.

OOR determinations are publicly available on the OOR's website and are searchable by agency, exemption, and topic. This transparency allows requesters to research how the OOR has interpreted specific exemptions and to craft their requests and appeals based on established precedent. The OOR's body of determinations has become a primary reference for RTKL interpretation, and courts regularly cite OOR determinations in their own opinions.

SPECIAL PROVISIONS FOR FINANCIAL AND CONTRACT RECORDS

The RTKL contains specific provisions ensuring public access to government financial records and contracts. Section 67.701 provides that financial records — including budgets, expenditure reports, invoices, receipts, and records of public fund disbursements — are presumptively public and not subject to most exemptions. This ensures that the public can track how government money is spent, which is one of the fundamental purposes of any public records law.

Government contracts, including the terms of contracts with private vendors, consultants, and service providers, are public records. The RTKL does not permit agencies to agree to confidentiality clauses in government contracts that would override the public's right to inspect contract terms. While specific trade secret information within a contract attachment might be exempt, the basic terms — parties, scope, duration, compensation — are always public.

PRACTICAL GUIDANCE

Requesters should submit written requests to the designated ORO, describe the records sought with sufficient specificity, include their contact information, and note the date of submission. If denied, requesters should file an appeal with the OOR within 15 business days. The OOR appeal is free, relatively quick, and does not require an attorney. The OOR has been a highly active and generally requester-friendly forum, making it a practical first step before considering litigation. Public bodies should designate an ORO, respond within the five-business-day window, cite specific exemptions when denying access, segregate and redact rather than deny entirely, and maintain records in a manner that facilitates access. The criminal penalty provision for willful violations adds an additional layer of deterrence against deliberate noncompliance.'''
    },

    # =========================================================================
    # RHODE ISLAND
    # =========================================================================
    {
        'id': 'ri-statute-apra',
        'citation': 'R.I.G.L. §§ 38-2-1 through 38-2-15',
        'title': 'Rhode Island Access to Public Records Act (APRA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'RI',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'Rhode Island Access to Public Records Act establishing public access to government records with a 10-business-day response requirement, specific fee limits, administrative complaint process through the Attorney General, and enforcement via Superior Court with mandatory attorney fee awards for prevailing requesters.',
        'text': '''Rhode Island Access to Public Records Act (APRA)
R.I.G.L. §§ 38-2-1 through 38-2-15

OVERVIEW AND LEGISLATIVE FINDINGS

Rhode Island's Access to Public Records Act (APRA), codified at Rhode Island General Laws Sections 38-2-1 through 38-2-15, establishes the right of public access to records maintained by state and local government agencies. Section 38-2-1 declares that it is vital in a democratic society that public business be performed in an open and public manner, and that citizens be afforded access to records documenting the performance of governmental functions. The Act reflects the principle that secrecy in government is inconsistent with democratic accountability and that the public's right to know must be balanced against legitimate privacy interests and other recognized needs for confidentiality.

DEFINITIONS AND SCOPE

Section 38-2-2 defines the key terms. A "public record" includes all documents, papers, letters, maps, books, tapes, photographs, films, sound recordings, magnetic or other tapes, electronic data processing records, or other material regardless of physical form or characteristics made or received pursuant to law or ordinance or in connection with the transaction of official business by any agency. The definition is intentionally broad and technology-neutral.

A "public body" means any executive, legislative, judicial, regulatory, or advisory body of the state, or any political subdivision thereof, including but not limited to any department, division, agency, commission, board, office, bureau, authority, or any school district, fire district, water district, sewer district, or other district. The definition also includes any committee, subcommittee, or other body of a public body.

RIGHT OF ACCESS

Section 38-2-3 establishes the core right: every person has the right to inspect and copy public records of a public body. The right is not conditioned on the requester's identity, purpose, or affiliation. A public body may not deny a request based on who is asking or why they want the records. The Act applies equally to residents and non-residents, individuals and organizations, media and non-media requesters.

REQUEST AND RESPONSE PROCEDURES

Section 38-2-3 and related provisions set forth the procedures for requesting and responding to requests. A request for records should be directed to the public body that maintains them. While the Act does not require requests to be in writing, written requests are advisable because they establish a clear record.

The public body must respond to a request within ten (10) business days of receipt. The response must either provide the records, deny the request with a specific explanation, or notify the requester that the body needs additional time. The body may extend the response time by an additional twenty (20) business days if it provides written notice to the requester explaining the need for the extension. Extensions are available for requests that involve voluminous records, records in storage, or records requiring review and redaction.

If the public body fails to respond within the applicable timeframe, the request is deemed denied, and the requester may proceed with enforcement remedies.

When a public body denies a request, it must provide a written explanation specifying the reasons for the denial and citing the specific exemption or exemptions relied upon. A blanket denial without citation of specific authority is insufficient.

FEES

Section 38-2-4 governs fees. A public body may charge a fee for searching for and retrieving records, but the fee may not exceed fifteen dollars ($15) per hour after the first hour. The first hour of search and retrieval time is free. Copying fees are limited to fifteen cents ($0.15) per page for standard paper copies.

For electronic records, the fee for providing records in electronic format should reflect the actual cost of the media or transmission. A public body may not charge an inflated fee for electronic records or condition electronic access on payment of fees higher than what would be charged for paper copies.

Fee waivers are available for requests that serve the public interest. If the requester is a nonprofit organization, a member of the media, or a researcher, or if the request serves the public interest, the public body should consider waiving or reducing fees. The Act does not mandate fee waivers in all such cases, but it expresses a preference for making records available at minimal cost when the request advances the public interest.

EXEMPTIONS

Section 38-2-2(4) lists the categories of records that are not considered public records and are exempt from disclosure. The exemptions are specific and must be narrowly construed. The principal exemptions include:

Personnel files. The content of personnel files maintained by public bodies are exempt, except that the name, title, salary, length of service, and position held by public employees are public. The exemption protects personal information such as evaluations, disciplinary notes, medical information, and personal contact details, but does not shield the basic employment facts that the public has a right to know.

Medical and psychological records. Records pertaining to the medical or psychological treatment, condition, or history of an individual are exempt. This protects patient privacy and aligns with federal privacy requirements under HIPAA.

Law enforcement investigatory files. Investigatory records compiled for law enforcement purposes are exempt to the extent that disclosure would reasonably be expected to interfere with enforcement proceedings, deprive a person of a fair trial, disclose the identity of a confidential source, disclose investigative techniques and procedures, or endanger the safety of any individual. This exemption applies to active investigatory files and does not permanently shield completed investigation records from disclosure.

Trade secrets and commercial information. Trade secrets, commercial or financial information obtained from a person that is privileged or confidential, and information relating to the competitive position of a business are exempt if disclosure would cause competitive harm.

Attorney-client privilege and litigation materials. Communications and work product protected by the attorney-client privilege or the work-product doctrine are exempt.

Test questions and scoring keys. Test questions, scoring keys, and other examination data used to administer licensing or employment examinations are exempt.

Preliminary drafts, notes, and memoranda. Internal preliminary drafts, notes, impressions, memoranda, working papers, and other similar documents prepared for the purpose of internal deliberation are exempt. However, final reports, decisions, and policy statements are public.

Records protected by other law. Records whose confidentiality is specifically required by state or federal statute, regulation, or court order are exempt.

Library records. Records relating to the use of library materials by individual patrons are exempt.

SEGREGATION AND REDACTION

When a record contains both public and exempt information, the public body must segregate the exempt portions and release the non-exempt remainder. Redaction must be limited to the specific information covered by the exemption. A public body may not withhold an entire record when only a portion is exempt.

ADMINISTRATIVE COMPLAINTS — ATTORNEY GENERAL

Section 38-2-8 provides for an administrative complaint process through the Attorney General. A requester who has been denied access to records may file a complaint with the AG within 90 days of the denial. The AG investigates the complaint, may request the public body to produce the records for review, and issues a determination. If the AG finds that the public body improperly withheld records, the AG may order disclosure.

The AG complaint process provides a free, relatively accessible alternative to litigation. The AG's determinations constitute a body of interpretive guidance on the APRA. While the AG process is non-binding in a formal legal sense (the AG cannot impose sanctions or order compliance in the way a court can), public bodies generally comply with AG determinations, and a failure to do so strengthens the requester's position in subsequent litigation.

JUDICIAL ENFORCEMENT

Section 38-2-8 also provides for judicial enforcement. A requester may file a civil action in the Superior Court to compel disclosure. The court reviews the matter de novo, may inspect the records in camera, and the burden of proof is on the public body to establish that the exemption applies.

If the court orders disclosure, it shall award reasonable attorney's fees and costs to the prevailing requester. This mandatory fee-shifting provision is critical to making enforcement practical. Rhode Island's mandatory (rather than discretionary) fee award is more favorable to requesters than the discretionary approach used in some other states. The availability of attorney fees means that requesters are not deterred from enforcing their rights by the cost of litigation, and public bodies face a financial disincentive for improperly withholding records.

The court may also impose sanctions for willful violations and may order the public body to adopt remedial measures to prevent future violations.

ELECTRONIC RECORDS

APRA applies to records in all formats, including electronic records. Email, text messages, database records, social media communications, and other electronic materials created or received in connection with public business are public records subject to the Act. Public bodies must produce electronic records in electronic format upon request if the records exist in that format.

The use of personal devices or accounts by public employees to conduct public business does not exempt the resulting records from the Act. Public bodies should adopt policies ensuring the preservation and accessibility of electronic records, including records created on personal devices.

SPECIAL PROVISIONS FOR LAW ENFORCEMENT RECORDS

Rhode Island's APRA contains specific provisions addressing law enforcement records that deserve attention. While the general investigatory records exemption protects active investigation files, Rhode Island law provides that certain categories of law enforcement records are public regardless of investigative status. Arrest logs, booking records, and records of dispatched calls are generally public, as is information about the identity of arrested individuals (once formally charged). The distinction between routine law enforcement records (public) and investigatory files (potentially exempt) requires careful analysis and is a frequent source of disputes.

Body camera footage, dashboard camera recordings, and other law enforcement audio and video recordings are public records subject to APRA, though they may be subject to redaction to protect victim identities, undercover operations, or ongoing investigations. The increasing deployment of recording technology by law enforcement has generated significant litigation and AG opinions addressing the balance between transparency and investigative needs.

RECORDS RETENTION AND MANAGEMENT

Rhode Island's records management framework requires state and local agencies to adopt records retention schedules approved by the Public Records Administration. Records subject to an approved retention schedule may not be destroyed before the retention period expires, and the existence of a pending records request imposes a duty to preserve the requested records regardless of the retention schedule.

The obligation to preserve records extends to electronic communications, including email and text messages. Public employees who use personal devices or accounts for public business create records that must be preserved and produced upon request. Agencies are expected to adopt policies and practices that ensure the preservation and accessibility of electronic records, including those stored in cloud-based systems or on personal devices.

Rhode Island's integration of the AG complaint mechanism with the records management framework means that the AG's office can address not only individual denials but also systemic failures in records management that impede public access. The AG has the authority to investigate patterns of noncompliance and to recommend institutional reforms.

MUNICIPAL AND SCHOOL DISTRICT RECORDS

Rhode Island's APRA applies with equal force to municipalities and school districts, which together maintain a vast volume of public records. Municipal records include budgets, tax records, building permits, zoning decisions, contracts with vendors, meeting minutes, and correspondence. School district records include budgets, expenditure reports, teacher and administrator contracts, collective bargaining agreements, standardized test results (in aggregate form), and administrative correspondence. All of these records are subject to APRA unless a specific exemption applies.

Rhode Island's relatively small geographic size and large number of municipalities (39 cities and towns) means that many records requests are directed at local government entities with limited staff and resources. The APRA applies the same requirements to all public bodies regardless of size, but the practical reality is that smaller municipalities may take longer to process requests. Requesters should be aware of this but should not accept unreasonable delays, as the ten-business-day response requirement applies uniformly.

PRACTICAL GUIDANCE

Requesters should submit requests in writing, describe the records with reasonable specificity, and note the date of submission. If the public body does not respond within ten business days, the request is deemed denied and the requester may file a complaint with the AG or an action in Superior Court. If the body denies the request, it must cite specific exemptions. Requesters should consider the AG complaint process before litigation, as it is free and may resolve the dispute without the expense and delay of a court proceeding. The mandatory attorney fee provision in Superior Court actions gives requesters strong economic incentive to pursue judicial enforcement when the AG process is insufficient. Public bodies should respond promptly, designate records custodians, cite specific exemptions, segregate and redact, and keep fee charges within statutory limits.'''
    },

    # =========================================================================
    # SOUTH CAROLINA
    # =========================================================================
    {
        'id': 'sc-statute-foia',
        'citation': 'S.C. Code §§ 30-4-10 through 30-4-165',
        'title': 'South Carolina Freedom of Information Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'SC',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'South Carolina Freedom of Information Act providing public access to records of public bodies with a 15-business-day response requirement for written requests, specific fee guidelines, and enforcement through circuit court actions with discretionary attorney fees and civil fines for knowing violations.',
        'text': '''South Carolina Freedom of Information Act
S.C. Code §§ 30-4-10 through 30-4-165

OVERVIEW AND DECLARATION OF POLICY

South Carolina's Freedom of Information Act (FOIA), codified at South Carolina Code Sections 30-4-10 through 30-4-165, declares that it is the public policy of the state that the business of government should be open and transparent, and that citizens are entitled to information about the activities of their government. Section 30-4-15 states that all public records are public property and must be made available to citizens for inspection and copying unless specifically exempted by the Act. The Act applies to both the records and meetings of public bodies, creating a comprehensive transparency framework. Exemptions are to be narrowly construed, and any doubt about whether a record is subject to disclosure should be resolved in favor of openness.

DEFINITIONS

Section 30-4-20 defines the key terms. A "public body" includes any department, agency, authority, commission, council, board, committee, subcommittee, or other body of the executive, legislative, or judicial branch of state government, as well as any political subdivision and its departments, agencies, boards, commissions, councils, committees, and subcommittees. It also includes any organization, corporation, or agency supported in whole or in part by public funds or expending public funds, and any quasi-governmental body. The broad definition ensures coverage of the full range of entities performing governmental functions.

A "public record" includes all books, papers, maps, photographs, cards, tapes, recordings, or other documentary materials regardless of physical form or characteristics prepared, owned, used, in the possession of, or retained by a public body. The definition is technology-neutral and covers electronic records, emails, text messages, and digital materials.

"Person" includes any individual, corporation, partnership, firm, organization, or association. The right of access belongs to any person, without regard to residency, citizenship, or organizational affiliation.

RIGHT OF ACCESS

Section 30-4-30 establishes the fundamental right. Any person has the right to inspect or copy any public record of a public body, except as otherwise provided by the Act. The public body must make records available during normal business hours. The requester need not state the purpose of the request or demonstrate any particular need for the records. The public body may not condition access on the requester's identity or intended use.

REQUEST AND RESPONSE PROCEDURES

Section 30-4-30 and related provisions set forth the request and response procedures. Requests may be made in person, by mail, by email, or by other means. While oral requests are permitted for records that are immediately available, written requests are advisable for records that require retrieval, review, or redaction, as they create a record of the request.

For written requests, the public body must respond within fifteen (15) business days. If the body determines that it will take longer to produce the records, it must notify the requester within the 15-day period and provide a reasonable estimated date for compliance. For oral requests for records that are immediately available, the body should provide access promptly — within the same business day when possible.

If the public body denies a request, it must notify the requester in writing, stating the reasons for the denial and citing the specific exemption relied upon. If the denial is based on the body's determination that the record does not exist, the body must so state. A blanket denial without specific citation is insufficient and may be challenged in court.

FEES

Section 30-4-30(b) addresses fees. A public body may charge a fee for copies of records. The fee must be reasonable and must reflect the actual cost of searching for, retrieving, and copying the records. The Act establishes specific guidelines: fees may not exceed the actual cost of the search, retrieval, and reproduction of records. For standard paper copies, fees are typically set at a per-page rate. For electronic records, fees should reflect the actual cost of the medium and any necessary data processing.

The Act permits public bodies to require prepayment of estimated fees if the estimated cost exceeds a specified amount. Public bodies may also charge for the staff time spent searching for and retrieving records, but the charges must be based on the salary of the lowest-paid employee capable of fulfilling the request, not the salary of the highest-ranking official involved.

Fee waivers may be requested when disclosure is in the public interest, and public bodies are encouraged to waive fees when the cost of collection would exceed the amount collected.

EXEMPTIONS

Section 30-4-40 lists the categories of records exempt from disclosure. The exemptions are specific and must be narrowly construed. The principal exemptions include:

Trade secrets and proprietary information. Trade secrets, commercial or financial information, and proprietary data submitted to a public body in confidence are exempt if disclosure would cause competitive harm to the submitting party.

Personnel information. Records containing personal information in employee personnel files are exempt, but certain basic information about public employees is public: name, title, agency, salary, date of hire, and dates of promotion. The exemption protects sensitive personal data (Social Security numbers, medical information, personal contact details) but does not shield employment facts from public scrutiny.

Law enforcement records. Records compiled for law enforcement purposes are exempt to the extent that disclosure would interfere with an active investigation, reveal the identity of a confidential source, disclose investigative techniques not generally known to the public, or endanger the safety of any individual. Incident reports containing limited factual information (date, time, location, nature of offense, name of arrested person) are public records even while an investigation is ongoing. The exemption for investigatory records applies only during the active investigation and does not permanently shield records once the investigation concludes or charges are filed.

Attorney-client communications. Records protected by attorney-client privilege or work product doctrine are exempt. However, the privilege belongs to the public body and may be waived.

Medical and health records. Records pertaining to the medical condition, diagnosis, or treatment of an individual are exempt, consistent with federal and state health privacy laws.

Student records. Records protected by the Family Educational Rights and Privacy Act (FERPA) or state educational privacy laws are exempt.

Security plans and measures. Records that, if disclosed, would compromise the security of a public body, including security plans, vulnerability assessments, and emergency response protocols, are exempt.

Internal deliberative materials. Internal memoranda, correspondence, and working papers relating to policy deliberation within a public body are exempt to the extent that they reflect the predecisional deliberative process. This exemption does not apply to factual information within such documents, and once a decision is made, the deliberative rationale becomes less protected.

Records protected by other law. Records whose confidentiality is required by state or federal statute are exempt.

SEGREGATION AND REDACTION

When a record contains both exempt and non-exempt information, the public body must segregate the exempt portions and release the non-exempt remainder. The body may not withhold an entire record because a portion of it is exempt. Redactions must be limited to the specific exempt information.

ENFORCEMENT AND REMEDIES

Section 30-4-100 provides for judicial enforcement. Any person denied access to records may apply to the circuit court for an order compelling disclosure. The court examines the records in camera if necessary and makes an independent determination of whether the exemption applies. The burden of proof is on the public body to justify its refusal.

If the court orders disclosure, it may in its discretion award reasonable attorney's fees and costs to the prevailing requester. While the fee award is discretionary rather than mandatory, courts regularly exercise this discretion in favor of requesters, particularly when the public body's denial was unreasonable.

Section 30-4-110 provides for civil fines. A public body member or employee who knowingly violates the Act is subject to a civil fine of up to one hundred dollars ($100) for each violation, and up to two hundred dollars ($200) for each subsequent violation. The fines are relatively modest but serve as a deterrent, particularly for repeated or willful violations.

TRAINING

The Act encourages public bodies to train employees on FOIA requirements. While the Act does not mandate training with the specificity of some other states, public bodies are expected to designate responsible officials and ensure that staff understand the procedures for responding to requests, the scope of exemptions, and the consequences of noncompliance.

ELECTRONIC RECORDS

The FOIA applies to records in all formats. Electronic records — email, text messages, database records, social media communications, and other digital materials — created or received in connection with the transaction of public business are public records subject to the Act. Public bodies must produce electronic records in electronic format when they exist in that format and the requester asks for it. The use of personal devices or accounts to conduct public business does not exempt the resulting records from the Act.

SPECIAL PROVISIONS FOR LAW ENFORCEMENT AND INCIDENT RECORDS

South Carolina's FOIA contains nuanced provisions governing law enforcement records that balance transparency with investigative needs. Section 30-4-40(a)(3) provides the exemption for investigatory records, but this exemption is qualified by the requirement that incident reports containing basic factual information are always public. An incident report must include the date, time, location, and general nature of the incident, as well as the name, sex, race, and age of the arrested person and the charges, if any. This ensures that the public has access to basic information about law enforcement activity even when the detailed investigation file remains confidential.

Booking photographs (mugshots), arrest records, and records of dispatched calls for service are generally public in South Carolina. The FOIA's treatment of law enforcement records reflects the principle that routine police activity is public business, and the investigatory exemption is reserved for records whose disclosure would genuinely interfere with an active investigation or endanger individuals.

Courts in South Carolina have addressed the scope of the law enforcement exemption in numerous cases, generally holding that the exemption does not automatically attach to all records in a law enforcement agency's possession — only those records specifically compiled for law enforcement investigatory purposes qualify. Administrative, operational, and statistical records maintained by law enforcement agencies remain public.

RELATIONSHIP TO JUDICIAL RECORDS AND COURT PROCEEDINGS

South Carolina's FOIA interacts with separate rules governing access to court records and judicial proceedings. While the FOIA applies to the judicial branch as a public body, court records (filings, orders, transcripts) are primarily governed by court rules rather than the FOIA. The FOIA covers administrative records of the judicial branch — budgets, personnel records, contracts, and operational records of court administration — while the substantive content of court proceedings is governed by the rules of court and constitutional principles of open courts.

This distinction is important because requesters seeking court records should typically use the court rules and procedures rather than the FOIA, while requesters seeking administrative records from the court system should use the FOIA process.

GOVERNMENT CONTRACTS AND FINANCIAL RECORDS

South Carolina's FOIA places particular emphasis on the public availability of government financial records. Records documenting the receipt and expenditure of public funds — including budgets, financial statements, audit reports, contracts, purchase orders, and records of disbursements — are core public records that are subject to few if any exemptions. The principle that the public has a right to know how its money is spent runs throughout the FOIA and is reinforced by the general policy declaration in Section 30-4-15.

Government contracts with private vendors, consultants, and service providers are public records. The FOIA does not permit public bodies to agree to blanket confidentiality clauses in government contracts that would prevent disclosure of the contract terms. While specific trade secret information within contract attachments may be redactable under the trade secrets exemption, the fundamental terms of a government contract — the parties, scope of work, compensation, duration, and performance standards — are always public.

PRACTICAL GUIDANCE

Requesters should submit written requests, describe the records sought with reasonable specificity, note the date and method of submission, and request a response within the 15-business-day period. If denied, requesters should demand a written explanation and consider filing an action in circuit court. The civil fine provision for knowing violations gives the FOIA an enforcement mechanism beyond attorney fees and judicial orders. Public bodies should respond within the statutory timeframe, cite specific exemptions when denying access, segregate and redact rather than withhold entirely, and maintain reasonable fee schedules. Training employees on FOIA obligations is strongly encouraged and helps prevent inadvertent violations that could result in civil fines and attorney fee awards.'''
    },

    # =========================================================================
    # SOUTH DAKOTA
    # =========================================================================
    {
        'id': 'sd-statute-open-records',
        'citation': 'S.D.C.L. §§ 1-27-1 through 1-27-46',
        'title': 'South Dakota Open Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'SD',
        'source': 'prdb-built',
        'jurisdiction_level': 'state',
        'summary': 'South Dakota Open Records Law providing public access to records of state and local government with prompt response requirements, reasonable copy fees, and enforcement through circuit court actions with no express statutory attorney fee provision, relying instead on general equitable authority.',
        'text': '''South Dakota Open Records Law
S.D.C.L. §§ 1-27-1 through 1-27-46

OVERVIEW AND PURPOSE

South Dakota's Open Records Law, codified at South Dakota Codified Laws Sections 1-27-1 through 1-27-46, establishes the right of public access to records maintained by state and local government entities. The statute reflects the state's policy that citizens should be able to review government records to hold their government accountable. South Dakota's approach to open records is relatively straightforward compared to some larger states, with a broad right of access, a moderate number of specific exemptions, and enforcement through the circuit court system. The law applies to all levels of state and local government, including school districts, counties, cities, and special districts.

DEFINITIONS AND SCOPE

Section 1-27-1 defines a "public record" as a record of any payment of public funds, the minutes of proceedings of a public body, and all records and documents required by law to be filed with any officer or public body, or any records or documents that were actually filed. Subsequent provisions and judicial interpretations have expanded the practical scope beyond this narrow definition to include all records maintained by public entities in connection with the transaction of public business, consistent with the law's transparency purpose.

The law applies to all state agencies, departments, boards, commissions, and offices, as well as counties, municipalities, townships, school districts, and other political subdivisions. Any entity that performs governmental functions or expends public funds is subject to the open records requirements with respect to those functions.

RIGHT OF ACCESS

Sections 1-27-1 and 1-27-1.1 establish the right of access. Any citizen has the right to inspect and copy public records maintained by state and local government entities. The records must be made available during normal office hours at the office where the records are maintained. The right of access belongs to citizens of the state, and the statute frames the right in terms of citizenship rather than the broader "any person" language used by some other states. However, in practice, government entities generally provide access to any requester regardless of residency.

The requester is not required to state the purpose of the request. The public entity may not condition access on the requester's identity (beyond establishing that the requester is a citizen, where required) or intended use of the records. The right is broadly inclusive, and the entity should err on the side of providing access.

REQUEST AND RESPONSE PROCEDURES

South Dakota does not impose rigid statutory deadlines for responding to records requests in the manner of some other states. The expectation is that requests will be handled promptly and that access will be provided within a reasonable time. What constitutes a reasonable time depends on the volume and complexity of the request, the location of the records, and the operational capacity of the government entity.

Requests may be made orally or in writing. Written requests are advisable because they create a record of what was requested and when. The request should describe the records sought with reasonable specificity. The government entity should respond as promptly as circumstances permit and should communicate with the requester about any delays or difficulties.

If the entity determines that a record or portion of a record is exempt from disclosure, it should inform the requester and identify the basis for the exemption. While the statute does not contain the same detailed procedural requirements found in some other states, the general principle is that denials should be explained and based on specific statutory authority.

FEES

Section 1-27-1.5 addresses fees for copies. The government entity may charge a reasonable fee for copies of public records. The fee must reflect the actual cost of reproduction and may not be set at a level designed to discourage requests. For standard paper copies, the fee is typically set at a per-page rate. For electronic records, the fee should reflect the cost of the medium or transmission.

The statute authorizes fees for copying but is less specific about search and retrieval fees than some other states' laws. In practice, government entities generally do not charge for the time spent searching for and retrieving records unless the search involves an extraordinary amount of staff time. Disputes about fees may be addressed through the courts.

EXEMPTIONS

South Dakota's exemption framework is found in various provisions throughout the Codified Laws, rather than consolidated in a single section of the Open Records Law. The principal categories of exempt records include:

Law enforcement investigatory records. Records compiled for law enforcement purposes may be withheld to the extent that disclosure would interfere with an active investigation, reveal the identity of a confidential source, disclose investigative techniques not generally known to the public, or endanger the safety of an individual. Routine law enforcement records such as incident reports, arrest records, and booking information are generally public.

Personnel records. Personal information in personnel files of public employees — including Social Security numbers, home addresses, home telephone numbers, and medical information — is exempt. The names, titles, salaries, and dates of employment of public employees are public.

Medical records. Records pertaining to the medical condition, diagnosis, or treatment of an individual, including mental health records, are exempt from public disclosure. This exemption aligns with federal HIPAA requirements.

Attorney-client communications. Communications between a government entity and its attorney that are subject to the attorney-client privilege are exempt. Work product prepared by attorneys in anticipation of litigation is also protected.

Trade secrets and commercial information. Trade secrets and confidential commercial or financial information submitted to a government entity are exempt if disclosure would cause competitive harm.

Tax records. Individual and corporate tax return information is confidential and exempt from public disclosure.

Juvenile records. Records relating to juvenile proceedings are confidential under state law and exempt from public disclosure.

Student records. Records protected by FERPA and state educational privacy laws are exempt.

Security-related records. Records that, if disclosed, would compromise the security of government facilities or the safety of government employees or the public are exempt.

Adoption records. Records relating to adoption proceedings are confidential and sealed by statute.

Records protected by other law. Records whose confidentiality is specifically required by other provisions of state or federal law are exempt.

The burden of establishing that an exemption applies rests on the government entity. If a record contains both exempt and non-exempt information, the entity should segregate the exempt portions and release the non-exempt remainder.

ENFORCEMENT AND REMEDIES

Section 1-27-1.5 and general provisions of South Dakota law provide for judicial enforcement. A person who is denied access to public records may bring an action in circuit court to compel disclosure. The court reviews the denial de novo and may examine the records in camera to determine whether the exemption applies. The burden of proof is on the government entity.

If the court orders disclosure, it may award appropriate relief. South Dakota's Open Records Law does not contain an express provision for mandatory attorney fee awards to prevailing requesters, which is a notable difference from states with stronger enforcement mechanisms. Attorney fees may be available under the court's general equitable authority or under other applicable statutes, but the absence of an express fee-shifting provision makes enforcement less economically accessible for individual requesters.

The court may order the government entity to produce the records and may impose other appropriate remedies, including injunctive relief against ongoing violations. In cases of willful or repeated violations, the court may take additional remedial action.

RELATIONSHIP TO OPEN MEETINGS LAW

South Dakota's Open Records Law operates alongside the state's open meetings law (S.D.C.L. Chapter 1-25). Records generated by or for government entities in connection with public meetings — including minutes, agendas, and supporting materials — are public records subject to the Open Records Law. The two statutes form a complementary transparency framework.

ELECTRONIC RECORDS

The Open Records Law applies to records in all formats, including electronic records. Email, text messages, electronic documents, database records, and other digital materials created or received in connection with the transaction of public business are public records. Government entities must provide electronic records in electronic format upon request when the records exist in that format, and may not charge more for electronic copies than is reasonably necessary to cover the cost of the medium or transmission.

Public officials and employees who use personal devices or accounts to conduct public business create public records that are subject to the Open Records Law. Government entities should adopt policies requiring the preservation of such records and facilitating their production upon request.

SPECIAL CONSIDERATIONS FOR COUNTY AND MUNICIPAL RECORDS

South Dakota's governmental structure includes a large number of counties, municipalities, and special districts, many of which are small and have limited staff. The Open Records Law applies to all of these entities, but the practical reality is that compliance practices vary considerably. In small towns and rural counties, the records custodian may be a part-time clerk or treasurer who handles records requests along with many other duties. Requesters dealing with smaller governmental entities should be patient but persistent, and should be aware that the same legal obligations apply regardless of the entity's size.

County auditors, treasurers, and registers of deeds maintain significant volumes of public records, including property records, tax records, financial records, and official filings. Many of these records are available online through county websites or through the state's centralized records systems, but requesters may need to submit formal requests for records that are not posted online.

School districts and special districts (water, sewer, fire, sanitation) are also subject to the Open Records Law. Records of these entities — including budgets, contracts, meeting minutes, and personnel records (to the extent not exempt) — are public and must be made available upon request.

ROLE OF THE ATTORNEY GENERAL

While South Dakota does not have a formal Attorney General petition or complaint process specifically dedicated to open records disputes (unlike some states such as Oregon or Pennsylvania), the Attorney General's office does issue informal guidance and opinions on open records questions. These opinions, while not legally binding, provide interpretive guidance that public entities and requesters can rely upon. The AG's office may also become involved in open records disputes in the context of broader law enforcement or government accountability inquiries.

The absence of a formal AG review mechanism means that requesters whose requests are denied have fewer options short of litigation. This makes it particularly important for requesters to document their requests carefully and to preserve evidence of the government entity's response or non-response. In practice, many records disputes in South Dakota are resolved informally through negotiation between the requester and the government entity, without resort to the courts.

FINANCIAL RECORDS AND GOVERNMENT SPENDING

South Dakota law places strong emphasis on public access to records documenting the expenditure of public funds. Section 1-27-1 specifically includes records of "any payment of public funds" in the definition of public records, making financial transparency a core component of the law. This includes budgets, expenditure reports, invoices, purchase orders, contracts with vendors and service providers, payroll records, and records of grants and subsidies.

Government contracts are public records, and South Dakota does not permit public entities to agree to confidentiality clauses that would override the public's right to inspect the terms of government contracts. While proprietary information and trade secrets within contract attachments may be exempt, the fundamental terms of any government contract — parties, scope, compensation, duration — are public. This principle is essential to ensuring accountability in government procurement and contracting.

The state maintains a centralized transparency portal that publishes certain categories of financial data, including employee compensation, vendor payments, and budget information. This proactive disclosure supplements the individual request process and makes certain commonly sought information available without the need for a formal records request.

PRACTICAL CONSIDERATIONS

Requesters should submit written requests, describe the records sought with reasonable specificity, and retain a copy of the request for their records. If access is denied, requesters should demand an explanation and identify the specific exemption cited. Because South Dakota does not have an administrative appeal mechanism, the requester's remedy is to file an action in circuit court. Requesters should be aware that the absence of express statutory attorney fee provisions means that the cost of litigation may not be recoverable, which is a significant consideration when deciding whether to pursue enforcement. Despite this limitation, the circuit court's equitable authority provides some flexibility, and requesters who can demonstrate willful or bad-faith violations may have stronger grounds for seeking fee recovery. Public entities should handle requests promptly, designate responsible personnel, cite specific exemptions when denying access, segregate and redact rather than withhold entirely, and maintain reasonable fee schedules.'''
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
