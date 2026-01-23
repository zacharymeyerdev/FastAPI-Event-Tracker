import sqlite3
from datetime import datetime
from typing import Optional, Any
from src.event_tracker.schemas import EventCreate

def create_event(conn: sqlite3.Connection, event_create: EventCreate) -> int:
    """Create a new event in the database and return its ID"""
    cursor = conn.cursor()

    ts_str = event_create.ts.isoformat()

    cursor.execute(
        """
        INSERT INTO events (ts, label, description, x, y, source)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ts_str, event_create.label, event_create.description, event_create.x, event_create.y, event_create.source
        )
    )
    conn.commit()
    event_id = cursor.lastrowid
    return get_event(conn, event_id)

def get_event(conn: sqlite3.Connection, event_id: int) -> Optional[dict]:
    """Fetch a single event by ID"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM events WHERE id = ?",
        (event_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def delete_event(conn: sqlite3.Connection, event_id: int) -> bool:
    """Delete an event by ID. Returns True if deleted, False if not found."""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM events WHERE id = ?",
        (event_id,)
    )
    conn.commit()
    return cursor.rowcount > 0
    
def list_events(
    conn: sqlite3.Connection,
    start: Optional[str] = None,
    end: Optional[str] = None,
    label: Optional[str] = None,
    min_x: Optional[float] = None,
    max_x: Optional[float] = None,
    min_y: Optional[float] = None,
    max_y: Optional[float] = None,
    limit: int = 50,
    offset: int = 0
) -> list[dict]:
    """List events with optional filtering and pagination"""
    cursor = conn.cursor()
    where_parts = ["1=1"]
    params: list[Any] = []

    if start:
        where_parts.append("ts >= ?")
        params.append(start)

    if end:
        where_parts.append("ts <= ?")
        params.append(end)

    if label:
        where_parts.append("label = ?")
        params.append(label)

    if min_x is not None:
        where_parts.append("x >= ?")
        params.append(min_x)

    if max_x is not None:
        where_parts.append("x <= ?")
        params.append(max_x)

    if min_y is not None:
        where_parts.append("y >= ?")
        params.append(min_y)

    if max_y is not None:
        where_parts.append("y <= ?")
        params.append(max_y)

    where_clause = " AND ".join(where_parts)

    params.append(limit)
    params.append(offset)

    query = f"""
        SELECT * FROM events
        WHERE {where_clause}
        ORDER BY ts DESC
        LIMIT ? OFFSET ?
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def count_events(
    conn: sqlite3.Connection,
    start: Optional[str] = None,
    end: Optional[str] = None,
    label: Optional[str] = None,
    min_x: Optional[float] = None,
    max_x: Optional[float] = None,
    min_y: Optional[float] = None,
    max_y: Optional[float] = None
) -> int:
    """Count total events matching the filters"""
    cursor = conn.cursor()
    where_parts = ["1=1"]
    params: list[Any] = []

    if start:
        where_parts.append("ts >= ?")
        params.append(start)

    if end:
        where_parts.append("ts <= ?")
        params.append(end)

    if label:
        where_parts.append("label = ?")
        params.append(label)

    if min_x is not None:
        where_parts.append("x >= ?")
        params.append(min_x)

    if max_x is not None:
        where_parts.append("x <= ?")
        params.append(max_x)

    if min_y is not None:
        where_parts.append("y >= ?")
        params.append(min_y)

    if max_y is not None:
        where_parts.append("y <= ?")
        params.append(max_y)

    where_clause = " AND ".join(where_parts)

    query = f"""
        SELECT COUNT(*) as count FROM events
        WHERE {where_clause}
    """

    cursor.execute(query, params)
    row = cursor.fetchone()
    return row["count"] if row else 0