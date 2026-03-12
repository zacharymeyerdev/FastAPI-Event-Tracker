# FastAPI Event Tracker + ETL

Lightweight project with:
- FastAPI endpoints for event CRUD, filtering, and CSV export
- Modular ETL pipeline for ingest, standardization, validation, and what-if analysis

Detailed runbook: [SOP.md](SOP.md)

## Quick Start

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -e .[dev]
```

3. Run the API:

```bash
uvicorn src.event_tracker.main:app --reload
```

## API Endpoints

- `GET /health`
- `POST /events`
- `GET /events`
- `GET /events/{event_id}`
- `DELETE /events/{event_id}`
- `GET /events/export`

## ETL Pipeline

Baseline run:

```bash
python -m src.event_tracker.etl.cli --input-csv data/input/events.csv --db-path data/output/etl_events.db --report-path data/output/validation_report.json --multipliers-json "{}"
```

What-if scenario run:

```bash
python -m src.event_tracker.etl.cli --input-csv data/input/events.csv --db-path data/output/etl_events.db --report-path data/output/validation_report_scenario.json --multipliers-json "{\"damage\":1.10,\"corrosion\":0.95}"
```

## ETL Outputs

- Clean rows in SQLite table `etl_events`
- Validation report JSON with:
  - `missing_values`
  - `duplicates`
  - `schema_mismatches`
  - `out_of_range`
  - summary counts
- What-if comparison with:
  - baseline metrics
  - scenario metrics
  - `delta_total`
  - `delta_pct`

## Tests

```bash
pytest -q
```
