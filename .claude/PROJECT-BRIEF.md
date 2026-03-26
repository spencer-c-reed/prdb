# PRDB — Public Records Request Database & Assistant

Placeholder name "prdb" — will be replaced with final project name.

## What This Is

A comprehensive public records request tool combining:
1. A research corpus of every FOIA/public records statute, regulation, AG opinion, court decision, exemption, fee schedule, and agency directory across all US jurisdictions
2. An operational tool that drafts requests, routes to the right agency, tracks deadlines, generates appeals, and optionally submits requests
3. A maximally agentic LLM layer over accessible infrastructure

## Architecture

Same pattern as canvass law (election-law project):
- SQLite + FTS5 research corpus
- Flask frontend (read-only, PRAGMA query_only)
- Python query engine (fetch_json.py)
- Phased cron-driven ingestion
- OpenClaw skill integration for agent workflows

New vs canvass law: request lifecycle management, agency directory, exemption catalog, deadline calculation, appeal generation.

## Key Files

- db/prdb.db — SQLite database
- db/schema.sql — Schema definition
- fetch_json.py — Query engine
- app.py — Flask web app (port 8402)
- ingest/ — Ingestion scripts
- config/ — Document types, domain signals, coverage requirements
- PROJECT-SPEC.md — Full project specification
- TRACKER.md — Single source of truth for project state
