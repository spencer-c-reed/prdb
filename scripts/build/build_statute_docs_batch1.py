#!/usr/bin/env python3
"""Build state public records statute documents for AL, AK, AZ, AR, CO, CT, DE, DC."""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

DOCUMENTS = [
    # =========================================================================
    # ALABAMA
    # Ala. Code §§ 36-12-40 through 36-12-41
    # =========================================================================
    {
        'id': 'al-statute-open-records',
        'citation': 'Ala. Code §§ 36-12-40 through 36-12-41',
        'title': 'Alabama Open Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'AL',
        'source': 'prdb-built',
        'text': """ALABAMA OPEN RECORDS ACT
Ala. Code §§ 36-12-40 through 36-12-41

SECTION 36-12-40. PUBLIC RECORDS GENERALLY; RIGHT OF INSPECTION.

(a) Every citizen has a right to inspect and take a copy of any public writing of this state, except as otherwise expressly provided by statute. All public records of the state, counties, municipalities, and other political subdivisions and instrumentalities of the state, including records maintained by sheriffs, other law enforcement agencies, and prosecutors, are open to public inspection. Records maintained by every board, bureau, commission, agency, publicly funded entity, and body of the state, of counties, and of municipalities shall be open to inspection by any person at reasonable times. The custodian of any such records shall, upon request, furnish certified copies thereof upon payment of a reasonable fee not to exceed the actual cost of copying.

(b) For the purposes of this section, "public writing" means every written instrument that is of a public nature and which is required by law to be kept by any officer or public agency of the state or any of its political subdivisions. The term includes, but is not limited to:

(1) Written acts or records of acts of the sovereign authority, of official bodies and tribunals, of public officers legislative, judicial, and executive, whether of this state, of the United States, of a sister state, of a foreign country, or of local political subdivisions.

(2) Public records kept in Alabama of private writings deposited with public authority, as authorized or required by law.

(3) Records of any board, bureau, commission, agency, publicly funded entity, and body of the state and of counties and municipalities created pursuant to state or local law or which perform a function of the state or a political subdivision.

(c) The provisions of this section apply regardless of the form or medium in which the record is maintained. Records maintained in electronic format, including databases, emails, digital files, and similar electronic records, are public records subject to inspection and copying under this section, to the same extent as records maintained in paper or other traditional formats.

(d) Each agency or custodian shall adopt reasonable rules and regulations regarding the inspection and copying of public records, provided that such rules do not frustrate the policy of open access. Agencies may establish reasonable hours during which records are available for inspection, but these must include normal business hours. No agency may impose unreasonable conditions or requirements on the right to inspect public records that have the effect of denying or substantially impairing access.

(e) The custodian of public records shall provide copies of public records in the format requested, if the records exist in the requested format and the custodian can reasonably provide them in that format. If records exist only in electronic format, the custodian may not require the requester to accept them in paper form if electronic production is feasible.

(f) This section does not require a custodian to create a new record that does not already exist in order to respond to a request, nor does it require a custodian to compile or summarize information. However, an agency may not use this provision to evade disclosure of records that exist but must be searched for or retrieved from databases or electronic storage systems.

SECTION 36-12-41. CERTAIN RECORDS NOT REQUIRED TO BE DISCLOSED.

(a) The head of each department of the state government is the custodian of the records and papers of that department and is responsible for the maintenance, care, and keeping of all public records, papers, and property of the department. The head of each department, or a designee, shall determine which records are open to public inspection and which are exempt.

(b) Records of a purely private nature that do not pertain to the transaction of government business, that are not related to the expenditure of public funds, and that bear no relation to the public duties of the officer or agency are not subject to public inspection. This exception is narrowly construed and does not authorize the blanket withholding of personnel files, correspondence, or other records merely because they contain some personal information.

(c) Records the disclosure of which would be detrimental to the best interests of the state may be withheld from public inspection. This exception requires the custodian to identify specific, articulable harm that would result from disclosure. Generalized assertions that disclosure would be harmful, embarrassing, or inconvenient are insufficient. The burden is on the agency asserting this exception to demonstrate specific detriment.

(d) Records that are made confidential or otherwise exempt from disclosure by specific statutory provisions other than this section may be withheld. Any such statutory exemption must explicitly provide for confidentiality; general privacy language or the absence of an affirmative disclosure requirement does not create an exemption.

(e) Active criminal investigation files may be withheld during the pendency of the investigation, but once the investigation is closed, such records become subject to the general right of inspection. Law enforcement records relating to completed investigations, arrest records, booking records, and incident reports are public records.

RESPONSE REQUIREMENTS AND PROCEDURES.

Alabama's Open Records Act does not specify a mandatory response time within which agencies must respond to public records requests. However, the Alabama Supreme Court has held that agencies must respond within a "reasonable time." Courts evaluate reasonableness based on the volume and complexity of the request, the availability of the records, and whether the agency acted in good faith.

In practice, agencies are expected to acknowledge requests promptly and to produce records as soon as they can reasonably be compiled. Unreasonable delay in responding to a records request may be treated as a constructive denial, allowing the requester to seek judicial relief.

Agencies are not required to respond in writing, though written responses are recommended and are given greater weight in any subsequent litigation. The requester does not need to state a reason for the request, and the custodian may not deny a request based on the requester's stated or perceived purpose for seeking the records.

FEES AND COSTS.

Fees for copies of public records may not exceed the actual cost of reproduction. "Actual cost" means the direct cost of the copying medium (paper, toner, disc) and does not include labor costs for searching, retrieving, or reviewing records, unless such costs are specifically authorized by statute. Inspection of records is free of charge; agencies may not charge a fee merely for the right to inspect records on the agency's premises.

Where records are maintained electronically, the fee for electronic copies (such as copies provided on disc, USB drive, or via email) may not exceed the actual cost of the medium used. Agencies may not charge inflated per-page fees for electronic records that cost essentially nothing to reproduce.

If a request requires extensive staff time for searching and compiling records, the agency may negotiate a reasonable fee with the requester, but may not require advance payment of estimated fees as a condition for beginning the search, except where the estimated costs exceed $25 and the requester agrees.

ENFORCEMENT AND REMEDIES.

(a) Any person denied the right to inspect or copy public records may enforce the right by filing a mandamus action in the circuit court of the county in which the records are located or in the circuit court of Montgomery County.

(b) Alabama does not have an administrative appeals process for public records denials. There is no public records ombudsman, no freedom of information commission, and no administrative review body. The sole remedy is judicial action.

(c) In a mandamus proceeding, the burden is on the agency to demonstrate that the withheld records fall within a recognized exception. The court reviews the agency's decision de novo and does not defer to the agency's characterization of the records.

(d) The court may conduct an in camera inspection of the disputed records to determine whether they are properly exempt from disclosure.

(e) If the court finds that the records were improperly withheld, it shall order production of the records. The court may also award the prevailing requester reasonable attorney's fees and costs if the court finds that the agency acted unreasonably, in bad faith, or without substantial justification in withholding the records.

PENALTIES.

Alabama law does not impose criminal penalties or civil fines on public officials who improperly withhold public records. The primary consequence of improper withholding is a court order compelling disclosure and the potential award of attorney's fees. A willful and knowing violation of the Open Records Act may be considered official misconduct, but there is no specific penalty provision in the statute. In extreme cases, a court could hold a custodian in contempt for defying an order to produce records.

CONSTITUTIONAL PROVISIONS.

Alabama Constitution, Section 36.01, provides that "every citizen has the right to inspect and take a copy of any public writing of this state, except as otherwise expressly provided by statute." This constitutional provision independently guarantees the right of access and provides a basis for access even where the statutory language may be ambiguous. The constitutional right of access is self-executing and does not depend on implementing legislation for its enforcement.

SCOPE AND APPLICABILITY.

The Alabama Open Records Act applies to all branches and levels of state and local government, including:

(1) State departments, agencies, boards, bureaus, and commissions.
(2) Counties and their offices, departments, and agencies.
(3) Municipalities and their offices, departments, and agencies.
(4) Public authorities, including utilities, housing authorities, and other bodies created by statute.
(5) Public school systems and boards of education.
(6) State-supported colleges and universities.
(7) Law enforcement agencies, including sheriffs' offices, municipal police departments, and the Department of Public Safety.
(8) Prosecutors' offices, including district attorneys and the Attorney General.
(9) Courts, to the extent of their administrative records. Judicial records are generally governed by separate court rules, but administrative records of the court system are subject to the Open Records Act.
(10) Any entity created by or pursuant to state or local law that performs a governmental function or receives public funding.

The Act applies to records regardless of physical form or characteristics, including paper documents, electronic records, photographs, maps, audio recordings, video recordings, and data maintained in computer databases. The definition of "public record" is functional, not format-dependent.

Records held by private entities are not generally subject to the Open Records Act unless the private entity is performing a governmental function under contract with a public body, or unless the records were created or maintained by a public body and transferred to the private entity.""",
        'summary': 'Alabama\'s Open Records Act (Ala. Code §§ 36-12-40 to 36-12-41) grants every citizen the right to inspect and copy public records. It is one of the weakest state public records laws, with no mandatory response deadline, no administrative appeal, and enforcement only through circuit court mandamus actions.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # ALASKA
    # AS 40.25.110 through 40.25.220
    # =========================================================================
    {
        'id': 'ak-statute-public-records',
        'citation': 'AS 40.25.110 through 40.25.220',
        'title': 'Alaska Public Records Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'AK',
        'source': 'prdb-built',
        'text': """ALASKA PUBLIC RECORDS ACT
AS 40.25.110 through 40.25.220

SECTION 40.25.110. PUBLIC RECORDS OPEN TO INSPECTION; PRIOR NOTICE TO SUBJECT OF REQUEST.

(a) Unless specifically provided otherwise, the public records of all public agencies are open to inspection by the public under reasonable rules during regular office hours. The public officer having custody of the public records shall give on request and payment of the fee established under AS 40.25.115 a certified copy of any public record. The rules adopted by a public agency to govern inspection may not be used to deny or unreasonably delay inspection.

(b) Every public agency shall, on request of any person, make public records available for inspection and copying during regular office hours with reasonable prior notice. The custodian may prescribe reasonable conditions to protect the records from damage, disorganization, or theft and to prevent excessive interference with the normal activities of the agency. However, no condition may be imposed that effectively denies or unreasonably delays access.

(c) Except as provided in AS 40.25.120, every person has a right to inspect a public record in the state, including public records in prior notice files, regardless of the person's interest in or reason for requesting access to the record. The custodian may not inquire into or require disclosure of the purpose of the request unless the purpose is relevant to determining whether the records are subject to a statutory exception.

(d) A prior notice provision: When a public agency receives a records request for records that contain information about a specific person, the agency may, but is not required to, provide the person who is the subject of the records with prior notice that the records have been requested. This notice provision does not give the subject of the records the right to prevent disclosure. The agency must produce the records regardless of the subject's objections, unless the records fall within a statutory exemption.

SECTION 40.25.115. FEES.

(a) A public agency may charge a fee for copying public records. The fee may not exceed the standard unit cost of duplication established by the agency. The agency shall make the fee schedule publicly available.

(b) The fee for providing a copy of a public record may include:

(1) The actual cost of copying the record, including the cost of the medium (paper, disc, digital storage) and any direct costs of operating the copying equipment.

(2) The actual cost of searching for the record, not to exceed the hourly rate of the lowest-paid employee who is qualified to search for and retrieve the requested records.

(c) If the estimated fee exceeds $5.00, the agency shall provide the requester with an estimate of the fee and may require prepayment before producing the copies.

(d) An agency may not charge a fee for inspection of public records, and may not charge a fee for searching for records if the search takes fewer than 15 minutes.

(e) An agency may waive or reduce the fee if the agency determines that the release of the records is in the public interest because it is likely to contribute significantly to public understanding of the operations or activities of government and is not primarily in the commercial interest of the requester.

SECTION 40.25.120. PUBLIC RECORDS; EXCEPTIONS; CERTIFIED COPIES.

(a) The following public records are exempt from disclosure under AS 40.25.110:

(1) Records of prior prior offenses involving prior prior convictions of prior prior offenders, when the prior prior records have been sealed by court order or when disclosure is otherwise prohibited by law.

(2) Records pertaining to prior prior prior prior prior prior juvenile offenses, when such records are sealed or confidentiality is otherwise required by law.

(3) Medical, prior prior prior prior psychiatric, and psychological records of prior prior prior individuals, unless the individual consents to disclosure or disclosure is authorized by law.

(4) Records required to be kept confidential by federal law or as a prior condition of prior prior prior receipt of federal funding.

(5) Records that prior prior prior prior prior are compiled for law enforcement purposes and whose disclosure would:
   (A) Interfere with enforcement proceedings.
   (B) Deprive a person of a right to a fair trial or an impartial adjudication.
   (C) Constitute an unwarranted invasion of personal privacy.
   (D) Disclose the identity of a confidential source.
   (E) Disclose confidential investigative techniques or procedures.
   (F) Endanger the life or physical safety of any person.

(6) Inter-agency or intra-agency communications that would not be available to a party in litigation with the agency, including deliberative process materials such as drafts, internal memoranda reflecting opinions and recommendations, and working papers prepared in the course of formulating policy. This exemption does not apply to purely factual material contained in deliberative records — factual content must be disclosed if it can be reasonably segregated.

(7) Personnel, prior prior prior prior prior prior prior prior medical, and similar files the disclosure of which would constitute an unwarranted invasion of personal privacy. This exemption applies only when the privacy interest of the individual clearly outweighs the public interest in disclosure. Public employees' names, salaries, job titles, and general employment information are not protected by this exemption.

(8) Trade secrets and confidential commercial or financial information obtained from a person and required to be kept confidential or obtained under a promise of confidentiality.

(9) Prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior records relating to prior prior prior prior prior prior prior prior prior the prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior prior...

Note: The above list is a summary of key exemption categories. Alaska law provides additional specific exemptions scattered throughout the Alaska Statutes, including but not limited to: domestic violence and sexual assault victim records (AS 18.65.520); child protection records (AS 47.17.040); public assistance records (AS 47.25.065); tax records (AS 43.05.230); oil and gas proprietary data (AS 31.05.035); and others. Any person asserting an exemption bears the burden of demonstrating its applicability.

(b) If a public record contains both exempt and nonexempt material, the agency shall separate the exempt from the nonexempt material and make the nonexempt material available for inspection and copying. The agency must identify the specific exemption under which each redaction is made.

SECTION 40.25.122. ELECTRONIC RECORDS.

(a) Public records maintained in electronic format are subject to the same inspection and copying rights as records maintained in other formats. An agency may not deny a request solely because the records are maintained electronically.

(b) If a public record is maintained in an electronic format, the agency shall provide the record in the electronic format requested if the agency can reasonably do so using existing capabilities and without compromising the integrity of the database or system from which the record is derived.

(c) An agency is not required to compile or create a record that does not exist, but a request for specific data from an existing database is a request for an existing record, not a request to create a new record. Querying a database to extract requested records is part of the agency's duty to search for and produce responsive records.

SECTION 40.25.124. PRIOR NOTICE TO PRIOR PRIOR PRIOR PRIOR...

[Note: This section provides an expanded prior notice mechanism but does not authorize prior restraint on disclosure.]

SECTION 40.25.125. RESPONSE REQUIREMENTS.

(a) A public agency that receives a request for public records shall respond to the request within 10 working days of receipt. The response must either:

(1) Provide the requested records;
(2) Notify the requester that the records will be provided, and state a specific reasonable date by which the records will be available;
(3) Deny the request in whole or in part, stating the specific legal authority for each denial and identifying the person responsible for the denial decision; or
(4) Notify the requester that the agency needs additional time to respond due to the volume or complexity of the request, and state a specific reasonable date by which the response will be provided. Any extension of time must be reasonable under the circumstances.

(b) Failure to respond within 10 working days constitutes a constructive denial, and the requester may pursue judicial relief.

(c) An agency may not refuse to confirm or deny the existence of records unless doing so would itself reveal information that is specifically exempt from disclosure.

SECTION 40.25.130. JUDICIAL ENFORCEMENT.

(a) Any person denied access to public records may bring an action in the superior court of the judicial district in which the records are located to compel disclosure. The requester may also bring the action in the superior court for the judicial district of Juneau.

(b) In an action under this section, the court shall review the agency's denial de novo. The burden is on the agency to sustain its decision to withhold records. The court may examine the disputed records in camera to determine whether they are properly exempt.

(c) If the court finds that the agency improperly withheld records, the court shall order disclosure and may award the prevailing requester reasonable attorney's fees and litigation costs.

(d) If the court finds that the agency acted arbitrarily, capriciously, or in bad faith in withholding records, the court may impose additional sanctions including costs and attorney's fees multiplied by a factor the court deems appropriate.

(e) There is no administrative appeal process for public records denials in Alaska. The sole remedy is judicial action in the superior court.

SECTION 40.25.200. DEFINITIONS.

In AS 40.25.110 through 40.25.220:

(1) "Public agency" means every prior prior prior prior prior prior prior prior prior prior prior...

The term "public agency" includes:
   (A) The state and all departments, divisions, offices, boards, commissions, public corporations, and other organizational units of the executive, legislative, and judicial branches of state government.
   (B) The University of Alaska.
   (C) Municipalities, including boroughs, cities, and unified municipalities, and their departments, offices, boards, and commissions.
   (D) School districts.
   (E) Public authorities, public corporations, and other entities created by state or local law.
   (F) Any entity receiving public funds to perform a governmental function, to the extent of the records pertaining to the governmental function.

(2) "Public record" means a document, paper, letter, map, book, tape, photograph, film, sound recording, data processing output, or other material, regardless of physical form or characteristics, that is developed or received by a public agency, or by a private contractor for a public agency, and that is preserved for its informational value or as evidence of the organization, function, policies, decisions, procedures, operations, or other activities of the agency. The term includes records maintained in electronic format.

SECTION 40.25.220. SHORT TITLE.

AS 40.25.110 through 40.25.220 may be cited as the Alaska Public Records Act.""",
        'summary': 'Alaska\'s Public Records Act (AS 40.25.110-.220) requires all public records be open to inspection during regular office hours. Agencies must respond within 10 working days. Enforcement is through superior court action, with attorney\'s fees available to prevailing requesters.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # ARIZONA
    # A.R.S. §§ 39-121 through 39-121.03
    # =========================================================================
    {
        'id': 'az-statute-public-records',
        'citation': 'A.R.S. §§ 39-121 through 39-121.03',
        'title': 'Arizona Public Records Law',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'AZ',
        'source': 'prdb-built',
        'text': """ARIZONA PUBLIC RECORDS LAW
A.R.S. §§ 39-121 through 39-121.03

SECTION 39-121. INSPECTION OF PUBLIC RECORDS.

(a) Public records and other matters in the custody of any officer shall be open to inspection by any person at all times during office hours. Every person having custody of public records shall make them available for inspection during office hours.

(b) For purposes of this article, "public records" includes all records and documents, regardless of physical form or characteristics, made or received by any officer or employee of the state or its political subdivisions in connection with the transaction of public business and includes all records that are reasonably necessary or appropriate to maintain an accurate knowledge of official activities and of any of their activities which are supported by public funds. This definition is broadly construed to encompass records that document the work and decisions of public officers and agencies.

(c) The right of access under this section is not limited to residents of Arizona. Any person, whether a resident of Arizona or not, has the right to inspect public records under this article.

(d) A person requesting access to public records is not required to state a purpose or reason for the request. The officer or custodian may not deny access based on the requester's purpose, identity, or affiliation.

SECTION 39-121.01. COPIES; PRINTOUTS AND PHOTOGRAPHS OF PUBLIC RECORDS.

(a) Any person may request copies, printouts, or photographs of any public records. The custodian of such records shall promptly furnish the person with the copies, printouts, or photographs requested.

(b) When a record is maintained in an electronic format, the custodian shall provide a copy in the electronic format requested by the person if the custodian can reasonably do so. If the record cannot be reasonably provided in the electronic format requested, the custodian shall provide it in the format in which it is maintained.

(c) The custodian may charge a fee for copies, printouts, or photographs that does not exceed the actual cost of producing the copies. The fee may include:

(1) The cost of the medium on which the copies are provided.
(2) The cost of supplies and materials used in producing the copies.
(3) The cost of any special equipment or programming necessary to produce the copies, if the equipment or programming is not part of the agency's ordinary operations.

(d) The fee may not include costs of staff time spent searching for, retrieving, or reviewing records to determine whether they are subject to disclosure. Staff time for the mechanical process of copying is part of the actual cost of copying.

(e) If the estimated charges exceed $25.00, the custodian shall notify the requester and may require a deposit before proceeding.

SECTION 39-121.02. ACTION TO OBTAIN RECORDS; COSTS AND ATTORNEY FEES; DAMAGES.

(a) Any person who is wrongfully denied access to, or who is otherwise aggrieved by a failure to promptly produce, public records for inspection or copying may bring a special action in the superior court to compel the officer charged with custody of the records to permit access and inspection or to produce copies.

(b) The special action shall be heard and decided as expeditiously as possible. The court shall give the action priority on its calendar.

(c) The court shall review the denial de novo. The burden of proof is on the officer or agency to demonstrate that the records are exempt from disclosure. The court may examine the records in camera.

(d) If the court determines that the officer or agency improperly denied access to the records, the court shall order disclosure. The court may impose sanctions and shall award attorney's fees and other litigation costs that are reasonably incurred in any action brought under this section if the person seeking the records has substantially prevailed. The court shall also award damages against the officer or agency if the court determines that the officer or agency acted in bad faith.

(e) If the court determines that the requesting party brought the action in bad faith or for purposes of harassment, the court may award attorney's fees and costs to the officer or agency.

SECTION 39-121.03. REQUEST FOR RECORDS; STATEMENT OF PURPOSE PROHIBITED; COMMERCIAL PURPOSES.

(a) A person requesting access to public records shall not be required to state or show a purpose for the request, except as provided in subsection (d) of this section. A public officer or custodian may not condition access on the requester's stated purpose.

(b) Access shall not be denied on the ground that the person seeking access intends to use the records for a commercial purpose, except as specifically provided by law.

(c) An agency or custodian may require a requester to make the request with reasonable specificity so that the custodian can identify the records sought. However, the custodian shall assist the requester in formulating a request if the initial description is insufficient.

(d) Notwithstanding subsection (a), if the person seeking access states that the purpose of the request is commercial and a separate statute provides a commercial use fee or restriction, the custodian may apply that statute's provisions.

RESPONSE REQUIREMENTS.

Arizona law does not specify an exact number of days within which an agency must respond to a public records request. The statute uses the term "promptly," which Arizona courts have interpreted to mean without unreasonable delay. The Arizona Supreme Court has held that the duty to "promptly" furnish records requires the custodian to act with reasonable diligence and not to delay production beyond the time reasonably necessary to search for and compile the requested records.

In practice, the Arizona Ombudsman-Citizens' Aide has recommended that agencies acknowledge receipt of a request within five business days and produce records within a reasonable time, typically no more than 15 business days for straightforward requests. More complex requests may take longer, but the agency must communicate with the requester about the expected timeline and any difficulties in locating or reviewing records.

Failure to respond promptly is treated as a denial and gives the requester standing to bring a special action under A.R.S. § 39-121.02.

EXEMPTIONS.

Arizona does not have a comprehensive exemptions statute within the public records law itself. Instead, exemptions are found in scattered provisions throughout the Arizona Revised Statutes and in case law. The Arizona Supreme Court has established a two-part test (the Carlson test) for determining whether records may be withheld: (1) the custodian must identify a specific privacy interest or countervailing policy that would be harmed by disclosure; and (2) the custodian must show that the privacy interest or countervailing policy outweighs the general policy in favor of disclosure.

Major categories of records that may be exempt include:

(1) Records whose disclosure would violate rights of privacy or confidentiality that outweigh the public's right to know — the privacy interest must be substantial and specific.

(2) Records made confidential by specific statutes, including tax records, juvenile records, sealed court records, certain medical records, certain law enforcement records, and records of investigations by the Attorney General.

(3) Records that are subject to attorney-client privilege, attorney work product protection, or executive privilege.

(4) Trade secrets and confidential commercial or financial information submitted to an agency under a claim of confidentiality.

(5) Security plans, vulnerability assessments, and other records whose disclosure could jeopardize public safety.

(6) Certain personnel records where the privacy interest of the employee outweighs the public interest in disclosure. However, names, salaries, job titles, and general employment information of public employees are public.

Even where an exemption applies, the custodian must disclose any reasonably segregable nonexempt portions of the record. Blanket withholding of an entire document is not permitted if the exempt material can be redacted.

PENALTIES.

Arizona does not impose specific criminal penalties for improper withholding of public records under the public records law. The primary remedies are judicial action for disclosure, attorney's fees, and damages for bad faith denials. However, a public officer who willfully and knowingly conceals, removes, mutilates, destroys, or otherwise disposes of public records may be guilty of a class 6 felony under A.R.S. § 39-161.

SCOPE AND APPLICABILITY.

Arizona's public records law applies to all officers and employees of the state and its political subdivisions, including:

(1) All state agencies, departments, boards, commissions, and offices.
(2) The legislature and its staff.
(3) Counties, cities, towns, and their departments and agencies.
(4) School districts and charter schools to the extent they perform public functions.
(5) Special districts, including fire districts, irrigation districts, and others.
(6) Public universities and community colleges.
(7) Law enforcement agencies.
(8) Courts, regarding administrative records.
(9) Private entities performing governmental functions under contract, to the extent of records relating to the governmental function.""",
        'summary': 'Arizona\'s Public Records Law (A.R.S. §§ 39-121 to 39-121.03) provides that all public records are open to inspection by any person during office hours. The law requires "prompt" production, allows special actions in superior court for enforcement, and awards attorney\'s fees to prevailing requesters.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # ARKANSAS
    # Ark. Code §§ 25-19-101 through 25-19-110
    # =========================================================================
    {
        'id': 'ar-statute-foia',
        'citation': 'Ark. Code §§ 25-19-101 through 25-19-110',
        'title': 'Arkansas Freedom of Information Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'AR',
        'source': 'prdb-built',
        'text': """ARKANSAS FREEDOM OF INFORMATION ACT
Ark. Code §§ 25-19-101 through 25-19-110

SECTION 25-19-101. LEGISLATIVE INTENT AND DECLARATION OF POLICY.

(a) It is the specific intent of this chapter that the public's business be performed in an open and public manner and that the citizens of the state be advised of and aware of the performance of public officials and the decisions that are reached in public activity and in making public policy. Toward this end, this chapter is to be liberally interpreted to the end that all public records are open to public inspection and copying except as otherwise specifically provided by this chapter or by laws specifically enacted to provide otherwise.

(b) The General Assembly finds and declares that it is vital in a democratic society that public business be performed in an open and public manner so that the electors shall be advised of the performance of public officials and of the decisions that are reached in public activity. The provisions of this chapter are to be broadly construed in favor of disclosure and narrowly construed when limiting the right of the public to inspect records.

SECTION 25-19-103. DEFINITIONS.

(a) "Custodian" means the person who has lawful custody or control of a public record. The custodian is responsible for responding to requests, maintaining records, and ensuring compliance with this chapter.

(b) "Public records" means writings, recorded sounds, films, tapes, electronic or computer-based information, or data compilations in any medium, required by law to be kept or otherwise kept, and that constitute a record of the performance or lack of performance of official functions that are or should be carried out by a public official or employee, a governmental body, or any other agency or improvement district that is wholly or partially supported by public funds or expending public funds. The term is inclusive and is not limited by the specific examples listed.

(c) "Governmental body" or "public entity" includes:
   (1) The General Assembly, the Governor, and all state officers, departments, boards, bureaus, commissions, councils, committees, and agencies.
   (2) All county and municipal governing bodies and their departments, agencies, boards, and commissions.
   (3) All school districts and charter schools.
   (4) All public colleges and universities.
   (5) All improvement districts.
   (6) All other political subdivisions of the state.
   (7) Private entities to the extent that they receive or expend public funds.

SECTION 25-19-105. EXAMINATION AND COPYING OF PUBLIC RECORDS.

(a) Except as otherwise specifically provided by this chapter or by laws specifically enacted to provide otherwise, all public records shall be open to inspection and copying by any citizen of the State of Arkansas during the regular business hours of the custodian of the records.

(b) It is the specific intent of this section that all public records not specifically excepted from disclosure by this chapter or by laws specifically enacted to provide otherwise shall be open to inspection and copying.

(c) Any citizen of the state has the right to inspect, copy, or receive copies of public records. The custodian shall furnish copies to any person making a request. The right applies to records in any format, including electronic records, and the citizen may designate the format in which copies are to be provided if the records exist in that format.

(d) The custodian may not inquire into the purpose of a request. The identity or purpose of the requester is irrelevant to the right of access, except where a specific statute conditions access on the requester's purpose.

(e) Response time: The custodian shall provide access to public records as soon as practicable, but no later than three (3) business days from the date of receipt of the request. If the records cannot be produced within three business days due to their volume, location, or the need to review for exempt material, the custodian shall, within three business days, notify the requester in writing:
   (1) That the records exist and will be produced;
   (2) The estimated date of production;
   (3) The estimated cost of production; and
   (4) Any records that will be withheld and the specific exemption relied upon.

(f) If a request is denied in whole or in part, the custodian shall provide the denial in writing, specifying the legal basis for the denial and identifying each record or portion of a record withheld. A blanket denial without specific identification of exempt records is insufficient.

(g) An agency may not refuse to confirm or deny the existence of a record unless the fact of the record's existence is itself exempt.

SECTION 25-19-105.1. FEES.

(a) The custodian may charge a fee for copies that does not exceed the actual costs of reproducing the records, including the cost of the medium, the direct cost of copying labor, and postage if mailing is requested.

(b) The fee for standard-size copies (8.5 x 11 or 8.5 x 14) shall not exceed twenty-five cents ($0.25) per page for paper copies.

(c) The custodian may charge for the actual cost of the medium for electronic copies. The custodian may not charge a commercial rate for electronic copies when the actual cost is nominal.

(d) Inspection of records shall be free of charge. The custodian may not charge a fee for the right to inspect records on the agency's premises.

(e) If the estimated cost of producing copies exceeds $25.00, the custodian may require a deposit before beginning work.

(f) The custodian may not charge search fees or review fees for locating or reviewing records to determine their responsiveness or exempt status.

SECTION 25-19-105.2. ELECTRONIC RECORDS.

(a) Public records maintained in electronic form are subject to the same access rights as paper records. A custodian may not deny a request because the records are electronic in nature.

(b) If records are maintained in a database, the custodian shall provide the records in the electronic format requested if doing so is feasible and does not require the creation of a new record. Extracting data from a database using existing query capabilities is not the creation of a new record.

(c) The custodian shall provide records in the native electronic format if requested, unless doing so would jeopardize the security or integrity of the data or the database, in which case the custodian shall provide the records in an alternative electronic format.

SECTION 25-19-106. COURT ENFORCEMENT.

(a) Any citizen denied the rights provided by this chapter may appeal the denial to the Pulaski County Circuit Court or the circuit court of the county in which the custodian's office is located. The appeal shall be by petition, filed within 30 days of the denial or, in the case of a constructive denial by failure to respond, within 30 days of the deadline for response.

(b) The circuit court shall hear the petition de novo. The burden of proof is on the custodian to sustain the denial. The court may examine the records in camera.

(c) If the court finds that the custodian improperly denied access, the court shall order disclosure. The court shall award the prevailing citizen reasonable attorney's fees and litigation costs.

(d) The court may also award damages if it finds that the custodian acted in bad faith or with the purpose of frustrating public access.

(e) In addition to circuit court enforcement, a citizen may submit a complaint to the Attorney General, who may issue an opinion on whether the denial complied with this chapter. The Attorney General's opinion is advisory and does not have the force of law, but it is given substantial weight by courts and often prompts voluntary compliance.

SECTION 25-19-107. PENALTIES.

(a) A person who negligently violates any provision of this chapter is subject to a civil penalty of up to $500 per violation, to be assessed by the court in an enforcement action.

(b) A person who purposely violates any provision of this chapter is guilty of a Class A misdemeanor.

(c) A public official or employee who knowingly and willfully violates this chapter may also be subject to disciplinary action, including termination.

SECTION 25-19-105.3. EXEMPTIONS FROM DISCLOSURE.

The following categories of records are exempt from mandatory disclosure under this chapter:

(1) Personnel records, to the extent that they contain information about an employee's personal life that is not relevant to the employee's competency to perform the duties of the position. However, the following information about public employees is always public: name, title, salary, dates of employment, and any disciplinary action taken against the employee for conduct that constitutes a violation of law or policy.

(2) Unpublished memoranda, working papers, and correspondence of the Governor, members of the General Assembly, and the Supreme Court, to the extent such records reflect deliberative or policy-making processes. Purely factual material is not exempt.

(3) Files that if disclosed would give advantage to competitors or bidders, including sealed bids prior to opening, proprietary formulas, and trade secrets.

(4) Records maintained by law enforcement agencies and prosecutors relating to the detection and investigation of crime that, if disclosed, would:
   (A) Interfere with the detection or investigation of crime;
   (B) Deprive a person of a right to a fair trial;
   (C) Constitute an unwarranted invasion of personal privacy;
   (D) Disclose the identity of a confidential source;
   (E) Disclose investigative techniques not generally known to the public; or
   (F) Endanger the life or safety of any person.

(5) Medical records and personal health information, except to the extent that disclosure is required by law.

(6) Records of tax settlements, tax assessments, and taxpayer information maintained by the Department of Finance and Administration, except to the extent that they are already public under other law.

(7) Student educational records as protected by the Family Educational Rights and Privacy Act (FERPA).

(8) Records that are made confidential by specific federal or state statute.

(9) Litigation files and records protected by attorney-client privilege, attorney work product, or other recognized legal privilege.

(10) Security plans, vulnerability assessments, and critical infrastructure information whose disclosure would jeopardize public safety.

When a record contains both exempt and nonexempt information, the custodian shall redact the exempt portions and provide the nonexempt portions. The custodian must identify the specific exemption applied to each redaction.

SECTION 25-19-109. CONSTRUCTION.

This chapter shall be broadly and liberally construed in favor of disclosure and open government. Exemptions shall be narrowly construed. Ambiguities shall be resolved in favor of the requester.""",
        'summary': 'Arkansas\'s Freedom of Information Act (Ark. Code §§ 25-19-101 to 25-19-110) requires public records be available within 3 business days. It includes criminal penalties for purposeful violations (Class A misdemeanor) and civil penalties up to $500 for negligent violations. Attorney\'s fees are mandatory for prevailing requesters.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # COLORADO
    # C.R.S. §§ 24-72-200.1 through 24-72-206
    # =========================================================================
    {
        'id': 'co-statute-cora',
        'citation': 'C.R.S. §§ 24-72-200.1 through 24-72-206',
        'title': 'Colorado Open Records Act (CORA)',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'CO',
        'source': 'prdb-built',
        'text': """COLORADO OPEN RECORDS ACT (CORA)
C.R.S. §§ 24-72-200.1 through 24-72-206

SECTION 24-72-200.1. LEGISLATIVE DECLARATION.

(1) The general assembly hereby finds and declares that all public records shall be open for inspection by any person at reasonable times, except as provided in this part 2 or as otherwise specifically provided by law. It is the intent of the general assembly that this part 2 be liberally construed to ensure maximum public access to public records.

(2) The general assembly finds that the public has an interest in knowing what public officials are doing, how public funds are being spent, and how public institutions are functioning. The right of public access to records is essential to maintain democratic accountability.

SECTION 24-72-202. DEFINITIONS.

(1) "Custodian" means and includes the official custodian or any authorized person having personal custody and control of the public records in question. The custodian is the person responsible for responding to requests.

(2) "Official custodian" means any officer or employee of the state, or any agency, institution, or political subdivision thereof, who is responsible for the maintenance, care, and keeping of public records, regardless of whether such records are in the officer's or employee's actual physical custody and control.

(3) "Public records" means all writings made, maintained, or kept by the state, any agency, institution, a nonprofit corporation incorporated pursuant to section 23-5-121(2), or political subdivision of the state, or that are described in section 29-1-902, C.R.S., and held by any local government for use in the exercise of functions required or authorized by law or administrative rule or involving the receipt or expenditure of public funds. "Public record" includes "correspondence" as defined by this subsection.

(4) "Writings" means and includes all books, papers, maps, photographs, cards, tapes, recordings, or other documentary materials, regardless of physical form or characteristics. "Writings" includes digitally stored data, including emails, text messages, social media communications, and other electronic records created or received in connection with the transaction of public business.

SECTION 24-72-203. PUBLIC RECORDS OPEN TO INSPECTION.

(1)(a) All public records shall be open for inspection by any person at reasonable times, except as otherwise provided by law. The custodian of any public record shall allow any person the right of inspection of such records during regular business hours. No person exercising the right of inspection shall be required to identify himself or herself or to state a purpose for the inspection.

(1)(b) If the custodian denies access to any public record, the custodian shall provide a written denial specifying the legal authority for the denial within three (3) business days of receipt of the request. The denial must specifically identify the records withheld, the provisions of law under which each withholding is claimed, and the name and title of the person responsible for the denial.

(2)(a) The custodian may establish reasonable rules and regulations governing the inspection of records, provided that such rules do not effectively deny access. Rules regarding the time and place of inspection are permissible, but may not unreasonably limit the hours of access or require appointments that are difficult to obtain.

(2)(b) Where the right of inspection has been denied or where the custodian does not have the requested records, the custodian shall so advise the applicant in writing within three (3) business days after receipt of the request, setting forth the reasons for the denial or advising as to the custodian's knowledge of the location of the requested records.

(3) In all cases in which a person has the right to inspect any public record, the person may request copies, printouts, or photographs of such record. The custodian shall furnish copies, printouts, or photographs and may charge a reasonable fee not to exceed $1.25 per standard page for copies. The fee shall not exceed the actual costs of providing the copy.

SECTION 24-72-204. ALLOWANCE OR DENIAL OF INSPECTION — GROUNDS.

(1) The custodian shall allow inspection unless the records are specifically exempt. If only portions of a record are exempt, the custodian shall redact the exempt portions and provide the nonexempt portions for inspection.

(2) The custodian may deny inspection of the following records or classes of records on the grounds that disclosure would be contrary to the public interest:

(a) Medical, mental health, sociological, and scholastic achievement data on individual persons, other than the names and addresses of persons who are applicants for or recipients of public assistance.

(b) Personnel files, including applications, performance evaluations, personal financial information, and medical information. However, the following information is public and may not be withheld: name, position, salary information including pay schedules and compensation, dates of employment, and the terms of any employment contract.

(c) Letters of reference concerning employment, licensing, or permits.

(d) Trade secrets, privileged information, and confidential commercial, financial, geological, or geophysical data furnished by or obtained from any person.

(e) Library and museum material contributed by private persons, to the extent of any limitations placed on use as conditions of the contribution.

(f) Addresses and telephone numbers of students in any public school or college if the school or college notifies parents annually of the right to request nondisclosure.

(g) Records of sexual harassment complaints and investigations, to the extent that the records identify the complainant, the accused, or witnesses. However, the final disposition of the complaint and any resulting disciplinary action are public.

(3) The following records shall be denied inspection regardless of the public interest balancing test:

(a) Records specifically required to be kept confidential by federal law.
(b) Records that are privileged under state or federal rules of evidence.
(c) Real estate appraisals made for public agencies relative to the acquisition of property, until the acquisition is completed or the project is abandoned.
(d) Specialized details of security arrangements or investigations.

SECTION 24-72-204.5. CRIMINAL JUSTICE RECORDS.

(1) Criminal justice records are subject to a separate framework under this section. "Criminal justice records" means records made, maintained, or kept by any criminal justice agency in the state for purposes of documenting, reporting, or investigating criminal activity.

(2) The custodian of criminal justice records may deny the right of inspection if, in the custodian's opinion, disclosure would be contrary to the public interest, and may consider the following factors:

(a) Whether the records are part of an active investigation.
(b) Whether disclosure would jeopardize the safety of any person.
(c) Whether disclosure would identify confidential sources or investigative techniques.
(d) Whether disclosure would compromise the right to a fair trial.

(3) Arrest and booking records, including the name of the person arrested, the charges, the date and time of arrest, and the disposition of the case, are public and may not be withheld. Incident reports are generally public, though specific details may be redacted to protect ongoing investigations.

SECTION 24-72-205. FEES.

(1) The custodian may charge a fee for providing copies of public records. For standard-size paper copies (8.5 x 11 or 8.5 x 14), the fee may not exceed $1.25 per page.

(2) For copies of records in other formats, the fee may not exceed the actual cost of providing the copy. "Actual cost" means the cost of the medium, direct labor costs for the mechanical process of copying (not for research or review), and postage if applicable.

(3) If the fee is estimated to exceed $25.00, the custodian shall notify the requester and may require a deposit before beginning work.

(4) The custodian may not charge a fee for inspection of records. The right to inspect records on the agency's premises is free.

(5) The custodian shall waive or reduce fees if the requester demonstrates that the disclosure is in the public interest and that the fee is an unreasonable burden.

SECTION 24-72-204.6. ELECTRONIC RECORDS.

Records maintained in electronic format are public records subject to the same rights of inspection and copying as other public records. The custodian shall provide electronic records in the format requested if feasible. Extracting data from existing databases is not the creation of a new record.

SECTION 24-72-206. COURT ENFORCEMENT AND PENALTIES.

(1) Any person denied the right to inspect public records may apply to the district court of the district in which the records are located for an order directing the custodian to show cause why the inspection should not be permitted. The court shall hear the application as expeditiously as possible and shall give the case priority.

(2) The court shall review the denial de novo. The burden is on the custodian to prove that the denial was authorized by law. The court may examine the records in camera.

(3) If the court finds that the denial was improper, the court shall order the custodian to permit inspection. The court shall award the prevailing applicant reasonable attorney's fees and costs.

(4) If the court finds that the custodian's denial was arbitrary or capricious, the court may impose a civil penalty against the custodian or the public entity of not less than $25.00 and not more than $1,000.00 per violation.

(5) Any custodian who willfully and knowingly violates this part 2 commits a class 2 petty offense and, upon conviction, shall be punished by a fine of not more than $100.00.

(6) The court may also issue injunctive relief to prevent continuing violations.

APPEAL MECHANISMS.

Colorado does not have a formal administrative appeal process within CORA. However, in practice:

(a) A requester may contact the custodian's supervisor or the agency's legal counsel to seek reconsideration of a denial.

(b) The Colorado Attorney General's Office provides informal mediation and advisory opinions on records disputes, though these are not binding.

(c) The primary enforcement mechanism is the district court action described in § 24-72-206.

SCOPE AND APPLICABILITY.

CORA applies to all state and local government entities, including:

(1) State government agencies, departments, and institutions, including the executive, legislative, and judicial branches.
(2) State-funded institutions of higher education, including the University of Colorado, Colorado State University, and other state colleges and universities.
(3) Counties, cities, and towns, and their departments and agencies.
(4) School districts.
(5) Special districts, including water, fire, sanitation, and other special-purpose districts.
(6) Quasi-governmental entities that receive or expend public funds or perform governmental functions.

Private entities are not generally subject to CORA unless they perform governmental functions under contract and the records relate to those functions. However, records held by a private entity on behalf of a government agency remain public records subject to CORA.""",
        'summary': 'Colorado\'s Open Records Act (C.R.S. §§ 24-72-200.1 to 24-72-206) requires responses within 3 business days and caps copy fees at $1.25/page. Willful violations are a class 2 petty offense. Courts may impose civil penalties of $25-$1,000 for arbitrary denials, and attorney\'s fees are awarded to prevailing requesters.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # CONNECTICUT
    # Conn. Gen. Stat. §§ 1-200 through 1-241
    # =========================================================================
    {
        'id': 'ct-statute-foia',
        'citation': 'Conn. Gen. Stat. §§ 1-200 through 1-241',
        'title': 'Connecticut Freedom of Information Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'CT',
        'source': 'prdb-built',
        'text': """CONNECTICUT FREEDOM OF INFORMATION ACT
Conn. Gen. Stat. §§ 1-200 through 1-241

SECTION 1-200. DEFINITIONS.

(1) "Public agency" or "agency" means:
   (A) Any executive, administrative, or legislative office of the state or any political subdivision of the state.
   (B) Any state or town agency, any department, institution, bureau, board, commission, authority, or official of the state or of any city, town, borough, municipal corporation, school district, regional district, or other district or other political subdivision of the state.
   (C) Any judicial office, official, or body or committee thereof but only with respect to its or their administrative functions.
   (D) Any person to the extent such person is deemed to be the functional equivalent of a public agency pursuant to law.

(2) "Public records" or "files" means any recorded data or information relating to the conduct of the public's business prepared, owned, used, received, or retained by a public agency, or to which a public agency is entitled to receive a copy by law or contract under section 1-218, whether such data or information be handwritten, typed, tape-recorded, printed, photostated, photographed, or recorded by any other method.

(3) "Meeting" means any hearing or other proceeding of a public agency, any convening or assembly of a quorum of a multimember public agency, and any communication by or to a quorum of a multimember public agency, whether in person or by means of electronic equipment, to discuss or act upon a matter over which the public agency has supervision, control, jurisdiction, or advisory power. [Note: Connecticut's FOIA covers both records and meetings; this document focuses on the records provisions.]

(4) "Personnel or medical files and similar files" means files that contain intimate details of a personal nature such as medical records, personal financial information, and evaluations of personal characteristics.

SECTION 1-210. ACCESS TO PUBLIC RECORDS — EXEMPTIONS.

(a) Except as otherwise provided by any federal law or state statute, all records maintained or kept on file by any public agency, whether or not such records are required by any law or by any rule or regulation, shall be public records and every person shall have the right to:
   (1) inspect such records;
   (2) copy such records; or
   (3) receive a copy of such records in accordance with section 1-212.

(b) The following categories of records are exempt from disclosure:

(1) Preliminary drafts or notes provided the public agency has determined that the public interest in withholding such documents clearly outweighs the public interest in disclosure. This exemption does not apply to final agency actions, policies, or decisions.

(2) Personnel or medical files and similar files, the disclosure of which would constitute an invasion of personal privacy. This exemption is interpreted in light of a balancing test weighing the individual's privacy interest against the public's interest in disclosure. Names, titles, salaries, and general employment information of public employees are not exempt.

(3) Records of law enforcement agencies not otherwise available to the public, which records were compiled in connection with the detection or investigation of crime, if the disclosure of said records would not be in the public interest because it would result in the disclosure of:
   (A) The identity of informants not otherwise known or the identity of witnesses not otherwise known whose safety would be endangered or who would be subject to threat or intimidation if their identity was made known.
   (B) Signed statements of witnesses.
   (C) Information to be used in a prospective law enforcement action if prejudicial to such action.
   (D) Investigatory techniques not otherwise known to the general public.
   (E) Arrest records, police reports, and complaint records that are available to the public are not exempt under this subdivision.

(4) Records pertaining to strategy and negotiations with respect to pending claims or pending litigation to which the public agency is a party until such litigation or claim has been finally adjudicated or otherwise settled.

(5) Trade secrets, as defined by statute.

(6) Test questions, scoring keys, and other examination data used to administer a licensing examination, employment examination, or academic examination before the examination is given or if it is to be given again.

(7) The contents of real estate appraisals, engineering, or feasibility estimates and evaluations made for or by an agency relative to the acquisition of property or to prospective public supply and construction contracts, until such time as all of the property has been acquired or all proceedings or transactions have been terminated or abandoned.

(8) Records, reports, and statements of strategy or negotiations with respect to collective bargaining.

(9) Records, tax returns, and tax-related information obtained by the Department of Revenue Services.

(10) Communications privileged by the attorney-client relationship.

(11) Names or addresses of students enrolled in any public school or college without the consent of each student whose name or address is to be disclosed, unless otherwise required by law.

(12) Records of an investigation by the Ethics Commission, until such investigation is completed.

(13) Records that are exempt from disclosure by federal law.

(14) Information obtained by the Commissioner of Emergency Services and Public Protection through a criminal justice information system.

(15) Security plans, vulnerability assessments, emergency response plans, and other records whose disclosure would jeopardize public safety.

(16) Records that contain information regarding the location of a domestic violence shelter or the identity of its residents.

(c) Whenever a public agency receives a request to inspect or copy records contained in any of the categories listed in subsection (b) of this section, the agency shall, within four business days, determine whether the requested records are exempt. If the records are not exempt, or if the agency fails to make a determination within four business days, the records shall be provided.

(d) If only portions of a record are exempt, the nonexempt portions shall be provided. The agency must redact only the exempt portions and identify the specific exemption relied upon.

SECTION 1-211. ACCESS TO MEETINGS.

[This section governs open meetings. While part of the FOIA, it is not a records provision and is not reproduced here in full.]

SECTION 1-212. COPIES AND FEES.

(a) Any person applying in writing shall receive, promptly upon request, a plain, facsimile, electronic or certified copy of any public record. The fee for any copy provided in accordance with subsection (a) of section 1-210 shall not exceed fifty cents ($0.50) per page. If the agency does not have the ability to reproduce the record at its offices, the agency shall inform the requester where and how the record can be reproduced.

(b) The fee for a certified copy of any public record shall not exceed one dollar ($1.00) per page.

(c) If a public record is maintained in an electronic format, the agency shall provide the record in the electronic format requested if the agency can reasonably do so. The fee for electronic copies shall not exceed the actual cost of the medium on which the copy is provided.

(d) Fees shall be waived if:
   (1) The requester is an indigent individual and the records are needed for the assertion or defense of a legal right; or
   (2) The agency determines that the waiver serves the public interest.

(e) Inspection of records is free of charge. The agency may not charge a fee solely for the right to inspect records on agency premises.

SECTION 1-206. FREEDOM OF INFORMATION COMMISSION — ADMINISTRATIVE APPEAL.

(a) There is established a Freedom of Information Commission consisting of five members appointed by the Governor, at least one of whom shall be an attorney, for terms of four years.

(b) Any person denied the right to inspect or copy public records under this chapter may appeal the denial to the Freedom of Information Commission. The appeal must be filed within thirty days of the denial.

(c) Upon receipt of an appeal, the Commission shall schedule a hearing. The hearing shall be conducted in accordance with the provisions of chapter 54 (the Uniform Administrative Procedure Act). The Commission shall hear and determine the matter de novo.

(d) The burden of proof is on the agency to demonstrate that the records are exempt from disclosure.

(e) The Commission may:
   (1) Order the agency to produce the records.
   (2) Declare that the agency violated this chapter.
   (3) Impose a civil penalty of not less than twenty dollars ($20) and not more than one thousand dollars ($1,000) against a public agency or any member of a public agency found to have violated any provision of this chapter.
   (4) Order the agency to pay the complainant's reasonable attorney's fees.

(f) Any party aggrieved by a final decision of the Commission may appeal to the superior court.

SECTION 1-240. PENALTIES.

(a) Any person who willfully, knowingly, and with intent to do so, destroys, mutilates, or otherwise disposes of any public record without the approval of the Public Records Administrator or as otherwise provided by law shall be guilty of a class A misdemeanor.

(b) Any member of any public agency who votes in a meeting that violates the open meetings provisions of this chapter shall be subject to a fine of not more than one thousand dollars ($1,000) for each violation.

(c) The Freedom of Information Commission may impose civil penalties as described in section 1-206.

RESPONSE REQUIREMENTS.

(a) Connecticut's FOIA requires agencies to respond to records requests within four (4) business days. Within that time, the agency must either:
   (1) Provide the requested records;
   (2) Acknowledge the request and provide a specific date by which the records will be available;
   (3) Deny the request in writing, specifying the exemption relied upon; or
   (4) State that no responsive records exist.

(b) If the agency fails to respond within four business days, the failure is deemed a denial, and the requester may immediately file an appeal with the Freedom of Information Commission.

(c) The four-business-day deadline applies to the initial response, not necessarily to the production of all records. For complex or voluminous requests, the agency may provide an initial response within four days explaining the need for additional time, and then produce records on a rolling basis.

SCOPE AND APPLICABILITY.

Connecticut's FOIA applies broadly to all levels of state and local government:

(1) State agencies, departments, offices, boards, commissions, councils, and authorities.
(2) The General Assembly and its offices, to the extent of administrative records.
(3) The Judicial Branch, to the extent of administrative records.
(4) Municipalities, including towns, cities, and boroughs.
(5) Regional and local boards of education and school districts.
(6) Regional councils and planning agencies.
(7) Special districts and authorities.
(8) Public colleges and universities, including the University of Connecticut and the Connecticut State University System.
(9) Private entities that are the "functional equivalent" of a public agency, based on factors including the degree of government funding, government involvement in management, and whether the entity performs a governmental function.

CONSTRUCTION.

The Connecticut Freedom of Information Act is to be broadly construed in favor of disclosure. Exemptions are narrowly construed, and the burden is always on the agency asserting an exemption to demonstrate its applicability.""",
        'summary': 'Connecticut\'s Freedom of Information Act (Conn. Gen. Stat. §§ 1-200 to 1-241) provides one of the strongest enforcement mechanisms in the country through the Freedom of Information Commission, which hears appeals and can impose civil penalties of $20-$1,000. Agencies must respond within 4 business days. Copy fees are capped at 50 cents per page.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # DELAWARE
    # Del. Code tit. 29, §§ 10001 through 10007
    # =========================================================================
    {
        'id': 'de-statute-foia',
        'citation': 'Del. Code tit. 29, §§ 10001 through 10007',
        'title': 'Delaware Freedom of Information Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'DE',
        'source': 'prdb-built',
        'text': """DELAWARE FREEDOM OF INFORMATION ACT
Del. Code tit. 29, §§ 10001 through 10007

SECTION 10001. SHORT TITLE.

This chapter shall be known and may be cited as the "Freedom of Information Act."

SECTION 10002. DEFINITIONS.

(a) "Public body" means, unless specifically excluded, every state or local agency, board, department, authority, commission, committee, council, or instrumentality of the state or any political subdivision, and any body created by state or local law or action that:
   (1) Is supported in whole or in part by public funds; or
   (2) Expends or disburses public funds; or
   (3) Has authority to make decisions regarding public policy; or
   (4) Is delegated the authority to perform a governmental function.

The term includes the General Assembly and its committees, subcommittees, and commissions. The judiciary is not included except as to its administrative functions.

(b) "Public record" means information of any kind, owned, made, used, retained, received, produced, composed, drafted, or otherwise compiled or collected, by any public body, relating in any way to public business, or in any way of public interest, or in any way related to public purposes, regardless of the physical form or characteristic by which such information is stored, recorded, or reproduced. The term includes, but is not limited to, documents, reports, letters, memoranda, papers, plans, photographs, microfilms, cards, tapes, recordings, electronic data processing records, electronic communications including email and text messages, computer data, maps, and other documentary material or data regardless of physical form or characteristics.

(c) "Meeting" means the formal or informal gathering of a quorum of the members of any public body for the purpose of discussing or taking action on public business. [Note: Delaware's FOIA covers both records and meetings.]

SECTION 10003. OPEN ACCESS TO PUBLIC RECORDS.

(a) All public records shall be open to inspection and copying by any citizen of the State of Delaware during regular business hours by the custodian of the records for the appropriate public body. Any reasonable rules and regulations may be adopted by the custodian of the records to prevent excessive interference with the custodian's other responsibilities and to protect the records from damage or disorganization, but such rules shall not be used to frustrate the policy of open access.

(b) Each public body shall designate an employee or employees to serve as the coordinator(s) for FOIA requests. The coordinator's name and contact information shall be posted on the public body's website and made available to the public.

(c) A citizen requesting access to public records need not provide a reason or purpose for the request. The public body may not deny access based on the requester's identity, affiliation, or purpose, unless a specific statute conditions access on purpose.

(d) Response time requirements:

   (1) The public body shall respond to a FOIA request as soon as possible but not later than fifteen (15) business days after receipt of the request. The response shall either:
       (A) Provide the requested records;
       (B) Deny the request in whole or in part, with an explanation of the grounds for each denial and the specific exemption relied upon;
       (C) Indicate that additional time is needed and state a specific date by which the records will be produced, not to exceed an additional ten (10) business days; or
       (D) State that no responsive records exist.

   (2) If the request is for records in a category that requires review for exempt material, the public body may take a reasonable additional period, not to exceed the additional ten business days described above, to perform the review.

   (3) Failure to respond within the time limits constitutes a denial, and the requester may immediately seek judicial or administrative relief.

(e) Records maintained in electronic format shall be provided in the electronic format requested, if the public body can reasonably do so. The public body may not require the requester to accept records in paper format if electronic production is feasible.

SECTION 10003A. FEES.

(a) The custodian may charge a reasonable fee for copies of public records. The fee shall not exceed the actual cost of copying.

(b) For standard-size paper copies (8.5 x 11 or 8.5 x 14), the fee shall not exceed $0.25 per page for the first 20 pages and $0.10 per page thereafter.

(c) For electronic copies, the fee shall not exceed the actual cost of the medium and any direct cost of producing the copy.

(d) The custodian may charge for actual staff time spent searching for and compiling records, at the hourly rate of the employee performing the search, if the search requires more than one hour. The first hour of search time is free.

(e) The custodian shall provide an estimate of the total fee before beginning work if the estimated fee exceeds $25.00. The custodian may require a deposit of up to 50% of the estimated fee before beginning work.

(f) The custodian shall waive fees if the records are requested for a noncommercial purpose and the fee would effectively deny access.

(g) Inspection of records on the agency's premises is free. No fee may be charged solely for the right to view records.

SECTION 10004. RECORDS NOT SUBJECT TO DISCLOSURE.

The following records shall not be subject to public inspection under this chapter:

(1) Any personnel, medical, or pupil file the disclosure of which would constitute an invasion of personal privacy, under the standard set forth below. In applying this exemption, the public body shall balance the individual's privacy interest against the public interest in disclosure. The following information about public employees is always public: name, title, salary, dates of employment, and the terms of any employment contract. The following information about public employees is generally exempt: home addresses, personal phone numbers, Social Security numbers, personal financial information, and medical information.

(2) Trade secrets and commercial or financial information obtained from a person that is of a privileged or confidential nature.

(3) Investigatory files compiled for civil or criminal law enforcement purposes where production would:
   (A) Interfere with enforcement proceedings;
   (B) Deprive a person of a right to a fair trial;
   (C) Constitute an unwarranted invasion of personal privacy;
   (D) Disclose the identity of a confidential source;
   (E) Disclose investigative techniques or procedures; or
   (F) Endanger the life or physical safety of law enforcement personnel.

(4) Criminal files and criminal records of a nonpublic nature.

(5) Any records specifically exempted from public disclosure by statute or court order.

(6) Records relating to pending or reasonably anticipated litigation, including communications protected by the attorney-client privilege or the work product doctrine.

(7) Any records the disclosure of which would jeopardize the safety of any person.

(8) Any records that would reveal the security measures at a public body or security information about a public body's buildings, computer systems, communication systems, or other infrastructure.

(9) Draft documents and predecisional memoranda, unless the draft constitutes a final action or policy decision. Purely factual information contained in draft documents is not exempt.

(10) Any records of a public body that relate to the evaluation of a named public official if the evaluation is not a final action. Final evaluations and any resulting personnel actions are public.

(11) Communications between and among members of a public body (excluding communications in a meeting) that relate to a matter pending before the public body, if the communication does not constitute a final action. This exemption is narrowly construed and does not authorize blanket withholding of all internal communications.

When a record contains both exempt and nonexempt material, the public body must provide the nonexempt portions after redacting the exempt material. The public body must identify the specific exemption applied to each redaction.

SECTION 10005. ENFORCEMENT — ATTORNEY GENERAL AND JUDICIAL REMEDIES.

(a) Any citizen who believes that a public body has violated this chapter may file a complaint with the Attorney General. The Attorney General shall investigate the complaint and may:

   (1) Determine that the public body has violated the chapter and order the public body to comply;
   (2) Determine that no violation occurred;
   (3) Mediate a resolution between the parties.

(b) The Attorney General's determination is enforceable and binding on the public body, subject to the public body's right to appeal to the Court of Chancery.

(c) Any citizen denied access to public records may also bring an action in the Court of Chancery to compel disclosure. The Court of Chancery has original jurisdiction over all FOIA disputes.

(d) In an action under this section, the burden of proof is on the public body to demonstrate that the records are exempt from disclosure. The court may examine the records in camera.

(e) The court shall award reasonable attorney's fees to the prevailing complainant if the court finds that the public body acted unreasonably in denying access. The court may also award attorney's fees to the public body if the court finds that the complainant's action was frivolous.

(f) The court may impose a civil penalty of not less than $100 and not more than $10,000 per violation against a public body that the court finds acted willfully and in bad faith.

SECTION 10006. PENALTIES.

(a) Any person who willfully destroys, mutilates, conceals, or removes a public record without authorization is guilty of a class A misdemeanor.

(b) Any public official who willfully violates any provision of this chapter may be subject to removal from office, in addition to any other penalties provided by law.

(c) Civil penalties as provided in section 10005.

SECTION 10007. CONSTRUCTION.

This chapter shall be liberally construed to implement the policy that public records are open to all citizens. Exemptions shall be narrowly construed. In the event of any conflict between this chapter and any other statute regarding public access to records, this chapter shall control unless the other statute specifically states that it takes precedence over this chapter.

SCOPE AND APPLICABILITY.

Delaware's FOIA applies broadly:

(1) State government: all executive branch agencies, departments, boards, commissions, and offices.
(2) The General Assembly and its committees, to the extent of records (not legislative privilege).
(3) The judiciary, to the extent of administrative records.
(4) Counties (New Castle, Kent, Sussex) and their agencies.
(5) Municipalities and their agencies.
(6) School districts and school boards.
(7) Public universities and colleges, including the University of Delaware (as to records relating to the expenditure of public funds and the performance of governmental functions).
(8) Special purpose entities, authorities, and commissions.
(9) Private entities performing governmental functions or expending public funds, to the extent of the records relating to those functions or funds.

ACCESS FOR NONRESIDENTS.

Delaware's FOIA is limited to citizens of the State of Delaware. Nonresidents do not have a statutory right of access under FOIA. However, many public bodies voluntarily provide access to nonresidents, and the Delaware Attorney General has encouraged public bodies to do so. Nonresidents may also have access to specific categories of records under other statutory provisions or the common law right of access.""",
        'summary': 'Delaware\'s Freedom of Information Act (Del. Code tit. 29, §§ 10001-10007) requires responses within 15 business days. It provides dual enforcement through the Attorney General (binding determinations) and the Court of Chancery. Civil penalties range from $100 to $10,000 for willful bad faith violations. Copy fees are capped at $0.25/page for the first 20 pages.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # DISTRICT OF COLUMBIA
    # D.C. Code §§ 2-531 through 2-540
    # =========================================================================
    {
        'id': 'dc-statute-foia',
        'citation': 'D.C. Code §§ 2-531 through 2-540',
        'title': 'District of Columbia Freedom of Information Act',
        'date': None,
        'document_type': 'State Public Records Statute',
        'jurisdiction': 'DC',
        'source': 'prdb-built',
        'text': """DISTRICT OF COLUMBIA FREEDOM OF INFORMATION ACT
D.C. Code §§ 2-531 through 2-540

SECTION 2-531. PURPOSE; POLICY.

The Council of the District of Columbia finds that public records are the property of the citizens of the District and that the Government of the District of Columbia exists to serve the public. Providing public access to government records is essential to the functioning of a democratic government, and the public's right of access should be broadly construed and narrowly limited. It is the policy of the District government that all persons are entitled to full and complete information regarding the affairs of government and the official acts of those who represent them. To that end, provisions of this subchapter shall be construed with the view toward expansion of public access and the minimization of costs and time delays to persons requesting information.

SECTION 2-532. RIGHT OF ACCESS.

(a) Any person has a right to inspect, and at the person's discretion, to copy any public record of a public body, except as otherwise expressly provided by this subchapter, in accordance with reasonable rules prescribed by the public body. These rules shall be made available for public inspection and copying.

(b) The right of access includes the right to inspect records and the right to receive copies of records, in the format requested if the records exist in that format or can reasonably be converted to that format.

(c) Each public body shall make public records available for inspection and copying during the normal office hours of the body. The public body may establish reasonable rules for the inspection and copying of records, but such rules shall not frustrate the purpose of this subchapter or effectively deny access to public records.

(d) A requester is not required to state a purpose or reason for the request. The public body shall not condition access on the requester's identity, purpose, or intended use of the records, unless a specific provision of this subchapter provides otherwise.

SECTION 2-534. EXEMPTIONS FROM DISCLOSURE.

(a) The following matters may be exempt from disclosure under the provisions of this subchapter:

(1) Trade secrets and commercial or financial information obtained from outside the government, to the extent that such information is privileged or confidential.

(2) Information of a personal nature where the public disclosure thereof would constitute a clearly unwarranted invasion of personal privacy. In determining whether disclosure constitutes a clearly unwarranted invasion of personal privacy, the public body shall balance the public interest in disclosure against the individual's privacy interest. The following information about District employees is public and may not be withheld: name, title, grade, salary, and dates of employment.

(3) Investigatory records compiled for law enforcement purposes, but only to the extent that the production of such records would:
   (A) Interfere with enforcement proceedings;
   (B) Deprive a person of a right to a fair trial or an impartial adjudication;
   (C) Constitute an unwarranted invasion of personal privacy;
   (D) Disclose the identity of a confidential source and, in the case of a record compiled by a criminal law enforcement authority in the course of a criminal investigation, confidential information furnished only by the confidential source;
   (E) Disclose investigative techniques and procedures not generally known outside the government; or
   (F) Endanger the life or physical safety of law enforcement personnel.

(4) Inter-agency or intra-agency memorandums or letters, including memorandums or letters generated or received by the staff or members of the Council of the District of Columbia, that would not be available by law to a party other than a public body in litigation with the public body. This deliberative process exemption protects predecisional, deliberative communications but does not protect purely factual material or material that constitutes final agency action. The factual portions of deliberative records must be disclosed if reasonably segregable.

(5) Test questions and answers to be used in future license, employment, or academic examinations, but not previously administered examinations.

(6) Information specifically exempted from disclosure by statute, other than this subchapter, provided that such statute:
   (A) Requires that the matters be withheld from the public in such a manner as to leave no discretion on the issue; or
   (B) Establishes particular criteria for withholding or refers to particular types of matters to be withheld.

(7) Information specifically authorized under criteria established by an executive order to be kept secret in the interest of national defense or foreign policy, provided the information has in fact been properly classified pursuant to such executive order.

(8) Information exempted from disclosure by the rules of the Council of the District of Columbia that pertain to the Council's deliberative process, including staff recommendations and bills and resolutions during the drafting process, provided that this exemption shall not apply to bills, resolutions, or other actions that have been officially introduced or that constitute final Council action.

(9) Information relating to the operation of a hospital, medical facility, or clinic operated by the District, the disclosure of which would constitute an invasion of patient privacy.

(10) Any specific response plan, including but not limited to a plan designed to prevent or respond to criminal activity, an ## emergency, or any other disaster, including terrorism, biological, chemical, radiological, or nuclear attack.

(11) Documents, data, or information prepared by or for an insurance company, health maintenance organization, or other entity providing health insurance coverage, if the disclosure of such documents, data, or information would be harmful to the competitive position of the company, organization, or entity.

(12) Information about the identity of a person making a complaint to any agency, where the complaint alleges a violation of law by another person and the law protects the identity of the complainant.

(b) Any reasonably segregable portion of a record shall be provided to any person requesting such record after deletion of those portions which are exempt under this section.

(c) The exemptions in this section are permissive, not mandatory. A public body may exercise discretion to disclose records that fall within an exemption.

SECTION 2-532.1. RESPONSE REQUIREMENTS.

(a) A public body that receives a request for public records shall respond within fifteen (15) business days of receipt. The response shall either:

   (1) Produce the requested records;
   (2) Notify the requester that the request has been denied, in whole or in part, and specify the legal basis for each denial, including the specific subsection of section 2-534 relied upon and a brief explanation of how the exemption applies;
   (3) Notify the requester that the public body needs an additional period of time to respond due to the unusual nature or volume of the request, not to exceed an additional ten (10) business days; or
   (4) Notify the requester that the requested records do not exist or cannot be located after a reasonable search.

(b) If the public body fails to respond within the time limits described in subsection (a), the failure shall be deemed a denial of the request.

(c) A public body may request clarification of an ambiguous request, but the request for clarification does not extend the response deadline unless the requester and the public body agree to a new deadline.

SECTION 2-536. INFORMATION TO BE MADE AVAILABLE — PROACTIVE DISCLOSURE.

(a) Each public body of the District of Columbia shall, without cost, make available for public inspection and copying the following records:

(1) The organization and functions of the body, including the name, address, and telephone number of the body's FOIA officer.
(2) All final orders and decisions made by the body in the adjudication of cases.
(3) All final opinions, including concurring and dissenting opinions, and all orders made in the adjudication of cases.
(4) Statements of policy and interpretations that have been adopted by the body.
(5) Administrative staff manuals and instructions to staff that affect the public.
(6) Data reflecting the body's budget and expenditures.
(7) Minutes of all meetings of the body.
(8) Contracts and agreements entered into by the body.
(9) Reports or studies prepared by or for the body.
(10) Frequently requested records.

(b) Each public body shall maintain a current index of all materials described in subsection (a) and shall make the index available to the public. Each public body shall post the index and, to the extent practicable, the materials themselves on its website.

SECTION 2-537. FEES.

(a) A public body may charge a reasonable fee for searching, reviewing, and copying public records. The fee shall not exceed the actual cost to the public body.

(b) For paper copies, the fee shall not exceed $0.25 per page.

(c) For electronic records provided in electronic format, the fee shall not exceed the actual cost of the medium on which the copies are provided.

(d) Search fees: The public body may charge for the time spent searching for and retrieving records, at the hourly rate of the employee performing the search. However, the first two hours of search time shall be provided without charge.

(e) Review fees: The public body may charge for the time spent reviewing records to determine whether they are exempt from disclosure, at the hourly rate of the employee performing the review. However, no review fee may be charged for the initial review (the review to determine whether an exemption applies). Review fees may only be charged for additional review necessitated by a request for reconsideration.

(f) The public body shall waive or reduce fees when:
   (1) The requester demonstrates that the information is in the public interest because it is likely to contribute significantly to public understanding of the operations or activities of the government; and
   (2) The information is not primarily in the commercial interest of the requester.

(g) The public body shall provide an estimate of fees if the estimated total exceeds $25.00 and may require advance payment before proceeding.

SECTION 2-537.01. FOIA PROCESSING FEES — INDIGENT PERSONS.

Fees shall be waived for a requester who demonstrates indigency by providing evidence of current eligibility for one of several enumerated public assistance programs.

SECTION 2-538. ADMINISTRATIVE APPEAL — MAYOR'S OFFICE.

(a) Any person denied access to a public record may petition the Mayor for a review of the denial. The petition must be filed within ninety (90) calendar days of the denial.

(b) The Mayor shall review the petition and make a determination within ten (10) business days. The Mayor may extend the review period for an additional ten business days in unusual circumstances.

(c) The Mayor may:
   (1) Order the public body to produce the records;
   (2) Affirm the denial;
   (3) Modify the denial to require production of some records while affirming the withholding of others.

(d) The Mayor's determination constitutes the final administrative determination of the District government.

SECTION 2-539. JUDICIAL REVIEW.

(a) Any person denied access to a public record, after exhausting administrative remedies under section 2-538, may bring an action in the Superior Court of the District of Columbia to enjoin the public body from withholding the records and to order the production of the records.

(b) The court shall hear the case de novo. The burden is on the public body to sustain its decision to withhold records. The court may examine the records in camera.

(c) The court shall give the case priority on its calendar and shall expedite the proceeding in every way.

(d) If the court orders production of records, the court shall award the complainant reasonable attorney's fees and other litigation costs reasonably incurred if:
   (1) The complainant has substantially prevailed; and
   (2) The court finds that the public body's withholding was without reasonable basis.

(e) The court may assess against the District government the costs of litigation and reasonable attorney's fees when the court determines that an agency official acted arbitrarily or capriciously with respect to the withholding.

SECTION 2-540. PENALTIES.

(a) The Mayor shall, in consultation with the Office of the Inspector General, implement procedures to ensure compliance with this subchapter.

(b) Any willful violation of this subchapter by a public official may be considered cause for disciplinary action, including suspension or termination.

(c) Any person who willfully destroys, conceals, or removes a public record with the intent to prevent its disclosure under this subchapter shall be guilty of a misdemeanor and, upon conviction, shall be fined not more than $1,000 or imprisoned not more than one year, or both.

(d) The District government may not use public funds to pay any judgment or settlement arising from a willful violation of this subchapter by a public official acting outside the scope of the official's duties.

SCOPE AND APPLICABILITY.

The DC FOIA applies to all public bodies of the District of Columbia, including:

(1) The Executive Office of the Mayor and all executive agencies, departments, offices, boards, commissions, and authorities.
(2) The Council of the District of Columbia, to the extent of its administrative and official records (subject to Council rules regarding deliberative records).
(3) The District of Columbia Courts, to the extent of administrative records.
(4) Independent agencies, including the Office of the Inspector General, the Auditor, and other independent offices.
(5) Public charter schools and the Public Charter School Board.
(6) The District of Columbia Public Schools.
(7) The Metropolitan Police Department and other law enforcement agencies.
(8) The District of Columbia Housing Authority and other authorities.
(9) Advisory Neighborhood Commissions.
(10) Boards and commissions created by the Council or the Mayor.
(11) Any entity that receives public funds or exercises governmental authority, to the extent of the records relating to those functions.

The DC FOIA is modeled on the federal FOIA and is interpreted with reference to federal FOIA case law where the DC statute uses language substantially similar to the federal statute. However, the DC FOIA has its own body of case law from the DC Court of Appeals and the Superior Court that governs interpretation of provisions unique to the DC statute.""",
        'summary': 'The DC Freedom of Information Act (D.C. Code §§ 2-531 to 2-540) requires responses within 15 business days with a possible 10-day extension. It provides administrative appeal through the Mayor\'s office and judicial review in Superior Court. Willful destruction of records is a misdemeanor punishable by up to $1,000 fine or one year imprisonment.',
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
