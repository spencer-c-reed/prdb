#!/usr/bin/env python3
"""Build appeal templates for direct-to-court states: ND, NH, NM, NV, OH, OK, RI, SC, SD, TN, WA, WI, WV, WY.

These states have NO administrative appeal process. The only remedy after a denial
is filing suit in court. Each template is a pre-litigation demand letter — the step
before filing a complaint — citing the relevant statute and setting a deadline.

Run: python3 scripts/build/build_appeal_templates_batch2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

TEMPLATES = [
    {
        'jurisdiction': 'ND',
        'record_type': 'appeal',
        'template_name': 'North Dakota Open Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under N.D.C.C. § 44-04-18; Notice of Intent to File Suit Under N.D.C.C. § 44-04-21.2

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my open records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the North Dakota open records law, N.D.C.C. § 44-04-18, which provides that all records of a public entity are public unless specifically exempted by law.

North Dakota does not provide an administrative appeal process for records denials. The sole remedy is a civil action under N.D.C.C. § 44-04-21.2. Before filing suit, I am providing you this opportunity to reconsider and comply voluntarily.

Specifically, I note the following:

1. Under N.D.C.C. § 44-04-21.2, the burden of proof rests on the public entity to establish that the records are exempt from disclosure. Your denial has not met that burden.

2. {{exemption_challenge_arguments}}

3. Even if portions of the requested records contain exempt information, you are required to segregate and produce the nonexempt portions. See N.D.C.C. § 44-04-18(7).

4. If I am compelled to file suit and prevail, the court may award reasonable attorney fees and costs under N.D.C.C. § 44-04-21.2(3). The court may also impose a civil penalty of up to $1,000 if the violation was committed knowingly.

DEMAND: I demand that you produce the requested records, or provide a legally sufficient written explanation of each exemption claimed, within ten (10) calendar days of your receipt of this letter. If you fail to do so, I intend to file a complaint in district court seeking an order compelling disclosure and an award of attorney fees, costs, and any applicable civil penalties.

Sincerely,
{{requester_name}}''',
        'notes': 'ND has no administrative appeal. Only remedy is district court action under N.D.C.C. § 44-04-21.2. Burden on agency. Court may award attorney fees and civil penalties up to $1,000 for knowing violations.',
    },
    {
        'jurisdiction': 'NH',
        'record_type': 'appeal',
        'template_name': 'New Hampshire Right-to-Know — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under RSA 91-A; Notice of Intent to Petition Superior Court Under RSA 91-A:7

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my Right-to-Know request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates New Hampshire's Right-to-Know Law, RSA 91-A:4, which mandates that governmental records shall be available for public inspection.

New Hampshire does not provide a formal administrative appeal process for records denials. The remedy is a petition to the superior court under RSA 91-A:7, or a complaint to the Ombudsman (RSA 91-A:7-a), though the Ombudsman's findings are non-binding. Before pursuing judicial relief, I am giving you this opportunity to reconsider.

I note the following:

1. Under RSA 91-A:7, the burden of proof is on the public body to sustain the denial. Your response has not demonstrated that the requested records fall within any recognized exemption.

2. {{exemption_challenge_arguments}}

3. Even if some records contain exempt material, you must segregate and release all nonexempt portions. See RSA 91-A:5, IV.

4. If I petition the court and prevail, RSA 91-A:8 provides that the court shall award reasonable attorney fees and costs. In cases of bad faith, the court may award damages as well.

DEMAND: I demand that you produce the requested records, or provide a detailed written justification for each exemption claimed, within ten (10) calendar days of your receipt of this letter. If you fail to comply, I will file a petition in superior court seeking an order compelling disclosure and an award of attorney fees and costs as provided by RSA 91-A:8.

Sincerely,
{{requester_name}}''',
        'notes': 'NH has no mandatory administrative appeal. Remedy is superior court petition under RSA 91-A:7 or non-binding Ombudsman complaint under RSA 91-A:7-a. Burden on agency. Mandatory attorney fee award to prevailing requesters under RSA 91-A:8.',
    },
    {
        'jurisdiction': 'NM',
        'record_type': 'appeal',
        'template_name': 'New Mexico IPRA — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under the Inspection of Public Records Act; Notice of Intent to File Suit Under NMSA § 14-2-12

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my public records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the New Mexico Inspection of Public Records Act (IPRA), NMSA § 14-2-1 et seq., which declares that every person has a right to inspect public records.

New Mexico does not provide an administrative appeal process for IPRA denials. The sole remedy is an enforcement action in district court under NMSA § 14-2-12. Before filing suit, I am providing you this opportunity to comply.

I note the following:

1. Under NMSA § 14-2-12(D), the burden of proof is on the custodian to demonstrate that the records are exempt from disclosure. Your denial has not met that burden.

2. {{exemption_challenge_arguments}}

3. You are required to separate exempt from nonexempt material and produce everything that is not specifically exempt. See NMSA § 14-2-9.

4. If I file suit and the court finds that records were wrongfully withheld, the court shall award damages, costs, and reasonable attorney fees under NMSA § 14-2-12(D). The court may also award additional damages up to $100 per day for each day the records were wrongfully withheld.

DEMAND: I demand that you produce the requested records, or provide a particularized written explanation of each exemption claimed, within fifteen (15) calendar days of your receipt of this letter. If you fail to do so, I will file an action in district court seeking injunctive relief, damages, attorney fees, and per-diem penalties as authorized by NMSA § 14-2-12.

Sincerely,
{{requester_name}}''',
        'notes': 'NM has no administrative appeal. Only remedy is district court under NMSA § 14-2-12. Burden on custodian. Mandatory attorney fees plus up to $100/day in per-diem penalties for wrongful withholding.',
    },
    {
        'jurisdiction': 'NV',
        'record_type': 'appeal',
        'template_name': 'Nevada Public Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under NRS 239.010; Notice of Intent to File Suit Under NRS 239.011

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my public records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the Nevada Public Records Act, NRS 239.010, which establishes that all public books and records are open to inspection by any person.

Nevada does not provide a mandatory administrative appeal for records denials. The remedy is a district court action under NRS 239.011. Before filing suit, I am providing you this opportunity to reconsider.

I note the following:

1. Under NRS 239.0113, the burden of proof is on the governmental entity to demonstrate by a preponderance of the evidence that the records are confidential. Your denial has not carried that burden.

2. {{exemption_challenge_arguments}}

3. If records contain both confidential and public information, you must segregate the confidential portions and produce the remainder. See NRS 239.010(3).

4. If I file suit and prevail, the court may award attorney fees and costs under NRS 239.011(2). The court is also authorized to impose a civil penalty of $25 per day for each day the records were wrongfully withheld, up to $1,000.

DEMAND: I demand that you produce the requested records, or provide a written explanation identifying the specific statutory authority for each claimed exemption, within ten (10) calendar days of your receipt of this letter. If you fail to do so, I will file an action in district court seeking an order compelling production, attorney fees, and applicable civil penalties under NRS 239.011.

Sincerely,
{{requester_name}}''',
        'notes': 'NV has no mandatory administrative appeal. Remedy is district court under NRS 239.011. Burden on agency by preponderance of evidence. Court may award fees and civil penalties of $25/day up to $1,000.',
    },
    {
        'jurisdiction': 'OH',
        'record_type': 'appeal',
        'template_name': 'Ohio Public Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under R.C. § 149.43; Notice of Intent to File Mandamus Under R.C. § 149.43(C)

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my public records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates Ohio's Public Records Act, R.C. § 149.43(B), which requires that public records be made available promptly for inspection.

Ohio does not provide a formal administrative appeal for public records denials. The remedy is a mandamus action in the Court of Claims under R.C. § 149.43(C), or in any other court of competent jurisdiction. Before filing suit, I am providing you this opportunity to comply.

I note the following:

1. Under R.C. § 149.43(C)(1), the burden of proof is on the public office to establish that the requested records are exempt from disclosure.

2. {{exemption_challenge_arguments}}

3. If any portion of a record is exempt, you must redact the exempt material and release the rest. See R.C. § 149.43(B)(1).

4. Ohio's mandamus remedy includes significant fee-shifting provisions. Under R.C. § 149.43(C)(2), if the court orders production, the court shall award the requester reasonable attorney fees, court costs, and statutory damages. The statutory damages provision provides $100 for each business day the records were not made available, up to $1,000. Additionally, if the court finds the denial was made in bad faith, it may award additional penalties.

DEMAND: I demand that you produce the requested records, or provide a written explanation identifying the specific exception under R.C. § 149.43(A)(1) for each withheld record, within ten (10) calendar days of your receipt of this letter. If you fail to do so, I will file a mandamus action in the Court of Claims seeking an order compelling disclosure, statutory damages, and attorney fees under R.C. § 149.43(C).

Sincerely,
{{requester_name}}''',
        'notes': 'OH has no administrative appeal. Remedy is mandamus in Court of Claims or other court under R.C. § 149.43(C). Burden on agency. Mandatory attorney fees plus statutory damages of $100/business day up to $1,000.',
    },
    {
        'jurisdiction': 'OK',
        'record_type': 'appeal',
        'template_name': 'Oklahoma Open Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under the Oklahoma Open Records Act; Notice of Intent to File Suit Under 51 O.S. § 24A.17

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my open records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the Oklahoma Open Records Act, 51 O.S. § 24A.1 et seq., which provides that all records of public bodies are open to any person for inspection and copying.

Oklahoma does not provide a formal administrative appeal for open records denials. The remedy is a civil action in district court under 51 O.S. § 24A.17. Before resorting to litigation, I am providing you this opportunity to reconsider.

I note the following:

1. Under 51 O.S. § 24A.17(B), the burden of proof is on the public body to demonstrate that the records are exempt from disclosure. Your denial has not satisfied that burden.

2. {{exemption_challenge_arguments}}

3. Exempt material must be segregated from nonexempt material, and the nonexempt portions must be released. See 51 O.S. § 24A.5(4).

4. If I file suit and the court orders disclosure, 51 O.S. § 24A.17(C) provides that the court shall award reasonable attorney fees to the prevailing plaintiff. The court may also award costs. Willful violations carry additional penalties.

DEMAND: I demand that you produce the requested records, or provide a detailed written explanation citing the specific statutory exemption for each withheld record, within ten (10) calendar days of your receipt of this letter. If you fail to comply, I will file a civil action in district court seeking an order compelling disclosure, attorney fees, and costs under 51 O.S. § 24A.17.

Sincerely,
{{requester_name}}''',
        'notes': 'OK has no administrative appeal. Remedy is district court under 51 O.S. § 24A.17. Burden on agency. Mandatory attorney fees to prevailing plaintiff under 51 O.S. § 24A.17(C).',
    },
    {
        'jurisdiction': 'RI',
        'record_type': 'appeal',
        'template_name': 'Rhode Island APRA — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under R.I.G.L. § 38-2-1 et seq.; Notice of Intent to File Suit Under R.I.G.L. § 38-2-9

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my Access to Public Records Act (APRA) request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the Rhode Island Access to Public Records Act, R.I.G.L. § 38-2-1 et seq.

While Rhode Island allows for a complaint to the Attorney General, the AG's determination is advisory and non-binding. The binding remedy is a civil action in superior court under R.I.G.L. § 38-2-9. Before pursuing litigation, I am providing you this opportunity to reconsider.

I note the following:

1. Under R.I.G.L. § 38-2-10, the burden of proof rests on the public body to demonstrate that the records are exempt from public access. Your denial has not carried that burden.

2. {{exemption_challenge_arguments}}

3. If a record contains both exempt and nonexempt material, you must segregate the exempt portions and produce the rest. See R.I.G.L. § 38-2-6(a).

4. If I file suit and prevail, the court shall assess reasonable attorney fees and costs against the public body under R.I.G.L. § 38-2-9(d). If the court finds the denial was willful or made in bad faith, the court may assess a fine of $20 to $200 per violation.

DEMAND: I demand that you produce the requested records, or provide a written explanation identifying the specific APRA exemption for each withheld record, within fifteen (15) calendar days of your receipt of this letter. If you fail to do so, I will file a complaint in superior court seeking an order compelling disclosure, attorney fees, and any applicable fines under R.I.G.L. § 38-2-9.

Sincerely,
{{requester_name}}''',
        'notes': 'RI AG complaints are non-binding/advisory. Binding remedy is superior court under R.I.G.L. § 38-2-9. Burden on agency. Mandatory attorney fees; fines of $20-$200 per willful/bad faith violation.',
    },
    {
        'jurisdiction': 'SC',
        'record_type': 'appeal',
        'template_name': 'South Carolina FOIA — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under S.C. Freedom of Information Act; Notice of Intent to File Suit Under S.C. Code § 30-4-100

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my Freedom of Information Act request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the South Carolina Freedom of Information Act (FOIA), S.C. Code § 30-4-10 et seq., which provides that all public records are to be available for inspection and copying unless specifically exempted.

South Carolina does not provide a mandatory administrative appeal for FOIA denials. The remedy is a civil action in circuit court under S.C. Code § 30-4-100. Before filing suit, I am providing you this opportunity to comply.

I note the following:

1. Under S.C. Code § 30-4-100(b), the public body has the burden of proving that it has complied with the requirements of the FOIA. Your denial has not met that burden.

2. {{exemption_challenge_arguments}}

3. If records contain both exempt and nonexempt material, you are required to redact the exempt portions and produce the remainder. See S.C. Code § 30-4-40(a)(5).

4. If I file suit and prevail, the court may award reasonable attorney fees and other costs of litigation under S.C. Code § 30-4-100(c). In addition, if the court finds that the denial was willful, the court may assess a civil fine not to exceed $100 against the custodian and/or not to exceed $500 against the public body.

DEMAND: I demand that you produce the requested records, or provide a detailed written explanation citing the specific FOIA exemption for each withheld record, within fifteen (15) calendar days of your receipt of this letter. If you fail to comply, I will file a civil action in circuit court seeking an order compelling production, attorney fees, and applicable penalties under S.C. Code § 30-4-100.

Sincerely,
{{requester_name}}''',
        'notes': 'SC has no mandatory administrative appeal. Remedy is circuit court under S.C. Code § 30-4-100. Burden on agency. Court may award attorney fees; civil fines up to $100 against custodian and $500 against body for willful violations.',
    },
    {
        'jurisdiction': 'SD',
        'record_type': 'appeal',
        'template_name': 'South Dakota Open Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under S.D.C.L. § 1-27-1 et seq.; Notice of Intent to File Suit Under S.D.C.L. § 1-27-37

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my open records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates South Dakota's open records law, S.D.C.L. § 1-27-1, which provides that all records of public bodies are public unless otherwise provided by law.

South Dakota does not provide a formal administrative appeal for records denials. The remedy is a civil action in circuit court under S.D.C.L. § 1-27-37. Before filing suit, I am providing you this opportunity to reconsider.

I note the following:

1. Under S.D.C.L. § 1-27-37, the burden of proof is on the public entity to demonstrate that the records are specifically exempt from disclosure.

2. {{exemption_challenge_arguments}}

3. Exempt material must be segregated from nonexempt material, and the nonexempt portions must be released. See S.D.C.L. § 1-27-1.5.

4. If I file suit and the court orders disclosure, the court may assess reasonable attorney fees against the public entity under S.D.C.L. § 1-27-37.

DEMAND: I demand that you produce the requested records, or provide a written explanation identifying the specific statutory authority for each exemption claimed, within ten (10) calendar days of your receipt of this letter. If you fail to comply, I will file a civil action in circuit court seeking an order compelling disclosure and attorney fees under S.D.C.L. § 1-27-37.

Sincerely,
{{requester_name}}''',
        'notes': 'SD has no administrative appeal. Remedy is circuit court under S.D.C.L. § 1-27-37. Burden on agency. Court may award attorney fees.',
    },
    {
        'jurisdiction': 'TN',
        'record_type': 'appeal',
        'template_name': 'Tennessee Public Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under the Tennessee Public Records Act; Notice of Intent to File Suit Under Tenn. Code § 10-7-505

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my public records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the Tennessee Public Records Act, Tenn. Code § 10-7-503, which provides that all state, county, and municipal records are open for personal inspection by any citizen of Tennessee.

While Tennessee's Office of Open Records Counsel (OORC) can review complaints, its opinions are advisory and non-binding. The binding remedy is a petition to chancery or circuit court under Tenn. Code § 10-7-505. Before filing suit, I am providing you this opportunity to reconsider.

I note the following:

1. Under Tenn. Code § 10-7-505(c), the burden of proof is on the entity resisting disclosure to demonstrate that the records are exempt. Your denial has not met that burden.

2. {{exemption_challenge_arguments}}

3. If the records contain both confidential and public information, you must redact the confidential portions and release the rest. See Tenn. Code § 10-7-503(b).

4. If I file a petition and the court orders disclosure, the court may award reasonable attorney fees under Tenn. Code § 10-7-505(g). The court may also assess a willful-violation penalty.

DEMAND: I demand that you produce the requested records, or provide a detailed written explanation citing the specific statutory exemption for each withheld record, within fifteen (15) calendar days of your receipt of this letter. If you fail to comply, I will file a petition in chancery court seeking an order compelling disclosure and attorney fees under Tenn. Code § 10-7-505.

Sincerely,
{{requester_name}}''',
        'notes': 'TN OORC opinions are advisory/non-binding. Binding remedy is chancery or circuit court under Tenn. Code § 10-7-505. Burden on agency. Court may award attorney fees.',
    },
    {
        'jurisdiction': 'WA',
        'record_type': 'appeal',
        'template_name': 'Washington Public Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under the Washington Public Records Act; Notice of Intent to File Suit Under RCW 42.56.550

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my Public Records Act request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the Washington Public Records Act (PRA), RCW 42.56.001 et seq., which the legislature has declared "shall be liberally construed and its exemptions narrowly construed to promote this public policy."

Washington does not provide a mandatory administrative appeal for PRA denials. The remedy is an action in superior court under RCW 42.56.550(1). Before filing suit, I am providing you this opportunity to comply.

I note the following:

1. Under RCW 42.56.550(1), the burden of proof is on the agency to demonstrate that the records fall within a specific exemption. Your denial has not carried that burden.

2. {{exemption_challenge_arguments}}

3. If records contain both exempt and nonexempt material, you must redact the exempt portions and produce the rest. See RCW 42.56.210(1).

4. Washington's PRA provides strong fee-shifting and penalty provisions. If the court orders disclosure, RCW 42.56.550(4) provides that the court shall award reasonable attorney fees, costs, and a per-day penalty of between $5 and $100 for each day the agency denied access. For agencies acting in bad faith, penalties can be significantly higher. The per-day penalty is mandatory, not discretionary.

DEMAND: I demand that you produce the requested records, or provide a written explanation identifying the specific PRA exemption for each withheld record, within ten (10) calendar days of your receipt of this letter. If you fail to do so, I will file an action in superior court seeking an order compelling production, attorney fees, and per-day penalties under RCW 42.56.550.

Sincerely,
{{requester_name}}''',
        'notes': 'WA has no administrative appeal. Remedy is superior court under RCW 42.56.550. Burden on agency. Mandatory attorney fees plus mandatory per-day penalty of $5-$100 for each day of wrongful denial. Exemptions narrowly construed by statute.',
    },
    {
        'jurisdiction': 'WI',
        'record_type': 'appeal',
        'template_name': 'Wisconsin Open Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under the Wisconsin Open Records Law; Notice of Intent to File Suit Under Wis. Stat. § 19.37

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my open records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the Wisconsin Public Records Law, Wis. Stat. § 19.31 et seq., which declares that it is the public policy of this state that all persons are entitled to the greatest possible information regarding the affairs of government.

Wisconsin does not provide a formal administrative appeal for records denials. The remedy is a mandamus or injunction action in circuit court under Wis. Stat. § 19.37(1). Before filing suit, I am providing you this opportunity to reconsider.

I note the following:

1. Under the Wisconsin Open Records Law, the custodian bears the burden of demonstrating that the denial was justified. An authority that withholds a record must provide a specific written explanation of the legal basis for the denial. See Wis. Stat. § 19.35(4)(b).

2. {{exemption_challenge_arguments}}

3. If a record contains both exempt and nonexempt material, you must delete or redact the exempt portions and provide the remainder. See Wis. Stat. § 19.36(6).

4. Under Wis. Stat. § 19.37(2), the court shall award reasonable attorney fees, damages of not less than $100, and other actual costs to a requester who prevails in a mandamus or injunctive action. If the court finds that the denial was made without a reasonable basis, it shall award punitive damages of not more than $1,000.

DEMAND: I demand that you produce the requested records, or provide a specific written explanation of the legal basis for the denial as required by Wis. Stat. § 19.35(4)(b), within ten (10) calendar days of your receipt of this letter. If you fail to comply, I will file a mandamus action in circuit court seeking an order compelling production, statutory damages, attorney fees, and punitive damages under Wis. Stat. § 19.37.

Sincerely,
{{requester_name}}''',
        'notes': 'WI has no administrative appeal. Remedy is mandamus/injunction in circuit court under Wis. Stat. § 19.37. Burden on custodian. Mandatory attorney fees, minimum $100 damages, and punitive damages up to $1,000 for unreasonable denials.',
    },
    {
        'jurisdiction': 'WV',
        'record_type': 'appeal',
        'template_name': 'West Virginia FOIA — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under the West Virginia Freedom of Information Act; Notice of Intent to File Suit Under W. Va. Code § 29B-1-5

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my Freedom of Information Act request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the West Virginia Freedom of Information Act (WVFOIA), W. Va. Code § 29B-1-1 et seq., which provides that all public records are the property of the citizens and the right of access shall be preserved.

West Virginia does not provide a mandatory administrative appeal for FOIA denials. The remedy is a civil action in circuit court under W. Va. Code § 29B-1-5. Before filing suit, I am providing you this opportunity to reconsider.

I note the following:

1. Under W. Va. Code § 29B-1-5(3), the burden of proof is on the public body to sustain its refusal to make available the requested records. Your denial has not met that burden.

2. {{exemption_challenge_arguments}}

3. If a record contains both exempt and nonexempt material, you must redact the exempt portions and produce the rest. See W. Va. Code § 29B-1-4(a)(4).

4. If I file suit and the court orders disclosure, the court may assess reasonable attorney fees and court costs against the public body under W. Va. Code § 29B-1-5(3). The court may also award damages in appropriate cases.

DEMAND: I demand that you produce the requested records, or provide a written explanation identifying the specific WVFOIA exemption for each withheld record, within ten (10) calendar days of your receipt of this letter. If you fail to comply, I will file a civil action in circuit court seeking an order compelling disclosure, attorney fees, and costs under W. Va. Code § 29B-1-5.

Sincerely,
{{requester_name}}''',
        'notes': 'WV has no mandatory administrative appeal. Remedy is circuit court under W. Va. Code § 29B-1-5. Burden on agency. Court may award attorney fees and costs.',
    },
    {
        'jurisdiction': 'WY',
        'record_type': 'appeal',
        'template_name': 'Wyoming Public Records — Pre-Litigation Demand',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{{custodian_name}}
{{agency_name}}
{{agency_address}}

Re: Demand to Produce Records Under the Wyoming Public Records Act; Notice of Intent to File Suit Under Wyo. Stat. § 16-4-204

Dear {{custodian_name}}:

I write concerning your {{denial_date}} response to my public records request dated {{original_request_date}}, in which I requested:

{{description_of_records}}

Your office {{description_of_denial}}. I believe this denial violates the Wyoming Public Records Act, Wyo. Stat. § 16-4-201 et seq., which provides that all public records shall be open for inspection by any person at reasonable times.

Wyoming does not provide a formal administrative appeal for records denials. The remedy is a civil action in district court under Wyo. Stat. § 16-4-204(c). Before filing suit, I am providing you this opportunity to comply.

I note the following:

1. Under Wyo. Stat. § 16-4-204(d), the burden of proof is on the custodian to sustain the denial of access. Your denial has not carried that burden.

2. {{exemption_challenge_arguments}}

3. If records contain both exempt and nonexempt information, you must redact the exempt material and produce the rest. See Wyo. Stat. § 16-4-203(d).

4. If I file suit and prevail, the court shall award costs and reasonable attorney fees to the prevailing party under Wyo. Stat. § 16-4-205(b). The court may also award damages for any loss sustained.

DEMAND: I demand that you produce the requested records, or provide a written explanation identifying the specific statutory exemption for each withheld record, within ten (10) calendar days of your receipt of this letter. If you fail to comply, I will file a civil action in district court seeking an order compelling disclosure and attorney fees under Wyo. Stat. § 16-4-204.

Sincerely,
{{requester_name}}''',
        'notes': 'WY has no administrative appeal. Remedy is district court under Wyo. Stat. § 16-4-204. Burden on custodian. Mandatory attorney fees to prevailing party under § 16-4-205(b).',
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
