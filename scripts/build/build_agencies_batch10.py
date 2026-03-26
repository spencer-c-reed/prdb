#!/usr/bin/env python3
"""Build state agency directories for AK, WY, DC."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ingest.utils.dedup import db_connect

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

AGENCIES = [
    # =========================================================================
    # ALASKA (AK) — Alaska Public Records Act, AS 40.25.100-40.25.220
    # FOIA Officer title: "Public Records Officer"
    # =========================================================================
    {'name': 'Alaska Governor\'s Office', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': None, 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Executive office of the Governor.'},
    {'name': 'Alaska Department of Law', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DOL', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'State attorney general\'s office. Issues public records opinions.'},
    {'name': 'Alaska Department of Public Safety', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DPS', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Includes Alaska State Troopers. Statewide law enforcement.'},
    {'name': 'Alaska Department of Education and Early Development', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DEED', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'State education agency. Oversees K-12 and early childhood programs.'},
    {'name': 'Alaska Department of Health and Social Services', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DHSS', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Public health, Medicaid, behavioral health, and social services.'},
    {'name': 'Alaska Department of Transportation and Public Facilities', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'ADOT&PF', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'State highways, airports, harbors, and public facilities.'},
    {'name': 'Alaska Department of Corrections', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DOC', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'State prison and community corrections system.'},
    {'name': 'Alaska Office of the Lieutenant Governor', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': None, 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Serves as Secretary of State equivalent. Elections, corporations, notaries.'},
    {'name': 'Alaska Department of Revenue', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DOR', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Tax administration and Permanent Fund Dividend. Individual tax records confidential.'},
    {'name': 'Alaska Department of Environmental Conservation', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DEC', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Environmental regulation, spill prevention, water and air quality.'},
    {'name': 'Alaska Department of Labor and Workforce Development', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DOLWD', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Unemployment insurance, workers\' compensation, workforce programs.'},
    {'name': 'Alaska Department of Commerce, Community, and Economic Development', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DCCED', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Business licensing, banking regulation, community assistance.'},
    {'name': 'Alaska Department of Natural Resources', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DNR', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'State lands, oil and gas leasing, mining, forestry, parks.'},
    {'name': 'Alaska Department of Fish and Game', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'ADF&G', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Wildlife and fisheries management, subsistence programs.'},
    {'name': 'Alaska Department of Military and Veterans\' Affairs', 'jurisdiction': 'AK', 'level': 'state', 'abbreviation': 'DMVA', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Public Records Officer', 'notes': 'Alaska National Guard, veterans\' services, emergency management.'},

    # =========================================================================
    # WYOMING (WY) — Wyoming Public Records Act, Wyo. Stat. § 16-4-201 et seq.
    # FOIA Officer title: "Records Officer"
    # =========================================================================
    {'name': 'Wyoming Governor\'s Office', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': None, 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Executive office of the Governor.'},
    {'name': 'Wyoming Attorney General\'s Office', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'AG', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'State attorney general. Division of Criminal Investigation provides statewide law enforcement.'},
    {'name': 'Wyoming Division of Criminal Investigation', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'DCI', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Under AG\'s office. Includes Wyoming Highway Patrol, criminal investigations, and forensic lab.'},
    {'name': 'Wyoming Department of Education', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'WDE', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'State education agency.'},
    {'name': 'Wyoming Department of Health', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'WDH', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Public health, Medicaid, behavioral health, aging services.'},
    {'name': 'Wyoming Department of Transportation', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'WYDOT', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'State highways, aeronautics, and driver services.'},
    {'name': 'Wyoming Department of Corrections', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'WDOC', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'State prison and community corrections system.'},
    {'name': 'Wyoming Secretary of State', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'SOS', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Elections, business filings, administrative rules.'},
    {'name': 'Wyoming Department of Revenue', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'DOR', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Tax administration. Wyoming has no state income tax; primarily mineral and sales tax.'},
    {'name': 'Wyoming Department of Environmental Quality', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'DEQ', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Environmental regulation, permitting, air and water quality, land quality.'},
    {'name': 'Wyoming Department of Workforce Services', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'DWS', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Unemployment insurance, workforce development, vocational rehabilitation.'},
    {'name': 'Wyoming State Auditor', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': None, 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'State fiscal officer. Manages state payroll, claims, and financial oversight.'},
    {'name': 'Wyoming Game and Fish Department', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': None, 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Wildlife and fisheries management, hunting and fishing licenses, habitat conservation.'},
    {'name': 'Wyoming Oil and Gas Conservation Commission', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': 'WOGCC', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Oil and gas well permitting, production data, and conservation regulation.'},
    {'name': 'Wyoming Office of State Lands and Investments', 'jurisdiction': 'WY', 'level': 'state', 'abbreviation': None, 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'Records Officer', 'notes': 'Manages state trust lands, mineral royalties, and state investments.'},

    # =========================================================================
    # DISTRICT OF COLUMBIA (DC) — DC FOIA, D.C. Code § 2-531 et seq.
    # FOIA Officer title: "FOIA Officer"
    # =========================================================================
    {'name': 'Executive Office of the Mayor', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'EOM', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Office of the Mayor of the District of Columbia.'},
    {'name': 'Office of the Attorney General for the District of Columbia', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'OAG', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'DC attorney general. Independent elected official since 2014.'},
    {'name': 'Metropolitan Police Department', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'MPD', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'DC\'s primary law enforcement agency. Major FOIA volume.'},
    {'name': 'District of Columbia Public Schools', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DCPS', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'DC public school system. Student records protected by FERPA.'},
    {'name': 'DC Health', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DOH', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Public health services, vital records, health regulation.'},
    {'name': 'District Department of Transportation', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DDOT', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Streets, sidewalks, traffic, and transportation infrastructure.'},
    {'name': 'DC Department of Corrections', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DOC', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Operates the DC Jail. Sentenced felons serve time in federal BOP facilities.'},
    {'name': 'Department of Insurance, Securities and Banking', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DISB', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Regulates insurance, securities, and banking in the District.'},
    {'name': 'DC Department of Energy and Environment', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DOEE', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Environmental protection, energy policy, sustainability programs.'},
    {'name': 'Department of Employment Services', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DOES', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Unemployment insurance, workforce development, workers\' compensation.'},
    {'name': 'Child and Family Services Agency', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'CFSA', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Child welfare and protective services. Many records restricted by federal and DC law.'},
    {'name': 'Office of the Chief Financial Officer', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'OCFO', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Independent fiscal authority. Budget, tax, and revenue administration.'},
    {'name': 'Council of the District of Columbia', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': None, 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'DC\'s legislative body. 13-member council.'},
    {'name': 'Department of Consumer and Regulatory Affairs', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DCRA', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Building permits, business licensing, housing inspections, code enforcement.'},
    {'name': 'Office of Unified Communications', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'OUC', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Operates 911 and 311 call centers for the District.'},
    {'name': 'DC Fire and Emergency Medical Services Department', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'FEMS', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Fire suppression, emergency medical services, hazmat response.'},
    {'name': 'Department of Public Works', 'jurisdiction': 'DC', 'level': 'state', 'abbreviation': 'DPW', 'email': None, 'portal_url': None, 'submission_method': 'email', 'phone': None, 'mailing_address': None, 'foia_officer_title': 'FOIA Officer', 'notes': 'Trash collection, parking enforcement, fleet management, snow removal.'},
]

def build():
    conn = db_connect(DB_PATH)
    for jur in ('AK', 'WY', 'DC'):
        conn.execute('DELETE FROM agencies WHERE jurisdiction=? AND level="state"', (jur,))

    for ag in AGENCIES:
        conn.execute('''
            INSERT INTO agencies (name, jurisdiction, level, abbreviation, email, portal_url,
                                  submission_method, phone, mailing_address, foia_officer_title, notes)
            VALUES (:name, :jurisdiction, :level, :abbreviation, :email, :portal_url,
                    :submission_method, :phone, :mailing_address, :foia_officer_title, :notes)
        ''', ag)

    conn.commit()
    for jur in ('AK', 'WY', 'DC'):
        count = conn.execute('SELECT COUNT(*) FROM agencies WHERE jurisdiction=? AND level="state"', (jur,)).fetchone()[0]
        print(f'{jur}: {count} agencies')
    conn.close()

if __name__ == '__main__':
    build()
