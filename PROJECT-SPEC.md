# PRDB: Public Records Request Database & Assistant

## Project Spec v0.1 — 2026-03-26

**Internal codename:** `prdb` (placeholder — won't false-positive against "sunshine law" in corpus text).
When final name is chosen, find-and-replace `prdb`/`PRDB` across all project files.

---

## 1. What This Is

A comprehensive public records request tool combining:

1. **A research corpus** of every FOIA/public records statute, regulation, AG opinion, court decision, exemption, fee schedule, and agency directory across all US jurisdictions
2. **An operational tool** that drafts requests, routes them to the right agency, tracks deadlines, generates appeals, and (optionally) submits requests on behalf of users
3. **A maximally agentic layer** that lets an LLM handle the entire request lifecycle end-to-end, or lets experienced users do it manually with the raw data

The architecture mirrors canvass law: SQLite + FTS5 corpus, Flask frontend, Python query engine, cron-driven ingestion, OpenClaw skill integration. The major new dimension is **active workflow management** — request drafting, submission, deadline tracking, appeals — which canvass law doesn't have.

---

## 2. Name & Branding

**Working title: Sunshine**

Rationale: "Sunshine laws" is the term of art for open records and open meetings statutes. It's short, memorable, evokes transparency, and isn't taken by any major competing tool.

**Alternatives to consider:**
- **Daylight** — similar vibe, slightly more distinctive
- **Clearlight** — evokes clarity + transparency
- **Glass** — minimal, sharp, "see through"
- **Aperture** — the opening that lets light in
- **Public Eye** — direct, descriptive

**Decision needed:** Pick a name before Phase 2 (when we build the frontend).

---

## 3. Users

### First users
Spencer and Savannah, via OpenClaw skill interface.

### Target audience (later)
- Journalists investigating public agencies
- Civic researchers and transparency advocates
- Advocacy organizations filing records requests
- General public who know what a public records request is but don't know jurisdiction-specific procedures

### Skill floor
Knows what a public records request is. Doesn't need to know which law applies, which agency to contact, what exemptions exist, or how to appeal.

### Access model
- **Research corpus:** Open, no auth required (browse statutes, exemptions, case law, AG opinions)
- **Request tools + LLM layer:** Backend-controlled, skill-gated (like canvass law's agent API)
- **Request tracking:** Requires account (deferred — build schema now, add auth later)
- **Public registry:** Opt-in sharing of request metadata and outcomes (deferred)

---

## 4. Architecture

### Stack (mirrors canvass law)

| Layer | Technology |
|-------|-----------|
| Database | SQLite + FTS5 (single file, WAL mode) |
| Query engine | Python CLI (`fetch_json.py` equivalent) |
| Web frontend | Flask (read-only, PRAGMA query_only) |
| Ingestion | Python scripts, three-tier cron (daily/weekly/monthly) |
| Summarization | Gemini Flash Lite (cost-efficient bulk) |
| Agent layer | OpenClaw skill (research + request workflow) |
| Hosting | VPS (localhost, Tailscale-gated) |
| Port | TBD (not 8401, that's election-law) |

### What's new vs. canvass law
- **Request lifecycle tables** — campaigns, requests, state machine, deadline tracking
- **Agency directory** — structured, kept fresh via automated scraping
- **Exemption catalog** — first-class entities with structured metadata
- **Deadline calculation engine** — jurisdiction-aware, business-day-aware
- **Template system** — model request language with fill-in fields
- **Submission guidance** — per-agency instructions (portal URL, email, mailing address, required forms)
- **Appeal generation** — LLM-drafted appeals citing case law and AG opinions from the corpus

---

## 5. Database Schema

### 5.1 Research Corpus Tables

#### `documents`
The core corpus table. Same pattern as canvass law.

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    citation TEXT,              -- canonical citation (e.g., "N.Y. Pub. Off. Law § 87")
    title TEXT NOT NULL,
    date TEXT,                  -- ISO 8601
    court TEXT,                 -- court or issuing body
    document_type TEXT NOT NULL,-- from document_types.json
    jurisdiction TEXT,          -- "Federal", "NY", "CA", "TX", etc.
    source TEXT,                -- origin system/URL
    source_url TEXT,
    text TEXT,                  -- full text
    summary_ai TEXT,            -- LLM-generated summary
    holdings TEXT,              -- key holdings/rules (JSON array)
    cited_authorities TEXT,     -- JSON array of citations
    topics TEXT,                -- comma-separated topic tags
    authority_weight REAL DEFAULT 0,
    precedent_strength TEXT,    -- "binding", "persuasive", "advisory"
    content_hash TEXT,          -- MD5 for dedup
    parent_id INTEGER,          -- for chunks
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (parent_id) REFERENCES documents(id)
);
```

#### `documents_fts`
FTS5 virtual table, same pattern as canvass law.

```sql
CREATE VIRTUAL TABLE documents_fts USING fts5(
    citation, title, text, summary_ai, topics,
    content=documents, content_rowid=rowid,
    tokenize="unicode61"
);
-- Auto-sync triggers on INSERT/UPDATE/DELETE
```

#### `document_citations`
Citation graph between documents.

```sql
CREATE TABLE document_citations (
    id INTEGER PRIMARY KEY,
    source_doc_id INTEGER NOT NULL,
    target_doc_id INTEGER,
    normalized_citation TEXT,
    edge_type TEXT,             -- "cites", "distinguishes", "overrules", "follows"
    FOREIGN KEY (source_doc_id) REFERENCES documents(id),
    FOREIGN KEY (target_doc_id) REFERENCES documents(id)
);
```

#### `authority_aliases`
Pattern-based lookup for known authorities.

```sql
CREATE TABLE authority_aliases (
    id INTEGER PRIMARY KEY,
    doc_id INTEGER NOT NULL,
    alias TEXT NOT NULL,        -- e.g., "FOIA", "FOIL", "PRA"
    alias_type TEXT,            -- "acronym", "short_name", "statute_cite"
    FOREIGN KEY (doc_id) REFERENCES documents(id)
);
```

#### `supersession`
Tracks when documents are replaced/updated.

```sql
CREATE TABLE supersession (
    old_id INTEGER NOT NULL,
    new_id INTEGER NOT NULL,
    superseded_date TEXT,
    reason TEXT,
    PRIMARY KEY (old_id, new_id)
);
```

### 5.2 Domain-Specific Reference Tables

#### `exemptions`
First-class exemption catalog. Each state/federal exemption is a row.

```sql
CREATE TABLE exemptions (
    id INTEGER PRIMARY KEY,
    jurisdiction TEXT NOT NULL,     -- "Federal", "NY", "CA", etc.
    statute_citation TEXT NOT NULL, -- e.g., "5 U.S.C. § 552(b)(1)"
    exemption_number TEXT,         -- e.g., "Exemption 1", "b(1)"
    short_name TEXT,               -- e.g., "National Security"
    description TEXT,              -- plain-language description
    scope TEXT,                    -- what it covers
    key_terms TEXT,                -- JSON array of triggering terms
    common_agency_uses TEXT,       -- JSON: which agencies cite this most
    successful_challenge_rate REAL,-- if data available (nullable for now)
    related_case_law TEXT,         -- JSON array of doc_ids
    related_ag_opinions TEXT,      -- JSON array of doc_ids
    counter_arguments TEXT,        -- JSON: known successful challenge strategies
    notes TEXT,
    last_verified TEXT,            -- when this was last confirmed accurate
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

#### `agencies`
Directory of FOIA-responsive agencies.

```sql
CREATE TABLE agencies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    level TEXT NOT NULL,           -- "federal", "state", "county", "municipal"
    parent_agency_id INTEGER,     -- for sub-agencies/components
    foia_officer_title TEXT,
    foia_officer_name TEXT,       -- may go stale, refresh via cron
    email TEXT,
    mailing_address TEXT,
    phone TEXT,
    portal_url TEXT,              -- online submission portal
    submission_method TEXT,       -- "portal", "email", "mail", "fax", "multiple"
    required_form_url TEXT,       -- if agency requires a specific form
    fee_schedule TEXT,            -- JSON: { "search_per_hour": 25.00, ... }
    fee_waiver_available BOOLEAN DEFAULT 1,
    fee_waiver_criteria TEXT,     -- what qualifies for fee waiver
    avg_response_days REAL,       -- computed from tracked requests (nullable)
    notes TEXT,
    source_url TEXT,              -- where we scraped this from
    last_verified TEXT,
    last_scraped TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (parent_agency_id) REFERENCES agencies(id)
);
```

#### `response_rules`
Jurisdiction-level procedural rules (deadlines, extensions, fees).

```sql
CREATE TABLE response_rules (
    id INTEGER PRIMARY KEY,
    jurisdiction TEXT NOT NULL,
    rule_type TEXT NOT NULL,        -- "initial_response", "extension", "appeal_deadline",
                                   -- "judicial_review_deadline", "fee_cap", "fee_waiver"
    param_key TEXT NOT NULL,        -- e.g., "days_to_respond", "max_extension_days"
    param_value TEXT NOT NULL,      -- the value
    day_type TEXT,                  -- "business" or "calendar"
    statute_citation TEXT,          -- source law
    notes TEXT,
    last_verified TEXT,
    UNIQUE(jurisdiction, rule_type, param_key)
);
```

Example rows:
```
| jurisdiction | rule_type         | param_key          | param_value | day_type | statute_citation        |
|-------------|-------------------|--------------------|-------------|----------|-------------------------|
| Federal     | initial_response  | days_to_respond    | 20          | business | 5 U.S.C. § 552(a)(6)(A) |
| Federal     | extension         | max_extension_days | 10          | business | 5 U.S.C. § 552(a)(6)(B) |
| NY          | initial_response  | days_to_respond    | 5           | business | N.Y. Pub. Off. Law § 89 |
| CA          | initial_response  | days_to_respond    | 10          | calendar | Cal. Gov. Code § 6253(c)|
| TX          | initial_response  | days_to_respond    | 10          | business | Tex. Gov. Code § 552.301|
```

#### `request_templates`
Model request language, per jurisdiction and record type.

```sql
CREATE TABLE request_templates (
    id INTEGER PRIMARY KEY,
    jurisdiction TEXT NOT NULL,
    record_type TEXT,              -- "general", "police_records", "emails",
                                  -- "contracts", "meeting_minutes", etc.
    template_name TEXT NOT NULL,
    template_text TEXT NOT NULL,   -- with {{placeholders}}
    fee_waiver_language TEXT,      -- optional fee waiver paragraph
    expedited_language TEXT,       -- optional expedited processing paragraph
    notes TEXT,
    source TEXT,                   -- who wrote/tested this template
    created_at TEXT DEFAULT (datetime('now'))
);
```

### 5.3 Request Lifecycle Tables (Forward-Compatible)

These tables support the operational side. Built now for schema stability, fully wired later when auth is added.

#### `campaigns`
A campaign groups related requests across multiple agencies.

```sql
CREATE TABLE campaigns (
    id INTEGER PRIMARY KEY,
    user_id TEXT,                  -- nullable until auth exists
    title TEXT NOT NULL,
    description TEXT,
    record_type TEXT,              -- what kind of records
    date_range_start TEXT,         -- date range of records sought
    date_range_end TEXT,
    status TEXT DEFAULT 'active',  -- "active", "completed", "abandoned"
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

#### `requests`
Individual requests within a campaign (or standalone).

```sql
CREATE TABLE requests (
    id INTEGER PRIMARY KEY,
    campaign_id INTEGER,
    user_id TEXT,
    agency_id INTEGER NOT NULL,
    jurisdiction TEXT NOT NULL,
    status TEXT DEFAULT 'draft',   -- state machine (see §6)
    request_text TEXT,             -- the actual request letter
    submission_method TEXT,        -- how it was/will be sent
    submitted_at TEXT,
    acknowledged_at TEXT,
    due_date TEXT,                 -- computed from response_rules
    extended_due_date TEXT,
    extension_reason TEXT,
    response_type TEXT,            -- "full_grant", "partial_grant", "denial",
                                  -- "no_responsive_records", "fee_estimate"
    response_received_at TEXT,
    response_summary TEXT,
    denial_exemptions TEXT,        -- JSON array of exemption_ids cited
    fee_quoted REAL,
    fee_paid REAL,
    fee_waiver_requested BOOLEAN DEFAULT 0,
    fee_waiver_granted BOOLEAN,
    appeal_deadline TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (agency_id) REFERENCES agencies(id)
);
```

#### `request_events`
Audit log for every state transition and action.

```sql
CREATE TABLE request_events (
    id INTEGER PRIMARY KEY,
    request_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,      -- "status_change", "fee_estimate", "extension",
                                  -- "response_received", "appeal_filed", "note"
    old_value TEXT,
    new_value TEXT,
    details TEXT,                  -- JSON blob for structured event data
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (request_id) REFERENCES requests(id)
);
```

#### `response_documents`
Metadata about documents received in response (actual files stored on disk).

```sql
CREATE TABLE response_documents (
    id INTEGER PRIMARY KEY,
    request_id INTEGER NOT NULL,
    filename TEXT,
    file_path TEXT,               -- local path to stored file
    file_size INTEGER,
    page_count INTEGER,
    content_type TEXT,
    description TEXT,
    received_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (request_id) REFERENCES requests(id)
);
```

### 5.4 Indexes

```sql
-- Core corpus
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_jurisdiction ON documents(jurisdiction);
CREATE INDEX idx_documents_date ON documents(date);
CREATE INDEX idx_documents_source ON documents(source);
CREATE INDEX idx_documents_hash ON documents(content_hash);
CREATE INDEX idx_documents_parent ON documents(parent_id);
CREATE INDEX idx_documents_type_jurisdiction ON documents(document_type, jurisdiction);
CREATE INDEX idx_documents_authority ON documents(authority_weight DESC);

-- Citations
CREATE INDEX idx_citations_source ON document_citations(source_doc_id);
CREATE INDEX idx_citations_target ON document_citations(target_doc_id);

-- Aliases
CREATE INDEX idx_aliases_alias ON authority_aliases(alias);
CREATE INDEX idx_aliases_doc ON authority_aliases(doc_id);

-- Exemptions
CREATE INDEX idx_exemptions_jurisdiction ON exemptions(jurisdiction);
CREATE INDEX idx_exemptions_citation ON exemptions(statute_citation);

-- Agencies
CREATE INDEX idx_agencies_jurisdiction ON agencies(jurisdiction);
CREATE INDEX idx_agencies_level ON agencies(level);
CREATE INDEX idx_agencies_jurisdiction_level ON agencies(jurisdiction, level);

-- Requests
CREATE INDEX idx_requests_campaign ON requests(campaign_id);
CREATE INDEX idx_requests_agency ON requests(agency_id);
CREATE INDEX idx_requests_status ON requests(status);
CREATE INDEX idx_requests_user ON requests(user_id);
CREATE INDEX idx_requests_due ON requests(due_date);

-- Events
CREATE INDEX idx_events_request ON request_events(request_id);
CREATE INDEX idx_events_type ON request_events(event_type);
```

---

## 6. Request State Machine

```
draft ──→ submitted ──→ acknowledged ──→ processing ──→ responded
  │                         │                │              │
  │                         │                ▼              ├──→ full_grant ──→ closed
  │                         │            extended           ├──→ partial_grant ──→ [appeal?]
  │                         │                │              ├──→ denial ──→ [appeal?]
  │                         │                ▼              ├──→ no_records ──→ [appeal?]
  │                         │            processing         └──→ fee_estimate ──→ [pay/waive?]
  │                         │
  │                         └──→ (auto-compute due_date from response_rules)
  │
  └──→ abandoned

Appeal sub-flow:
  denial/partial ──→ appeal_draft ──→ appeal_submitted ──→ appeal_decided
                                                              ├──→ appeal_granted ──→ processing
                                                              ├──→ appeal_denied ──→ [judicial?]
                                                              └──→ appeal_partial ──→ [judicial?]
```

**Deadline calculation:**
- On `submitted → acknowledged`: compute `due_date` = acknowledged_date + jurisdiction's `days_to_respond` (respecting `day_type`)
- On extension: compute `extended_due_date` = due_date + extension days
- On denial/partial: compute `appeal_deadline` from response_rules
- Business day calculation accounts for federal/state holidays per jurisdiction

---

## 7. Document Types

```json
{
  "document_types": [
    {"type": "Federal FOIA Statute", "authority": "highest", "phase": 1},
    {"type": "State Public Records Statute", "authority": "highest", "phase": 1},
    {"type": "Federal FOIA Regulation", "authority": "high", "phase": 1},
    {"type": "State Public Records Regulation", "authority": "high", "phase": 2},
    {"type": "AG Opinion - Public Records", "authority": "high", "phase": 2},
    {"type": "AG Guidance - Public Records", "authority": "medium", "phase": 2},
    {"type": "Federal Court Opinion", "authority": "high", "phase": 2},
    {"type": "State Court Opinion", "authority": "high", "phase": 3},
    {"type": "OGIS Advisory Opinion", "authority": "medium", "phase": 2},
    {"type": "Agency FOIA Handbook", "authority": "reference", "phase": 3},
    {"type": "Agency FOIA Report", "authority": "reference", "phase": 3},
    {"type": "Fee Schedule", "authority": "reference", "phase": 2},
    {"type": "Request Template", "authority": "reference", "phase": 2},
    {"type": "Practitioner Guide", "authority": "reference", "phase": 3},
    {"type": "Legislative History", "authority": "reference", "phase": 4},
    {"type": "Academic Analysis", "authority": "reference", "phase": 4},
    {"type": "FOIA Annual Report", "authority": "reference", "phase": 3},
    {"type": "Open Meetings Statute", "authority": "highest", "phase": 3},
    {"type": "Open Meetings Regulation", "authority": "high", "phase": 3},
    {"type": "Open Meetings Opinion", "authority": "high", "phase": 4}
  ]
}
```

**Phase assignments reflect ingestion order** — highest-authority sources first.

---

## 8. Ingestion Pipeline

### 8.1 Phased Build Strategy

#### Phase 1: Federal Foundation (Week 1-2)
**Goal:** Complete federal FOIA corpus + schema + query engine

| Source | Script | Count (est.) |
|--------|--------|-------------|
| 5 U.S.C. § 552 (FOIA statute) | `ingest_uscode.py` | 1 (with amendments) |
| 5 U.S.C. § 552a (Privacy Act) | `ingest_uscode.py` | 1 |
| 5 U.S.C. § 552b (Sunshine Act) | `ingest_uscode.py` | 1 |
| DOJ FOIA regulations (28 CFR Part 16) | `ingest_cfr.py` | ~20 sections |
| Agency-specific FOIA regs | `ingest_cfr.py` | ~200 sections |
| OGIS advisory opinions | `ingest_ogis.py` | ~100 |
| DOJ OIP guidance memos | `ingest_doj_oip.py` | ~200 |
| Federal FOIA case law (CourtListener) | `ingest_courtlistener_foia.py` | ~2,000 |
| FOIA.gov agency directory | `ingest_foia_gov.py` | ~130 agencies |
| Federal fee schedules | `ingest_federal_fees.py` | ~130 entries |
| Federal exemptions catalog | `build_federal_exemptions.py` | 9 exemptions + 3 exclusions |
| Federal response rules | `build_federal_response_rules.py` | ~10 rules |
| Federal request templates | `build_federal_templates.py` | ~10 templates |

**Deliverables:**
- Working SQLite database with FTS5
- `fetch_json.py` query engine (adapted from canvass law)
- Flask frontend (search + browse)
- Federal exemptions fully cataloged
- Federal agency directory populated
- Basic request template generation

#### Phase 2: Priority States — NY, CA, TX (Week 3-5)
**Goal:** Deep coverage for three high-volume states

Per state:
| Source | Script Pattern | Count (est.) |
|--------|---------------|-------------|
| Public records statute | `ingest_state_statute_{st}.py` | 1 statute (multi-section) |
| Implementing regulations | `ingest_state_regs_{st}.py` | 10-50 sections |
| AG opinions on public records | `ingest_state_ag_{st}.py` | 50-500 |
| State court opinions | `ingest_courtlistener_state.py` | 200-1,000 |
| State agency directory | `build_state_agencies_{st}.py` | 50-200 agencies |
| State fee schedules | `build_state_fees_{st}.py` | varies |
| State exemptions catalog | `build_state_exemptions_{st}.py` | 20-60 per state |
| State response rules | `build_state_rules_{st}.py` | ~10 per state |
| State request templates | `build_state_templates_{st}.py` | ~5 per state |

**State-specific notes:**
- **NY:** FOIL (Freedom of Information Law) + Open Meetings Law. Committee on Open Government (COOG) advisory opinions are gold — hundreds of them. Strong AG opinion tradition.
- **CA:** California Public Records Act (CPRA) — recently recodified (2023, now Gov. Code §§ 7920-7931). Many court decisions. Fee waiver broadly available.
- **TX:** Texas Public Information Act (TPIA). AG decisions are the primary interpretive authority (TX AG rules on most disputes, not courts). Thousands of AG rulings.

#### Phase 3: Canvass 10 States (Week 6-9)
Extend to the 10 canvass law states: CA (done), MN, NE, NY (done), AZ, MA, MI, MO, ME, VT. Plus TX (done).

Same per-state script pattern. Prioritize by:
1. Volume of AG opinions available
2. Strength of online resources
3. Population/likely request volume

#### Phase 4: Remaining States (Week 10-16)
All remaining states + DC + territories. Lighter initial coverage:
- Statute text
- Basic exemptions catalog
- Response rules (deadlines, fees)
- Agency directory (state-level agencies only, not municipal)
- AG opinions where digitally available

#### Phase 5: Depth & Enrichment (Ongoing)
- Municipal agency directories for major cities
- Historical AG opinion archives
- Academic/practitioner literature
- Open meetings law integration
- Cross-citation graph building
- Summarization backfill
- Template refinement from real-world usage

### 8.2 Cron Schedule (Post-Build)

**Daily (2 AM):**
- Federal court opinions (CourtListener, FOIA-filtered)
- FOIA.gov agency directory refresh
- Summarization backfill (500 docs/day)
- Citation extraction
- Freshness monitor

**Weekly (Mon 3 AM):**
- Federal statute/regulation check for amendments
- DOJ OIP new guidance
- OGIS new opinions
- State AG opinions (NY, CA, TX — high volume)
- State court opinions (CourtListener, filtered)
- Agency directory spot-checks (sample verification)
- Smoke tests + coverage audits

**Monthly (1st @ 4 AM):**
- All state statutes (full refresh)
- All state AG opinions
- All state agency directories (full scrape)
- Exemption catalog verification
- Response rules verification
- Fee schedule verification
- FOIA annual reports

### 8.3 Agency Directory Freshness

This is the hardest freshness problem. Agency FOIA pages change when:
- FOIA officers rotate (quarterly-ish)
- Agencies reorganize
- Portal URLs change
- Fee schedules update

**Strategy:**
1. **Monthly full scrape** of agency FOIA pages
2. **Weekly spot-check** — sample 10% of agencies, verify key fields (email, portal URL)
3. **Staleness flag** — if last_verified > 90 days, flag as potentially stale
4. **User reports** — (future) let users flag incorrect agency info
5. **Cost:** Weekly checks are cheap — just HTTP HEAD requests + page scrapes for sampled agencies. ~50-100 requests/week for federal, more for states. Well within acceptable compute/API budget.

---

## 9. Query Engine (`fetch_json.py`)

Adapted from canvass law's query engine with domain-specific modifications.

### 9.1 Domain Detection Profiles

```python
DOMAIN_SIGNALS = {
    "foia_federal": ["foia", "freedom of information", "5 usc 552", "ogis",
                     "foia request", "agency records", "federal records"],
    "foia_exemptions": ["exemption", "b(1)", "b(2)", "b(3)", "b(4)", "b(5)",
                        "b(6)", "b(7)", "deliberative process", "law enforcement",
                        "trade secret", "personal privacy", "national security"],
    "foia_fees": ["fee", "fee waiver", "search fee", "duplication", "commercial use",
                  "news media", "educational institution"],
    "foia_appeals": ["appeal", "denial", "adverse determination", "ogis mediation",
                     "judicial review", "de novo", "vaughn index"],
    "foia_expedited": ["expedited processing", "compelling need", "imminent threat",
                       "breaking news", "due process"],
    "state_public_records": ["public records", "open records", "foil", "cpra",
                             "sunshine law", "right to know"],
    "open_meetings": ["open meetings", "sunshine act", "brown act", "public meeting",
                      "executive session", "closed session"],
    "ag_rulings": ["attorney general", "ag opinion", "ag ruling", "ag decision",
                   "open records decision"],
    "police_records": ["body camera", "body cam", "use of force", "police report",
                       "incident report", "arrest record", "booking"],
    "government_contracts": ["contract", "procurement", "rfp", "bid", "vendor",
                             "purchase order", "sole source"],
    "emails_communications": ["email", "text message", "correspondence", "memo",
                              "communication", "slack", "teams"]
}
```

### 9.2 Query Expansion

Same pattern as canvass law:
- Type-filter-first for precision
- Domain-detected expansion for vague queries
- Alias injection for known authorities
- Diversity constraints to prevent single-type flooding

### 9.3 Exemption-Aware Search

New capability: when a query involves an exemption, the engine:
1. Identifies the exemption(s) from the `exemptions` table
2. Injects related case law and AG opinions (from `related_case_law`, `related_ag_opinions`)
3. Surfaces counter-arguments from `counter_arguments` field
4. Flags successful challenge strategies

---

## 10. Skill Architecture

### 10.1 Skills

**`sunshine`** — Production research + request workflow (like `canvass`)

**`sunshine-request`** — Full request lifecycle:
1. Intake (plain English → structured request parameters)
2. Jurisdiction identification
3. Agency routing
4. Exemption risk assessment
5. Request drafting
6. Submission guidance (or direct submission)
7. Deadline calculation
8. Tracking setup

**`sunshine-appeal`** — Appeal workflow:
1. Analyze denial/partial grant
2. Research exemption cited
3. Find counter-arguments (AG opinions, case law, successful challenges)
4. Draft appeal letter
5. Submission guidance

**`sunshine-research`** — Pure research mode (like `canvass`):
1. Query the corpus
2. Synthesize findings
3. Produce memo with citations

### 10.2 Intake Flow

User says: *"I want the meeting minutes from the Springfield city council for January 2026"*

System:
1. **Disambiguate:** "Which Springfield? IL, MO, MA, OH, OR...?" (or auto-detect from context)
2. **Identify custodian:** City Clerk, Springfield, [State] → look up in `agencies` table
3. **Look up applicable law:** [State] public records act → `response_rules` for deadlines
4. **Check exemptions:** Meeting minutes are generally public, but check for executive session portions
5. **Generate request:** Pull template from `request_templates`, fill in specifics
6. **Provide submission instructions:** Email/portal/mail address from `agencies` table
7. **Calculate deadlines:** "They must respond within [X] [business/calendar] days"
8. **Offer to send:** "Want me to email this request to clerk@springfield.gov?"

### 10.3 Appeal Flow

Agency denies citing "deliberative process privilege":

System:
1. Look up "deliberative process" in `exemptions` → Exemption 5 (federal) or state equivalent
2. Query corpus: `fetch_json.py '"deliberative process" Type:"Federal Court Opinion"' --authority`
3. Find key rulings: *Vaughn v. Rosen*, *EPA v. Mink*, recent circuit decisions
4. Check if the specific record type has been held non-exempt in similar cases
5. Draft appeal letter citing applicable precedent
6. Include fee waiver language if applicable
7. Provide appeal submission instructions + deadline

---

## 11. Flask Frontend

### 11.1 Pages

| Route | Function |
|-------|----------|
| `/` | Landing page with corpus stats |
| `/search` | Full-text search with filters (type, jurisdiction, date range) |
| `/document/<id>` | Individual document with citation network |
| `/jurisdictions` | State-by-state guide (statute, deadlines, exemptions, fees) |
| `/jurisdiction/<state>` | Deep dive: one state's complete FOIA landscape |
| `/exemptions` | Browseable exemption catalog |
| `/exemption/<id>` | Single exemption with case law, AG opinions, challenge strategies |
| `/agencies` | Agency directory (searchable, filterable) |
| `/agency/<id>` | Agency detail: contact info, submission method, fee schedule |
| `/templates` | Request template library |
| `/api/search` | JSON search endpoint (key-gated) |
| `/api/documents/<id>` | JSON document endpoint (key-gated) |
| `/api/exemptions` | JSON exemptions endpoint |
| `/api/agencies` | JSON agency directory endpoint |

### 11.2 Jurisdiction Guide Page

Each state page shows:
- Applicable statute (with link to full text in corpus)
- Who can request (residency requirements — some states restrict)
- What's covered (definition of "public record")
- Response deadline + extension rules
- Fee schedule
- Fee waiver eligibility
- Exemptions list (linked to exemption detail pages)
- Appeal process (administrative → judicial)
- AG opinions (recent, notable)
- Key court decisions
- Agency directory for that state
- Request templates for that state
- Tips and common pitfalls

---

## 12. Quality Gates

### 12.1 Ingestion Validation
- Hash-based dedup (same as canvass law)
- JSON receipts per script (`{"added": N, "skipped": M, "errors": K}`)
- Zero-doc alerts via Telegram
- Coverage requirements per jurisdiction (minimum doc counts by type)

### 12.2 Data Accuracy
- **Exemptions:** Every exemption entry must cite a statute. Counter-arguments must cite case law or AG opinions.
- **Response rules:** Every deadline must cite a statute. Day type (business/calendar) must be explicit.
- **Agency directory:** Every entry must have a source_url. last_verified must be within 90 days.
- **Fee schedules:** Must cite statutory authority. Mark as "agency-specific" vs "statewide default."

### 12.3 Search Quality
- Smoke tests: known-answer queries for each jurisdiction
- Retrieval benchmark: precision/recall on curated test set
- Exemption retrieval: when user cites an exemption number, the system must surface it

### 12.4 Request Quality (Agent Layer)
- Guard pipeline adapted from canvass law:
  - Citation presence (every legal claim in a request/appeal cites authority)
  - Deadline accuracy (computed deadline matches response_rules)
  - Agency info freshness (flag if agency last_verified > 90 days)
  - Exemption argument validity (cited precedent actually exists in corpus)

---

## 13. Project Structure

```
~/projects/sunshine/
├── .claude/
│   ├── CURRENT-STATE.md
│   ├── PROJECT-BRIEF.md
│   └── error-log.json
├── app.py                      # Flask application
├── fetch_json.py               # Query engine
├── schema.sql                  # Full schema definition
├── config/
│   ├── document_types.json
│   ├── coverage_requirements.json
│   ├── domain_signals.json
│   └── state_sources.json
├── scripts/
│   ├── ingest/
│   │   ├── federal/
│   │   │   ├── ingest_uscode.py
│   │   │   ├── ingest_cfr.py
│   │   │   ├── ingest_courtlistener_foia.py
│   │   │   ├── ingest_foia_gov.py
│   │   │   ├── ingest_ogis.py
│   │   │   └── ingest_doj_oip.py
│   │   └── state/
│   │       ├── ingest_state_statute_ny.py
│   │       ├── ingest_state_ag_ny.py
│   │       ├── ingest_state_ag_tx.py
│   │       └── ...
│   ├── build/
│   │   ├── build_federal_exemptions.py
│   │   ├── build_state_exemptions.py
│   │   ├── build_federal_response_rules.py
│   │   ├── build_state_agencies.py
│   │   └── build_templates.py
│   ├── process/
│   │   ├── summarize_docs.py
│   │   ├── extract_citations.py
│   │   └── backfill_citations.py
│   ├── audit/
│   │   ├── coverage_audit.py
│   │   ├── freshness_monitor.py
│   │   ├── smoke_tests.py
│   │   └── agency_verify.py
│   └── cron/
│       ├── daily.sh
│       ├── weekly.sh
│       └── monthly.sh
├── templates/                  # Flask HTML templates
│   ├── base.html
│   ├── index.html
│   ├── search.html
│   ├── document.html
│   ├── jurisdiction.html
│   ├── exemption.html
│   └── agency.html
├── static/
├── data/
│   └── sunshine.db             # SQLite database
├── logs/
├── cache/                      # Ingestion cache (downloaded pages)
├── tests/
│   ├── test_fetch.py
│   ├── test_schema.py
│   └── test_smoke.py
└── TRACKER.md                  # Single source of truth
```

---

## 14. Implementation Plan

### Phase 0: Scaffolding (Day 1)
- [ ] Create project directory structure
- [ ] Write schema.sql and initialize database
- [ ] Adapt fetch_json.py from canvass law
- [ ] Set up Flask app skeleton
- [ ] Create config files (document_types.json, etc.)
- [ ] Set up TRACKER.md
- [ ] Pick a port number

### Phase 1: Federal Foundation (Week 1-2)
- [ ] Ingest federal FOIA statute (5 U.S.C. § 552)
- [ ] Ingest federal FOIA regulations (28 CFR Part 16)
- [ ] Build federal exemptions catalog (9 exemptions + 3 exclusions)
- [ ] Ingest FOIA.gov agency directory
- [ ] Build federal response rules
- [ ] Ingest OGIS advisory opinions
- [ ] Ingest DOJ OIP guidance
- [ ] Ingest federal FOIA case law from CourtListener
- [ ] Build federal request templates
- [ ] Build federal fee schedules
- [ ] Wire up Flask search + browse
- [ ] Smoke tests passing
- [ ] Coverage audit green

### Phase 2: Priority States (Week 3-5)
- [ ] NY: FOIL statute + COOG opinions + AG opinions + court opinions + agencies + exemptions
- [ ] CA: CPRA statute + AG opinions + court opinions + agencies + exemptions
- [ ] TX: TPIA statute + AG rulings + court opinions + agencies + exemptions
- [ ] Per-state response rules, fee schedules, templates
- [ ] State jurisdiction guide pages
- [ ] Cross-jurisdiction search working
- [ ] Exemption detail pages

### Phase 3: Canvass 10 States (Week 6-9)
- [ ] MN, NE, AZ, MA, MI, MO, ME, VT (CA + NY done in Phase 2)
- [ ] Per-state full coverage
- [ ] Cron automation for all states

### Phase 4: All States (Week 10-16)
- [ ] Remaining 37 states + DC
- [ ] Lighter coverage: statute + exemptions + rules + state agencies
- [ ] AG opinions where digitally available

### Phase 5: Skill Integration (Parallel with Phase 2+)
- [ ] `sunshine` research skill
- [ ] `sunshine-request` intake + drafting skill
- [ ] `sunshine-appeal` appeal workflow skill
- [ ] Guard pipeline
- [ ] Request lifecycle tracking

### Phase 6: Enrichment (Ongoing)
- [ ] Agency scorecards (forward-compatible tracking)
- [ ] Public registry opt-in
- [ ] Open meetings law integration
- [ ] Municipal coverage for major cities
- [ ] Cross-citation graph
- [ ] Name + branding finalized

---

## 15. Open Decisions (Deferred)

| Decision | When Needed | Notes |
|----------|-------------|-------|
| Final name | Before Phase 2 frontend | "Sunshine" is working title |
| Auth system | Before public request tracking | Schema ready, wire up later |
| Revenue model | Before public launch | Free research, gated tools? |
| Public registry design | Phase 6 | Same DB or separate store? Privacy model? |
| Direct submission | Phase 5 | Email sending? Portal automation? |
| Open source scope | Before public launch | Core DB open, agent layer private? |
| Mobile/offline | Post-launch | Not needed initially |

---

## 16. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Agency directory goes stale | Monthly full scrape + weekly spot-check + staleness flags |
| State AG opinion archives vary wildly | Phase by availability; some states (TX) have thousands, others (VT) have few |
| Exemption catalog accuracy | Every entry must cite statute; guard pipeline validates |
| State law changes | Monthly statute refresh; weekly check for amendments in priority states |
| Cost of LLM summarization | Gemini Flash Lite at ~$0.01/doc; budget cap like canvass law |
| CourtListener rate limits | Same patterns as canvass law (respect limits, cache aggressively) |
| Scope creep into open meetings | Deferred to Phase 6; schema supports it but don't build until core is solid |

---

## 17. How This Differs from Existing Tools

| Tool | What It Does | What Sunshine Adds |
|------|-------------|-------------------|
| FOIA.gov | Federal agency directory + annual reports | All jurisdictions, not just federal. Plus case law, AG opinions, exemption analysis, request drafting |
| MuckRock | Request filing + tracking service | Deeper legal research corpus. Exemption-specific challenge strategies. Full appeal workflow with legal arguments |
| RCFP Open Government Guide | State-by-state reference | Machine-readable, searchable, with case law + AG opinions integrated. Not just a reference — an operational tool |
| iFOIA | Simple request generator | Jurisdiction-aware templates, exemption risk assessment, appeal generation, deadline tracking |
| NFOIC | Advocacy + state FOI resources | Comprehensive structured database vs. curated links. Agent-powered research |

Sunshine's differentiator: **the research corpus and the operational tool are the same system.** When you get denied, the system doesn't just tell you "file an appeal" — it searches its own corpus of AG opinions and case law to build your appeal arguments. That feedback loop between research and action is unique.
