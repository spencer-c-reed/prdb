# PRDB Tracker — Single Source of Truth

## Project Status: Phase 0 Complete — Ready for Phase 1

**Placeholder name:** "prdb" — will be replaced with final project name.
To rename: `grep -r "prdb\|PRDB" --include="*.py" --include="*.html" --include="*.json" --include="*.sql" --include="*.md" -l`

## Corpus Stats

| Metric | Count |
|--------|-------|
| Total documents | 0 |
| Exemptions | 0 |
| Agencies | 0 |
| Response rules | 0 |
| Templates | 0 |

## Phase Progress

### Phase 0: Scaffolding [COMPLETE]
- [x] Directory structure
- [x] Schema v1 (documents, exemptions, agencies, response_rules, request_templates, campaigns, requests, request_events, response_documents, citations)
- [x] FTS5 with triggers
- [x] Ingestion utilities
- [x] Query engine (fetch_json.py)
- [x] Flask app + templates
- [x] Config files
- [x] Documentation

### Phase 1: Federal Foundation [NOT STARTED]
- [ ] Federal FOIA statute (5 U.S.C. § 552)
- [ ] Privacy Act (5 U.S.C. § 552a)
- [ ] Federal FOIA regulations (28 CFR Part 16)
- [ ] Agency-specific FOIA regs
- [ ] Federal exemptions catalog (9 exemptions + 3 exclusions)
- [ ] FOIA.gov agency directory (~130 agencies)
- [ ] OGIS advisory opinions
- [ ] DOJ OIP guidance memos
- [ ] Federal FOIA case law (CourtListener)
- [ ] Federal response rules
- [ ] Federal request templates
- [ ] Federal fee schedules
- [ ] Smoke tests
- [ ] Coverage audit

### Phase 2: Priority States (NY, CA, TX) [NOT STARTED]
- [ ] NY: FOIL statute + COOG opinions + AG + court + agencies + exemptions
- [ ] CA: CPRA statute + AG + court + agencies + exemptions
- [ ] TX: TPIA statute + AG rulings + court + agencies + exemptions

### Phase 3: Canvass 10 States [NOT STARTED]
- [ ] MN, NE, AZ, MA, MI, MO, ME, VT

### Phase 4: All States [NOT STARTED]
- [ ] Remaining 37 + DC

### Phase 5: Skill Integration [NOT STARTED]
- [ ] Research skill
- [ ] Request skill
- [ ] Appeal skill

## Infrastructure

| Component | Status |
|-----------|--------|
| Database | db/prdb.db (empty, schema v1) |
| Flask app | app.py (port 8402) |
| Query engine | fetch_json.py |
| Cron | Not configured yet |
| Nginx | Not configured yet |
| Systemd | Not configured yet |

## Verify Command
```bash
cd ~/projects/prdb && sqlite3 db/prdb.db "SELECT 'documents:', COUNT(*) FROM documents WHERE parent_id IS NULL UNION ALL SELECT 'exemptions:', COUNT(*) FROM exemptions UNION ALL SELECT 'agencies:', COUNT(*) FROM agencies UNION ALL SELECT 'templates:', COUNT(*) FROM request_templates UNION ALL SELECT 'rules:', COUNT(*) FROM response_rules;"
```
