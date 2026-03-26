# PRDB Current State

## Status: Phase 0 — Scaffolding Complete

### What's Built
- [x] Project directory structure
- [x] SQLite schema (v1) with all tables
- [x] FTS5 full-text search with auto-sync triggers
- [x] Ingestion utilities (dedup, normalize, metadata, receipt, pdf_extract)
- [x] Query engine (fetch_json.py)
- [x] Flask web app with all routes
- [x] HTML templates
- [x] Config files
- [x] Project documentation

### What's Next
- Phase 1: Federal FOIA ingestion

### Database
- Path: db/prdb.db
- Port: 8402
- Documents: 0 (ready for ingestion)
