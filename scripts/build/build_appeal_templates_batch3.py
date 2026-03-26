#!/usr/bin/env python3
"""Build appeal templates for states with admin appeal bodies."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

TEMPLATES = [
    {
        'jurisdiction': 'CT',
        'record_type': 'appeal',
        'template_name': 'Connecticut FOI Commission Complaint',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Freedom of Information Commission
18-20 Trinity Street, Suite 205
Hartford, CT 06106

Re: Complaint — Denial of Public Records Request
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}

Dear Freedom of Information Commission:

Pursuant to Conn. Gen. Stat. § 1-206(b)(1), I file this complaint alleging that {{agency_name}} violated the Freedom of Information Act by denying my request for public records.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, stating:

{{denial_basis}}

My original request was assigned reference number {{request_number}}.

BASIS FOR COMPLAINT

The denial is improper because the requested records are public records under Conn. Gen. Stat. § 1-200(5) and no exemption under § 1-210(b) applies. The agency bears the burden of proving applicability of any claimed exemption. See Conn. Gen. Stat. § 1-206(b)(1).

RELIEF REQUESTED

I respectfully request that the Commission:

1. Schedule a hearing on this complaint;
2. Find that the denial violated the Freedom of Information Act;
3. Order {{agency_name}} to produce the requested records in full; and
4. Award reasonable attorney's fees and costs if applicable under Conn. Gen. Stat. § 1-206(b)(2).

I understand that this complaint must be filed within 30 calendar days of the denial, and I am filing within that deadline. The denial was dated {{denial_date}}.

Enclosed: Copy of original request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'Must file within 30 calendar days of denial. FOIC conducts hearings and issues binding orders. Commission has subpoena power and can order production. Filing is free. Can also file online via FOIC website.'
    },
    {
        'jurisdiction': 'DE',
        'record_type': 'appeal',
        'template_name': 'Delaware Attorney General FOIA Advisory Opinion Request',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Office of the Attorney General
FOIA Unit
Carvel State Office Building
820 N. French Street
Wilmington, DE 19801

Re: Request for Advisory Opinion — FOIA Denial
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear FOIA Unit:

Pursuant to 29 Del. C. § 10005(e), I request an advisory opinion regarding {{agency_name}}'s denial of my Freedom of Information Act request.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a FOIA request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request on the following basis:

{{denial_basis}}

GROUNDS FOR REQUESTING OPINION

The denial is improper because the requested records are "public records" as defined by 29 Del. C. § 10002(l) and are not exempt under § 10002(l)(1)-(17). The agency has not met its burden of demonstrating that a specific exemption applies to each withheld record.

I believe the agency's reliance on the cited exemption is misplaced because the records requested do not fall within the scope of the claimed exemption.

REQUESTED RELIEF

I respectfully request that the Attorney General:

1. Issue an advisory opinion finding that the agency's denial violated FOIA;
2. Determine that the requested records are public records subject to disclosure; and
3. Recommend that {{agency_name}} produce the records in full.

I understand that this request must be filed within 60 days of the denial and that the Attorney General will issue a written opinion. Although the opinion is advisory, it carries significant persuasive authority in any subsequent court action under 29 Del. C. § 10005(d).

Enclosed: Copy of original request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'Must file within 60 days of denial. AG opinion is advisory but highly persuasive. If unsatisfied with AG opinion, requester may file in Superior Court under 29 Del. C. § 10005(d). Filing is free.'
    },
    {
        'jurisdiction': 'HI',
        'record_type': 'appeal',
        'template_name': 'Hawaii Office of Information Practices Complaint',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Office of Information Practices
No. 1 Capitol District Building
250 South Hotel Street, Suite 107
Honolulu, HI 96813

Re: Request for OIP Opinion — UIPA Records Denial
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Office of Information Practices:

Pursuant to Haw. Rev. Stat. § 92F-42(1), I request a formal opinion regarding {{agency_name}}'s denial of my request for government records under the Uniform Information Practices Act (UIPA).

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, stating:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR COMPLAINT

The denial is improper. Under Haw. Rev. Stat. § 92F-11(a), all government records are open to public inspection unless an exception in § 92F-13 specifically applies. The agency bears the burden of justifying any withholding. I believe the cited basis for denial does not apply to the requested records.

REQUESTED RELIEF

I respectfully request that OIP:

1. Investigate this complaint and review the records at issue;
2. Issue a formal opinion finding that the denial was improper under the UIPA;
3. Recommend or order that {{agency_name}} disclose the requested records; and
4. Provide any other relief OIP deems appropriate under Haw. Rev. Stat. § 92F-42.

I understand that OIP has authority to issue advisory opinions and that agencies generally comply with OIP guidance. If the matter is not resolved through OIP, I reserve the right to bring an action in circuit court under Haw. Rev. Stat. § 92F-15.

Enclosed: Copy of original request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'No strict filing deadline for OIP complaints, but file promptly. OIP opinions are advisory but agencies typically comply. OIP may also attempt informal mediation. Free to file. Can also file directly in circuit court under § 92F-15.'
    },
    {
        'jurisdiction': 'IA',
        'record_type': 'appeal',
        'template_name': 'Iowa Public Information Board Complaint',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Iowa Public Information Board
Wallace State Office Building
502 East 9th Street
Des Moines, IA 50319

Re: Formal Complaint — Denial of Open Records Request
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Iowa Public Information Board:

Pursuant to Iowa Code § 23.6, I file this formal complaint alleging that {{agency_name}} violated Iowa's Open Records Law (Iowa Code Chapter 22) by improperly denying my request for public records.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, citing:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

ALLEGED VIOLATION

Under Iowa Code § 22.2(1), every person has the right to examine and copy public records. The agency's denial is improper because the requested records do not fall within any exception recognized under Iowa Code § 22.7 or other applicable confidentiality provisions. The agency bears the burden of establishing that a specific exception applies.

REQUESTED RELIEF

I respectfully request that the Board:

1. Investigate this complaint under Iowa Code § 23.8;
2. Issue a finding that {{agency_name}} violated Chapter 22;
3. Order {{agency_name}} to produce the requested records in full;
4. Impose any appropriate remedies under Iowa Code § 23.10, including civil penalties if the violation was willful; and
5. Award costs and attorney's fees if applicable.

I understand that the Board has binding authority to adjudicate open records complaints and that its orders are enforceable. I also understand that the Board may attempt informal resolution before formal adjudication.

Enclosed: Copy of original request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'IPIB issues binding decisions. Board may attempt informal resolution first. Can impose civil penalties for willful violations. Free to file. Complaints can be submitted online via IPIB website. Board decisions are enforceable in court.'
    },
    {
        'jurisdiction': 'IL',
        'record_type': 'appeal',
        'template_name': 'Illinois Public Access Counselor Request for Review',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Access Counselor
Office of the Attorney General
500 South Second Street
Springfield, IL 62701
publicaccess@ilag.gov

Re: Request for Review — FOIA Denial
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Public Access Counselor:

Pursuant to 5 ILCS 140/9.5(a), I request review of {{agency_name}}'s denial of my Freedom of Information Act request.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a FOIA request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, providing the following basis:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR REVIEW

The denial is improper. Under 5 ILCS 140/1, FOIA is to be construed liberally in favor of disclosure. All records in the possession of a public body are presumed to be public, and the burden is on the agency to demonstrate that a specific exemption under 5 ILCS 140/7 applies. I believe the agency has not met that burden because the cited exemption does not apply to the records requested.

REQUESTED RELIEF

I respectfully request that the Public Access Counselor:

1. Review the denial and the records at issue;
2. Issue a binding opinion finding that the denial violated FOIA;
3. Order {{agency_name}} to disclose the requested records in full; and
4. Direct the agency to produce any reasonably segregable nonexempt portions of partially exempt records under 5 ILCS 140/7(1).

I understand that this request for review must be filed within 60 days of the denial and that the Public Access Counselor will issue a binding opinion. I am filing within that deadline.

Enclosed: Copy of original FOIA request, agency denial letter, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'Must file within 60 days of denial. PAC opinions are binding on the agency. PAC may also mediate informally. Free to file. Can also submit electronically via the AG FOIA website. Agency must comply with binding opinion unless it seeks judicial review within 35 days.'
    },
    {
        'jurisdiction': 'IN',
        'record_type': 'appeal',
        'template_name': 'Indiana Public Access Counselor Complaint',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Access Counselor
Office of the Attorney General
Indiana Government Center South, 5th Floor
302 West Washington Street
Indianapolis, IN 46204
pac@atg.in.gov

Re: Formal Complaint — Denial of Public Records Request
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Public Access Counselor:

Pursuant to Ind. Code § 5-14-5-6, I file this formal complaint alleging that {{agency_name}} violated Indiana's Access to Public Records Act (APRA), Ind. Code § 5-14-3, by denying my request for public records.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, stating:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR COMPLAINT

Under Ind. Code § 5-14-3-3(a), public records are available for inspection and copying. The denial is improper because the requested records do not fall within any exception under Ind. Code § 5-14-3-4. The agency bears the burden of sustaining its denial, and the cited basis does not justify withholding.

REQUESTED RELIEF

I respectfully request that the Public Access Counselor:

1. Investigate this complaint;
2. Issue an advisory opinion finding that the denial violated APRA; and
3. Recommend that {{agency_name}} produce the requested records in full.

I understand that Public Access Counselor opinions are advisory rather than binding, but they carry significant persuasive weight. I reserve the right to pursue enforcement in court under Ind. Code § 5-14-3-9 if the matter is not resolved.

Enclosed: Copy of original request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'PAC opinions are advisory only but carry persuasive weight. Free to file. Complaints can be submitted via email to pac@atg.in.gov. PAC typically responds within 30 days. If unsatisfied, requester may file suit in circuit or superior court under Ind. Code § 5-14-3-9.'
    },
    {
        'jurisdiction': 'KY',
        'record_type': 'appeal',
        'template_name': 'Kentucky Attorney General Open Records Appeal',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Office of the Attorney General
Open Records Division
700 Capitol Avenue, Suite 118
Frankfort, KY 40601

Re: Open Records Appeal
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Open Records Division:

Pursuant to KRS 61.880(1), I appeal the denial of my open records request by {{agency_name}}.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, citing:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR APPEAL

Under KRS 61.870 et seq., public records are open for inspection by any person unless a specific exemption under KRS 61.878(1) applies. The burden is on the public agency to sustain its denial. KRS 61.882(3). I believe the denial is improper because the cited exemption does not apply to the requested records.

The Open Records Act is to be construed liberally in favor of disclosure, and exceptions are to be strictly construed. Any doubts must be resolved in favor of disclosure.

REQUESTED RELIEF

I respectfully request that the Attorney General:

1. Review the agency's denial;
2. Issue an opinion finding that the denial violated the Open Records Act; and
3. Direct {{agency_name}} to produce the requested records in full.

I understand that the Attorney General must issue an opinion within 20 business days under KRS 61.880(2)(a), and that the AG's opinion is binding on the agency unless the agency appeals to circuit court within 30 days under KRS 61.880(5)(b).

Enclosed: Copy of original request, copy of agency denial, and any supporting documentation.

Sincerely,
{{requester_name}}""",
        'notes': 'AG must issue opinion within 20 business days. AG opinions are binding — agency must comply or appeal to circuit court within 30 days. Free to file. One of the strongest administrative appeal mechanisms in the country. Appeal should include copies of request and denial.'
    },
    {
        'jurisdiction': 'MD',
        'record_type': 'appeal',
        'template_name': 'Maryland Public Information Act Compliance Board Complaint',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Information Act Compliance Board
Office of the Attorney General
200 Saint Paul Place, 20th Floor
Baltimore, MD 21202

Re: Complaint — Denial of PIA Request
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Compliance Board:

Pursuant to Md. Code, Gen. Prov. § 4-1B-04, I file this complaint alleging that {{agency_name}} violated the Maryland Public Information Act (PIA) by improperly denying my request for public records.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a PIA request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, stating:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR COMPLAINT

Under Md. Code, Gen. Prov. § 4-103, all persons are entitled to inspect public records. The denial is improper because the requested records do not fall within any exemption under Part III of the PIA (§§ 4-301 through 4-362). The agency bears the burden of justifying its refusal to disclose.

REQUESTED RELIEF

I respectfully request that the Compliance Board:

1. Investigate this complaint;
2. Issue an opinion finding that the denial violated the PIA;
3. Recommend that {{agency_name}} produce the requested records; and
4. Refer the matter for further action if appropriate under Gen. Prov. § 4-1B-06.

I understand that this complaint must be filed within 30 days of the denial. The denial was dated {{denial_date}}, and I am filing within that deadline.

I also understand that the Compliance Board issues advisory opinions and may refer matters involving willful or knowing violations for further enforcement. I reserve the right to file suit in circuit court under Gen. Prov. § 4-362 if the matter is not resolved.

Enclosed: Copy of original PIA request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'Must file within 30 days of denial. Compliance Board opinions are advisory but influential. Board can refer willful violations to AG for enforcement. Free to file. Can also file directly in circuit court under Gen. Prov. § 4-362. Board also handles fee disputes.'
    },
    {
        'jurisdiction': 'MO',
        'record_type': 'appeal',
        'template_name': 'Missouri Attorney General Sunshine Law Complaint',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Office of the Attorney General
Sunshine Law Enforcement
P.O. Box 899
Jefferson City, MO 65102

Re: Sunshine Law Complaint — Denial of Records Request
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Attorney General:

Pursuant to Mo. Rev. Stat. § 610.027, I file this complaint alleging that {{agency_name}} violated Missouri's Sunshine Law (Chapter 610) by improperly denying my request for public records.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a Sunshine Law request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, citing:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR COMPLAINT

Under Mo. Rev. Stat. § 610.011, the Sunshine Law is to be liberally construed to promote maximum public access. All records of a public governmental body are presumed open under § 610.011(2). The agency bears the burden of proving that a specific closure provision under § 610.021 applies. The cited basis for denial does not justify withholding.

REQUESTED ACTION

I respectfully request that the Attorney General:

1. Investigate this complaint under § 610.027;
2. Determine that {{agency_name}}'s denial violated the Sunshine Law; and
3. Take appropriate enforcement action, including seeking a court order compelling disclosure if warranted.

I understand that the Attorney General may investigate Sunshine Law complaints and has authority to bring enforcement actions. I also reserve the right to file a civil action in circuit court under Mo. Rev. Stat. § 610.027(1), where a court may award actual damages, civil penalties of up to $5,000, and reasonable attorney's fees.

Enclosed: Copy of original request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'Missouri has no formal administrative appeal body. AG can investigate Sunshine Law complaints and bring enforcement actions. Primary remedy is circuit court action under § 610.027. Court can award actual damages, civil penalties up to $5,000, costs, and attorney fees. Knowingly violating the law can result in a Class A misdemeanor.'
    },
    {
        'jurisdiction': 'NE',
        'record_type': 'appeal',
        'template_name': 'Nebraska Pre-Litigation Demand Letter (Public Records)',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{agency_head_name}}
{{agency_name}}
{{agency_address}}

Re: Demand for Production of Public Records
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear {{agency_head_name}}:

I write to demand production of public records that {{agency_name}} improperly denied on {{denial_date}}, in violation of the Nebraska Public Records Statutes, Neb. Rev. Stat. §§ 84-712 to 84-712.09.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, your office denied my request, citing:

{{denial_basis}}

LEGAL ANALYSIS

Under Neb. Rev. Stat. § 84-712, all citizens have the right to examine public records during normal business hours. Records may only be withheld if they fall within a specific statutory exception under § 84-712.05. The burden of justifying nondisclosure rests entirely with the custodian.

The cited basis for denial does not apply to the requested records. The Nebraska Supreme Court has held that exceptions to the public records statutes must be narrowly construed, and any doubt is to be resolved in favor of disclosure.

DEMAND

I demand that {{agency_name}} produce the requested records within 10 business days of receiving this letter.

If the records are not produced, I intend to pursue all available legal remedies, including filing a mandamus action under Neb. Rev. Stat. § 84-712.03 in the district court. Under that provision, the court may award reasonable attorney's fees to a prevailing plaintiff.

I have also forwarded a copy of this correspondence to the Office of the Attorney General for informational purposes and to request any available advisory guidance on this matter.

This letter is intended as a good-faith attempt to resolve this dispute without litigation.

Enclosed: Copy of original request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}

cc: Office of the Attorney General, State of Nebraska""",
        'notes': 'Nebraska has no formal administrative appeal body. AG may issue advisory opinions on public records questions but there is no complaint mechanism. Primary remedy is mandamus in district court under § 84-712.03. Court can award attorney fees to prevailing requester. This template is a pre-litigation demand letter — send before filing suit to demonstrate good faith.'
    },
    {
        'jurisdiction': 'NJ',
        'record_type': 'appeal',
        'template_name': 'New Jersey Government Records Council Complaint',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Government Records Council
101 South Broad Street
P.O. Box 819
Trenton, NJ 08625-0819

Re: Denial of Access Complaint
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Government Records Council:

Pursuant to N.J.S.A. 47:1A-6, I file this Denial of Access Complaint alleging that {{agency_name}} violated the Open Public Records Act (OPRA) by improperly denying my request for government records.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted an OPRA request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, stating:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR COMPLAINT

Under N.J.S.A. 47:1A-1, government records are to be readily accessible for examination, copying, or inspection by citizens. OPRA is to be construed in favor of the public's right of access. The agency bears the burden of proving that a specific exemption applies. N.J.S.A. 47:1A-6. The denial is improper because the cited basis does not justify withholding the requested records.

REQUESTED RELIEF

I respectfully request that the GRC:

1. Accept this complaint for adjudication;
2. Investigate the denial and review the records in camera if necessary;
3. Issue a final decision finding that the denial violated OPRA;
4. Order {{agency_name}} to produce the requested records in full; and
5. Award reasonable attorney's fees and costs pursuant to N.J.S.A. 47:1A-6.

I understand that this complaint must be filed within 45 days of the denial and that I am filing within that deadline. I also understand that filing with the GRC is an alternative to filing in Superior Court, and that GRC decisions are binding.

Enclosed: Copy of original OPRA request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'Must file within 45 days of denial. GRC decisions are binding. Alternative to Superior Court — cannot pursue both simultaneously. GRC process is free. Can be filed online. GRC may order in camera review and can award attorney fees. Process can be slow (months to years).'
    },
    {
        'jurisdiction': 'PA',
        'record_type': 'appeal',
        'template_name': 'Pennsylvania Office of Open Records Appeal',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Office of Open Records
Commonwealth Keystone Building
400 North Street, Plaza Level
Harrisburg, PA 17120

Re: Right-to-Know Law Appeal
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear Office of Open Records:

Pursuant to 65 P.S. § 67.1101, I appeal the denial of my Right-to-Know Law request by {{agency_name}}.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a Right-to-Know Law request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, citing:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

GROUNDS FOR APPEAL

Under 65 P.S. § 67.305(a), a record in the possession of a Commonwealth agency or local agency is presumed to be a public record. The burden of proving that a record is exempt from disclosure rests with the agency under § 67.708(a)(1). The denial is improper because the cited exemption does not apply to the requested records.

The Right-to-Know Law is remedial legislation that must be construed liberally to effect its purpose of promoting transparency and access to public records.

REQUESTED RELIEF

I respectfully request that the Office of Open Records:

1. Review this appeal and the agency's denial;
2. Conduct an in camera review of the records if necessary;
3. Issue a final determination finding that the denial was improper; and
4. Order {{agency_name}} to produce the requested records in full.

I understand that this appeal must be filed within 15 business days of the denial. The denial was dated {{denial_date}}, and I am filing within that deadline.

I understand that OOR must issue a final determination within 30 days (extendable for good cause) and that OOR determinations are binding unless appealed to the Court of Common Pleas within 30 days.

Enclosed: Copy of original RTK request, agency denial, and any supporting documentation.

Sincerely,
{{requester_name}}""",
        'notes': 'Must file within 15 business days of denial. OOR determinations are binding. OOR can conduct in camera review and take testimony. Free to file. Can file online via OOR website. OOR must decide within 30 days (extendable). Either party can appeal to Court of Common Pleas within 30 days. For legislative/judicial records, appeal goes to respective appeals officer, not OOR.'
    },
    {
        'jurisdiction': 'UT',
        'record_type': 'appeal',
        'template_name': 'Utah State Records Committee Appeal',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

State Records Committee
c/o Division of Archives and Records Service
346 South Rio Grande Street
Salt Lake City, UT 84101

Re: GRAMA Appeal — Denial of Records Request
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear State Records Committee:

Pursuant to Utah Code § 63G-2-403, I appeal the denial of my records request by {{agency_name}} under the Government Records Access and Management Act (GRAMA).

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a GRAMA request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, citing:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

I appealed to the chief administrative officer of {{agency_name}} as required by Utah Code § 63G-2-401, and on {{denial_date}} that appeal was also denied.

GROUNDS FOR APPEAL

Under Utah Code § 63G-2-201(2), every person has the right to inspect and receive a copy of a public record. Records may only be classified as private, controlled, or protected under the specific provisions of §§ 63G-2-302 through 63G-2-305. The agency bears the burden of proving that a record is not a public record. The cited classification is improper because the requested records do not fall within the scope of the exemption claimed.

REQUESTED RELIEF

I respectfully request that the State Records Committee:

1. Schedule a hearing on this appeal;
2. Review the records in camera;
3. Find that the records are public under GRAMA; and
4. Order {{agency_name}} to release the records in full.

I understand that this appeal must be filed within 30 days of the chief administrative officer's denial. The denial was dated {{denial_date}}, and I am filing within that deadline. I understand the hearing is free and that I may present testimony and evidence.

Enclosed: Copy of original GRAMA request, agency denial, chief administrative officer's decision, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'Must first appeal to agency head under § 63G-2-401. Then appeal to State Records Committee within 30 days. Committee holds hearings and issues binding orders. Free to file. Alternative: can appeal directly to district court under § 63G-2-404 instead (cannot do both). Committee has in camera review authority.'
    },
    {
        'jurisdiction': 'VA',
        'record_type': 'appeal',
        'template_name': 'Virginia FOIA Advisory Council Opinion Request',
        'template_text': """{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

FOIA Advisory Council
Virginia Division of Legislative Services
Pocahontas Building
900 East Main Street, Suite 801
Richmond, VA 23219
foiacouncil@dls.virginia.gov

Re: Request for Written Advisory Opinion — FOIA Denial
    Agency: {{agency_name}}
    Date of Original Request: {{original_request_date}}
    Date of Denial: {{denial_date}}
    Request Reference: {{request_number}}

Dear FOIA Advisory Council:

Pursuant to Va. Code § 30-179(A)(5), I request a written advisory opinion regarding {{agency_name}}'s denial of my Virginia Freedom of Information Act request.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a FOIA request to {{agency_name}} for:

{{description_of_records}}

On {{denial_date}}, {{agency_name}} denied my request, citing:

{{denial_basis}}

My request was assigned reference number {{request_number}}.

ISSUE PRESENTED

Whether {{agency_name}}'s denial of my request was proper under the Virginia Freedom of Information Act, Va. Code §§ 2.2-3700 through 2.2-3714.

ANALYSIS

Under Va. Code § 2.2-3704(A), all public records are presumed open and must be made available for inspection and copying. Exemptions under § 2.2-3705.1 through § 2.2-3705.8 are discretionary — the agency is not required to withhold records even if an exemption applies. The burden is on the agency to justify its denial with specificity.

The denial is improper because the cited exemption does not apply to the requested records, or alternatively, the agency should exercise its discretion in favor of disclosure consistent with the policy of openness expressed in § 2.2-3700.

REQUESTED RELIEF

I respectfully request that the FOIA Advisory Council:

1. Issue a written advisory opinion finding that the denial was improper under FOIA;
2. Advise that the requested records should be disclosed; and
3. Provide any other guidance the Council deems appropriate.

I understand that FOIA Advisory Council opinions are advisory and non-binding, but they provide authoritative guidance on FOIA questions and are given significant weight by courts and agencies. I reserve the right to file a petition for mandamus or injunction in general district or circuit court under Va. Code § 2.2-3713 if the matter is not resolved.

Enclosed: Copy of original FOIA request, agency denial, and any related correspondence.

Sincerely,
{{requester_name}}""",
        'notes': 'FOIA Advisory Council opinions are advisory and non-binding but carry significant persuasive authority. Free to request. Council also offers mediation services. Primary enforcement is through court action under § 2.2-3713. Court may award attorney fees and costs to a prevailing petitioner. No strict filing deadline for Council opinions but file promptly.'
    },
]


def build():
    conn = db_connect(DB_PATH)
    for t in TEMPLATES:
        existing = conn.execute(
            "SELECT id FROM request_templates WHERE jurisdiction=? AND record_type='appeal'",
            (t['jurisdiction'],)
        ).fetchone()
        if existing:
            print(f"  {t['jurisdiction']}: appeal template already exists, skipping")
            continue
        conn.execute('''
            INSERT INTO request_templates (jurisdiction, record_type, template_name, template_text, notes)
            VALUES (:jurisdiction, :record_type, :template_name, :template_text, :notes)
        ''', t)
        print(f"  {t['jurisdiction']}: inserted appeal template")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    build()
