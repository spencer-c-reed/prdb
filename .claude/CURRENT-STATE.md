# PRDB Current State

## Status: Phase 5 Complete — Skills Integrated, All Jurisdictions Live

**Last updated:** 2026-03-26 06:24 PM EDT

### What's Built
- [x] SQLite schema (v1) with all tables, FTS5 full-text search
- [x] Ingestion utilities (dedup, normalize, metadata, receipt, pdf_extract)
- [x] Query engine (fetch_json.py) with domain detection, type expansion
- [x] Flask web app (port 8402) with 12 HTML templates
- [x] Federal FOIA foundation: statutes, 413 agencies, 76 case law opinions, OIP guidance, OGIS docs
- [x] All 50 states + DC + federal: 569 exemptions, 717 response rules, 159 templates
- [x] 23/23 tests passing
- [x] Three OpenClaw skills: /prdb-research, /prdb-request, /prdb-appeal

### Database
- Path: db/prdb.db
- Documents: 120
- Agencies: 413
- Exemptions: 569
- Response Rules: 717
- Templates: 159
- Jurisdictions: 52

### Skills
- `/prdb-research` — Query the database, compare jurisdictions, find exemptions/rules
- `/prdb-request` — Generate a complete PIA request letter for any jurisdiction
- `/prdb-appeal` — Generate an appeal using counter-arguments from the exemptions catalog

### What's Next (Phase 6: Enrichment)
- State agency directories (state-level FOIA offices)
- Jurisdiction scorecards (transparency rankings)
- Open meetings coverage
- Municipal coverage
- Cron-driven ingestion for case law freshness
- Nginx/systemd deployment
