# PRDB Tracker — Single Source of Truth

## Project Status: Phase 4 Complete — All 50 States + DC + Federal

**Last updated:** 2026-03-26 06:18 PM EDT

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

### Phase 5: Skill Integration [NOT STARTED]
- [ ] Research skill (prdb-research)
- [ ] Request skill (prdb-request)
- [ ] Appeal skill (prdb-appeal)

### Phase 6: Enrichment [NOT STARTED]
- [ ] State agency directories
- [ ] Scorecards
- [ ] Open meetings coverage
- [ ] Municipal coverage

## Infrastructure

| Component | Status |
|-----------|--------|
| Database | db/prdb.db (120 docs, schema v1) |
| Flask app | app.py (port 8402) |
| Query engine | fetch_json.py |
| Cron | Not configured yet |
| Nginx | Not configured yet |
| Systemd | Not configured yet |

## Verify Command
```bash
cd ~/projects/prdb && sqlite3 db/prdb.db "SELECT 'documents:', COUNT(*) FROM documents WHERE parent_id IS NULL UNION ALL SELECT 'exemptions:', COUNT(*) FROM exemptions UNION ALL SELECT 'agencies:', COUNT(*) FROM agencies UNION ALL SELECT 'templates:', COUNT(*) FROM request_templates UNION ALL SELECT 'rules:', COUNT(*) FROM response_rules;"
```
