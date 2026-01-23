from contextlib import contextmanager
from typing import Generator, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.event_tracker.db import init_db, get_conn
from src.event_tracker.schemas import EventCreate, EventOut
from src.event_tracker import crud

import sqlite3

app = FastAPI(title="Event Tracker", description="REST API for tracking timestamped events with filtering and export", version="0.1.0")

@app.on_event("startup")
def startup_event():
    """Initialize the database on startup"""
    init_db()

def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Dependency to get a database connection"""
    conn = get_conn()
    try:
        yield conn
    finally:
        conn.close()

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/events", response_model=EventOut, status_code=201)
def create_event(event: EventCreate, conn: sqlite3.Connection = Depends(get_db)):
    """Create a new event"""
    event_dict = crud.create_event(conn, event)
    return event_dict

@app.get("/events/{event_id}", response_model=EventOut)
def get_event(event_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Get an event by ID"""
    event = crud.get_event(conn, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Delete an event by ID"""
    deleted = crud.delete_event(conn, event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return None

@app.get("/events", response_model=dict)
def list_events(
    start: Optional[str] = None,
    end: Optional[str] = None,
    label: Optional[str] = None,
    min_x: Optional[float] = None,
    max_x: Optional[float] = None,
    min_y: Optional[float] = None,
    max_y: Optional[float] = None,
    limit: int = 50,
    offset: int = 0,
    conn: sqlite3.Connection = Depends(get_db)
):
    """List events with optional filtering and pagination"""
    total = crud.count_events(
        conn,
        start=start,
        end=end,
        label=label,
        min_x=min_x,
        max_x=max_x,
        min_y=min_y,
        max_y=max_y,
    )
    items = crud.list_events(
        conn,
        start=start,
        end=end,
        label=label,
        min_x=min_x,
        max_x=max_x,
        min_y=min_y,
        max_y=max_y,
        limit=limit,
        offset=offset
    )
    return{
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }