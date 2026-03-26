# PRDB Tracker — Single Source of Truth

## Project Status: Phase 7 Complete — Analytical Features Live

**Last updated:** 2026-03-26 07:17 PM EDT

**Placeholder name:** "prdb" — will be replaced with final project name.
To rename: `grep -r "prdb\|PRDB" --include="*.py" --include="*.html" --include="*.json" --include="*.sql" --include="*.md" -l`

## Corpus Stats

| Metric | Count |
|--------|-------|
| Documents | 120 |
| Exemptions | 569 |
| Agencies | 413 |
| Response Rules | 717 |
| Templates | 159 |
| Jurisdictions | 52 (50 states + DC + federal) |
| FTS5 indexed | 120 |
| Tests | 23/23 passing |

## Phase Progress

### Phase 0: Scaffolding [COMPLETE]
- [x] Directory structure
- [x] Schema v1 (documents, exemptions, agencies, response_rules, request_templates, campaigns, requests, request_events, response_documents, citations)
- [x] FTS5 with triggers
- [x] Ingestion utilities (dedup, normalize, metadata, receipt, pdf_extract)
- [x] Query engine (fetch_json.py) with domain detection, type expansion, alias injection
- [x] Flask app + 12 HTML templates
- [x] Config files (document_types, domain_signals, coverage_requirements, sqlite_helpers)
- [x] Documentation (PROJECT-SPEC.md, PROJECT-BRIEF.md, CURRENT-STATE.md)

### Phase 1: Federal Foundation [COMPLETE]
- [x] Federal FOIA statute — 5 U.S.C. §§ 552, 552a, 552b (Cornell LII)
- [x] FOIA.gov agency directory — 413 federal agencies with contact info
- [x] OGIS advisory opinions — 19 documents
- [x] DOJ OIP guidance memos — 7 documents
- [x] Federal FOIA case law — 76 circuit court opinions (CourtListener)
- [x] Federal exemptions catalog — 12 (9 exemptions + 3 exclusions) with counter-arguments
- [x] Federal response rules — 16 rules covering all deadline/fee categories
- [x] Federal request templates — 6 templates (general, emails, contracts, police, appeal, first party)
- [x] FOIA.gov API key registered (heyspencebot@gmail.com)
- [x] Coverage audit + smoke tests

### Phase 2: Priority States (NY, CA, TX) [COMPLETE]
- [x] NY: 7 statute sections, 11 exemptions, 17 rules, 6 templates
- [x] CA: 7 statute sections, 12 exemptions, 19 rules, 5 templates
- [x] TX: 1 statute (full chapter), 17 exemptions, 28 rules, 7 templates

### Phase 3: Canvass 10 States [COMPLETE]
- [x] FL, MA, AZ, MI, MN, MO, ME, VT, NE, WA

### Phase 4: All Remaining States + DC [COMPLETE]
- [x] OH, PA, IL, GA, NC, NJ, VA, MD, CT, OR
- [x] CO, SC, AL, LA, KY
- [x] TN, IN, WI, OK, IA, KS, MS, AR, UT, NV
- [x] NM, WV, HI, ID, NH
- [x] RI, MT, DE, SD, ND, AK, WY, DC

### Phase 5: Skill Integration [COMPLETE]
- [x] Research skill (prdb-research)
- [x] Request skill (prdb-request)
- [x] Appeal skill (prdb-appeal)

### Phase 6: Web Interface [COMPLETE]
- [x] React + Vite static site with HashRouter
- [x] GitHub Pages deployment (spencer-c-reed.github.io/prdb/)
- [x] MiniSearch client-side full-text search
- [x] Jurisdiction detail pages, exemption catalog, agency directory, template library
- [x] Side-by-side jurisdiction comparison tool

### Phase 7: Analytical Features [COMPLETE]
- [x] Transparency scorecards (A+ through F grading, 9 scoring factors)
- [x] Deadline rankings (sorted by calendar-equivalent response time)
- [x] Fee comparison (per-page copy fee table with distribution chart)
- [x] Penalty comparison (attorney fees, civil/criminal penalties, per diem)
- [x] Exemption category crosswalk (24 categories across jurisdictions)
- [x] Appeal pathway summaries (admin vs judicial step flows)
- [x] Model provision flags (best-in-class features highlighted)

### Phase 8: Gap Filling [IN PROGRESS]

#### 8A: State Agency Directories [IN PROGRESS]
- [ ] All 51 non-federal jurisdictions have 0 agencies (federal has 413)
- [ ] Target: ~15-25 key agencies per state (governor, AG, state police, DOT, health, education, corrections, environment, etc.)
- [ ] Include: name, abbreviation, portal_url, email, submission_method

#### 8B: Appeal Templates [NOT STARTED]
- [ ] Only 11 of 52 jurisdictions have appeal templates (CA, DC, FL, MA, ME, MI, MN, NY, TX, VT, federal)
- [ ] Remaining 41 states need appeal letter templates

#### 8C: Template Expansion [NOT STARTED]
- [ ] NE has only 1 template; AZ, MA, ME, MI, MO, VT, WA have only 2
- [ ] Most states have only 3 templates (general + law enforcement + contracts)
- [ ] Missing types: body camera, education, personnel, electronic records, financial

#### 8D: State Statutes as Documents [NOT STARTED]
- [ ] 48 jurisdictions have 0 source documents (only federal=105, CA=7, NY=7, TX=1)
- [ ] Need: statute text for each state's public records law

#### 8E: State Case Law / AG Opinions [NOT STARTED]
- [ ] 0 state-level case law documents
- [ ] 0 state AG advisory opinions
- [ ] Many states publish FOIA guidance/advisory opinions

### Phase 9: Future Enrichment [NOT STARTED]
- [ ] Open meetings coverage
- [ ] Municipal coverage
- [ ] Scorecards with weighted user-configurable factors

## Infrastructure

| Component | Status |
|-----------|--------|
| Database | db/prdb.db (120 docs, schema v1) |
| Flask app | app.py (port 8402) |
| Query engine | fetch_json.py |
| Web (static) | React + Vite → GitHub Pages |
| Live URL | https://spencer-c-reed.github.io/prdb/ |
| Cron | Not configured yet |
| Nginx | Not configured yet |
| Systemd | Not configured yet |

## Verify Command
```bash
cd ~/projects/prdb && sqlite3 db/prdb.db "SELECT 'documents:', COUNT(*) FROM documents WHERE parent_id IS NULL UNION ALL SELECT 'exemptions:', COUNT(*) FROM exemptions UNION ALL SELECT 'agencies:', COUNT(*) FROM agencies UNION ALL SELECT 'templates:', COUNT(*) FROM request_templates UNION ALL SELECT 'rules:', COUNT(*) FROM response_rules;"
```
