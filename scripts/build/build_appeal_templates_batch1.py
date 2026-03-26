#!/usr/bin/env python3
"""Build appeal templates for direct-to-court states: AK, AL, AR, AZ, CO, GA, ID, KS, LA, MS, MT, NC.

These states have NO administrative appeal process. The only remedy for a
denied public records request is filing suit in court. Templates are pre-
litigation demand letters designed to prompt voluntary reconsideration
before the requester incurs the cost of litigation.

Run: python3 scripts/build/build_appeal_templates_batch1.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

TEMPLATES = [
    # =========================================================================
    # ALASKA
    # AS 40.25.110-120 (Alaska Public Records Act)
    # =========================================================================
    {
        'jurisdiction': 'AK',
        'record_type': 'appeal',
        'template_name': 'Alaska -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Public Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Alaska Public Records Act, AS 40.25.110-.220. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I am compelled to seek judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

Alaska law establishes a broad right of public access to government records. AS 40.25.110 provides that "every person has a right to inspect a public record," and exemptions must be narrowly construed. The burden of justifying nondisclosure rests squarely on the agency, not the requester. See Fuller v. City of Homer, 75 P.3d 1059 (Alaska 2003).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

Even if portions of the requested records fall within a recognized exemption, AS 40.25.110 requires your agency to segregate and release all non-exempt portions. A blanket denial is not permissible when redaction would preserve confidentiality while honoring the public's right of access.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file an action for injunctive relief in the Alaska Superior Court pursuant to AS 40.25.120. Please be advised that under AS 40.25.120, a court may award reasonable attorney's fees and costs to a requester who substantially prevails. A court will also review the withheld records in camera and make an independent determination as to whether the claimed exemption applies.

I would prefer to resolve this matter without litigation and hope your agency will take this opportunity to reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Alaska. No administrative appeal exists; the sole remedy is suit in Superior Court under AS 40.25.120. Court reviews de novo, may award attorney fees to prevailing requester. Burden of proof on agency. 15-day response deadline is a courtesy period before filing.',
    },

    # =========================================================================
    # ALABAMA
    # Ala. Code Section 36-12-40 (Alabama Open Records Act)
    # =========================================================================
    {
        'jurisdiction': 'AL',
        'record_type': 'appeal',
        'template_name': 'Alabama -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Open Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Alabama Open Records Act, Ala. Code Section 36-12-40. This letter constitutes a formal demand that your agency reconsider its denial and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request on the following grounds:

{{denial_basis}}

LEGAL ANALYSIS

Alabama law provides that "[e]very citizen has a right to inspect and take a copy of any public writing of this state, except as otherwise expressly provided by statute." Ala. Code Section 36-12-40. The Alabama Supreme Court has held that this right is to be liberally construed in favor of disclosure, and exemptions are to be narrowly applied. See Stone v. Consolidated Publishing Co., 404 So. 2d 678 (Ala. 1981).

The burden of establishing that records fall within a statutory exemption rests on the governmental body asserting it. Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

Even assuming arguendo that some portion of the requested records may be exempt, your agency is obligated to segregate and produce all non-exempt material. A blanket withholding is not justified when the exempt information can be redacted.

DEMAND

I respectfully demand that {{agency_name}} reconsider its position and produce the requested records, in full or with narrowly tailored redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file a mandamus action in circuit court to compel disclosure. Please note that Alabama courts have consistently enforced the public's right of access through mandamus, and that the costs of unsuccessful litigation will fall on your agency. See Chambers v. Birmingham News Co., 552 So. 2d 854 (Ala. 1989).

I would prefer to resolve this matter without litigation and trust your agency will give this demand serious consideration.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Alabama. No administrative appeal exists; the remedy is a mandamus action in circuit court. Alabama does not have a statutory attorney fee provision for open records cases, but courts can award costs. Burden of proof on agency. The statute is brief (Section 36-12-40) and case law fills in the gaps.',
    },

    # =========================================================================
    # ARKANSAS
    # Ark. Code Section 25-19-107 (Arkansas FOIA)
    # =========================================================================
    {
        'jurisdiction': 'AR',
        'record_type': 'appeal',
        'template_name': 'Arkansas -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- FOIA Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Arkansas Freedom of Information Act (FOIA), Ark. Code Section 25-19-101 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I am compelled to seek judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

The Arkansas FOIA declares that "it is vital in a democratic society that public business be performed in an open and public manner" and mandates that its provisions "shall be liberally interpreted to implement this policy." Ark. Code Section 25-19-102. All records are presumed open, and the custodian bears the burden of proving that an exemption applies. See City of Fayetteville v. Edmark, 304 Ark. 179 (1990).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

Even if portions of the requested records contain exempt information, the FOIA requires that all reasonably segregable, non-exempt material be disclosed. A blanket denial is impermissible when redaction is feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with appropriate redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file suit in circuit court pursuant to Ark. Code Section 25-19-107. Please be advised that under Section 25-19-107(d), a court shall award reasonable attorney's fees and litigation costs to a requester who substantially prevails. Courts review withholdings de novo and may conduct in camera inspection of the disputed records.

I would prefer to resolve this matter cooperatively and hope your agency will take this opportunity to reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Arkansas. No administrative appeal; sole remedy is suit in circuit court under Ark. Code Section 25-19-107. Mandatory attorney fee award to substantially prevailing requester under Section 25-19-107(d). De novo review. Liberal construction mandate in Section 25-19-102.',
    },

    # =========================================================================
    # ARIZONA
    # A.R.S. Section 39-121.02 (Arizona Public Records Law)
    # =========================================================================
    {
        'jurisdiction': 'AZ',
        'record_type': 'appeal',
        'template_name': 'Arizona -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Public Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under Arizona's public records law, A.R.S. Section 39-121 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

Arizona's public records law is rooted in the state constitution. Article II, Section 3 of the Arizona Constitution guarantees that public records "shall be open to inspection by any person at all reasonable times." The Arizona Supreme Court has held that this right is to be construed broadly and that exemptions are disfavored. See Carlson v. Pima County, 141 Ariz. 487, 687 P.2d 1242 (1984).

The burden of demonstrating that records fall within a recognized exemption rests on the custodian. Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

Arizona law does not permit blanket withholding. If any portion of a record is exempt, the custodian must redact the exempt material and produce the remainder. See Phoenix Newspapers, Inc. v. Ellis, 215 Ariz. 268 (App. 2007).

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file a special action in superior court pursuant to A.R.S. Section 39-121.02. Please be advised that under Section 39-121.02(B), a court shall award reasonable attorney's fees and other litigation costs to a person who brings a successful special action to enforce the public records law. Courts review the matter de novo and may inspect records in camera.

I would prefer to resolve this matter without litigation and hope your agency will reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Arizona. No administrative appeal; the remedy is a special action in superior court under A.R.S. Section 39-121.02. Mandatory attorney fees for successful enforcement actions under Section 39-121.02(B). Constitutional basis in Art. II, Sec. 3. De novo review with in camera inspection.',
    },

    # =========================================================================
    # COLORADO
    # C.R.S. Section 24-72-204 (Colorado Open Records Act / CORA)
    # =========================================================================
    {
        'jurisdiction': 'CO',
        'record_type': 'appeal',
        'template_name': 'Colorado -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- CORA Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Colorado Open Records Act (CORA), C.R.S. Section 24-72-200.1 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

CORA declares that "all public records shall be open for inspection by any person at reasonable times" and mandates that the Act be liberally construed in favor of disclosure. C.R.S. Section 24-72-201. The custodian bears the burden of establishing that records fall within a specific statutory exception, and any doubts must be resolved in favor of disclosure. See Denver Publishing Co. v. Dreyfus, 520 P.2d 104 (Colo. 1974).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

CORA requires the custodian to produce all reasonably segregable non-exempt portions of records. C.R.S. Section 24-72-204(3)(a). A blanket denial is impermissible when redaction can preserve confidentiality while honoring the right of public access.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with appropriate redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file an application for an order to show cause in the district court pursuant to C.R.S. Section 24-72-204(5). Please be advised that under Section 24-72-204(5), a court may award reasonable attorney's fees and court costs to a requester who substantially prevails. The court will review the denial de novo and may inspect records in camera.

I would prefer to resolve this matter without litigation and hope your agency will reconsider its position.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Colorado. No administrative appeal; the remedy is an application for order to show cause in district court under C.R.S. Section 24-72-204(5). Discretionary attorney fees for substantially prevailing requester. De novo review. Liberal construction mandate in Section 24-72-201.',
    },

    # =========================================================================
    # GEORGIA
    # O.C.G.A. Section 50-18-73 (Georgia Open Records Act)
    # =========================================================================
    {
        'jurisdiction': 'GA',
        'record_type': 'appeal',
        'template_name': 'Georgia -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Open Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Georgia Open Records Act, O.C.G.A. Section 50-18-70 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

Georgia's Open Records Act provides that "public records shall be open for personal inspection and copying" and declares that "the General Assembly finds and declares that the strong public policy of this state is in favor of open government." O.C.G.A. Section 50-18-70(a). Exemptions must be narrowly construed, and the agency bears the burden of demonstrating that the claimed exemption applies. See Napper v. Georgia Television Co., 257 Ga. 156 (1987).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

The Open Records Act requires that when a record contains both exempt and non-exempt material, the agency must produce the non-exempt portions after redacting the exempt information. A blanket denial is impermissible when segregation is feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within ten (10) days of the date of this letter.

If the records are not produced within this period, I intend to file an action in superior court pursuant to O.C.G.A. Section 50-18-73. Please be advised that under Section 50-18-73(b), a court shall award reasonable attorney's fees and litigation costs to a requester who substantially prevails. Additionally, under Section 50-18-74, a public officer who knowingly and willfully fails to comply with the Open Records Act is subject to civil penalties of up to $1,000 for each violation, and criminal penalties for intentional violations. The court will conduct a de novo review and may inspect records in camera.

I would prefer to resolve this matter without litigation and strongly encourage your agency to reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Georgia. No administrative appeal; the remedy is suit in superior court under O.C.G.A. Section 50-18-73. Mandatory attorney fees for substantially prevailing requester under Section 50-18-73(b). Civil penalties up to $1,000 per violation under Section 50-18-74. Criminal penalties for intentional violations. 10-day demand deadline (Georgia has fast statutory response times).',
    },

    # =========================================================================
    # IDAHO
    # Idaho Code Section 74-115 (Idaho Public Records Act)
    # =========================================================================
    {
        'jurisdiction': 'ID',
        'record_type': 'appeal',
        'template_name': 'Idaho -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Public Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Idaho Public Records Act, Idaho Code Section 74-101 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

The Idaho Public Records Act declares that "[e]very person has a right to examine and take a copy of any public record," Idaho Code Section 74-102(1), and mandates that the Act "shall be liberally construed and the exemptions from disclosure narrowly construed to promote maximum access." Idaho Code Section 74-102(1). The burden of justifying nondisclosure rests entirely on the public agency. See Dalton v. Idaho Dairy Products Commission, 107 Idaho 6 (1984).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

The Act requires that if a record contains both exempt and non-exempt material, the non-exempt portions must be produced after redaction of the exempt information. Idaho Code Section 74-113. A blanket denial is not permissible when segregation is feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file a petition for enforcement in the district court pursuant to Idaho Code Section 74-115. Please be advised that under Section 74-115(2), a court shall award reasonable attorney's fees, witness fees, and other reasonable expenses of litigation to a requester who substantially prevails. The court will conduct a de novo review and may inspect the disputed records in camera.

I would prefer to resolve this matter without litigation and hope your agency will take this opportunity to reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Idaho. No administrative appeal; the remedy is a petition in district court under Idaho Code Section 74-115. Mandatory attorney fees for substantially prevailing requester under Section 74-115(2). Liberal construction mandate in Section 74-102(1). Segregability required under Section 74-113.',
    },

    # =========================================================================
    # KANSAS
    # K.S.A. Section 45-222 (Kansas Open Records Act / KORA)
    # =========================================================================
    {
        'jurisdiction': 'KS',
        'record_type': 'appeal',
        'template_name': 'Kansas -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- KORA Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Kansas Open Records Act (KORA), K.S.A. Section 45-215 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

KORA establishes that "[i]t is declared to be the public policy of the state that public records shall be open for inspection by any person unless otherwise provided by this act." K.S.A. Section 45-216(a). Exemptions are to be strictly construed in favor of disclosure. The custodian bears the burden of establishing that the records fall within a specific statutory exemption, and must cite the particular provision of law relied upon. K.S.A. Section 45-218(d).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

KORA requires that if a record contains both open and closed information, the agency must separate and disclose the open portions. K.S.A. Section 45-221(a). A blanket denial is impermissible when segregation is feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with appropriate redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file suit in district court pursuant to K.S.A. Section 45-222. Please be advised that under Section 45-222(c), a court shall award reasonable attorney's fees and court costs to a requester who substantially prevails. Additionally, under Section 45-223, any public officer or employee who knowingly violates KORA may be subject to civil penalties and removal from office. The court will review the denial de novo and may inspect records in camera.

I would prefer to resolve this matter without litigation and hope your agency will reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Kansas. No administrative appeal; the remedy is suit in district court under K.S.A. Section 45-222. Mandatory attorney fees for substantially prevailing requester under Section 45-222(c). Civil penalties and potential removal from office under Section 45-223. Segregability required under Section 45-221(a).',
    },

    # =========================================================================
    # LOUISIANA
    # La. R.S. 44:35 (Louisiana Public Records Act)
    # =========================================================================
    {
        'jurisdiction': 'LA',
        'record_type': 'appeal',
        'template_name': 'Louisiana -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Public Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Louisiana Public Records Act, La. R.S. 44:1 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

The Louisiana Constitution, Article XII, Section 3, guarantees that "[n]o person shall be denied the right to ... examine public documents, except in cases established by law." The Public Records Act further declares that "[p]roviding access to public records is a responsibility and duty of the appointive or elective office of every public body." La. R.S. 44:31(A). Louisiana courts have consistently held that the Act is to be liberally construed in favor of access and that exemptions are narrowly interpreted. See Title Research Corp. v. Rausch, 450 So. 2d 933 (La. 1984).

The custodian bears the burden of establishing that records fall within a specific statutory exemption. Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

The Public Records Act requires that when a record contains both exempt and non-exempt information, the custodian must separate and produce the non-exempt portions. La. R.S. 44:32(C). A blanket denial is impermissible when segregation and redaction are feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within ten (10) days of the date of this letter.

If the records are not produced within this period, I intend to file suit in district court pursuant to La. R.S. 44:35. Please be advised that under La. R.S. 44:35(E), a court shall award reasonable attorney's fees and other costs of litigation to a requester who prevails. Additionally, under La. R.S. 44:35(E), a custodian who unreasonably or arbitrarily fails to comply may be subject to civil penalties of up to $100 per day. Courts may also issue injunctive or declaratory relief and conduct in camera inspection of withheld records.

I would prefer to resolve this matter without litigation and hope your agency will take this opportunity to reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Louisiana. No administrative appeal; the remedy is suit in district court under La. R.S. 44:35. Mandatory attorney fees for prevailing requester. Civil penalties up to $100/day for arbitrary noncompliance. Constitutional right of access in Art. XII, Sec. 3. Segregability under La. R.S. 44:32(C). 10-day demand deadline (Louisiana has short statutory response times).',
    },

    # =========================================================================
    # MISSISSIPPI
    # Miss. Code Section 25-61-13 (Mississippi Public Records Act)
    # =========================================================================
    {
        'jurisdiction': 'MS',
        'record_type': 'appeal',
        'template_name': 'Mississippi -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Public Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the Mississippi Public Records Act, Miss. Code Section 25-61-1 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

Mississippi's Public Records Act provides that "[a]ll public records are hereby declared to be public property" and that "any person shall have the right to inspect, copy, or mechanically reproduce ... any public record." Miss. Code Section 25-61-5. The Mississippi Ethics Commission has advised that the Act should be liberally construed to maximize public access. The custodian bears the burden of proving that a specific statutory exemption applies. See Mississippi Department of Wildlife, Fisheries & Parks v. Mississippi Wildlife Enforcement Officers' Ass'n, 740 So. 2d 925 (Miss. 1999).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

When a record contains both exempt and non-exempt material, the custodian must redact the exempt portions and produce the remainder. A blanket denial is impermissible when segregation is feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file suit in chancery court pursuant to Miss. Code Section 25-61-13. Please be advised that under Section 25-61-15, a court may award reasonable attorney's fees and litigation costs to a requester who substantially prevails. Additionally, a public official who denies access without a reasonable basis may be subject to penalties. The court will review the denial and may inspect records in camera.

I would prefer to resolve this matter without litigation and hope your agency will reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Mississippi. No administrative appeal; the remedy is suit in chancery court under Miss. Code Section 25-61-13. Discretionary attorney fees under Section 25-61-15. Enforcement through the Mississippi Ethics Commission is also available for complaints but has no binding authority. Burden on custodian to justify exemption.',
    },

    # =========================================================================
    # MONTANA
    # Mont. Code Section 2-6-110 (Montana Constitution Art. II, Sec. 9)
    # =========================================================================
    {
        'jurisdiction': 'MT',
        'record_type': 'appeal',
        'template_name': 'Montana -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Public Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under Montana's constitutional and statutory right of access to public records. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a written request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

Montana provides one of the strongest constitutional guarantees of public access to government records in the nation. Article II, Section 9 of the Montana Constitution provides that "[n]o person shall be deprived of the right to examine documents ... of all public bodies or agencies of state government and its subdivisions." This right is self-executing and requires no implementing legislation. See Great Falls Tribune v. Montana Public Service Commission, 319 Mont. 38, 82 P.3d 876 (2003).

Mont. Code Section 2-6-102 further provides that "[e]very person has a right to examine and take a copy of any public writings of this state." Exemptions must be established by a specific constitutional provision or statute that explicitly restricts disclosure, and they are construed narrowly. The burden of justifying nondisclosure rests on the agency. See Yellowstone County v. Billings Gazette, 365 Mont. 534 (2012).

Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

When a record contains both exempt and non-exempt material, the agency must segregate and produce all non-exempt portions. A blanket denial is impermissible when redaction is feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file an action in district court pursuant to Mont. Code Section 2-6-110. Please be advised that under Section 2-6-110, a court may award costs, including reasonable attorney's fees, to a requester who prevails. Given the constitutional status of the right of access in Montana, courts apply heightened scrutiny to agency denials and may inspect records in camera.

I would prefer to resolve this matter without litigation and hope your agency will take this opportunity to reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for Montana. No administrative appeal; the remedy is suit in district court under Mont. Code Section 2-6-110. Discretionary attorney fees. Montana has one of the strongest constitutional right-to-know provisions in the country (Art. II, Sec. 9), which is self-executing. Courts apply strict scrutiny to restrictions on access.',
    },

    # =========================================================================
    # NORTH CAROLINA
    # N.C.G.S. Section 132-9 (North Carolina Public Records Act)
    # =========================================================================
    {
        'jurisdiction': 'NC',
        'record_type': 'appeal',
        'template_name': 'North Carolina -- Pre-Litigation Demand for Records Disclosure',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

{{custodian_name_or_title}}
{{agency_name}}
{{agency_address}}

Re: Pre-Litigation Demand -- Public Records Request Dated {{original_request_date}}
Reference No. {{request_number}}

Dear {{custodian_name_or_title}}:

I write regarding your agency's denial, dated {{denial_date}}, of my public records request submitted on {{original_request_date}} under the North Carolina Public Records Act, N.C.G.S. Section 132-1 et seq. This letter constitutes a formal demand that your agency reconsider its position and produce the requested records before I pursue judicial relief.

BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following records:

{{description_of_records}}

On {{denial_date}}, your agency denied this request, citing the following basis:

{{denial_basis}}

LEGAL ANALYSIS

North Carolina's Public Records Act declares that the "public records and public information compiled by the agencies of North Carolina government or its subdivisions are the property of the people." N.C.G.S. Section 132-1(b). The North Carolina Supreme Court has consistently held that the Act is to be liberally construed in favor of access, and exemptions are to be strictly limited to those created by specific statutory authority. See News & Observer Publishing Co. v. Poole, 330 N.C. 465, 412 S.E.2d 7 (1992).

The burden of establishing that records fall within a statutory exemption rests on the custodian. Your agency's reliance on the cited exemption is misplaced for the following reasons:

{{arguments_for_disclosure}}

When a document contains both public and confidential information, the custodian must segregate and produce the public portions after redacting any genuinely confidential material. A blanket denial is impermissible when segregation is feasible.

DEMAND

I respectfully demand that {{agency_name}} reconsider its denial and produce the requested records, in full or with narrowly tailored redactions, within fifteen (15) days of the date of this letter.

If the records are not produced within this period, I intend to file an action in superior court pursuant to N.C.G.S. Section 132-9. Please be advised that under Section 132-9(c), a court may award reasonable attorney's fees to a substantially prevailing requester. Courts conduct de novo review of the agency's denial and may order in camera inspection of the disputed records. Additionally, the court may issue injunctive relief compelling production and, in cases of willful noncompliance, may hold the custodian in contempt.

I would prefer to resolve this matter without litigation and hope your agency will take this opportunity to reconsider.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Pre-litigation demand letter for North Carolina. No administrative appeal; the remedy is suit in superior court under N.C.G.S. Section 132-9. Discretionary attorney fees for substantially prevailing requester under Section 132-9(c). Liberal construction mandate. Records are declared property of the people under Section 132-1(b). De novo review with in camera inspection.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for t in TEMPLATES:
            existing = conn.execute(
                "SELECT id FROM request_templates WHERE jurisdiction=? AND record_type='appeal'",
                (t['jurisdiction'],)
            ).fetchone()

            if existing:
                print(f"  {t['jurisdiction']}: appeal template already exists, skipping")
                skipped += 1
                continue

            conn.execute('''
                INSERT INTO request_templates (
                    jurisdiction, record_type, template_name,
                    template_text, fee_waiver_language, expedited_language,
                    notes, source
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 'prdb-built')
            ''', (t['jurisdiction'], t['record_type'], t['template_name'],
                  t['template_text'], t.get('fee_waiver_language'),
                  t.get('expedited_language'), t.get('notes')))
            print(f"  {t['jurisdiction']}: inserted appeal template")
            added += 1

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'\nAppeal templates (batch 1): {added} added, {skipped} skipped, {errors} errors')
    write_receipt(script='build_appeal_templates_batch1', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
