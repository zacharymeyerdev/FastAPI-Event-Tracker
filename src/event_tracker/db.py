import os
import sqlite3
from pathlib import Path

def get_db_path() -> str:
    """Get database file path from env var or default to project root"""
    if "EVENTS_DB_PATH" in os.environ:
        return os.environ["EVENTS_DB_PATH"]
    return str(Path(__file__).parent.parent.parent / "events.db")

def get_conn() -> sqlite3.Connection:
    """Get a new database connection"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize database schema if not already created"""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            label TEXT NOT NULL,
            description TEXT,
            x REAL,
            y REAL,
            source TEXT
        )
        """
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_events_ts ON events (ts)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_events_label ON events (label)"
    )

    conn.commit()
    conn.close()