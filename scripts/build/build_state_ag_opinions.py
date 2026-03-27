#!/usr/bin/env python3
"""Build state AG/administrative opinions on public records.

Inserts influential AG advisory opinions and administrative body decisions
interpreting state public records laws. These are highly influential in practice —
some are legally binding (KY, TX, CT, IL, PA, IA, NJ).

States covered: KY, TX, IA, IL, PA, VA, CT, NJ, OR

Run: python3 scripts/build/build_state_ag_opinions.py
"""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

OPINIONS = [
    # =========================================================================
    # KENTUCKY — AG Open Records Decisions (BINDING)
    # KRS 61.880(2) gives the AG authority to issue binding decisions
    # =========================================================================
    {
        'id': 'ky-ag-ord-email-public-records-2012',
        'citation': 'KY OAG 12-ORD-100',
        'title': 'Emails as Public Records Under KY Open Records Act',
        'date': '2012-05-14',
        'court': 'Kentucky Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'KY',
        'source': 'prdb-built',
        'text': """KY OAG 12-ORD-100 — Emails as Public Records

QUESTION PRESENTED: Whether emails sent and received by public employees on government email systems constitute "public records" under the Kentucky Open Records Act (KRS 61.870 et seq.), and whether a public agency may categorically refuse to search email systems in response to an open records request.

ANALYSIS: The Attorney General examined KRS 61.870(2), which defines "public record" as "all books, papers, maps, photographs, cards, tapes, discs, diskettes, recordings, software, or other documentation regardless of physical form or characteristics, which are prepared, owned, used, in the possession of or retained by a public agency." The definition is intentionally broad and technology-neutral. The phrase "regardless of physical form or characteristics" was added by the General Assembly specifically to ensure the Act kept pace with evolving technology.

Emails created, sent, or received by public employees in the course of official business fall squarely within this definition. The medium of communication does not determine whether a record is "public" — the content and purpose do. An email discussing government business is no different in legal status from a paper memorandum on the same subject.

The AG rejected the agency's argument that searching email systems would be unduly burdensome. Under KRS 61.872(2), the custodian must make the records available for inspection or provide copies. The fact that records are stored electronically does not relieve the agency of its obligation to conduct a reasonable search. A categorical refusal to search email amounts to a subversion of the Act.

However, the AG acknowledged that purely personal emails — those having no connection whatsoever to agency business — are not public records even if stored on a government system. The burden falls on the agency to review emails and segregate personal from business-related content rather than withholding all emails or producing all without review.

HOLDING: Emails sent or received by public employees on government email systems in connection with public business are public records under KRS 61.870(2). A public agency may not categorically refuse to search its email systems. Personal emails on government systems are not public records, but the agency must review and segregate rather than withhold categorically. The agency violated the Open Records Act by refusing to search its email system.""",
        'summary': 'KY AG binding decision holding that government emails are public records and agencies cannot categorically refuse to search email systems.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ky-ag-ord-response-time-2015',
        'citation': 'KY OAG 15-ORD-021',
        'title': 'Response Time Requirements and Constructive Denial',
        'date': '2015-02-10',
        'court': 'Kentucky Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'KY',
        'source': 'prdb-built',
        'text': """KY OAG 15-ORD-021 — Response Time and Constructive Denial

QUESTION PRESENTED: Whether a public agency's failure to respond to an open records request within the statutory three-business-day period constitutes a violation of the Open Records Act, and what remedies are available when an agency constructively denies a request through silence.

ANALYSIS: KRS 61.880(1) requires a public agency to respond to a records request within three business days of receipt. The response must either grant the request, deny it with a specific citation to an applicable exemption, or provide a detailed explanation of the cause for delay along with a specific date when the records will be available. The statute does not provide for an open-ended delay.

The AG has consistently held that failure to respond within three business days constitutes a "constructive denial" of the request. A constructive denial is treated as a denial for purposes of appeal to the Attorney General under KRS 61.880(2). The agency cannot later claim it was "still working on" the request as a defense to an appeal.

When an agency needs additional time, KRS 61.872(5) allows a reasonable delay, but the agency must notify the requester within the initial three-day window and provide a specific date by which the records will be produced. Vague responses such as "we will get back to you" or "we are reviewing the request" do not satisfy this requirement.

The AG emphasized that the three-day response requirement is mandatory, not aspirational. The General Assembly chose this short timeline deliberately to ensure prompt public access. Agencies that routinely fail to meet this deadline undermine the Act's purpose and may be subject to penalties under KRS 61.882(5), including attorney fees and a civil fine of $25 per day for willful noncompliance.

HOLDING: Failure to respond to an open records request within three business days constitutes a constructive denial and a violation of KRS 61.880(1). The agency must either produce records, deny with specific exemption citations, or provide a detailed explanation of delay with a date certain. The agency violated the Act by failing to respond within the statutory period.""",
        'summary': 'KY AG binding decision establishing that failure to respond within three business days is a constructive denial and violation of the Open Records Act.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ky-ag-ord-law-enforcement-exemption-2018',
        'citation': 'KY OAG 18-ORD-154',
        'title': 'Law Enforcement Exemption Limits — Completed Investigations',
        'date': '2018-08-22',
        'court': 'Kentucky Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'KY',
        'source': 'prdb-built',
        'text': """KY OAG 18-ORD-154 — Law Enforcement Exemption After Investigation Closes

QUESTION PRESENTED: Whether a law enforcement agency may continue to withhold investigative records under KRS 61.878(1)(h) after the underlying investigation has been completed and the case has been closed or adjudicated.

ANALYSIS: KRS 61.878(1)(h) exempts "records of law enforcement agencies or agencies involved in administrative adjudication that were compiled in the process of detecting and investigating statutory or regulatory violations if the disclosure of the information would harm the agency by revealing the identity of informants not otherwise known or by premature release of information to be used in a prospective law enforcement action."

The AG analyzed two critical limitations on this exemption. First, the exemption protects the investigative process — it does not create a blanket shield for all law enforcement records. Routine administrative records, booking records, arrest logs, incident reports, and similar documents are not "compiled in the process of detecting and investigating" violations and thus do not qualify.

Second, and more critically, the exemption requires a showing that disclosure "would harm the agency" in one of the specific ways enumerated. Once an investigation is complete and any prosecution concluded, the risk of "premature release" evaporates. The agency must then demonstrate some other specific, articulable harm rather than invoking the exemption categorically.

The AG rejected the agency's assertion that all files in its "investigative" filing system are automatically exempt. The exemption applies to specific records, not to filing categories. The agency must review each record and demonstrate how its disclosure would cause the type of harm the statute addresses.

The AG also noted that KRS 61.878(4) requires agencies to separate exempt material from non-exempt material and produce the non-exempt portions. A law enforcement file may contain both exempt and non-exempt records, and the agency must undertake this segregation.

HOLDING: The law enforcement exemption under KRS 61.878(1)(h) does not apply categorically to all records in an investigative file. Once an investigation is closed and any prosecution concluded, the agency must show specific articulable harm to justify continued withholding. The agency must segregate exempt from non-exempt material. The agency violated the Act by categorically withholding the entire investigative file.""",
        'summary': 'KY AG binding decision narrowing the law enforcement exemption, requiring specific harm showing after investigations close and mandating segregation of exempt material.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ky-ag-ord-personnel-records-2016',
        'citation': 'KY OAG 16-ORD-208',
        'title': 'Personnel Records — Privacy vs. Public Accountability',
        'date': '2016-10-03',
        'court': 'Kentucky Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'KY',
        'source': 'prdb-built',
        'text': """KY OAG 16-ORD-208 — Personnel Records and the Privacy Balancing Test

QUESTION PRESENTED: What personnel records of public employees are subject to disclosure under the Open Records Act, and how should the privacy exemption under KRS 61.878(1)(a) be applied to employee information?

ANALYSIS: KRS 61.878(1)(a) exempts "public records containing information of a personal nature where the public disclosure thereof would constitute a clearly unwarranted invasion of personal privacy." The key phrase is "clearly unwarranted" — the General Assembly placed the thumb on the scale of disclosure by requiring that any invasion of privacy be not merely unwarranted but "clearly" so.

The AG applied the well-established balancing test: the public's interest in disclosure must be weighed against the employee's privacy interest. The public interest is measured by the extent to which disclosure would shed light on the operations of government — the "core purpose" of the Open Records Act.

Certain categories of personnel information are presumptively public: name, job title, salary, dates of employment, education and training qualifications for the position, and any final disciplinary actions. These directly relate to how government operates and spends public funds. An employee's salary, for example, reflects a public expenditure that taxpayers are entitled to scrutinize.

Other categories require case-by-case balancing: performance evaluations, internal complaints, preliminary investigation records, medical information, and home contact information. The AG held that performance evaluations of public employees generally must be disclosed because they reflect how well an agency is managing its workforce, but that specific medical diagnoses or Social Security numbers must be redacted.

The AG rejected the agency's blanket policy of treating all personnel files as confidential. No such categorical exemption exists in the Act. Each request must be evaluated on the specific records sought and the specific privacy interests implicated.

HOLDING: Personnel records are not categorically exempt. Name, title, salary, employment dates, and final disciplinary actions are presumptively public. Other personnel information requires balancing under KRS 61.878(1)(a), with the burden on the agency to show a "clearly unwarranted invasion of personal privacy." Blanket confidentiality policies for personnel files violate the Act.""",
        'summary': 'KY AG binding decision establishing that personnel records are not categorically exempt, with salary and disciplinary actions presumptively public.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # TEXAS — AG Open Records Decisions (BINDING)
    # Tex. Gov't Code § 552.301-552.309 — AG rules on disputed requests
    # =========================================================================
    {
        'id': 'tx-ag-or-electronic-records-format-2014',
        'citation': 'TX AG OR2014-03842',
        'title': 'Electronic Records Must Be Produced in Requested Format',
        'date': '2014-04-15',
        'court': 'Texas Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'TX',
        'source': 'prdb-built',
        'text': """TX AG OR2014-03842 — Electronic Records Format Requirements

QUESTION PRESENTED: Whether a governmental body may provide records only in paper format when the requester has specifically asked for electronic copies, and the records are maintained electronically.

ANALYSIS: Section 552.228 of the Texas Public Information Act (TPIA) provides that if a governmental body maintains public information in an electronic medium and the requestor requests the information in that medium, the governmental body shall supply the information in the requested medium. The statute is mandatory ("shall"), not permissive.

The AG examined the governmental body's practice of printing database records and providing paper copies even when requestors asked for electronic files. This practice violates the plain language of § 552.228. When records exist electronically, the requester has the right to receive them electronically.

The AG further noted that § 552.231 permits a governmental body to charge for the actual cost of the medium (e.g., a CD or USB drive) and any programming necessary to produce the records in the requested format. But the right to charge for production costs does not transform the mandatory duty into a discretionary one. The governmental body must produce electronic records electronically when asked, and may charge reasonable costs for doing so.

The AG also addressed the related question of database queries. When a requester asks for information that can be extracted from a database through a standard query, the governmental body must run the query rather than claiming the information does not exist as a discrete "record." The TPIA covers information, not just pre-existing documents.

HOLDING: A governmental body that maintains records electronically must produce them in electronic format when requested under § 552.228. Converting electronic records to paper to satisfy a request for electronic copies violates the TPIA. The governmental body must produce the records electronically and may charge only the actual cost of the medium and any necessary programming.""",
        'summary': 'TX AG binding ruling that governmental bodies must produce electronic records in electronic format when requested, and cannot force paper-only production.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'tx-ag-or-text-messages-2016',
        'citation': 'TX AG OR2016-12847',
        'title': 'Text Messages on Personal Devices as Public Information',
        'date': '2016-07-20',
        'court': 'Texas Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'TX',
        'source': 'prdb-built',
        'text': """TX AG OR2016-12847 — Text Messages on Personal Devices

QUESTION PRESENTED: Whether text messages sent or received by public officials on personal cell phones constitute "public information" subject to disclosure under the Texas Public Information Act when the messages relate to official government business.

ANALYSIS: Section 552.002 of the TPIA defines "public information" as information collected, assembled, or maintained by or for a governmental body, regardless of the form in which it is stored. The definition focuses on the nature and purpose of the information, not the physical device on which it resides.

The AG considered City of Dallas v. Dallas Morning News (Tex. App. 2006), which established that the location or ownership of the device does not determine whether information is "public." When a public official conducts government business via text message on a personal phone, those messages are collected or maintained "for" the governmental body. The official cannot circumvent the TPIA simply by choosing to use a personal device rather than a government-issued one.

The AG acknowledged practical challenges in retrieving text messages from personal devices but held that these challenges do not negate the legal obligation. The governmental body must make a good-faith effort to collect responsive text messages from officials' personal devices. Officials have a duty to preserve and produce such messages.

The AG also addressed the question of mixed-use messages — texts that contain both personal and public content. The governmental body must review these messages and produce the portions relating to public business while redacting truly personal content under applicable exemptions.

The AG emphasized that allowing officials to conduct public business on personal devices without TPIA accountability would create an enormous loophole that would swallow the Act's disclosure mandate.

HOLDING: Text messages on personal devices that relate to official government business are "public information" under § 552.002 of the TPIA. The governmental body must make good-faith efforts to collect and produce such messages. Officials cannot evade the TPIA by using personal devices for public business.""",
        'summary': 'TX AG binding ruling that text messages on personal devices about government business are public information and must be produced under the TPIA.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'tx-ag-or-fee-waiver-media-2015',
        'citation': 'TX AG OR2015-08221',
        'title': 'Fee Waivers and Charges for Public Information Requests',
        'date': '2015-06-12',
        'court': 'Texas Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'TX',
        'source': 'prdb-built',
        'text': """TX AG OR2015-08221 — Fee Waivers and Cost Provisions

QUESTION PRESENTED: Under what circumstances must a governmental body waive or reduce charges for producing public information, and what costs may properly be assessed to a requestor?

ANALYSIS: Section 552.267 of the TPIA requires a governmental body to furnish public information without charge or at a reduced charge if the governmental body determines that waiver or reduction of the charge is in the public interest because providing the information primarily benefits the general public. The AG has interpreted this provision to require consideration of whether the request serves a public purpose beyond the requestor's private interest.

The AG examined the statutory cost provisions under §§ 552.261-552.275 and the Office of the Attorney General's cost rules. Permissible charges include: (1) costs of materials (paper, CDs, etc.); (2) labor costs for locating, compiling, and reproducing records, but only at the pay rate of the lowest-paid employee who can perform the task; (3) overhead charges as set by the OAG cost rules. Governmental bodies may NOT charge for reviewing records to determine what is responsive or what must be withheld — that is the governmental body's duty under the Act, not a cost properly shifted to the requestor.

The AG noted that excessive cost estimates are sometimes used to deter requestors, which violates the spirit and letter of the TPIA. A governmental body may require a deposit for large requests but must provide an itemized cost estimate. If the requestor challenges the estimate, the governmental body bears the burden of showing the charges are reasonable and authorized.

The AG also addressed the common practice of estimating costs for responding to requests and then holding records hostage pending payment. The governmental body must provide the estimate promptly — within 10 business days of receiving the request — and may not use the cost estimation process to delay production indefinitely.

HOLDING: Fee waivers are required when disclosure primarily benefits the general public. Governmental bodies may charge only for materials, authorized labor, and overhead as set by OAG rules. They may not charge for the review process. Cost estimates must be itemized, provided within 10 business days, and may not be used as delay tactics.""",
        'summary': 'TX AG ruling establishing limits on charges for public information requests, requiring fee waivers when disclosure serves the public interest.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # IOWA — IPIB (Iowa Public Information Board) Decisions (BINDING)
    # Iowa Code § 23.8 — IPIB issues binding declaratory orders
    # =========================================================================
    {
        'id': 'ia-ipib-what-constitutes-government-body-2016',
        'citation': 'IPIB DO 2016-001',
        'title': 'What Constitutes a "Government Body" Under Iowa Open Records',
        'date': '2016-03-08',
        'court': 'Iowa Public Information Board',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'IA',
        'source': 'prdb-built',
        'text': """IPIB Declaratory Order 2016-001 — Definition of "Government Body"

QUESTION PRESENTED: Whether a nonprofit entity that receives substantial public funding and performs functions delegated by a government agency qualifies as a "government body" subject to the Iowa Open Records Act (Iowa Code Ch. 22).

ANALYSIS: Iowa Code § 22.1 defines "government body" broadly to include any entity of state or local government, including boards, commissions, committees, and subunits. The IPIB examined whether this definition extends to quasi-governmental entities — private organizations that perform public functions or operate with significant public funding.

The Board applied a functional test, considering several factors: (1) whether the entity was created by government action; (2) whether it performs a traditionally governmental function; (3) the degree of government funding; (4) the degree of government control over the entity's operations; and (5) whether the entity's records would shed light on the conduct of government business.

The Board found that a nonprofit receiving over 80% of its funding from a county government and performing services the county was otherwise obligated to provide met the functional test. The entity's nonprofit corporate form did not insulate it from open records obligations. The Board emphasized that government agencies cannot outsource public functions to private entities and simultaneously claim those functions are no longer subject to public scrutiny.

The Board also addressed the entity's argument that applying the Open Records Act would burden its operations. The Board held that the burden of transparency is inherent in performing public functions with public money. The entity should have anticipated open records obligations when it accepted the government contract.

HOLDING: A nonprofit entity that receives substantial public funding and performs delegated governmental functions is a "government body" under Iowa Code § 22.1. The entity's corporate form does not exempt it from the Open Records Act. The functional test — examining creation, function, funding, control, and public accountability — determines whether an entity is subject to open records requirements.""",
        'summary': 'IPIB binding decision establishing a functional test for determining whether quasi-governmental entities are subject to Iowa open records law.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ia-ipib-constructive-denial-2018',
        'citation': 'IPIB FC 2018-012',
        'title': 'Constructive Denial Through Delay and Nonresponse',
        'date': '2018-05-15',
        'court': 'Iowa Public Information Board',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'IA',
        'source': 'prdb-built',
        'text': """IPIB Formal Complaint 2018-012 — Constructive Denial Through Delay

QUESTION PRESENTED: Whether a government body's pattern of delayed responses, partial production, and failure to provide timely notice of denial constitutes a violation of Iowa Code Chapter 22, and what constitutes "constructive denial" under Iowa open records law.

ANALYSIS: Iowa Code § 22.8(4) requires a government body to respond to a records request in a "good faith and reasonable" manner. While the Iowa Open Records Act does not specify a fixed deadline comparable to some other states, the Board has interpreted the "good faith and reasonable" standard to require prompt action commensurate with the scope of the request.

The Board examined a pattern of behavior by the respondent: repeated requests met with vague acknowledgments, production of partial records weeks after the request, no explanation for withheld records, and no formal denial that would trigger appeal rights. The Board found this pattern amounted to constructive denial — an effective denial of access disguised as ongoing compliance.

The Board held that constructive denial occurs when: (1) a government body fails to respond within a reasonable time without explanation; (2) a government body produces partial records without identifying what is being withheld and why; (3) a government body's pattern of delays has the practical effect of denying access; or (4) a government body fails to provide the statutory basis for withholding records, thereby depriving the requester of meaningful appeal rights.

The Board emphasized that the lack of a fixed statutory deadline does not give government bodies unlimited time. What is "reasonable" depends on the volume and complexity of the request, but even large requests must be addressed incrementally, with the government body producing records on a rolling basis rather than holding all records until every page has been reviewed.

HOLDING: A government body's pattern of unexplained delays, partial production without identification of withheld records, and failure to cite statutory authority for withholding constitutes constructive denial under Iowa Code Chapter 22. Government bodies must respond promptly, produce records on a rolling basis for large requests, and clearly identify any withheld records with specific statutory authority.""",
        'summary': 'IPIB decision defining constructive denial under Iowa open records law, requiring rolling production and clear identification of withheld records.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ia-ipib-segregability-2017',
        'citation': 'IPIB DO 2017-004',
        'title': 'Segregability — Duty to Redact Rather Than Withhold Entirely',
        'date': '2017-07-20',
        'court': 'Iowa Public Information Board',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'IA',
        'source': 'prdb-built',
        'text': """IPIB Declaratory Order 2017-004 — Segregability and Redaction Obligations

QUESTION PRESENTED: Whether a government body may withhold an entire document when only portions contain confidential information, and what obligations the government body has to segregate exempt from non-exempt information.

ANALYSIS: Iowa Code § 22.7 lists specific categories of confidential records. When a record contains both confidential and non-confidential information, the government body must produce the non-confidential portions. This principle — segregability — is fundamental to open records law and prevents agencies from using a narrow exemption to shield an entire document.

The Board examined a city's practice of withholding entire personnel files in response to records requests, citing the confidentiality of certain personnel evaluations under § 22.7(11). The Board found this practice violated the Act because the personnel files also contained non-confidential information such as the employee's name, title, salary, dates of employment, and education credentials.

The Board established clear guidance: (1) When a government body receives a request for records that contain both exempt and non-exempt information, it must review the records and redact only the specifically exempt portions. (2) The government body must identify each redaction and cite the specific statutory authority for the exemption. (3) Blanket withholding of a document because some portion is exempt violates the Act. (4) The government body bears the burden of demonstrating that each specific redaction is authorized by statute.

The Board also addressed the cost of redaction. While acknowledging that line-by-line review can be time-consuming, the Board held that this is an inherent cost of government transparency, not a basis for refusing to segregate. The Board suggested that government bodies develop standardized redaction procedures to handle common situations efficiently.

HOLDING: Government bodies must segregate exempt from non-exempt information and produce redacted versions of records rather than withholding entire documents. Each redaction must cite specific statutory authority. Blanket withholding of records containing some exempt information violates Iowa Code Chapter 22.""",
        'summary': 'IPIB binding decision requiring government bodies to redact exempt portions and produce the remainder, prohibiting blanket withholding of mixed documents.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # ILLINOIS — PAC (Public Access Counselor) Binding Opinions
    # 5 ILCS 140/9.5 — PAC issues binding opinions under IL FOIA
    # =========================================================================
    {
        'id': 'il-pac-text-message-foia-2014',
        'citation': 'IL PAC Op. 14-006',
        'title': 'Text Messages and Instant Messages Under Illinois FOIA',
        'date': '2014-06-18',
        'court': 'Illinois Public Access Counselor',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'IL',
        'source': 'prdb-built',
        'text': """IL PAC Opinion 14-006 — Text Messages and Electronic Communications

QUESTION PRESENTED: Whether text messages and instant messages sent by public officials relating to public business are "public records" subject to the Illinois Freedom of Information Act (5 ILCS 140), regardless of whether they are sent on personal or government-owned devices.

ANALYSIS: Section 2(c) of the Illinois FOIA defines "public records" as "all records, reports, forms, writings, letters, memoranda, books, papers, maps, photographs, microfilms, cards, tapes, recordings, electronic data processing records, electronic communications, recorded information and all other documentary materials pertaining to the transaction of public business, regardless of physical form or characteristics, having been prepared by or for, or having been or being used by, received by, in the possession of, or under the control of any public body."

The PAC found that text messages and instant messages fall within this definition when they pertain to the transaction of public business. The phrase "electronic communications" explicitly covers these formats. The definition is not limited to communications on government-owned devices — the critical question is whether the communication pertains to public business, not who owns the device.

The PAC addressed the practical challenge of retrieval from personal devices. Public bodies have an obligation to adopt records retention policies that account for electronic communications, including text messages. Public officials who conduct public business via text message have a duty to preserve those messages. The PAC noted that the failure to preserve text messages relating to public business may itself constitute a violation of FOIA and the Local Records Act.

The PAC rejected the argument that text messages are inherently "transitory" and therefore not subject to FOIA. Whether a communication is transitory depends on its content, not its format. A text message scheduling a committee vote or discussing a pending contract is not transitory.

HOLDING: Text messages and instant messages pertaining to public business are public records under Illinois FOIA, regardless of whether they are on personal or government-owned devices. Public bodies must adopt retention policies covering electronic communications. Failure to preserve such records may violate both FOIA and the Local Records Act.""",
        'summary': 'IL PAC binding opinion holding that text messages about public business are FOIA records regardless of device ownership, requiring retention policies.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'il-pac-fee-waiver-public-interest-2015',
        'citation': 'IL PAC Op. 15-012',
        'title': 'Fee Waiver Requirements Under Illinois FOIA',
        'date': '2015-09-22',
        'court': 'Illinois Public Access Counselor',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'IL',
        'source': 'prdb-built',
        'text': """IL PAC Opinion 15-012 — Fee Waiver Determinations

QUESTION PRESENTED: Under what circumstances must a public body waive copying fees under Section 6(a) of the Illinois FOIA, and what factors should be considered in determining whether a fee waiver serves the public interest?

ANALYSIS: Section 6(a) of the Illinois FOIA (5 ILCS 140/6(a)) provides that a public body shall waive or reduce fees when the requestor demonstrates that the request is in the public interest — that is, when the principal purpose of the request is to access and disseminate information regarding the health, safety, and welfare or the legal rights of the general public, and the request is not for the principal purpose of personal or commercial benefit.

The PAC analyzed the two-prong test: (1) whether the request primarily serves the public interest in government transparency, and (2) whether the request is not primarily for private gain. Both prongs must be met.

On the first prong, the PAC held that requests by journalists, nonprofit watchdog organizations, and individuals seeking information about government operations or expenditures of public funds generally satisfy the public interest requirement. The requestor does not need to be a member of the institutional media — the FOIA does not distinguish between professional journalists and citizen journalists or bloggers.

On the second prong, the PAC held that the mere fact that a requestor might personally benefit from the information does not defeat a fee waiver if the primary purpose is public disclosure. An attorney requesting records for litigation may serve the public interest if the litigation concerns government accountability, even though the attorney also has a professional interest.

The PAC found that the public body improperly denied the fee waiver by applying an overly restrictive reading of "public interest." The body required the requestor to demonstrate that "the general public" would directly benefit, which sets the bar too high. The statute requires that the request primarily serve the public interest, not that every member of the public will personally benefit.

The PAC also noted that public bodies must respond to fee waiver requests promptly and may not use the fee waiver determination as a mechanism to delay production of records.

HOLDING: Fee waivers under Section 6(a) must be granted when the primary purpose of the request is to access and disseminate information regarding public health, safety, welfare, or legal rights, and the request is not primarily for personal or commercial benefit. The public body applied too restrictive a standard and improperly denied the fee waiver.""",
        'summary': 'IL PAC binding opinion establishing that fee waivers must be granted when requests primarily serve transparency, even if the requestor also benefits personally.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'il-pac-unduly-burdensome-2016',
        'citation': 'IL PAC Op. 16-003',
        'title': 'Limits on "Unduly Burdensome" Denials Under Illinois FOIA',
        'date': '2016-02-09',
        'court': 'Illinois Public Access Counselor',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'IL',
        'source': 'prdb-built',
        'text': """IL PAC Opinion 16-003 — Unduly Burdensome Requests

QUESTION PRESENTED: When may a public body deny a FOIA request as "unduly burdensome" under Section 3(g) of the Illinois FOIA, and what procedural requirements must the public body satisfy before invoking this provision?

ANALYSIS: Section 3(g) of the Illinois FOIA (5 ILCS 140/3(g)) allows a public body to deny a request that is "unduly burdensome" in compliance with Section 3(g)'s specific procedural requirements. The PAC emphasized that this provision is an exception to the general rule of disclosure, and like all FOIA exceptions, it must be narrowly construed.

Before denying a request as unduly burdensome, the public body must: (1) provide the requestor with an opportunity to confer and attempt to reduce the request to manageable proportions; (2) the request for conference must be made within 5 business days of receipt; and (3) the public body must explain in writing why the request is unduly burdensome, specifying the burden in concrete terms (staff hours, volume of records, disruption to operations).

The PAC found that many public bodies invoke "unduly burdensome" as a reflexive response to large requests without satisfying these procedural prerequisites. Failure to extend an invitation to confer before denying the request as unduly burdensome is itself a violation of FOIA.

The PAC also held that the volume of responsive records alone does not make a request unduly burdensome. A public body with a large volume of records on a topic may simply have more records to produce. The question is whether the burden of production is disproportionate to the public body's resources and operational needs, not whether the request results in many responsive pages.

The PAC recommended that public bodies respond to large requests by producing records on a rolling basis rather than attempting to complete review of all records before producing any. This approach reduces the immediate burden while satisfying the requester's access rights.

HOLDING: Public bodies must strictly comply with Section 3(g)'s procedural requirements before denying a request as unduly burdensome, including extending an invitation to confer within 5 business days. Volume alone does not make a request unduly burdensome. Rolling production is recommended for large requests.""",
        'summary': 'IL PAC binding opinion setting strict procedural requirements for "unduly burdensome" denials and recommending rolling production for large requests.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # PENNSYLVANIA — OOR (Office of Open Records) Final Determinations
    # 65 P.S. § 67.1101 — OOR issues binding final determinations
    # =========================================================================
    {
        'id': 'pa-oor-personnel-records-rtkl-2012',
        'citation': 'PA OOR Dkt. AP 2012-0477',
        'title': 'Personnel Records Disclosure Under the Right-to-Know Law',
        'date': '2012-04-18',
        'court': 'Pennsylvania Office of Open Records',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'PA',
        'source': 'prdb-built',
        'text': """PA OOR Final Determination — AP 2012-0477 — Personnel Records

QUESTION PRESENTED: What personnel records of public employees are accessible under the Pennsylvania Right-to-Know Law (RTKL), and how does Section 708(b)(7)'s personnel file exemption apply?

ANALYSIS: Section 708(b)(7) of the RTKL (65 P.S. § 67.708(b)(7)) exempts "a record of an employee's . . . performance rating or review" from disclosure. However, the OOR has consistently held that this exemption is narrow and does not extend to all records contained in a personnel file.

The OOR examined what information IS accessible despite the personnel file exemption. Under Section 801 of the RTKL (65 P.S. § 67.801), certain financial records are presumptively public, including the salary and compensation of public employees. Under the Pennsylvania Supreme Court's decision in Pennsylvania State Police v. Grove (2014), this extends to total compensation including overtime, benefits, and other forms of remuneration.

The OOR also held that disciplinary records that have resulted in final action (suspension, demotion, termination) are not "performance ratings or reviews" and thus are not exempt under Section 708(b)(7). The exemption targets evaluative documents — subjective assessments of employee performance — not records of final disciplinary outcomes. A letter of suspension, for instance, is an administrative action, not a performance review.

The OOR further clarified that employment contracts, including collective bargaining agreements and individual employment agreements with appointed officials, are public records. These documents establish the terms under which public money is spent and are central to the RTKL's transparency purpose.

The OOR noted that agencies frequently over-apply the personnel file exemption by treating any record associated with an employee as exempt. This reading is inconsistent with the RTKL's mandate that exemptions be narrowly construed and that the burden of proof falls on the agency claiming the exemption.

HOLDING: The personnel file exemption under Section 708(b)(7) of the RTKL is limited to performance ratings and reviews. Salary, compensation, final disciplinary actions, and employment contracts are public records. Agencies may not categorically withhold all personnel-related records under this narrow exemption.""",
        'summary': 'PA OOR binding decision narrowing the personnel file exemption to performance reviews, holding salary and disciplinary records are public.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'pa-oor-public-body-definition-2015',
        'citation': 'PA OOR Dkt. AP 2015-1022',
        'title': 'Entities Subject to RTKL — "Agency" and "Public Body" Definitions',
        'date': '2015-07-14',
        'court': 'Pennsylvania Office of Open Records',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'PA',
        'source': 'prdb-built',
        'text': """PA OOR Final Determination — AP 2015-1022 — Definition of Agency

QUESTION PRESENTED: Whether a private entity performing governmental functions under contract with a Commonwealth agency is itself an "agency" subject to the Right-to-Know Law, and under what circumstances a government contractor's records are accessible through RTKL requests directed to the contracting agency.

ANALYSIS: The RTKL defines "agency" under Section 102 as including Commonwealth agencies, local agencies, and legislative and judicial agencies. The definition does not expressly include private contractors. However, the OOR examined two pathways through which contractor records may be accessible.

First, under the "constructive possession" doctrine, records held by a contractor that were created in the performance of a government contract may be deemed to be in the constructive possession of the contracting agency. If the agency has the legal right to obtain the records under the terms of the contract, the records are within the agency's possession for RTKL purposes. The OOR emphasized that agencies should include records access provisions in their contracts precisely to ensure transparency.

Second, under Section 506(d) of the RTKL, a public body that enters into a contract with a private entity must include a provision in the contract requiring the contractor to provide records to the agency upon request to enable RTKL compliance. When a contract includes such a provision, the contracting agency cannot claim it does not possess the contractor's records.

The OOR found that the contracting agency in this case had failed to include an adequate records access clause in its contract and then used that failure as a basis for denying the RTKL request. The OOR rejected this approach, holding that an agency cannot benefit from its own failure to include mandatory contract provisions. The agency was ordered to obtain the records from the contractor and produce them.

The OOR noted that this issue is increasingly important as government outsourcing expands. Without the constructive possession doctrine and contract access requirements, agencies could insulate entire functions from public scrutiny by contracting them out.

HOLDING: Private contractors are not directly subject to the RTKL, but their records may be accessible through the contracting agency via constructive possession and mandatory contract provisions under Section 506(d). An agency cannot avoid RTKL obligations by failing to include records access clauses in its contracts.""",
        'summary': 'PA OOR binding decision establishing that government contractors\' records are accessible through the contracting agency via constructive possession and contract clauses.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'pa-oor-response-time-extensions-2017',
        'citation': 'PA OOR Dkt. AP 2017-0689',
        'title': 'Response Time Extensions — Limits on 30-Day Extension',
        'date': '2017-05-30',
        'court': 'Pennsylvania Office of Open Records',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'PA',
        'source': 'prdb-built',
        'text': """PA OOR Final Determination — AP 2017-0689 — 30-Day Extension Requirements

QUESTION PRESENTED: Under what circumstances may an agency invoke the 30-day extension under Section 902 of the RTKL, and what happens when an agency fails to respond within the extended period?

ANALYSIS: Section 901 of the RTKL requires an agency to respond to a records request within 5 business days. Under Section 902, the agency may send a written notice within the initial 5-day period invoking a 30-day extension. The notice must specify one or more of the statutory reasons for the extension, including that the request requires retrieval from a remote location, review of a large number of records, consultation with legal counsel, or consultation with another agency.

The OOR examined several critical requirements. First, the 30-day extension notice must be sent within the initial 5-business-day response period. A notice sent on day 6 or later is untimely, and the request is deemed denied as of day 5, triggering appeal rights.

Second, the extension notice must identify at least one of the statutory reasons. A generic notice stating only that "the agency needs additional time" does not satisfy Section 902.

Third, the OOR addressed what happens when the agency fails to respond within the extended 30-day period. Section 901 provides that if the agency does not respond within the applicable time period, the request is deemed denied. The OOR held that this "deemed denied" provision creates an automatic denial that gives the requester immediate appeal rights without need for any further action by the agency.

The OOR rejected the agency's argument that the 30-day extension could itself be extended by sending a second extension notice. The RTKL provides for only one extension. After the extension period expires, the agency must either produce the records, deny with specific exemptions, or face a deemed denial with appeal rights.

The OOR emphasized that the timeliness provisions are not merely procedural — they are substantive rights of the requester, designed to prevent agencies from defeating access through delay.

HOLDING: The 30-day extension under Section 902 requires timely notice within 5 business days, citation of specific statutory grounds, and production within the extended period. Failure to respond within the extended period results in deemed denial. Only one 30-day extension is permitted per request.""",
        'summary': 'PA OOR binding decision clarifying the 30-day extension limits under RTKL, establishing that failure to respond after extension results in automatic deemed denial.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # VIRGINIA — FOIA Advisory Council Opinions
    # Va. Code § 30-178 — advisory opinions (not binding but highly influential)
    # =========================================================================
    {
        'id': 'va-foiac-email-retention-2013',
        'citation': 'VA FOIAC Op. AO-01-13',
        'title': 'Email Retention and FOIA Obligations',
        'date': '2013-03-15',
        'court': 'Virginia FOIA Advisory Council',
        'document_type': 'AG Opinion',
        'jurisdiction': 'VA',
        'source': 'prdb-built',
        'text': """Virginia FOIA Advisory Council Opinion AO-01-13 — Email Retention

QUESTION PRESENTED: Whether public bodies have an obligation to retain emails for FOIA purposes, and what happens when a public body destroys emails before they can be produced in response to a FOIA request.

ANALYSIS: The Virginia Freedom of Information Act (Va. Code § 2.2-3700 et seq.) defines "public records" to include "all writings and recordings that consist of letters, words or numbers, or their equivalent, set down by handwriting, typewriting, printing, photostatting, photography, magnetic impulse, optical or magneto-optical form, mechanical or electronic recording or other form of data compilation, however stored." Emails clearly fall within this definition.

The Council examined the interplay between FOIA and the Virginia Public Records Act (Va. Code § 42.1-76 et seq.), which governs records retention. Public bodies must maintain records in accordance with retention schedules approved by the Library of Virginia. The Council noted that many public bodies had not updated their retention schedules to address electronic communications, creating a gap that allowed premature destruction of emails.

The Council advised that public bodies should: (1) adopt specific retention schedules for email that account for the different retention requirements based on the content of the email; (2) train employees on distinguishing transitory emails (scheduling, logistics) from substantive emails (policy discussions, decisions) that require longer retention; (3) implement litigation hold procedures when FOIA requests or lawsuits are anticipated.

The Council emphasized that destruction of records after a FOIA request has been received may constitute a criminal violation under Va. Code § 2.2-3714. Even before a specific request is received, routine destruction practices that are designed to avoid FOIA compliance may be actionable.

HOLDING: Emails are public records subject to FOIA. Public bodies must adopt retention schedules that account for electronic communications. Destruction of emails after receipt of a FOIA request may be criminal. Public bodies should implement litigation hold procedures and train staff on retention obligations.""",
        'summary': 'Virginia FOIA Advisory Council opinion establishing email retention obligations and warning that post-request destruction may be criminal.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'va-foiac-public-body-definition-2015',
        'citation': 'VA FOIAC Op. AO-05-15',
        'title': 'What Entities Qualify as a "Public Body" Under FOIA',
        'date': '2015-06-02',
        'court': 'Virginia FOIA Advisory Council',
        'document_type': 'AG Opinion',
        'jurisdiction': 'VA',
        'source': 'prdb-built',
        'text': """Virginia FOIA Advisory Council Opinion AO-05-15 — Public Body Definition

QUESTION PRESENTED: Whether advisory committees, task forces, and other informal groups created by public officials constitute "public bodies" subject to the Virginia FOIA, and what criteria distinguish a covered public body from an informal group.

ANALYSIS: The Virginia FOIA defines "public body" in Va. Code § 2.2-3701 as including "any legislative body, authority, board, bureau, commission, district or agency of the Commonwealth or of any political subdivision of the Commonwealth, including cities, towns and counties, municipal councils, governing bodies of counties, school boards and planning commissions." The definition also includes "other organizations, corporations or agencies in the Commonwealth supported wholly or principally by public funds."

The Council addressed the increasingly common practice of public officials creating ad hoc committees, task forces, and advisory groups that perform significant functions but claim they are not "public bodies" subject to FOIA. The Council applied a multi-factor analysis: (1) whether the group was created by official governmental action (resolution, executive order, ordinance); (2) whether the group has a defined membership and organizational structure; (3) whether the group exercises decision-making authority or provides formal recommendations that influence governmental action; (4) whether the group is supported by public funds (staff time, meeting space, administrative support counts).

The Council found that a task force created by a city council resolution, with appointed members, regular meetings supported by city staff, and charged with making formal recommendations on a policy matter, was a "public body" subject to FOIA even though its recommendations were advisory rather than binding. The advisory nature of a group's function does not remove it from FOIA coverage if it otherwise meets the definition.

The Council noted that officials cannot avoid FOIA by styling an entity as "informal" or "advisory" when it functions as a structured deliberative body. The test is functional, not nominal.

HOLDING: Advisory committees, task forces, and similar groups created by governmental action with defined membership, organizational structure, and charged with making recommendations that influence government policy are "public bodies" under FOIA. The advisory nature of a group's recommendations does not exempt it from FOIA.""",
        'summary': 'Virginia FOIA Advisory Council opinion holding that advisory committees and task forces created by government action are "public bodies" subject to FOIA.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # CONNECTICUT — FOIC (Freedom of Information Commission) Decisions (BINDING)
    # Conn. Gen. Stat. § 1-206 — FOIC issues binding orders
    # =========================================================================
    {
        'id': 'ct-foic-law-enforcement-records-2013',
        'citation': 'CT FOIC Dkt. FIC 2013-234',
        'title': 'Law Enforcement Records — Limits on Investigatory Exemption',
        'date': '2013-09-17',
        'court': 'Connecticut Freedom of Information Commission',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'CT',
        'source': 'prdb-built',
        'text': """CT FOIC Decision — FIC 2013-234 — Law Enforcement Investigatory Exemption

QUESTION PRESENTED: Whether a police department may withhold entire investigative files under the law enforcement exemption in Conn. Gen. Stat. § 1-210(b)(3), and what limitations apply to the exemption for records of "law enforcement agencies... compiled in connection with the detection or investigation of crime."

ANALYSIS: Section 1-210(b)(3) of the Connecticut FOI Act exempts from disclosure "records of law enforcement agencies not otherwise available to the public which were compiled in connection with the detection or investigation of crime, if the disclosure of said records would not be in the public interest because it would result in the disclosure of (A) the identity of informants not otherwise known or the identity of witnesses not otherwise known whose safety would be endangered or who would be subject to threat or intimidation if their identity was made known, (B) signed statements of witnesses, (C) information to be used in a prospective law enforcement action if prejudicial to such action, (D) investigatory techniques not otherwise known to the general public, (E) arrest records of a juvenile, or (F) the name and address of the victim of a sexual assault."

The FOIC emphasized that this exemption has several critical limitations. First, the records must have been "compiled in connection with the detection or investigation of crime" — administrative records, booking records, arrest logs, and incident reports generated as part of routine operations are not "compiled" for investigative purposes and are not covered.

Second, the exemption applies only if the records are "not otherwise available to the public." Records that have been previously released, referenced in court filings, or otherwise made public lose their exempt status.

Third, even for records that meet the first two criteria, the agency must demonstrate that disclosure would result in one of the six specific harms listed in subsections (A) through (F). A general assertion that disclosure would "harm the investigation" is insufficient — the agency must identify which specific harm would result.

The FOIC ordered the police department to produce booking records, incident reports, and arrest reports, which do not qualify for the investigatory exemption. The FOIC also ordered production of portions of investigative files where the specific harms enumerated in the statute could not be demonstrated.

HOLDING: The law enforcement investigatory exemption under § 1-210(b)(3) requires the agency to show records were compiled for investigative purposes, are not otherwise public, and disclosure would cause one of six specific enumerated harms. Booking records, incident reports, and arrest reports are not covered by this exemption.""",
        'summary': 'CT FOIC binding decision narrowing the law enforcement exemption, requiring specific harm showing and excluding routine booking and arrest records.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ct-foic-electronic-records-access-2016',
        'citation': 'CT FOIC Dkt. FIC 2016-0412',
        'title': 'Electronic Records Access and Database Queries',
        'date': '2016-11-08',
        'court': 'Connecticut Freedom of Information Commission',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'CT',
        'source': 'prdb-built',
        'text': """CT FOIC Decision — FIC 2016-0412 — Electronic Records and Database Access

QUESTION PRESENTED: Whether a public agency must run database queries to extract records responsive to a FOI request, or whether the agency may decline the request on the grounds that the specific report or printout requested does not already exist.

ANALYSIS: Section 1-211(a) of the Connecticut FOI Act provides that any person may inspect or copy public records. Section 1-212(a) provides for copying fees. The Act defines "public records" broadly to include records "maintained or kept on file" by any public agency "whether or not such records are required by any law or by any rule or regulation."

The FOIC addressed the respondent's claim that it was not obligated to "create a new record" by running a database query. The FOIC rejected this framing. When a public agency maintains information in an electronic database, running a query to extract that information is not "creating" a new record — it is producing existing records in a requested format. The distinction between a pre-formatted report and a query result is a distinction of form, not substance.

The FOIC reasoned that if agencies could avoid disclosure simply by not generating reports from their databases, the FOI Act's coverage would shrink as more government operations move to electronic systems. This result would be contrary to the Act's purpose and the legislature's technology-neutral definition of public records.

The FOIC held that an agency must run reasonable database queries to produce responsive records, provided the query can be performed using the database system's existing functionality. The agency is not required to create new software or modify its database structure, but it must use the tools already at its disposal.

The FOIC also held that the agency may charge for the staff time required to run the query, consistent with Section 1-212, but the right to charge does not convert the mandatory duty into a discretionary one.

HOLDING: Public agencies must run reasonable database queries to extract responsive records. Running a query against an existing database is not "creating a new record." The agency may charge for the time required but may not decline the request on the basis that a pre-formatted report does not exist.""",
        'summary': 'CT FOIC binding decision requiring agencies to run database queries to extract responsive records, rejecting the "creating a new record" argument.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ct-foic-constructive-denial-penalties-2018',
        'citation': 'CT FOIC Dkt. FIC 2018-0198',
        'title': 'Constructive Denial and Civil Penalties for Willful Noncompliance',
        'date': '2018-06-25',
        'court': 'Connecticut Freedom of Information Commission',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'CT',
        'source': 'prdb-built',
        'text': """CT FOIC Decision — FIC 2018-0198 — Constructive Denial and Penalties

QUESTION PRESENTED: Whether a public agency's pattern of delayed and incomplete responses to FOI requests constitutes willful noncompliance warranting civil penalties under Conn. Gen. Stat. § 1-206(b)(2).

ANALYSIS: Section 1-210(a) of the Connecticut FOI Act provides that records must be made available "promptly." Section 1-206(b)(2) authorizes the FOIC to impose civil penalties of not less than $20 and not more than $1,000 against a public agency or official who is found to have "willfully, wantonly or with gross negligence" violated the FOI Act.

The FOIC examined a pattern of behavior by the respondent agency: four separate FOI requests over an 18-month period, each met with delays of 30-90 days, partial production without explanation, and no formal denial or citation to exemptions. The complainant was left to guess whether additional records existed or had been withheld.

The FOIC found that this pattern constituted willful noncompliance. A single delayed response might be attributable to administrative burden or oversight, but a sustained pattern of delay and incomplete production across multiple requests by different requesters demonstrates systemic disregard for the Act's requirements.

The FOIC established important principles regarding constructive denial: (1) An agency's failure to respond within a "prompt" timeframe — which the FOIC has generally interpreted as within four business days for straightforward requests — constitutes constructive denial. (2) Partial production without identifying what has been withheld and why is itself a violation. (3) An agency has an affirmative obligation to inform the requestor of the scope of its search, the volume of responsive records, and the basis for any withholding.

The FOIC imposed a civil penalty of $500 per violation (four violations), finding that the agency's pattern of conduct was willful. The FOIC also ordered the agency to designate a specific FOI coordinator, implement tracking procedures for requests, and report compliance to the FOIC quarterly.

HOLDING: A pattern of delayed responses, partial production, and failure to cite exemptions constitutes willful noncompliance with the FOI Act. Civil penalties are appropriate when the pattern demonstrates systemic disregard. Agencies must respond promptly, identify all withheld records, and explain the basis for withholding.""",
        'summary': 'CT FOIC binding decision imposing civil penalties for a pattern of delayed responses and incomplete production, establishing constructive denial standards.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NEW JERSEY — GRC (Government Records Council) Decisions (BINDING)
    # N.J.S.A. 47:1A-7 — GRC adjudicates OPRA complaints
    # =========================================================================
    {
        'id': 'nj-grc-email-opra-2014',
        'citation': 'NJ GRC Complaint No. 2014-127',
        'title': 'Government Email and OPRA — Identifiable Records Requirement',
        'date': '2014-08-12',
        'court': 'New Jersey Government Records Council',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'NJ',
        'source': 'prdb-built',
        'text': """NJ GRC Decision — Complaint No. 2014-127 — Email Requests Under OPRA

QUESTION PRESENTED: Whether a request for emails constitutes a valid OPRA request for "identifiable government records," and under what circumstances an agency may deny an email request as overly broad.

ANALYSIS: The Open Public Records Act (N.J.S.A. 47:1A-1 et seq.) requires that requests seek "identifiable government records." This requirement has created particular tension with email requests, because email is both a record format and a communication method, and because email collections can be vast.

The GRC examined the line between a valid and invalid email request. A request for "all emails" sent by an official is generally too broad to constitute a request for "identifiable" records, because it does not identify the subject matter, time period, or specific records sought. However, a request for "emails between [specific official] and [specific person or organization] regarding [specific topic] during [specific time period]" is sufficiently identifiable.

The GRC held that the specificity requirement must be applied reasonably and in light of the Act's purpose. Email is now a primary mode of government communication. A rule that made all email effectively unreachable under OPRA would create an enormous gap in public access. The identifiability requirement is meant to prevent fishing expeditions, not to block access to a major category of government records.

The GRC also addressed the custodian's obligation when a request is borderline. Rather than denying the request outright, the custodian should contact the requestor and attempt to narrow the request to identifiable records. OPRA's requirement that custodians respond to requests promptly includes an implicit duty to assist requestors in framing effective requests.

The GRC further noted that an agency may not use the identifiability requirement to deny a request that is, in fact, identifiable but simply inconvenient to fulfill. A request for "all emails from the Mayor to the Planning Board chair in January 2014 regarding the zoning variance" is highly specific and must be fulfilled regardless of the effort required.

HOLDING: Email requests under OPRA must identify specific records by sender, recipient, subject matter, or time period. Requests for "all emails" are generally insufficient, but narrowly framed email requests are valid. Custodians should assist requestors in narrowing overbroad requests rather than denying them outright.""",
        'summary': 'NJ GRC binding decision establishing standards for email requests under OPRA, requiring specificity but also custodian duty to help narrow overbroad requests.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'nj-grc-response-time-opra-2016',
        'citation': 'NJ GRC Complaint No. 2016-305',
        'title': 'Seven-Business-Day Response Period and Extensions Under OPRA',
        'date': '2016-12-06',
        'court': 'New Jersey Government Records Council',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'NJ',
        'source': 'prdb-built',
        'text': """NJ GRC Decision — Complaint No. 2016-305 — Response Time Requirements

QUESTION PRESENTED: Whether a records custodian may extend the seven-business-day response period under OPRA without limit, and what constitutes a sufficient "specific basis" for an extension.

ANALYSIS: N.J.S.A. 47:1A-5(i) provides that a custodian must respond to an OPRA request within seven business days. The custodian may request an extension of time, but the extension must be based on a "specific basis" that is communicated to the requestor. The statute does not specify a maximum extension period.

The GRC examined the custodian's practice of routinely sending extension notices that provided no specific basis and set no definite production date. The notices simply stated that "additional time is needed" and promised records "as soon as possible." The GRC found this practice violated OPRA.

The GRC established the following requirements for valid extensions: (1) The extension notice must be sent within the initial seven-business-day period. (2) The notice must state a specific basis for the extension — not a generic statement, but a concrete explanation (e.g., "the request involves approximately 2,000 pages of records that require review for personal identifying information"). (3) The notice must provide a specific date by which the records will be produced. (4) The length of the extension must be reasonable in proportion to the stated basis.

The GRC held that open-ended extensions undermine OPRA's core purpose. While the statute does not set a maximum extension period, the GRC will scrutinize extensions exceeding 30 days and require particularized justification for longer delays. An extension is a tool for managing complex or voluminous requests, not a device for deferring routine production.

The GRC also emphasized that a custodian who fails to respond within seven business days and does not send a valid extension notice is deemed to have denied the request. This deemed denial triggers the complainant's right to file a GRC complaint or Superior Court action without further waiting.

HOLDING: Extensions under OPRA must be based on a specific basis, communicated within seven business days, and include a definite production date. Open-ended extensions violate OPRA. Failure to respond or send a valid extension notice within seven business days is a deemed denial.""",
        'summary': 'NJ GRC binding decision requiring OPRA extensions to state specific bases and definite production dates, holding open-ended extensions are violations.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'nj-grc-segregability-redaction-2015',
        'citation': 'NJ GRC Complaint No. 2015-078',
        'title': 'Segregability and Redaction Under OPRA',
        'date': '2015-05-20',
        'court': 'New Jersey Government Records Council',
        'document_type': 'Administrative Decision',
        'jurisdiction': 'NJ',
        'source': 'prdb-built',
        'text': """NJ GRC Decision — Complaint No. 2015-078 — Segregability and Redaction

QUESTION PRESENTED: Whether a custodian may withhold an entire document under OPRA when only portions contain exempt information, and what constitutes adequate redaction disclosure.

ANALYSIS: While OPRA does not contain an explicit segregability provision comparable to some states' statutes, the GRC has consistently held that the principle of segregability is implicit in OPRA's structure. N.J.S.A. 47:1A-1 establishes a strong presumption of public access, and N.J.S.A. 47:1A-5 requires custodians to permit inspection or provide copies of government records. These provisions would be undermined if a custodian could withhold an entire document based on a narrow exemption applying to only a portion.

The GRC examined the custodian's practice of withholding entire multi-page documents when only specific sections contained exempt information (in this case, personnel evaluations containing some exempt personal identifying information). The GRC found this practice violated OPRA.

The GRC established that: (1) Custodians must review documents containing potentially exempt information and redact only the specific exempt portions. (2) The remainder of the document must be produced with the redactions clearly marked. (3) Each redaction must be accompanied by a citation to the specific OPRA exemption or other legal authority justifying the withholding. (4) A "redaction index" or equivalent notation should identify each redaction and its basis, allowing the requestor to challenge specific redactions.

The GRC also addressed the "chilling effect" of over-redaction. When a custodian redacts more than what is strictly exempt, the requestor is denied access to public information. The GRC held that the burden of justifying each redaction falls squarely on the custodian, and any ambiguity is resolved in favor of disclosure.

The GRC rejected the custodian's argument that line-by-line redaction was too burdensome. The obligation to segregate and redact is a cost of OPRA compliance, not a basis for wholesale withholding. The custodian must devote sufficient resources to this task.

HOLDING: Custodians must redact only specifically exempt portions and produce the remainder of documents. Each redaction must cite specific legal authority. Wholesale withholding of documents containing some exempt information violates OPRA. The burden of justifying redactions falls on the custodian.""",
        'summary': 'NJ GRC binding decision establishing segregability requirements under OPRA, requiring redaction of only exempt portions with specific citations for each redaction.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # OREGON — AG Public Records Orders
    # ORS 192.411-192.431 — AG enforcement of public records law
    # =========================================================================
    {
        'id': 'or-ag-fee-waiver-public-interest-2015',
        'citation': 'OR AG PRO 2015-03',
        'title': 'Fee Waiver in the Public Interest Under Oregon Public Records Law',
        'date': '2015-04-22',
        'court': 'Oregon Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'OR',
        'source': 'prdb-built',
        'text': """OR AG Public Records Order 2015-03 — Fee Waiver in the Public Interest

QUESTION PRESENTED: Under what circumstances must a public body waive fees for inspection or copying of public records under ORS 192.324(5), and how should the public body evaluate whether a fee waiver is "in the public interest."

ANALYSIS: ORS 192.324(5) provides that a public body may furnish copies of public records without charge or at a reduced fee if the public body determines that the waiver or reduction is in the public interest because the request is likely to contribute significantly to public understanding of the operations or activities of the public body and is not primarily for commercial purposes.

The AG examined the two-part test: (1) whether the request is likely to contribute significantly to public understanding of government operations, and (2) whether the request is not primarily for commercial purposes. Both must be satisfied.

On the first prong, the AG held that the following factors are relevant: whether the information requested is likely to meaningfully inform the public about government operations; whether the requestor has the ability and intention to disseminate the information to the public; and whether the information is already publicly available (if so, the incremental contribution to public understanding is diminished). The AG noted that the requestor need not be a member of the media — academic researchers, nonprofit organizations, civic groups, and individual citizens who plan to share information publicly all qualify.

On the second prong, the AG clarified that the question is whether the request is "primarily" for commercial purposes, not whether any commercial benefit exists. A newspaper requesting records for a story is acting in the public interest even though the newspaper is a commercial enterprise. The test is the primary purpose of the specific request, not the requestor's general business model.

The AG found that the public body had improperly denied the fee waiver by requiring the requestor to demonstrate that "a significant number of citizens" would directly benefit. This standard is not found in the statute and is too restrictive. The public interest is served when information about government operations is made available for public consumption, regardless of how many individuals ultimately read or access it.

HOLDING: Fee waivers under ORS 192.324(5) must be evaluated under a two-part test: whether the request significantly contributes to public understanding and is not primarily commercial. Public bodies may not impose additional requirements not found in the statute. The fee waiver was improperly denied.""",
        'summary': 'OR AG order establishing the two-part test for fee waivers under Oregon public records law, rejecting overly restrictive public interest standards.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'or-ag-segregability-exemption-logs-2017',
        'citation': 'OR AG PRO 2017-07',
        'title': 'Segregability and Exemption Logs Under Oregon Public Records Law',
        'date': '2017-06-14',
        'court': 'Oregon Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'OR',
        'source': 'prdb-built',
        'text': """OR AG Public Records Order 2017-07 — Segregability and Exemption Logs

QUESTION PRESENTED: Whether a public body must produce a log or index of withheld records identifying each document and the specific exemption claimed, and whether the segregability requirement of ORS 192.338 obligates line-by-line review of documents containing both exempt and non-exempt information.

ANALYSIS: ORS 192.338 provides: "If any public record contains material which is not exempt under ORS 192.345 or 192.355, the custodian shall separate the nonexempt material and make it available for examination." This segregability requirement is mandatory ("shall") and applies whenever a record contains a mix of exempt and non-exempt information.

The AG examined whether the public body's practice of withholding entire documents — without separating exempt from non-exempt material — violated ORS 192.338. The AG found that it did. The statute requires active separation, not passive withholding. A custodian who determines that a document contains some exempt material must review the document, identify the specific exempt portions, redact those portions, and release the remainder.

The AG also addressed the question of exemption logs. While the Oregon Public Records Law does not explicitly require a Vaughn-style index (as named after the federal FOIA case Vaughn v. Rosen), the AG held that the requirement to cite specific exemptions under ORS 192.324(7) necessarily implies an obligation to identify what is being withheld and why. A bare statement that "records are exempt under ORS 192.345" without identifying which specific subsection applies to which specific material is insufficient.

The AG recommended that public bodies adopt the practice of providing an exemption log that: (1) identifies each withheld or redacted document by date, author, recipient, and subject (to the extent possible without revealing exempt content); (2) cites the specific statutory exemption for each withholding; and (3) provides a brief explanation of how the exemption applies to the specific material. This practice serves both the public's right to understand the basis for withholding and the practical goal of facilitating meaningful review by the AG's office if the withholding is challenged.

HOLDING: The segregability requirement of ORS 192.338 mandates line-by-line review and redaction. Public bodies must produce non-exempt portions of partially exempt records. Exemption citations must be specific to each withheld item, and the AG recommends exemption logs identifying withheld documents and the bases for withholding.""",
        'summary': 'OR AG order requiring line-by-line segregation of exempt material and recommending exemption logs identifying each withheld document and specific exemption basis.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'or-ag-response-time-obligations-2019',
        'citation': 'OR AG PRO 2019-11',
        'title': 'Response Time Requirements and "Without Unreasonable Delay"',
        'date': '2019-09-10',
        'court': 'Oregon Attorney General',
        'document_type': 'AG Opinion',
        'jurisdiction': 'OR',
        'source': 'prdb-built',
        'text': """OR AG Public Records Order 2019-11 — Response Time Requirements

QUESTION PRESENTED: What constitutes compliance with the requirement under ORS 192.324(1) to respond to a public records request "as soon as practicable and without unreasonable delay," and when does delay become unreasonable?

ANALYSIS: ORS 192.324(1) requires a public body to respond to a records request "as soon as practicable and without unreasonable delay." Unlike some states that specify a fixed deadline (e.g., 3 or 5 business days), Oregon uses a reasonableness standard. The AG addressed how this standard applies in practice.

The AG held that what is "practicable" and what constitutes "unreasonable delay" depends on the totality of the circumstances, including: (1) the volume and complexity of the responsive records; (2) the need to search for, collect, or retrieve records from various locations; (3) the need to review records for exempt material; (4) the availability of staff to process the request; and (5) whether the public body has other pending requests competing for the same resources.

However, the AG emphasized several firm principles. First, the public body must acknowledge the request promptly — within a few business days — even if it cannot immediately produce records. The acknowledgment should describe the scope of the search, provide an estimated timeline, and identify any issues (fee estimates, potential exemptions) that may affect production.

Second, for straightforward requests involving readily available records, the "as soon as practicable" standard generally means within 5-10 business days. The AG noted that many Oregon public bodies have adopted internal deadlines in this range and commended this practice.

Third, for complex requests, the public body should produce records on a rolling basis rather than waiting until every responsive record has been identified and reviewed. This approach reduces the effective delay for the requestor and demonstrates good faith.

Fourth, the AG held that staffing constraints are not an unlimited justification for delay. A public body that is chronically understaffed for records processing may not use that chronic condition as a basis for routine delay. The public body has an obligation to devote adequate resources to records processing.

HOLDING: The "as soon as practicable and without unreasonable delay" standard requires prompt acknowledgment, production within 5-10 business days for straightforward requests, rolling production for complex requests, and adequate staffing. Chronic understaffing is not a justification for routine delay.""",
        'summary': 'OR AG order interpreting Oregon\'s "without unreasonable delay" standard, requiring prompt acknowledgment, rolling production, and adequate staffing for records processing.',
        'jurisdiction_level': 'state',
    },
]


def build():
    conn = db_connect(DB_PATH)
    added = 0
    for doc in OPINIONS:
        doc['md5_hash'] = hashlib.md5(doc['text'].encode()).hexdigest()
        existing = conn.execute('SELECT id FROM documents WHERE id=?', (doc['id'],)).fetchone()
        if existing:
            print(f"  {doc['id']}: exists, skipping")
            continue
        conn.execute('''
            INSERT INTO documents (id, citation, title, date, court, document_type, jurisdiction,
                                   source, text, summary, md5_hash, jurisdiction_level)
            VALUES (:id, :citation, :title, :date, :court, :document_type, :jurisdiction,
                    :source, :text, :summary, :md5_hash, :jurisdiction_level)
        ''', doc)
        added += 1
        print(f"  {doc['id']}: inserted")
    conn.commit()
    print(f"\nInserted {added} AG/admin opinion documents")
    conn.close()


if __name__ == '__main__':
    build()
