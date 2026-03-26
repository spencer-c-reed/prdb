-- PRDB: Public Records Request Database Schema
-- Created: 2026-03-26
-- Schema version: 1
--
-- Placeholder name "prdb" — find-and-replace to final name later.
-- "prdb" chosen to avoid false positives with "sunshine law" in corpus text.

PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now')),
    description TEXT
);

INSERT INTO schema_version (version, description) VALUES (1, 'Initial schema');

-- =============================================================================
-- CORE DOCUMENT CORPUS
-- =============================================================================

CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    citation TEXT,
    title TEXT,
    date TEXT,
    court TEXT,                     -- issuing body (court, AG, agency, etc.)
    document_type TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,     -- "federal", 2-letter state code, etc.
    source TEXT NOT NULL,           -- standardized source tag
    source_url TEXT,
    text TEXT NOT NULL,
    summary TEXT,
    md5_hash TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    -- AI-generated fields (populated by summarizer)
    summary_ai TEXT,
    summary_brief TEXT,
    topics TEXT,
    holdings TEXT,                  -- JSON array of key holdings
    cited_authorities TEXT,         -- JSON array of cited authorities
    summarized_at TEXT,
    summary_model TEXT,
    -- Classification
    jurisdiction_level TEXT DEFAULT 'federal',  -- federal, state, county, city
    authority_weight INTEGER DEFAULT 50,
    precedent_strength TEXT,        -- settled, established, guidance
    -- Chunking support
    parent_id TEXT REFERENCES documents(id),
    section_path TEXT,
    section_order INTEGER
);

CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_jurisdiction ON documents(jurisdiction);
CREATE INDEX idx_documents_date ON documents(date);
CREATE INDEX idx_documents_court ON documents(court);
CREATE INDEX idx_documents_source ON documents(source);
CREATE INDEX idx_documents_md5 ON documents(md5_hash);
CREATE INDEX idx_documents_citation ON documents(citation);
CREATE INDEX idx_documents_jurisdiction_level ON documents(jurisdiction_level);
CREATE INDEX idx_documents_authority_weight ON documents(authority_weight);
CREATE INDEX idx_documents_parent ON documents(parent_id);
CREATE INDEX idx_documents_type_jurisdiction ON documents(document_type, jurisdiction);

-- FTS5 full-text search index
CREATE VIRTUAL TABLE documents_fts USING fts5(
    citation, title, text, summary, summary_ai, topics,
    content=documents, content_rowid=rowid,
    tokenize="unicode61"
);

-- FTS sync triggers
CREATE TRIGGER documents_ai AFTER INSERT ON documents BEGIN
    INSERT INTO documents_fts(rowid, citation, title, text, summary)
    VALUES (new.rowid, new.citation, new.title, new.text, new.summary);
END;

CREATE TRIGGER documents_au AFTER UPDATE ON documents BEGIN
    INSERT INTO documents_fts(documents_fts, rowid, citation, title, text, summary)
    VALUES ('delete', old.rowid, old.citation, old.title, old.text, old.summary);
    INSERT INTO documents_fts(rowid, citation, title, text, summary)
    VALUES (new.rowid, new.citation, new.title, new.text, new.summary);
END;

CREATE TRIGGER documents_ad AFTER DELETE ON documents BEGIN
    INSERT INTO documents_fts(documents_fts, rowid, citation, title, text, summary)
    VALUES ('delete', old.rowid, old.citation, old.title, old.text, old.summary);
END;

-- Auto-infer state jurisdiction_level from 2-letter codes
CREATE TRIGGER documents_infer_jurisdiction_level
AFTER INSERT ON documents
WHEN NEW.jurisdiction_level = 'federal'
  AND length(NEW.jurisdiction) = 2
  AND NEW.jurisdiction NOT IN ('US', 'DC')
  AND NEW.jurisdiction GLOB '[A-Z][A-Z]'
BEGIN
    UPDATE documents
    SET jurisdiction_level = 'state'
    WHERE rowid = NEW.rowid;
END;

-- =============================================================================
-- INGESTION LOG
-- =============================================================================

CREATE TABLE ingestion_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    run_date TEXT DEFAULT (datetime('now')),
    documents_added INTEGER DEFAULT 0,
    documents_skipped INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    notes TEXT
);

-- =============================================================================
-- CITATION INFRASTRUCTURE
-- =============================================================================

-- Document citation graph
CREATE TABLE document_citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_doc_id TEXT NOT NULL,
    target_doc_id TEXT NOT NULL,
    raw_citation TEXT,
    normalized_citation TEXT,
    edge_type TEXT NOT NULL,        -- cites, distinguishes, overrules, follows
    extractor TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    source_field TEXT,
    evidence_snippet TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE(source_doc_id, target_doc_id, edge_type, extractor),
    FOREIGN KEY (source_doc_id) REFERENCES documents(id),
    FOREIGN KEY (target_doc_id) REFERENCES documents(id)
);

CREATE INDEX idx_document_citations_source ON document_citations(source_doc_id);
CREATE INDEX idx_document_citations_target ON document_citations(target_doc_id);
CREATE INDEX idx_document_citations_edge_type ON document_citations(edge_type);
CREATE INDEX idx_document_citations_normalized ON document_citations(normalized_citation);

-- Authority aliases (citation normalization / pattern lookup)
CREATE TABLE authority_aliases (
    alias TEXT PRIMARY KEY,
    normalized_alias TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    alias_type TEXT NOT NULL,      -- acronym, short_name, statute_cite
    source TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (doc_id) REFERENCES documents(id)
);

CREATE INDEX idx_authority_aliases_doc_id ON authority_aliases(doc_id);
CREATE INDEX idx_authority_aliases_normalized ON authority_aliases(normalized_alias);
CREATE INDEX idx_authority_aliases_type ON authority_aliases(alias_type);

-- Supersession tracking
CREATE TABLE supersession_edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    old_doc_id TEXT NOT NULL,
    new_doc_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,    -- supersedes, amends, repeals, replaces
    scope TEXT DEFAULT 'full',
    effective_date TEXT,
    extractor TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    evidence_snippet TEXT,
    validation_status TEXT DEFAULT 'auto',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE(old_doc_id, new_doc_id, relation_type, scope, extractor),
    FOREIGN KEY (old_doc_id) REFERENCES documents(id),
    FOREIGN KEY (new_doc_id) REFERENCES documents(id)
);

CREATE INDEX idx_supersession_edges_old ON supersession_edges(old_doc_id);
CREATE INDEX idx_supersession_edges_new ON supersession_edges(new_doc_id);

-- Extracted citations (intermediate queue)
CREATE TABLE extracted_citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_doc_id TEXT NOT NULL,
    raw_citation TEXT NOT NULL,
    normalized_citation TEXT NOT NULL,
    citation_type TEXT,
    extractor TEXT NOT NULL,
    source_field TEXT,
    target_doc_id TEXT,
    resolution_method TEXT,
    resolution_status TEXT NOT NULL, -- resolved, unresolved, ambiguous
    confidence REAL DEFAULT 0.5,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE(source_doc_id, raw_citation, extractor),
    FOREIGN KEY (source_doc_id) REFERENCES documents(id),
    FOREIGN KEY (target_doc_id) REFERENCES documents(id)
);

CREATE INDEX idx_extracted_citations_source ON extracted_citations(source_doc_id);
CREATE INDEX idx_extracted_citations_status ON extracted_citations(resolution_status);

-- =============================================================================
-- DOMAIN-SPECIFIC: EXEMPTIONS (FIRST-CLASS)
-- =============================================================================

CREATE TABLE exemptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jurisdiction TEXT NOT NULL,         -- "federal", "NY", "CA", "TX", etc.
    statute_citation TEXT NOT NULL,     -- e.g., "5 U.S.C. § 552(b)(1)"
    exemption_number TEXT,             -- e.g., "Exemption 1", "b(1)", "(c)(1)"
    short_name TEXT,                   -- e.g., "National Security"
    category TEXT,                     -- e.g., "law_enforcement", "privacy", "deliberative"
    description TEXT,                  -- plain-language description
    scope TEXT,                        -- what it covers
    key_terms TEXT,                    -- JSON array of triggering terms
    common_agency_uses TEXT,           -- JSON: which agencies cite this most
    successful_challenge_rate REAL,    -- nullable for now
    related_case_law TEXT,             -- JSON array of doc_ids
    related_ag_opinions TEXT,          -- JSON array of doc_ids
    counter_arguments TEXT,            -- JSON: known successful challenge strategies
    notes TEXT,
    last_verified TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_exemptions_jurisdiction ON exemptions(jurisdiction);
CREATE INDEX idx_exemptions_citation ON exemptions(statute_citation);
CREATE INDEX idx_exemptions_category ON exemptions(category);

-- =============================================================================
-- DOMAIN-SPECIFIC: AGENCY DIRECTORY
-- =============================================================================

CREATE TABLE agencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    level TEXT NOT NULL,                -- federal, state, county, municipal
    parent_agency_id INTEGER,
    abbreviation TEXT,                 -- e.g., "FBI", "NYPD"
    foia_officer_title TEXT,
    foia_officer_name TEXT,
    email TEXT,
    mailing_address TEXT,
    phone TEXT,
    fax TEXT,
    portal_url TEXT,                   -- online submission portal
    submission_method TEXT,            -- portal, email, mail, fax, multiple
    required_form_url TEXT,
    fee_schedule TEXT,                 -- JSON: { "search_per_hour": 25.00, ... }
    fee_waiver_available INTEGER DEFAULT 1,
    fee_waiver_criteria TEXT,
    avg_response_days REAL,            -- computed from tracked requests (nullable)
    common_denial_exemptions TEXT,     -- JSON array of exemption IDs commonly cited
    notes TEXT,
    source_url TEXT,                   -- where we scraped this from
    last_verified TEXT,
    last_scraped TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (parent_agency_id) REFERENCES agencies(id)
);

CREATE INDEX idx_agencies_jurisdiction ON agencies(jurisdiction);
CREATE INDEX idx_agencies_level ON agencies(level);
CREATE INDEX idx_agencies_jurisdiction_level ON agencies(jurisdiction, level);
CREATE INDEX idx_agencies_abbreviation ON agencies(abbreviation);

-- =============================================================================
-- DOMAIN-SPECIFIC: RESPONSE RULES
-- =============================================================================

CREATE TABLE response_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jurisdiction TEXT NOT NULL,
    rule_type TEXT NOT NULL,            -- initial_response, extension, appeal_deadline,
                                       -- judicial_review_deadline, fee_cap, fee_waiver,
                                       -- expedited_processing
    param_key TEXT NOT NULL,            -- e.g., "days_to_respond", "max_extension_days"
    param_value TEXT NOT NULL,
    day_type TEXT,                      -- "business" or "calendar"
    statute_citation TEXT,
    notes TEXT,
    last_verified TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE(jurisdiction, rule_type, param_key)
);

CREATE INDEX idx_response_rules_jurisdiction ON response_rules(jurisdiction);
CREATE INDEX idx_response_rules_type ON response_rules(rule_type);

-- =============================================================================
-- DOMAIN-SPECIFIC: REQUEST TEMPLATES
-- =============================================================================

CREATE TABLE request_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jurisdiction TEXT NOT NULL,
    record_type TEXT,                   -- general, police_records, emails, contracts, etc.
    template_name TEXT NOT NULL,
    template_text TEXT NOT NULL,        -- with {{placeholders}}
    fee_waiver_language TEXT,
    expedited_language TEXT,
    appeal_template TEXT,              -- template for appeal letters
    notes TEXT,
    source TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_templates_jurisdiction ON request_templates(jurisdiction);
CREATE INDEX idx_templates_record_type ON request_templates(record_type);

-- =============================================================================
-- REQUEST LIFECYCLE (forward-compatible, wired later with auth)
-- =============================================================================

-- Campaigns group related requests
CREATE TABLE campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,                       -- nullable until auth exists
    title TEXT NOT NULL,
    description TEXT,
    record_type TEXT,
    date_range_start TEXT,
    date_range_end TEXT,
    status TEXT DEFAULT 'active',      -- active, completed, abandoned
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_campaigns_user ON campaigns(user_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);

-- Individual requests
CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    user_id TEXT,
    agency_id INTEGER NOT NULL,
    jurisdiction TEXT NOT NULL,
    status TEXT DEFAULT 'draft',        -- see state machine in PROJECT-SPEC.md §6
    request_text TEXT,
    submission_method TEXT,
    submitted_at TEXT,
    acknowledged_at TEXT,
    due_date TEXT,                      -- computed from response_rules
    extended_due_date TEXT,
    extension_reason TEXT,
    response_type TEXT,                -- full_grant, partial_grant, denial,
                                       -- no_responsive_records, fee_estimate
    response_received_at TEXT,
    response_summary TEXT,
    denial_exemptions TEXT,            -- JSON array of exemption IDs cited
    fee_quoted REAL,
    fee_paid REAL,
    fee_waiver_requested INTEGER DEFAULT 0,
    fee_waiver_granted INTEGER,
    appeal_deadline TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (agency_id) REFERENCES agencies(id)
);

CREATE INDEX idx_requests_campaign ON requests(campaign_id);
CREATE INDEX idx_requests_agency ON requests(agency_id);
CREATE INDEX idx_requests_status ON requests(status);
CREATE INDEX idx_requests_user ON requests(user_id);
CREATE INDEX idx_requests_due ON requests(due_date);
CREATE INDEX idx_requests_jurisdiction ON requests(jurisdiction);

-- Request event audit log
CREATE TABLE request_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,          -- status_change, fee_estimate, extension,
                                       -- response_received, appeal_filed, note
    old_value TEXT,
    new_value TEXT,
    details TEXT,                      -- JSON blob
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (request_id) REFERENCES requests(id)
);

CREATE INDEX idx_events_request ON request_events(request_id);
CREATE INDEX idx_events_type ON request_events(event_type);

-- Response document metadata (files stored on disk)
CREATE TABLE response_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    filename TEXT,
    file_path TEXT,
    file_size INTEGER,
    page_count INTEGER,
    content_type TEXT,
    description TEXT,
    received_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (request_id) REFERENCES requests(id)
);

CREATE INDEX idx_response_docs_request ON response_documents(request_id);

-- =============================================================================
-- AUTHORITY STATUS (derived, tracks current/superseded)
-- =============================================================================

CREATE TABLE authority_status (
    doc_id TEXT PRIMARY KEY,
    is_current INTEGER NOT NULL,
    latest_doc_id TEXT,
    superseded_by_doc_id TEXT,
    supersession_depth INTEGER DEFAULT 0,
    cited_by_count INTEGER DEFAULT 0,
    cites_count INTEGER DEFAULT 0,
    status_confidence TEXT DEFAULT 'derived',
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (doc_id) REFERENCES documents(id),
    FOREIGN KEY (latest_doc_id) REFERENCES documents(id),
    FOREIGN KEY (superseded_by_doc_id) REFERENCES documents(id)
);

CREATE INDEX idx_authority_status_current ON authority_status(is_current);
