"""Standardized JSON receipt for script runs.

Each script calls write_receipt() at the end of its run. The receipt is written
to logs/receipts/{script}_{timestamp}.json and a single JSONL line is appended
to logs/receipts/all.jsonl for easy tailing.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

RECEIPT_DIR = Path(__file__).resolve().parents[2] / "logs" / "receipts"


def write_receipt(
    *,
    script: str | None = None,
    status: str = "ok",
    added: int = 0,
    skipped: int = 0,
    errors: int = 0,
    elapsed_s: float | None = None,
    extras: dict | None = None,
) -> Path:
    """Write a JSON receipt and return the path."""
    if script is None:
        script = os.path.splitext(os.path.basename(sys.argv[0]))[0] if sys.argv else "unknown"

    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%dT%H%M%SZ")

    receipt = {
        "script": script,
        "ts": now.isoformat(),
        "status": status,
        "added": added,
        "skipped": skipped,
        "errors": errors,
    }
    if elapsed_s is not None:
        receipt["elapsed_s"] = round(elapsed_s, 1)
    if extras:
        receipt.update(extras)

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    # Individual receipt file
    path = RECEIPT_DIR / f"{script}_{ts}.json"
    path.write_text(json.dumps(receipt, indent=2) + "\n")

    # Append to combined JSONL
    jsonl_path = RECEIPT_DIR / "all.jsonl"
    with open(jsonl_path, "a") as f:
        f.write(json.dumps(receipt) + "\n")

    # Emit stdout marker for cron wrappers
    print("RECEIPT_JSON:" + json.dumps(receipt, ensure_ascii=True, sort_keys=True), flush=True)

    return path
