"""SQLite connection helpers for mixed service/CLI access.

The web app may hold the main DB in WAL mode under a different Unix user,
which can make the live -wal/-shm sidecars unreadable to CLI scripts.
For read-only commands, fall back to immutable mode.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3


def _db_uri(db_path: str | Path, immutable: bool = False) -> str:
    path = Path(db_path).resolve()
    suffix = "&immutable=1" if immutable else ""
    return f"file:{path}?mode=ro{suffix}"


def connect_readonly(db_path: str | Path, timeout: int = 30) -> sqlite3.Connection:
    """Open a read-only connection, falling back to immutable mode if needed."""
    try:
        conn = sqlite3.connect(_db_uri(db_path), uri=True, timeout=timeout)
        conn.execute("PRAGMA schema_version").fetchone()
    except sqlite3.OperationalError as exc:
        if "unable to open database file" not in str(exc).lower():
            raise
        conn = sqlite3.connect(_db_uri(db_path, immutable=True), uri=True, timeout=timeout)
    conn.execute("PRAGMA query_only = ON")
    return conn
