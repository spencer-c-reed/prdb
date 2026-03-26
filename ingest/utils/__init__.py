from .normalize import normalize_text, compute_hash, normalize_citation, extract_date
from .dedup import db_connect, document_exists, insert_document, upsert_document, log_ingestion, get_document_count
from .receipt import write_receipt
from .metadata import apply_metadata_defaults

# Lazy import: pdf_extract needs PyMuPDF (fitz) which isn't needed at web runtime
def __getattr__(name):
    if name in ('extract_text_from_pdf', 'extract_text_from_bytes'):
        from .pdf_extract import extract_text_from_pdf, extract_text_from_bytes
        globals()['extract_text_from_pdf'] = extract_text_from_pdf
        globals()['extract_text_from_bytes'] = extract_text_from_bytes
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
