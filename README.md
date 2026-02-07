# FastAPI-Event-Tracker

A simple REST API for recording and querying timestamped events with filtering and CSV export.

## Setup

1. Create a virtual environment:

    '''bash
    python -m venv venv
    .venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    pip install fastapi uvicorn pydantic
    '''

2. Run the server at 'http://127.0.0.1:8000':

    '''bash
    uvicorn src.event_tracker.main:app --reload
    '''

## Running Tests

    '''bash
    pip install pytest httpx
    pytest -q
    '''

## Project Structure

FastAPI-Event-Tracker/
├── src/
│   └── event_tracker/
│       ├── __init__.py          # Package marker
│       ├── main.py              # FastAPI app and HTTP routes
│       ├── schemas.py           # Pydantic models for validation
│       ├── db.py                # SQLite connection and initialization
│       ├── crud.py              # Database query functions
│       └── csv_export.py        # CSV conversion logic
├── tests/
│   ├── __init__.py
│   ├── test_health.py           # Health check endpoint tests
│   ├── test_events_crud.py      # Create/read/delete tests
│   ├── test_events_filters.py   # Filtering and pagination tests
│   └── test_events_export.py    # CSV export tests
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD pipeline
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Project metadata and dependencies
├── README.md                    # Documentation
├── LICENSE                      # License file
├── events.db                    # SQLite database
└── .venv/                       # Virtual environment
    
## API Usage

ISO Format: '2026-01-21T12:00:00'

**List events with filters:**
    '''bash
    GET /events?label=noted&start=2026-01-01T00:00:00&limit=10&offset=0
    '''

**Get one event:**
    '''bash
    GET /events/1
    '''

**Delete an event:**
    '''bash
    DELETE /events/1
    '''

**Export as CSV:**
    '''bash
    GET /events/export?label=note
    '''
