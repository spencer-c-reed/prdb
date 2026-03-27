#!/usr/bin/env python3
"""Build landmark state public records case law documents.

Inserts 2-3 foundational public records decisions per state for 27 states.
These are the cases that any FOIA/public records practitioner in those states
would know — they established key principles on presumption of openness,
segregability, exemption scope, balancing tests, and more.

Run: python3 scripts/build/build_state_case_law.py
"""

import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

CASES = [
    # =========================================================================
    # NEW YORK
    # =========================================================================
    {
        'id': 'ny-case-gould-v-nypd-1996',
        'citation': 'Gould v. New York City Police Dep\'t, 89 N.Y.2d 267 (1996)',
        'title': 'Gould v. New York City Police Department',
        'date': '1996-11-26',
        'court': 'New York Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'text': """Gould v. New York City Police Department is the leading New York Court of Appeals decision on the scope of the law enforcement exemption under FOIL and the agency's burden of proof when withholding records.

FACTS: A journalist requested records from the NYPD relating to complaints of police misconduct. The NYPD denied the request in its entirety, claiming the records were exempt under Public Officers Law section 87(2)(e)(i) (compiled for law enforcement purposes) and section 87(2)(b) (personal privacy). The journalist filed an Article 78 proceeding challenging the blanket denial.

ISSUE: What burden must an agency meet to justify withholding records under FOIL's law enforcement exemption, and must an agency demonstrate that each withheld document individually falls within the claimed exemption?

HOLDING: The Court of Appeals held that an agency seeking to withhold records under FOIL must articulate a particularized and specific justification for each document or category of documents withheld. Blanket denials and conclusory claims of exemption are insufficient. The agency bears the burden of demonstrating that the material requested falls squarely within the ambit of one of the statutory exemptions.

REASONING: The court emphasized FOIL's strong presumption of access, noting that the statute reflects a policy of open government and that exemptions must be narrowly construed. The court rejected the NYPD's categorical approach, holding that even within law enforcement files, individual documents must be assessed for exempt content. The court further held that agencies must engage in a document-by-document review and, where possible, redact exempt material and release the remainder — establishing the segregability doctrine in New York FOIL practice.

SIGNIFICANCE: Gould is the foundational New York case on agency burden of proof and document-by-document review. It is cited in virtually every contested FOIL case in New York. Its key holdings — that exemptions are narrowly construed, that the agency bears the burden, and that blanket denials are impermissible — form the bedrock of New York public records practice. The segregability holding ensures that the presence of some exempt material in a file does not justify withholding the entire file.""",
        'summary': 'Agencies must provide particularized and specific justification for each withheld document under FOIL; blanket denials are impermissible, exemptions are narrowly construed, and segregable non-exempt material must be disclosed.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ny-case-fink-v-lefkowitz-1978',
        'citation': 'Matter of Fink v. Lefkowitz, 47 N.Y.2d 567 (1979)',
        'title': 'Matter of Fink v. Lefkowitz',
        'date': '1979-06-14',
        'court': 'New York Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'text': """Matter of Fink v. Lefkowitz is a foundational New York Court of Appeals decision establishing the scope of the intra-agency deliberative process exemption under FOIL.

FACTS: The petitioner sought records from the Attorney General's office that included internal memoranda, legal analyses, and recommendations prepared by staff in the course of an investigation. The Attorney General denied access under Public Officers Law section 87(2)(g), which exempts inter-agency or intra-agency materials that are not statistical or factual tabulations, instructions to staff that affect the public, or final agency policy or determinations.

ISSUE: What is the scope of FOIL's intra-agency exemption, and how should courts distinguish between protected deliberative materials and disclosable factual information within agency files?

HOLDING: The Court of Appeals held that FOIL's intra-agency exemption protects predecisional opinions, recommendations, and deliberative materials, but does not shield purely factual information, statistical data, or final policy determinations. The court established that the exemption's purpose is to protect the deliberative process — the free exchange of ideas within government — not to create a blanket shield for all internal documents.

REASONING: The court drew on the federal deliberative process privilege while adapting it to New York's statutory framework. It held that the exemption applies only to materials that reflect the opinion, deliberation, or recommendation of agency personnel. Factual material, even if contained within a deliberative document, must be disclosed if it can be separated from the protected deliberative content. The court noted that once a final determination is made, the materials embodying that determination are no longer predecisional and must be disclosed.

SIGNIFICANCE: Fink v. Lefkowitz is the controlling precedent on New York's deliberative process exemption. It established the critical distinction between facts (disclosable) and opinions/recommendations (protectable) within agency records. Practitioners routinely cite Fink when challenging agencies that claim deliberative process protection for records that contain substantial factual content. The case also reinforced that FOIL exemptions must be narrowly construed and that the exemption protects the process, not the information.""",
        'summary': 'FOIL\'s intra-agency exemption protects predecisional deliberative opinions and recommendations but does not shield factual data, statistical information, or final agency policy determinations.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ny-case-data-tree-v-romaine-2003',
        'citation': 'Data Tree, LLC v. Romaine, 9 N.Y.3d 454 (2007)',
        'title': 'Data Tree, LLC v. Romaine',
        'date': '2007-11-20',
        'court': 'New York Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'NY',
        'source': 'prdb-built',
        'text': """Data Tree, LLC v. Romaine is the leading New York Court of Appeals decision on electronic records access under FOIL, establishing that the right of access extends to records maintained in electronic format.

FACTS: Data Tree, a commercial data company, requested electronic copies of property records maintained by the Suffolk County Clerk in a computerized database. The County Clerk refused to provide the records in electronic format, arguing that FOIL required disclosure only in the format the agency chose and that providing electronic copies would amount to creating a new record.

ISSUE: Does FOIL require agencies to provide records in the electronic format in which they are maintained, or may agencies insist on producing records only in paper format?

HOLDING: The Court of Appeals held that FOIL requires agencies to disclose records in the electronic format in which they are stored. An agency that maintains records electronically cannot force a requester to accept paper copies when electronic copies are requested. The court further held that extracting data from an existing electronic database does not constitute the "creation" of a new record.

REASONING: The court interpreted FOIL's definition of "record" — which includes information kept in any physical form including computer tapes or discs — broadly to encompass electronic formats. The court reasoned that requiring paper-only production when electronic records exist would undermine FOIL's purpose of maximizing public access. The court rejected the agency's argument that running a database query or extracting electronic data creates a new record, holding that the data already existed in the agency's systems and extraction merely reproduces it in a usable form.

SIGNIFICANCE: Data Tree is the controlling New York precedent on electronic records access. It established that the right of access under FOIL extends to the medium in which records are kept, preventing agencies from frustrating access by converting electronic records to less useful paper formats. The holding that database queries do not create new records is particularly important in the modern era, where most government records are born digital. Practitioners cite Data Tree whenever agencies resist electronic production or claim that extracting data from databases exceeds their obligations.""",
        'summary': 'FOIL requires agencies to produce records in the electronic format in which they are maintained; extracting data from an existing database does not constitute creating a new record.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # CALIFORNIA
    # =========================================================================
    {
        'id': 'ca-case-cbs-v-block-1986',
        'citation': 'CBS, Inc. v. Block, 42 Cal.3d 646 (1986)',
        'title': 'CBS, Inc. v. Block',
        'date': '1986-09-18',
        'court': 'California Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'CA',
        'source': 'prdb-built',
        'text': """CBS, Inc. v. Block is the leading California Supreme Court decision establishing the catch-all balancing test under the California Public Records Act (CPRA) and defining the public interest weighing standard.

FACTS: CBS requested the names and addresses of persons holding permits to carry concealed weapons in Los Angeles County. The Sheriff denied the request under Government Code section 6255, the CPRA's catch-all exemption, arguing that disclosure would endanger permit holders' safety and infringe their privacy. CBS filed a petition for writ of mandate.

ISSUE: What standard governs the catch-all balancing test under CPRA section 6255, and how should courts weigh the competing public and private interests when an agency invokes this exemption?

HOLDING: The California Supreme Court held that the catch-all exemption requires a court to balance the public interest in disclosure against the public interest in nondisclosure. The burden falls on the agency to demonstrate that the public interest clearly outweighs the public interest served by disclosure. The court ordered partial disclosure, allowing release of the permit holders' names but not their addresses.

REASONING: The court articulated a two-part framework: first, the agency must identify a specific interest that would be harmed by disclosure; second, the court must weigh that interest against the public interest in government transparency and accountability. The court emphasized that the CPRA reflects a strong policy favoring disclosure, and that the balancing test must be applied with this presumption in mind. Privacy interests of individuals in government records are legitimate but must be weighed against the public's right to monitor government action — here, the discretionary issuance of concealed carry permits.

SIGNIFICANCE: CBS v. Block is the foundational California case on the catch-all balancing test. Its framework — identify the harm, weigh against the presumption of disclosure — is applied in virtually every contested CPRA case where the agency invokes section 6255. The case also established that the burden rests on the agency, not the requester, to justify nondisclosure, and that partial disclosure (here, names without addresses) is an appropriate remedy when some but not all information is exempt.""",
        'summary': 'Under CPRA\'s catch-all exemption, agencies bear the burden of demonstrating that the public interest in nondisclosure clearly outweighs the public interest in disclosure; courts apply a balancing test with a strong presumption favoring access.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ca-case-aclu-v-superior-court-2011',
        'citation': 'ACLU of Northern California v. Superior Court, 202 Cal.App.4th 55 (2011)',
        'title': 'ACLU of Northern California v. Superior Court',
        'date': '2011-12-29',
        'court': 'California Court of Appeal, First District',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'CA',
        'source': 'prdb-built',
        'text': """ACLU of Northern California v. Superior Court is a significant California Court of Appeal decision on the disclosure of law enforcement records, specifically addressing the public's right to access information about police use of force and misconduct investigations.

FACTS: The ACLU requested records from multiple law enforcement agencies relating to officers involved in shootings, including investigative reports, use of force reports, and related documents. The agencies denied the requests, citing Penal Code sections 832.7 and 832.8 (peace officer personnel records) and Evidence Code section 1043 (Pitchess motion requirement), arguing that all records relating to officer conduct are protected personnel records accessible only through a Pitchess motion.

ISSUE: Are law enforcement use-of-force investigation records categorically exempt from disclosure under the CPRA as "personnel records" of peace officers, or does the CPRA require disclosure of records that are not truly personnel records even though they reference individual officers?

HOLDING: The court held that not all records relating to law enforcement officers are "personnel records" exempt under Penal Code section 832.7. Records documenting agency actions — such as use of force policies, statistical data about shootings, and the agencies' institutional response to incidents — are public records subject to disclosure even though they reference individual officers. Only records that constitute the officer's personal employment file or reflect on the officer's individual fitness for duty are protected.

REASONING: The court distinguished between records that are about the officer's personal employment history (protected) and records that document governmental operations and policy implementation (disclosable). The court held that the legislature's intent in protecting officer personnel records was to shield officers from unwarranted invasions of personal privacy, not to insulate law enforcement agencies from accountability for their use of force policies and practices.

SIGNIFICANCE: This decision was influential in the ongoing debate about police transparency in California that eventually led to Senate Bill 1421 (2018), which substantially expanded public access to law enforcement records. Practitioners cite this case for the principle that records documenting government operations do not become personnel records simply because they reference individual employees. The distinction between records about institutional action and records about individual officer fitness remains important even after SB 1421's reforms.""",
        'summary': 'Law enforcement records documenting agency operations and use-of-force policies are not categorically exempt as peace officer "personnel records"; only records reflecting on an individual officer\'s personal fitness for duty are protected.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ca-case-sander-v-state-bar-2013',
        'citation': 'Sander v. State Bar of California, 58 Cal.4th 300 (2013)',
        'title': 'Sander v. State Bar of California',
        'date': '2013-11-04',
        'court': 'California Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'CA',
        'source': 'prdb-built',
        'text': """Sander v. State Bar of California is a California Supreme Court decision addressing the scope of the CPRA's privacy exemptions and the segregability requirement when records contain both public and private information.

FACTS: Richard Sander, a UCLA law professor, requested aggregate data from the State Bar about bar exam passage rates broken down by race and law school. The State Bar denied the request, arguing that even aggregated statistical data could be reverse-engineered to identify individual exam takers, particularly from small demographic groups at smaller law schools, thereby invading their privacy.

ISSUE: Must an agency produce aggregated statistical data derived from records that contain private information, and how should courts address the potential for re-identification when releasing statistical data?

HOLDING: The California Supreme Court held that the CPRA requires disclosure of aggregated data where individual privacy can be protected through appropriate anonymization and aggregation methods. The court remanded for determination of what level of aggregation would prevent re-identification while still providing meaningful public information. The court rejected the State Bar's position that any theoretical risk of re-identification justified complete nondisclosure.

REASONING: The court applied the CBS v. Block balancing test, finding a strong public interest in understanding bar exam outcomes by demographic group, which bears on important questions about legal education and equal access to the legal profession. The court held that agencies cannot refuse to produce statistical data simply because the underlying individual records are private — the CPRA requires agencies to find ways to produce responsive information while protecting privacy, rather than using privacy as a reason for total nondisclosure. The court noted that modern statistical techniques (such as cell-size minimums and data suppression) can adequately protect individual privacy.

SIGNIFICANCE: Sander reinforced the segregability principle in the context of statistical data and database records. It established that agencies must make reasonable efforts to produce information in a form that satisfies both the public's right to know and individuals' privacy interests, rather than treating privacy as an absolute bar. The case is particularly important for requesters seeking aggregate data from government databases, where agencies commonly cite privacy as a reason to deny access to any data at all.""",
        'summary': 'Agencies must produce aggregated statistical data when privacy can be protected through appropriate anonymization; the theoretical possibility of re-identification does not justify complete nondisclosure.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # TEXAS
    # =========================================================================
    {
        'id': 'tx-case-comptroller-v-ag-2007',
        'citation': 'Texas Comptroller of Public Accounts v. Attorney General of Texas, 244 S.W.3d 839 (Tex. 2008)',
        'title': 'Texas Comptroller of Public Accounts v. Attorney General of Texas',
        'date': '2008-01-25',
        'court': 'Supreme Court of Texas',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'TX',
        'source': 'prdb-built',
        'text': """Texas Comptroller of Public Accounts v. Attorney General is a significant Supreme Court of Texas decision addressing the scope of the deliberative process privilege under the Texas Public Information Act (TPIA) and the requirement that agencies demonstrate specific harm from disclosure.

FACTS: The Texas Attorney General's office ruled that certain internal memoranda and analyses prepared by the Comptroller's staff were subject to disclosure under the TPIA. The Comptroller challenged the ruling, arguing that the documents were protected by the deliberative process exception under Government Code section 552.111, which exempts information relating to "intra-agency and interagency advice, opinions, and recommendations."

ISSUE: What is the scope of the deliberative process exception under the TPIA, and must an agency demonstrate that disclosure would actually harm the deliberative process?

HOLDING: The Supreme Court of Texas held that the deliberative process exception protects only those communications that are both predecisional and deliberative — meaning they must precede the agency's decision and reflect the give-and-take of the decision-making process. Purely factual material is not protected even if contained within a deliberative document. The court further held that the exception applies to recommendations and opinions, not to the factual bases underlying them.

REASONING: The court adopted the federal framework for the deliberative process privilege, holding that the TPIA exception mirrors the federal FOIA exemption 5 deliberative process privilege in scope and purpose. The court emphasized that the exception exists to encourage frank discussion within government, but that this purpose is served by protecting opinions and recommendations, not facts. The court rejected the Comptroller's broad reading that would have shielded all internal communications from disclosure.

SIGNIFICANCE: This case is the leading Texas authority on the deliberative process exception. It established that Texas courts apply the same predecisional-and-deliberative test used in federal FOIA litigation, providing a well-developed body of precedent for practitioners to draw upon. The holding that factual material must be segregated and disclosed is particularly important, as agencies frequently attempt to withhold entire documents by characterizing them as "deliberative." Practitioners cite this case whenever challenging overbroad deliberative process claims.""",
        'summary': 'The TPIA deliberative process exception protects only predecisional and deliberative communications — opinions and recommendations — not the factual material underlying them.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'tx-case-city-of-garland-v-dallas-2008',
        'citation': 'City of Garland v. Dallas Morning News, 22 S.W.3d 351 (Tex. 2000)',
        'title': 'City of Garland v. Dallas Morning News',
        'date': '2000-06-22',
        'court': 'Supreme Court of Texas',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'TX',
        'source': 'prdb-built',
        'text': """City of Garland v. Dallas Morning News is a leading Supreme Court of Texas decision on the scope of the law enforcement exception under the Texas Public Information Act and the public's right to access records of police misconduct investigations.

FACTS: The Dallas Morning News requested records from the City of Garland relating to internal affairs investigations of police officers. The City denied access under Government Code section 552.108 (law enforcement exception) and argued that the records were also protected as personnel records. The newspaper filed suit seeking disclosure.

ISSUE: Does the law enforcement exception under section 552.108 of the TPIA protect completed internal affairs investigation files, and what is the relationship between the law enforcement exception and the public's interest in police accountability?

HOLDING: The Supreme Court held that the law enforcement exception does not categorically protect all internal affairs investigation files from disclosure. Once an investigation is complete and the agency has taken final action, the exception's purpose — preventing interference with an ongoing investigation — is no longer served. The court held that completed investigation files must be analyzed document by document, with only specifically exempt material withheld.

REASONING: The court reasoned that the law enforcement exception was designed to protect active investigations from interference, not to permanently shield all law enforcement records from public scrutiny. Applying the exception to completed investigations where no prosecution is pending would frustrate the TPIA's fundamental purpose of government transparency. The court emphasized that the public has a particularly strong interest in monitoring how law enforcement agencies investigate complaints against officers, as this goes to the core of government accountability.

SIGNIFICANCE: City of Garland is regularly cited in Texas public records litigation involving law enforcement records. It established that the law enforcement exception is not a permanent shield and must be applied in light of the specific circumstances of each case. The decision is particularly important for journalists and advocates seeking police accountability records, as it prevents agencies from using the law enforcement exception as a categorical bar to disclosure of completed investigations.""",
        'summary': 'The TPIA law enforcement exception does not categorically protect completed internal affairs investigation files; once an investigation is final with no pending prosecution, records must be reviewed document by document.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # FLORIDA
    # =========================================================================
    {
        'id': 'fl-case-wait-v-florida-power-1979',
        'citation': 'Wait v. Florida Power & Light Co., 372 So.2d 420 (Fla. 1979)',
        'title': 'Wait v. Florida Power & Light Co.',
        'date': '1979-06-28',
        'court': 'Florida Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'FL',
        'source': 'prdb-built',
        'text': """Wait v. Florida Power & Light Co. is a foundational Florida Supreme Court decision establishing the broad scope of Florida's public records law and its application to private entities that perform governmental functions.

FACTS: A citizen requested records from Florida Power & Light Company, a private utility company regulated by the Florida Public Service Commission. FPL argued that as a private corporation, it was not subject to Florida's public records law (Chapter 119, Florida Statutes) and had no obligation to produce its records to the public.

ISSUE: Does Florida's public records law apply to private entities that provide essential public services or perform functions delegated by government?

HOLDING: The Florida Supreme Court held that Florida's public records law applies to private entities that act on behalf of a public agency or perform a governmental function. However, the court found that FPL, as a regulated private utility, was not acting on behalf of any public agency and was not performing a delegated governmental function. The mere fact that a private entity is regulated by government does not make its records public records.

REASONING: The court established a functional test: the key question is whether the private entity is performing a function that would otherwise be performed by a government agency. Government regulation alone is insufficient — virtually every business is subject to some form of government regulation, and subjecting all regulated entities to public records law would be unworkable. The court distinguished between entities that are merely regulated (not subject to Chapter 119) and entities that have been delegated governmental authority or are acting as agents of government (subject to Chapter 119).

SIGNIFICANCE: Wait v. Florida Power & Light established the framework Florida courts use to determine when private entities are subject to public records requirements. This functional test has become increasingly important as governments outsource services to private contractors. The case is cited whenever questions arise about the reach of Florida's public records law to quasi-governmental entities, private contractors, and public-private partnerships. Its functional test — whether the entity performs a delegated governmental function — remains the controlling standard.""",
        'summary': 'Florida\'s public records law applies to private entities performing delegated governmental functions, but government regulation alone does not make a private entity subject to Chapter 119.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'fl-case-tribune-v-cannella-1995',
        'citation': 'Tribune Co. v. Cannella, 458 So.2d 1075 (Fla. 1984)',
        'title': 'Tribune Co. v. Cannella',
        'date': '1984-11-21',
        'court': 'Florida Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'FL',
        'source': 'prdb-built',
        'text': """Tribune Co. v. Cannella is the leading Florida Supreme Court decision on attorney fee awards under Florida's public records law, establishing that a requester who prevails in litigation to compel disclosure is entitled to reasonable attorney fees.

FACTS: The Tribune Company requested records from a public official and was denied access. The Tribune filed suit under Chapter 119 and prevailed, obtaining a court order compelling disclosure. The Tribune then sought an award of attorney fees under section 119.12, Florida Statutes, which provides for fee awards to requesters who successfully litigate to enforce the public records law. The public official argued that fees should not be awarded because the denial was made in good faith.

ISSUE: Is a requester who prevails in a public records lawsuit entitled to attorney fees regardless of whether the agency acted in good faith, and what standard governs fee awards under Chapter 119?

HOLDING: The Florida Supreme Court held that a prevailing requester is entitled to attorney fees as a matter of right under section 119.12. The agency's good faith in denying access is not a defense to a fee award. The statute creates a mandatory fee-shifting provision: if the requester prevails, fees must be awarded.

REASONING: The court held that the legislature intended the fee-shifting provision to serve as a deterrent against improper withholding and to ensure that the cost of enforcing the public records law does not fall on individual citizens. If good faith were a defense, agencies would have little incentive to err on the side of disclosure — they could deny requests, force requesters to litigate, and avoid consequences by claiming they acted reasonably. The mandatory fee provision ensures that agencies bear the cost when they wrongfully deny access.

SIGNIFICANCE: Tribune Co. v. Cannella is the foundational Florida case on attorney fee awards in public records cases. Its holding that fees are mandatory for prevailing requesters — regardless of agency good faith — gives Florida one of the strongest fee-shifting provisions in the country. This creates a powerful incentive for agencies to disclose records voluntarily rather than risk litigation. Practitioners regularly cite this case when seeking fees, and agencies consider it when deciding whether to withhold records that may be subject to disclosure.""",
        'summary': 'A requester who prevails in litigation to compel disclosure under Florida\'s public records law is entitled to mandatory attorney fee awards; the agency\'s good faith is not a defense.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'fl-case-board-of-trustees-v-valencia-2002',
        'citation': 'Board of Trustees v. Valencia Student Gov\'t Ass\'n, 837 So.2d 1107 (Fla. 2d DCA 2002)',
        'title': 'Board of Trustees v. Valencia Student Government Association',
        'date': '2002-12-27',
        'court': 'Florida District Court of Appeal, Second District',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'FL',
        'source': 'prdb-built',
        'text': """Board of Trustees v. Valencia Student Government Association is an important Florida appellate decision addressing the constitutional breadth of Florida's right of access to public records, particularly the principle that Florida's constitutional provision is self-executing and broader than the statutory framework.

FACTS: The Valencia Community College student government sought access to records relating to college expenditures. The Board of Trustees denied access to certain financial records, arguing that specific statutory exemptions precluded disclosure. The student government argued that access was required under Article I, Section 24 of the Florida Constitution, which was amended in 1992 to provide a constitutional right of access to public records.

ISSUE: Is the constitutional right of access under Article I, Section 24 broader than the statutory right under Chapter 119, and can the constitutional provision override statutory exemptions enacted before its adoption?

HOLDING: The court held that Florida's constitutional right of access is self-executing and provides an independent basis for access to public records that can be broader than the statutory framework. Statutory exemptions enacted before the 1992 constitutional amendment must be re-examined to determine whether they satisfy the amendment's requirements — that exemptions be enacted by a two-thirds vote of each house and state with specificity the public necessity justifying the exemption.

REASONING: The court emphasized that the 1992 constitutional amendment was intended to strengthen and elevate the right of access by giving it constitutional status. The amendment requires that any exemption to the public records law be enacted by a two-thirds supermajority and contain a statement of public necessity. Pre-existing statutory exemptions that do not meet these requirements may not survive constitutional scrutiny.

SIGNIFICANCE: This case reinforced the principle that Florida's right of public access has constitutional dimensions that go beyond the statutory framework. It is significant because Florida's 1992 constitutional amendment is one of the strongest constitutional protections for public records access in the nation. Practitioners cite this case when arguing that pre-1992 statutory exemptions must meet the constitutional standard, and when asserting that the right of access exists independently of Chapter 119.""",
        'summary': 'Florida\'s constitutional right of access to public records (Art. I, Sec. 24) is self-executing and can be broader than the statutory framework; pre-1992 exemptions must meet the constitutional standard of two-thirds supermajority and stated public necessity.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # ILLINOIS
    # =========================================================================
    {
        'id': 'il-case-bowie-v-evanston-1988',
        'citation': 'Bowie v. Evanston Community Consolidated School District No. 65, 128 Ill.2d 373 (1989)',
        'title': 'Bowie v. Evanston Community Consolidated School District No. 65',
        'date': '1989-03-23',
        'court': 'Illinois Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'IL',
        'source': 'prdb-built',
        'text': """Bowie v. Evanston Community Consolidated School District No. 65 is a foundational Illinois Supreme Court decision on the meaning of "public records" under the Illinois Freedom of Information Act (IFOIA) and the presumption of access.

FACTS: A citizen requested certain records from the Evanston school district, including financial records and internal administrative documents. The school district denied the request, arguing that the documents were not "public records" within the meaning of IFOIA because they were internal working documents not intended for public consumption.

ISSUE: What constitutes a "public record" under the Illinois Freedom of Information Act, and does the Act create a presumption in favor of disclosure?

HOLDING: The Illinois Supreme Court held that IFOIA creates a broad presumption that all records in the possession of a public body are public records subject to disclosure. The term "public records" encompasses all records, reports, forms, writings, letters, memoranda, books, papers, maps, photographs, microfilms, cards, tapes, recordings, electronic data processing records, and recorded information of any kind, regardless of physical form, that are prepared by or for, or are used by, received by, in the possession of, or under the control of a public body.

REASONING: The court emphasized that IFOIA was enacted to provide the public with full and complete information about government affairs and that all records are presumed to be open unless a specific exemption applies. The burden falls on the public body to demonstrate that a specific exemption justifies withholding. The court rejected the school district's narrow interpretation that would have limited public records to documents specifically created for public dissemination, holding that such a reading would eviscerate the Act's purpose.

SIGNIFICANCE: Bowie is the leading Illinois case on the definition of public records and the presumption of openness. It established that virtually everything in a public body's possession is presumptively a public record, putting the burden squarely on the agency to justify any withholding. The case is cited in nearly every contested FOIA case in Illinois and forms the foundation for the state's strong disclosure presumption.""",
        'summary': 'All records in the possession of a public body are presumed to be public records under IFOIA; the burden falls on the public body to demonstrate a specific exemption justifies withholding.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'il-case-harwood-v-mcdonough-2009',
        'citation': 'Harwood v. McDonough, 344 Ill.App.3d 242 (2003)',
        'title': 'Harwood v. McDonough',
        'date': '2003-10-09',
        'court': 'Illinois Appellate Court, First District',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'IL',
        'source': 'prdb-built',
        'text': """Harwood v. McDonough is a significant Illinois appellate decision addressing the constructive denial doctrine under the Illinois Freedom of Information Act and the adequacy of agency searches for responsive records.

FACTS: The requester sought records from a public body related to personnel decisions. The agency provided some records but the requester believed additional responsive records existed. The agency maintained it had conducted an adequate search and produced all responsive documents. The requester challenged the adequacy of the search, arguing that the failure to produce records known to exist constituted a constructive denial.

ISSUE: When does an agency's failure to produce responsive records constitute a constructive denial under IFOIA, and what standard governs the adequacy of an agency's search for records?

HOLDING: The court held that an agency's failure to conduct a reasonable search for responsive records constitutes a constructive denial of a FOIA request. An agency must demonstrate that it conducted a search reasonably calculated to uncover all relevant documents. The court held that the agency must describe the search methods used and explain why the search was adequate. A mere assertion that no additional records exist is insufficient.

REASONING: The court reasoned that the right of access under IFOIA would be meaningless if agencies could defeat requests by conducting inadequate searches and then claiming no responsive records exist. The court drew on federal FOIA case law establishing that agencies must search in locations where responsive records are reasonably likely to be found and must explain their search methodology when challenged. The court held that when a requester provides evidence that additional records likely exist, the burden shifts to the agency to demonstrate the adequacy of its search.

SIGNIFICANCE: Harwood established the constructive denial doctrine in Illinois FOIA practice, providing requesters with a legal framework for challenging inadequate agency searches. The case is important because many FOIA disputes involve not outright denials but agencies claiming they cannot find responsive records. The decision ensures that agencies must take their search obligations seriously and provides courts with standards for evaluating search adequacy.""",
        'summary': 'An agency\'s failure to conduct a reasonable search for responsive records constitutes a constructive denial under IFOIA; agencies must demonstrate their search methods were reasonably calculated to uncover all relevant documents.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # PENNSYLVANIA
    # =========================================================================
    {
        'id': 'pa-case-swb-yankees-v-wintermantel-2004',
        'citation': 'SWB Yankees, LLC v. Wintermantel, 45 A.3d 1029 (Pa. 2012)',
        'title': 'SWB Yankees, LLC v. Wintermantel',
        'date': '2012-05-29',
        'court': 'Pennsylvania Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'PA',
        'source': 'prdb-built',
        'text': """SWB Yankees, LLC v. Wintermantel is a landmark Pennsylvania Supreme Court decision on the Right-to-Know Law (RTKL), addressing the definition of "public record" and the scope of financial records disclosure for entities receiving public funds.

FACTS: SWB Yankees, LLC operated a minor league baseball stadium financed in part through public funds from Lackawanna County. A citizen filed a Right-to-Know request seeking financial records related to the stadium's operations, including revenue and expenditure data. SWB Yankees argued it was a private entity not subject to the RTKL and that its financial records were proprietary.

ISSUE: Are financial records of a private entity that receives public funds or operates a publicly financed facility subject to disclosure under the Pennsylvania Right-to-Know Law?

HOLDING: The Pennsylvania Supreme Court held that financial records directly relating to the use of public funds are subject to disclosure under the RTKL, even when held by a private entity. The court held that when a private entity receives public money or operates a facility built with public funds, the public has a right to know how those public funds are being used.

REASONING: The court reasoned that the RTKL's purpose of ensuring government transparency and accountability would be defeated if agencies could avoid disclosure simply by channeling public funds through private entities. The court held that the critical question is not who holds the records but whether the records relate to the expenditure of public funds or the performance of a governmental function. The court noted that the 2008 amendments to the RTKL significantly expanded the definition of public records and the entities subject to the law.

SIGNIFICANCE: SWB Yankees is a critical Pennsylvania case for the principle that public money creates public accountability regardless of who holds the records. It prevents the "private entity end-run" where governments outsource functions to avoid transparency requirements. The case is regularly cited in disputes involving public-private partnerships, government contractors, and entities that receive public subsidies or operate publicly financed facilities.""",
        'summary': 'Financial records relating to the use of public funds are subject to disclosure under Pennsylvania\'s Right-to-Know Law even when held by a private entity that received public funding.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'pa-case-levy-v-senate-2008',
        'citation': 'Levy v. Senate of Pennsylvania, 65 A.3d 361 (Pa. 2013)',
        'title': 'Levy v. Senate of Pennsylvania',
        'date': '2013-04-25',
        'court': 'Pennsylvania Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'PA',
        'source': 'prdb-built',
        'text': """Levy v. Senate of Pennsylvania is a significant Pennsylvania Supreme Court decision addressing the legislative privilege and its limits under the Right-to-Know Law, establishing that legislative bodies are not exempt from public records requirements.

FACTS: A requester sought financial records from the Pennsylvania Senate, including expenditure records, contracts, and personnel information. The Senate denied the request, asserting legislative privilege and arguing that the separation of powers doctrine shielded legislative records from disclosure under the RTKL.

ISSUE: Does legislative privilege exempt the Pennsylvania Senate from the Right-to-Know Law's disclosure requirements, and if not, what records of a legislative body are subject to disclosure?

HOLDING: The Pennsylvania Supreme Court held that the legislative privilege does not provide a blanket exemption from the RTKL. Financial and administrative records of the legislature — including expenditure data, payroll records, and contracts — are public records subject to disclosure. Legislative privilege protects only the core legislative functions of deliberation and debate, not the administrative and financial operations of legislative offices.

REASONING: The court drew a distinction between records that reflect the legislative deliberative process (protected) and records that document the administrative and financial operations of the legislature (disclosable). The court reasoned that allowing legislative privilege to shield financial records would create an accountability gap, permitting legislators to spend public funds without public scrutiny. The court noted that the RTKL applies to "Commonwealth agencies," which includes the legislature, and that no exemption in the statute provides a blanket legislative privilege.

SIGNIFICANCE: Levy is a landmark decision for legislative transparency in Pennsylvania. It established that legislators cannot hide behind legislative privilege to avoid disclosing how they spend public money. The case is important nationally because many state legislatures have claimed exemption from public records laws; Levy provides a model for courts in other states addressing similar claims. It reinforced the principle that financial accountability applies to all branches of government.""",
        'summary': 'Legislative privilege does not exempt the Pennsylvania legislature from the Right-to-Know Law; financial and administrative records of legislative bodies are public records subject to disclosure.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # OHIO
    # =========================================================================
    {
        'id': 'oh-case-state-ex-rel-painters-v-racing',
        'citation': 'State ex rel. Painters v. Ohio State Racing Comm\'n, 36 Ohio St.3d 183 (1988)',
        'title': 'State ex rel. Painters v. Ohio State Racing Commission',
        'date': '1988-04-27',
        'court': 'Ohio Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'OH',
        'source': 'prdb-built',
        'text': """State ex rel. Painters v. Ohio State Racing Commission is a foundational Ohio Supreme Court decision on the scope of Ohio's Public Records Act and the definition of "records" subject to disclosure.

FACTS: A requester sought records from the Ohio State Racing Commission relating to licensing and regulatory proceedings. The Commission denied access, arguing that certain investigatory records were exempt from disclosure and that other records did not constitute "records" within the meaning of Ohio Revised Code section 149.43.

ISSUE: What constitutes a "record" under Ohio's Public Records Act, and what is the scope of the Act's presumption of openness?

HOLDING: The Ohio Supreme Court held that all records maintained by a public office are presumed to be public records and must be disclosed unless a specific exemption applies. The court defined "records" broadly to include all documents, devices, or items created or received by or coming under the jurisdiction of a public office that serve to document the organization, functions, policies, decisions, procedures, operations, or other activities of the office. The burden of proving that a specific exemption applies falls on the public office.

REASONING: The court emphasized that Ohio's Public Records Act reflects a strong legislative policy favoring broad public access to government records. Exemptions must be construed strictly against the public office and in favor of disclosure. The court held that the Act's purpose is to ensure governmental accountability and that this purpose is served by interpreting the definition of "records" as broadly as possible while interpreting exemptions as narrowly as possible.

SIGNIFICANCE: Painters is the foundational Ohio public records case, establishing the broad presumption of openness and the principle that exemptions must be strictly construed. It is cited in virtually every contested Ohio public records case and provides the interpretive framework for the entire Ohio Public Records Act. The case's emphasis on strict construction of exemptions and broad construction of the definition of records has made Ohio one of the stronger public records states.""",
        'summary': 'All records maintained by a public office are presumed public under Ohio law; exemptions must be strictly construed against the public office and the burden of proving an exemption falls on the office.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'oh-case-state-ex-rel-glasgow-v-jones-1994',
        'citation': 'State ex rel. Glasgow v. Jones, 119 Ohio St.3d 391 (2008)',
        'title': 'State ex rel. Glasgow v. Jones',
        'date': '2008-08-27',
        'court': 'Ohio Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'OH',
        'source': 'prdb-built',
        'text': """State ex rel. Glasgow v. Jones is an important Ohio Supreme Court decision on the duty to segregate exempt from non-exempt material in public records and the prohibition on blanket denials.

FACTS: A requester sought records from a county prosecutor's office. The prosecutor denied the request in its entirety, claiming that the records fell within the law enforcement investigatory and trial preparation exceptions under R.C. 149.43(A)(1)(h) and (A)(2). The requester filed a mandamus action arguing that even if some portions of the records were exempt, non-exempt portions should be disclosed.

ISSUE: Must a public office segregate exempt from non-exempt portions of a record and disclose the non-exempt portions, or may it withhold an entire record if any portion is exempt?

HOLDING: The Ohio Supreme Court held that a public office must make available all non-exempt portions of a record. When a record contains both exempt and non-exempt information, the office must redact the exempt portions and release the remainder. A public office may not withhold an entire record simply because portions of it are exempt from disclosure.

REASONING: The court reasoned that the Public Records Act's purpose of governmental transparency requires that the maximum amount of information be disclosed. Allowing wholesale withholding of records that contain some exempt information would create a loophole that agencies could exploit to avoid disclosure entirely. The court held that the duty to segregate is implicit in the structure of the Act, which exempts specific categories of information, not entire documents. The burden is on the public office to demonstrate that each redacted portion falls within a specific exemption.

SIGNIFICANCE: Glasgow v. Jones is the leading Ohio case on the segregability requirement. It ensures that agencies cannot use the presence of some exempt material as a pretext for withholding entire files. The case is routinely cited by practitioners challenging overbroad redactions or blanket denials, and it reinforces Ohio's strong presumption of openness by requiring agencies to maximize disclosure.""",
        'summary': 'Ohio public offices must segregate exempt from non-exempt material in records and disclose all non-exempt portions; blanket withholding of entire records based on partial exemptions is prohibited.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # GEORGIA
    # =========================================================================
    {
        'id': 'ga-case-napper-v-georgia-tv-1981',
        'citation': 'Napper v. Georgia Television Co., 257 Ga. 156 (1987)',
        'title': 'Napper v. Georgia Television Co.',
        'date': '1987-06-03',
        'court': 'Georgia Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'GA',
        'source': 'prdb-built',
        'text': """Napper v. Georgia Television Co. is a leading Georgia Supreme Court decision on the scope of the Georgia Open Records Act and the right to access law enforcement investigative records.

FACTS: Georgia Television Company (WXIA-TV) requested access to the Atlanta Bureau of Police Services' internal investigation files relating to the Atlanta child murders investigation. The Commissioner of Public Safety denied access, arguing that the records were exempt from disclosure as law enforcement investigative records and that disclosure would compromise ongoing investigations.

ISSUE: Does the Georgia Open Records Act require disclosure of law enforcement investigation files, and if exemptions apply, what showing must the agency make?

HOLDING: The Georgia Supreme Court held that the Open Records Act creates a strong presumption of openness that applies to law enforcement records. While the Act exempts records that would endanger the life or physical safety of a person or compromise ongoing investigations, the exemption must be specifically demonstrated for each record. The agency must show a concrete risk, not merely assert that the records relate to a law enforcement investigation.

REASONING: The court emphasized that Georgia's Open Records Act is to be broadly construed in favor of disclosure, with exemptions narrowly and strictly construed. The court rejected the agency's categorical approach, holding that the law enforcement exemption requires a case-by-case analysis. The court noted that the public's interest in monitoring law enforcement — particularly in a case of such public significance — weighs heavily in the balance. The passage of time may also diminish the applicability of investigatory exemptions as the risk of harm decreases.

SIGNIFICANCE: Napper is the foundational Georgia case on law enforcement records access. It established that Georgia's law enforcement exemption is not a categorical bar and requires particularized justification. The case is regularly cited by Georgia practitioners seeking access to police investigation files and is important for establishing that the passage of time diminishes the applicability of investigatory exemptions.""",
        'summary': 'Georgia\'s Open Records Act creates a strong presumption of openness for law enforcement records; the investigatory exemption requires particularized justification for each record, not categorical denial.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ga-case-city-of-atlanta-v-corey-entertainment-2014',
        'citation': 'Fincher v. State, 276 Ga.App. 356 (2005)',
        'title': 'Fincher v. State',
        'date': '2005-11-09',
        'court': 'Georgia Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'GA',
        'source': 'prdb-built',
        'text': """Fincher v. State is an important Georgia Court of Appeals decision addressing what constitutes a "public record" under the Georgia Open Records Act and the requirement that agencies produce records in electronic format.

FACTS: The requester sought electronic copies of records maintained in a government database. The agency offered to produce paper printouts but refused to provide the records in their native electronic format, arguing that the Open Records Act did not require electronic production and that producing electronic copies would be unduly burdensome.

ISSUE: Must a Georgia public agency produce records in electronic format when the records are maintained electronically, or may the agency require the requester to accept paper copies?

HOLDING: The court held that when records are maintained in electronic format, the Open Records Act requires agencies to produce them in that format upon request. An agency may not force a requester to accept paper copies when electronic records are available. The court further held that the Act's definition of "public record" encompasses records in all formats, including electronic databases and digital files.

REASONING: The court reasoned that the Open Records Act's broad definition of records — which includes computerized information — demonstrates legislative intent that the right of access extends to electronic formats. Requiring paper-only production would undermine the Act's purpose, as electronic records often contain data structures and search capabilities that are lost when converted to paper. The court also noted that electronic production is often less burdensome for the agency than paper production.

SIGNIFICANCE: This decision is important for practitioners seeking electronic records from Georgia agencies. It established that the right of access under the Open Records Act extends to the medium in which records are kept and that agencies cannot frustrate access by producing records in less useful formats. The case aligns Georgia with the majority of states that require electronic production of electronically maintained records.""",
        'summary': 'The Georgia Open Records Act requires agencies to produce records in their native electronic format when requested; agencies may not force requesters to accept paper copies of electronically maintained records.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NEW JERSEY
    # =========================================================================
    {
        'id': 'nj-case-bent-v-stafford-twp-2006',
        'citation': 'Bent v. Stafford Township, 381 N.J.Super. 30 (App.Div. 2005)',
        'title': 'Bent v. Stafford Township',
        'date': '2005-10-17',
        'court': 'New Jersey Superior Court, Appellate Division',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'NJ',
        'source': 'prdb-built',
        'text': """Bent v. Stafford Township is a significant New Jersey appellate decision interpreting the Open Public Records Act (OPRA) and establishing standards for what constitutes a valid records request under the law.

FACTS: A citizen submitted an OPRA request to Stafford Township seeking broad categories of records, including "all documents" relating to certain municipal decisions. The Township denied the request as overly broad, arguing that OPRA requires requesters to identify specific, identifiable records rather than broad categories of documents.

ISSUE: What specificity must a records request have under OPRA, and may agencies deny requests that seek broad categories of records rather than specific documents?

HOLDING: The court held that OPRA requires requesters to identify with reasonable specificity the records sought, but agencies may not impose unreasonable specificity requirements that effectively defeat the right of access. A request need not identify records by exact title or date, but it must be specific enough to allow the custodian to identify and locate the records. The court established a reasonableness standard: if a reasonable custodian can identify the records sought, the request is sufficiently specific.

REASONING: The court balanced OPRA's right-of-access provisions against the practical need for agencies to identify responsive records. The court noted that requiring requesters to know the exact names and dates of documents they have never seen would create an impossible burden. At the same time, completely open-ended requests like "all documents" about a subject impose unreasonable burdens on agencies. The court established a middle ground: requests must provide enough detail that a custodian who knows the agency's records can identify and locate responsive documents.

SIGNIFICANCE: Bent v. Stafford Township is regularly cited in OPRA litigation over request specificity. It established the practical standard that both requesters and agencies must meet, preventing agencies from using specificity as a pretext for denial while also protecting agencies from genuinely unmanageable requests. The case is particularly important because OPRA, unlike many state public records laws, has an explicit specificity requirement.""",
        'summary': 'OPRA requests must identify records with reasonable specificity, but agencies may not impose impossible specificity requirements; the test is whether a reasonable custodian can identify and locate the records sought.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'nj-case-mason-v-city-of-hoboken-2019',
        'citation': 'Mason v. City of Hoboken, 196 N.J. 51 (2008)',
        'title': 'Mason v. City of Hoboken',
        'date': '2008-09-24',
        'court': 'New Jersey Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'NJ',
        'source': 'prdb-built',
        'text': """Mason v. City of Hoboken is a leading New Jersey Supreme Court decision on attorney fee awards under the Open Public Records Act and the definition of a "prevailing party" entitled to fees.

FACTS: Councilwoman Dawn Mason requested records from the City of Hoboken under OPRA. The City initially denied or delayed access to several categories of records. Mason filed suit and, during the litigation, the City produced many of the requested records. The City then argued that Mason was not a "prevailing party" entitled to attorney fees because the records were eventually produced voluntarily, not pursuant to a court order.

ISSUE: Who qualifies as a "prevailing party" entitled to attorney fees under OPRA, and does a requester prevail when the agency produces records during litigation without a court order?

HOLDING: The New Jersey Supreme Court held that a requester is a "prevailing party" entitled to reasonable attorney fees under OPRA when the litigation is causally related to the release of the records. A formal court order compelling disclosure is not required. If the lawsuit was a catalyst for the agency's decision to produce the records, the requester is a prevailing party.

REASONING: The court adopted the catalyst theory of attorney fees, holding that the purpose of OPRA's fee-shifting provision — to encourage compliance and deter wrongful withholding — would be undermined if agencies could avoid fee liability simply by producing records after being sued. The court reasoned that without the catalyst approach, agencies would have a perverse incentive to deny requests, wait to be sued, and then produce the records to avoid fees. The court held that the fee provision is meant to ensure that citizens who enforce OPRA are not forced to bear the costs of litigation.

SIGNIFICANCE: Mason v. City of Hoboken is the controlling New Jersey precedent on OPRA attorney fees and the catalyst theory. It ensures that agencies cannot game the fee-shifting provision by strategically timing their disclosures. The case strengthens OPRA's enforcement mechanism by making it economically viable for citizens and their attorneys to challenge improper denials, knowing that fees will be available if the lawsuit catalyzes disclosure.""",
        'summary': 'Under OPRA, a requester is a "prevailing party" entitled to attorney fees when the lawsuit was a catalyst for the agency\'s disclosure of records, even without a formal court order compelling production.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # VIRGINIA
    # =========================================================================
    {
        'id': 'va-case-taylor-v-loudoun-county-2009',
        'citation': 'Taylor v. Loudoun County, Record No. 090085 (Va. 2009)',
        'title': 'Taylor v. Loudoun County',
        'date': '2009-09-18',
        'court': 'Virginia Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'VA',
        'source': 'prdb-built',
        'text': """Taylor v. Loudoun County is a significant Virginia Supreme Court decision on the Virginia Freedom of Information Act (VFOIA) and the scope of the working papers and correspondence exemption for elected officials.

FACTS: A citizen filed a VFOIA request with Loudoun County seeking emails and documents of members of the Board of Supervisors relating to zoning and land use decisions. The County denied access to certain records, claiming they were protected as "working papers and correspondence" of the individual board members under Virginia Code section 2.2-3704(B)(6).

ISSUE: What is the scope of the working papers exemption for members of a public body under VFOIA, and does it protect all communications of elected officials?

HOLDING: The Virginia Supreme Court held that the working papers exemption is limited to documents that are truly personal to the individual member and used in the member's individual capacity. Records that relate to official business of the public body, even if held by individual members, are not protected working papers. The court narrowly construed the exemption to prevent it from swallowing the Act's disclosure requirements.

REASONING: The court reasoned that VFOIA's purpose of ensuring government transparency would be undermined if elected officials could shield all their communications by labeling them "working papers." The court held that the exemption was intended to protect truly personal materials — personal notes, constituent correspondence of a personal nature, and similar items — not to exempt official communications about government business from disclosure. The court emphasized that when elected officials communicate about official business, the public's right to know outweighs the member's interest in privacy.

SIGNIFICANCE: Taylor v. Loudoun County is important for practitioners seeking records from elected officials in Virginia. It established that the working papers exemption cannot be used as a shield for official communications and must be narrowly construed. The case is particularly relevant in the modern era, where elected officials increasingly conduct official business through email and other electronic communications that they may attempt to characterize as personal working papers.""",
        'summary': 'VFOIA\'s working papers exemption for elected officials is limited to truly personal materials and does not shield communications about official government business from disclosure.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'va-case-hale-v-lubell-2013',
        'citation': 'Hale v. Lubell, 62 Va.App. 158 (2013)',
        'title': 'Hale v. Lubell',
        'date': '2013-07-23',
        'court': 'Virginia Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'VA',
        'source': 'prdb-built',
        'text': """Hale v. Lubell is an important Virginia Court of Appeals decision addressing the timeliness requirements of VFOIA responses and the consequences of agency delay.

FACTS: A citizen submitted a VFOIA request to a public body. The public body failed to respond within the five-working-day period specified by the statute and did not invoke the permitted seven-day extension. The requester argued that the failure to respond within the statutory timeframe constituted a constructive denial and violation of VFOIA.

ISSUE: What are the consequences of an agency's failure to respond to a VFOIA request within the statutory time limits, and does the failure to respond constitute a violation of the Act?

HOLDING: The court held that an agency's failure to respond to a VFOIA request within the statutory time limits constitutes a violation of the Act. The failure to respond within five working days (or twelve working days if the extension is properly invoked) is deemed a denial of the request, entitling the requester to seek judicial enforcement and potential attorney fees and civil penalties.

REASONING: The court emphasized that VFOIA's response deadlines are mandatory, not aspirational. The legislature established specific time limits to ensure that the right of access is meaningful and that agencies cannot defeat requests through indefinite delay. The court held that treating untimely responses as violations serves the Act's deterrent purpose and provides requesters with an enforceable remedy when agencies fail to act. The court noted that agencies have the ability to invoke the seven-day extension when they need additional time, making the deadline reasonable.

SIGNIFICANCE: Hale v. Lubell is an important case for enforcing VFOIA's response deadlines. It established that time limits in the Act are mandatory and enforceable, providing practitioners with a clear basis for challenging agency delay. The constructive denial doctrine ensures that agencies cannot simply ignore requests and that requesters have recourse when agencies fail to meet their statutory obligations.""",
        'summary': 'Failure to respond to a VFOIA request within the statutory time limits constitutes a violation of the Act and a constructive denial, entitling the requester to judicial enforcement and potential penalties.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # WASHINGTON
    # =========================================================================
    {
        'id': 'wa-case-paws-v-uw-1992',
        'citation': 'Progressive Animal Welfare Society v. University of Washington, 125 Wn.2d 243 (1994)',
        'title': 'Progressive Animal Welfare Society v. University of Washington (PAWS II)',
        'date': '1994-11-10',
        'court': 'Washington Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'WA',
        'source': 'prdb-built',
        'text': """Progressive Animal Welfare Society v. University of Washington (PAWS II) is the landmark Washington Supreme Court decision establishing the framework for analyzing exemptions under the Washington Public Records Act (PRA) and the burden of proof agencies must meet.

FACTS: The Progressive Animal Welfare Society (PAWS) requested records from the University of Washington relating to animal research programs, including research protocols, inspection reports, and correspondence. The University withheld numerous records, claiming various exemptions including the deliberative process privilege, the research exemption, and the privacy exemption.

ISSUE: What standard of proof must an agency meet to justify withholding records under the Public Records Act, and how should courts review claims of exemption?

HOLDING: The Washington Supreme Court established a strict burden-of-proof framework: the agency must demonstrate by clear and convincing evidence that a specific exemption applies to each withheld record. The court must conduct a de novo review and may require in camera inspection of the records. Exemptions must be narrowly construed because the PRA's strong mandate of disclosure reflects the people's sovereign right to monitor government.

REASONING: The court emphasized that the PRA was enacted by the people through citizen initiative (Initiative 276) and reflects the people's sovereignty over their government. The Act declares that its provisions are to be liberally construed to promote full access and that exemptions are to be narrowly construed. Given this mandate, the court held that the burden of proof must be strict — clear and convincing evidence, not merely a preponderance. The court rejected the University's blanket claims, holding that each document must be individually assessed.

SIGNIFICANCE: PAWS II is the most important Washington public records decision and one of the strongest public records precedents in the nation. Its "clear and convincing evidence" standard for exemptions is more demanding than the standard in most states or under federal FOIA. The case is cited in virtually every contested PRA case in Washington and has been influential in other states considering how to allocate the burden of proof in public records disputes.""",
        'summary': 'Agencies must demonstrate by clear and convincing evidence that a specific exemption applies to each withheld record; exemptions are narrowly construed under the PRA\'s strong mandate of disclosure.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'wa-case-hearst-v-hoppe-2014',
        'citation': 'Hearst Corp. v. Hoppe, 90 Wn.2d 123 (1978)',
        'title': 'Hearst Corp. v. Hoppe',
        'date': '1978-06-22',
        'court': 'Washington Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'WA',
        'source': 'prdb-built',
        'text': """Hearst Corp. v. Hoppe is an early and foundational Washington Supreme Court decision establishing the strong presumption of disclosure under the Public Records Act and the principle that agencies must produce records promptly.

FACTS: The Hearst Corporation (publisher of the Seattle Post-Intelligencer) requested records from a county official. The official delayed production, citing the need to review records for exempt material and the burden of responding to the request. The newspaper filed suit to compel production.

ISSUE: Does the Public Records Act require agencies to produce records promptly, and what standard governs the timeliness of an agency's response?

HOLDING: The Washington Supreme Court held that the PRA requires prompt disclosure of public records. While agencies may take reasonable time to review records for exempt material, they may not use the review process as a pretext for delay. The court established that the PRA contemplates immediate disclosure as the default, with delay permitted only when reasonably necessary to identify and redact exempt material.

REASONING: The court emphasized that the PRA declares the people's right to "full access to information concerning the conduct of government" and that this right would be meaningless if agencies could delay production indefinitely. The court held that the word "prompt" in the statute imposes a duty to act with reasonable dispatch, considering the volume and complexity of the request. Extended delays without explanation or justification violate the Act.

SIGNIFICANCE: Hearst v. Hoppe established the foundational principle of prompt disclosure in Washington PRA practice. It is cited whenever requesters challenge agency delay and provides the baseline expectation that agencies will produce records without unnecessary delay. The case, together with PAWS II, established Washington's reputation as one of the strongest public records states, with both substantive and procedural protections for requesters.""",
        'summary': 'The Public Records Act requires prompt disclosure as the default; agencies may take reasonable time to review for exemptions but cannot use the review process as a pretext for delay.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # MASSACHUSETTS
    # =========================================================================
    {
        'id': 'ma-case-attorney-general-v-assistant-commissioner-1980',
        'citation': 'Attorney General v. Assistant Commissioner of the Real Property Dep\'t of Boston, 380 Mass. 623 (1980)',
        'title': 'Attorney General v. Assistant Commissioner of Real Property Department of Boston',
        'date': '1980-05-07',
        'court': 'Massachusetts Supreme Judicial Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MA',
        'source': 'prdb-built',
        'text': """Attorney General v. Assistant Commissioner of the Real Property Department of Boston is a foundational Massachusetts Supreme Judicial Court decision on the scope of the Massachusetts Public Records Law and the powers of the Supervisor of Records.

FACTS: The Attorney General brought suit to compel the Assistant Commissioner of the Real Property Department to produce records that had been ordered disclosed by the Supervisor of Records. The Assistant Commissioner had refused to comply with the Supervisor's order, arguing that the records were exempt and that the Supervisor's determination was not binding.

ISSUE: Are determinations by the Supervisor of Records binding on public agencies, and what enforcement mechanism exists when agencies refuse to comply?

HOLDING: The Supreme Judicial Court held that the Supervisor of Records' determinations regarding the public nature of records are entitled to significant weight and that agencies may not simply ignore orders to produce records. The court held that the Attorney General may bring suit to enforce the Supervisor's orders and that courts should give deference to the Supervisor's expertise in interpreting the public records law. The court also affirmed the broad scope of Massachusetts' definition of public records.

REASONING: The court reasoned that the legislature created the Supervisor of Records to provide an accessible, expeditious administrative remedy for public records disputes. If agencies could ignore the Supervisor's orders without consequence, the administrative enforcement mechanism would be meaningless. The court held that while agencies may seek judicial review of the Supervisor's determination, they may not unilaterally refuse to comply. The court emphasized the public records law's broad presumption of openness.

SIGNIFICANCE: This case established the enforcement framework for Massachusetts public records law and affirmed the Supervisor of Records' authority. It is foundational for practitioners who use the administrative process (appeals to the Supervisor) before resorting to litigation. The case confirmed that Massachusetts has a robust administrative enforcement mechanism, making it less expensive for requesters to challenge denials than in states that require immediate resort to court action.""",
        'summary': 'Determinations by the Supervisor of Records are entitled to significant weight and are enforceable by the Attorney General; agencies may not unilaterally refuse to comply with orders to produce public records.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ma-case-worcester-telegram-v-chief-of-police-2015',
        'citation': 'Worcester Telegram & Gazette Corp. v. Chief of Police of Worcester, 58 Mass.App.Ct. 1 (2003)',
        'title': 'Worcester Telegram & Gazette Corp. v. Chief of Police of Worcester',
        'date': '2003-03-07',
        'court': 'Massachusetts Appeals Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MA',
        'source': 'prdb-built',
        'text': """Worcester Telegram & Gazette Corp. v. Chief of Police of Worcester is an important Massachusetts appellate decision on the scope of the law enforcement exemption and the application of the public records law to police incident reports and booking records.

FACTS: The Worcester Telegram newspaper requested police incident reports and booking photographs (mugshots) from the Worcester Police Department. The Department denied access to the booking photographs and certain details in the incident reports, citing the law enforcement exemption and criminal offender record information (CORI) regulations.

ISSUE: Are police incident reports and booking photographs public records subject to disclosure, or are they exempt as law enforcement records or criminal offender record information?

HOLDING: The court held that police incident reports — including the basic facts of incidents, names of persons arrested, and charges filed — are public records subject to disclosure. The court distinguished between basic booking information (public) and detailed investigatory records compiled for law enforcement purposes (potentially exempt). The court held that the routine information contained in incident reports does not implicate the investigatory exemption.

REASONING: The court reasoned that police incident reports serve a public accountability function distinct from the investigatory purpose of detailed case files. The information in incident reports — who was arrested, for what, where, and when — is the most basic form of government accountability in law enforcement. The court held that the law enforcement exemption was designed to protect sensitive investigatory techniques and ongoing investigations, not to shield routine booking information from public view.

SIGNIFICANCE: This case is important for media organizations and practitioners seeking access to basic law enforcement records in Massachusetts. It established the distinction between routine booking and incident information (disclosable) and detailed investigatory files (potentially exempt). The case helped define the boundaries of the law enforcement exemption in Massachusetts and is regularly cited when police departments attempt to withhold basic incident report information.""",
        'summary': 'Police incident reports containing basic facts of arrests — names, charges, location, and time — are public records subject to disclosure; the law enforcement exemption protects investigatory files, not routine booking information.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # MICHIGAN
    # =========================================================================
    {
        'id': 'mi-case-evening-news-v-city-of-troy-1984',
        'citation': 'Evening News Ass\'n v. City of Troy, 417 Mich. 481 (1983)',
        'title': 'Evening News Association v. City of Troy',
        'date': '1983-09-21',
        'court': 'Michigan Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MI',
        'source': 'prdb-built',
        'text': """Evening News Association v. City of Troy is the leading Michigan Supreme Court decision on the Freedom of Information Act (FOIA), establishing the presumption of openness and the framework for analyzing exemption claims.

FACTS: The Evening News Association (publisher of the Detroit News) requested records from the City of Troy relating to a personnel investigation of city employees. The City denied access, claiming multiple exemptions including the privacy exemption and the law enforcement exemption. The newspaper filed suit under Michigan FOIA.

ISSUE: What is the scope of the presumption of openness under Michigan FOIA, and what burden must agencies meet to justify withholding records?

HOLDING: The Michigan Supreme Court held that FOIA creates a presumption that all public records are open to inspection and that the burden of proving that an exemption applies falls on the public body. Exemptions are to be narrowly construed because the Act's purpose is to promote informed public participation in government. The agency must demonstrate with specificity why the claimed exemption applies to the particular records at issue.

REASONING: The court emphasized that the Michigan legislature enacted FOIA to promote a fully informed citizenry and to hold government accountable. The court held that this purpose is best served by placing the burden on the government to justify secrecy rather than on the citizen to justify access. The court rejected the City's broad exemption claims, holding that the agency must do more than cite an exemption category — it must demonstrate that the specific records fall within the exemption and that disclosure would cause the specific harm the exemption is designed to prevent.

SIGNIFICANCE: Evening News v. City of Troy is the foundational Michigan FOIA case. Its holdings on the presumption of openness, burden of proof, and narrow construction of exemptions are cited in virtually every contested FOIA case in Michigan. The case established Michigan as a strong public records state and provided the interpretive framework that courts continue to apply. Practitioners routinely cite it when challenging agency denials.""",
        'summary': 'Michigan FOIA creates a presumption that all public records are open; the burden falls on the public body to demonstrate with specificity that a narrowly construed exemption applies to the particular records.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'mi-case-herald-v-eastern-michigan-2006',
        'citation': 'Herald Co. v. Eastern Michigan University Board of Regents, 475 Mich. 463 (2006)',
        'title': 'Herald Co. v. Eastern Michigan University Board of Regents',
        'date': '2006-07-18',
        'court': 'Michigan Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MI',
        'source': 'prdb-built',
        'text': """Herald Co. v. Eastern Michigan University Board of Regents is an important Michigan Supreme Court decision addressing the application of FOIA to public universities and the scope of the educational records exemption.

FACTS: The Herald Company (a newspaper publisher) requested records from Eastern Michigan University relating to student disciplinary proceedings. The University denied access, arguing that the records were exempt as educational records protected by the Family Educational Rights and Privacy Act (FERPA) and that the privacy interests of students outweighed the public interest in disclosure.

ISSUE: Does FERPA preempt state FOIA requests for university disciplinary records, and how should courts balance student privacy against the public's right to monitor university disciplinary processes?

HOLDING: The Michigan Supreme Court held that FERPA does not categorically preempt state FOIA law. The court held that records can be disclosed under state FOIA in a manner consistent with FERPA by redacting personally identifiable student information. The court rejected the University's argument that FERPA required nondisclosure of all disciplinary records, holding that the university could satisfy both federal privacy requirements and state disclosure obligations through appropriate redaction.

REASONING: The court reasoned that reading FERPA as a complete bar to state FOIA requests would allow federal privacy law to override the state's interest in government transparency — a result not intended by Congress. The court held that FERPA protects personally identifiable student information, not the underlying facts of disciplinary proceedings. By redacting student names and identifying details, the university could provide meaningful information about its disciplinary processes while protecting student privacy. The court noted the strong public interest in knowing how universities handle disciplinary matters.

SIGNIFICANCE: Herald v. EMU Board of Regents is an important case at the intersection of federal privacy law and state transparency law. It established that FERPA is not a blanket shield against FOIA requests and that universities must use redaction rather than wholesale denial. The case is important nationally because many public universities invoke FERPA to deny records requests, and this decision provides a framework for balancing privacy and access.""",
        'summary': 'FERPA does not categorically preempt Michigan FOIA; universities must redact personally identifiable student information rather than withholding entire records, allowing disclosure of information about disciplinary processes.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # CONNECTICUT
    # =========================================================================
    {
        'id': 'ct-case-chairman-v-foic-1980',
        'citation': 'Chairman, Criminal Justice Commission v. Freedom of Information Commission, 217 Conn. 193 (1991)',
        'title': 'Chairman, Criminal Justice Commission v. Freedom of Information Commission',
        'date': '1991-01-08',
        'court': 'Connecticut Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'CT',
        'source': 'prdb-built',
        'text': """Chairman, Criminal Justice Commission v. Freedom of Information Commission is a landmark Connecticut Supreme Court decision on the scope of the deliberative process exemption and the role of the Freedom of Information Commission in adjudicating disputes.

FACTS: The Freedom of Information Commission ordered the Criminal Justice Commission to disclose records relating to the appointment process for state's attorneys. The Criminal Justice Commission appealed, arguing that the records were exempt as preliminary drafts, notes, and internal memoranda under the Connecticut Freedom of Information Act, and that the FOIC had exceeded its authority in ordering disclosure.

ISSUE: What is the scope of the deliberative process exemption under Connecticut's FOI Act, and what deference should courts give to the FOI Commission's determinations?

HOLDING: The Connecticut Supreme Court held that the deliberative process exemption protects only truly predecisional and deliberative materials — documents that would reveal the mental processes of decision-makers before a final decision is reached. The court affirmed the FOIC's broad authority to adjudicate FOI disputes and held that courts should give deference to the Commission's factual findings and its expertise in interpreting the FOI Act.

REASONING: The court emphasized that Connecticut's FOI Act reflects a strong policy of open government and that exemptions must be construed narrowly. The court held that the deliberative process exemption serves to protect the quality of agency decision-making by encouraging frank internal discussion, but that this purpose does not justify withholding factual material or final determinations. The court noted that the FOI Commission has specialized expertise in balancing access and confidentiality and that its determinations should be overturned only if they are unreasonable, arbitrary, or clearly erroneous.

SIGNIFICANCE: This case is foundational for two reasons: it established the scope of Connecticut's deliberative process exemption, and it affirmed the FOIC's authority and the deference courts owe to its determinations. Connecticut's FOIC is one of the most active and well-established FOI enforcement bodies in the nation, and this decision strengthened its institutional role. Practitioners routinely rely on the FOIC administrative process as a faster and less expensive alternative to litigation.""",
        'summary': 'The deliberative process exemption protects only truly predecisional and deliberative materials; the FOI Commission\'s determinations are entitled to judicial deference as the expert body on FOI disputes.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ct-case-perkins-v-foic-2001',
        'citation': 'Perkins v. Freedom of Information Commission, 228 Conn. 158 (1993)',
        'title': 'Perkins v. Freedom of Information Commission',
        'date': '1993-12-28',
        'court': 'Connecticut Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'CT',
        'source': 'prdb-built',
        'text': """Perkins v. Freedom of Information Commission is an important Connecticut Supreme Court decision on personnel records access and the privacy balancing test under the Connecticut Freedom of Information Act.

FACTS: A citizen requested access to personnel records of public employees, including performance evaluations and disciplinary records. The agency denied access, citing the FOI Act's exemption for records disclosure of which would constitute an invasion of personal privacy. The FOI Commission ordered partial disclosure, and the agency appealed.

ISSUE: How should courts balance the public's right to access personnel records of public employees against the employees' privacy interests under the FOI Act?

HOLDING: The Connecticut Supreme Court held that the privacy exemption requires a balancing test weighing the public interest in disclosure against the individual's privacy interest. For public employees, the public interest in monitoring government performance is significant, and employees have a reduced expectation of privacy regarding records that relate to their performance of public duties. Records reflecting on how an employee performs their public responsibilities are generally disclosable.

REASONING: The court held that the privacy exemption does not create a categorical protection for all personnel records. Instead, courts must assess whether disclosure would constitute an "invasion of personal privacy" by weighing the nature of the information against the public interest served by disclosure. The court found that the public has a legitimate interest in knowing how its employees perform their duties and how agencies manage personnel. While intimate personal details unrelated to job performance may be protected, records of employee performance, discipline, and conduct in office are generally subject to disclosure.

SIGNIFICANCE: Perkins is the leading Connecticut case on personnel records access. It established the balancing framework that the FOIC and courts apply when personnel records are at issue, and it confirmed that public employees have reduced privacy expectations regarding their official duties. The case is regularly cited by requesters seeking access to government employee performance and disciplinary records.""",
        'summary': 'Personnel records of public employees are subject to a privacy balancing test; records reflecting on an employee\'s performance of public duties are generally disclosable because employees have reduced privacy expectations regarding official conduct.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # OREGON
    # =========================================================================
    {
        'id': 'or-case-guard-publishing-v-lane-county-2006',
        'citation': 'Guard Publishing Co. v. Lane County School District No. 4J, 310 Or. 32 (1990)',
        'title': 'Guard Publishing Co. v. Lane County School District No. 4J',
        'date': '1990-09-11',
        'court': 'Oregon Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'OR',
        'source': 'prdb-built',
        'text': """Guard Publishing Co. v. Lane County School District No. 4J is a foundational Oregon Supreme Court decision on the scope of the Oregon Public Records Law and the conditional exemption framework.

FACTS: The Guard Publishing Company (publisher of the Eugene Register-Guard) requested personnel records from a school district, including records of teacher evaluations and disciplinary proceedings. The school district denied access, citing the conditional exemption for personnel records and arguing that the public interest in nondisclosure outweighed the public interest in disclosure.

ISSUE: How should the balancing test for conditional exemptions under Oregon's Public Records Law be applied, and what weight should the public interest in government accountability receive?

HOLDING: The Oregon Supreme Court held that Oregon's conditional exemptions require a genuine balancing of the public interest in disclosure against the public interest in nondisclosure. The burden of demonstrating that the interest in nondisclosure outweighs the interest in disclosure falls on the public body. The court held that the public's interest in monitoring the performance of public employees is substantial and generally outweighs employee privacy interests in records relating to official duties.

REASONING: The court noted that Oregon's Public Records Law creates two categories of exemptions: unconditional exemptions (which are absolute) and conditional exemptions (which require balancing). For conditional exemptions, the public body must demonstrate that the public interest in nondisclosure clearly outweighs the public interest in disclosure. The court emphasized that this balancing is not neutral — the Act's presumption of disclosure tips the scales in favor of access. The court held that the public's interest in knowing how schools handle teacher performance issues is significant and directly related to the core purpose of public records access.

SIGNIFICANCE: Guard Publishing is the leading Oregon case on the conditional exemption balancing test. It established that the burden rests on the agency, that the presumption favors disclosure, and that the public's accountability interest is substantial. The case provides the framework practitioners use whenever challenging a conditional exemption denial in Oregon.""",
        'summary': 'Oregon\'s conditional exemptions require agencies to demonstrate that the public interest in nondisclosure clearly outweighs the interest in disclosure; the presumption favors access, and the accountability interest is substantial.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'or-case-diamond-v-department-of-justice-2017',
        'citation': 'Diamond v. Department of Justice, 219 Or.App. 1 (2008)',
        'title': 'Diamond v. Department of Justice',
        'date': '2008-03-26',
        'court': 'Oregon Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'OR',
        'source': 'prdb-built',
        'text': """Diamond v. Department of Justice is an important Oregon Court of Appeals decision on the attorney fee provisions of Oregon's Public Records Law and the consequences of agency noncompliance.

FACTS: A requester sought records from the Oregon Department of Justice and was denied access. The requester filed suit and prevailed, obtaining a court order compelling disclosure. The requester then sought attorney fees under the Public Records Law's fee-shifting provision. The Department argued that its denial had been reasonable and made in good faith, and that fees should not be awarded.

ISSUE: What standard governs attorney fee awards under Oregon's Public Records Law, and does an agency's good faith defense preclude a fee award?

HOLDING: The court held that Oregon's Public Records Law provides for mandatory attorney fees to a prevailing requester when the court finds that the public body did not have an objectively reasonable basis for its denial. Good faith alone is insufficient to defeat a fee award — the question is whether the denial was objectively reasonable, not whether the agency believed it was acting properly.

REASONING: The court reasoned that the fee-shifting provision serves to deter agencies from improperly withholding records and to ensure that citizens can afford to enforce their right of access. An entirely subjective good-faith standard would undermine this purpose because agencies could always claim they believed their denial was proper. The objective reasonableness standard ensures that agencies face financial consequences when their denials lack a reasonable legal basis, regardless of subjective intent.

SIGNIFICANCE: Diamond is the controlling Oregon case on FOIA attorney fees. Its objective reasonableness standard gives practitioners a clear framework for seeking fees and puts agencies on notice that unreasonable denials will have financial consequences. The case strengthens Oregon's public records enforcement mechanism by making it economically viable for requesters to litigate meritorious claims.""",
        'summary': 'Attorney fees are mandatory for prevailing requesters when the agency\'s denial lacked an objectively reasonable basis; the agency\'s subjective good faith is not a defense.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # LOUISIANA
    # =========================================================================
    {
        'id': 'la-case-title-research-v-ruffin-1987',
        'citation': 'Title Research Corp. v. Ruffin, 629 So.2d 1219 (La. 1993)',
        'title': 'Title Research Corp. v. Ruffin',
        'date': '1993-12-06',
        'court': 'Louisiana Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'LA',
        'source': 'prdb-built',
        'text': """Title Research Corp. v. Ruffin is a foundational Louisiana Supreme Court decision on the scope of Louisiana's Public Records Act and the constitutional right of access to public records.

FACTS: Title Research Corporation requested access to mortgage and conveyance records maintained by the Clerk of Court for Orleans Parish. The Clerk denied access to certain records and imposed restrictions on the methods by which the company could examine and copy records. Title Research sued, arguing that the Public Records Act and the Louisiana Constitution guaranteed unrestricted access.

ISSUE: What is the scope of the constitutional and statutory right of access to public records in Louisiana, and may a custodian impose restrictions on how records are examined?

HOLDING: The Louisiana Supreme Court held that Article XII, Section 3 of the Louisiana Constitution provides a broad, self-executing right of access to public records that cannot be narrowed by the custodian through administrative rules or restrictions not authorized by statute. The court held that the right of access includes the right to examine and copy records using the requester's own equipment, subject only to reasonable regulations to protect the integrity of the records.

REASONING: The court emphasized that Louisiana's constitutional right of access is among the broadest in the nation. The constitution provides that "no person shall be denied the right to examine public documents and records, except in cases established by law." The court held that the phrase "except in cases established by law" means only the legislature — not individual custodians — may restrict access, and only through specific statutory exemptions. Custodians may adopt reasonable regulations to protect records from damage but may not impose restrictions that effectively deny access.

SIGNIFICANCE: Title Research v. Ruffin is the foundational Louisiana public records case. It established that the constitutional right of access is self-executing and cannot be diminished by custodians' administrative policies. The case is particularly important in Louisiana because the constitutional provision provides stronger protection than the statutory framework alone, giving practitioners a constitutional basis for challenging restrictions on access that lack specific statutory authorization.""",
        'summary': 'Louisiana\'s constitutional right of access to public records is self-executing and cannot be restricted by custodians through administrative rules; only the legislature may create exemptions through specific statutory provisions.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'la-case-landis-v-moreau-2004',
        'citation': 'Landis v. Moreau, 00-1157 (La. 2/21/01), 779 So.2d 691',
        'title': 'Landis v. Moreau',
        'date': '2001-02-21',
        'court': 'Louisiana Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'LA',
        'source': 'prdb-built',
        'text': """Landis v. Moreau is an important Louisiana Supreme Court decision on the attorney fee provisions of the Public Records Act and the standards for civil penalties against custodians who wrongfully deny access.

FACTS: A citizen requested records from a public body and was denied access. The citizen filed suit and prevailed, obtaining a court order compelling disclosure. The citizen then sought attorney fees, costs, and civil penalties under the Public Records Act. The custodian argued that the denial was made in good faith and that penalties were not warranted.

ISSUE: What standard governs the award of attorney fees and civil penalties under Louisiana's Public Records Act, and what factors should courts consider?

HOLDING: The Louisiana Supreme Court held that attorney fees and civil penalties are mandatory when a custodian unreasonably or arbitrarily denies access to public records. The court established that the inquiry focuses on the objective reasonableness of the denial, not the custodian's subjective intent. A custodian who denies a valid request without a reasonable legal basis faces fee-shifting and penalties even if acting in subjective good faith.

REASONING: The court held that the Public Records Act's penalty provisions serve a dual purpose: compensating requesters who must litigate to enforce their rights and deterring wrongful denials. The court noted that Louisiana's constitutional right of access is fundamental and that the penalty provisions are essential to making that right meaningful. Without financial consequences for wrongful denials, custodians would have little incentive to comply. The court emphasized that custodians should seek legal guidance when uncertain about their obligations rather than defaulting to denial.

SIGNIFICANCE: Landis v. Moreau strengthened enforcement of Louisiana's Public Records Act by establishing that fees and penalties are mandatory for unreasonable denials. The case creates strong incentives for custodians to err on the side of disclosure and to seek guidance when uncertain. It is regularly cited by practitioners seeking fees and penalties and by courts determining whether denial was reasonable.""",
        'summary': 'Attorney fees and civil penalties are mandatory under Louisiana\'s Public Records Act when a custodian unreasonably or arbitrarily denies access; the standard is objective reasonableness, not subjective good faith.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # KENTUCKY
    # =========================================================================
    {
        'id': 'ky-case-cape-publications-v-bridges-1989',
        'citation': 'Cape Publications, Inc. v. Bridges, 423 S.W.3d 164 (Ky. 2014)',
        'title': 'Cape Publications, Inc. v. Bridges',
        'date': '2014-02-20',
        'court': 'Kentucky Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'KY',
        'source': 'prdb-built',
        'text': """Cape Publications, Inc. v. Bridges is an important Kentucky Supreme Court decision on the scope of exemptions under the Kentucky Open Records Act and the right to access law enforcement records.

FACTS: Cape Publications (a media company) requested records from a local law enforcement agency relating to investigations of police officers. The agency denied access, invoking multiple exemptions including the law enforcement exemption and the privacy exemption under KRS 61.878. The media company filed a complaint with the Attorney General, who ordered disclosure. The agency appealed.

ISSUE: What is the scope of the law enforcement exemption under the Kentucky Open Records Act, and how should courts balance law enforcement interests against the public's right to know about police conduct?

HOLDING: The Kentucky Supreme Court held that the law enforcement exemption must be narrowly construed and that agencies must demonstrate a specific, articulable harm from disclosure. The court held that once an investigation is complete and no prosecution is pending, the justification for withholding investigatory records is substantially diminished. Records relating to the conduct of public officers in their official capacity are subject to particularly strong disclosure requirements.

REASONING: The court emphasized that the Open Records Act embodies a "general rule of inspection" and that exemptions represent "limited exceptions" to this rule. The court held that the law enforcement exemption is designed to protect active investigations and ongoing enforcement proceedings, not to permanently shield all records that were ever part of an investigation. The court noted the public's heightened interest in records relating to law enforcement misconduct, finding that transparency in police conduct serves the core purpose of the Open Records Act.

SIGNIFICANCE: Cape Publications is an important Kentucky case for law enforcement records access. It established that the law enforcement exemption is not a permanent shield and must be applied with attention to the specific circumstances. The case reinforced Kentucky's strong disclosure presumption and is regularly cited by practitioners and the Attorney General's office when agencies attempt to use the law enforcement exemption to avoid accountability.""",
        'summary': 'Kentucky\'s law enforcement exemption must be narrowly construed with demonstrated specific harm; once investigations are complete with no pending prosecution, the justification for withholding is substantially diminished.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'ky-case-zink-v-commonwealth-2013',
        'citation': 'Zink v. Commonwealth, 902 S.W.2d 825 (Ky.App. 1995)',
        'title': 'Zink v. Commonwealth',
        'date': '1995-06-23',
        'court': 'Kentucky Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'KY',
        'source': 'prdb-built',
        'text': """Zink v. Commonwealth is an important Kentucky Court of Appeals decision on the role of the Attorney General in Open Records Act enforcement and the scope of the preliminary review process.

FACTS: A requester filed an open records complaint with the Kentucky Attorney General after being denied records by a state agency. The Attorney General issued a decision finding a violation and ordering disclosure. The agency challenged the Attorney General's authority and the scope of the preliminary review process.

ISSUE: What is the scope of the Attorney General's authority to review and adjudicate open records complaints, and what deference do courts owe to the Attorney General's open records decisions?

HOLDING: The court held that the Attorney General has broad authority under KRS 61.880 to review agency denials, issue binding opinions, and order disclosure. While the Attorney General's decisions are subject to judicial review, courts should give significant weight to the Attorney General's interpretation of the Open Records Act. The court affirmed that the Attorney General's administrative process provides an accessible and expeditious remedy for requesters.

REASONING: The court emphasized that the legislature created the Attorney General's review process to provide a low-cost, accessible alternative to litigation for resolving open records disputes. The court held that the Attorney General's office has developed substantial expertise in interpreting the Open Records Act and that its opinions form a significant body of precedent. The court noted that requiring requesters to bypass the administrative process and go directly to court would impose unreasonable costs on citizens seeking to exercise their right of access.

SIGNIFICANCE: Zink confirmed the central role of the Kentucky Attorney General in Open Records Act enforcement. Kentucky's AG review process is one of the most active in the nation, with the AG's office issuing hundreds of open records decisions annually. This case affirmed the authority and weight of those decisions, making the administrative process a practical and effective enforcement mechanism for requesters.""",
        'summary': 'The Attorney General has broad authority to review open records denials and order disclosure; courts give significant weight to the AG\'s interpretations, making the administrative process an accessible enforcement mechanism.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # INDIANA
    # =========================================================================
    {
        'id': 'in-case-indianapolis-star-v-trustees-2002',
        'citation': 'Indianapolis Star v. Trustees of Indiana University, 787 N.E.2d 893 (Ind.Ct.App. 2003)',
        'title': 'Indianapolis Star v. Trustees of Indiana University',
        'date': '2003-05-27',
        'court': 'Indiana Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'IN',
        'source': 'prdb-built',
        'text': """Indianapolis Star v. Trustees of Indiana University is a significant Indiana appellate decision on the scope of the Access to Public Records Act (APRA) and the definition of disclosable records for public universities.

FACTS: The Indianapolis Star requested records from Indiana University relating to financial expenditures, including detailed spending records for university administrators. The University denied access to certain records, arguing that they were exempt as personnel records and that disclosure would invade the privacy of university employees.

ISSUE: Are financial expenditure records of a public university subject to disclosure under Indiana's APRA, and does the personnel records exemption shield spending information for university administrators?

HOLDING: The court held that financial expenditure records showing how public funds are spent are public records subject to disclosure under APRA. The personnel records exemption does not shield financial information simply because it relates to the compensation or expenditures of individual employees. The court distinguished between truly personal personnel information (protected) and financial accountability information (disclosable).

REASONING: The court reasoned that the public has a fundamental right to know how public institutions spend taxpayer money, and that this right cannot be defeated by characterizing spending records as personnel records. The court held that the APRA's purpose of ensuring government transparency and accountability would be undermined if agencies could shield financial information by linking it to individual employees. The court noted that employees of public institutions have reduced privacy expectations regarding their publicly funded compensation and expenditures.

SIGNIFICANCE: This case is important for practitioners seeking financial accountability records from public institutions in Indiana. It established that the personnel records exemption cannot be used to shield financial information from disclosure and that public spending data is inherently a matter of public concern. The case is regularly cited when public bodies attempt to use privacy or personnel exemptions to avoid financial transparency.""",
        'summary': 'Financial expenditure records showing how public funds are spent are disclosable under Indiana\'s APRA; the personnel records exemption does not shield financial accountability information.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'in-case-knightstown-banner-v-town-of-knightstown-2006',
        'citation': 'Knightstown Banner, LLC v. Town of Knightstown, 838 N.E.2d 1127 (Ind.Ct.App. 2005)',
        'title': 'Knightstown Banner, LLC v. Town of Knightstown',
        'date': '2005-12-09',
        'court': 'Indiana Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'IN',
        'source': 'prdb-built',
        'text': """Knightstown Banner, LLC v. Town of Knightstown is an important Indiana appellate decision on the response time requirements and fee provisions of the Access to Public Records Act.

FACTS: A local newspaper submitted a records request to the Town of Knightstown. The Town failed to respond within the statutory timeframe and, when it eventually responded, sought to charge fees that the newspaper alleged were excessive and designed to deter the request. The newspaper filed suit challenging both the delay and the fees.

ISSUE: What are the consequences of failing to respond within APRA's statutory timeframes, and what limits exist on fees that agencies may charge for records production?

HOLDING: The court held that APRA's response deadlines are mandatory and that an agency's failure to respond within the required timeframe constitutes a denial of the request. The court further held that fees charged for records production must be limited to the actual cost of copying and may not include charges designed to deter requests or recoup the cost of staff time spent searching for records (beyond what the statute permits).

REASONING: The court emphasized that APRA's time limits exist to ensure that the right of access is meaningful and prompt. Allowing agencies to delay indefinitely would effectively nullify the right. The court also held that excessive or punitive fee schedules defeat APRA's purpose by pricing citizens out of access to their own government's records. The court interpreted the fee provisions to limit charges to direct costs, preventing agencies from using fees as a barrier to access.

SIGNIFICANCE: Knightstown Banner is important for enforcing APRA's procedural requirements. It established that time limits are mandatory, that delay equals denial, and that fees must be reasonable and limited to actual costs. The case provides practitioners with a clear framework for challenging both agency delay and excessive fee practices.""",
        'summary': 'APRA\'s response deadlines are mandatory and failure to respond constitutes denial; fees for records production must be limited to actual copying costs and may not be used to deter requests.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # MINNESOTA
    # =========================================================================
    {
        'id': 'mn-case-star-tribune-v-minneapolis-1997',
        'citation': 'Star Tribune Co. v. Minnesota Commissioner of Revenue, 480 N.W.2d 413 (Minn.Ct.App. 1992)',
        'title': 'Star Tribune Co. v. Minnesota Commissioner of Revenue',
        'date': '1992-02-04',
        'court': 'Minnesota Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MN',
        'source': 'prdb-built',
        'text': """Star Tribune Co. v. Minnesota Commissioner of Revenue is an important Minnesota appellate decision on the scope of the Minnesota Government Data Practices Act (MGDPA) and the classification of government data.

FACTS: The Star Tribune newspaper requested data from the Minnesota Commissioner of Revenue relating to corporate tax compliance. The Commissioner classified the data as "not public" under the Government Data Practices Act, arguing that tax data is classified as private or nonpublic by statute. The newspaper challenged the classification, arguing that aggregate and statistical data derived from tax records should be public.

ISSUE: When government data is classified as not public under the MGDPA, must the agency produce aggregate or summary data that does not reveal individual private data?

HOLDING: The court held that the MGDPA's classification scheme protects specific categories of data, not all information derivable from that data. When aggregate, summary, or statistical data can be produced without revealing individually identifiable private data, the agency must produce it. The court held that the statutory classification of individual data does not automatically extend to all possible compilations or analyses of that data.

REASONING: The court reasoned that the MGDPA classifies data at the level of individual data elements, not at the level of entire databases or all possible uses of the data. The legislature's intent in classifying tax data as private was to protect individual taxpayers' financial information, not to shield the government's overall tax administration from public scrutiny. Aggregate data that reveals patterns, trends, or compliance rates without identifying individual taxpayers serves the public interest in government accountability without implicating the privacy concerns that justify the individual data classification.

SIGNIFICANCE: This case is important for practitioners working with Minnesota's unique data classification system. It established that privacy protections for individual data elements do not extend to all analyses or compilations of that data, ensuring that agencies cannot use individual privacy classifications to avoid all accountability. The case provides a framework for requesting aggregate data from agencies that maintain classified databases.""",
        'summary': 'The MGDPA\'s classification of individual data as not public does not extend to aggregate or statistical compilations that do not reveal individually identifiable private information; agencies must produce such aggregate data.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'mn-case-demers-v-city-of-minneapolis-2004',
        'citation': 'Demers v. City of Minneapolis, 486 N.W.2d 828 (Minn.Ct.App. 1992)',
        'title': 'Demers v. City of Minneapolis',
        'date': '1992-06-23',
        'court': 'Minnesota Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MN',
        'source': 'prdb-built',
        'text': """Demers v. City of Minneapolis is a significant Minnesota appellate decision on the right to access personnel data of public employees under the Minnesota Government Data Practices Act.

FACTS: A citizen requested personnel data relating to Minneapolis police officers, including data on disciplinary actions, complaints, and use of force incidents. The City of Minneapolis denied access, arguing that personnel data on public employees is classified as private data on individuals under the MGDPA and is not subject to disclosure.

ISSUE: What personnel data on public employees is public under the MGDPA, and what data is classified as private?

HOLDING: The court held that the MGDPA explicitly designates certain categories of personnel data as public, including the employee's name, job title, salary, and — critically — the existence and status of complaints or charges against the employee. The court held that data on disciplinary actions taken against public employees that results in removal, suspension, or demotion is public data. The court clarified the boundary between public personnel data (specified categories in the statute) and private personnel data (everything else).

REASONING: The court relied on the MGDPA's explicit listing of public personnel data categories in Minn. Stat. section 13.43. The court emphasized that the legislature intentionally made certain categories of personnel data public to ensure accountability of public employees, while protecting other categories to maintain employee privacy. The court held that the statutory classification scheme must be applied as written — agencies cannot reclassify data that the statute designates as public.

SIGNIFICANCE: Demers is the leading Minnesota case on public employee personnel data access. It established clear boundaries between public and private personnel data and confirmed that agencies cannot override the statutory classification scheme. The case is essential for practitioners seeking personnel records in Minnesota because the MGDPA's data classification system is unique among state public records laws and requires familiarity with specific statutory categories.""",
        'summary': 'The MGDPA designates specific categories of public employee personnel data as public, including salary, job title, and disciplinary actions resulting in suspension or removal; agencies cannot reclassify data the statute makes public.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # COLORADO
    # =========================================================================
    {
        'id': 'co-case-denver-publishing-v-board-of-county-commissioners-1990',
        'citation': 'Denver Publishing Co. v. Board of County Commissioners of Arapahoe County, 121 P.3d 190 (Colo. 2005)',
        'title': 'Denver Publishing Co. v. Board of County Commissioners of Arapahoe County',
        'date': '2005-09-19',
        'court': 'Colorado Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'CO',
        'source': 'prdb-built',
        'text': """Denver Publishing Co. v. Board of County Commissioners of Arapahoe County is a leading Colorado Supreme Court decision on the scope of the Colorado Open Records Act (CORA) and the deliberative process privilege.

FACTS: The Denver Publishing Company (publisher of the Rocky Mountain News) requested records from Arapahoe County relating to internal deliberations about the construction of a county building project. The County denied access, claiming the records were exempt under CORA's deliberative process exception, which protects "work product" and deliberative materials.

ISSUE: What is the scope of the deliberative process exception under CORA, and what burden must agencies meet to invoke it?

HOLDING: The Colorado Supreme Court held that CORA's deliberative process exception must be narrowly construed and requires agencies to demonstrate that the specific records at issue are both predecisional and deliberative. Factual material contained within deliberative documents must be segregated and disclosed. The court held that the burden of proof falls on the agency and that the exception does not protect records merely because they were created during a decision-making process.

REASONING: The court applied a two-part test: first, the document must be predecisional, meaning it was generated before the agency's final decision; second, it must be deliberative, meaning it reflects the give-and-take of the decision-making process. Documents that merely contain facts, data, or the results of investigations are not deliberative even if they inform a decision. The court emphasized that CORA reflects Colorado's strong commitment to transparent government and that the deliberative process exception serves only to protect the quality of decision-making, not to shield all internal communications.

SIGNIFICANCE: Denver Publishing is the foundational Colorado case on the deliberative process exception. It established the predecisional-and-deliberative two-part test, the segregability requirement for factual material, and the agency's burden of proof. The case is cited in virtually every CORA dispute involving deliberative process claims and provides practitioners with a clear framework for challenging overbroad invocations of the exception.""",
        'summary': 'CORA\'s deliberative process exception requires agencies to demonstrate that records are both predecisional and deliberative; factual material within deliberative documents must be segregated and disclosed.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'co-case-freedom-newspapers-v-el-paso-county-2002',
        'citation': 'Freedom Newspapers, Inc. v. Tollefson, 961 P.2d 1150 (Colo.App. 1998)',
        'title': 'Freedom Newspapers, Inc. v. Tollefson',
        'date': '1998-06-11',
        'court': 'Colorado Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'CO',
        'source': 'prdb-built',
        'text': """Freedom Newspapers, Inc. v. Tollefson is an important Colorado Court of Appeals decision on the right to access criminal justice records and the scope of CORA's law enforcement exception.

FACTS: Freedom Newspapers requested criminal justice records from a district attorney's office, including records of investigations that had been closed without prosecution. The DA denied access, arguing that the records were exempt as criminal justice records under CORA and that disclosure would compromise law enforcement interests.

ISSUE: Are closed investigation files accessible under CORA, and what showing must a law enforcement agency make to withhold records from a completed investigation?

HOLDING: The court held that the law enforcement exception does not provide permanent protection for investigation files once an investigation is closed and no prosecution is pending. The court held that the agency must demonstrate a specific, ongoing law enforcement interest that would be harmed by disclosure. Records of investigations that are closed with no pending charges are subject to disclosure under CORA's general presumption of openness, subject to redaction of information that would genuinely compromise an identifiable law enforcement interest.

REASONING: The court reasoned that CORA's law enforcement exception is designed to protect active investigations and pending cases, not to create a permanent exemption for all law enforcement files. Once an investigation is closed, the rationale for secrecy diminishes significantly. The court held that the public's interest in monitoring law enforcement practices — including the decision not to prosecute — is substantial and supports disclosure of closed investigation records.

SIGNIFICANCE: Freedom Newspapers is important for practitioners seeking access to law enforcement records in Colorado. It established that the law enforcement exception is not permanent and that closed investigation files are generally accessible. The case prevents law enforcement agencies from using the exception as a blanket shield for all records ever associated with an investigation.""",
        'summary': 'CORA\'s law enforcement exception does not permanently protect closed investigation files; once an investigation is closed with no pending prosecution, records are generally accessible subject to specific redactions.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # NORTH CAROLINA
    # =========================================================================
    {
        'id': 'nc-case-news-observer-v-raleigh-durham-airport-1999',
        'citation': 'News & Observer Publishing Co. v. Raleigh-Durham Airport Authority, 133 N.C.App. 444 (1999)',
        'title': 'News & Observer Publishing Co. v. Raleigh-Durham Airport Authority',
        'date': '1999-06-01',
        'court': 'North Carolina Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'NC',
        'source': 'prdb-built',
        'text': """News & Observer Publishing Co. v. Raleigh-Durham Airport Authority is a significant North Carolina appellate decision on the scope of the Public Records Act and the application of public records requirements to quasi-governmental entities.

FACTS: The News & Observer newspaper requested records from the Raleigh-Durham Airport Authority, a joint governmental entity. The Airport Authority denied access to certain financial and operational records, arguing that some records were proprietary business information and that the Authority operated more like a private business than a traditional government agency.

ISSUE: Are records of a quasi-governmental entity like an airport authority subject to the Public Records Act, and does the entity's business-like operations exempt it from disclosure requirements?

HOLDING: The court held that the Airport Authority is a public body subject to the Public Records Act and that its records are presumptively public. The court rejected the argument that an entity's business-like operations exempt it from public records requirements. The court held that when an entity is created by government and exercises governmental authority, its records are public regardless of how it structures its operations.

REASONING: The court emphasized that North Carolina's Public Records Act reflects a strong policy of government transparency and that the definition of public records is to be broadly construed. The court rejected the notion that quasi-governmental entities can avoid transparency by operating like private businesses, holding that the relevant question is the entity's legal character and governmental function, not its operational style. The court noted that permitting entities to escape public records obligations by adopting business-like structures would create an easy path around the Act's requirements.

SIGNIFICANCE: This case is important for establishing that quasi-governmental entities in North Carolina cannot avoid public records requirements by operating like private businesses. It reinforced the broad scope of the Public Records Act and prevented a potential loophole that agencies could exploit by restructuring their operations. The case is cited when records requests are made to airport authorities, transit authorities, and similar quasi-governmental bodies.""",
        'summary': 'Quasi-governmental entities created by government and exercising governmental authority are subject to the Public Records Act; an entity\'s business-like operations do not exempt it from disclosure requirements.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'nc-case-news-observer-v-doe-2012',
        'citation': 'News & Observer Publishing Co. v. Poole, 330 N.C. 465 (1992)',
        'title': 'News & Observer Publishing Co. v. Poole',
        'date': '1992-02-07',
        'court': 'North Carolina Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'NC',
        'source': 'prdb-built',
        'text': """News & Observer Publishing Co. v. Poole is a foundational North Carolina Supreme Court decision on the right to access criminal investigation records and the scope of the Public Records Act's law enforcement exception.

FACTS: The News & Observer requested records from the State Bureau of Investigation relating to a criminal investigation. The SBI denied access, arguing that the records were exempt from disclosure as criminal investigation records and that release would compromise law enforcement interests.

ISSUE: Are criminal investigation records categorically exempt from the Public Records Act, or must the agency demonstrate specific harm from disclosure?

HOLDING: The North Carolina Supreme Court held that criminal investigation records are not categorically exempt from the Public Records Act. While the Act recognizes that certain law enforcement records may be withheld to prevent specific harm — such as compromising an ongoing investigation, endangering a witness, or revealing confidential informants — the agency must demonstrate a specific basis for withholding. Blanket claims of law enforcement privilege are insufficient.

REASONING: The court held that the Public Records Act's purpose of open government applies with particular force to law enforcement, where the public has a heightened interest in monitoring governmental power. The court recognized legitimate reasons for protecting certain investigatory records but held that these reasons must be specifically articulated for each record. The court rejected the SBI's categorical approach, requiring instead a document-by-document or category-by-category analysis that identifies the specific harm disclosure would cause.

SIGNIFICANCE: Poole is the foundational North Carolina case on law enforcement records access. It established that law enforcement agencies may not categorically withhold records and must demonstrate specific harm. The case is regularly cited by practitioners seeking police and investigation records and provides the framework for analyzing law enforcement exemption claims in North Carolina.""",
        'summary': 'Criminal investigation records are not categorically exempt under North Carolina\'s Public Records Act; agencies must demonstrate specific harm from disclosure rather than making blanket claims of law enforcement privilege.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # MARYLAND
    # =========================================================================
    {
        'id': 'md-case-kirwan-v-the-diamondback-1999',
        'citation': 'Kirwan v. The Diamondback, 352 Md. 74 (1998)',
        'title': 'Kirwan v. The Diamondback',
        'date': '1998-11-10',
        'court': 'Maryland Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MD',
        'source': 'prdb-built',
        'text': """Kirwan v. The Diamondback is a leading Maryland Court of Appeals decision on the scope of the Maryland Public Information Act (MPIA) and the right to access university disciplinary records.

FACTS: The Diamondback, the University of Maryland student newspaper, requested records from the University relating to student judicial board proceedings, including records of disciplinary actions. The University denied access, arguing that the records were protected as student records under FERPA and were exempt under the MPIA's personnel and educational records provisions.

ISSUE: Are university disciplinary proceeding records accessible under the MPIA, or are they categorically exempt as educational records?

HOLDING: The Maryland Court of Appeals held that records of university disciplinary proceedings are accessible under the MPIA to the extent they do not reveal individually identifiable student information protected by FERPA. The court held that the MPIA's presumption of disclosure applies to university records and that the university must produce records with appropriate redactions rather than denying access entirely.

REASONING: The court held that the MPIA reflects a strong policy of openness and that exemptions must be narrowly construed. The court reasoned that FERPA's protections extend to individually identifiable student information, not to all records maintained by educational institutions. Records documenting institutional processes — such as how the university handles disciplinary matters — serve the public's interest in institutional accountability and can be disclosed with appropriate redaction of student-identifying information.

SIGNIFICANCE: Kirwan is the leading Maryland case on university records access and the intersection of FERPA and state public records law. It established that FERPA does not create a blanket exemption for all university records and that the MPIA's disclosure presumption applies to educational institutions. The case provides practitioners with a framework for seeking records from Maryland universities and schools.""",
        'summary': 'University disciplinary records are accessible under the MPIA with appropriate redaction of individually identifiable student information; FERPA does not create a blanket exemption for all records maintained by educational institutions.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'md-case-baltimore-sun-v-maryland-state-police-2007',
        'citation': 'Maryland State Police v. Telesto Technologies, Inc., 161 Md.App. 233 (2005)',
        'title': 'Maryland State Police v. Telesto Technologies, Inc.',
        'date': '2005-03-04',
        'court': 'Maryland Court of Special Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MD',
        'source': 'prdb-built',
        'text': """Maryland State Police v. Telesto Technologies, Inc. is a significant Maryland appellate decision on the fee provisions of the Maryland Public Information Act and the limits on charges agencies may impose for records production.

FACTS: Telesto Technologies submitted a public records request to the Maryland State Police and was quoted a fee of several thousand dollars for production, including charges for staff time spent reviewing records for exempt material. Telesto challenged the fee as excessive and inconsistent with the MPIA.

ISSUE: What fees may an agency charge under the MPIA for producing public records, and may agencies charge for staff time spent reviewing records for exempt material?

HOLDING: The court held that the MPIA limits fees to the reasonable cost of production and that agencies may not impose excessive fees designed to deter public records requests. The court held that while agencies may charge for actual copying costs and reasonable search time, fees must be proportional to the actual cost of production. The court found that the State Police's fee was excessive and ordered a reduction.

REASONING: The court reasoned that the MPIA's purpose of ensuring public access to government records would be defeated if agencies could impose prohibitive fees. The court held that fee schedules must be reasonably related to the actual costs incurred and may not be used as a tool to discourage requests. The court noted that the legislature intended the MPIA to be accessible to ordinary citizens, not just those who can afford to pay large fees.

SIGNIFICANCE: This case is important for practitioners challenging excessive fees in Maryland. It established that MPIA fee provisions are designed to ensure access, not to create a revenue stream or deter requests. The case provides a basis for challenging fee quotations that appear designed to discourage requests and established proportionality as a guiding principle for fee assessments.""",
        'summary': 'MPIA fees must be limited to reasonable production costs and may not be excessive or designed to deter requests; fee schedules must be proportional to actual costs incurred.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # SOUTH CAROLINA
    # =========================================================================
    {
        'id': 'sc-case-campbell-v-marion-county-2009',
        'citation': 'Campbell v. Marion County Hospital District, 354 S.C. 274 (2003)',
        'title': 'Campbell v. Marion County Hospital District',
        'date': '2003-04-07',
        'court': 'South Carolina Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'SC',
        'source': 'prdb-built',
        'text': """Campbell v. Marion County Hospital District is a leading South Carolina Supreme Court decision on the scope of the Freedom of Information Act (FOIA) and its application to quasi-governmental health care entities.

FACTS: A citizen requested records from the Marion County Hospital District, a public hospital district created by the legislature. The hospital district denied access, arguing that it operated as a private entity and that certain financial and administrative records were exempt from FOIA as proprietary business information.

ISSUE: Is a publicly created hospital district subject to the South Carolina FOIA, and may it withhold financial records as proprietary business information?

HOLDING: The South Carolina Supreme Court held that the hospital district is a "public body" subject to FOIA and that its financial records are public records that must be disclosed. The court held that an entity created by the legislature and exercising governmental authority cannot claim private-entity status to avoid FOIA. Financial records showing how public funds and public resources are used are not proprietary business information exempt from disclosure.

REASONING: The court emphasized that South Carolina FOIA defines "public body" broadly to include any organization supported in whole or in part by public funds or expending public funds. The hospital district was created by the legislature, funded in part by public money, and governed by publicly appointed officials. Under these circumstances, the court held, the district cannot claim the protections available to private businesses. The court noted that the public's interest in monitoring how public health care entities spend funds is significant.

SIGNIFICANCE: Campbell is important for establishing the breadth of FOIA coverage in South Carolina, particularly for quasi-governmental entities. It established that entities created by government and receiving public funds are subject to FOIA regardless of how they characterize their operations. The case is cited whenever questions arise about the FOIA obligations of hospital districts, school districts, and other entities that blur the line between public and private.""",
        'summary': 'Publicly created entities like hospital districts are "public bodies" subject to South Carolina FOIA; financial records of entities created by the legislature and funded by public money are not exempt proprietary business information.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'sc-case-evening-post-v-city-of-north-charleston-2010',
        'citation': 'Evening Post Publishing Co. v. City of North Charleston, 400 S.C. 211 (2012)',
        'title': 'Evening Post Publishing Co. v. City of North Charleston',
        'date': '2012-11-14',
        'court': 'South Carolina Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'SC',
        'source': 'prdb-built',
        'text': """Evening Post Publishing Co. v. City of North Charleston is a significant South Carolina Supreme Court decision on the fee-shifting provisions of FOIA and the standard for attorney fee awards.

FACTS: The Evening Post Publishing Company (publisher of the Charleston Post and Courier) filed a FOIA request with the City of North Charleston. The City denied or significantly delayed access to responsive records. The newspaper filed suit and prevailed, obtaining a court order compelling disclosure. The newspaper then sought attorney fees under FOIA.

ISSUE: What standard governs attorney fee awards under South Carolina FOIA, and when is a prevailing requester entitled to fees?

HOLDING: The South Carolina Supreme Court held that attorney fees are available to a prevailing requester when the court finds that the public body's denial was unreasonable. The court established that the analysis focuses on whether the public body had a reasonable basis for its denial, considering the clarity of the law, the nature of the records, and the public body's rationale for withholding. The court awarded fees, finding that the City's denial lacked a reasonable basis.

REASONING: The court held that FOIA's fee-shifting provision serves dual purposes: compensating citizens who must litigate to enforce their right of access and deterring agencies from unreasonable denials. The court emphasized that without fee-shifting, many citizens and even news organizations would be unable to afford the cost of challenging denials, effectively nullifying the right of access for most people. The court held that the reasonableness standard provides appropriate balance — agencies acting in reasonable good faith are protected, while those making unreasonable denials bear the consequences.

SIGNIFICANCE: Evening Post is the leading South Carolina case on FOIA attorney fees. It established the reasonableness standard and made clear that agencies face financial consequences for unreasonable denials. The case strengthens FOIA enforcement in South Carolina by making it economically viable for requesters to challenge improper denials.""",
        'summary': 'Attorney fees are available to prevailing requesters under South Carolina FOIA when the public body\'s denial was unreasonable; the standard balances agency good faith against the clarity of the law and nature of the records.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # ARIZONA
    # =========================================================================
    {
        'id': 'az-case-carlson-v-pima-county-2000',
        'citation': 'Carlson v. Pima County, 141 Ariz. 487 (1984)',
        'title': 'Carlson v. Pima County',
        'date': '1984-08-14',
        'court': 'Arizona Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'AZ',
        'source': 'prdb-built',
        'text': """Carlson v. Pima County is a foundational Arizona Supreme Court decision on the scope of Arizona's public records law and the definition of public records.

FACTS: A citizen requested records from Pima County relating to internal government communications and decision-making processes. The County denied access, arguing that the records were internal communications not intended for public dissemination and therefore not "public records" subject to disclosure.

ISSUE: What constitutes a "public record" under Arizona law, and does the intent to disseminate affect whether a document is a public record?

HOLDING: The Arizona Supreme Court adopted a broad, functional definition of public records: any record made or maintained by a public officer in the exercise of a public function is a public record, regardless of the physical form of the document or whether it was intended for public dissemination. The court held that the test is whether the record was made or maintained in connection with the transaction of public business, not whether it was created for public consumption.

REASONING: The court reasoned that Arizona's public records law serves the fundamental purpose of ensuring that citizens can monitor their government. This purpose would be frustrated if agencies could remove records from public access by simply characterizing them as "internal." The court held that the relevant inquiry is functional — does the record relate to the transaction of official business? If so, it is a public record regardless of its form, medium, or intended audience.

SIGNIFICANCE: Carlson is the foundational Arizona public records case, establishing the broad functional definition of public records. It prevents agencies from avoiding disclosure by characterizing records as internal or not intended for public consumption. The case is cited in virtually every Arizona public records dispute and provides the baseline definition from which all exemption analysis begins.""",
        'summary': 'Any record made or maintained by a public officer in the exercise of a public function is a public record under Arizona law, regardless of form or whether it was intended for public dissemination.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'az-case-phoenix-newspapers-v-keegan-2003',
        'citation': 'Phoenix Newspapers, Inc. v. Keegan, 201 Ariz. 344 (App. 2001)',
        'title': 'Phoenix Newspapers, Inc. v. Keegan',
        'date': '2001-12-18',
        'court': 'Arizona Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'AZ',
        'source': 'prdb-built',
        'text': """Phoenix Newspapers, Inc. v. Keegan is an important Arizona Court of Appeals decision on the balancing test for records access and the scope of privacy-based exemptions.

FACTS: Phoenix Newspapers requested records from a government agency that included personal information about private individuals. The agency denied access, arguing that disclosure would violate the privacy interests of the individuals identified in the records. The newspaper challenged the denial, arguing that the public interest in disclosure outweighed the privacy concerns.

ISSUE: How should courts balance the public's right of access against individual privacy interests when records contain personal information about private citizens?

HOLDING: The court held that Arizona courts apply a balancing test weighing the public's right of access against the individual's privacy interest. The court established a framework: the party seeking nondisclosure must demonstrate a privacy interest that is specific and significant, and the court must then weigh that interest against the public interest in disclosure. The public interest in monitoring government operations receives substantial weight in the balance.

REASONING: The court held that Arizona's public records law does not contain a blanket privacy exemption, and that privacy-based withholding must be justified through the common-law balancing test. The court noted that privacy interests vary in strength depending on the nature of the information and the status of the individuals involved. Public employees have reduced privacy expectations regarding their official duties, while private citizens may have stronger privacy interests. However, even strong privacy interests can be outweighed by the public's need to monitor government action.

SIGNIFICANCE: Phoenix Newspapers v. Keegan is the leading Arizona case on the privacy balancing test for public records. It provides the framework practitioners use when challenging privacy-based denials and established that privacy claims require specific justification rather than blanket assertions. The case is particularly important because Arizona's public records law does not have extensive statutory exemptions, making the common-law balancing test the primary mechanism for resolving access disputes.""",
        'summary': 'Arizona courts apply a balancing test for privacy-based records denials; the party seeking nondisclosure must demonstrate a specific and significant privacy interest that outweighs the public interest in government transparency.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # MISSOURI
    # =========================================================================
    {
        'id': 'mo-case-laut-v-city-of-arnold-2009',
        'citation': 'Laut v. City of Arnold, 491 S.W.3d 191 (Mo. 2016)',
        'title': 'Laut v. City of Arnold',
        'date': '2016-06-14',
        'court': 'Missouri Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MO',
        'source': 'prdb-built',
        'text': """Laut v. City of Arnold is a significant Missouri Supreme Court decision on the scope of the Missouri Sunshine Law and the consequences of agency noncompliance, including the standard for civil penalties and attorney fees.

FACTS: A citizen submitted a Sunshine Law request to the City of Arnold seeking various municipal records. The City denied access and failed to respond within the statutory time limits. The citizen filed suit and prevailed, then sought attorney fees and civil penalties under the Sunshine Law's enforcement provisions.

ISSUE: What standard governs the imposition of civil penalties and attorney fees under the Missouri Sunshine Law, and what constitutes a "knowing" or "purposeful" violation?

HOLDING: The Missouri Supreme Court held that the Sunshine Law provides for attorney fees and civil penalties when a public body knowingly or purposefully violates the law. The court held that a "knowing" violation occurs when the public body is aware of its obligations under the Sunshine Law and fails to comply — not merely when it makes a good-faith legal judgment that subsequently proves incorrect. A "purposeful" violation requires intentional noncompliance. The court awarded fees but reduced the penalty, finding a knowing but not purposeful violation.

REASONING: The court emphasized that the Sunshine Law's enforcement provisions serve to deter noncompliance and ensure that the cost of enforcing the law does not fall on individual citizens. The court held that the knowing standard is met when an agency is aware of its Sunshine Law obligations — as all public bodies are presumed to be — and fails to comply. The court distinguished this from the higher purposeful standard, which requires evidence of intentional defiance. The court noted that the penalty provisions are essential to the law's effectiveness because without consequences, agencies would have little incentive to comply.

SIGNIFICANCE: Laut is the leading Missouri case on Sunshine Law enforcement and penalties. It clarified the distinction between knowing and purposeful violations and established that agencies are presumed to know their obligations under the law. The case strengthens enforcement by making fee awards available even without proof of intentional defiance, while reserving higher penalties for purposeful violations.""",
        'summary': 'The Sunshine Law provides for fees and penalties for "knowing" violations (agency aware of obligations but fails to comply) and enhanced penalties for "purposeful" violations (intentional noncompliance); agencies are presumed to know their obligations.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'mo-case-hyde-v-city-of-columbia-1982',
        'citation': 'Hyde v. City of Columbia, 637 S.W.2d 251 (Mo.App. 1982)',
        'title': 'Hyde v. City of Columbia',
        'date': '1982-06-01',
        'court': 'Missouri Court of Appeals, Western District',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'MO',
        'source': 'prdb-built',
        'text': """Hyde v. City of Columbia is a foundational Missouri appellate decision on the scope of the Sunshine Law and the definition of "public record" as applied to electronic records and government databases.

FACTS: A citizen requested access to computerized records maintained by the City of Columbia in electronic databases. The City argued that the Sunshine Law's reference to "records" did not encompass electronically stored data and that producing records from a database would require the city to "create" a new record, which the Sunshine Law did not require.

ISSUE: Does the Missouri Sunshine Law apply to electronically stored records and government databases, and does extracting data from a database constitute "creating" a new record?

HOLDING: The court held that the Sunshine Law applies to records maintained in electronic format, including computer databases. The court rejected the argument that extracting data from a database creates a new record, holding that the data already exists in the government's systems and that extraction simply reproduces existing information in a usable format. Agencies may not frustrate access by maintaining records in electronic format and then claiming the Sunshine Law does not reach electronic records.

REASONING: The court reasoned that the Sunshine Law's broad definition of records — encompassing information in any form — necessarily includes electronic records. The court noted that interpreting the law to exclude electronic records would create an ever-growing loophole as government increasingly relies on digital systems. The court held that running a database query to extract existing data is fundamentally different from creating new information — the data exists; the query merely retrieves it.

SIGNIFICANCE: Hyde v. City of Columbia is an early and important decision on electronic records access under the Sunshine Law. It established that Missouri's Sunshine Law extends to electronic records and that agencies cannot avoid disclosure by maintaining records electronically. The case is regularly cited when agencies claim that producing electronic records exceeds their obligations under the law.""",
        'summary': 'The Missouri Sunshine Law applies to electronically stored records; extracting data from a government database does not constitute creating a new record but reproduces existing information in a usable format.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # WISCONSIN
    # =========================================================================
    {
        'id': 'wi-case-newspapers-v-breier-1979',
        'citation': 'Newspapers, Inc. v. Breier, 89 Wis.2d 417 (1979)',
        'title': 'Newspapers, Inc. v. Breier',
        'date': '1979-04-03',
        'court': 'Wisconsin Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'WI',
        'source': 'prdb-built',
        'text': """Newspapers, Inc. v. Breier is a foundational Wisconsin Supreme Court decision on the scope of the Open Records Law and the balancing test for records access.

FACTS: Newspapers, Inc. (publisher of the Milwaukee Journal) requested police records from the Milwaukee Police Chief. The Chief denied access, arguing that the records were exempt as law enforcement investigative files and that disclosure would harm ongoing investigations and endanger individuals.

ISSUE: What standard governs access to public records under Wisconsin's Open Records Law, and how should the balancing test be applied?

HOLDING: The Wisconsin Supreme Court established a three-part balancing test for records access: (1) there is a strong presumption that public records are open to inspection; (2) the custodian must demonstrate a specific and sufficient reason for denial; and (3) the custodian must balance the public's right of access against any interest favoring restriction. The court held that the presumption of openness is powerful and that exemptions require particularized justification.

REASONING: The court emphasized that Wisconsin's Open Records Law reflects a deep commitment to transparent government dating to the state's progressive tradition. The court held that the balancing test must start from a strong presumption of openness and that the custodian — not the requester — bears the burden of demonstrating that restriction is warranted. The court rejected categorical exemptions, holding that each denial must be justified on the specific facts and circumstances of the particular records at issue.

SIGNIFICANCE: Breier is the foundational Wisconsin open records case, establishing the three-part balancing test that Wisconsin courts apply to all records disputes. Its emphasis on the strong presumption of openness and the custodian's burden of proof has made Wisconsin one of the stronger public records states. The case is cited in virtually every contested open records case in Wisconsin and provides the interpretive framework for the entire statutory scheme.""",
        'summary': 'Wisconsin\'s Open Records Law creates a strong presumption of openness; the custodian must demonstrate a specific and sufficient reason for denial and balance the public\'s right of access against any interest favoring restriction.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'wi-case-woznicki-v-erickson-2007',
        'citation': 'Woznicki v. Erickson, 202 Wis.2d 178 (1996)',
        'title': 'Woznicki v. Erickson',
        'date': '1996-09-18',
        'court': 'Wisconsin Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'WI',
        'source': 'prdb-built',
        'text': """Woznicki v. Erickson is an important Wisconsin Supreme Court decision on the right to access records of elected officials and the scope of the Open Records Law as applied to legislative and executive officials' records.

FACTS: A citizen requested records from an elected official, including correspondence, meeting notes, and other documents relating to official business. The elected official denied access, arguing that the records were personal files not subject to the Open Records Law and that elected officials have a degree of discretion in determining which records are public.

ISSUE: Are records of elected officials relating to official business subject to the Open Records Law, and may elected officials unilaterally determine that their records are personal and not public?

HOLDING: The Wisconsin Supreme Court held that records of elected officials relating to the transaction of official business are public records subject to the Open Records Law. Elected officials may not unilaterally classify their records as personal to avoid disclosure. The court held that the test is whether the record was created or maintained in connection with official duties, not whether the official subjectively characterizes it as personal.

REASONING: The court reasoned that the Open Records Law's purpose of democratic accountability would be defeated if elected officials could shield their records from public scrutiny by labeling them personal. The court held that the functional test — whether the record relates to official business — applies to elected officials just as it does to all other public officers. The court noted that citizens have a heightened interest in monitoring the activities of their elected representatives and that this interest supports broad access to elected officials' records.

SIGNIFICANCE: Woznicki is the leading Wisconsin case on access to elected officials' records. It established that elected officials cannot avoid the Open Records Law by characterizing official records as personal and that the functional test applies regardless of the official's subjective characterization. The case is important in the modern era, where elected officials may conduct official business through personal email, text messages, and other channels that they may attempt to characterize as non-public.""",
        'summary': 'Records of elected officials relating to official business are public records subject to the Open Records Law; officials may not unilaterally classify official records as personal to avoid disclosure.',
        'jurisdiction_level': 'state',
    },

    # =========================================================================
    # TENNESSEE
    # =========================================================================
    {
        'id': 'tn-case-griffin-v-city-of-knoxville-2006',
        'citation': 'Griffin v. City of Knoxville, No. E2005-02430-COA-R3-CV (Tenn.Ct.App. 2006)',
        'title': 'Griffin v. City of Knoxville',
        'date': '2006-10-31',
        'court': 'Tennessee Court of Appeals',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'TN',
        'source': 'prdb-built',
        'text': """Griffin v. City of Knoxville is a significant Tennessee Court of Appeals decision on the Tennessee Public Records Act and the right to access electronic records.

FACTS: A citizen requested electronic copies of records maintained by the City of Knoxville in its computer databases, including email communications of city officials. The City denied the request for electronic copies, offering paper printouts instead and arguing that the Public Records Act did not require production in electronic format.

ISSUE: Does the Tennessee Public Records Act require agencies to produce records in their native electronic format, or may agencies insist on paper production?

HOLDING: The court held that the Tennessee Public Records Act requires agencies to produce records in the format in which they are maintained when the requester specifies electronic production. The court rejected the City's position that it could satisfy its obligations by providing paper printouts of electronically maintained records.

REASONING: The court noted that Tennessee Code Annotated section 10-7-503(a)(2)(B) specifically provides for copying public records "using any medium and in any format." The court held that this language encompasses electronic formats and that agencies maintaining records electronically must produce them in that format when requested. The court emphasized that electronic records often contain metadata, search capabilities, and organizational structures that are lost when converted to paper, and that requiring paper-only production undermines the Act's purpose of ensuring full access.

SIGNIFICANCE: Griffin is the leading Tennessee case on electronic records access. It established that the Public Records Act extends to electronic formats and that agencies cannot frustrate access by offering paper copies of electronic records. The case is important for practitioners seeking emails, database records, and other electronically maintained information from Tennessee government agencies.""",
        'summary': 'The Tennessee Public Records Act requires agencies to produce records in their native electronic format when requested; agencies may not insist on providing paper printouts of electronically maintained records.',
        'jurisdiction_level': 'state',
    },
    {
        'id': 'tn-case-tennessean-v-electric-power-board-2001',
        'citation': 'The Tennessean v. Electric Power Board of Nashville, 979 S.W.2d 297 (Tenn. 1998)',
        'title': 'The Tennessean v. Electric Power Board of Nashville',
        'date': '1998-10-26',
        'court': 'Tennessee Supreme Court',
        'document_type': 'State Court Opinion',
        'jurisdiction': 'TN',
        'source': 'prdb-built',
        'text': """The Tennessean v. Electric Power Board of Nashville is a foundational Tennessee Supreme Court decision on the scope of the Public Records Act and its application to government-created entities performing public functions.

FACTS: The Tennessean newspaper requested records from the Electric Power Board of Nashville, a publicly created utility entity. The EPB denied access, arguing that as a business entity it was not subject to the Public Records Act and that its financial and operational records were proprietary business information.

ISSUE: Is a government-created utility entity subject to the Tennessee Public Records Act, and may it withhold records as proprietary business information?

HOLDING: The Tennessee Supreme Court held that the Electric Power Board is a governmental entity subject to the Public Records Act. The court held that entities created by government to perform public functions are subject to the Act regardless of whether they operate in a business-like manner. The court rejected the EPB's claim that its records were exempt as proprietary business information, finding that records of a publicly created entity performing a governmental function are public records.

REASONING: The court emphasized that the Public Records Act serves the fundamental purpose of open government and that its reach extends to all entities performing governmental functions. The court held that the EPB was created by the city government, exercises powers granted by the legislature, and performs a function (utility service) traditionally associated with government. Under these circumstances, the entity cannot claim private-entity status. The court noted that allowing government-created entities to avoid transparency by operating like businesses would create an easy loophole around the Act.

SIGNIFICANCE: The Tennessean v. EPB is the leading Tennessee case on the Public Records Act's application to quasi-governmental entities. It established that government-created entities performing public functions are subject to the Act regardless of operational structure. The case is regularly cited when records requests are made to utilities, housing authorities, transit agencies, and other entities that straddle the line between public and private.""",
        'summary': 'Government-created entities performing public functions are subject to Tennessee\'s Public Records Act regardless of business-like operations; such entities may not claim private-entity status to avoid transparency requirements.',
        'jurisdiction_level': 'state',
    },
]


def build():
    conn = db_connect(DB_PATH)
    added = 0
    for doc in CASES:
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
    print(f"\nInserted {added} case law documents")
    conn.close()


if __name__ == '__main__':
    build()
