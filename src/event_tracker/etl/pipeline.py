from .extract import extract_csv
from .transform import transform_rows
from .validate import validate_raw_rows
from .load import load_clean_events, write_validation_report
from .metrics import summarize
from .what_if import run_what_if

def run_pipeline(input_csv: str, db_path: str, report_path: str, multipliers: dict | None = None) -> dict:
    raw = extract_csv(input_csv)
    validation = validate_raw_rows(raw)
    clean = transform_rows(raw)
    loaded = load_clean_events(db_path, clean)
    base = summarize(clean)
    scenario = run_what_if(clean, multipliers or {})
    write_validation_report(report_path, validation)
    return {"loaded_rows": loaded, "validation": validation["summary"], "what_if": scenario}